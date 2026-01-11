"""
Notes skill utilities.

Provides:
- Notes content structure generation
- Educational level-based content adaptation
"""

from skills.notes.utils.notes_generator import (
    NotesGenerator,
    get_level_characteristics,
    generate_section_template,
    EDUCATIONAL_LEVELS,
)

__all__ = [
    "NotesGenerator",
    "get_level_characteristics",
    "generate_section_template",
    "EDUCATIONAL_LEVELS",
]
