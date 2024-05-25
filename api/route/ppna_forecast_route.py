from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound
from api.model.ppna_forecast import PpnaForecast
import json
#from api.schema.ppna_forecast_schema import *
#from api.service.ppna_forecast_service import PpnaForecastService

from api.errors.errors import *

ppna_forecast_bp = Blueprint('ppna_forecast', __name__)

# 
@ppna_forecast_bp.route("/api/v1/ppna_forecast/point", methods=["POST"])
@jwt_required()
def get_ppna_forecast_point():
    # Validar
    # Falta el service
    data = request.json
    ppna_forecast = PpnaForecast()
    
    # Lista para almacenar las respuestas por ubicación
    responses = []
    
    # Iterar sobre cada ubicación en los datos
    for location in data:
        points = ppna_forecast.load_ppna_points(location)
        last_date = ppna_forecast.get_last_date(points)
        points = ppna_forecast.date_to_date_signal(points)
        points_sequence = ppna_forecast.prepare_sequence_point(points)
        points_forecast = ppna_forecast.forecast_ppna(points_sequence)
        response = ppna_forecast.format_output(points_forecast, location, last_date)
        
        # Agregar la respuesta a la lista de respuestas
        responses.append(response)
    
    # Crear el diccionario con el campo "data" que contiene la lista de respuestas
    json_data = {"data": responses}
    
    # Convertir el diccionario a formato JSON
    json_string = json.dumps(json_data)
    
    # Retornar la respuesta JSON
    return json_string, 200
