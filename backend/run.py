from app import create_app
from infra.scripts import services

app = create_app()

if __name__ == "__main__":
    # Run the Flask app
    services.up()
    app.run(debug=True, host='0.0.0.0')