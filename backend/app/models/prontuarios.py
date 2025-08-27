from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Prontuario(db.Model):
    __tablename__ = "prontuarios"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    amnese = db.Column(db.String(255), nullable=False)
    exame_fisico = db.Column(db.String(255))
    suspeita_diaginostica = db.Column(db.String(255))
    diagnostico_final = db.Column(db.String(255))
    tratamento_prescrito = db.Column(db.String(255))
    obs_retorno = db.Column(db.String(255))
    id_atendimento = db.Column(UUID(as_uuid=True), ForeignKey("atendimentos.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ativo")
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    atendimento_fk = relationship("Atendimento", back_populates="prontuarios")