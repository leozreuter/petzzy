import os
from app.infra.scripts import services
import dotenv

class Config():

    if os.environ.get("FLASK_ENV") == "production":
        print("\nRODANDO EM PRODUÇAO\n")
        dotenv.load_dotenv(".env.production")
    else:
        print("\nRODANDO EM DESENVOLVIMENTO\n")
        dotenv.load_dotenv(".env.development")
        services.up()

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
