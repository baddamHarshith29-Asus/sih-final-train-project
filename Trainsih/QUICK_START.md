# Quick Start Guide

## Step 1: Start Backend (Required)
Open Command Prompt in project folder and run:
```bash
python start_backend.py
```
Wait until you see: "Running on http://127.0.0.1:5000"

## Step 2: Start Frontend
Open ANOTHER Command Prompt in project folder and run:
```bash
start_frontend.bat
```
Wait until you see: "Local: http://localhost:8080"

## Step 3: Use the Application
1. Open browser: http://localhost:8080
2. Go to "Simulator" tab
3. Fill in train details:
   - Train 1: ID="EXP-001", Source="Mumbai Central", Destination="New Delhi", Priority="High"
   - Train 2: ID="LOCAL-002", Source="Mumbai Central", Destination="New Delhi", Priority="Medium"
4. Click "Run Simulator"
5. Check console output for algorithm results
6. View AI analysis in the interface

## Troubleshooting
- If backend fails: Check Python dependencies with `pip install -r requirements.txt`
- If frontend fails: Check Node.js dependencies with `npm install`
- If "Error running backend scenario": Make sure backend is running first!

## Expected Output
```
Algorithm output:
Conflicts:
('Mumbai Central-New Delhi', 'EXP-001', 'LOCAL-002', (15.0, 240.0))
Decisions:
EXP-001 -> PROCEED
LOCAL-002 -> HOLD
```