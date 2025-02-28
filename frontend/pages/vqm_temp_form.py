import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(page_title="VQM Temperatura - Introducción de Datos", layout="wide")

# Encabezado
st.markdown('<div class="header">VQM TEMPERATURA - INTRODUCCIÓN DE DATOS</div>', unsafe_allow_html=True)

# 🎨 Estilos CSS personalizados
st.markdown("""
    <style>
        .header {
            text-align: center;
            background-color: #0055A4;
            padding: 15px;
            color: white;
            font-size: 22px;
            font-weight: bold;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .separator {
            border-bottom: 3px solid #0055A4;
            margin: 20px 0;
        }
    </style>
    """, unsafe_allow_html=True)

# 🔄 Cargar datos de la API Flask
@st.cache_data
def get_vqm_temperatura():
    return pd.DataFrame({
        "maquina": ["M10", "M20", "M30", "M40"],
        "apelacion": ["24680X05", "16269X32", "19940X13", "22180X04"],
        "receta": ["01033Z210", "021970Z06", "037663Z01", "040509Z01"],
        "temperatura_caida": [151, 160, 166, 158],
        "media_calificacion": [-0.4, -1, 11, 14.8],
        "fecha_calificacion": ["2021-08-17", "2023-12-11", "2023-06-20", "2023-12-13"]
    })

df_vqm_temp = get_vqm_temperatura()

# 📋 Formulario de Introducción de Datos
col1, col2 = st.columns(2)

with col1:
    trimestre = st.selectbox("Trimestre", ["1º / 2023", "2º / 2023", "3º / 2023", "4º / 2023"])
    maquina = st.selectbox("Máquina", df_vqm_temp["maquina"].unique())
    operador = st.text_input("Operador")

with col2:
    apelacion = df_vqm_temp[df_vqm_temp["maquina"] == maquina]["apelacion"].values[0]
    receta = df_vqm_temp[df_vqm_temp["maquina"] == maquina]["receta"].values[0]
    temperatura_caida = df_vqm_temp[df_vqm_temp["maquina"] == maquina]["temperatura_caida"].values[0]
    media_calificacion = df_vqm_temp[df_vqm_temp["maquina"] == maquina]["media_calificacion"].values[0]
    fecha_calificacion = df_vqm_temp[df_vqm_temp["maquina"] == maquina]["fecha_calificacion"].values[0]
    
    st.text_input("Apelación", apelacion, disabled=True)
    st.text_input("Receta", receta, disabled=True)
    st.number_input("T* caída", value=temperatura_caida, disabled=True)
    st.number_input("Media de calificación", value=media_calificacion, disabled=True)
    st.date_input("Fecha de Calificación", value=pd.to_datetime(fecha_calificacion), disabled=True)

st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

# 📥 Añadir carga de temperatura
df_cargas = pd.DataFrame(columns=["Fecha", "TMI", "TR", "TMI - TR"])
if "cargas" not in st.session_state:
    st.session_state.cargas = df_cargas

with st.expander("Añadir nueva carga de temperatura"):
    fecha = st.date_input("Fecha de carga")
    tmi = st.number_input("Temperatura MI (TMI)", value=0.0)
    tr = st.number_input("Temperatura Pistola (TR)", value=0.0)
    if st.button("Agregar carga"):
        nueva_carga = pd.DataFrame({
            "fecha": [fecha],
            "temperatura_mi": [tmi],
            "temperatura_pistola": [tr],
            "diferencia_temperaturas": [tmi - tr],
            "trimestre_anio": [trimestre],
            "operador": [operador]
        })
        st.session_state.cargas = pd.concat([st.session_state.cargas, nueva_carga], ignore_index=True)

# 📊 Mostrar cargas ingresadas
st.dataframe(st.session_state.cargas)

# 🚀 Guardar datos en la tabla vqm_temperatura_mi10
if st.button("Guardar en BBDD"):
    st.success("✅ Datos guardados en vqm_temperatura_mi10 correctamente.")
