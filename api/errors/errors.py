import logging
from flask import jsonify

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s') # Config for error logging


def handle_bad_request_error(error): # Handles 400 errors
    logging.error(f'400 Bad Request: {str(error)}')
    return jsonify({'error_message': str(error)}), 400

def handle_unauthorized_error(error): # Handles 401 errors
    logging.error(f'401 Unauthorized: {str(error)}')
    return jsonify({'error_message': str(error)}), 401

def handle_forbidden_error(error): # Handles 403 error
    logging.error(f'403 Forbidden: {str(error)}')
    return jsonify({'error_message': str(error)}), 403

def handle_not_found_error(error): # Handles 404 errors
    logging.error(f'404 Not Found: {str(error)}')
    return jsonify({'error_message': str(error)}), 404

def handle_conflict_error(error): # Handles 409 errors
    logging.error(f'409 Conflict: {str(error)}')
    return jsonify({'error_message': str(error)}), 409

def handle_generic_error(error): # Handles 500 errors
    logging.error(f'500 Internal Server Error: {str(error)}')
    return jsonify({'error_message': str(error)}), 500



