from flask import Blueprint, request, jsonify
from models import db, VqmTemperatura, VqmMdm

api_blueprint = Blueprint('api', __name__)

# ruta de prueba
@api_blueprint.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "API funcionando correctamente"}), 200

@api_blueprint.route('/')
def home():
    return "Bienvenido a la API"

@api_blueprint.route('/api/data')
def get_data():
    return {"message": "Datos de la API"}

# obtener datos de VQM Temperatura
@api_blueprint.route('/vqm/temperatura', methods=['GET'])
def get_vqm_temperatura():
    datos = VqmTemperatura.query.all()
    return jsonify([d.to_dict() for d in datos])

# insertar un nuevo registro
@api_blueprint.route('/vqm/temperatura', methods=['POST'])
def add_vqm_temperatura():
    data = request.json
    nuevo_registro = VqmTemperatura(**data)
    db.session.add(nuevo_registro)
    db.session.commit()
    return jsonify({"message": "Registro agregado"}), 201