"""Test login endpoint directly with detailed error logging"""

import sys
import logging

sys.path.insert(0, ".")

# Set up logging to capture errors
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from app import create_app
import json

app = create_app()

# Enable Flask debug mode to see detailed errors
app.config["TESTING"] = True
app.config["DEBUG"] = True

with app.test_client() as client:
    print("Testing login endpoint...")

    # Test login
    try:
        response = client.post(
            "/api/auth/login",
            data=json.dumps({"username": "admin", "password": "admin123"}),
            content_type="application/json",
        )

        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.get_json(), indent=2)}")

        if response.status_code == 200:
            print("\n✅ Login successful!")
        else:
            print("\n❌ Login failed!")
            print(f"Response data: {response.get_data(as_text=True)}")
    except Exception as e:
        print(f"\n❌ Exception during login test: {e}")
        import traceback

        traceback.print_exc()
