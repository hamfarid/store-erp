"""
Script to start test servers for E2E testing
Starts backend and frontend servers for testing
"""

import subprocess
import sys
import time
import os
from pathlib import Path


def start_backend_server():
    """Start backend server"""
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)
    
    print("Starting backend server on port 1005...")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "1005"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    if process.poll() is None:
        print("✓ Backend server started")
        return process
    else:
        print("✗ Backend server failed to start")
        return None


def start_frontend_server():
    """Start frontend server"""
    project_root = Path(__file__).parent.parent.parent
    frontend_dir = project_root / "frontend"
    
    if not frontend_dir.exists():
        print("⚠ Frontend directory not found")
        return None
    
    os.chdir(frontend_dir)
    
    print("Starting frontend server on port 1505...")
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], check=False)
    
    process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "1505"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(5)
    
    if process.poll() is None:
        print("✓ Frontend server started")
        return process
    else:
        print("✗ Frontend server failed to start")
        return None


def check_server_health(url, timeout=10):
    """Check if server is responding"""
    import requests
    
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Starting Test Servers")
    print("=" * 60)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = start_backend_server()
        
        # Start frontend
        frontend_process = start_frontend_server()
        
        if backend_process:
            # Check backend health
            print("\nChecking backend health...")
            if check_server_health("http://localhost:1005/api/v1/health"):
                print("✓ Backend is healthy")
            else:
                print("⚠ Backend may not be ready yet")
        
        if frontend_process:
            # Check frontend
            print("\nChecking frontend...")
            if check_server_health("http://localhost:1505"):
                print("✓ Frontend is ready")
            else:
                print("⚠ Frontend may not be ready yet")
        
        print("\n" + "=" * 60)
        print("Servers are running. Press Ctrl+C to stop.")
        print("=" * 60)
        
        # Keep servers running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
        
        if backend_process:
            backend_process.terminate()
            print("✓ Backend server stopped")
        
        if frontend_process:
            frontend_process.terminate()
            print("✓ Frontend server stopped")
        
        print("\nServers stopped.")


if __name__ == "__main__":
    main()

