import requests
import json

# Test login with admin credentials
url = "http://localhost:5002/api/auth/login"
data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing login API:")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("\n" + "="*60 + "\n")

try:
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nResponse Body:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
    print(f"Response Text: {response.text if 'response' in locals() else 'N/A'}")
