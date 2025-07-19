#!/usr/bin/env python3
"""
Simple script to start the backend server
"""
import os
import sys
import subprocess

def get_python_executable():
    """Get the correct Python executable for the virtual environment"""
    # Check if we're in a virtual environment
    venv_path = r"C:\Users\madhu\OneDrive\Desktop\hachathons\Tata hackathon\venv\Scripts\python.exe"
    if os.path.exists(venv_path):
        return venv_path
    return sys.executable

def main():
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    python_exe = get_python_executable()
    
    print("🚀 Starting Smart EV Backend Server...")
    print(f"📍 Backend directory: {backend_dir}")
    print(f"🐍 Using Python: {python_exe}")
    
    # Initialize database first
    print("📊 Initializing database...")
    try:
        subprocess.run([python_exe, 'init_db.py'], check=True)
        print("✅ Database initialized successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Database initialization failed: {e}")
        return
    
    # Start the server
    print("🌐 Starting FastAPI server on http://localhost:8000")
    print("📖 API docs will be available at http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([python_exe, 'main.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")

if __name__ == "__main__":
    main()
