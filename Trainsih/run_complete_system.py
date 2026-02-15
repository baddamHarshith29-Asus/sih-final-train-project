#!/usr/bin/env python3
"""
Complete system runner with testing
"""
import subprocess
import sys
import time
import os
import requests
import json
from pathlib import Path

def test_backend_scenario():
    """Test the backend scenario processing"""
    print("Testing backend scenario processing...")
    
    test_data = {
        "trains": [
            {
                "train_id": "NDLS-PNBE-EXP",
                "name": "New Delhi Patna Express",
                "train_type": "passenger",
                "priority_level": "High",
                "speed_kmph": 80,
                "length_m": 200,
                "sched_departure": "08:00",
                "sched_arrival": "18:00",
                "source": "New Delhi",
                "destination": "Patna Jn",
                "route_path": ["New Delhi", "Kanpur Central", "Patna Jn"]
            },
            {
                "train_id": "NDLS-PNBE-ALT",
                "name": "New Delhi Patna Alternative",
                "train_type": "passenger",
                "priority_level": "Medium",
                "speed_kmph": 60,
                "length_m": 180,
                "sched_departure": "08:30",
                "sched_arrival": "19:00",
                "source": "New Delhi",
                "destination": "Patna Jn",
                "route_path": ["New Delhi", "Kanpur Central", "Patna Jn"]
            }
        ],
        "sections": [
            {"from_node": "New Delhi", "to_node": "Kanpur Central", "travel_time_min": 240.0, "availability": "single", "section_capacity": 1, "signalling": "Automatic Block"},
            {"from_node": "Kanpur Central", "to_node": "Patna Jn", "travel_time_min": 290.0, "availability": "single", "section_capacity": 1, "signalling": "Automatic Block"}
        ],
        "stations": [
            {"station_id": "New Delhi", "platform_count": 16, "platform_length_m": 700, "halt_time_min": 2.0, "station_priority": "major_junction"},
            {"station_id": "Kanpur Central", "platform_count": 8, "platform_length_m": 500, "halt_time_min": 3.0, "station_priority": "major_junction"},
            {"station_id": "Patna Jn", "platform_count": 10, "platform_length_m": 600, "halt_time_min": 2.0, "station_priority": "major_junction"}
        ],
        "constraints": {
            "min_headway_min": 2.0,
            "allow_overtake": True,
            "crossing_rule": "passenger_first",
            "track_conflict_rule": "single_line_opposite_forbidden"
        },
        "simulation": {
            "simulation_speed": "realtime",
            "num_trains": 2,
            "scenario_type": "normal",
            "optimization_goal": "prioritize_passenger"
        }
    }
    
    try:
        response = requests.post('http://localhost:5000/analyze_scenario', 
                               json=test_data, 
                               timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("Backend test successful!")
            print("Conflicts detected:", len(result.get('conflict_analysis', [])))
            print("Decisions made:", len(result.get('decision_reasoning', [])))
            if result.get('gemini_output'):
                print("Gemini integration working!")
            return True
        else:
            print(f"Backend test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Backend test error: {e}")
        return False

def main():
    """Main function"""
    print("Starting Complete Train Control System...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("app.py").exists() or not Path("package.json").exists():
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Install Python dependencies
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("Python dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Python dependencies: {e}")
        sys.exit(1)
    
    # Install Node.js dependencies
    print("Installing Node.js dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True, capture_output=True, shell=True)
        print("Node.js dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Node.js dependencies: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Starting servers...")
    
    # Start backend
    print("Starting backend server...")
    backend_process = subprocess.Popen([sys.executable, "app.py"], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
    time.sleep(5)  # Give backend more time to start
    
    if backend_process.poll() is None:
        print("Backend server started on http://localhost:5000")
    else:
        print("Backend server failed to start")
        sys.exit(1)
    
    # Test backend
    print("Testing backend functionality...")
    if test_backend_scenario():
        print("Backend is working correctly with AI analysis!")
    else:
        print("Backend test failed, but continuing...")
    
    # Start frontend
    print("Starting frontend server...")
    frontend_process = subprocess.Popen(["npm", "run", "dev"], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE,
                                      shell=True)
    time.sleep(3)
    
    if frontend_process.poll() is None:
        print("Frontend server started on http://localhost:8080")
    else:
        print("Frontend server failed to start")
        backend_process.terminate()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("TRAIN CONTROL SYSTEM IS READY!")
    print("=" * 60)
    print("Frontend: http://localhost:8080")
    print("Backend:  http://localhost:5000")
    print("")
    print("USAGE INSTRUCTIONS:")
    print("1. Open http://localhost:8080 in your browser")
    print("2. Go to 'Simulator' tab")
    print("3. Click 'Run Simulator' to see AI analysis")
    print("4. Check 'Analytics' tab for detailed reports")
    print("")
    print("Expected Output Format:")
    print("- Algorithm conflicts with station names")
    print("- AI-driven decisions (PROCEED/HOLD)")
    print("- Detailed Gemini analysis")
    print("")
    print("Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("Backend process stopped")
                break
            if frontend_process.poll() is not None:
                print("Frontend process stopped")
                break
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped")

if __name__ == "__main__":
    main()