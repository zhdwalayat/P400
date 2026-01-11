"""
Subject API endpoints.

Provides CRUD operations for academic subjects:
- GET /subjects - List all subjects
- POST /subjects - Create new subject
- GET /subjects/{slug} - Get subject by slug
- PUT /subjects/{slug} - Update subject
- DELETE /subjects/{slug} - Delete subject
- GET /subjects/{slug}/topics - List topics for subject
- GET /subjects/{slug}/materials - List materials for subject
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from api.database import get_db
from api.services.subject_service import SubjectService
from api.services.topic_service import TopicService
from api.services.material_service import MaterialService
from api.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
    SubjectListResponse,
    SubjectDetailResponse,
)
from api.schemas.topic import TopicResponse, TopicListResponse
from api.schemas.material import MaterialResponse, MaterialListResponse

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("", response_model=SubjectListResponse)
def list_subjects(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    db: Session = Depends(get_db)
):
    """List all subjects with pagination and optional search."""
    service = SubjectService(db)
    skip = (page - 1) * page_size
    subjects, total = service.get_all(skip=skip, limit=page_size, search=search)

    return SubjectListResponse(
        subjects=[SubjectResponse.model_validate(s) for s in subjects],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=SubjectResponse, status_code=201)
def create_subject(
    data: SubjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new subject."""
    service = SubjectService(db)
    try:
        subject = service.create(data)
        return SubjectResponse.model_validate(subject)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{slug}", response_model=SubjectDetailResponse)
def get_subject(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get subject by slug with statistics."""
    service = SubjectService(db)
    subject = service.get_by_slug(slug)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{slug}' not found")

    stats = service.get_statistics(subject.id)

    return SubjectDetailResponse(
        id=subject.id,
        name=subject.name,
        slug=subject.slug,
        description=subject.description,
        created_at=subject.created_at,
        updated_at=subject.updated_at,
        **stats
    )


@router.put("/{slug}", response_model=SubjectResponse)
def update_subject(
    slug: str,
    data: SubjectUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing subject."""
    service = SubjectService(db)
    subject = service.get_by_slug(slug)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{slug}' not found")

    try:
        updated = service.update(subject.id, data)
        return SubjectResponse.model_validate(updated)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{slug}", status_code=204)
def delete_subject(
    slug: str,
    db: Session = Depends(get_db)
):
    """Delete a subject."""
    service = SubjectService(db)
    subject = service.get_by_slug(slug)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{slug}' not found")

    service.delete(subject.id)


@router.get("/{slug}/topics", response_model=TopicListResponse)
def list_subject_topics(
    slug: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all topics for a subject."""
    subject_service = SubjectService(db)
    subject = subject_service.get_by_slug(slug)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{slug}' not found")

    topic_service = TopicService(db)
    skip = (page - 1) * page_size
    topics, total = topic_service.get_by_subject(subject.id, skip=skip, limit=page_size)

    return TopicListResponse(
        topics=[TopicResponse.model_validate(t) for t in topics],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{slug}/materials", response_model=MaterialListResponse)
def list_subject_materials(
    slug: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all materials for a subject."""
    subject_service = SubjectService(db)
    subject = subject_service.get_by_slug(slug)
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{slug}' not found")

    material_service = MaterialService(db)
    skip = (page - 1) * page_size
    materials, total = material_service.get_all(
        skip=skip, limit=page_size, subject_id=subject.id
    )

    return MaterialListResponse(
        materials=[MaterialResponse.model_validate(m) for m in materials],
        total=total,
        page=page,
        page_size=page_size,
    )
