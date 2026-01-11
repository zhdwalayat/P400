"""
Material model for tracking generated educational materials.

A Material represents a generated file:
- Notes (PDF or Markdown)
- Quiz (Word document)
- Presentation (PowerPoint)

Materials are versioned and linked to Topics.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from api.models.base import MaterialType, OutputFormat

if TYPE_CHECKING:
    from api.models.topic import Topic
    from api.models.task import Task
    from api.models.clo import CLO


class MaterialBase(SQLModel):
    """Base fields for Material model."""
    material_type: MaterialType = Field(
        description="Type of material (notes, quiz, presentation)"
    )
    output_format: OutputFormat = Field(
        description="Output file format (pdf, md, docx, pptx)"
    )


class Material(MaterialBase, table=True):
    """
    Material database model.

    Represents a generated educational material file.
    Tracks version history and file location.
    """
    __tablename__ = "materials"

    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int = Field(
        foreign_key="topics.id",
        index=True,
        description="ID of the parent topic"
    )
    version: str = Field(
        default="v1.0",
        description="Version string (e.g., 'v1.0', 'v1.1')"
    )
    file_path: str = Field(
        description="Relative path to the generated file"
    )
    file_size: Optional[int] = Field(
        default=None,
        description="File size in bytes"
    )

    # Type-specific metadata stored as JSON string
    metadata_json: Optional[str] = Field(
        default=None,
        description="JSON string containing material-specific metadata"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the material was first created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the material was last updated"
    )

    # Relationships
    topic: Optional["Topic"] = Relationship(back_populates="materials")
    tasks: list["Task"] = Relationship(back_populates="material")
    clos: list["CLO"] = Relationship(back_populates="material")


class MaterialCreate(MaterialBase):
    """Schema for creating a new material."""
    topic_id: int
    version: str = "v1.0"
    file_path: str
    file_size: Optional[int] = None
    metadata_json: Optional[str] = None


class MaterialUpdate(SQLModel):
    """Schema for updating an existing material."""
    version: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    metadata_json: Optional[str] = None


class MaterialRead(MaterialBase):
    """Schema for reading material data."""
    id: int
    topic_id: int
    version: str
    file_path: str
    file_size: Optional[int]
    created_at: datetime
    updated_at: datetime


class MaterialReadWithTopic(MaterialRead):
    """Schema for reading material with topic info."""
    topic_name: str
    topic_slug: str
    subject_name: str
    subject_slug: str


class MaterialVersionHistory(SQLModel):
    """Schema for version history entry."""
    version: str
    date: str
    changes: str
