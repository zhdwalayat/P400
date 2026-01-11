"""
FastAPI application entry point for the Task Management API.

This module initializes the FastAPI application and registers all routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import settings
from api.database import create_db_and_tables
from api.routes import (
    subjects_router,
    topics_router,
    materials_router,
    tasks_router,
    utils_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: Cleanup if needed
    pass


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with API prefix
app.include_router(subjects_router, prefix=settings.API_PREFIX)
app.include_router(topics_router, prefix=settings.API_PREFIX)
app.include_router(materials_router, prefix=settings.API_PREFIX)
app.include_router(tasks_router, prefix=settings.API_PREFIX)
app.include_router(utils_router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json",
        "endpoints": {
            "subjects": f"{settings.API_PREFIX}/subjects",
            "topics": f"{settings.API_PREFIX}/topics",
            "materials": f"{settings.API_PREFIX}/materials",
            "tasks": f"{settings.API_PREFIX}/tasks",
            "utilities": f"{settings.API_PREFIX}/utils",
            "health": f"{settings.API_PREFIX}/health",
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
