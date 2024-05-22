import os
import tensorflow as tf
import keras 
from flask import Flask 
from flask_jwt_extended import JWTManager
from api.errors.errors import *
from api.route.ppna_forecast_route import ppna_forecast_bp
from dotenv import load_dotenv
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow request regardless the origin
### Environment variables
load_dotenv()

### JWT 
app.config['JWT_PUBLIC_KEY'] = open(os.environ.get('PUBLIC_KEY_PATH')).read()
#app.config['JWT_ALGORITHM'] = os.environ.get('ENCRYPT_ALG')
app.config['JWT_ALGORITHM'] = 'RS256'
jwt = JWTManager(app)

### Blueprints 
app.register_blueprint(ppna_forecast_bp)


### Errors
app.register_error_handler(400, handle_bad_request_error) 
app.register_error_handler(401, handle_unauthorized_error)
app.register_error_handler(403, handle_forbidden_error)
app.register_error_handler(404, handle_not_found_error)
app.register_error_handler(409, handle_conflict_error)
app.register_error_handler(500, handle_generic_error)




if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
