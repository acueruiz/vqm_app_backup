import streamlit as st
import pandas as pd
import requests

def mostrar_dashboard():
    st.header("Dashboard VQM")

    response = requests.get("http://127.0.0.1:5000/vqm/temperatura")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Mostrar tabla de datos
        st.dataframe(df)

        # Gráfica de tendencia
        st.line_chart(df.set_index("fecha")["valor_bascula"])
    else:
        st.error("Error al cargar los datos")
