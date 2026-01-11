"""
Pydantic schemas for Task API endpoints.

Defines request and response schemas for:
- Creating tasks
- Updating tasks
- Reading tasks (single, list, by status)
"""

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

from api.models.base import MaterialType, TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new generation task."""
    subject_id: int = Field(
        ...,
        description="ID of the target subject"
    )
    material_type: MaterialType = Field(
        ...,
        description="Type of material to generate"
    )
    topic_id: Optional[int] = Field(
        default=None,
        description="ID of existing topic (if updating)"
    )
    topic_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Topic name (for new topics)"
    )
    input_params: Optional[dict[str, Any]] = Field(
        default=None,
        description="Generation parameters (CLOs, educational level, etc.)"
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    status: Optional[TaskStatus] = Field(
        default=None,
        description="New task status"
    )
    topic_id: Optional[int] = Field(
        default=None,
        description="ID of created/linked topic"
    )
    material_id: Optional[int] = Field(
        default=None,
        description="ID of generated material"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if failed"
    )


class TaskStatusUpdate(BaseModel):
    """Schema for updating only task status."""
    status: TaskStatus = Field(
        ...,
        description="New task status"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message (required if status is 'failed')"
    )


class TaskResponse(BaseModel):
    """Schema for task in API responses."""
    id: int
    subject_id: int
    topic_id: Optional[int]
    topic_name: Optional[str]
    material_type: MaterialType
    status: TaskStatus
    material_id: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class TaskWithDetailsResponse(TaskResponse):
    """Schema for task with subject and topic details."""
    subject_name: str
    subject_slug: str
    topic_slug: Optional[str] = None


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""
    tasks: list[TaskResponse]
    total: int
    page: int = 1
    page_size: int = 20


class TaskDetailResponse(TaskWithDetailsResponse):
    """Schema for detailed task response with input params."""
    input_params: Optional[dict[str, Any]] = None
    duration_seconds: Optional[int] = None  # Time from started to completed


class TaskStatsResponse(BaseModel):
    """Schema for task statistics."""
    total_tasks: int
    pending: int
    in_progress: int
    completed: int
    failed: int
    by_material_type: dict[str, int]
