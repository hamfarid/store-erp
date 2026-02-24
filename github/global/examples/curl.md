# cURL Examples — GAARA API

## Health Check
```bash
curl -X GET http://localhost:8000/api/health
```

## Authentication
```bash
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}'
```

## Plant Diagnosis (GAARA-AI)
```bash
curl -X POST http://localhost:8000/api/plant-doctor/diagnose \
  -H "Authorization: Bearer $TOKEN" \
  -F "image=@plant_photo.jpg"
```

## Gold Price Prediction
```bash
curl -X GET http://localhost:8001/api/predict/gold \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```
