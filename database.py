from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear conexión a la base de datos
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Base para los modelos
Base = declarative_base()

# 📌 Importar modelos después de definir Base
import models  # Ahora sí lo usaremos correctamente

# Función para inicializar la base de datos
def init_db():
    print("📌 Tablas detectadas en SQLAlchemy antes de create_all():", models.Base.metadata.tables.keys())  # 🔍 Depuración
    print("📌 Eliminando y recreando tablas...")
    models.Base.metadata.drop_all(engine)  # Elimina todas las tablas
    models.Base.metadata.create_all(engine)  # Vuelve a crearlas
    print("✅ Tablas recreadas correctamente.")

# Ejecutar la función si el script se ejecuta directamente
if __name__ == "__main__":
    init_db()
    print("📌 Base de datos creada correctamente.")
