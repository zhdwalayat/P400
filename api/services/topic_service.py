"""
Topic service for business logic operations.

Handles:
- Topic CRUD operations
- Topic-subject relationships
- Material counts per topic
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Session, select, func

from api.models.topic import Topic
from api.models.subject import Subject
from api.models.material import Material
from api.models.base import MaterialType
from api.schemas.topic import TopicCreate, TopicUpdate
from shared.validators.name_validator import sanitize_name


class TopicService:
    """Service for topic-related operations."""

    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session

    def create(self, data: TopicCreate) -> Topic:
        """
        Create a new topic.

        Args:
            data: Topic creation data

        Returns:
            Created topic

        Raises:
            ValueError: If subject not found or topic slug already exists for subject
        """
        # Verify subject exists
        subject = self.session.get(Subject, data.subject_id)
        if not subject:
            raise ValueError(f"Subject with ID {data.subject_id} not found")

        slug = sanitize_name(data.name)

        # Check for existing topic with same slug under same subject
        existing = self.get_by_subject_and_slug(data.subject_id, slug)
        if existing:
            raise ValueError(
                f"Topic with slug '{slug}' already exists for subject '{subject.name}'"
            )

        topic = Topic(
            name=data.name,
            slug=slug,
            subject_id=data.subject_id,
            description=data.description,
        )
        self.session.add(topic)
        self.session.commit()
        self.session.refresh(topic)
        return topic

    def get_by_id(self, topic_id: int) -> Optional[Topic]:
        """Get topic by ID."""
        return self.session.get(Topic, topic_id)

    def get_by_subject_and_slug(
        self,
        subject_id: int,
        slug: str
    ) -> Optional[Topic]:
        """Get topic by subject ID and slug."""
        statement = select(Topic).where(
            Topic.subject_id == subject_id,
            Topic.slug == slug
        )
        return self.session.exec(statement).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        subject_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> tuple[list[Topic], int]:
        """
        Get all topics with pagination and optional filters.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            subject_id: Optional filter by subject
            search: Optional search term for name

        Returns:
            Tuple of (topics list, total count)
        """
        statement = select(Topic)
        count_statement = select(func.count()).select_from(Topic)

        if subject_id:
            statement = statement.where(Topic.subject_id == subject_id)
            count_statement = count_statement.where(Topic.subject_id == subject_id)

        if search:
            statement = statement.where(Topic.name.ilike(f"%{search}%"))
            count_statement = count_statement.where(Topic.name.ilike(f"%{search}%"))

        total = self.session.exec(count_statement).one()

        statement = statement.offset(skip).limit(limit).order_by(Topic.name)
        topics = list(self.session.exec(statement).all())

        return topics, total

    def get_by_subject(
        self,
        subject_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[list[Topic], int]:
        """Get all topics for a subject."""
        return self.get_all(skip=skip, limit=limit, subject_id=subject_id)

    def update(self, topic_id: int, data: TopicUpdate) -> Optional[Topic]:
        """
        Update an existing topic.

        Args:
            topic_id: ID of topic to update
            data: Update data

        Returns:
            Updated topic or None if not found
        """
        topic = self.get_by_id(topic_id)
        if not topic:
            return None

        if data.name is not None:
            topic.name = data.name
            topic.slug = sanitize_name(data.name)

        if data.description is not None:
            topic.description = data.description

        topic.updated_at = datetime.utcnow()
        self.session.add(topic)
        self.session.commit()
        self.session.refresh(topic)
        return topic

    def delete(self, topic_id: int) -> bool:
        """
        Delete a topic.

        Args:
            topic_id: ID of topic to delete

        Returns:
            True if deleted, False if not found
        """
        topic = self.get_by_id(topic_id)
        if not topic:
            return False

        self.session.delete(topic)
        self.session.commit()
        return True

    def get_material_counts(self, topic_id: int) -> dict:
        """
        Get material counts for a topic.

        Args:
            topic_id: ID of topic

        Returns:
            Dictionary with counts by material type
        """
        notes_count = self.session.exec(
            select(func.count()).select_from(Material)
            .where(Material.topic_id == topic_id)
            .where(Material.material_type == MaterialType.NOTES)
        ).one()

        quiz_count = self.session.exec(
            select(func.count()).select_from(Material)
            .where(Material.topic_id == topic_id)
            .where(Material.material_type == MaterialType.QUIZ)
        ).one()

        presentation_count = self.session.exec(
            select(func.count()).select_from(Material)
            .where(Material.topic_id == topic_id)
            .where(Material.material_type == MaterialType.PRESENTATION)
        ).one()

        return {
            "notes_count": notes_count,
            "quiz_count": quiz_count,
            "presentation_count": presentation_count,
        }

    def get_with_subject_info(self, topic_id: int) -> Optional[dict]:
        """
        Get topic with subject information.

        Args:
            topic_id: ID of topic

        Returns:
            Dictionary with topic and subject info
        """
        topic = self.get_by_id(topic_id)
        if not topic:
            return None

        subject = self.session.get(Subject, topic.subject_id)

        return {
            "topic": topic,
            "subject_name": subject.name if subject else None,
            "subject_slug": subject.slug if subject else None,
        }
