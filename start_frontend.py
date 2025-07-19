#!/usr/bin/env python3
"""
Simple script to start the frontend application
"""
import os
import sys
import subprocess

def get_python_executable():
    """Get the correct Python executable for the virtual environment"""
    # Check if we're in a virtual environment
    venv_path = r"C:\Users\madhu\OneDrive\Desktop\hachathons\Tata hackathon\project_root\frontend"
    if os.path.exists(venv_path):
        return venv_path
    return sys.executable

def main():
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)
    
    python_exe = get_python_executable()
    
    print("🖥️  Starting Smart EV Frontend Application...")
    print(f"📍 Frontend directory: {frontend_dir}")
    print(f"🐍 Using Python: {python_exe}")
    print("🌐 Make sure the backend is running on http://localhost:8000")
    print("🛑 Close the application window to stop")
    
    try:
        subprocess.run([python_exe, 'main.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed to start: {e}")
        print("💡 Make sure PyQt6 is installed: pip install PyQt6 PyQt6-WebEngine")

if __name__ == "__main__":
    main()
