from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
import keras
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from pandas import json_normalize
from datetime import datetime, timedelta



class PpnaForecast:

    #enrealidad model_name y past samples van av enir como parametros desde el service
    def __init__(self):
        model_name = os.environ.get('MODEL')
        self.model = keras.layers.TFSMLayer(f"./models/{model_name}", call_endpoint='serving_default')
        self.n_past_samples = int(os.environ.get('N_PAST_SAMPLES'))

    """
    This function is key in a LSTM model, prepare the data in form of past observations. For example, if the data is [1,2,3,4,5,6,7,8,9,10], 
    the seq_len = 5 : 
    past_data = [[1],[2],[3],[4],[5]],
    past_data = [[2],[3],[4],[5],[6]]
    and so on...
    """
    def prepare_sequence_point(self, points_df):
        
        self.n_past_samples
  
        past_data = []  # Window for the past 
        for i in range(points_df.shape[0] - int(self.n_past_samples - 1)):
            a = points_df[i: i + self.n_past_samples] 
            past_data.append(a[:self.n_past_samples])

        past_data = np.array(past_data)

        return past_data

    """
    This function takes input json with format {location:[lat:xx,long:yy,sample:[date:a, ppna:1], ..], ..} and 
    convert to the dataframe neeeded by the model. (hay que mejorarlo, es una cagada)
    """
    def load_ppna_points(self, data_json):       

        # Extraer las columnas 'latitude' y 'longitude' de los datos JSON
        latitude = data_json['location']['latitude']
        longitude = data_json['location']['longitude']

        # Aplanar la lista de diccionarios dentro de 'sample'
        sample_list = data_json['location']['sample']
        flattened_data = json_normalize(sample_list)

        # Agregar las columnas 'latitude' y 'longitude' al DataFrame aplanado
        flattened_data['latitude'] = latitude
        flattened_data['longitude'] = longitude

        # Crear el DataFrame con los datos aplanados y las columnas 'latitude' y 'longitude'
        points_df = pd.DataFrame(flattened_data, columns=['latitude', 'longitude', 'temp', 'ppt', 'ppna','date'])
        points_df['date'] = pd.to_datetime(points_df['date'], format='%m/%d/%Y', errors='coerce')

        # Ordenar por fecha
        points_df = points_df.sort_values(by='date', ascending=True)

        return points_df


    #PRE: The DataManager df must have a column labeled "date" which contains calendar dates formated as MONTH-DAY-YEAR.
    #POST: A new column labeled "timestamp_date" is added to the df. It contains the date column info presented in a timestamp format.
    def date_to_date_signal(self, points_df): 

        #convert date to timestamp
        points_df['date_signal'] = pd.to_datetime(points_df['date'], format='%m-%d-%Y').map(pd.Timestamp.timestamp)
        points_df = points_df.drop(columns=['date'])

        #conver timestamp to a periodic datesignal
        seconds_in_a_year = 24*60*60*365
        points_df['date_signal'] = np.sin(points_df['date_signal'] * (2 * np.pi / seconds_in_a_year))

        return points_df

    def forecast_ppna(self, sequence_points): 
        
        points_forecast = self.model(sequence_points)

        return points_forecast
    
    def get_last_date(self, points_df):
        return points_df['date'].iloc[-1]
                    

    def format_output(self, forecast, point, last_date): 
        # Paso 1: Extraer latitud y longitud
        latitude = point['location']['latitude']
        longitude = point['location']['longitude']
        
        # Paso 2: Crear una lista de diccionarios para las muestras de datos, ordenadas por fecha
        sample_list = []
        for data in sorted(point['location']['sample'], key=lambda x: datetime.strptime(x['date'], '%m/%d/%Y')):
            sample_list.append({'date': data['date'], 'ppna': data['ppna']})
        
        # Paso 3: Crear una lista de diccionarios para los pronósticos
        forecast_list = []
        tensor = forecast['dense_1']

        # Iterar sobre los valores del tensor
        for ppna in tensor.numpy()[0]:
            last_date += timedelta(days=15)
            last_date_str = last_date.strftime('%Y-%m-%d')
            forecast_list.append({'date': last_date_str, 'ppna': str(ppna)})
        
        # Paso 4: Construir el diccionario de respuesta
        response = {
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'sample': sample_list,
                'forecast': forecast_list
            }
        }

        return response

