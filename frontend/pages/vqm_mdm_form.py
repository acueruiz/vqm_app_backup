import streamlit as st
import pandas as pd
import requests

# URL de la API Flask
API_URL = "http://127.0.0.1:5000/vqm"

# Configuración de la página
st.set_page_config(page_title="VQM MDM - Introducción de Datos", layout="wide")

# Estilos personalizados
st.markdown(
    """
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

        .stButton > button {
            background-color: #0055A4;
            color: white;
            font-size: 16px;
            padding: 12px 18px;
            border-radius: 8px;
            border: none;
            transition: 0.3s;
        }

        .stButton > button:hover {
            background-color: #003C7E;
            transform: scale(1.05);
        }

        .separator {
            border-bottom: 3px solid #0055A4;
            margin: 20px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# encabezado
st.markdown('<div class="header">VQM MDM - INTRODUCCIÓN DE DATOS</div>', unsafe_allow_html=True)

# 🔄 cargar datos de la API Flask
@st.cache_data
def get_mdm_data():
    response = requests.get(f"{API_URL}/datos_mdms")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("❌ Error al obtener datos de la API.")
        return pd.DataFrame()

df_mdm = get_mdm_data()

# selección del MDM
if not df_mdm.empty:
    mdm_selected = st.selectbox("Módulo MDM:", df_mdm["masico"].unique())
    mdm_info = df_mdm[df_mdm["masico"] == mdm_selected].iloc[0]
else:
    mdm_selected = None
    mdm_info = {}

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# formulario de datos
col1, col2, col3 = st.columns(3)

with col1:
    circuito = st.text_input("Circuito", mdm_info.get("circuito", ""))
    bascula = st.text_input("Báscula", mdm_info.get("bascula", ""))

with col2:
    fecha = st.date_input("Fecha")
    operador = st.text_input("Operador", mdm_info.get("operador", ""))

# pesos patrón obtenidos de la BBDD
col1, col2, col3 = st.columns(3)

with col1:
    peso_patron = st.number_input("Peso masas patrón (kg)", value=mdm_info.get("valor_bascula", 0.0))
    primera_cantidad = st.number_input("Primera cantidad (kg)", value=mdm_info.get("valor_test1", 0.0))
    segunda_cantidad = st.number_input("Segunda cantidad (kg)", value=mdm_info.get("valor_test2", 0.0))

with col2:
    valor_vqm_bascula = st.number_input("Valor VQM báscula (kg)", value=mdm_info.get("valor_bascula", 0.0))
    valor_cero_bascula = st.number_input("Valor cero VQM báscula (kg)", value=mdm_info.get("valor_cero_bascula", 0.0))

with col3:
    verif1_valor_maxico = st.number_input("Verif1 - Valor máxico (kg)", value=0.0)
    verif1_valor_bascula = st.number_input("Verif1 - Valor báscula (kg)", value=0.0)
    verif2_valor_maxico = st.number_input("Verif2 - Valor máxico (kg)", value=0.0)
    verif2_valor_bascula = st.number_input("Verif2 - Valor báscula (kg)", value=0.0)

# cálculo de errores en tiempo real
error_cantidad_1 = verif1_valor_bascula - verif1_valor_maxico
error_cantidad_2 = verif2_valor_bascula - verif2_valor_maxico

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# verificación de conformidad
col1, col2 = st.columns(2)

with col1:
    st.number_input("Error cantidad 1", value=error_cantidad_1, disabled=True)
    st.number_input("Error cantidad 2", value=error_cantidad_2, disabled=True)

with col2:
    vqm_bascula_conforme = st.checkbox("VQM Báscula Conforme", value=mdm_info.get("vqm_bascula_conforme", False))
    vqm_maxico_conforme = st.checkbox("VQM Másico Conforme", value=mdm_info.get("vqm_masico_conforme", False))

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# enviar datos a la API Flask
def enviar_datos():
    nuevo_registro = {
        "titulo": mdm_selected,
        "fecha": str(fecha),
        "operador": operador,
        "valor_bascula": valor_vqm_bascula,
        "valor_cero_bascula": valor_cero_bascula,
        "vqm_bascula_conforme": vqm_bascula_conforme,
        "error_cantidad1": error_cantidad_1,
        "error_cantidad2": error_cantidad_2,
        "vqm_masico_conforme": vqm_maxico_conforme
    }

    response = requests.post(f"{API_URL}/vqm_mdm", json=nuevo_registro)
    
    if response.status_code == 201:
        st.success("✅ Datos enviados correctamente.")
    else:
        st.error(f"❌ Error al enviar los datos: {response.text}")

# botones de acción
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Limpiar formulario"):
        st.experimental_rerun()

with col2:
    if st.button("📥 Guardar datos"):
        enviar_datos()

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
