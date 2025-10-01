# app/models/atendimentos.py

import uuid
from datetime import datetime, timedelta
from urllib.parse import quote_plus

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from flask_mail import Message

# Importações do seu projeto
from .. import db  # <-- ALTERAÇÃO 1: Removi a importação do 'mail' daqui
from app.infra.erros import ValidationError
from .pets import Pet
from .usuarios import Usuario
from .clinicas import Clinica

STATUS_AGENDADO = "agendado"
STATUS_REALIZADO = "realizado"
STATUS_CANCELADO = "cancelado"

# --- FUNÇÃO AUXILIAR PARA CRIAR O LINK DA AGENDA ---
def gerar_link_google_calendar(atendimento, pet, clinica, veterinario):
    """Gera um link dinâmico para adicionar o evento ao Google Calendar."""
    base_url = "https://www.google.com/calendar/render?action=TEMPLATE"
    
    # Formato de data/hora para o Google: YYYYMMDDTHHMMSSZ
    start_time = atendimento.dthr_atendimento.strftime('%Y%m%dT%H%M%S')
    end_time = (atendimento.dthr_atendimento + timedelta(hours=1)).strftime('%Y%m%dT%H%M%S')
    
    params = {
        'text': quote_plus(f'Atendimento Petzzy: {pet.nome}'),
        'dates': f'{start_time}/{end_time}',
        'details': quote_plus(f'Consulta para {pet.nome}.\nMotivo: {atendimento.motivo}\nVeterinário(a): {veterinario.nome}'),
        'location': quote_plus(clinica.nome_fantasia)
    }
    
    return f"{base_url}&{'&'.join([f'{key}={value}' for key, value in params.items()])}"


class Atendimento(db.Model):
    __tablename__ = "atendimentos"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    dthr_atendimento = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    id_pet = db.Column(UUID(as_uuid=True), db.ForeignKey("pets.id"), nullable=False) 
    id_veterinario = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False)
    id_clinica = db.Column(UUID(as_uuid=True), db.ForeignKey("clinicas.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_AGENDADO)
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    pet_fk = relationship("Pet", back_populates="atendimentos")
    veterinario_fk = relationship("Usuario", back_populates="atendimentos")
    clinica_fk = relationship("Clinica", back_populates="atendimentos")
    prontuarios = relationship("Prontuario", back_populates="atendimento_fk")

    @classmethod
    def procuraPeloID(cls, id):
        atendimento = cls.query.filter_by(id=id).first()
        if not atendimento:
            raise ValidationError(message=f"Atendimento com ID '{id}' não encontrado.")
        return atendimento

    @classmethod
    def criarAtendimento(cls, user, props):
        from .. import mail  
        
        id_pet = props.get("id_pet")
        id_veterinario = props.get("id_veterinario")
        id_clinica = props.get("id_clinica")
        
        if not all([id_pet, id_veterinario, id_clinica, props.get("dthr_atendimento"), props.get("motivo")]):
            raise ValidationError(message="Campos obrigatórios ausentes para agendar o atendimento.")
        
        pet = Pet.procuraPeloID(id_pet)
        veterinario = Usuario.procuraPeloID(id_veterinario)
        clinica = Clinica.procuraPeloID(id_clinica)
       
        Pet.validaTutor(user.id,id_pet)

        novo_atendimento = cls(
            id_pet=id_pet,
            id_veterinario=id_veterinario,
            id_clinica=id_clinica,
            dthr_atendimento=datetime.fromisoformat(props.get("dthr_atendimento")),
            motivo=props.get("motivo").strip()
        )
        
        db.session.add(novo_atendimento)
        db.session.commit() # Salva no banco primeiro

        try:
            link_agenda = gerar_link_google_calendar(novo_atendimento, pet, clinica, veterinario)
            
            html_body = f"""
            <h3>Olá, {veterinario.nome}!</h3>
            <p>Um novo atendimento foi agendado para você na plataforma Petzzy.</p>
            <ul>
                <li><strong>Paciente:</strong> {pet.nome}</li>
                <li><strong>Clínica:</strong> {clinica.nome_fantasia}</li>
                <li><strong>Data e Hora:</strong> {novo_atendimento.dthr_atendimento.strftime('%d/%m/%Y às %H:%M')}</li>
                <li><strong>Motivo:</strong> {novo_atendimento.motivo}</li>
            </ul>
            <p>Clique no botão abaixo para adicionar este evento à sua agenda.</p>
            <a href="{link_agenda}" style="background-color: #34a853; color: white; padding: 12px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; font-weight: bold;">
                Adicionar ao Google Calendar
            </a>
            """
            
            msg = Message(
                subject="Novo Atendimento Agendado - Petzzy",
                sender="noreply@petzzy.com",
                recipients=[veterinario.email],
                html=html_body
            )
            
            mail.send(msg)
            print(f"E-mail de agendamento enviado para {veterinario.email} via Mailtrap.")
        except Exception as e:
            # Se o envio de e-mail falhar, o sistema não quebra a aplicação.
            # Apenas registra o erro no console.
            print(f"ERRO AO ENVIAR E-MAIL DE AGENDAMENTO: {e}")
        # --- FIM DA LÓGICA DE E-MAIL ---
        
        return novo_atendimento

    def realizarAtendimento(self):
        if self.status != STATUS_AGENDADO:
            raise ValidationError(message="Apenas atendimentos agendados podem ser marcados como realizados.")
        self.status = STATUS_REALIZADO
        db.session.commit()
    
    def cancelarAtendimento(self):
        if self.status == STATUS_CANCELADO:
            raise ValidationError(message="Este atendimento já está cancelado.")
        self.status = STATUS_CANCELADO
        db.session.commit()

    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "id_pet": str(self.id_pet),
            "id_veterinario": str(self.id_veterinario),
            "id_clinica": str(self.id_clinica),
            "clinica": str(self.clinica_fk.nome_fantasia),
            "dthr_atendimento": self.dthr_atendimento.isoformat(),
            "motivo": self.motivo,
            "status": self.status
        }
    
    @staticmethod
    def listaAtendimentos():
        atendimentos = Atendimento.query.all()
        return [a.retornaDicionario() for a in atendimentos]
        
    @staticmethod
    def listaAtendimentosPorIdUsuario(userID):
        atendimentos = Atendimento.query.join(Atendimento.pet_fk)\
        .filter(Pet.id_tutor == userID).all()
        return [a.retornaDicionario() for a in atendimentos]