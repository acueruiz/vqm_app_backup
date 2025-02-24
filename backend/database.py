from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

def reset_db():
    """Borra todos los datos de la base de datos y recrea las tablas."""
    with db.engine.connect() as connection:
        transaction = connection.begin()
        try:
            db.session.commit()  # Asegurarse de que no haya transacciones abiertas
            db.reflect()  # Refleja la estructura de la base de datos
            db.drop_all()  # Borra todas las tablas
            db.create_all()  # Vuelve a crearlas
            transaction.commit()
            print("🚀 Base de datos reiniciada con éxito.")
        except Exception as e:
            transaction.rollback()
            print(f"❌ Error al reiniciar la base de datos: {e}")
