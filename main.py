from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
import logging
from models import Performance, DormUtility
from datetime import date

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')  # Changed from @app.route to @app.get
async def home():
    return {'status': 'active', 'message': 'Server Remote api đang chạy!'}

# Constants for target APIs
TARGET_API_BASE = "https://tp75fhs.tphomelab.io.vn/"
PERFORMANCE_API = f"{TARGET_API_BASE}/performance/batch"
DORM_UTILITIES_API = f"{TARGET_API_BASE}/dorm-utilities/batch"

def serialize_data(obj):
    if obj is None:
        return None
    if isinstance(obj, date):
        return obj.isoformat()
    if hasattr(obj, 'dict'):
        try:
            return obj.dict()
        except Exception as e:
            logger.error(f"Serialization error: {str(e)}")
            return str(obj)
    return obj

def validate_data(items: list) -> bool:
    if not items:
        return False
    return all(item is not None for item in items)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

@app.post("/performance/batch", response_model=List[Performance])
async def create_performances_batch(performances: List[Performance]):
    try:
        # Validate input data
        if not validate_data(performances):
            raise ValueError("Invalid or empty performance data")

        # Convert models to dict with proper date serialization
        data = []
        for perf in performances:
            item = {}
            try:
                for k, v in perf.dict().items():
                    item[k] = serialize_data(v)
                data.append(item)
            except Exception as e:
                logger.error(f"Error processing performance data: {str(e)}")
                raise ValueError(f"Data processing error: {str(e)}")
        
        logger.info(f"Sending performance data: {data}")
        
        response = requests.post(
            PERFORMANCE_API, 
            json=data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.text
            try:
                error_json = response.json()
                if 'detail' in error_json:
                    error_detail = error_json['detail']
            except:
                pass
            raise HTTPException(status_code=response.status_code, detail=error_detail)
            
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Request timed out")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Processing error: {str(e)}")

@app.post("/dorm-utilities/batch", response_model=List[DormUtility])
async def create_utilities_batch(utilities: List[DormUtility]):
    try:
        # Validate input data
        if not validate_data(utilities):
            raise ValueError("Invalid or empty utilities data")

        # Convert models to dict with proper date serialization
        data = []
        for util in utilities:
            item = {}
            try:
                for k, v in util.dict().items():
                    item[k] = serialize_data(v)
                data.append(item)
            except Exception as e:
                logger.error(f"Error processing utilities data: {str(e)}")
                raise ValueError(f"Data processing error: {str(e)}")
        
        logger.info(f"Sending utilities data: {data}")
        
        response = requests.post(
            DORM_UTILITIES_API, 
            json=data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            error_detail = response.text
            try:
                error_json = response.json()
                if 'detail' in error_json:
                    error_detail = error_json['detail']
            except:
                pass
            raise HTTPException(status_code=response.status_code, detail=error_detail)
            
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Request timed out")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Request failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Processing error: {str(e)}")
