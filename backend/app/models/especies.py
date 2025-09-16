from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.infra.erros import ValidationError

STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class Especie(db.Model):
    __tablename__ = "especies"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ativo")
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    racas = relationship("Raca", back_populates="especie_fk")
    
    @classmethod
    def procuraPeloID(cls, id):
        especie = cls.query.filter_by(id=id).first()
        if not especie:
            raise ValidationError(
                message=f"Espécie com ID '{id}' não encontrada.",
                action="Verifique o ID fornecido e tente novamente."
            )
        return especie
        
    @classmethod
    def verificaNomeUnico(cls, nome):
        return cls.query.filter_by(nome=nome).first()

    @classmethod
    def criarEspecie(cls, props):
        nome = props.get("nome")

        if not nome:
            raise ValidationError(
                message="O campo 'nome' é obrigatório.",
                action="Forneça o nome para criar a espécie."
            )
        
        nome_tratado = nome.strip().capitalize()

        if cls.verificaNomeUnico(nome_tratado):
            raise ValidationError(
                message=f"A espécie '{nome_tratado}' já está cadastrada.",
                action="Utilize outro nome."
            )

        nova_especie = cls(nome=nome_tratado)
        
        db.session.add(nova_especie)
        db.session.commit()
        return nova_especie

    def atualizarEspecie(self, props):
        nome_novo = props.get('nome', self.nome).strip().capitalize()
        
        especie_existente = self.verificaNomeUnico(nome_novo)
        if especie_existente and especie_existente.id != self.id:
            raise ValidationError(
                message=f"A espécie '{nome_novo}' já existe.",
                action="Escolha outro nome."
            )

        self.nome = nome_novo
        db.session.commit()
        return self

    def ativarEspecie(self):
        if self.status == STATUS_ATIVO:
            raise ValidationError(message="A espécie já está ativa.")
        self.status = STATUS_ATIVO
        db.session.commit()

    def inativarEspecie(self):
        if self.status == STATUS_INATIVO:
            raise ValidationError(message="A espécie já está inativa.")
        self.status = STATUS_INATIVO
        db.session.commit()
        
    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "status": self.status
        }

    @staticmethod
    def listaEspecies():
        especies = Especie.query.all()
        return [especie.retornaDicionario() for especie in especies]