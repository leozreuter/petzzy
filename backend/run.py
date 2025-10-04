from app import create_app
from flask_migrate import upgrade
from app.infra.scripts.wait_for_postgres import check_postgres
from app.infra.scripts.init_default_users import create_default_users
import os
from dotenv import load_dotenv

load_dotenv('.env.development')
load_dotenv('.env.production')

app = create_app()

if __name__ == "__main__":
    if os.environ.get("DEBUG_MODE")!="1":
        os.environ["DEBUG_MODE"] = "1"
        if os.environ.get("FLASK_ENV") == "development"
            check_postgres()
        with app.app_context():
            upgrade()
            create_default_users()
        
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port='5001')
    os.environ["DEBUG_MODE"] = "0"
    
