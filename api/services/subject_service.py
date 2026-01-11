"""
Subject service for business logic operations.

Handles:
- Subject CRUD operations
- Slug generation from names
- Subject statistics
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Session, select, func

from api.models.subject import Subject
from api.models.topic import Topic
from api.models.material import Material
from api.models.task import Task
from api.models.base import TaskStatus, MaterialType
from api.schemas.subject import SubjectCreate, SubjectUpdate
from shared.validators.name_validator import sanitize_name


class SubjectService:
    """Service for subject-related operations."""

    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session

    def create(self, data: SubjectCreate) -> Subject:
        """
        Create a new subject.

        Args:
            data: Subject creation data

        Returns:
            Created subject

        Raises:
            ValueError: If subject with same slug already exists
        """
        slug = sanitize_name(data.name)

        # Check for existing subject with same slug
        existing = self.get_by_slug(slug)
        if existing:
            raise ValueError(f"Subject with slug '{slug}' already exists")

        subject = Subject(
            name=data.name,
            slug=slug,
            description=data.description,
        )
        self.session.add(subject)
        self.session.commit()
        self.session.refresh(subject)
        return subject

    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        """Get subject by ID."""
        return self.session.get(Subject, subject_id)

    def get_by_slug(self, slug: str) -> Optional[Subject]:
        """Get subject by slug."""
        statement = select(Subject).where(Subject.slug == slug)
        return self.session.exec(statement).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None
    ) -> tuple[list[Subject], int]:
        """
        Get all subjects with pagination and optional search.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            search: Optional search term for name

        Returns:
            Tuple of (subjects list, total count)
        """
        statement = select(Subject)

        if search:
            statement = statement.where(Subject.name.ilike(f"%{search}%"))

        # Get total count
        count_statement = select(func.count()).select_from(Subject)
        if search:
            count_statement = count_statement.where(Subject.name.ilike(f"%{search}%"))
        total = self.session.exec(count_statement).one()

        # Get paginated results
        statement = statement.offset(skip).limit(limit).order_by(Subject.name)
        subjects = list(self.session.exec(statement).all())

        return subjects, total

    def update(self, subject_id: int, data: SubjectUpdate) -> Optional[Subject]:
        """
        Update an existing subject.

        Args:
            subject_id: ID of subject to update
            data: Update data

        Returns:
            Updated subject or None if not found
        """
        subject = self.get_by_id(subject_id)
        if not subject:
            return None

        if data.name is not None:
            subject.name = data.name
            subject.slug = sanitize_name(data.name)

        if data.description is not None:
            subject.description = data.description

        subject.updated_at = datetime.utcnow()
        self.session.add(subject)
        self.session.commit()
        self.session.refresh(subject)
        return subject

    def delete(self, subject_id: int) -> bool:
        """
        Delete a subject.

        Args:
            subject_id: ID of subject to delete

        Returns:
            True if deleted, False if not found
        """
        subject = self.get_by_id(subject_id)
        if not subject:
            return False

        self.session.delete(subject)
        self.session.commit()
        return True

    def get_statistics(self, subject_id: int) -> dict:
        """
        Get statistics for a subject.

        Args:
            subject_id: ID of subject

        Returns:
            Dictionary with counts and statistics
        """
        subject = self.get_by_id(subject_id)
        if not subject:
            return {}

        # Count topics
        topic_count = self.session.exec(
            select(func.count()).select_from(Topic).where(Topic.subject_id == subject_id)
        ).one()

        # Count materials by type
        topic_ids = self.session.exec(
            select(Topic.id).where(Topic.subject_id == subject_id)
        ).all()

        notes_count = 0
        quiz_count = 0
        presentation_count = 0

        if topic_ids:
            notes_count = self.session.exec(
                select(func.count()).select_from(Material)
                .where(Material.topic_id.in_(topic_ids))
                .where(Material.material_type == MaterialType.NOTES)
            ).one()

            quiz_count = self.session.exec(
                select(func.count()).select_from(Material)
                .where(Material.topic_id.in_(topic_ids))
                .where(Material.material_type == MaterialType.QUIZ)
            ).one()

            presentation_count = self.session.exec(
                select(func.count()).select_from(Material)
                .where(Material.topic_id.in_(topic_ids))
                .where(Material.material_type == MaterialType.PRESENTATION)
            ).one()

        # Count pending tasks
        pending_tasks = self.session.exec(
            select(func.count()).select_from(Task)
            .where(Task.subject_id == subject_id)
            .where(Task.status == TaskStatus.PENDING)
        ).one()

        return {
            "topic_count": topic_count,
            "notes_count": notes_count,
            "quiz_count": quiz_count,
            "presentation_count": presentation_count,
            "pending_tasks": pending_tasks,
        }
