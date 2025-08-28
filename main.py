from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
from typing import List, Dict, Any
from datetime import date

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Constants for target APIs
TARGET_API_BASE = "https://tp75fhs.tphomelab.io.vn"
PERFORMANCE_API = f"{TARGET_API_BASE}/performance/batch"
DORM_UTILITIES_API = f"{TARGET_API_BASE}/dorm-utilities/batch"

def clean_none_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove None values and handle date objects"""
    cleaned = {}
    for k, v in data.items():
        if v is None:
            cleaned[k] = ''
        elif isinstance(v, date):
            cleaned[k] = v.isoformat()
        else:
            cleaned[k] = v
    return cleaned

def serialize_data(obj):
    if obj is None:
        return ''
    if isinstance(obj, date):
        return obj.isoformat()
    if hasattr(obj, 'dict'):
        try:
            data = obj.dict()
            return clean_none_values(data)
        except Exception as e:
            logger.error(f"Serialization error: {str(e)}")
            return str(obj)
    return obj

def validate_data(items: list) -> bool:
    if not items:
        return False
    return all(item is not None for item in items)

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return jsonify({'status': 'active', 'message': 'Server Remote api đang chạy!'})

@app.route("/performance/batch", methods=['POST'])
def create_performances_batch():
    try:
        performances = request.get_json()
        if not performances:
            return jsonify({"detail": "No data provided"}), 422

        # Convert models to dict with proper date serialization
        data = []
        for perf in performances:
            try:
                item = clean_none_values(perf)
                data.append(item)
            except Exception as e:
                logger.error(f"Error processing performance data: {str(e)}")
                return jsonify({"detail": f"Data processing error: {str(e)}"}), 422
        
        logger.info(f"Sending data count: {len(data)}")
        
        response = requests.post(
            PERFORMANCE_API, 
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            return jsonify(response.json())
        
        return jsonify({"detail": f"API Error: {response.text}"}), response.status_code
            
    except Exception as e:
        logger.error(f"Error in create_performances_batch: {str(e)}")
        return jsonify({"detail": f"Processing error: {str(e)}"}), 422

@app.route("/dorm-utilities/batch", methods=['POST'])
def create_utilities_batch():
    try:
        utilities = request.get_json()
        if not utilities:
            return jsonify({"detail": "No data provided"}), 422

        data = []
        for util in utilities:
            try:
                item = clean_none_values(util)
                data.append(item)
            except Exception as e:
                logger.error(f"Error processing utilities data: {str(e)}")
                return jsonify({"detail": f"Data processing error: {str(e)}"}), 422

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
        return jsonify({"detail": f"Processing error: {str(e)}"}), 422

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
