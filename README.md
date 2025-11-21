# AI-Driven IoT-Inspired Supply Chain Monitoring Dashboard (Hybrid)

This repository implements a **hybrid** IoT-style Supply Chain Monitoring Dashboard that uses **simulated sensors** + **AI models** (ETA prediction & spoilage detection).

**Project contents created automatically for you in this workspace.**

## Quick structure
```
IoT_SCM_Dashboard/
├── backend/
│   ├── main.py              # FastAPI backend
│   ├── firebase_config.py   # Firebase connection
│   ├── models/
│   │   ├── eta_model.pkl
│   │   └── spoilage_model.pkl
│   └── utils/
│       └── anomaly_detector.py
├── simulator/
│   └── sensor_simulator.py  # Simulated IoT sensors that POST to backend
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── database/
│   └── sample_data.json
└── README.md
```

## Resume (local file)
Your uploaded resume is included in this workspace at:
`/mnt/data/cv_resume.docx`

> Use this path if you want to reference your resume in documentation or when zipping projects for submission.

---
## How to run (local demo)
1. Install dependencies (recommended inside a virtualenv):
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

---
## Notes
- This starter uses **synthetic data** and trains simple ML models on generated data so you have runnable `.pkl` models for demo purposes.
- Replace synthetic training with your real dataset if available.
- Firebase integration points are provided in `firebase_config.py` — set your Firebase Realtime DB URL to push data to Firebase if you want real-time cloud storage.
- The frontend is kept minimal and polls backend endpoints for simplicity (no complex websockets).

---
