from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.infra.erros import ValidationError
from .pets import Pet
from .usuarios import Usuario
from .clinicas import Clinica

STATUS_AGENDADO = "agendado"
STATUS_REALIZADO = "realizado"
STATUS_CANCELADO = "cancelado"

class Atendimento(db.Model):
    __tablename__ = "atendimentos"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    dthr_atendimento = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    id_pet = db.Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False) 
    id_veterinario = db.Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    id_clinica = db.Column(UUID(as_uuid=True), ForeignKey("clinicas.id"), nullable=False)
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
        id_pet = props.get("id_pet")
        id_veterinario = props.get("id_veterinario")
        id_clinica = props.get("id_clinica")
        
        if not all([id_pet, id_veterinario, id_clinica, props.get("dthr_atendimento"), props.get("motivo")]):
            raise ValidationError(message="Campos obrigatórios ausentes para agendar o atendimento.")
        

        Pet.procuraPeloID(id_pet)
        #Usuario.procuraPeloID(id_veterinario)
        Clinica.procuraPeloID(id_clinica)
        Pet.validaTutor(user.id,id_pet)

        novo_atendimento = cls(
            id_pet=id_pet,
            id_veterinario=id_veterinario,
            id_clinica=id_clinica,
            dthr_atendimento=props.get("dthr_atendimento"),
            motivo=props.get("motivo").strip()
        )
        db.session.add(novo_atendimento)
        db.session.commit()
        return novo_atendimento

    def realizarAtendimento(self):
        if self.status != STATUS_AGENDADO:
            raise ValidationError(message=f"Apenas atendimentos agendados podem ser marcados como realizados.")
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