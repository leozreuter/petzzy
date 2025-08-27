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

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False,)
    nome = db.Column(db.String, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    salt = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String(13))
    crmv = db.Column(db.String(20))
    status = db.Column(db.String(20), nullable=False, default="ativo")
    id_perfil = db.Column(UUID(as_uuid=True), ForeignKey("perfis.id"), nullable=False)
    id_clinica = db.Column(UUID(as_uuid=True), ForeignKey("clinicas.id"))
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)

    perfil_fk = relationship("Perfil", back_populates="usuarios")
    clinica_fk = relationship("Clinica", back_populates="usuarios")
    
    agendas = relationship("Agenda", back_populates="usuario_fk")
    pets = relationship("Pet", back_populates="tutor_fk")
    atendimentos = relationship("Atendimento", back_populates="veterinario_fk")
    vacinas = relationship("Vacina", back_populates="veterinario_fk")
    
    @staticmethod
    def create(props):
        email=props.get("email").lower()
        Usuario.validadeEmail(email)

        nome=props.get("nome")
        senha=props.get("senha").encode('utf-8')
        idperfil=props.get("idperfil")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(senha, salt)

        usuario = Usuario(
            email=email,
            nome=nome,
            idperfil=idperfil,
            senha=hashed_password.decode('utf-8'),
            salt=salt.decode('utf-8')
        )
        db.session.add(usuario)
        db.session.commit()
        return usuario
            
    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "nome": self.nome,
            "idperfil": self.idperfil,
            "senha": self.senha,
            "dthr_ins": self.dthr_ins
        }
    
    @staticmethod
    def validadeEmail(email):
        
        result = Usuario.query.filter_by(email=email).first()
        if result:
            raise ValidationError(message="O email informado já está em uso",
                                  action="Utilize outro email para realizar o cadastro.")