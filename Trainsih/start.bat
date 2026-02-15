@echo off
echo Starting Train Control System...

echo Installing Python dependencies...
pip install -r requirements.txt

echo Starting Backend Server...
start "Backend" cmd /k "python app.py"

timeout /t 3

echo Starting Frontend Server...
start "Frontend" cmd /k "npm run dev"

echo Both servers are starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8080
pause