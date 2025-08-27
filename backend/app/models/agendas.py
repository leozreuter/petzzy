from .. import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Agenda(db.Model):
    __tablename__ = "agendas"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    dia_semana = db.Column(ARRAY(Integer))
    hora_inicio = db.Column(db.DateTime)
    hora_fim = db.Column(db.DateTime)
    status = db.Column(db.String(20), nullable=False, default="ativo")
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    id_veterinario = db.Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    id_clinica = db.Column(UUID(as_uuid=True), ForeignKey("clinicas.id"), nullable=False)
    
    usuario_fk = relationship("Usuario", back_populates="agendas")
    clinica_fk = relationship("Clinica", back_populates="agendas")

