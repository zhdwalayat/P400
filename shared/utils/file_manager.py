"""
File management utilities for the Educational Material Automation System.

Handles:
- Storage path resolution based on CLAUDE.md specifications
- Directory creation
- Topic existence checking for version management

Storage Paths (from CLAUDE.md):
- Notes: subjects/{subject}/notes/{topic}/{topic}.pdf or .md
- Quizzes: subjects/{subject}/quizzes/{topic}/{topic}-quiz.docx
- Presentations: subjects/{subject}/presentations/{topic}/Slides/{topic}.pptx
"""

import os
from pathlib import Path
from typing import Optional, Literal

from shared.validators.name_validator import sanitize_name


# Base path for all generated content
BASE_PATH = Path(__file__).parent.parent.parent / "subjects"

MaterialType = Literal["notes", "quizzes", "presentations"]
OutputFormat = Literal["pdf", "md", "docx", "pptx"]


def get_base_path() -> Path:
    """
    Get the base path for all generated content.

    Returns:
        Path to the subjects/ directory
    """
    return BASE_PATH


def get_material_path(
    subject: str,
    material_type: MaterialType,
    topic: str,
    include_slides_subfolder: bool = True
) -> Path:
    """
    Get the storage directory path for a material.

    Args:
        subject: Subject name (will be sanitized)
        material_type: Type of material (notes, quizzes, presentations)
        topic: Topic name (will be sanitized)
        include_slides_subfolder: For presentations, include the Slides/ subfolder

    Returns:
        Path to the material directory

    Examples:
        >>> get_material_path("Data Structures", "notes", "Binary Search Trees")
        Path('.../subjects/data-structures/notes/binary-search-trees')
        >>> get_material_path("Chemistry", "quizzes", "Alkene Reactions")
        Path('.../subjects/chemistry/quizzes/alkene-reactions')
        >>> get_material_path("History", "presentations", "French Revolution")
        Path('.../subjects/history/presentations/french-revolution/Slides')
    """
    subject_slug = sanitize_name(subject)
    topic_slug = sanitize_name(topic)

    base = BASE_PATH / subject_slug / material_type / topic_slug

    if material_type == "presentations" and include_slides_subfolder:
        return base / "Slides"
    return base


def get_file_name(
    topic: str,
    material_type: MaterialType,
    output_format: OutputFormat
) -> str:
    """
    Get the file name for a material.

    Args:
        topic: Topic name (will be sanitized)
        material_type: Type of material
        output_format: Output format extension

    Returns:
        File name string

    Examples:
        >>> get_file_name("Binary Search Trees", "notes", "pdf")
        'binary-search-trees.pdf'
        >>> get_file_name("Alkene Reactions", "quizzes", "docx")
        'alkene-reactions-quiz.docx'
        >>> get_file_name("French Revolution", "presentations", "pptx")
        'french-revolution.pptx'
    """
    topic_slug = sanitize_name(topic)

    if material_type == "quizzes":
        return f"{topic_slug}-quiz.{output_format}"
    return f"{topic_slug}.{output_format}"


def get_full_file_path(
    subject: str,
    material_type: MaterialType,
    topic: str,
    output_format: OutputFormat
) -> Path:
    """
    Get the full file path for a material including filename.

    Args:
        subject: Subject name
        material_type: Type of material
        topic: Topic name
        output_format: Output format extension

    Returns:
        Full path to the file
    """
    directory = get_material_path(subject, material_type, topic)
    filename = get_file_name(topic, material_type, output_format)
    return directory / filename


def ensure_directory(path: Path) -> None:
    """
    Create directory if it doesn't exist.

    Args:
        path: Directory path to create
    """
    path.mkdir(parents=True, exist_ok=True)


def check_topic_exists(
    subject: str,
    material_type: MaterialType,
    topic: str
) -> bool:
    """
    Check if a topic directory already exists (for version management).

    Used to determine if we should create v1.0 or increment version.

    Args:
        subject: Subject name
        material_type: Type of material
        topic: Topic name

    Returns:
        True if the topic directory exists, False otherwise
    """
    # For presentations, check the parent directory (not Slides/)
    path = get_material_path(subject, material_type, topic, include_slides_subfolder=False)
    return path.exists()


def list_topics_for_subject(
    subject: str,
    material_type: MaterialType
) -> list[str]:
    """
    List all topics for a given subject and material type.

    Args:
        subject: Subject name
        material_type: Type of material

    Returns:
        List of topic slugs
    """
    subject_slug = sanitize_name(subject)
    material_dir = BASE_PATH / subject_slug / material_type

    if not material_dir.exists():
        return []

    return [
        d.name for d in material_dir.iterdir()
        if d.is_dir() and not d.name.startswith('.')
    ]


def list_subjects() -> list[str]:
    """
    List all subjects.

    Returns:
        List of subject slugs
    """
    if not BASE_PATH.exists():
        return []

    return [
        d.name for d in BASE_PATH.iterdir()
        if d.is_dir() and not d.name.startswith('.')
    ]


def get_metadata_path(
    subject: str,
    material_type: MaterialType,
    topic: str
) -> Path:
    """
    Get the path to the metadata.json file for a material.

    Args:
        subject: Subject name
        material_type: Type of material
        topic: Topic name

    Returns:
        Path to metadata.json
    """
    # Metadata is stored in the topic directory (not Slides/ for presentations)
    path = get_material_path(subject, material_type, topic, include_slides_subfolder=False)
    return path / "metadata.json"
