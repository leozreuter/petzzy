from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.infra.erros import ValidationError
from .atendimentos import Atendimento

STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"

class Prontuario(db.Model):
    __tablename__ = "prontuarios"
    __table_args__ = {'schema': 'public'}
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    anamnese = db.Column(db.String(255), nullable=False)
    exame_fisico = db.Column(db.String(255))
    suspeita_diagnostica = db.Column(db.String(255))
    diagnostico_final = db.Column(db.String(255))
    tratamento_prescrito = db.Column(db.String(255))
    obs_retorno = db.Column(db.String(255))
    id_atendimento = db.Column(UUID(as_uuid=True), ForeignKey("atendimentos.id"), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_ATIVO)
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    atendimento_fk = relationship("Atendimento", back_populates="prontuarios")

    @classmethod
    def procuraPeloID(cls, id):
        prontuario = cls.query.filter_by(id=id).first()
        if not prontuario:
            raise ValidationError(message=f"Prontuário com ID '{id}' não encontrado.")
        return prontuario

    @classmethod
    def criarProntuario(cls, props):
        id_atendimento = props.get("id_atendimento")
        anamnese = props.get("anamnese")

        if not id_atendimento or not anamnese:
            raise ValidationError(message="'id_atendimento' and 'anamnese' are required fields.")

        Atendimento.procuraPeloID(id_atendimento)
        
        novo_prontuario = cls(
            id_atendimento=id_atendimento,
            anamnese=anamnese.strip(),
            exame_fisico=props.get("exame_fisico"),
            suspeita_diagnostica=props.get("suspeita_diagnostica"),
            diagnostico_final=props.get("diagnostico_final"),
            tratamento_prescrito=props.get("tratamento_prescrito"),
            obs_retorno=props.get("obs_retorno")
        )
        db.session.add(novo_prontuario)
        db.session.commit()
        return novo_prontuario
        
    def ativarProntuario(self):
        if self.status == STATUS_ATIVO:
            raise ValidationError(message="O prontuário já está ativo.")
        self.status = STATUS_ATIVO
        db.session.commit()

    def inativarProntuario(self):
        if self.status == STATUS_INATIVO:
            raise ValidationError(message="O prontuário já está inativo.")
        self.status = STATUS_INATIVO
        db.session.commit()

    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "id_atendimento": str(self.id_atendimento),
            "anamnese": self.anamnese,
            "exame_fisico": self.exame_fisico,
            "suspeita_diagnostica": self.suspeita_diagnostica,
            "diagnostico_final": self.diagnostico_final,
            "tratamento_prescrito": self.tratamento_prescrito,
            "obs_retorno": self.obs_retorno,
            "status": self.status
        }

    @staticmethod
    def listaProntuarios():
        prontuarios = Prontuario.query.all()
        return [p.retornaDicionario() for p in prontuarios]