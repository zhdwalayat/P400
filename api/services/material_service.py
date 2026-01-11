"""
Material service for business logic operations.

Handles:
- Material CRUD operations
- Version tracking
- Material metadata management
"""

import json
from datetime import datetime
from typing import Optional, Any
from sqlmodel import Session, select, func

from api.models.material import Material
from api.models.topic import Topic
from api.models.subject import Subject
from api.models.clo import CLO
from api.models.base import MaterialType, OutputFormat
from api.schemas.material import MaterialCreate, MaterialUpdate
from shared.utils.version_manager import increment_version


class MaterialService:
    """Service for material-related operations."""

    def __init__(self, session: Session):
        """Initialize with database session."""
        self.session = session

    def create(self, data: MaterialCreate) -> Material:
        """
        Create a new material.

        Args:
            data: Material creation data

        Returns:
            Created material

        Raises:
            ValueError: If topic not found
        """
        # Verify topic exists
        topic = self.session.get(Topic, data.topic_id)
        if not topic:
            raise ValueError(f"Topic with ID {data.topic_id} not found")

        material = Material(
            topic_id=data.topic_id,
            material_type=data.material_type,
            output_format=data.output_format,
            version=data.version,
            file_path=data.file_path,
            file_size=data.file_size,
            metadata_json=data.metadata_json,
        )
        self.session.add(material)
        self.session.commit()
        self.session.refresh(material)
        return material

    def get_by_id(self, material_id: int) -> Optional[Material]:
        """Get material by ID."""
        return self.session.get(Material, material_id)

    def get_by_topic_and_type(
        self,
        topic_id: int,
        material_type: MaterialType
    ) -> Optional[Material]:
        """Get latest material by topic and type."""
        statement = (
            select(Material)
            .where(Material.topic_id == topic_id)
            .where(Material.material_type == material_type)
            .order_by(Material.updated_at.desc())
        )
        return self.session.exec(statement).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        topic_id: Optional[int] = None,
        material_type: Optional[MaterialType] = None,
        subject_id: Optional[int] = None
    ) -> tuple[list[Material], int]:
        """
        Get all materials with pagination and filters.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            topic_id: Optional filter by topic
            material_type: Optional filter by type
            subject_id: Optional filter by subject (via topics)

        Returns:
            Tuple of (materials list, total count)
        """
        statement = select(Material)
        count_statement = select(func.count()).select_from(Material)

        if topic_id:
            statement = statement.where(Material.topic_id == topic_id)
            count_statement = count_statement.where(Material.topic_id == topic_id)

        if material_type:
            statement = statement.where(Material.material_type == material_type)
            count_statement = count_statement.where(
                Material.material_type == material_type
            )

        if subject_id:
            topic_ids = self.session.exec(
                select(Topic.id).where(Topic.subject_id == subject_id)
            ).all()
            if topic_ids:
                statement = statement.where(Material.topic_id.in_(topic_ids))
                count_statement = count_statement.where(
                    Material.topic_id.in_(topic_ids)
                )

        total = self.session.exec(count_statement).one()

        statement = statement.offset(skip).limit(limit).order_by(
            Material.updated_at.desc()
        )
        materials = list(self.session.exec(statement).all())

        return materials, total

    def update(self, material_id: int, data: MaterialUpdate) -> Optional[Material]:
        """
        Update an existing material.

        Args:
            material_id: ID of material to update
            data: Update data

        Returns:
            Updated material or None if not found
        """
        material = self.get_by_id(material_id)
        if not material:
            return None

        if data.version is not None:
            material.version = data.version

        if data.file_path is not None:
            material.file_path = data.file_path

        if data.file_size is not None:
            material.file_size = data.file_size

        if data.metadata_json is not None:
            material.metadata_json = data.metadata_json

        material.updated_at = datetime.utcnow()
        self.session.add(material)
        self.session.commit()
        self.session.refresh(material)
        return material

    def delete(self, material_id: int) -> bool:
        """
        Delete a material.

        Args:
            material_id: ID of material to delete

        Returns:
            True if deleted, False if not found
        """
        material = self.get_by_id(material_id)
        if not material:
            return False

        self.session.delete(material)
        self.session.commit()
        return True

    def increment_version(
        self,
        material_id: int,
        changes_description: str
    ) -> Optional[Material]:
        """
        Increment material version and update metadata.

        Args:
            material_id: ID of material
            changes_description: Description of changes

        Returns:
            Updated material or None if not found
        """
        material = self.get_by_id(material_id)
        if not material:
            return None

        new_version = increment_version(material.version)
        material.version = new_version

        # Update metadata with version history
        metadata = {}
        if material.metadata_json:
            try:
                metadata = json.loads(material.metadata_json)
            except json.JSONDecodeError:
                pass

        version_history = metadata.get("version_history", [])
        version_history.append({
            "version": new_version,
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "changes": changes_description
        })
        metadata["version_history"] = version_history
        metadata["current_version"] = new_version
        metadata["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d")

        material.metadata_json = json.dumps(metadata)
        material.updated_at = datetime.utcnow()

        self.session.add(material)
        self.session.commit()
        self.session.refresh(material)
        return material

    def get_version_history(self, material_id: int) -> list[dict]:
        """
        Get version history for a material.

        Args:
            material_id: ID of material

        Returns:
            List of version history entries
        """
        material = self.get_by_id(material_id)
        if not material or not material.metadata_json:
            return []

        try:
            metadata = json.loads(material.metadata_json)
            return metadata.get("version_history", [])
        except json.JSONDecodeError:
            return []

    def get_with_details(self, material_id: int) -> Optional[dict]:
        """
        Get material with topic and subject details.

        Args:
            material_id: ID of material

        Returns:
            Dictionary with material and related info
        """
        material = self.get_by_id(material_id)
        if not material:
            return None

        topic = self.session.get(Topic, material.topic_id)
        subject = self.session.get(Subject, topic.subject_id) if topic else None

        # Get CLOs if it's a quiz
        clos = []
        if material.material_type == MaterialType.QUIZ:
            clos = list(self.session.exec(
                select(CLO).where(CLO.material_id == material_id)
            ).all())

        # Parse metadata
        metadata = None
        if material.metadata_json:
            try:
                metadata = json.loads(material.metadata_json)
            except json.JSONDecodeError:
                pass

        return {
            "material": material,
            "topic_name": topic.name if topic else None,
            "topic_slug": topic.slug if topic else None,
            "subject_name": subject.name if subject else None,
            "subject_slug": subject.slug if subject else None,
            "metadata": metadata,
            "clos": [{"number": c.number, "description": c.description, "bloom_level": c.bloom_level} for c in clos],
        }
