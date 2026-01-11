"""
Pydantic schemas for Topic API endpoints.

Defines request and response schemas for:
- Creating topics
- Updating topics
- Reading topics (single and list)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TopicCreate(BaseModel):
    """Schema for creating a new topic."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Topic name (e.g., 'Binary Search Trees')",
        json_schema_extra={"examples": ["Binary Search Trees"]}
    )
    subject_id: int = Field(
        ...,
        description="ID of the parent subject"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional description of the topic"
    )


class TopicUpdate(BaseModel):
    """Schema for updating an existing topic."""
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="New topic name"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="New description"
    )


class TopicResponse(BaseModel):
    """Schema for topic in API responses."""
    id: int
    name: str
    slug: str
    subject_id: int
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TopicWithSubjectResponse(TopicResponse):
    """Schema for topic with subject information."""
    subject_name: str
    subject_slug: str


class TopicListResponse(BaseModel):
    """Schema for list of topics response."""
    topics: list[TopicResponse]
    total: int
    page: int = 1
    page_size: int = 20


class TopicDetailResponse(TopicWithSubjectResponse):
    """Schema for detailed topic response with material counts."""
    notes_count: int = 0
    quiz_count: int = 0
    presentation_count: int = 0
    latest_notes_version: Optional[str] = None
    latest_quiz_version: Optional[str] = None
    latest_presentation_version: Optional[str] = None
