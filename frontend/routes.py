from flask import Blueprint, render_template
import requests

# Crear Blueprint para las rutas del frontend
frontend_bp = Blueprint('frontend', __name__, template_folder='templates')

@frontend_bp.route('/')
def home():
    # Usar la ruta correcta para obtener los datos
    response = requests.get('http://127.0.0.1:5000/vqm/vqm_mdm')  # 👈 Corrige si el endpoint es /api/vqm/vqm_mdm
    
    if response.status_code == 200:
        datos = response.json()
    else:
        datos = []

    return render_template('index.html', datos=datos)

@frontend_bp.route('/vqm_mdm')
def vqm_mdm():
    return render_template('form_vqm_mdm.html')

@frontend_bp.route('/vqm_temp')
def vqm_temp():
    return render_template('form_vqm_temp.html')
