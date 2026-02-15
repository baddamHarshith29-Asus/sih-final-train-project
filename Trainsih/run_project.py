#!/usr/bin/env python3
"""
Script to run the Train Control System project
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def install_python_deps():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Python dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Python dependencies: {e}")
        return False
    return True

def install_node_deps():
    """Install Node.js dependencies"""
    print("Installing Node.js dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True, shell=True)
        print("✓ Node.js dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install Node.js dependencies: {e}")
        return False
    return True

def start_backend():
    """Start the Flask backend server"""
    print("Starting backend server...")
    try:
        backend_process = subprocess.Popen([sys.executable, "app.py"], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE)
        time.sleep(3)  # Give backend time to start
        if backend_process.poll() is None:
            print("✓ Backend server started on http://localhost:5000")
            return backend_process
        else:
            print("✗ Backend server failed to start")
            return None
    except Exception as e:
        print(f"✗ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the Vite frontend server"""
    print("Starting frontend server...")
    try:
        frontend_process = subprocess.Popen(["npm", "run", "dev"], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE,
                                          shell=True)
        time.sleep(3)  # Give frontend time to start
        if frontend_process.poll() is None:
            print("✓ Frontend server started on http://localhost:8080")
            return frontend_process
        else:
            print("✗ Frontend server failed to start")
            return None
    except Exception as e:
        print(f"✗ Failed to start frontend: {e}")
        return None

def main():
    """Main function to run the project"""
    print("🚂 Starting Train Control System...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists() or not Path("package.json").exists():
        print("✗ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    if not install_python_deps():
        sys.exit(1)
    
    if not install_node_deps():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Starting servers...")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Train Control System is running!")
    print("Frontend: http://localhost:8080")
    print("Backend:  http://localhost:5000")
    print("Press Ctrl+C to stop both servers")
    print("=" * 50)
    
    try:
        # Keep both processes running
        while True:
            time.sleep(1)
            # Check if processes are still running
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
        print("✓ Servers stopped")

if __name__ == "__main__":
    main()