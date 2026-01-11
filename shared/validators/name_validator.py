"""
Name validation and sanitization utilities.

Sanitization rules from CLAUDE.md:
1. Convert to lowercase
2. Replace spaces with hyphens
3. Remove special characters (keep only alphanumeric and hyphens)
4. Trim leading/trailing hyphens

Examples:
- "Data Structures and Algorithms" -> "data-structures-and-algorithms"
- "The French Revolution (1789-1799)" -> "the-french-revolution-1789-1799"
- "Alkene Reactions & Mechanisms" -> "alkene-reactions-mechanisms"
"""

import re
from typing import Tuple


def sanitize_name(name: str) -> str:
    """
    Convert a name to a URL-safe slug.

    Args:
        name: The original name (e.g., "Data Structures and Algorithms")

    Returns:
        Sanitized slug (e.g., "data-structures-and-algorithms")

    Examples:
        >>> sanitize_name("Data Structures and Algorithms")
        'data-structures-and-algorithms'
        >>> sanitize_name("The French Revolution (1789-1799)")
        'the-french-revolution-1789-1799'
        >>> sanitize_name("Alkene Reactions & Mechanisms")
        'alkene-reactions-mechanisms'
    """
    if not name:
        raise ValueError("Name cannot be empty")

    # Convert to lowercase
    slug = name.lower()

    # Replace spaces with hyphens
    slug = slug.replace(' ', '-')

    # Remove special characters (keep only alphanumeric and hyphens)
    slug = re.sub(r'[^a-z0-9-]', '', slug)

    # Remove consecutive hyphens
    slug = re.sub(r'-+', '-', slug)

    # Trim leading/trailing hyphens
    slug = slug.strip('-')

    if not slug:
        raise ValueError("Name results in empty slug after sanitization")

    return slug


def validate_slug(slug: str) -> bool:
    """
    Validate that a string is a valid slug.

    A valid slug:
    - Contains only lowercase letters, numbers, and hyphens
    - Does not start or end with a hyphen
    - Does not contain consecutive hyphens

    Args:
        slug: The slug to validate

    Returns:
        True if valid, False otherwise

    Examples:
        >>> validate_slug("data-structures-and-algorithms")
        True
        >>> validate_slug("Data Structures")
        False
        >>> validate_slug("-invalid-")
        False
    """
    if not slug:
        return False

    # Pattern: starts with alphanumeric, optionally followed by
    # groups of (single hyphen + alphanumeric characters)
    pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
    return bool(re.match(pattern, slug))


def extract_name_parts(name: str) -> Tuple[str, str]:
    """
    Extract base name and any parenthetical suffix.

    Useful for handling names like "The French Revolution (1789-1799)"

    Args:
        name: The full name

    Returns:
        Tuple of (base_name, suffix) where suffix may be empty

    Examples:
        >>> extract_name_parts("The French Revolution (1789-1799)")
        ('The French Revolution', '1789-1799')
        >>> extract_name_parts("Binary Search Trees")
        ('Binary Search Trees', '')
    """
    match = re.match(r'^(.+?)\s*\(([^)]+)\)\s*$', name)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return name.strip(), ''
