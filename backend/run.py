from app import create_app
from flask_migrate import upgrade
from app.infra.scripts.wait_for_postgres import check_postgres
import os

app = create_app()

if __name__ == "__main__":
    if os.environ.get("DEBUG_MODE")!="1":
        os.environ["DEBUG_MODE"] = "1"
        check_postgres()
        with app.app_context():
            upgrade()
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0')
    os.environ["DEBUG_MODE"] = "0"
    