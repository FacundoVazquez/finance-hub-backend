import logging

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.errors.error_handler import register_error_handlers
from app.routers import assets, health, indicators

logging.basicConfig(level=logging.DEBUG)

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI(title="Finance API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend
    # allow_origins=["*" or "http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)

# API v1 router
api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health.router)
api_v1_router.include_router(assets.router)
api_v1_router.include_router(indicators.router)

app.include_router(api_v1_router)

register_error_handlers(app)
# register_exception_handlers(app)
