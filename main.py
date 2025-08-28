from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
from models import Performance, DormUtility
from datetime import date

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
    if isinstance(obj, date):
        return obj.isoformat()
    return obj.dict()

@app.post("/performance/batch", response_model=List[Performance])
async def create_performances_batch(performances: List[Performance]):
    try:
        # Convert models to dict with proper date serialization
        data = [{k: serialize_data(v) if isinstance(v, date) else v 
                for k, v in perf.dict().items()} 
               for perf in performances]
        
        response = requests.post(PERFORMANCE_API, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.post("/dorm-utilities/batch", response_model=List[DormUtility])
async def create_utilities_batch(utilities: List[DormUtility]):
    try:
        # Convert models to dict with proper date serialization
        data = [{k: serialize_data(v) if isinstance(v, date) else v 
                for k, v in util.dict().items()} 
               for util in utilities]
        
        response = requests.post(DORM_UTILITIES_API, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
