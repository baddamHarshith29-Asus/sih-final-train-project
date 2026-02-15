#!/usr/bin/env python3
"""
Simple backend starter
"""
import sys
import os
from app import app

if __name__ == "__main__":
    print("Starting Train Control Backend...")
    print("Backend will run on: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\nBackend stopped")
    except Exception as e:
        print(f"Backend error: {e}")
        sys.exit(1)