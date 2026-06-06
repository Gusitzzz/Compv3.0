from flask import request
from config import API_KEY

def validate_api_key():
    api_key = request.headers.get('X-API-Key')
    return api_key == API_KEY