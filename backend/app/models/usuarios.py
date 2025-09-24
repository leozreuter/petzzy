from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from datetime import datetime, timedelta
import bcrypt
import jwt

from app.infra.erros import ValidationError
from .perfis import Perfil
from .clinicas import Clinica

STATUS_ATIVO = 'ativo'
STATUS_INATIVO = 'inativo'

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
    
    #Validações
  
    #Metodo para verificar a senha
    def verificaSenha(self, senhaInserida) -> bool:
        hashedSenhaInserida = bcrypt.hashpw(senhaInserida.encode("utf-8"), self.salt.encode("utf-8"))
        if hashedSenhaInserida.decode("utf-8")==self.senha:
            return True
        return False

    
    def gerarToken(self, expires_in=60*60*24*30):
        payload = {
            "user_id": str(self.id),
            "exp": datetime.now() + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, "KEY", algorithm="HS256"),payload.get("exp")

    @classmethod
    def verificaEmail(self, email: str):
        return self.query.filter_by(email=email).first()
    
    @classmethod
    def verificaID(self, id):
        return self.query.filter_by(id=id).first()
    
    @classmethod
    def verificaID(cls, id):
        usuario = cls.query.filter_by(id=id).first()
        if not usuario:
            raise ValidationError(
                message=f"Usuário com ID '{id}' não encontrado.",
                action="Verifique se o ID fornecido está correto."
            )
        return usuario
    
    #CRUD
  
    def criarUsuario(props):
        email=props.get("email").lower().strip()
        nome=props.get("nome").lower().strip()
        senha=props.get("senha").encode('utf-8')
        id_perfil=props.get("id_perfil")
        telefone=props.get("telefone")
        crmv=props.get("crmv")
        id_clinica=props.get("id_clinica")
        
        if Usuario.verificaEmail(email):
            raise ValidationError(message="O email informado já está em uso",
                                  action="Utilize outro email para realizar o cadastro.")

        Perfil.procuraPeloID(id_perfil)
        

        if id_clinica:
            Clinica.procuraPeloID(id_clinica)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(senha, salt)

        usuario = Usuario(
            email=email,
            nome=nome,
            id_perfil=id_perfil,
            senha=hashed_password.decode('utf-8'),
            salt=salt.decode('utf-8'),
            telefone=telefone,
            id_clinica=id_clinica,
            crmv=crmv
        )
        db.session.add(usuario)
        db.session.commit()
       
        return usuario
  
    def ativarUsuario(self):
        if not self.status != STATUS_ATIVO:
            raise ValidationError(message="O cliente já está ativo!",
                                  action="qualquer merda.")
        self.status = STATUS_ATIVO
        db.session.commit()
        
    def inativarUsuario(self):
        if not self.status != STATUS_INATIVO:
            raise ValidationError(message="O cliente já está inativo!",
                                  action="qualquer merda.")
            
        self.status = STATUS_INATIVO
        db.session.commit()
         
    def retornaDicionario(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "nome": self.nome,
            "id_perfil": self.id_perfil,
            "senha": self.senha,
            "telefone": self.telefone,
            "id_clinica": self.id_clinica,
            "crmv": self.crmv,
            "dthr_ins": self.dthr_ins,
            "status": self.status
        }

    @staticmethod
    def listaUsuarios():
        usuarios = Usuario.query.all()
        lista_usuarios=[]
        for user in usuarios:
            lista_usuarios.append(user.retornaDicionario())
        return lista_usuarios
    
    