from flask import Blueprint, render_template
import requests

# crear Blueprint para las rutas del frontend
frontend_bp = Blueprint('frontend', __name__, template_folder='templates')

@frontend_bp.route('/')
def home():
    # usar la ruta correcta para obtener los datos
    response = requests.get('http://127.0.0.1:5000/vqm/vqm_mdm')  # 👈 Corrige si el endpoint es /api/vqm/vqm_mdm
    
    if response.status_code == 200:
        datos = response.json()
    else:
        datos = []

    total_vqm = len(datos)
    conformes = sum(1 for d in datos if d.get('vqm_bascula_conforme'))
    no_conformes = total_vqm - conformes

    # obtener operadores únicos
    operadores = list(set(d.get('operador', 'Desconocido') for d in datos))

    # calcular errores
    max_error1 = max([d.get("error_cantidad1", 0) if d.get("error_cantidad1") is not None else 0 for d in datos], default=0)
    max_error2 = max([d.get("error_cantidad2", 0) if d.get("error_cantidad2") is not None else 0 for d in datos], default=0)


    return render_template('index.html', datos=datos, total_vqm=total_vqm,
                           conformes=conformes, no_conformes=no_conformes,
                           operadores=operadores, max_error1=max_error1,
                           max_error2=max_error2)

@frontend_bp.route('/vqm_mdm')
def vqm_mdm():
    return render_template('form_vqm_mdm.html')

@frontend_bp.route('/vqm_temp')
def vqm_temp():
    return render_template('form_vqm_temp.html')
