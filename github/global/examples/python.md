# Python Examples — GAARA System Integration

## API Client Setup
```python
import requests

BASE_URL = "http://localhost:8000/api"
TOKEN = "your-jwt-token"
headers = {"Authorization": f"Bearer {TOKEN}"}
```

## Plant Disease Detection
```python
with open("plant.jpg", "rb") as img:
    response = requests.post(
        f"{BASE_URL}/plant-doctor/diagnose",
        headers=headers,
        files={"image": img}
    )
    diagnosis = response.json()
    print(f"Disease: {diagnosis['disease']}, Confidence: {diagnosis['confidence']}")
```

## Gold Price Prediction Query
```python
response = requests.get(
    f"{BASE_URL}/predict/gold",
    headers=headers,
    params={"asset": "XAU/USD", "horizon": "7d"}
)
prediction = response.json()
print(f"Predicted: {prediction['price']} ± {prediction['margin']}")
```
