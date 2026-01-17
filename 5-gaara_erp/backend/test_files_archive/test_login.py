#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Login Script
Tests the login functionality by making API calls to the running server.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def get_csrf_token(session):
    """Get CSRF token from the server"""
    try:
        response = session.get(f"{BASE_URL}/api/csrf-token", timeout=10)
        if response.status_code == 200:
            # The CSRF token is set in a cookie, not in the JSON response
            token = session.cookies.get("csrf_token")
            if token:
                print(f"✅ Got CSRF token from cookie: {token[:20]}...")
                return token
            else:
                print("⚠️  No CSRF token in cookies")
                return None
        else:
            print(f"⚠️  Could not get CSRF token, status: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️  Error getting CSRF token: {e}")
        return None


def test_login(username, password):
    """Test login with given credentials"""
    print(f"\n🔍 Testing login with username: {username}")

    try:
        # Create a session to maintain cookies
        session = requests.Session()

        # Get CSRF token
        csrf_token = get_csrf_token(session)

        # Prepare headers
        headers = {"Content-Type": "application/json"}
        if csrf_token:
            # Flask-WTF expects the token in X-CSRF-Token header
            headers["X-CSRF-Token"] = csrf_token

        # Make login request
        response = session.post(
            f"{BASE_URL}/api/user/login",
            json={"username": username, "password": password},
            headers=headers,
            timeout=10,
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        try:
            print(
                f"Response JSON: {json.dumps(response.json(), indent=2, ensure_ascii=False)}"
            )
        except:
            print("(Could not parse as JSON)")

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Login successful!")
                return True
            else:
                print(f"❌ Login failed: {data.get('message')}")
                return False
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error during login: {e}")
        return False


def check_session():
    """Check if session is valid"""
    print("\n🔍 Checking session...")

    try:
        response = requests.get(f"{BASE_URL}/api/user/check-session", timeout=10)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        return response.status_code == 200

    except Exception as e:
        print(f"❌ Error checking session: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("Testing Login Functionality")
    print("=" * 60)

    # Test with admin credentials
    print("\n📝 Attempting login with admin credentials...")
    success = test_login("admin", "admin123")

    if success:
        # Check session
        check_session()
        print("\n✅ Login test passed!")
    else:
        print("\n❌ Login test failed!")
        print("\nℹ️  The admin user might not exist yet.")
        print("   The system will create it automatically on first login attempt.")
        print("   Try logging in through the frontend at: http://localhost:5502")

    print("=" * 60)


if __name__ == "__main__":
    main()
