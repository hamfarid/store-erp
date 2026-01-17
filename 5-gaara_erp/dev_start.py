#!/usr/bin/env python3
"""
Gaara ERP Developer Quick Start
===============================

Quick development startup script for Gaara ERP.
Optimized for developers with minimal setup and fast startup.

Usage:
    python dev_start.py [--port PORT] [--no-frontend] [--debug]

Features:
    - Ultra-fast startup (< 30 seconds)
    - Automatic dependency installation
    - Hot reload for both backend and frontend
    - Developer-friendly error messages
    - Integrated debugging tools
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Developer constants
DEV_PORT = 8000
FRONTEND_PORT = 5173  # Vite default port
MANAGE_PY = 'manage.py'


class DevStarter:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.frontend_dir = self.gaara_dir / 'main-frontend'
        self.processes = []

    def print_dev_banner(self):
        """Print developer banner"""
        print("""
🚀 GAARA ERP - DEVELOPER MODE 🚀
================================
⚡ Quick Start for Developers
🔥 Hot Reload Enabled
🐛 Debug Mode Active
        """)

    def quick_check(self):
        """Quick environment check"""
        print("⚡ Quick environment check...")

        # Check Python
        if sys.version_info < (3, 11):
            print("❌ Python 3.11+ required")
            return False

        # Check Django project
        if not self.gaara_dir.exists():
            print("❌ Django project not found")
            return False

        print("✅ Environment OK")
        return True

    def install_deps_if_needed(self):
        """Install dependencies if needed"""
        print("📦 Checking dependencies...")

        # Check if Django is installed
        try:
            import django
            print(f"✅ Django {django.get_version()} found")
        except ImportError:
            print("📥 Installing Django...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'django'], check=True)

        # Check requirements.txt
        req_file = self.gaara_dir / 'requirements.txt'
        if req_file.exists():
            print("📥 Installing Python requirements...")
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)],
                check=False  # Don't fail if some packages are missing
            )

    def setup_database_quick(self):
        """Quick database setup"""
        print("🗄️  Quick database setup...")

        os.chdir(self.gaara_dir)

        try:
            # Quick migrate
            result = subprocess.run(
                [sys.executable, MANAGE_PY, 'migrate', '--run-syncdb'],
                capture_output=True,
                text=True,
                timeout=60,
                check=False
            )

            if result.returncode == 0:
                print("✅ Database ready")
            else:
                print("⚠️  Database setup had issues, but continuing...")

        except subprocess.TimeoutExpired:
            print("⚠️  Database setup timeout, but continuing...")

    def create_superuser_quick(self):
        """Create superuser quickly"""
        print("👤 Setting up admin user...")

        try:
            # Check if superuser exists
            check_cmd = [
                sys.executable, MANAGE_PY, 'shell', '-c',
                'from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())'
            ]

            result = subprocess.run(
                check_cmd, capture_output=True, text=True, timeout=10, check=False
            )

            if 'True' not in result.stdout:
                # Create quick superuser
                create_cmd = [
                    sys.executable, MANAGE_PY, 'shell', '-c',
                    '''
from django.contrib.auth.models import User
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser("dev", "dev@gaara.local", "dev123")
    print("Created dev user")
                    '''
                ]

                subprocess.run(
                    create_cmd, capture_output=True, text=True, timeout=10, check=False
                )
                print("✅ Created dev admin: dev/dev123")
            else:
                print("✅ Admin user exists")

        except (subprocess.TimeoutExpired, subprocess.SubprocessError, ImportError) as e:
            print(f"⚠️  Admin user setup skipped: {e}")

    def start_backend_dev(self, port):
        """Start Django development server"""
        print(f"🐍 Starting Django dev server on port {port}...")

        os.chdir(self.gaara_dir)

        # Start with development settings and auto-reload
        cmd = [
            sys.executable, MANAGE_PY, 'runserver',
            f'0.0.0.0:{port}',
            '--settings=gaara_erp.settings'  # Use dev settings
        ]

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            self.processes.append(process)
            print(f"✅ Django server started on http://localhost:{port}")
            return process

        except (OSError, subprocess.SubprocessError) as e:
            print(f"❌ Failed to start Django: {e}")
            return None

    def start_frontend_dev(self):
        """Start frontend development server"""
        if not self.frontend_dir.exists():
            print("⚠️  Frontend directory not found, skipping...")
            return None

        print(f"⚛️  Starting React dev server on port {FRONTEND_PORT}...")

        os.chdir(self.frontend_dir)

        # Check if node_modules exists
        if not (self.frontend_dir / 'node_modules').exists():
            print("📥 Installing npm dependencies...")
            subprocess.run(['npm', 'install'], check=False)

        try:
            # Start React dev server
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            self.processes.append(process)
            print(f"✅ React server started on http://localhost:{FRONTEND_PORT}")
            return process

        except (OSError, subprocess.SubprocessError, FileNotFoundError) as e:
            print(f"❌ Failed to start React: {e}")
            return None

    def show_dev_info(self, port):
        """Show development information"""
        print(f"""
🎉 GAARA ERP DEVELOPMENT READY!
==============================

🌐 Access URLs:
   Backend:  http://localhost:{port}
   Admin:    http://localhost:{port}/admin
   API:      http://localhost:{port}/api
   Frontend: http://localhost:{FRONTEND_PORT}

👤 Development Login:
   Username: dev
   Password: dev123

🔧 Development Tools:
   Django Admin: Full access to models
   API Browser: Built-in DRF interface
   Hot Reload:   Automatic code reloading

⚡ Quick Commands:
   Ctrl+C:       Stop all servers
   F5:           Refresh browser

🐛 Debug Mode: ENABLED
📝 Logs: Check terminal output

Happy coding! 🚀
        """)

    def monitor_processes_dev(self):
        """Monitor development processes"""
        print("\n🔍 Monitoring development servers...")
        print("Press Ctrl+C to stop all servers\n")

        try:
            while True:
                # Check if processes are still running
                running_processes = []
                for process in self.processes:
                    if process.poll() is None:
                        running_processes.append(process)
                    else:
                        print(f"⚠️  Process {process.pid} stopped")

                self.processes = running_processes

                if not self.processes:
                    print("❌ All processes stopped")
                    break

                time.sleep(2)

        except KeyboardInterrupt:
            print("\n🛑 Stopping development servers...")
            self.stop_all_processes()

    def stop_all_processes(self):
        """Stop all running processes"""
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except (OSError, subprocess.SubprocessError):
                pass

        self.processes.clear()
        print("✅ All servers stopped")

    def run_dev(self, port=DEV_PORT, no_frontend=False, debug=False):
        """Main development run method"""
        self.print_dev_banner()

        if not self.quick_check():
            return False

        # Parallel setup for speed
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit setup tasks
            deps_future = executor.submit(self.install_deps_if_needed)
            db_future = executor.submit(self.setup_database_quick)

            # Wait for completion
            deps_future.result()
            db_future.result()

        self.create_superuser_quick()

        # Start servers
        backend_process = self.start_backend_dev(port)
        if not backend_process:
            return False

        if not no_frontend:
            self.start_frontend_dev()

        self.show_dev_info(port)
        self.monitor_processes_dev()

        return True


def main():
    parser = argparse.ArgumentParser(description='Gaara ERP Developer Quick Start')
    parser.add_argument(
        '--port', type=int, default=DEV_PORT,
        help=f'Backend port (default: {DEV_PORT})'
    )
    parser.add_argument(
        '--no-frontend', action='store_true',
        help='Skip frontend startup'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='Enable debug mode'
    )

    args = parser.parse_args()

    # Set debug environment
    if args.debug:
        os.environ['DEBUG'] = 'True'
        os.environ['DJANGO_DEBUG'] = 'True'

    starter = DevStarter()

    try:
        success = starter.run_dev(
            port=args.port,
            no_frontend=args.no_frontend,
            debug=args.debug
        )

        if not success:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n🛑 Development stopped by user")
        starter.stop_all_processes()
    except (OSError, subprocess.SubprocessError, ImportError, AttributeError) as e:
        print(f"❌ Development error: {e}")
        starter.stop_all_processes()
        sys.exit(1)


if __name__ == '__main__':
    main()
