from flask import Flask
import dotenv, os

dotenv.load_dotenv("../.env")
API_VERSION = os.environ.get("API_VERSION") or "v1"

def create_app():
    app = Flask(__name__)
    #app.config.from_object('config.Config')

    # Import blueprints
    from .pages.home.index import bp as home_bp

    # Register blueprint
    app.register_blueprint(home_bp, url_prefix=f'/api/{API_VERSION}/home')

    return app
