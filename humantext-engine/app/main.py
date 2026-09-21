from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import sys

# Ensure app directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.v1.endpoints import humanize

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HumanText Engine API",
    description="Advanced Multi-Agent Natural Text Transformation System",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the new endpoint router
app.include_router(humanize.router, prefix="/api/v1", tags=["Humanization"])

@app.get("/")
async def root():
    return {"message": "Welcome to the HumanText Engine API"}

@app.get("/api/v1/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "message": "HumanText Engine is running"},
        status_code=200
    )
