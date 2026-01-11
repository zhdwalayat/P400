"""
Pydantic schemas for Material API endpoints.

Defines request and response schemas for:
- Creating materials
- Updating materials
- Reading materials (single, list, versions)
"""

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field

from api.models.base import MaterialType, OutputFormat


class MaterialCreate(BaseModel):
    """Schema for creating a new material."""
    topic_id: int = Field(
        ...,
        description="ID of the parent topic"
    )
    material_type: MaterialType = Field(
        ...,
        description="Type of material (notes, quiz, presentation)"
    )
    output_format: OutputFormat = Field(
        ...,
        description="Output format (pdf, md, docx, pptx)"
    )
    version: str = Field(
        default="v1.0",
        description="Version string"
    )
    file_path: str = Field(
        ...,
        description="Relative path to the generated file"
    )
    file_size: Optional[int] = Field(
        default=None,
        description="File size in bytes"
    )
    metadata_json: Optional[str] = Field(
        default=None,
        description="JSON string containing material-specific metadata"
    )


class MaterialUpdate(BaseModel):
    """Schema for updating an existing material."""
    version: Optional[str] = Field(
        default=None,
        description="New version string"
    )
    file_path: Optional[str] = Field(
        default=None,
        description="New file path"
    )
    file_size: Optional[int] = Field(
        default=None,
        description="New file size"
    )
    metadata_json: Optional[str] = Field(
        default=None,
        description="New metadata JSON"
    )


class MaterialResponse(BaseModel):
    """Schema for material in API responses."""
    id: int
    topic_id: int
    material_type: MaterialType
    output_format: OutputFormat
    version: str
    file_path: str
    file_size: Optional[int]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MaterialWithTopicResponse(MaterialResponse):
    """Schema for material with topic and subject information."""
    topic_name: str
    topic_slug: str
    subject_name: str
    subject_slug: str


class MaterialListResponse(BaseModel):
    """Schema for list of materials response."""
    materials: list[MaterialResponse]
    total: int
    page: int = 1
    page_size: int = 20


class MaterialDetailResponse(MaterialWithTopicResponse):
    """Schema for detailed material response with metadata."""
    metadata: Optional[dict[str, Any]] = None
    clos: Optional[list[dict[str, Any]]] = None  # For quiz materials


class MaterialVersionResponse(BaseModel):
    """Schema for version history entry."""
    version: str
    date: str
    changes: str


class MaterialVersionHistoryResponse(BaseModel):
    """Schema for material version history."""
    material_id: int
    current_version: str
    versions: list[MaterialVersionResponse]
