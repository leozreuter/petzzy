from flask.cli import FlaskGroup
from app import create_app

# python3 manage.py db migrate -m 'nome da migration'   -> criar migration
# python3 manage.py db upgrade                          -> rodar migrations

# Importar os models para o migrator identificar
from app.models.users import User

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
