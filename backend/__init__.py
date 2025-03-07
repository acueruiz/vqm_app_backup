from flask import Flask
from dotenv import load_dotenv
from .database import init_db
from .routes import api_blueprint
import os

# Cargar variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configurar base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar base de datos
    init_db(app)

    # Registrar la API con el prefijo correcto
    app.register_blueprint(api_blueprint, url_prefix='/vqm')

    return app