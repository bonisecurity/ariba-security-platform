"""Ariba Security Manager - Main Application Entry Point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ariba_manager.app.core.config import settings
from ariba_manager.app.db.session import create_tables, get_db
from ariba_manager.app.api.v1.endpoints.auth import router as auth_router

# Create database tables
create_tables()

app = FastAPI(
    title=settings.project_name,
    description="Ariba Security Platform - Manager Service",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_router, prefix=settings.api_v1_str)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    pass


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    pass


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Ariba Security Manager",
        "version": "0.1.0",
        "status": "operational",
    }