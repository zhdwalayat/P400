"""
Metadata management utilities for the Educational Material Automation System.

Handles:
- Reading and writing metadata.json files
- Creating initial metadata structures
- Updating metadata for version changes

Metadata Structure (from skill documentation):
{
    "topic": "Binary Search Trees",
    "subject": "Data Structures and Algorithms",
    "current_version": "v1.0",
    "created_date": "2026-01-11",
    "last_updated": "2026-01-11",
    ...material-specific fields...
}
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

from shared.utils.version_manager import increment_version, get_initial_version


def load_metadata(metadata_path: Path) -> Optional[dict[str, Any]]:
    """
    Load metadata from a JSON file.

    Args:
        metadata_path: Path to metadata.json file

    Returns:
        Metadata dictionary or None if file doesn't exist

    Examples:
        >>> metadata = load_metadata(Path("subjects/math/notes/calculus/metadata.json"))
        >>> metadata["topic"]
        'calculus'
    """
    if not metadata_path.exists():
        return None

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def save_metadata(metadata_path: Path, metadata: dict[str, Any]) -> None:
    """
    Save metadata to a JSON file.

    Args:
        metadata_path: Path to metadata.json file
        metadata: Metadata dictionary to save
    """
    # Ensure directory exists
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def create_initial_metadata(
    topic: str,
    subject: str,
    material_type: str,
    output_format: str,
    **additional_fields: Any
) -> dict[str, Any]:
    """
    Create initial metadata structure for new content.

    Args:
        topic: Topic name
        subject: Subject name
        material_type: Type of material (notes, quiz, presentation)
        output_format: Output format (pdf, md, docx, pptx)
        **additional_fields: Material-specific fields

    Returns:
        Initial metadata dictionary

    Examples:
        >>> metadata = create_initial_metadata(
        ...     topic="Binary Search Trees",
        ...     subject="Data Structures",
        ...     material_type="notes",
        ...     output_format="pdf",
        ...     educational_level="Graduate"
        ... )
        >>> metadata["current_version"]
        'v1.0'
    """
    today = datetime.now().strftime('%Y-%m-%d')

    metadata = {
        "topic": topic,
        "subject": subject,
        "material_type": material_type,
        "format": output_format,
        "current_version": get_initial_version(),
        "created_date": today,
        "last_updated": today,
        "version_history": [
            {
                "version": get_initial_version(),
                "date": today,
                "changes": "Initial creation"
            }
        ]
    }

    # Add material-specific fields
    metadata.update(additional_fields)

    return metadata


def update_metadata_version(
    metadata: dict[str, Any],
    changes_description: str
) -> dict[str, Any]:
    """
    Update metadata for a new version.

    Args:
        metadata: Existing metadata dictionary
        changes_description: Description of changes in this version

    Returns:
        Updated metadata dictionary

    Examples:
        >>> metadata = {"current_version": "v1.0", "version_history": [...]}
        >>> updated = update_metadata_version(metadata, "Added AVL rotations")
        >>> updated["current_version"]
        'v1.1'
    """
    today = datetime.now().strftime('%Y-%m-%d')

    # Increment version
    current_version = metadata.get("current_version", "v1.0")
    new_version = increment_version(current_version)

    # Update metadata
    metadata["current_version"] = new_version
    metadata["last_updated"] = today

    # Add to version history
    version_history = metadata.get("version_history", [])
    version_history.append({
        "version": new_version,
        "date": today,
        "changes": changes_description
    })
    metadata["version_history"] = version_history

    return metadata


def create_notes_metadata(
    topic: str,
    subject: str,
    educational_level: str,
    output_format: str,
    references: Optional[list[dict[str, str]]] = None
) -> dict[str, Any]:
    """
    Create metadata specific to NOTES material.

    Args:
        topic: Topic name
        subject: Subject name
        educational_level: Undergraduate/Graduate/Advanced
        output_format: pdf or md
        references: List of reference materials

    Returns:
        Notes-specific metadata dictionary
    """
    return create_initial_metadata(
        topic=topic,
        subject=subject,
        material_type="notes",
        output_format=output_format,
        educational_level=educational_level,
        references=references or []
    )


def create_quiz_metadata(
    topic: str,
    subject: str,
    clos: list[str],
    time_duration: int,
    total_questions: int,
    complexity_levels: list[str],
    question_types: list[str],
    reference: Optional[dict[str, str]] = None
) -> dict[str, Any]:
    """
    Create metadata specific to QUIZ material.

    Args:
        topic: Topic name
        subject: Subject name
        clos: List of Course Learning Outcomes
        time_duration: Duration in minutes
        total_questions: Number of questions
        complexity_levels: Bloom's taxonomy levels used
        question_types: Types of questions included
        reference: Reference material information

    Returns:
        Quiz-specific metadata dictionary
    """
    return create_initial_metadata(
        topic=topic,
        subject=subject,
        material_type="quiz",
        output_format="docx",
        clos=clos,
        time_duration=time_duration,
        total_questions=total_questions,
        complexity_levels=complexity_levels,
        question_types=question_types,
        reference=reference
    )


def create_presentation_metadata(
    topic: str,
    subject: str,
    number_of_slides: int,
    theme: dict[str, str],
    reference: Optional[dict[str, str]] = None,
    features: Optional[list[str]] = None
) -> dict[str, Any]:
    """
    Create metadata specific to PRESENTATION material.

    Args:
        topic: Topic name
        subject: Subject name
        number_of_slides: Total slide count
        theme: Theme information (type, name, colors)
        reference: Reference material information
        features: List of features used (diagrams, highlights, etc.)

    Returns:
        Presentation-specific metadata dictionary
    """
    return create_initial_metadata(
        topic=topic,
        subject=subject,
        material_type="presentation",
        output_format="pptx",
        number_of_slides=number_of_slides,
        theme=theme,
        reference_material=reference,
        features=features or ["Academic tone", "Modern theme"]
    )
