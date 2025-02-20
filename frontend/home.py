import streamlit as st

st.set_page_config(page_title="Apliación VQM", layout="wide")

st.title("Bienvenido a la apliacación VQM")

st.sidebar.header("Menú")
opcion = st.sidebar.radio("Navegación", ["Inicio", "Formulario VQM", "Dashboard", "Usuarios"])

if opcion == "Inicio":
    st.write("Esta es la pantalla principal de la aplicación VQM.")
elif opcion == "Formulario VQM":
    from frontend import form_vqm
    form_vqm.mostrar_formulario()
elif opcion == "Dashboard":
    from frontend import vqm_dashboard
    vqm_dashboard.mostrar_dashboard()
elif opcion == "Usuarios":
    from frontend import users
    users.mostrar_gestion_usuarios()