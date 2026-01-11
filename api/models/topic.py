"""
Topic model for tracking topics within subjects.

A Topic represents a specific area of study within a Subject:
- Subject: "Data Structures and Algorithms"
  - Topic: "Binary Search Trees"
  - Topic: "Hash Tables"
  - Topic: "Graph Algorithms"

Topics can have multiple Materials (notes, quizzes, presentations).
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from api.models.subject import Subject
    from api.models.material import Material
    from api.models.task import Task


class TopicBase(SQLModel):
    """Base fields for Topic model."""
    name: str = Field(
        index=True,
        description="Original topic name (e.g., 'Binary Search Trees')"
    )


class Topic(TopicBase, table=True):
    """
    Topic database model.

    Represents a specific topic within a subject.
    Contains multiple materials and can have multiple generation tasks.
    """
    __tablename__ = "topics"

    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = Field(
        index=True,
        description="URL-safe identifier (e.g., 'binary-search-trees')"
    )
    subject_id: int = Field(
        foreign_key="subjects.id",
        index=True,
        description="ID of the parent subject"
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional description of the topic"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the topic was first created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the topic was last updated"
    )

    # Relationships
    subject: Optional["Subject"] = Relationship(back_populates="topics")
    materials: list["Material"] = Relationship(back_populates="topic")
    tasks: list["Task"] = Relationship(back_populates="topic")


class TopicCreate(TopicBase):
    """Schema for creating a new topic."""
    subject_id: int
    description: Optional[str] = None


class TopicUpdate(SQLModel):
    """Schema for updating an existing topic."""
    name: Optional[str] = None
    description: Optional[str] = None


class TopicRead(TopicBase):
    """Schema for reading topic data."""
    id: int
    slug: str
    subject_id: int
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


class TopicReadWithSubject(TopicRead):
    """Schema for reading topic with subject info."""
    subject_name: str
    subject_slug: str


class TopicReadWithCounts(TopicRead):
    """Schema for reading topic with related counts."""
    notes_count: int = 0
    quiz_count: int = 0
    presentation_count: int = 0
