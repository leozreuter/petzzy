from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.infra.erros import ValidationError

STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"

class Clinica(db.Model):
    __tablename__ = "clinicas"
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    nome_fantasia = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    telefone_contato = db.Column(db.String(13))
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(6))
    bairro = db.Column(db.String(100))
    estado = db.Column(db.String(2))
    cidade = db.Column(db.String(100))
    cep = db.Column(db.String(8))
    status = db.Column(db.String(20), nullable=False, default=STATUS_ATIVO)
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    usuarios = relationship("Usuario", back_populates="clinica_fk")
    agendas = relationship("Agenda", back_populates="clinica_fk")
    atendimentos = relationship("Atendimento", back_populates="clinica_fk")

    @classmethod
    def procuraPeloID(cls, id):
        clinica = cls.query.filter_by(id=id).first()
        if not clinica:
            raise ValidationError(message=f"Clínica com ID '{id}' não encontrada.")
        return clinica

    @classmethod
    def verificaCnpjUnico(cls, cnpj):
        if cls.query.filter_by(cnpj=cnpj).first():
            raise ValidationError(message=f"O CNPJ '{cnpj}' já está em uso.")

    @classmethod
    def criarClinica(cls, props):
        nome_fantasia = props.get("nome_fantasia")
        cnpj = props.get("cnpj")

        if not nome_fantasia or not cnpj:
            raise ValidationError(message="'nome_fantasia' e 'cnpj' são campos obrigatórios.")
        
        cls.verificaCnpjUnico(cnpj)
        
        nova_clinica = cls(
            nome_fantasia=str(nome_fantasia.strip()).lower(),
            cnpj=cnpj,
            telefone_contato=props.get("telefone_contato"),
            logradouro=str(props.get("logradouro")).lower(),
            numero=props.get("numero"),
            bairro=str(props.get("bairro")).lower(),
            estado=props.get("estado"),
            cidade=str(props.get("cidade")).lower(),
            cep=props.get("cep")
        )
        db.session.add(nova_clinica)
        db.session.commit()
        return nova_clinica

    def ativarClinica(self):
        if self.status == STATUS_ATIVO:
            raise ValidationError(message="A clínica já está ativa.")
        self.status = STATUS_ATIVO
        db.session.commit()

    def inativarClinica(self):
        if self.status == STATUS_INATIVO:
            raise ValidationError(message="A clínica já está inativa.")
        self.status = STATUS_INATIVO
        db.session.commit()

    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "nome_fantasia": self.nome_fantasia,
            "cnpj": self.cnpj,
            "telefone_contato": self.telefone_contato,
            "logradouro": self.logradouro,
            "numero": self.numero,
            "bairro": self.bairro,
            "estado": self.estado,
            "cidade": self.cidade,
            "cep": self.cep,
            "status": self.status,
            "dthr_ins": self.dthr_ins.isoformat()
        }

    @staticmethod
    def listaClinicas():
        clinicas = Clinica.query.all()
        return [c.retornaDicionario() for c in clinicas]

    @staticmethod
    def listaVeterinarios(clinicaId):
        clinicas = Clinica.query.join(Clinica.pet_fk)\
        .filter(Pet.id_tutor == userID).all()
        return [c.retornaDicionario() for c in clinicas]