import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

# Absolute path to your frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

# Mount the frontend directory as static files at /static
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# Serve map.html at root "/"
@app.get("/")
async def serve_map():
    return FileResponse(os.path.join(frontend_dir, "map.html"))