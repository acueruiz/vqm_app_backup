from flask import Flask
from backend.database import init_db
from backend.routes import api_blueprint

def create_app():
    app = Flask(__name__)

    # conf base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aldama2122@localhost:5432/vqm_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # inicializar la bbdd
    init_db(app)

    # registro de blueprints
    app.register_blueprint(api_blueprint)

    return app