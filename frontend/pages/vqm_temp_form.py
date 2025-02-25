import streamlit as st
import pandas as pd
import requests
import numpy as np

# Configuración de la API Flask
API_URL = "http://127.0.0.1:5000/vqm"

st.set_page_config(page_title="Calcular VQM Temperatura", layout="wide")

st.markdown('<div class="header">📊 CALCULAR VQM TEMPERATURA</div>', unsafe_allow_html=True)

# 🎨 Estilos CSS personalizados
st.markdown(
    """
    <style>
        .header {
            text-align: center;
            background-color: #0055A4;
            padding: 15px;
            color: white;
            font-size: 24px;
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
    """,
    unsafe_allow_html=True
)

# 🔄 Cargar datos desde la API Flask
@st.cache_data
def get_vqm_temperatura():
    response = requests.get(f"{API_URL}/vqm_temperatura_mi10")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("❌ Error al obtener datos de la API.")
        return pd.DataFrame()

df_vqm = get_vqm_temperatura()

# 📌 Selección de filtro
titulo_options = df_vqm["titulo"].unique() if not df_vqm.empty else []
trimestre_anio_options = df_vqm["trimestre_anio"].unique() if not df_vqm.empty else []

col1, col2 = st.columns(2)

with col1:
    titulo_selected = st.multiselect("📌 Selecciona título(s):", titulo_options)
with col2:
    trimestre_selected = st.selectbox("📆 Selecciona trimestre-año:", trimestre_anio_options)

# 📊 Filtrar datos
if titulo_selected and trimestre_selected:
    df_filtered = df_vqm[(df_vqm["titulo"].isin(titulo_selected)) & (df_vqm["trimestre_anio"] == trimestre_selected)]
else:
    df_filtered = pd.DataFrame()

# 📋 Mostrar tabla editable
st.subheader("📋 Datos de Temperatura MI10")
if not df_filtered.empty:
    df_editable = st.data_editor(df_filtered, num_rows="dynamic", key="vqm_edit")
else:
    st.warning("⚠️ Selecciona un título y trimestre-año para ver los datos.")

# 🔢 Cálculo de estadísticas
if not df_filtered.empty and len(df_filtered) >= 14:
    media_diferencia = df_filtered["diferencia_temperaturas"].mean()
    desviacion_std = df_filtered["diferencia_temperaturas"].std()
    lsx = media_diferencia + 2 * desviacion_std
    lix = media_diferencia - 2 * desviacion_std
    
    conformidad = "CONFORME" if (lsx >= 0 and lix <= 0) else "NO CONFORME"
    
    st.metric("📏 Media Diferencia Temperaturas", f"{media_diferencia:.2f}°C")
    st.metric("📉 Desviación Estándar", f"{desviacion_std:.2f}")
    st.metric("🔼 Límite Superior", f"{lsx:.2f}")
    st.metric("🔽 Límite Inferior", f"{lix:.2f}")
    
    st.text_input("🟢 Estado de Conformidad", conformidad, disabled=True)
    
    # 🚨 Si no es conforme, notificar
    if conformidad == "NO CONFORME":
        st.error("⚠️ VQM NO CONFORME - Se notificará a los departamentos correspondientes.")

        # Simulación de envío de correos
        def enviar_correos():
            st.success("📨 Correos enviados a Mantenimiento, Obtención y Medida.")
        
        if st.button("📤 Enviar Notificación"):
            enviar_correos()

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# 📥 **Guardar Datos**
def guardar_datos():
    response = requests.post(f"{API_URL}/vqm_temperatura_mi10", json=df_editable.to_dict(orient="records"))
    if response.status_code == 201:
        st.success("✅ Datos guardados correctamente en la base de datos.")
    else:
        st.error("❌ Error al guardar los datos.")

if st.button("💾 Guardar Datos"):
    guardar_datos()
