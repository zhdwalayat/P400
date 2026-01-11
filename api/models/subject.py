"""
Subject model for tracking academic subjects.

A Subject represents an academic discipline or course area:
- "Data Structures and Algorithms"
- "Organic Chemistry"
- "European History"

Subjects contain Topics, which in turn have Materials.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from api.models.topic import Topic
    from api.models.task import Task


class SubjectBase(SQLModel):
    """Base fields for Subject model."""
    name: str = Field(
        index=True,
        description="Original subject name (e.g., 'Data Structures and Algorithms')"
    )


class Subject(SubjectBase, table=True):
    """
    Subject database model.

    Represents an academic subject/course area.
    Contains multiple topics and can have multiple generation tasks.
    """
    __tablename__ = "subjects"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(
        unique=True,
        index=True,
        description="URL-safe identifier (e.g., 'data-structures-and-algorithms')"
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional description of the subject"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the subject was first created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the subject was last updated"
    )

    # Relationships
    topics: list["Topic"] = Relationship(back_populates="subject")
    tasks: list["Task"] = Relationship(back_populates="subject")


class SubjectCreate(SubjectBase):
    """Schema for creating a new subject."""
    description: Optional[str] = None


class SubjectUpdate(SQLModel):
    """Schema for updating an existing subject."""
    name: Optional[str] = None
    description: Optional[str] = None


class SubjectRead(SubjectBase):
    """Schema for reading subject data."""
    id: int
    slug: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


class SubjectReadWithCounts(SubjectRead):
    """Schema for reading subject with related counts."""
    topic_count: int = 0
    material_count: int = 0
    task_count: int = 0
