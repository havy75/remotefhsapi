from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Constants for target APIs
TARGET_API_BASE = "https://tp75fhs.tphomelab.io.vn"
PERFORMANCE_API = f"{TARGET_API_BASE}/performance/batch"
DORM_UTILITIES_API = f"{TARGET_API_BASE}/dorm-utilities/batch"

def clean_none_values(data):
    cleaned = {}
    for k, v in data.items():
        if v is None:
            cleaned[k] = ''
        elif isinstance(v, date):
            cleaned[k] = v.isoformat()
        else:
            cleaned[k] = v
    return cleaned

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return jsonify({'status': 'active', 'message': 'Server Remote api đang chạy!'})

@app.route("/performance/batch", methods=['POST'])
def create_performances_batch():
    try:
        performances = request.get_json()
        data = [clean_none_values(perf) for perf in performances]
        
        response = requests.post(
            PERFORMANCE_API, 
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        return jsonify({"detail": response.text}), response.status_code
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"detail": str(e)}), 422

@app.route("/dorm-utilities/batch", methods=['POST'])
def create_utilities_batch():
    try:
        utilities = request.get_json()
        data = [clean_none_values(util) for util in utilities]
        
        response = requests.post(
            DORM_UTILITIES_API, 
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        return jsonify({"detail": response.text}), response.status_code
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({"detail": str(e)}), 422
