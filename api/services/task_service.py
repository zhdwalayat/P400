"""
Task service for business logic operations.

Handles:
- Task CRUD operations
- Task status management
- Task statistics and filtering
"""

import json
from datetime import datetime
from typing import Optional, Any
from sqlmodel import Session, select, func

from api.models.task import Task
from api.models.subject import Subject
from api.models.topic import Topic
from api.models.base import MaterialType, TaskStatus
from api.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate


class TaskService:
    """Service for task-related operations."""

    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session

    def create(self, data: TaskCreate) -> Task:
        """
        Create a new generation task.

        Args:
            data: Task creation data

        Returns:
            Created task

        Raises:
            ValueError: If subject not found
        """
        # Verify subject exists
        subject = self.session.get(Subject, data.subject_id)
        if not subject:
            raise ValueError(f"Subject with ID {data.subject_id} not found")

        # Verify topic if provided
        if data.topic_id:
            topic = self.session.get(Topic, data.topic_id)
            if not topic:
                raise ValueError(f"Topic with ID {data.topic_id} not found")

        # Convert input params to JSON if dict
        input_params_json = None
        if data.input_params:
            input_params_json = json.dumps(data.input_params)

        task = Task(
            subject_id=data.subject_id,
            topic_id=data.topic_id,
            topic_name=data.topic_name,
            material_type=data.material_type,
            input_params=input_params_json,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self.session.get(Task, task_id)

    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[TaskStatus] = None,
        subject_id: Optional[int] = None,
        material_type: Optional[MaterialType] = None
    ) -> tuple[list[Task], int]:
        """
        Get all tasks with pagination and filters.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            status: Optional filter by status
            subject_id: Optional filter by subject
            material_type: Optional filter by material type

        Returns:
            Tuple of (tasks list, total count)
        """
        statement = select(Task)
        count_statement = select(func.count()).select_from(Task)

        if status:
            statement = statement.where(Task.status == status)
            count_statement = count_statement.where(Task.status == status)

        if subject_id:
            statement = statement.where(Task.subject_id == subject_id)
            count_statement = count_statement.where(Task.subject_id == subject_id)

        if material_type:
            statement = statement.where(Task.material_type == material_type)
            count_statement = count_statement.where(
                Task.material_type == material_type
            )

        total = self.session.exec(count_statement).one()

        statement = statement.offset(skip).limit(limit).order_by(
            Task.created_at.desc()
        )
        tasks = list(self.session.exec(statement).all())

        return tasks, total

    def get_pending(self, limit: int = 10) -> list[Task]:
        """Get pending tasks."""
        statement = (
            select(Task)
            .where(Task.status == TaskStatus.PENDING)
            .order_by(Task.created_at.asc())
            .limit(limit)
        )
        return list(self.session.exec(statement).all())

    def update(self, task_id: int, data: TaskUpdate) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: ID of task to update
            data: Update data

        Returns:
            Updated task or None if not found
        """
        task = self.get_by_id(task_id)
        if not task:
            return None

        if data.status is not None:
            task.status = data.status

        if data.topic_id is not None:
            task.topic_id = data.topic_id

        if data.material_id is not None:
            task.material_id = data.material_id

        if data.error_message is not None:
            task.error_message = data.error_message

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update_status(
        self,
        task_id: int,
        data: TaskStatusUpdate
    ) -> Optional[Task]:
        """
        Update task status with appropriate timestamps.

        Args:
            task_id: ID of task
            data: Status update data

        Returns:
            Updated task or None if not found
        """
        task = self.get_by_id(task_id)
        if not task:
            return None

        now = datetime.utcnow()
        task.status = data.status

        if data.status == TaskStatus.IN_PROGRESS and task.started_at is None:
            task.started_at = now

        if data.status in (TaskStatus.COMPLETED, TaskStatus.FAILED):
            task.completed_at = now
            if data.error_message:
                task.error_message = data.error_message

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            task_id: ID of task to delete

        Returns:
            True if deleted, False if not found
        """
        task = self.get_by_id(task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def get_statistics(self) -> dict:
        """
        Get task statistics.

        Returns:
            Dictionary with task counts and statistics
        """
        total = self.session.exec(
            select(func.count()).select_from(Task)
        ).one()

        pending = self.session.exec(
            select(func.count()).select_from(Task)
            .where(Task.status == TaskStatus.PENDING)
        ).one()

        in_progress = self.session.exec(
            select(func.count()).select_from(Task)
            .where(Task.status == TaskStatus.IN_PROGRESS)
        ).one()

        completed = self.session.exec(
            select(func.count()).select_from(Task)
            .where(Task.status == TaskStatus.COMPLETED)
        ).one()

        failed = self.session.exec(
            select(func.count()).select_from(Task)
            .where(Task.status == TaskStatus.FAILED)
        ).one()

        # Count by material type
        by_material_type = {}
        for mt in MaterialType:
            count = self.session.exec(
                select(func.count()).select_from(Task)
                .where(Task.material_type == mt)
            ).one()
            by_material_type[mt.value] = count

        return {
            "total_tasks": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
            "failed": failed,
            "by_material_type": by_material_type,
        }

    def get_with_details(self, task_id: int) -> Optional[dict]:
        """
        Get task with subject and topic details.

        Args:
            task_id: ID of task

        Returns:
            Dictionary with task and related info
        """
        task = self.get_by_id(task_id)
        if not task:
            return None

        subject = self.session.get(Subject, task.subject_id)
        topic = self.session.get(Topic, task.topic_id) if task.topic_id else None

        # Parse input params
        input_params = None
        if task.input_params:
            try:
                input_params = json.loads(task.input_params)
            except json.JSONDecodeError:
                pass

        # Calculate duration
        duration_seconds = None
        if task.started_at and task.completed_at:
            duration_seconds = int(
                (task.completed_at - task.started_at).total_seconds()
            )

        return {
            "task": task,
            "subject_name": subject.name if subject else None,
            "subject_slug": subject.slug if subject else None,
            "topic_slug": topic.slug if topic else None,
            "input_params": input_params,
            "duration_seconds": duration_seconds,
        }
