"""
Pydantic schemas for Subject API endpoints.

Defines request and response schemas for:
- Creating subjects
- Updating subjects
- Reading subjects (single and list)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SubjectCreate(BaseModel):
    """Schema for creating a new subject."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Subject name (e.g., 'Data Structures and Algorithms')",
        json_schema_extra={"examples": ["Data Structures and Algorithms"]}
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional description of the subject"
    )


class SubjectUpdate(BaseModel):
    """Schema for updating an existing subject."""
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="New subject name"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="New description"
    )


class SubjectResponse(BaseModel):
    """Schema for subject in API responses."""
    id: int
    name: str
    slug: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SubjectListResponse(BaseModel):
    """Schema for list of subjects response."""
    subjects: list[SubjectResponse]
    total: int
    page: int = 1
    page_size: int = 20


class SubjectDetailResponse(SubjectResponse):
    """Schema for detailed subject response with counts."""
    topic_count: int = 0
    notes_count: int = 0
    quiz_count: int = 0
    presentation_count: int = 0
    pending_tasks: int = 0
