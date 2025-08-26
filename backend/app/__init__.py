from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate(directory="app/infra/migrations")

API_VERSION = os.environ.get("API_VERSION") or "v1"

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints
    from .pages.home.index import bp as home_bp
    from .pages.user.index import bp as user_bp

    # Register blueprint
    app.register_blueprint(home_bp, url_prefix=f'/api/{API_VERSION}/home')
    app.register_blueprint(user_bp, url_prefix=f'/api/{API_VERSION}/user')

    return app
