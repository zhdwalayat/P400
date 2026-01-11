"""
API route modules for the Task Management API.

Provides routers for:
- Subject CRUD endpoints
- Topic CRUD endpoints
- Material CRUD endpoints
- Task management endpoints
- Utility endpoints
"""

from api.routes.subjects import router as subjects_router
from api.routes.topics import router as topics_router
from api.routes.materials import router as materials_router
from api.routes.tasks import router as tasks_router
from api.routes.utils import router as utils_router

__all__ = [
    "subjects_router",
    "topics_router",
    "materials_router",
    "tasks_router",
    "utils_router",
]
