"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

Simple server runner
"""

import os
import subprocess
import sys


def main():
    """Run the main server"""
    # Get the path to main.py
    backend_dir = os.path.dirname(__file__)
    main_py_path = os.path.join(backend_dir, "src", "main.py")

    if not os.path.exists(main_py_path):
        print(f"❌ main.py not found at {main_py_path}")
        return 1

    print("🚀 Starting inventory management server...")
    print(f"📁 Running: {main_py_path}")

    try:
        # Run main.py directly
        result = subprocess.run(
            [sys.executable, main_py_path],
            cwd=os.path.dirname(main_py_path),
            check=False,
        )
        return result.returncode
    except KeyboardInterrupt:
        print("\n⏹️ Server stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error running server: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
