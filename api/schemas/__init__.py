"""
Pydantic schemas for API request/response validation.

Provides schemas for:
- Subject CRUD operations
- Topic CRUD operations
- Material CRUD operations
- Task management
- Utility responses
"""

from api.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
    SubjectListResponse,
    SubjectDetailResponse,
)
from api.schemas.topic import (
    TopicCreate,
    TopicUpdate,
    TopicResponse,
    TopicListResponse,
    TopicDetailResponse,
)
from api.schemas.material import (
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse,
    MaterialListResponse,
    MaterialDetailResponse,
    MaterialVersionResponse,
)
from api.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
    TaskListResponse,
    TaskDetailResponse,
)

__all__ = [
    # Subject
    "SubjectCreate",
    "SubjectUpdate",
    "SubjectResponse",
    "SubjectListResponse",
    "SubjectDetailResponse",
    # Topic
    "TopicCreate",
    "TopicUpdate",
    "TopicResponse",
    "TopicListResponse",
    "TopicDetailResponse",
    # Material
    "MaterialCreate",
    "MaterialUpdate",
    "MaterialResponse",
    "MaterialListResponse",
    "MaterialDetailResponse",
    "MaterialVersionResponse",
    # Task
    "TaskCreate",
    "TaskUpdate",
    "TaskStatusUpdate",
    "TaskResponse",
    "TaskListResponse",
    "TaskDetailResponse",
]
