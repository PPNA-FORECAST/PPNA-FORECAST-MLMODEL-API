from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
import keras
import tensorflow as tf
import numpy as np 
import pandas as pd
import os
from dotenv import load_dotenv

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

        #convierto el json que me llega en un data frame para el modelo 
        points_df = pd.DataFrame(data_json['location']['sample'], columns=['sample'])
        
        
        # Dividir la columna 'sample' en cuatro columnas 'date' y 'ppna'
        points_df = points_df['sample'].str.extract(r'date=(.*?); ppna=(.*?); ppt=(.*?); temp=(.*?)\}')
        points_df.columns = ['date_signal', 'ppna', 'ppt', 'temp']

        # Convertir las columnas al tipo float y saco caracteres no numericos 
        points_df['ppna'] = points_df['ppna'].str.replace('[^\d.]', '', regex=True).astype(float)
        points_df['ppt'] = points_df['ppt'].str.replace('[^\d.]', '', regex=True).astype(float)
        points_df['temp'] = points_df['temp'].str.replace('[^\d.]', '', regex=True).astype(float)

        # Convertir 'date_signal' a datetime
        points_df['date_signal'] = pd.to_datetime(points_df['date_signal'], format='%m/%d/%Y')

        # Agregar las columnas 'latitude' y 'longitude'
        points_df['latitude'] = float(data_json['location']['latitude'])
        points_df['longitude'] = float(data_json['location']['longitude'])

        # Reordenar las columnas
        points_df = points_df[['date_signal', 'latitude', 'longitude', 'temp', 'ppt', 'ppna']]

        # Ordenar por fecha
        points_df = points_df.sort_values(by='date_signal')

        return points_df


    #PRE: The DataManager df must have a column labeled "date" which contains calendar dates formated as MONTH-DAY-YEAR.
    #POST: A new column labeled "timestamp_date" is added to the df. It contains the date column info presented in a timestamp format.
    def date_to_date_signal(self, points_df): 

        #convert date to timestamp
        points_df['date_signal'] = pd.to_datetime(points_df['date_signal'], format='%m-%d-%Y').map(pd.Timestamp.timestamp)

        #conver timestamp to a periodic datesignal
        seconds_in_a_year = 24*60*60*365
        points_df['date_signal'] = np.sin(points_df['date_signal'] * (2 * np.pi / seconds_in_a_year))
        
        return points_df

    def forecast_ppna(self, sequence_points): 
        
        points_forecast = self.model(sequence_points)

        return points_forecast