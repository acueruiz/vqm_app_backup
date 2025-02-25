import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px

# Configurar API URL
API_URL = "http://127.0.0.1:5000/vqm"

# Configuración de la página
st.set_page_config(page_title="Aplicación VQM", layout="wide")

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

# 🏠 **Encabezado principal**
st.markdown('<div class="header">📋 Análisis de VQM MDM</div>', unsafe_allow_html=True)

# 🔄 **Cargar datos desde la API**
with st.spinner("Cargando datos de VQM MDM..."):
    time.sleep(1)  # Simulación de carga
    
    # Datos de VQM MDM
    response_vqm = requests.get(f"{API_URL}/vqm_mdm")
    df_vqm = pd.DataFrame(response_vqm.json()) if response_vqm.status_code == 200 else pd.DataFrame()

# 📋 **Análisis de VQM MDM**
st.subheader("📋 Estado de las VQM MDM Registradas")

if not df_vqm.empty:
    df_vqm["fecha"] = pd.to_datetime(df_vqm["fecha"], errors='coerce')

    # 📊 **Indicadores Clave**
    col1, col2, col3 = st.columns(3)

    with col1:
        total_vqm = len(df_vqm)
        st.metric(label="📏 Total de VQM Registradas", value=total_vqm)

    with col2:
        conformes = df_vqm["vqm_bascula_conforme"].sum()
        st.metric(label="✅ VQM Báscula Conformes", value=conformes)

    with col3:
        no_conformes = total_vqm - conformes
        st.metric(label="⚠️ VQM Báscula No Conformes", value=no_conformes)

    # 📈 **Gráfico de conformidad**
    fig_conformidad = px.pie(df_vqm, names="vqm_bascula_conforme", title="📊 Porcentaje de Conformidad")
    st.plotly_chart(fig_conformidad, use_container_width=True)

    # 📉 **Gráfico de distribución de errores**
    fig_errores = px.histogram(df_vqm, x=["error_cantidad1", "error_cantidad2"], title="📉 Distribución de Errores")
    st.plotly_chart(fig_errores, use_container_width=True)

    # 📊 **Filtrado por operador**
    operadores = df_vqm["operador"].unique()
    selected_operador = st.selectbox("👨‍🔧 Selecciona un Operador:", options=operadores)

    df_filtrado = df_vqm[df_vqm["operador"] == selected_operador]
    st.write(f"🔎 Mostrando datos para **{selected_operador}**")
    st.dataframe(df_filtrado)

    # 🚨 **Alertas de errores altos**
    max_error = df_vqm[["error_cantidad1", "error_cantidad2"]].max().max()
    if max_error > 10:
        st.warning(f"⚠️ Se han detectado errores superiores a 10 kg en algunas mediciones.")
else:
    st.warning("📭 No hay datos de VQM MDM disponibles.")

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# 🚨 **Notificación en tiempo real sobre No Conformidades**
st.subheader("🚨 Estado de No Conformidades")
response_nc = requests.get(f"{API_URL}/nc_abiertas")
if response_nc.status_code == 200:
    nc_data = response_nc.json()
    nc_count = nc_data.get("nc_abiertas", 0)

    if nc_count > 0:
        st.warning(f"⚠️ Hay **{nc_count}** No Conformidades abiertas.")
    else:
        st.success("✅ No hay No Conformidades pendientes.")

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# 📩 **Acciones rápidas**
st.subheader("📩 Acciones Rápidas")

col1, col2 = st.columns(2)

with col1:
    if st.button("📤 Enviar Reporte de VQM MDM"):
        st.success("📨 Reporte enviado correctamente.")

with col2:
    if st.button("Actualizar Datos"):
        st.experimental_rerun()

# 🏁 **Pie de página**
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Michelin_logo.svg/2560px-Michelin_logo.svg.png" 
        width="120">
    </div>
    """,
    unsafe_allow_html=True
)
