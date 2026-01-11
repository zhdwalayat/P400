"""
Bloom's Taxonomy utilities for quiz generation.

Provides:
- Keywords for each cognitive level
- Level identification from text
- Action verb selection
- CLO-Bloom alignment validation

Bloom's Taxonomy Levels (from QUIZ.md):
1. Remember - Recall facts and basic concepts
2. Understand - Explain ideas or concepts
3. Apply - Use information in new situations
4. Analyze - Draw connections among ideas
5. Evaluate - Justify a stand or decision
6. Create - Produce new or original work
"""

from enum import Enum
from typing import Optional
import random


class BloomLevel(str, Enum):
    """Bloom's Taxonomy cognitive levels."""
    REMEMBER = "Remember"
    UNDERSTAND = "Understand"
    APPLY = "Apply"
    ANALYZE = "Analyze"
    EVALUATE = "Evaluate"
    CREATE = "Create"


# Bloom's Taxonomy keywords (from QUIZ.md)
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

# Level descriptions for display
BLOOM_DESCRIPTIONS = {
    BloomLevel.REMEMBER: "Recall facts and basic concepts",
    BloomLevel.UNDERSTAND: "Explain ideas or concepts",
    BloomLevel.APPLY: "Use information in new situations",
    BloomLevel.ANALYZE: "Draw connections among ideas",
    BloomLevel.EVALUATE: "Justify a stand or decision",
    BloomLevel.CREATE: "Produce new or original work",
}

# Cognitive complexity order (lowest to highest)
BLOOM_ORDER = [
    BloomLevel.REMEMBER,
    BloomLevel.UNDERSTAND,
    BloomLevel.APPLY,
    BloomLevel.ANALYZE,
    BloomLevel.EVALUATE,
    BloomLevel.CREATE,
]


def get_keywords_for_level(level: BloomLevel) -> list[str]:
    """
    Get action verbs for a Bloom's Taxonomy level.

    Args:
        level: Bloom's Taxonomy level

    Returns:
        List of action verb keywords

    Example:
        >>> get_keywords_for_level(BloomLevel.ANALYZE)
        ['analyze', 'examine', 'compare', ...]
    """
    return BLOOM_KEYWORDS.get(level, [])


def get_all_keywords() -> dict[str, list[str]]:
    """
    Get all Bloom's Taxonomy keywords.

    Returns:
        Dictionary mapping level names to keyword lists
    """
    return {level.value: keywords for level, keywords in BLOOM_KEYWORDS.items()}


def identify_bloom_level(text: str) -> Optional[BloomLevel]:
    """
    Identify Bloom's Taxonomy level from question text.

    Scans the text for action verbs and returns the matching level.

    Args:
        text: Question text to analyze

    Returns:
        Identified BloomLevel or None if no match found

    Example:
        >>> identify_bloom_level("Analyze the time complexity")
        BloomLevel.ANALYZE
    """
    text_lower = text.lower()

    # Check each level's keywords
    for level in BLOOM_ORDER:
        keywords = BLOOM_KEYWORDS.get(level, [])
        for keyword in keywords:
            # Check for keyword at word boundary
            if keyword in text_lower:
                # Verify it's a whole word (not part of another word)
                import re
                if re.search(rf'\b{keyword}\b', text_lower):
                    return level

    return None


def get_action_verb(level: BloomLevel, variety: bool = True) -> str:
    """
    Get an action verb for a specific Bloom's level.

    Args:
        level: Bloom's Taxonomy level
        variety: If True, return random verb; if False, return first verb

    Returns:
        An action verb appropriate for the level

    Example:
        >>> get_action_verb(BloomLevel.APPLY)
        'solve'  # or another Apply-level verb
    """
    keywords = BLOOM_KEYWORDS.get(level, ["apply"])
    if variety:
        return random.choice(keywords)
    return keywords[0]


def validate_question_bloom_alignment(
    question_text: str,
    expected_level: BloomLevel
) -> tuple[bool, Optional[BloomLevel]]:
    """
    Validate that a question aligns with expected Bloom's level.

    Args:
        question_text: The question text
        expected_level: The expected Bloom's level

    Returns:
        Tuple of (is_aligned, detected_level)

    Example:
        >>> validate_question_bloom_alignment(
        ...     "Analyze the structure",
        ...     BloomLevel.ANALYZE
        ... )
        (True, BloomLevel.ANALYZE)
    """
    detected = identify_bloom_level(question_text)

    if detected is None:
        return False, None

    return detected == expected_level, detected


def get_level_description(level: BloomLevel) -> str:
    """
    Get description for a Bloom's level.

    Args:
        level: Bloom's Taxonomy level

    Returns:
        Description string
    """
    return BLOOM_DESCRIPTIONS.get(level, "")


def get_higher_levels(level: BloomLevel) -> list[BloomLevel]:
    """
    Get all levels higher than the given level.

    Args:
        level: Reference Bloom's level

    Returns:
        List of higher levels

    Example:
        >>> get_higher_levels(BloomLevel.APPLY)
        [BloomLevel.ANALYZE, BloomLevel.EVALUATE, BloomLevel.CREATE]
    """
    try:
        idx = BLOOM_ORDER.index(level)
        return BLOOM_ORDER[idx + 1:]
    except ValueError:
        return []


def get_lower_levels(level: BloomLevel) -> list[BloomLevel]:
    """
    Get all levels lower than the given level.

    Args:
        level: Reference Bloom's level

    Returns:
        List of lower levels
    """
    try:
        idx = BLOOM_ORDER.index(level)
        return BLOOM_ORDER[:idx]
    except ValueError:
        return []


def parse_bloom_levels(levels: list[str]) -> list[BloomLevel]:
    """
    Parse string level names to BloomLevel enum values.

    Args:
        levels: List of level name strings

    Returns:
        List of BloomLevel enum values

    Example:
        >>> parse_bloom_levels(["Apply", "Analyze"])
        [BloomLevel.APPLY, BloomLevel.ANALYZE]
    """
    result = []
    for level_str in levels:
        try:
            level = BloomLevel(level_str.capitalize())
            result.append(level)
        except ValueError:
            # Try to find by lowercase comparison
            for bl in BloomLevel:
                if bl.value.lower() == level_str.lower():
                    result.append(bl)
                    break
    return result
