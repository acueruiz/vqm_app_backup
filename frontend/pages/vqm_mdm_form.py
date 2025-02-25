import streamlit as st
import requests
import pandas as pd

# Configuración de la API Flask
API_URL = "http://127.0.0.1:5000/vqm"

# Configuración de la página
st.set_page_config(page_title="VQM MDM - Introducción de Datos", layout="wide")

# Encabezado
st.markdown('<div class="header">VQM MDM - INTRODUCCIÓN DE DATOS</div>', unsafe_allow_html=True)

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
        .stButton > button {
            background-color: #0055A4;
            color: white;
            font-size: 16px;
            padding: 10px 15px;
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
    """, unsafe_allow_html=True)

# 🔄 Cargar datos de la API Flask
@st.cache_data
def get_mdm_data():
    response = requests.get(f"{API_URL}/vqm_mdm")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("❌ Error al obtener datos de la API.")
        return pd.DataFrame()

@st.cache_data
def get_mdm_details():
    response = requests.get(f"{API_URL}/datos_mdms")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("❌ Error al obtener detalles de MDMs.")
        return pd.DataFrame()

df_mdm = get_mdm_data()
df_mdm_details = get_mdm_details()

# 🏷️ Selección del MDM
if not df_mdm.empty:
    mdm_selected = st.selectbox("Módulo MDM:", df_mdm["titulo"].unique())
    mdm_info = df_mdm[df_mdm["titulo"] == mdm_selected].iloc[0]
    mdm_details = df_mdm_details[df_mdm_details["masico"] == mdm_selected].iloc[0] if not df_mdm_details.empty else {}
else:
    mdm_selected = None
    mdm_info = {}
    mdm_details = {}

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# 📋 Formulario de Introducción de Datos
col1, col2, col3 = st.columns(3)

with col1:
    circuito = st.text_input("Circuito", mdm_details.get("circuito", ""))
    bascula = st.text_input("Báscula", mdm_details.get("bascula", ""))

with col2:
    fecha = st.date_input("Fecha")
    operador = st.text_input("Operador", "")

# 🏋️ Pesos patrón desde la BBDD
col1, col2, col3 = st.columns(3)

with col1:
    peso_patron = st.number_input("Peso masas patrón (kg)", value=mdm_details.get("valor_test1", 0.0))
    primera_cantidad = st.number_input("Primera cantidad (kg)", value=mdm_details.get("valor_test2", 0.0))
    segunda_cantidad = st.number_input("Segunda cantidad (kg)", value=mdm_details.get("tolerancia1", 0.0))

with col2:
    valor_vqm_bascula = st.number_input("Valor VQM báscula (kg)", value=0.0)
    valor_cero_bascula = st.number_input("Valor cero VQM báscula (kg)", value=0.0)

with col3:
    verif1_valor_maxico = st.number_input("Verif1 - Valor máxico (kg)", value=0.0)
    verif1_valor_bascula = st.number_input("Verif1 - Valor báscula (kg)", value=0.0)
    verif2_valor_maxico = st.number_input("Verif2 - Valor máxico (kg)", value=0.0)
    verif2_valor_bascula = st.number_input("Verif2 - Valor báscula (kg)", value=0.0)

# ⚠️ **Cálculo de errores**
error_cantidad_1 = (verif1_valor_bascula - verif1_valor_maxico) * 1000 if verif1_valor_bascula and verif1_valor_maxico else 0
error_cantidad_2 = (verif2_valor_bascula - verif2_valor_maxico) * 1000 if verif2_valor_bascula and verif2_valor_maxico else 0

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# ✅ **Verificación de conformidad**
col1, col2 = st.columns(2)

with col1:
    st.number_input("Error cantidad 1 (g)", value=error_cantidad_1, disabled=True)
    st.number_input("Error cantidad 2 (g)", value=error_cantidad_2, disabled=True)

with col2:
    tolerancia1 = mdm_details.get("tolerancia1", 10)
    tolerancia2 = mdm_details.get("tolerancia2", 10)

    vqm_masico_conforme = "NO CONFORME"
    if abs(error_cantidad_1) <= tolerancia1 and abs(error_cantidad_2) <= tolerancia2:
        vqm_masico_conforme = "CONFORME"
    elif segunda_cantidad == 0:
        vqm_masico_conforme = "Introducir datos cantidad 2"

    st.text_input("VQM Másico Conforme", value=vqm_masico_conforme, disabled=True)

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# 🚀 **Envío de datos a la API Flask**
def enviar_datos():
    # Convertir "CONFORME" y "NO CONFORME" a valores booleanos antes de guardar en la base de datos
    vqm_bascula_conforme_bool = True if vqm_masico_conforme == "CONFORME" else False
    vqm_masico_conforme_bool = True if vqm_masico_conforme == "CONFORME" else False

    nuevo_registro = {
        "titulo": mdm_selected,
        "fecha": str(fecha),
        "operador": operador,
        "valor_bascula": valor_vqm_bascula,
        "valor_cero_bascula": valor_cero_bascula,
        "vqm_bascula_conforme": vqm_bascula_conforme_bool,  # ✅ Enviar como Boolean
        "error_cantidad1": error_cantidad_1,
        "error_cantidad2": error_cantidad_2,
        "vqm_masico_conforme": vqm_masico_conforme_bool  # ✅ Enviar como Boolean
    }

    response = requests.post(f"{API_URL}/vqm_mdm", json=nuevo_registro)
    
    if response.status_code == 201:
        st.success("✅ Datos enviados correctamente.")
        if vqm_masico_conforme == "NO CONFORME":
            st.warning("⚠️ VQM NO CONFORME - Se enviará notificación a mantenimiento.")
    else:
        st.error("❌ Error al enviar los datos.")

# 🎯 **Botones de acción**
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Limpiar formulario"):
        st.experimental_rerun()

with col2:
    if st.button("📥 Guardar datos en la BBDD"):
        enviar_datos()

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
