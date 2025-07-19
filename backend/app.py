from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Handle both relative and absolute imports
try:
    from .routes import location, route, charging
except ImportError:
    from routes import location, route, charging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for tighter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(location.router, prefix="/api/location")
app.include_router(route.router, prefix="/api/route")
app.include_router(charging.router, prefix="/api/charging")

@app.get("/")
def home():
    return {"msg": "Backend running"}
