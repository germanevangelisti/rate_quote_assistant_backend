from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import random
import json
import asyncio

app = FastAPI(title="Shipping Quote API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuoteRequest(BaseModel):
    origin: str
    destination: str
    weight: float = Field(..., gt=0)
    shipmentType: str

class QuoteResponse(BaseModel):
    basePrice: float
    weightPrice: float
    totalPrice: float
    estimatedDelivery: str

# Simplified rate calculation logic
def calculate_shipping_rate(origin: str, destination: str, weight: float, shipment_type: str) -> dict:
    # Base price depends on shipment type
    base_price_map = {
        "standard": 10.0,
        "express": 25.0,
        "priority": 50.0
    }
    
    # Rate per kg depends on shipment type
    rate_per_kg_map = {
        "standard": 0.5,
        "express": 1.0,
        "priority": 2.0
    }
    
    # Delivery days estimation
    delivery_days_map = {
        "standard": (5, 7),
        "express": (2, 4),
        "priority": (1, 2)
    }
    
    base_price = base_price_map.get(shipment_type.lower(), 10.0)
    rate_per_kg = rate_per_kg_map.get(shipment_type.lower(), 0.5)
    delivery_range = delivery_days_map.get(shipment_type.lower(), (5, 7))
    
    # Calculate prices
    weight_price = weight * rate_per_kg
    total_price = base_price + weight_price
    
    # Calculate estimated delivery date
    days_to_deliver = random.randint(delivery_range[0], delivery_range[1])
    delivery_date = (datetime.now() + timedelta(days=days_to_deliver)).strftime("%Y-%m-%d")
    
    return {
        "basePrice": base_price,
        "weightPrice": weight_price,
        "totalPrice": total_price,
        "estimatedDelivery": delivery_date
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shipping Quote API"}

@app.post("/quote", response_model=QuoteResponse)
def get_quote(request: QuoteRequest):
    if request.weight <= 0:
        raise HTTPException(status_code=400, detail="Weight must be greater than 0")
    
    quote = calculate_shipping_rate(
        request.origin,
        request.destination,
        request.weight,
        request.shipmentType
    )
    
    return quote

# WebSocket endpoint for real-time quotes
@app.websocket("/ws/quote")
async def websocket_quote(websocket: WebSocket):
    await websocket.accept()
    
    try:
        # Wait for the client to send the quote request
        data = await websocket.receive_text()
        request = json.loads(data)
        
        # Validate the request data
        if not all(key in request for key in ["origin", "destination", "weight", "shipmentType"]):
            await websocket.send_text("Error: Invalid request format. Required fields: origin, destination, weight, shipmentType")
            await websocket.send_text("[END]")
            return
            
        # Send initial message
        await websocket.send_text("Connection established...")
        await asyncio.sleep(0.5)
        
        # Send processing steps with slight delays to simulate real processing
        await websocket.send_text(f"Processing quote request from {request['origin']} to {request['destination']}...")
        await asyncio.sleep(1)
        
        # Calculate base price
        base_price_map = {
            "standard": 10.0,
            "express": 25.0,
            "priority": 50.0
        }
        base_price = base_price_map.get(request['shipmentType'].lower(), 10.0)
        await websocket.send_text(f"Calculating base shipping cost for {request['shipmentType']} delivery...")
        await asyncio.sleep(0.8)
        await websocket.send_text(f"Base price: ${base_price:.2f}")
        await asyncio.sleep(0.5)
        
        # Calculate weight price
        rate_per_kg_map = {
            "standard": 0.5,
            "express": 1.0,
            "priority": 2.0
        }
        rate_per_kg = rate_per_kg_map.get(request['shipmentType'].lower(), 0.5)
        weight_price = float(request['weight']) * rate_per_kg
        await websocket.send_text(f"Calculating additional cost for {request['weight']} kg...")
        await asyncio.sleep(0.8)
        await websocket.send_text(f"Weight cost: ${weight_price:.2f} (${rate_per_kg} per kg)")
        await asyncio.sleep(0.5)
        
        # Calculate total price
        total_price = base_price + weight_price
        await websocket.send_text("Calculating total shipping cost...")
        await asyncio.sleep(0.7)
        await websocket.send_text(f"Total price: ${total_price:.2f}")
        await asyncio.sleep(0.5)
        
        # Calculate delivery estimate
        delivery_days_map = {
            "standard": (5, 7),
            "express": (2, 4),
            "priority": (1, 2)
        }
        delivery_range = delivery_days_map.get(request['shipmentType'].lower(), (5, 7))
        days_to_deliver = random.randint(delivery_range[0], delivery_range[1])
        delivery_date = (datetime.now() + timedelta(days=days_to_deliver)).strftime("%Y-%m-%d")
        
        await websocket.send_text("Calculating estimated delivery date...")
        await asyncio.sleep(0.8)
        await websocket.send_text(f"Estimated delivery: {delivery_date} ({days_to_deliver} days)")
        await asyncio.sleep(0.5)
        
        # Send final summary
        await websocket.send_text("\nQuote Summary:")
        await websocket.send_text(f"From: {request['origin']} To: {request['destination']}")
        await websocket.send_text(f"Weight: {request['weight']} kg, Service: {request['shipmentType']}")
        await websocket.send_text(f"Base Price: ${base_price:.2f}")
        await websocket.send_text(f"Weight Cost: ${weight_price:.2f}")
        await websocket.send_text(f"Total Price: ${total_price:.2f}")
        await websocket.send_text(f"Estimated Delivery: {delivery_date}")
        
        # End the stream
        await asyncio.sleep(0.5)
        await websocket.send_text("[END]")
        
    except WebSocketDisconnect:
        # Handle client disconnect
        pass
    except Exception as e:
        # Handle other errors
        await websocket.send_text(f"Error: {str(e)}")
        await websocket.send_text("[END]")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 