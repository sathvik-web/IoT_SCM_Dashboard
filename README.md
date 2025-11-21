# AI-Driven IoT-Inspired Supply Chain Monitoring Dashboard (Hybrid)
A real-time dashboard for monitoring supply-chain package conditions using IoT telemetry and AI models.
The system simulates sensor data (temperature, humidity, shock), predicts delivery ETA and spoilage risk, and visualizes everything in a modern frontend dashboard.

# Project Features
1. Real-Time IoT Telemetry -  Temperature, Humidity, Shock/Vibration, Timestamp, Package ID
2. AI Prediction Models - ETA Prediction (min),Spoilage Risk (0 = Safe, 1 = Warning, 2 = High Risk),Anomaly Detection (Auto detects abnormal sensor behavior)
3. Interactive Frontend Dashboard - Real-time charts, AI prediction panel, Alert system, Latest telemetry panel, Status indicator (Online / Offline)
4. FastAPI Backend 

# Dashboard Preview
<img width="1691" height="877" alt="image" src="https://github.com/user-attachments/assets/a90f649b-295a-49b7-8d58-2310c0753a54" />
<img width="1684" height="594" alt="image" src="https://github.com/user-attachments/assets/5169baa0-a7ad-4708-894d-9c10e91da3de" />

## How to run (local demo)
1. Install dependencies (inside a virtualenv):
```
pip install fastapi uvicorn scikit-learn pandas numpy requests python-multipart
```

2. Start backend:
```
cd backend
uvicorn main:app --reload --port 8000
```

3. In another terminal, run simulator to send simulated telemetry to backend:
```
python ../simulator/sensor_simulator.py --backend http://localhost:8000/api/push-data
```

4. Open `dashboard/index.html` in a browser. The dashboard polls the backend for latest telemetry and displays charts.



