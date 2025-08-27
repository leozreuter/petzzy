from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Clinica(db.Model):
    __tablename__ = "clinicas"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    nome_fantasia = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False)
    telefone_contato = db.Column(db.String(13))
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(6))
    bairro = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cidade = db.Column(db.String(100))
    cep = db.Column(db.String(8))
    status = db.Column(db.String(20), nullable=False, default="ativo")
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    usuarios = relationship("Usuario", back_populates="clinica_fk")
    agendas = relationship("Agenda", back_populates="clinica_fk")
    atendimentos = relationship("Atendimento", back_populates="clinica_fk")