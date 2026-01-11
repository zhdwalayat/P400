"""
Utility API endpoints.

Provides utility operations:
- POST /utils/sanitize - Sanitize a name to slug
- GET /utils/bloom-keywords - Get Bloom's Taxonomy keywords
- GET /health - Health check
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from shared.validators.name_validator import sanitize_name, validate_slug
from api.models.base import get_all_bloom_keywords, BloomLevel


router = APIRouter(tags=["utilities"])


class SanitizeRequest(BaseModel):
    """Request schema for name sanitization."""
    name: str = Field(
        ...,
        min_length=1,
        description="Name to sanitize",
        json_schema_extra={"examples": ["Data Structures and Algorithms"]}
    )


class SanitizeResponse(BaseModel):
    """Response schema for name sanitization."""
    original: str
    slug: str
    is_valid: bool


class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str
    version: str


class BloomKeywordsResponse(BaseModel):
    """Response schema for Bloom's keywords."""
    levels: dict[str, list[str]]
    descriptions: dict[str, str]


@router.post("/utils/sanitize", response_model=SanitizeResponse)
def sanitize_name_endpoint(data: SanitizeRequest):
    """
    Sanitize a name to URL-safe slug.

    Applies sanitization rules:
    1. Convert to lowercase
    2. Replace spaces with hyphens
    3. Remove special characters
    4. Trim leading/trailing hyphens
    """
    slug = sanitize_name(data.name)
    return SanitizeResponse(
        original=data.name,
        slug=slug,
        is_valid=validate_slug(slug)
    )


@router.get("/utils/bloom-keywords", response_model=BloomKeywordsResponse)
def get_bloom_keywords():
    """
    Get all Bloom's Taxonomy keywords.

    Returns action verbs organized by cognitive level.
    Used for CLO alignment in quiz generation.
    """
    keywords = get_all_bloom_keywords()

    descriptions = {
        BloomLevel.REMEMBER.value: "Recall facts and basic concepts",
        BloomLevel.UNDERSTAND.value: "Explain ideas or concepts",
        BloomLevel.APPLY.value: "Use information in new situations",
        BloomLevel.ANALYZE.value: "Draw connections among ideas",
        BloomLevel.EVALUATE.value: "Justify a stand or decision",
        BloomLevel.CREATE.value: "Produce new or original work",
    }

    return BloomKeywordsResponse(
        levels=keywords,
        descriptions=descriptions
    )


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    from api import __version__
    return HealthResponse(
        status="healthy",
        version=__version__
    )
