from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Atendimento(db.Model):
    __tablename__ = "atendimentos"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    dthr_atendimento = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    id_pet = db.Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False) 
    id_veterinario = db.Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    id_clinica = db.Column(UUID(as_uuid=True), ForeignKey("clinicas.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="agendado")
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    pet_fk = relationship("Pet", back_populates="atendimentos")
    veterinario_fk = relationship("Usuario", back_populates="atendimentos")
    clinica_fk = relationship("Clinica", back_populates="atendimentos")
    
    prontuarios = relationship("Prontuario", back_populates="atendimento_fk")