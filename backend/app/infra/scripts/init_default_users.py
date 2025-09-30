from app.models.perfis import Perfil
from app.models.usuarios import Usuario
from app.models.especies import Especie
from app.models.racas import Raca
from app import db
import bcrypt

def create_default_users():
    # Lista de perfis que queremos criar
    perfis_padrao = ["Administrador", "Usuario", "Veterinario"]
    especies_padrao = ["Cachorro", "Gato"]
    raca_cachorro = ["Pinscher","Golden","Pitbull","Labrador","Indefinido"]
    raca_gato = ["Frajolha","Persa","Siames","Indefinido"]
    perfis_obj = {}

    # Cria perfis se não existirem
    for desc in perfis_padrao:
        perfil = Perfil.query.filter_by(desc=desc).first()
        if not perfil:
            perfil = Perfil(desc=desc)
            db.session.add(perfil)
            try:
                db.session.commit()
                print(f"Criado Perfil {desc.upper()}")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao criar Perfil {desc}: {e}")
        perfis_obj[desc] = perfil

    # Cria usuário ADMIN se não existir
    if not Usuario.verificaEmail("admin@petzzy.com"):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw("admin".encode('utf-8'), salt)
        usuario = Usuario(
            nome="admin",
            email="admin@petzzy.com",
            id_perfil=perfis_obj["Administrador"].id,
            senha=hashed_password.decode('utf-8'),
            salt=salt.decode('utf-8'),
        )
        db.session.add(usuario)
        try:
            db.session.commit()
            print("Criado usuário ADMIN")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar usuário ADMIN: {e}")

    if not Usuario.verificaEmail("veterinario@petzzy.com"):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw("veterinario".encode('utf-8'), salt)
        usuario = Usuario(
            nome="Veterinário",
            email="veterinario@petzzy.com",
            id_perfil=perfis_obj["Veterinario"].id,
            senha=hashed_password.decode('utf-8'),
            salt=salt.decode('utf-8'),
        )
        db.session.add(usuario)
        try:
            db.session.commit()
            print("Criado usuário Veterinario")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar usuário Veterinario: {e}")

    for nome_esp in especies_padrao:
        especie = Especie.query.filter_by(nome=nome_esp).first()
        if not especie:
            especie = Especie(nome=nome_esp)
            db.session.add(especie)
            try:
                db.session.commit()
                print(f"Criado Especie {nome_esp.upper()}")
                if nome_esp == "Cachorro":
                    for nome_raca in raca_cachorro:
                        raca = Raca.query.filter_by(nome=nome_raca).first()
                        if not raca:
                            perfil = Raca(
                                nome=nome_raca,
                                id_especie=especie.id
                                )
                            db.session.add(perfil)
                            try:
                                db.session.commit()
                                print(f"Criado Raca {nome_raca.upper()}")
                            except Exception as e:
                                db.session.rollback()
                                print(f"Erro ao criar Raca {nome_raca}: {e}")

                if nome_esp == "Gato":
                    for nome_raca in raca_gato:
                        raca = Raca.query.filter_by(nome=nome_raca).first()
                        if not raca:
                            perfil = Raca(
                                nome=nome_raca,
                                id_especie=especie.id
                                )
                            db.session.add(perfil)
                            try:
                                db.session.commit()
                                print(f"Criado Raca {nome_raca.upper()}")
                            except Exception as e:
                                db.session.rollback()
                                print(f"Erro ao criar Raca {nome_raca}: {e}")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao criar Especie {nome_esp}: {e}")