from datetime import datetime
import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for tighter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(location.router, prefix="/api/location")
# app.include_router(route.router, prefix="/api/route")
# app.include_router(charging.router, prefix="/api/charging")

# Absolute path to your frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

# Mount the frontend directory as static files at /static
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Serve map.html at root "/"
@app.get("/")
async def serve_map():
    return FileResponse(os.path.join(frontend_dir, "map.html"))

@app.get("/get_weather_info")
async def get_weather_info(country: str = "India", city: str = "Delhi"):
    URL = f"https://www.timeanddate.com/weather/{country}/{city}"   # sample request URL -> http://127.0.0.1:8000/get_weather_info?country=India&city=Delhi

    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find temperature and weather description
    temperature = soup.find("div", class_="h2").text.strip()
    desc = soup.find("p").text.strip()

    return {"temperature": temperature, "description": desc}


class LocationUpdate(BaseModel):
    lat: float
    lng: float
    batteryLevel: float = Field(..., ge=0, le=100)
    timestamp: Optional[int]  # milliseconds since epoch

class ChargingStation(BaseModel):
    lat: float
    lon: float
    name: str

# @app.post("/api/location/update")
# async def update_location(data: LocationUpdate):
#     print(f"Received location update at {datetime.now()}: {data}")
    
#     # Logic: Redirect if battery < 20%
#     if data.batteryLevel < 20:
#         # Simulated nearby charging station
#         station = ChargingStation(
#             lat=data.lat + 0.005,  # just a nearby point
#             lon=data.lng + 0.005,
#             name="GreenCharge Station - Sector 5"
#         )
#         return {
#             "redirectToChargingStation": True,
#             "station": station
#         }