from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound
from api.model.ppna_forecast import PpnaForecast
#from api.schema.ppna_forecast_schema import *
#from api.service.ppna_forecast_service import PpnaForecastService

from api.errors.errors import *

ppna_forecast_bp = Blueprint('ppna_forecast', __name__)

# 
@ppna_forecast_bp.route("/api/v1/ppna_forecast/point", methods=["POST"])
@jwt_required()
def get_ppna_forecast_point():
    
    #validar! 
    #falta el service
    data = request.json
    ppna_forecast = PpnaForecast()
    #itero sobre cada location para devolverlo por location
    for location in data.items():
        
        points = ppna_forecast.load_ppna_points(data)
        points = ppna_forecast.date_to_date_signal(points)
        points_sequence = ppna_forecast.prepare_sequence_point(points)
        points_forecast = ppna_forecast.forecast_ppna(points_sequence)
        #ver como delvolver esto tipo {location:[lat:xx,long:yy,sample:[date:a, ppna:1], ..], ..}

    return "points",200

"""
#Get a geography and return all the locations inside the geography and the total area of the geography. 
#{area:xx , location: [latitude:mm, longitude:xx], ...}  and the total area 
@ppna_bp.route("/api/v1/ppna/location", methods=["POST"])
def calculate_polygon():

    data = request.json

    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input data. A list of coordinates is expected."}), 400

    
    polygon_area = PpnaService.get_area(data)
    locations = PpnaService.get_locations(data)

    return jsonify({"area": polygon_area, "location": locations }), 200
"""