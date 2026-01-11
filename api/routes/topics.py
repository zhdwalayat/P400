"""
Topic API endpoints.

Provides CRUD operations for topics:
- GET /topics - List all topics
- POST /topics - Create new topic
- GET /topics/{id} - Get topic by ID
- PUT /topics/{id} - Update topic
- DELETE /topics/{id} - Delete topic
- GET /topics/{id}/materials - List materials for topic
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from api.database import get_db
from api.services.topic_service import TopicService
from api.services.material_service import MaterialService
from api.schemas.topic import (
    TopicCreate,
    TopicUpdate,
    TopicResponse,
    TopicListResponse,
    TopicDetailResponse,
    TopicWithSubjectResponse,
)
from api.schemas.material import MaterialResponse, MaterialListResponse

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=TopicListResponse)
def list_topics(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    subject_id: Optional[int] = Query(None, description="Filter by subject ID"),
    search: Optional[str] = Query(None, description="Search term"),
    db: Session = Depends(get_db)
):
    """List all topics with pagination and optional filters."""
    service = TopicService(db)
    skip = (page - 1) * page_size
    topics, total = service.get_all(
        skip=skip, limit=page_size, subject_id=subject_id, search=search
    )

    return TopicListResponse(
        topics=[TopicResponse.model_validate(t) for t in topics],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=TopicResponse, status_code=201)
def create_topic(
    data: TopicCreate,
    db: Session = Depends(get_db)
):
    """Create a new topic."""
    service = TopicService(db)
    try:
        topic = service.create(data)
        return TopicResponse.model_validate(topic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{topic_id}", response_model=TopicDetailResponse)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    """Get topic by ID with details."""
    service = TopicService(db)
    result = service.get_with_subject_info(topic_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Topic {topic_id} not found")

    topic = result["topic"]
    counts = service.get_material_counts(topic_id)

    return TopicDetailResponse(
        id=topic.id,
        name=topic.name,
        slug=topic.slug,
        subject_id=topic.subject_id,
        description=topic.description,
        created_at=topic.created_at,
        updated_at=topic.updated_at,
        subject_name=result["subject_name"],
        subject_slug=result["subject_slug"],
        **counts
    )


@router.put("/{topic_id}", response_model=TopicResponse)
def update_topic(
    topic_id: int,
    data: TopicUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing topic."""
    service = TopicService(db)
    try:
        updated = service.update(topic_id, data)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Topic {topic_id} not found")
        return TopicResponse.model_validate(updated)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{topic_id}", status_code=204)
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    """Delete a topic."""
    service = TopicService(db)
    if not service.delete(topic_id):
        raise HTTPException(status_code=404, detail=f"Topic {topic_id} not found")


@router.get("/{topic_id}/materials", response_model=MaterialListResponse)
def list_topic_materials(
    topic_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all materials for a topic."""
    topic_service = TopicService(db)
    if not topic_service.get_by_id(topic_id):
        raise HTTPException(status_code=404, detail=f"Topic {topic_id} not found")

    material_service = MaterialService(db)
    skip = (page - 1) * page_size
    materials, total = material_service.get_all(
        skip=skip, limit=page_size, topic_id=topic_id
    )

    return MaterialListResponse(
        materials=[MaterialResponse.model_validate(m) for m in materials],
        total=total,
        page=page,
        page_size=page_size,
    )
