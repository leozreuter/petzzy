from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Perfil(db.Model):
    __tablename__ = "perfis"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    desc = db.Column(db.String, nullable=False)
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    usuarios = relationship("Usuario", back_populates="perfil_fk")