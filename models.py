from sqlalchemy import Column, Integer, String, Boolean
from database import Base  # Importar Base desde database.py

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
