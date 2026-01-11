"""
CLO (Course Learning Outcome) model for quiz alignment.

CLOs are MANDATORY for QUIZ skill (from QUIZ.md):
- Every quiz question must align to at least one CLO
- Uses Bloom's Taxonomy keywords
- Stored per quiz material

Example CLOs:
1. Analyze the structure and properties of binary search trees
2. Evaluate the efficiency of BST operations in different scenarios
3. Design and implement balanced tree solutions
"""

from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from api.models.base import BloomLevel

if TYPE_CHECKING:
    from api.models.material import Material


class CLOBase(SQLModel):
    """Base fields for CLO model."""
    number: int = Field(
        description="CLO number (1, 2, 3, ...)"
    )
    description: str = Field(
        description="CLO description text"
    )


class CLO(CLOBase, table=True):
    """
    CLO database model.

    Represents a Course Learning Outcome for a quiz.
    Used to track CLO alignment of quiz questions.
    """
    __tablename__ = "clos"

    id: Optional[int] = Field(default=None, primary_key=True)
    material_id: int = Field(
        foreign_key="materials.id",
        index=True,
        description="ID of the quiz material this CLO belongs to"
    )
    bloom_level: Optional[BloomLevel] = Field(
        default=None,
        description="Primary Bloom's Taxonomy level for this CLO"
    )

    # Relationship
    material: Optional["Material"] = Relationship(back_populates="clos")


class CLOCreate(CLOBase):
    """Schema for creating a new CLO."""
    material_id: int
    bloom_level: Optional[BloomLevel] = None


class CLORead(CLOBase):
    """Schema for reading CLO data."""
    id: int
    material_id: int
    bloom_level: Optional[BloomLevel]


class CLOWithKeywords(CLORead):
    """Schema for reading CLO with associated Bloom's keywords."""
    keywords: list[str] = []
