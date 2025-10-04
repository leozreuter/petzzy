from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from datetime import datetime

from app.infra.erros import NotFoundError

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Perfil(db.Model):
    __tablename__ = "perfis"
    __table_args__ = {'schema': 'public'}
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    desc = db.Column(db.String, nullable=False, unique=True)
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    usuarios = relationship("Usuario", back_populates="perfil_fk")

    @staticmethod
    def criar(props):

        desc = props.get("desc")

        perfil = Perfil(
            desc=desc
        )
        db.session.add(perfil)
        db.session.commit()
        return perfil

    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "email": self.desc,
            "dthr_ins": self.dthr_ins
        }

    def procuraPeloID(id):
        result = Perfil.query.filter_by(id=id).first()
        if not result:
            raise NotFoundError(message="O id do perfil informado não foi encontrado",
                                  action="Verifique se o perfil existe.")
        return result

    def procuraPeloNome(nome):
        result = Perfil.query.filter_by(desc=nome).first()
        if not result:
            raise NotFoundError(message="O id do perfil informado não foi encontrado",
                                  action="Verifique se o perfil existe.")
        return result