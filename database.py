from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
Base = db.Model  # Definir Base aquí

def init_db(app):
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()