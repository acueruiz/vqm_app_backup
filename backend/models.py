from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import db  # Importar Base desde database.py

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    admin = Column(Boolean, default=False)

    # relación con correos y permisos
    correos = relationship("CorreoUsuario", back_populates="usuario", cascade="all, delete")
    permisos = relationship("PermisoUsuario", back_populates="usuario", cascade="all, delete")


class CorreoUsuario(db.Model):
    __tablename__ = "correos_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    tipo_notificacion = Column(String, nullable=False)  # 'ALERTA_NC', 'INFORME_VQM', 'MANTENIMIENTO'
    activo = Column(Boolean, default=True)

    usuario = relationship("Usuario", back_populates="correos")


class PermisoUsuario(db.Model):
    __tablename__ = "permisos_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    grupo = Column(String, nullable=False)  # 'MEDIDA', 'OBTENCIÓN', 'MANTENIMIENTO'
    permiso_edicion = Column(Boolean, default=False)
    permiso_desbloqueo = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="permisos")


class VqmTemperatura(db.Model):
    __tablename__ = "vqm_temperatura"

    id = Column(Integer, primary_key=True, autoincrement=True)
    maquina = Column(String, nullable=False)
    apelacion = Column(String)
    receta = Column(String)
    temperatura_caida = Column(Float)
    media_calificacion = Column(Float)
    fecha_calificacion = Column(Date)
    operario = Column(String)


class TratamientoNCVqm(db.Model):
    __tablename__ = "tratamiento_nc_vqm"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    fecha = Column(Date)
    trimestre_anio = Column(String)
    instrumento_medida = Column(String)
    maquina = Column(String)
    operario = Column(String)
    vqm_conforme = Column(Boolean)
    descripcion_intervencion = Column(String)
    resultado_intervencion = Column(String)
    efectos_proceso = Column(String)
    efectos_producto = Column(String)
    acciones_nc = Column(String)
    nc_validada = Column(Boolean)
    fecha_acciones = Column(Date)


class DatosMdms(db.Model):
    __tablename__ = "datos_mdms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    masico = Column(String)
    kw = Column(Float)
    id_dosificador = Column(String)
    valor_test1 = Column(Float)
    tolerancia1 = Column(Float)
    valor_test2 = Column(Float)
    tolerancia2 = Column(Float)
    circuito = Column(String)
    bascula = Column(String)
    id_bascula = Column(String)


class VqmMdm(db.Model):
    __tablename__ = "vqm_mdm"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    fecha = Column(Date)
    operador = Column(String)
    valor_bascula = Column(Float)
    valor_cero_bascula = Column(Float)
    vqm_bascula_conforme = Column(Boolean)
    error_cantidad1 = Column(Float)
    error_cantidad2 = Column(Float)
    vqm_masico_conforme = Column(Boolean)


class VqmTemperaturaMI10(db.Model):
    __tablename__ = "vqm_temperatura_mi10"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    fecha = Column(Date)
    num_ml_dia = Column(Integer)
    temperatura_mi = Column(Float)
    temperatura_pistola = Column(Float)
    diferencia_temperaturas = Column(Float)
    trimestre_anio = Column(String)
    desviacion_tmi = Column(Float)
    desviacion_tmi_tr = Column(Float)
    media_tmi_tr = Column(Float)
    lsx = Column(Float)
    lix = Column(Float)
    vqm_conforme = Column(Boolean)
    operario = Column(String)