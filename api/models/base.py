"""
Base enums and configurations for database models.

Defines all enumeration types used across the application:
- MaterialType: notes, quiz, presentation
- TaskStatus: pending, in_progress, completed, failed
- EducationalLevel: undergraduate, graduate, advanced
- OutputFormat: pdf, md, docx, pptx
- BloomLevel: Bloom's Taxonomy cognitive levels
"""

from enum import Enum


class MaterialType(str, Enum):
    """Types of educational materials that can be generated."""
    NOTES = "notes"
    QUIZ = "quiz"
    PRESENTATION = "presentation"


class TaskStatus(str, Enum):
    """Status states for generation tasks."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class EducationalLevel(str, Enum):
    """Educational levels for content targeting (NOTES skill)."""
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    ADVANCED = "advanced"


class OutputFormat(str, Enum):
    """Output file formats for generated materials."""
    PDF = "pdf"
    MARKDOWN = "md"
    DOCX = "docx"
    PPTX = "pptx"


class BloomLevel(str, Enum):
    """
    Bloom's Taxonomy cognitive levels for quiz questions.

    Used for CLO alignment in QUIZ skill.
    """
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


# Bloom's Taxonomy keywords mapping (from QUIZ.md)
BLOOM_KEYWORDS = {
    BloomLevel.REMEMBER: [
        "define", "list", "label", "name", "identify", "recall", "state",
        "recognize", "describe", "match", "select", "reproduce"
    ],
    BloomLevel.UNDERSTAND: [
        "explain", "describe", "summarize", "interpret", "compare",
        "contrast", "classify", "discuss", "distinguish", "illustrate"
    ],
    BloomLevel.APPLY: [
        "apply", "demonstrate", "solve", "use", "execute", "implement",
        "calculate", "construct", "complete", "practice"
    ],
    BloomLevel.ANALYZE: [
        "analyze", "examine", "compare", "categorize", "differentiate",
        "investigate", "organize", "deconstruct", "attribute", "outline"
    ],
    BloomLevel.EVALUATE: [
        "evaluate", "assess", "justify", "critique", "judge", "defend",
        "recommend", "appraise", "argue", "support"
    ],
    BloomLevel.CREATE: [
        "design", "create", "develop", "formulate", "construct", "propose",
        "generate", "compose", "plan", "produce", "invent"
    ]
}


def get_bloom_keywords(level: BloomLevel) -> list[str]:
    """
    Get action verbs for a Bloom's Taxonomy level.

    Args:
        level: Bloom's Taxonomy level

    Returns:
        List of action verb keywords

    Example:
        >>> get_bloom_keywords(BloomLevel.ANALYZE)
        ['analyze', 'examine', 'compare', ...]
    """
    return BLOOM_KEYWORDS.get(level, [])


def get_all_bloom_keywords() -> dict[str, list[str]]:
    """
    Get all Bloom's Taxonomy keywords.

    Returns:
        Dictionary mapping level names to keyword lists
    """
    return {level.value: keywords for level, keywords in BLOOM_KEYWORDS.items()}
