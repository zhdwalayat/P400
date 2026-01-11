"""
Version management utilities for the Educational Material Automation System.

Handles:
- Version parsing (e.g., "v1.0" -> (1, 0))
- Version incrementing (v1.0 -> v1.1)
- Version comparison

Version Rules (from CLAUDE.md):
- Update, Not Duplicate: Always check if topic exists before creating
- When Updating: Increment version number (v1.0 -> v1.1), add update highlights
- When Creating: Set version to v1.0
"""

import re
from typing import Tuple, Optional
from datetime import datetime


def parse_version(version: str) -> Tuple[int, int]:
    """
    Parse a version string to (major, minor) tuple.

    Args:
        version: Version string (e.g., "v1.0", "v2.3")

    Returns:
        Tuple of (major, minor) version numbers

    Examples:
        >>> parse_version("v1.0")
        (1, 0)
        >>> parse_version("v2.3")
        (2, 3)
        >>> parse_version("invalid")
        (1, 0)
    """
    match = re.match(r'v?(\d+)\.(\d+)', version)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 1, 0  # Default to v1.0


def format_version(major: int, minor: int) -> str:
    """
    Format version tuple to string.

    Args:
        major: Major version number
        minor: Minor version number

    Returns:
        Formatted version string (e.g., "v1.0")

    Examples:
        >>> format_version(1, 0)
        'v1.0'
        >>> format_version(2, 3)
        'v2.3'
    """
    return f"v{major}.{minor}"


def increment_version(current: str, increment_type: str = "minor") -> str:
    """
    Increment a version string.

    Args:
        current: Current version string (e.g., "v1.0")
        increment_type: "minor" (default) or "major"

    Returns:
        Incremented version string

    Examples:
        >>> increment_version("v1.0")
        'v1.1'
        >>> increment_version("v1.9")
        'v1.10'
        >>> increment_version("v1.5", "major")
        'v2.0'
    """
    major, minor = parse_version(current)

    if increment_type == "major":
        return format_version(major + 1, 0)
    else:  # minor
        return format_version(major, minor + 1)


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two version strings.

    Args:
        version1: First version string
        version2: Second version string

    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2

    Examples:
        >>> compare_versions("v1.0", "v1.1")
        -1
        >>> compare_versions("v2.0", "v1.9")
        1
        >>> compare_versions("v1.5", "v1.5")
        0
    """
    major1, minor1 = parse_version(version1)
    major2, minor2 = parse_version(version2)

    if major1 != major2:
        return 1 if major1 > major2 else -1
    if minor1 != minor2:
        return 1 if minor1 > minor2 else -1
    return 0


def get_version_with_date(version: str, date: Optional[datetime] = None) -> str:
    """
    Format version with date for display.

    Args:
        version: Version string
        date: Date to include (defaults to today)

    Returns:
        Formatted string like "v1.0 (2026-01-11)"

    Examples:
        >>> get_version_with_date("v1.0")
        'v1.0 (2026-01-11)'
    """
    if date is None:
        date = datetime.now()
    return f"{version} ({date.strftime('%Y-%m-%d')})"


def is_valid_version(version: str) -> bool:
    """
    Check if a string is a valid version format.

    Args:
        version: String to check

    Returns:
        True if valid version format

    Examples:
        >>> is_valid_version("v1.0")
        True
        >>> is_valid_version("1.0")
        True
        >>> is_valid_version("invalid")
        False
    """
    pattern = r'^v?\d+\.\d+$'
    return bool(re.match(pattern, version))


def get_initial_version() -> str:
    """
    Get the initial version for new content.

    Returns:
        Initial version string "v1.0"
    """
    return "v1.0"
