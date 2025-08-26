from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.infra.erros import ValidationError
from datetime import datetime
import bcrypt

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False,)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    salt = db.Column(db.String, nullable=False)
    idperfil = db.Column(db.String, nullable=False)
    dthr_alt = db.Column(db.DateTime, nullable=False, default=datetime.now)
    dthr_ins = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def create(props):
        email=props.get("email").lower()
        User.validadeEmail(email)

        name=props.get("name")
        password=props.get("password").encode('utf-8')
        idperfil=props.get("idperfil")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)

        user = User(
            email=email,
            name=name,
            idperfil=idperfil,
            password=hashed_password.decode('utf-8'),
            salt=salt.decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        return user
            
    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "name": self.name,
            "idperfil": self.idperfil,
            "password": self.password,
            "dthr_ins": self.dthr_ins
        }
    
    @staticmethod
    def validadeEmail(email):
        
        result = User.query.filter_by(email=email).first()
        if result:
            raise ValidationError(message="O email informado já está em uso",
                                  action="Utilize outro email para realizar o cadastro.")