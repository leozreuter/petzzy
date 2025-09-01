from app.models.perfis import Perfil
from app.models.usuarios import Usuario
from app import db
import bcrypt


def create_default_users():
    perfil = Perfil(
            desc="Administrador"
        )
    db.session.add(perfil)
    db.session.commit()
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw("admin".encode('utf-8'), salt)

    usuario = Usuario(
        nome="admin",
        email="admin",
        id_perfil=perfil.id,
        senha=hashed_password.decode('utf-8'),
        salt=salt.decode('utf-8'),
    )
    db.session.add(usuario)
    db.session.commit()