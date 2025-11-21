from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Dict, Any
import uvicorn, os, time, pickle, json
from pathlib import Path

app = FastAPI(title="IoT SCM Backend (Demo)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL_DIR = Path(__file__).resolve().parent/"models"
DATA_STORE = Path(__file__).resolve().parent.parent/"database"/"data.json"
DATA_STORE.parent.mkdir(parents=True, exist_ok=True)

# load models if present
eta_model = None
spoil_model = None
try:
    eta_model = pickle.load(open(MODEL_DIR/"eta_model.pkl","rb"))
except Exception as e:
    print('ETA model not found or failed to load:', e)
try:
    spoil_model = pickle.load(open(MODEL_DIR/"spoilage_model.pkl","rb"))
except Exception as e:
    print('Spoilage model not found or failed to load:', e)

class SensorData(BaseModel):
    item_id: str
    temperature: float
    humidity: float
    lat: float
    lng: float
    shock: float = 0.0
    timestamp: float

def append_data(d: Dict[str,Any]):
    # append to local JSON list
    if DATA_STORE.exists():
        arr = json.loads(DATA_STORE.read_text())
    else:
        arr = []
    arr.append(d)
    DATA_STORE.write_text(json.dumps(arr, indent=2))

@app.post('/api/push-data')
async def push_data(payload: SensorData):
    d = payload.dict()
    d['received_at'] = time.time()
    append_data(d)
    result = {'status':'ok'}
    # run predictions if models available
    global eta_model, spoil_model
    features = [[d['temperature'], d['humidity'], d['shock']]]
    if eta_model is not None:
        try:
            eta_pred = eta_model.predict(features)[0]
            result['eta_minutes'] = float(eta_pred)
        except Exception as e:
            result['eta_error'] = str(e)
    if spoil_model is not None:
        try:
            spoil_pred = spoil_model.predict(features)[0]
            result['spoilage_risk'] = int(spoil_pred)
        except Exception as e:
            result['spoilage_error'] = str(e)
    return result

@app.get('/api/get-latest')
async def get_latest(n:int=1):
    if not DATA_STORE.exists():
        return []
    arr = json.loads(DATA_STORE.read_text())
    return arr[-n:]

@app.get('/api/health')
async def health():
    return {'status':'ok'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
