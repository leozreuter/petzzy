from flask.cli import FlaskGroup
from app import create_app

# python3 manage.py db migrate -m 'nome da migration'   -> criar migration
# python3 manage.py db upgrade                          -> rodar migrations

# Importar os models para o migrator identificar
from app.models.agendas import Agenda
from app.models.atendimentos import Atendimento
from app.models.clinicas import Clinica
from app.models.especies import Especie
from app.models.perfis import Perfil
from app.models.pets import Pet
from app.models.prontuarios import Prontuario
from app.models.racas import Raca
from app.models.usuarios import Usuario
from app.models.vacinas import Vacina


app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
