"""
Material API endpoints.

Provides CRUD operations for materials:
- GET /materials - List all materials
- POST /materials - Create new material
- GET /materials/{id} - Get material by ID
- PUT /materials/{id} - Update material
- DELETE /materials/{id} - Delete material
- GET /materials/{id}/versions - Get version history
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from api.database import get_db
from api.services.material_service import MaterialService
from api.models.base import MaterialType
from api.schemas.material import (
    MaterialCreate,
    MaterialUpdate,
    MaterialResponse,
    MaterialListResponse,
    MaterialDetailResponse,
    MaterialVersionHistoryResponse,
    MaterialVersionResponse,
)

router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("", response_model=MaterialListResponse)
def list_materials(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    topic_id: Optional[int] = Query(None, description="Filter by topic ID"),
    material_type: Optional[MaterialType] = Query(None, description="Filter by type"),
    subject_id: Optional[int] = Query(None, description="Filter by subject ID"),
    db: Session = Depends(get_db)
):
    """List all materials with pagination and optional filters."""
    service = MaterialService(db)
    skip = (page - 1) * page_size
    materials, total = service.get_all(
        skip=skip,
        limit=page_size,
        topic_id=topic_id,
        material_type=material_type,
        subject_id=subject_id
    )

    return MaterialListResponse(
        materials=[MaterialResponse.model_validate(m) for m in materials],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=MaterialResponse, status_code=201)
def create_material(
    data: MaterialCreate,
    db: Session = Depends(get_db)
):
    """Create a new material record."""
    service = MaterialService(db)
    try:
        material = service.create(data)
        return MaterialResponse.model_validate(material)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{material_id}", response_model=MaterialDetailResponse)
def get_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    """Get material by ID with details."""
    service = MaterialService(db)
    result = service.get_with_details(material_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Material {material_id} not found")

    material = result["material"]

    return MaterialDetailResponse(
        id=material.id,
        topic_id=material.topic_id,
        material_type=material.material_type,
        output_format=material.output_format,
        version=material.version,
        file_path=material.file_path,
        file_size=material.file_size,
        created_at=material.created_at,
        updated_at=material.updated_at,
        topic_name=result["topic_name"],
        topic_slug=result["topic_slug"],
        subject_name=result["subject_name"],
        subject_slug=result["subject_slug"],
        metadata=result["metadata"],
        clos=result["clos"] if result["clos"] else None,
    )


@router.put("/{material_id}", response_model=MaterialResponse)
def update_material(
    material_id: int,
    data: MaterialUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing material."""
    service = MaterialService(db)
    updated = service.update(material_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Material {material_id} not found")
    return MaterialResponse.model_validate(updated)


@router.delete("/{material_id}", status_code=204)
def delete_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    """Delete a material."""
    service = MaterialService(db)
    if not service.delete(material_id):
        raise HTTPException(status_code=404, detail=f"Material {material_id} not found")


@router.get("/{material_id}/versions", response_model=MaterialVersionHistoryResponse)
def get_material_versions(
    material_id: int,
    db: Session = Depends(get_db)
):
    """Get version history for a material."""
    service = MaterialService(db)
    material = service.get_by_id(material_id)
    if not material:
        raise HTTPException(status_code=404, detail=f"Material {material_id} not found")

    versions = service.get_version_history(material_id)

    return MaterialVersionHistoryResponse(
        material_id=material_id,
        current_version=material.version,
        versions=[MaterialVersionResponse(**v) for v in versions]
    )


@router.post("/{material_id}/increment-version", response_model=MaterialResponse)
def increment_material_version(
    material_id: int,
    changes_description: str = Query(..., description="Description of changes"),
    db: Session = Depends(get_db)
):
    """Increment material version."""
    service = MaterialService(db)
    material = service.increment_version(material_id, changes_description)
    if not material:
        raise HTTPException(status_code=404, detail=f"Material {material_id} not found")
    return MaterialResponse.model_validate(material)
