from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = None  # Inicializamos una variable global para Flask-Migrate

def init_db(app):
    global migrate
    db.init_app(app)
    migrate = Migrate(app, db)  # Habilita Flask-Migrate
