# Quote Assistant Backend

This is the backend for the Quote Assistant application. It's built with FastAPI.

## Getting Started

1. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Start the development server
```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /`: Root endpoint
- `POST /quote`: Calculate a shipping quote

### Quote Request Format

```json
{
  "origin": "New York",
  "destination": "Los Angeles",
  "weight": 10.5,
  "shipmentType": "standard"
}
```

### Quote Response Format

```json
{
  "basePrice": 10.0,
  "weightPrice": 5.25,
  "totalPrice": 15.25,
  "estimatedDelivery": "2023-05-15"
}
```

## Documentation

API documentation is automatically generated and available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 