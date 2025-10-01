from flask import Flask, current_app, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_mail import Mail


import app.infra.erros as Errors

db = SQLAlchemy()
mail = Mail()
migrate = Migrate(directory="app/infra/migrations")

API_VERSION = os.environ.get("API_VERSION") or "v1"

def create_app():
    app = Flask(__name__)
    
    app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '4eb77c18802746'
    app.config['MAIL_PASSWORD'] = '2fe2057256eb0a' 
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@petzzy.com'
    
    CORS(app, resources={r"*": {"origins": "*"}})

    app.config.from_object("config.Config")

    CORS(app)
   
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(Exception)
    def onErrorHandler(error):
        internal_error = Errors.InternalServerError(cause=error)
        return jsonify(internal_error.to_dict()), internal_error.status_code

    # Import blueprints
    from .pages.agenda.index import bp as agenda_bp
    app.register_blueprint(agenda_bp, url_prefix=f'/api/{API_VERSION}/agenda')

    from .pages.atendimento.index import bp as atendimento_bp
    app.register_blueprint(atendimento_bp, url_prefix=f'/api/{API_VERSION}/atendimento')

    from .pages.clinica.index import bp as clinica_bp
    app.register_blueprint(clinica_bp, url_prefix=f'/api/{API_VERSION}/clinica')

    from .pages.especie.index import bp as especie_bp
    app.register_blueprint(especie_bp, url_prefix=f'/api/{API_VERSION}/especie')

    from .pages.home.index import bp as home_bp
    app.register_blueprint(home_bp, url_prefix=f'/api/{API_VERSION}/home')

    from .pages.perfil.index import bp as perfil_bp
    app.register_blueprint(perfil_bp, url_prefix=f'/api/{API_VERSION}/perfil')

    from .pages.pet.index import bp as pet_bp
    app.register_blueprint(pet_bp, url_prefix=f'/api/{API_VERSION}/pet')
    app.register_blueprint(clinica_bp, url_prefix=f'/api/{API_VERSION}/clinica')
    app.register_blueprint(atendimento_bp, url_prefix=f'/api/{API_VERSION}/atendimento')


    from .pages.prontuario.index import bp as prontuario_bp
    app.register_blueprint(prontuario_bp, url_prefix=f'/api/{API_VERSION}/protuario')

    from .pages.raca.index import bp as raca_bp
    app.register_blueprint(raca_bp, url_prefix=f'/api/{API_VERSION}/raca')

    from .pages.user.index import bp as user_bp
    app.register_blueprint(user_bp, url_prefix=f'/api/{API_VERSION}/user')

    from .pages.vacina.index import bp as vacina_bp
    app.register_blueprint(vacina_bp, url_prefix=f'/api/{API_VERSION}/vacina')

    return app
