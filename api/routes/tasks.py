"""
Task API endpoints.

Provides operations for generation tasks:
- GET /tasks - List all tasks
- POST /tasks - Create new task
- GET /tasks/{id} - Get task by ID
- PUT /tasks/{id}/status - Update task status
- DELETE /tasks/{id} - Delete task
- GET /tasks/pending - Get pending tasks
- GET /tasks/stats - Get task statistics
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from api.database import get_db
from api.services.task_service import TaskService
from api.models.base import MaterialType, TaskStatus
from api.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
    TaskListResponse,
    TaskDetailResponse,
    TaskStatsResponse,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/stats", response_model=TaskStatsResponse)
def get_task_statistics(
    db: Session = Depends(get_db)
):
    """Get task statistics."""
    service = TaskService(db)
    stats = service.get_statistics()
    return TaskStatsResponse(**stats)


@router.get("/pending", response_model=list[TaskResponse])
def get_pending_tasks(
    limit: int = Query(10, ge=1, le=50, description="Maximum tasks to return"),
    db: Session = Depends(get_db)
):
    """Get pending tasks."""
    service = TaskService(db)
    tasks = service.get_pending(limit=limit)
    return [TaskResponse.model_validate(t) for t in tasks]


@router.get("", response_model=TaskListResponse)
def list_tasks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    subject_id: Optional[int] = Query(None, description="Filter by subject ID"),
    material_type: Optional[MaterialType] = Query(None, description="Filter by type"),
    db: Session = Depends(get_db)
):
    """List all tasks with pagination and optional filters."""
    service = TaskService(db)
    skip = (page - 1) * page_size
    tasks, total = service.get_all(
        skip=skip,
        limit=page_size,
        status=status,
        subject_id=subject_id,
        material_type=material_type
    )

    return TaskListResponse(
        tasks=[TaskResponse.model_validate(t) for t in tasks],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db)
):
    """Create a new generation task."""
    service = TaskService(db)
    try:
        task = service.create(data)
        return TaskResponse.model_validate(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}", response_model=TaskDetailResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Get task by ID with details."""
    service = TaskService(db)
    result = service.get_with_details(task_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    task = result["task"]

    return TaskDetailResponse(
        id=task.id,
        subject_id=task.subject_id,
        topic_id=task.topic_id,
        topic_name=task.topic_name,
        material_type=task.material_type,
        status=task.status,
        material_id=task.material_id,
        error_message=task.error_message,
        created_at=task.created_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        subject_name=result["subject_name"],
        subject_slug=result["subject_slug"],
        topic_slug=result["topic_slug"],
        input_params=result["input_params"],
        duration_seconds=result["duration_seconds"],
    )


@router.put("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    data: TaskStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update task status."""
    service = TaskService(db)
    task = service.update_status(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update task fields."""
    service = TaskService(db)
    task = service.update(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Delete a task."""
    service = TaskService(db)
    if not service.delete(task_id):
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
