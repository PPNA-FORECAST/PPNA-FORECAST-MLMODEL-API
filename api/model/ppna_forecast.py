from werkzeug.exceptions import NotFound, Forbidden, Conflict, Unauthorized, BadRequest
import keras
import tensorflow as tf
import numpy as np 
import pandas as pd

class PpnaForecast:

    """
    This function is key in a LSTM model, prepare the data in form of past observations. For example, if the data is [1,2,3,4,5,6,7,8,9,10], 
    the seq_len = 5 : 
    past_data = [[1],[2],[3],[4],[5]],
    past_data = [[2],[3],[4],[5],[6]]
    and so on...
    """
    @staticmethod
    def prepare_sequence_point(points, seq_len):
        
        past_data = []  # Window for the past 
        #print(points)
        print(points['sample'].shapep[0])
        for i in range(points.shape[0] - int(seq_len - 1)):
            a = points[i: i + seq_len] 
            past_data.append(a[:seq_len])

        past_data = np.array(past_data)

        print(past_data)
        return past_data
      

    @staticmethod
    def load_ppna_points(points_json):
        print(points_json)
        df = pd.DataFrame(points_json)
        print(df)
        return df

    @staticmethod
    def predict_ppna_points(sequence_points): 
        keras.layers.TFSMLayer("./model", call_endpoint='serving_default')
        return "hola2"