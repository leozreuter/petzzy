from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Pet(db.Model):
    __tablename__ = "pets"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.DateTime)
    sexo = db.Column(db.String(1))
    cor = db.Column(db.String(50))
    obs = db.Column(db.String(255))
    id_raca = db.Column(UUID(as_uuid=True), ForeignKey("racas.id"), nullable=False)
    id_tutor = db.Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ativo")
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    tutor_fk = relationship("Usuario", back_populates="pets")
    raca_fk = relationship("Raca", back_populates="pets")
    
    atendimentos = relationship("Atendimento", back_populates="pet_fk")
    vacinas      = relationship("Vacina", back_populates="pet_fk") 