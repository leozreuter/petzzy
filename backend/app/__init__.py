from flask import Flask, current_app, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

import app.infra.erros as Errors

db = SQLAlchemy()
migrate = Migrate(directory="app/infra/migrations")

API_VERSION = os.environ.get("API_VERSION") or "v1"

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    app.config.from_object("config.Config")
    db.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(Exception)
    def onErrorHandler(error):
        internal_error = Errors.InternalServerError(cause=error)
        return jsonify(internal_error.to_dict()), internal_error.status_code

    # Import blueprints
    from .pages.home.index import bp as home_bp
    from .pages.user.index import bp as user_bp
    from .pages.perfil.index import bp as perfil_bp
    from .pages.raca.index import bp as raca_bp
    from .pages.especie.index import bp as especie_bp
    from .pages.pet.index import bp as pet_bp

    # Register blueprint
    app.register_blueprint(home_bp, url_prefix=f'/api/{API_VERSION}/home')
    app.register_blueprint(user_bp, url_prefix=f'/api/{API_VERSION}/user')
    app.register_blueprint(perfil_bp, url_prefix=f'/api/{API_VERSION}/perfil')
    app.register_blueprint(raca_bp, url_prefix=f'/api/{API_VERSION}/raca')
    app.register_blueprint(especie_bp, url_prefix=f'/api/{API_VERSION}/especie')
    app.register_blueprint(pet_bp, url_prefix=f'/api/{API_VERSION}/pet')

    return app
