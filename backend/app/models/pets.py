from .. import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.infra.erros import ValidationError
import uuid
from datetime import datetime

from .usuarios import Usuario
from .racas import Raca

STATUS_ATIVO = "ativo"
STATUS_INATIVO = "inativo"

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
    
    @classmethod
    def procuraPeloID(cls, id):
        pet = cls.query.filter_by(id=id).first()
        if not pet:
            raise ValidationError(
                message=f"Pet com ID '{id}' não encontrado.",
                action="Verifique o ID fornecido e tente novamente."
            )
        return pet

    @classmethod
    def criarPet(cls, props):
        nome = props.get("nome")
        id_tutor = props.get("id_tutor")
        id_raca = props.get("id_raca")
        
        if not all([nome, id_tutor, id_raca]):
            raise ValidationError(
                message="Campos obrigatórios ausentes.",
                action="Forneça 'nome', 'id_tutor' e 'id_raca' para criar um pet."
            )
            
        Usuario.verificaID(id_tutor)
        Raca.procuraPeloID(id_raca)

        novo_pet = cls(
            nome=nome.strip(),
            data_nascimento=props.get("data_nascimento"),
            sexo=props.get("sexo"),
            cor=props.get("cor"),
            obs=props.get("obs"),
            id_tutor=id_tutor,
            id_raca=id_raca
        )
        
        db.session.add(novo_pet)
        db.session.commit()
        return novo_pet

    def atualizarPet(self, props):
        self.nome = props.get('nome', self.nome).strip()
        self.data_nascimento = props.get('data_nascimento', self.data_nascimento)
        self.sexo = props.get('sexo', self.sexo)
        self.cor = props.get('cor', self.cor)
        self.obs = props.get('obs', self.obs)
        
        if 'id_raca' in props:
            Raca.procuraPeloID(props['id_raca'])
            self.id_raca = props['id_raca']
        if 'id_tutor' in props:
            Usuario.verificaID(props['id_tutor'])
            self.id_tutor = props['id_tutor']
            
        self.dthr_alt = datetime.now() 
        db.session.commit()
        return self

    def ativarPet(self):
        if self.status == STATUS_ATIVO:
            raise ValidationError(
                message="O pet já está ativo.",
                action="Nenhuma ação necessária."
            )
        self.status = STATUS_ATIVO
        db.session.commit()

    def inativarPet(self):
        if self.status == STATUS_INATIVO:
            raise ValidationError(
                message="O pet já está inativo.",
                action="Nenhuma ação necessária."
            )
        self.status = STATUS_INATIVO
        db.session.commit()
        
    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "sexo": self.sexo,
            "cor": self.cor,
            "obs": self.obs,
            "id_raca": str(self.id_raca),
            "raca": self.raca_fk.nome if self.raca_fk else None, 
            "especie": self.raca_fk.especie_fk.nome if self.raca_fk else None,
            "tutor": self.tutor_fk.nome if self.tutor_fk else None, 
            "dthr_alt": self.dthr_alt.isoformat(),
            "dthr_ins": self.dthr_ins.isoformat()
        }

    @staticmethod
    def listaPets(user):
        pets = Pet.query.filter_by(id_tutor=user.id).all()
        return [pet.retornaDicionario() for pet in pets]