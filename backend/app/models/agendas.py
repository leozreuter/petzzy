from .. import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, String, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.infra.erros import ValidationError
from .usuarios import Usuario
from .clinicas import Clinica

STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"

class Agenda(db.Model):
    __tablename__ = "agendas"
    __table_args__ = {'schema': 'public'}
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    dia_semana = db.Column(ARRAY(Integer)) # Ex: [1, 2, 3] para Seg, Ter, Qua
    hora_inicio = db.Column(Time)
    hora_fim = db.Column(Time)
    status = db.Column(db.String(20), nullable=False, default=STATUS_ATIVO)
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    id_veterinario = db.Column(UUID(as_uuid=True), ForeignKey("public.usuarios.id"), nullable=False)
    id_clinica = db.Column(UUID(as_uuid=True), ForeignKey("public.clinicas.id"), nullable=False)
    
    usuario_fk = relationship("Usuario", back_populates="agendas")
    clinica_fk = relationship("Clinica", back_populates="agendas")

    @classmethod
    def procuraPeloID(cls, id):
        agenda = cls.query.filter_by(id=id).first()
        if not agenda:
            raise ValidationError(message=f"Agenda com ID '{id}' não encontrada.")
        return agenda
        
    @classmethod
    def criarAgenda(cls, props):
        id_veterinario = props.get("id_veterinario")
        id_clinica = props.get("id_clinica")

        if not all([id_veterinario, id_clinica, props.get("dia_semana"), props.get("hora_inicio"), props.get("hora_fim")]):
            raise ValidationError(message="Campos obrigatórios ausentes para criar a agenda.")

        Usuario.procuraPeloID(id_veterinario)
        Clinica.procuraPeloID(id_clinica)

        nova_agenda = cls(
            id_veterinario=id_veterinario,
            id_clinica=id_clinica,
            dia_semana=props.get("dia_semana"),
            hora_inicio=props.get("hora_inicio"),
            hora_fim=props.get("hora_fim")
        )
        db.session.add(nova_agenda)
        db.session.commit()
        return nova_agenda

    def ativarAgenda(self):
        if self.status == STATUS_ATIVO:
            raise ValidationError(message="A agenda já está ativa.")
        self.status = STATUS_ATIVO
        db.session.commit()

    def inativarAgenda(self):
        if self.status == STATUS_INATIVO:
            raise ValidationError(message="A agenda já está inativa.")
        self.status = STATUS_INATIVO
        db.session.commit()

    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "id_veterinario": str(self.id_veterinario),
            "id_clinica": str(self.id_clinica),
            "dia_semana": self.dia_semana,
            "hora_inicio": self.hora_inicio.isoformat() if self.hora_inicio else None,
            "hora_fim": self.hora_fim.isoformat() if self.hora_fim else None,
            "status": self.status
        }
    
    @staticmethod
    def listaAgendas():
        agendas = Agenda.query.all()
        return [a.retornaDicionario() for a in agendas]