import streamlit as st
import requests
import pandas as pd

# Configuración de la API Flask
API_URL = "http://127.0.0.1:5000/vqm"

# Configuración de la página
st.set_page_config(page_title="VQM MDM - Datos", layout="wide")

# encabezado
st.markdown('<div class="header">VQM MDM - VISUALIZACIÓN DE DATOS</div>', unsafe_allow_html=True)

# estilos CSS personalizados
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

# Cargar datos de la API Flask
@st.cache_data
def get_mdm_data():
    response = requests.get(f"{API_URL}/vqm_mdm")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())

        # Verificar que la columna 'fecha' existe y convertirla a datetime
        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"], errors='coerce')

        return df
    else:
        st.error("❌ Error al obtener detalles de MDMs.")
        return pd.DataFrame()

df_mdm = get_mdm_data()

# Verifica que el DataFrame no esté vacío antes de continuar
if df_mdm.empty:
    st.warning("No hay datos disponibles.")
    st.stop()

# Filtros de búsqueda
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    mdm_selected = st.selectbox("MDM", ["Todos"] + list(df_mdm["titulo"].unique()))

with col2:
    fecha_inicio = st.date_input("Desde fecha:")

with col3:
    fecha_fin = st.date_input("Hasta fecha:")

with col4:
    if st.button("🔍 Buscar"):
        st.session_state.filtrar = True

# Filtrar datos según selección
if "filtrar" in st.session_state and st.session_state.filtrar:
    if mdm_selected != "Todos":
        df_mdm = df_mdm[df_mdm["titulo"] == mdm_selected]

    if "fecha" in df_mdm.columns:
        df_mdm = df_mdm[(df_mdm["fecha"] >= pd.to_datetime(fecha_inicio)) & 
                        (df_mdm["fecha"] <= pd.to_datetime(fecha_fin))]

# Mostrar tabla con funcionalidades adicionales
if not df_mdm.empty:
    df_mdm = df_mdm.sort_values(by="fecha", ascending=False)
    df_mdm = df_mdm.reset_index(drop=True)
    
    def highlight_non_conform(val):
        if val is False:  # Corrigiendo el formato de "NO CONFORME" en booleanos
            return 'background-color: #FF4B4B; color: white; font-weight: bold;'
        return ''

    # Mostrar en Streamlit con los valores correctos
    st.dataframe(df_mdm.style.applymap(highlight_non_conform, 
                subset=["vqm_bascula_conforme", "vqm_masico_conforme"]))

else:
    st.warning("No se encontraron datos para los filtros seleccionados.")

# Botones adicionales
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("📥 Exportar a CSV"):
        df_mdm.to_csv("datos_vqm.csv", index=False)
        st.success("Archivo CSV generado correctamente.")

with col2:
    if st.button("📥 Exportar a Excel"):
        df_mdm.to_excel("datos_vqm.xlsx", index=False)
        st.success("Archivo Excel generado correctamente.")
