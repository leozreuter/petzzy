from app.models.perfis import Perfil
from app.models.usuarios import Usuario
from app import db
import bcrypt


def create_default_users():
    try:
        Perfil.procuraPeloNome("Administrador")
    except Exception as e: 
        perfil = Perfil(
                desc="Administrador"
            )
        db.session.add(perfil)
        db.session.commit()
        print("Criado Perfil ADMIN")
        
    try: 
        Usuario.verificaEmail("admin@petzzy.com")
    except Exception as e: 
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw("admin".encode('utf-8'), salt)

        usuario = Usuario(
            nome="admin",
            email="admin@petzzy.com",
            id_perfil=perfil.id,
            senha=hashed_password.decode('utf-8'),
            salt=salt.decode('utf-8'),
        )
        db.session.add(usuario)
        db.session.commit()
        print("Criado usuário ADMIN")

    try: 
        Perfil.procuraPeloNome("Usuário")
    except Exception as e: 
        perfilUsuario = Perfil(
                desc="Usuário"
            )
        db.session.add(perfilUsuario)
        db.session.commit()
        print("Criado Perfil USUARIO")
    try:
        Perfil.procuraPeloNome("Veterinário")
    except Exception as e:
        perfilVet = Perfil(
                desc="Veterinário"
            )
        db.session.add(perfil)
        db.session.commit()
        print("Criado Perfil VETERINARIO")

    except Exception as e:
        print(e)