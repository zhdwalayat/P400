"""
CLO (Course Learning Outcome) validation utilities.

Validates CLO format and content:
- At least one CLO required for quizzes
- CLO text must not be empty
- CLO should contain action verbs (Bloom's)
"""

from typing import Any
import re

from skills.quiz.utils.bloom_taxonomy import BLOOM_KEYWORDS, BloomLevel


def validate_clo_list(clos: list[str]) -> tuple[bool, list[str]]:
    """
    Validate a list of CLOs.

    Args:
        clos: List of CLO strings

    Returns:
        Tuple of (is_valid, list of error messages)

    Example:
        >>> validate_clo_list(["Analyze BST properties"])
        (True, [])
        >>> validate_clo_list([])
        (False, ["At least one CLO is required"])
    """
    errors = []

    if not clos:
        errors.append("At least one CLO is required")
        return False, errors

    for i, clo in enumerate(clos, 1):
        clo_errors = validate_single_clo(clo, i)
        errors.extend(clo_errors)

    return len(errors) == 0, errors


def validate_single_clo(clo: str, clo_number: int = 1) -> list[str]:
    """
    Validate a single CLO.

    Args:
        clo: CLO text
        clo_number: CLO number for error messages

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Check for empty CLO
    if not clo or not clo.strip():
        errors.append(f"CLO {clo_number}: Cannot be empty")
        return errors

    clo_stripped = clo.strip()

    # Check minimum length
    if len(clo_stripped) < 10:
        errors.append(f"CLO {clo_number}: Too short (minimum 10 characters)")

    # Check maximum length
    if len(clo_stripped) > 500:
        errors.append(f"CLO {clo_number}: Too long (maximum 500 characters)")

    return errors


def check_bloom_alignment(clo: str) -> tuple[bool, str]:
    """
    Check if CLO contains Bloom's Taxonomy action verbs.

    Args:
        clo: CLO text

    Returns:
        Tuple of (has_bloom_verb, detected_level or message)

    Example:
        >>> check_bloom_alignment("Analyze the structure of BSTs")
        (True, "Analyze")
        >>> check_bloom_alignment("Know about trees")
        (False, "No Bloom's Taxonomy action verb detected")
    """
    clo_lower = clo.lower()

    for level, keywords in BLOOM_KEYWORDS.items():
        for keyword in keywords:
            # Check for whole word match
            if re.search(rf'\b{keyword}\b', clo_lower):
                return True, level.value

    return False, "No Bloom's Taxonomy action verb detected"


def suggest_bloom_verbs(clo: str) -> list[str]:
    """
    Suggest Bloom's verbs to improve a CLO.

    Args:
        clo: CLO text

    Returns:
        List of suggested action verbs
    """
    # Common weak verbs and their suggested replacements
    weak_to_bloom = {
        "know": ["identify", "recall", "define", "list"],
        "learn": ["explain", "describe", "summarize", "interpret"],
        "understand": ["explain", "compare", "contrast", "classify"],
        "do": ["apply", "demonstrate", "solve", "implement"],
        "use": ["apply", "execute", "utilize", "implement"],
        "think": ["analyze", "evaluate", "assess", "examine"],
    }

    clo_lower = clo.lower()
    suggestions = []

    for weak, alternatives in weak_to_bloom.items():
        if weak in clo_lower:
            suggestions.extend(alternatives)

    # If no weak verbs found, suggest common high-level verbs
    if not suggestions:
        suggestions = ["analyze", "evaluate", "apply", "design", "compare"]

    return list(set(suggestions))[:5]  # Return up to 5 unique suggestions


def format_clo(clo: str, clo_number: int) -> str:
    """
    Format a CLO for display.

    Args:
        clo: CLO text
        clo_number: CLO number

    Returns:
        Formatted CLO string
    """
    return f"CLO {clo_number}: {clo.strip()}"


def parse_clos_from_text(text: str) -> list[str]:
    """
    Parse CLOs from user-provided text.

    Handles formats:
    - Numbered list (1. CLO text)
    - Bulleted list (- CLO text)
    - Line-separated text

    Args:
        text: Raw text containing CLOs

    Returns:
        List of CLO strings
    """
    clos = []

    # Split by newlines
    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Remove common prefixes
        # Numbered: "1.", "1)", "(1)"
        line = re.sub(r'^[\(\[]?\d+[\)\]\.:]?\s*', '', line)
        # Bulleted: "-", "*", "•"
        line = re.sub(r'^[-*•]\s*', '', line)
        # CLO prefix: "CLO 1:", "CLO1:"
        line = re.sub(r'^CLO\s*\d*[:\.]?\s*', '', line, flags=re.IGNORECASE)

        if line:
            clos.append(line)

    return clos
