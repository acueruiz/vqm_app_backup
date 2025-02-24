from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import db  # Importar Base desde database.py

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    admin = Column(Boolean, default=False)

    correos = relationship("CorreoUsuario", back_populates="usuario", cascade="all, delete")
    permisos = relationship("PermisoUsuario", back_populates="usuario", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "admin": self.admin
        }


class CorreoUsuario(db.Model):
    __tablename__ = "correos_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    tipo_notificacion = Column(String, nullable=False)
    activo = Column(Boolean, default=True)

    usuario = relationship("Usuario", back_populates="correos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo_notificacion": self.tipo_notificacion,
            "activo": self.activo
        }


class PermisoUsuario(db.Model):
    __tablename__ = "permisos_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"))
    grupo = Column(String, nullable=False)
    permiso_edicion = Column(Boolean, default=False)
    permiso_desbloqueo = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="permisos")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "grupo": self.grupo,
            "permiso_edicion": self.permiso_edicion,
            "permiso_desbloqueo": self.permiso_desbloqueo
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "maquina": self.maquina,
            "apelacion": self.apelacion,
            "receta": self.receta,
            "temperatura_caida": self.temperatura_caida,
            "media_calificacion": self.media_calificacion,
            "fecha_calificacion": self.fecha_calificacion.strftime('%Y-%m-%d') if self.fecha_calificacion else None,
            "operario": self.operario
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "fecha": self.fecha.strftime('%Y-%m-%d') if self.fecha else None,
            "trimestre_anio": self.trimestre_anio,
            "instrumento_medida": self.instrumento_medida,
            "maquina": self.maquina,
            "operario": self.operario,
            "vqm_conforme": self.vqm_conforme,
            "descripcion_intervencion": self.descripcion_intervencion,
            "resultado_intervencion": self.resultado_intervencion,
            "efectos_proceso": self.efectos_proceso,
            "efectos_producto": self.efectos_producto,
            "acciones_nc": self.acciones_nc,
            "nc_validada": self.nc_validada,
            "fecha_acciones": self.fecha_acciones.strftime('%Y-%m-%d') if self.fecha_acciones else None
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "masico": self.masico,
            "kw": self.kw,
            "id_dosificador": self.id_dosificador,
            "valor_test1": self.valor_test1,
            "tolerancia1": self.tolerancia1,
            "valor_test2": self.valor_test2,
            "tolerancia2": self.tolerancia2,
            "circuito": self.circuito,
            "bascula": self.bascula,
            "id_bascula": self.id_bascula
        }


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

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "fecha": self.fecha.strftime('%Y-%m-%d') if self.fecha else None,
            "operador": self.operador,
            "valor_bascula": self.valor_bascula,
            "valor_cero_bascula": self.valor_cero_bascula,
            "vqm_bascula_conforme": self.vqm_bascula_conforme,
            "error_cantidad1": self.error_cantidad1,
            "error_cantidad2": self.error_cantidad2,
            "vqm_masico_conforme": self.vqm_masico_conforme
        }
    
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

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "fecha": self.fecha.strftime('%Y-%m-%d') if self.fecha else None,
            "num_ml_dia": self.num_ml_dia,
            "temperatura_mi": self.temperatura_mi,
            "temperatura_pistola": self.temperatura_pistola,
            "diferencia_temperaturas": self.diferencia_temperaturas,
            "trimestre_anio": self.trimestre_anio,
            "desviacion_tmi": self.desviacion_tmi,
            "desviacion_tmi_tr": self.desviacion_tmi_tr,
            "media_tmi_tr": self.media_tmi_tr,
            "lsx": self.lsx,
            "lix": self.lix,
            "vqm_conforme": self.vqm_conforme,
            "operario": self.operario
        }