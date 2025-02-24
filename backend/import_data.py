from sqlalchemy import create_engine
from models import VqmTemperatura, VqmMdm, TratamientoNCVqm, VqmTemperaturaMI10, DatosMdms
from database import reset_db
from __init__ import create_app  # Importar la aplicación Flask
import pandas as pd
import os

# Crear la aplicación Flask y establecer contexto
app = create_app()

with app.app_context():
    reset_db()  # 🔴 Ahora se ejecuta dentro del contexto de la app

# Configuración de conexión
DB_URL = 'postgresql://postgres:Aldama2122@localhost:5432/vqm_db'
engine = create_engine(DB_URL)

# Definir ruta de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

files = {
    "Datos VQM Temperatura MI": os.path.join(DATA_DIR, "Datos VQM temperatura MI.ods"),
    "VQM MDM": os.path.join(DATA_DIR, "VQM MDM.ods"),
    "Tratamiento NC VQM": os.path.join(DATA_DIR, "Tratamiento de las NC de las VQM.ods"),
    "VQM Temperatura MI10": os.path.join(DATA_DIR, "VQM Temperatura MI10.ods"),
    "Datos MDMS": os.path.join(DATA_DIR, "Datos MDMs.ods")
}

def clean_and_insert(df, table_name, rename_dict, boolean_fields=None, date_fields=None, numeric_fields=None):
    df = df.rename(columns=rename_dict)
    df = df[list(rename_dict.values())]  # Filtra solo columnas válidas

    if boolean_fields:
        for field in boolean_fields:
            df[field] = df[field].map({"Sí": True, "No": False, 1: True, 0: False}).astype(bool)

    if date_fields:
        for field in date_fields:
            if field in df.columns:
                df[field] = pd.to_datetime(df[field], errors="coerce").dt.date
                df[field] = df[field].fillna(pd.to_datetime("2000-01-01").date())

    if numeric_fields:
        for field in numeric_fields:
            if field in df.columns:
                df[field] = pd.to_numeric(df[field], errors="coerce").fillna(0.0)

    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"✅ Datos insertados en {table_name} correctamente.")

# transformaciones específicas por tabla
temp_mi_rename = {
    "MI": "maquina",
    "Apelacion": "apelacion",
    "Receta": "receta",
    "Temperatura caida": "temperatura_caida",
    "Media de la calificación (Tmi-Tr)": "media_calificacion",
    "Fecha de la calificacion": "fecha_calificacion",
    "Operario": "operario"
}

temp_mdm_rename = {
    "Título": "titulo",
    "Fecha": "fecha",
    "Operador": "operador",
    "Valor VQM báscula": "valor_bascula",
    "Valor cero VQM báscula": "valor_cero_bascula",
    "VQM báscula conforme": "vqm_bascula_conforme",
    "Error cantidad 1": "error_cantidad1",
    "Error cantidad 2": "error_cantidad2",
    "VQM másico conforme": "vqm_masico_conforme"
}

tnc_rename = {
    "Título": "titulo",
    "Fecha": "fecha",
    "Trimestre-año": "trimestre_anio",
    "Instrumento de medida": "instrumento_medida",
    "Máquina": "maquina",
    "Operario": "operario",
    "VQM CONFORME": "vqm_conforme",
    "Descripción de la intervención": "descripcion_intervencion",
    "Resultado tras intervención": "resultado_intervencion",
    "Posibles efectos sobre PROCESO": "efectos_proceso",
    "Posibles efectos sobre PRODUCTO": "efectos_producto",
    "Si producto NC acciones": "acciones_nc",
    "NC validada": "nc_validada",
    "Fecha acciones producto": "fecha_acciones"
}

temp_mi10_rename = {
    "Título": "titulo",
    "Fecha": "fecha",
    "Nº ML/día": "num_ml_dia",
    "Temperatura MI": "temperatura_mi",
    "Temperatura pistola": "temperatura_pistola",
    "Diferencia temperaturas": "diferencia_temperaturas",
    "Trimestre-año": "trimestre_anio",
    "Desviacion TMI": "desviacion_tmi",
    "Desviacion (Tmi-Tr)": "desviacion_tmi_tr",
    "Media (Tmi-Tr)": "media_tmi_tr",
    "LSx": "lsx",
    "LIx": "lix",
    "VQM CONFORME": "vqm_conforme",
    "Operario": "operario"
}

datos_mdms_rename = {
    "Másico": "masico",
    "KW": "kw",
    "Nº Identificación del Dosificador Másico": "id_dosificador",
    "Valor test 1ª cantidad (kg)": "valor_test1",
    "Tolerancia 1ª cantidad (±g)": "tolerancia1",
    "Valor test 2ª cantidad (kg)": "valor_test2",
    "Tolerancia 2ª cantidad (±g)": "tolerancia2",
    "Circuito": "circuito",
    "Báscula": "bascula",
    "Nº Identificación de la Báscula": "id_bascula"
}

# Importar datos sin duplicaciones
with app.app_context():  # 🔴 Ejecutar la importación dentro del contexto de la app
    clean_and_insert(pd.read_excel(files["Datos VQM Temperatura MI"], engine="odf"), "vqm_temperatura", temp_mi_rename)
    clean_and_insert(pd.read_excel(files["VQM MDM"], engine="odf"), "vqm_mdm", temp_mdm_rename, 
                     boolean_fields=["vqm_bascula_conforme", "vqm_masico_conforme"], date_fields=["fecha"])
    clean_and_insert(pd.read_excel(files["Tratamiento NC VQM"], engine="odf"), "tratamiento_nc_vqm", tnc_rename, 
                     boolean_fields=["vqm_conforme", "nc_validada"], date_fields=["fecha", "fecha_acciones"])
    clean_and_insert(pd.read_excel(files["VQM Temperatura MI10"], engine="odf"), "vqm_temperatura_mi10", temp_mi10_rename, boolean_fields=["vqm_conforme"])
    clean_and_insert(pd.read_excel(files["Datos MDMS"], engine="odf"), "datos_mdms", datos_mdms_rename, 
                     numeric_fields=["kw", "valor_test1", "tolerancia1", "valor_test2", "tolerancia2"])

print("✅ Importación completada sin duplicados.")
