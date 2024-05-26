from flask_jwt_extended import jwt_required
from api.model.ppna_forecast import PpnaForecast
import json
from api.errors.errors import *
import os

class PpnaForecastService:
    
    def __init__(self):
        model_name = os.environ.get('MODEL')
        mean = os.environ.get('MEAN')
        std = os.environ.get('STD')
        n_past_samples = int(os.environ.get('N_PAST_SAMPLES'))
        self.ppna_forecast = PpnaForecast(n_past_samples, model_name, mean, std)

    """
    Esta funcion toma los datos de entrada, en el formato definido en el ppna_forecast_schema, y los transforma
    en el dataframe que necesita el modelo de ML de forecast. 
    """
    def get_forecast(self, data):	
        
        responses = []
        
        for location in data:
            
            points, last_date = self.process_raw_data(location)
            points_forecast = self.ppna_forecast.forecast_ppna(points)
            points_forecast = self.ppna_forecast.desnormalize_ppna(points_forecast)
            response = self.ppna_forecast.format_output(points_forecast, location, last_date)
            
            responses.append(response)
        

        json_data = {"data": responses}
        
        json_string = json.dumps(json_data)

        return json_string

    
    """
    Esta funcion toma los datos de entrada, en el formato definido en el ppna_forecast_schema, y los transforma
    en el dataframe que necesita el modelo de ML de forecast. 
    """
    def process_raw_data(self,location):	
        points = self.ppna_forecast.load_ppna_points(location)
        last_date = self.ppna_forecast.get_last_date(points)
        points = self.ppna_forecast.date_to_date_signal(points)
        points = self.ppna_forecast.normalize_ppna(points)
        points_sequence = self.ppna_forecast.prepare_sequence_point(points)
        return points_sequence, last_date