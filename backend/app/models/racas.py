from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Raca(db.Model):
    __tablename__ = "racas"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    id_especie = db.Column(UUID(as_uuid=True), ForeignKey("especies.id"), nullable=False)
    desc = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ativo")
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    especie_fk = relationship("Especie", back_populates="racas")
    pets = relationship("Pet", back_populates="raca_fk")