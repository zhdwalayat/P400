"""
Task model for tracking material generation tasks.

A Task represents a request to generate educational material:
- Status tracking (pending -> in_progress -> completed/failed)
- Input parameters storage
- Output material linking
- Error handling

Tasks are the main workflow tracking mechanism.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from api.models.base import MaterialType, TaskStatus

if TYPE_CHECKING:
    from api.models.subject import Subject
    from api.models.topic import Topic
    from api.models.material import Material


class TaskBase(SQLModel):
    """Base fields for Task model."""
    material_type: MaterialType = Field(
        description="Type of material to generate"
    )


class Task(TaskBase, table=True):
    """
    Task database model.

    Represents a material generation task/request.
    Tracks the entire lifecycle from pending to completed/failed.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(
        foreign_key="subjects.id",
        index=True,
        description="ID of the target subject"
    )
    topic_id: Optional[int] = Field(
        default=None,
        foreign_key="topics.id",
        index=True,
        description="ID of the target topic (may be created during task)"
    )
    topic_name: Optional[str] = Field(
        default=None,
        description="Topic name (used before topic is created)"
    )
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        index=True,
        description="Current task status"
    )

    # Input parameters stored as JSON string
    input_params: Optional[str] = Field(
        default=None,
        description="JSON string containing generation parameters"
    )

    # Output tracking
    material_id: Optional[int] = Field(
        default=None,
        foreign_key="materials.id",
        description="ID of the generated material (when completed)"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message (when failed)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the task was created"
    )
    started_at: Optional[datetime] = Field(
        default=None,
        description="When processing started"
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="When processing completed (success or failure)"
    )

    # Relationships
    subject: Optional["Subject"] = Relationship(back_populates="tasks")
    topic: Optional["Topic"] = Relationship(back_populates="tasks")
    material: Optional["Material"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    subject_id: int
    topic_id: Optional[int] = None
    topic_name: Optional[str] = None
    input_params: Optional[str] = None


class TaskUpdate(SQLModel):
    """Schema for updating an existing task."""
    status: Optional[TaskStatus] = None
    topic_id: Optional[int] = None
    material_id: Optional[int] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TaskRead(TaskBase):
    """Schema for reading task data."""
    id: int
    subject_id: int
    topic_id: Optional[int]
    topic_name: Optional[str]
    status: TaskStatus
    material_id: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]


class TaskReadWithDetails(TaskRead):
    """Schema for reading task with related info."""
    subject_name: str
    subject_slug: str
    topic_slug: Optional[str]


class TaskStatusUpdate(SQLModel):
    """Schema for updating task status."""
    status: TaskStatus
    error_message: Optional[str] = None
