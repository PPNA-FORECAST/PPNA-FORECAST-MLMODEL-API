from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound
import json
import jsonschema
from jsonschema.exceptions import ValidationError
from api.schema.ppna_forecast_schema import *
from api.service.ppna_forecast_service import PpnaForecastService

from api.errors.errors import *

ppna_forecast_bp = Blueprint('ppna_forecast', __name__)

# 
@ppna_forecast_bp.route("/api/v1/ppna_forecast/point", methods=["POST"])
@jwt_required()
def get_ppna_forecast_point():
    
    data = request.json

    try:    
        jsonschema.validate(data, ppna_points_schema)
        data = request.json
        ppna_forecast_service = PpnaForecastService()
        forecast = ppna_forecast_service.get_forecast(data)
        return forecast, 200
    
    except ValidationError as ve:  
        return handle_bad_request_error(ve)