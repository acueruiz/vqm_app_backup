import streamlit as st
import pandas as pd
import requests

# 📡 Configuración de la API Flask
API_URL = "http://127.0.0.1:5000/vqm"

# 🖥 Configuración de la página
st.set_page_config(page_title="VQM - Registros", layout="wide")

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

# 🏷 Encabezado principal
st.markdown('<div class="header">📋 VQM - REGISTROS HISTÓRICOS</div>', unsafe_allow_html=True)

# 🔄 Cargar datos desde la API Flask
@st.cache_data
def get_vqm_data():
    response = requests.get(f"{API_URL}/vqm_mdm")
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("❌ Error al obtener datos de la API.")
        return pd.DataFrame()

df = get_vqm_data()

# 📊 Mostrar los datos si existen
if not df.empty:
    # Convertir fechas a formato adecuado
    df["fecha"] = pd.to_datetime(df["fecha"], errors='coerce')

    # 📌 **Barra de búsqueda**
    search_query = st.text_input("🔍 Buscar por Operador, MDM o Estado de Conformidad:")
    
    # 📌 **Filtros dinámicos**
    col1, col2, col3 = st.columns(3)

    with col1:
        mdm_list = ["Todos"] + list(df["titulo"].unique())
        selected_mdm = st.selectbox("🏷️ Filtrar por MDM:", mdm_list)

    with col2:
        operador_list = ["Todos"] + list(df["operador"].unique())
        selected_operador = st.selectbox("👷 Filtrar por Operador:", operador_list)

    with col3:
        fecha_range = st.date_input("📅 Filtrar por Fecha:", [])

    # 🔍 **Aplicar filtros**
    df_filtered = df.copy()

    if search_query:
        df_filtered = df_filtered[df_filtered.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]

    if selected_mdm != "Todos":
        df_filtered = df_filtered[df_filtered["titulo"] == selected_mdm]

    if selected_operador != "Todos":
        df_filtered = df_filtered[df_filtered["operador"] == selected_operador]

    if fecha_range:
        df_filtered = df_filtered[(df_filtered["fecha"] >= pd.to_datetime(fecha_range[0])) & 
                                  (df_filtered["fecha"] <= pd.to_datetime(fecha_range[1]))]

    # 📌 **Mostrar tabla dinámica**
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.subheader("📊 Registros Filtrados")
    st.dataframe(df_filtered)

else:
    st.warning("📭 No hay datos disponibles.")

# 🔄 **Botón para actualizar datos**
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
if st.button("🔄 Actualizar Datos"):
    st.cache_data.clear()
    st.experimental_rerun()
