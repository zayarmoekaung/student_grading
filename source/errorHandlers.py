import json
from flask import jsonify

def handle_bad_request(error):
    return jsonify({"error": "Bad Request", "message": str(error)}), 400

def handle_internal_error(error):
    return jsonify({"error": "Internal Server Error", "message": "Something went wrong on the server."}), 500

def handle_json_decode_error(error):
    return jsonify({"error": "Invalid JSON", "message": "The JSON request body is malformed."}), 400


class ErrorHandlers():
    def init_app(self, app):
        error_handlers = {
        400: handle_bad_request,
        500: handle_internal_error,
        json.JSONDecodeError: handle_json_decode_error
        }
        for error_code, handler in error_handlers.items():
            app.register_error_handler(error_code, handler)

errorhandlers = ErrorHandlers()