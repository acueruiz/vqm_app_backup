import streamlit as st
import requests

def mostrar_formulario():
    st.header("Registrar nueva medición VQM")

    fecha = st.date_input("Fecha de medición")
    operador = st.text_input("Operador")
    valor_bascula = st.number_input("Valor VQM báscula (kg)", min_value=0.0)
    valor_cero = st.number_input("Valor cero báscula (kg)", min_value=0.0)
    conforme = st.selectbox("VQM conforme", ["Sí", "No"])

    if st.button("Guardar"):
        datos = {
            "fecha": str(fecha),
            "operador": operador,
            "valor_bascula": valor_bascula,
            "valor_cero_bascula": valor_cero,
            "vqm_conforme": True if conforme == "Sí" else False
        }
        response = requests.post("http://127.0.0.1:5000/vqm/temperatura", json=datos)

        if response.status_code == 201:
            st.success("Registro guardado con éxito")
        else:
            st.error("Error al guardar el registro")
