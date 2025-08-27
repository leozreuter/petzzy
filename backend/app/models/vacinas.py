from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infra.erros import ValidationError
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Vacina(db.Model):
    __tablename__ = "vacinas"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    nome_vacina = db.Column(db.String(100), nullable=False,)
    data_aplicacao = db.Column(db.Date, nullable=False)
    data_proxima_dose = db.Column(db.Date)
    lote = db.Column(db.String(50))
    
    id_pet = db.Column(UUID(as_uuid=True), ForeignKey("pets.id"), nullable=False)
    id_veterinario = db.Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)

    veterinario_fk  = relationship("Usuario", back_populates="vacinas")
    pet_fk          = relationship("Pet", back_populates="vacinas")