import re
import json
from flask import request, jsonify

def contains_unsanitized_data(data):
    if isinstance(data, str):
        if re.search(r'<script.*?>.*?</script>', data, flags=re.IGNORECASE):
            return "XSS script detected"
        elif re.search(r'<.*?(on\w+|javascript:|data:).*?>', data, flags=re.IGNORECASE):
            return "Potential XSS event handler detected"
        elif re.search(r"(?i)\b(select|insert|update|delete|drop|alter|exec|union|create|grant)\b", data):
            return "SQL injection keywords detected"
    elif isinstance(data, dict):
        for key, value in data.items():
            result = contains_unsanitized_data(value)
            if result:
                return f"In field '{key}': {result}"
    elif isinstance(data, list):
        for item in data:
            result = contains_unsanitized_data(item)
            if result:
                return f"In list item: {result}"
    return None

def reject_unsanitized_data():
    error_message = None
    if request.data:
        if request.is_json:
            data = json.loads(request.get_data(as_text=True))
            error_message = contains_unsanitized_data(data)
        elif request.form:
            error_message = contains_unsanitized_data(request.form)
    
    if not error_message and request.args:
        error_message = contains_unsanitized_data(request.args)
        
    if error_message:
            return jsonify({"error": error_message}), 400
    
    return None
