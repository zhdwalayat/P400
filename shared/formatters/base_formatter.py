"""
Base formatter class for educational material generation.

Provides common functionality for all formatters:
- Path resolution
- Directory creation
- Metadata handling
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

from shared.utils.file_manager import get_material_path, ensure_directory, get_file_name
from shared.utils.metadata_manager import save_metadata
from shared.validators.name_validator import sanitize_name


class BaseFormatter(ABC):
    """Abstract base class for all material formatters."""

    def __init__(self, subject: str, topic: str):
        """
        Initialize formatter with subject and topic.

        Args:
            subject: Subject name (will be sanitized)
            topic: Topic name (will be sanitized)
        """
        self.subject = subject
        self.topic = topic
        self.subject_slug = sanitize_name(subject)
        self.topic_slug = sanitize_name(topic)
        self.created_at = datetime.now()

    @property
    @abstractmethod
    def material_type(self) -> str:
        """Return the material type (notes, quizzes, presentations)."""
        pass

    @property
    @abstractmethod
    def output_format(self) -> str:
        """Return the output format extension (pdf, md, docx, pptx)."""
        pass

    def get_output_directory(self) -> Path:
        """Get the output directory for this material."""
        return get_material_path(self.subject, self.material_type, self.topic)

    def get_output_filename(self) -> str:
        """Get the output filename for this material."""
        return get_file_name(self.topic, self.material_type, self.output_format)

    def get_output_path(self) -> Path:
        """Get the full output path for this material."""
        return self.get_output_directory() / self.get_output_filename()

    def ensure_output_directory(self) -> None:
        """Create output directory if it doesn't exist."""
        ensure_directory(self.get_output_directory())

    def save_metadata(self, metadata: dict[str, Any]) -> None:
        """
        Save metadata to the material directory.

        Args:
            metadata: Metadata dictionary to save
        """
        # Metadata goes in the topic directory, not Slides/ for presentations
        metadata_dir = get_material_path(
            self.subject, self.material_type, self.topic,
            include_slides_subfolder=False
        )
        ensure_directory(metadata_dir)
        metadata_path = metadata_dir / "metadata.json"
        save_metadata(metadata_path, metadata)

    @abstractmethod
    def generate(self, content: dict[str, Any]) -> Path:
        """
        Generate the output file.

        Args:
            content: Content dictionary with material-specific data

        Returns:
            Path to the generated file
        """
        pass

    def _format_date(self, dt: Optional[datetime] = None) -> str:
        """Format datetime for display."""
        if dt is None:
            dt = self.created_at
        return dt.strftime("%Y-%m-%d")

    def _format_version_header(self, version: str) -> str:
        """Format version header string."""
        return f"{version} ({self._format_date()})"
