import os
from flask import Flask
from dotenv import load_dotenv
from .database import init_db
from .routes import api_blueprint

# cargar variables de entorno (para credenciales)
load_dotenv()

def create_app():
    app = Flask(__name__)

    # configurar base de datos desde variables de entorno
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # inicializar base de datos
    init_db(app)

    # registrar rutas
    app.register_blueprint(api_blueprint)

    return app
