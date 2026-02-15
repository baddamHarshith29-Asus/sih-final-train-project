# Train Control System - Setup Guide

## Quick Start

### Option 1: Using Python Script (Recommended)
```bash
python run_project.py
```

### Option 2: Using Batch File (Windows)
```bash
start.bat
```

### Option 3: Manual Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Node.js Dependencies**
   ```bash
   npm install
   ```

3. **Start Backend Server**
   ```bash
   python app.py
   ```

4. **Start Frontend Server** (in new terminal)
   ```bash
   npm run dev
   ```

## Access Points

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5000

## Key Features Fixed

✅ **Frontend-Backend Communication**
- Added CORS configuration
- Fixed API endpoint routing
- Added Vite proxy configuration

✅ **Error Handling**
- Improved error messages
- Better API response handling
- Graceful fallbacks

✅ **Data Flow**
- Fixed scenario data structure
- Proper train route handling
- Conflict detection working

✅ **UI Components**
- All components properly imported
- Interactive dashboard
- Real-time updates

## Usage

1. Go to **Simulator** tab
2. Enter train parameters
3. Click **Register Conflict** or **Run Simulator**
4. View results in **Conflicts** and **Analytics** tabs

## Troubleshooting

- If backend fails: Check Python dependencies with `pip install -r requirements.txt`
- If frontend fails: Check Node.js dependencies with `npm install`
- If CORS errors: Backend should be running on port 5000
- If API errors: Check that both servers are running

## Project Structure

```
Trainsih/
├── app.py                 # Flask backend
├── scenario_runner.py     # Core logic
├── rail_decision_engine.py # AI algorithms
├── src/
│   ├── components/        # React components
│   └── pages/            # React pages
├── requirements.txt       # Python deps
├── package.json          # Node.js deps
└── run_project.py        # Startup script
```