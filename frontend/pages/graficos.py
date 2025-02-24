import streamlit as st
from streamlit_echarts import st_echarts

# Configuración de la página
st.set_page_config(page_title="Aplicación VQM", layout="wide")

# Estilos personalizados en CSS
st.markdown(
    """
    <style>
        /* Diseño general */
        body {
            font-family: Arial, sans-serif;
        }
        
        /* Encabezado */
        .header {
            display: flex;
            align-items: center;
            background-color: #0055A4;
            padding: 15px 30px;
            color: white;
            border-radius: 8px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        .header h1 {
            font-size: 26px;
            font-weight: bold;
            margin: 0;
        }

        /* Barra lateral */
        .sidebar .sidebar-content {
            background-color: #E0E6F8;
            padding: 20px;
            border-radius: 8px;
        }

        /* Contenido principal */
        .main-content {
            padding: 20px;
        }

        /* Botones mejorados */
        .stButton > button {
            background-color: #0055A4;
            color: white;
            font-size: 16px;
            padding: 10px 15px;
            border-radius: 8px;
            border: none;
            transition: 0.3s;
        }
        
        /* Efecto hover en botones */
        .stButton > button:hover {
            background-color: #003C7E;
            transform: scale(1.05);
        }
        
        /* Separadores entre secciones */
        .separator {
            border-bottom: 3px solid #0055A4;
            margin: 20px 0;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Encabezado con ícono
st.markdown('<div class="header"><h1>📊 Aplicación VQM - Dashboard</h1></div>', unsafe_allow_html=True)

# Barra lateral de configuración
st.sidebar.title("⚙️ Configuración")
st.sidebar.markdown("**Elige tu API preferida:**")
apis = ["ECharts", "Plotly", "Matplotlib"]
api_selected = st.sidebar.selectbox("", apis)

st.sidebar.markdown("**Selecciona un tipo de gráfico:**")
examples = ["📈 Línea", "📊 Barras", "🍕 Pie"]
example_selected = st.sidebar.selectbox("", examples)

st.sidebar.markdown("""
📌 *ECharts demos están basados en [Apache ECharts](https://echarts.apache.org/examples/en/index.html). 
Convierte los JSON a diccionarios de Python para obtener visualizaciones dinámicas.*
""")

# Contenido principal
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
st.title("📊 Visualización de Datos")

# Configuración del gráfico
option = {
    "xAxis": {
        "type": "category",
        "data": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    },
    "yAxis": {
        "type": "value"
    },
    "series": [
        {
            "data": [820, 932, 901, 934, 1290, 1330, 1320],
            "type": "line",
            "smooth": True,  # Hace la línea más curva
            "lineStyle": {
                "color": "#0055A4",
                "width": 3
            },
            "areaStyle": {
                "color": "rgba(0, 85, 164, 0.3)"
            }
        }
    ]
}

# Mostrar gráfico
st_echarts(option, height="500px")

# Botón interactivo para futuras funciones
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
if st.button("🔄 Actualizar Datos"):
    st.success("📢 Datos actualizados correctamente.")

# Fuente del código
st.markdown("**📌 Fuente:** [Apache ECharts](https://echarts.apache.org/examples/en/editor.html?c=line-simple)")
