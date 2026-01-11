"""
Theme selection utilities for presentations.

Provides:
- Theme definitions with color schemes
- Subject-based theme selection
- Theme customization
"""

from typing import Optional
from enum import Enum


class ThemeType(str, Enum):
    """Available presentation themes."""
    STEM = "stem"
    SCIENCES = "sciences"
    HUMANITIES = "humanities"
    BUSINESS = "business"
    DEFAULT = "default"
    PROFESSIONAL = "professional"
    VIBRANT = "vibrant"
    DARK = "dark"


# Theme definitions (from PRESENTATION.md)
THEMES = {
    ThemeType.STEM: {
        "name": "Modern Tech Blue",
        "description": "Clean, modern design for STEM subjects",
        "primary": "#2E5C8A",
        "secondary": "#4A90E2",
        "accent": "#FF6B35",
        "text": "#333333",
        "background": "#FFFFFF",
        "aesthetic": "Modern tech",
    },
    ThemeType.SCIENCES: {
        "name": "Scientific Green",
        "description": "Professional theme for natural sciences",
        "primary": "#2D5A27",
        "secondary": "#4A8C41",
        "accent": "#FFD700",
        "text": "#333333",
        "background": "#FFFFFF",
        "aesthetic": "Professional scientific",
    },
    ThemeType.HUMANITIES: {
        "name": "Classic Warm",
        "description": "Elegant theme for humanities and arts",
        "primary": "#8B4513",
        "secondary": "#CD853F",
        "accent": "#DAA520",
        "text": "#333333",
        "background": "#FFF8F0",
        "aesthetic": "Elegant, classic academic",
    },
    ThemeType.BUSINESS: {
        "name": "Corporate Blue",
        "description": "Professional theme for business subjects",
        "primary": "#1C3D5A",
        "secondary": "#4682B4",
        "accent": "#FF8C00",
        "text": "#333333",
        "background": "#FFFFFF",
        "aesthetic": "Corporate design",
    },
    ThemeType.DEFAULT: {
        "name": "Modern Minimalist",
        "description": "Clean, universal design",
        "primary": "#2E5C8A",
        "secondary": "#6B7B8C",
        "accent": "#E74C3C",
        "text": "#333333",
        "background": "#FFFFFF",
        "aesthetic": "Modern minimalist",
    },
    ThemeType.PROFESSIONAL: {
        "name": "Professional Gray",
        "description": "Neutral professional appearance",
        "primary": "#34495E",
        "secondary": "#7F8C8D",
        "accent": "#3498DB",
        "text": "#2C3E50",
        "background": "#FFFFFF",
        "aesthetic": "Professional neutral",
    },
    ThemeType.VIBRANT: {
        "name": "Vibrant Energy",
        "description": "Bold, energetic colors",
        "primary": "#E74C3C",
        "secondary": "#9B59B6",
        "accent": "#F39C12",
        "text": "#2C3E50",
        "background": "#FFFFFF",
        "aesthetic": "Bold and energetic",
    },
    ThemeType.DARK: {
        "name": "Dark Mode",
        "description": "Dark background with light text",
        "primary": "#3498DB",
        "secondary": "#2ECC71",
        "accent": "#F1C40F",
        "text": "#ECF0F1",
        "background": "#2C3E50",
        "aesthetic": "Dark modern",
    },
}

# Subject type to theme mapping
SUBJECT_THEME_MAP = {
    # STEM
    "computer science": ThemeType.STEM,
    "programming": ThemeType.STEM,
    "data structures": ThemeType.STEM,
    "algorithms": ThemeType.STEM,
    "mathematics": ThemeType.STEM,
    "engineering": ThemeType.STEM,
    "technology": ThemeType.STEM,
    "software": ThemeType.STEM,

    # Sciences
    "biology": ThemeType.SCIENCES,
    "chemistry": ThemeType.SCIENCES,
    "physics": ThemeType.SCIENCES,
    "environmental": ThemeType.SCIENCES,
    "ecology": ThemeType.SCIENCES,
    "medicine": ThemeType.SCIENCES,
    "health": ThemeType.SCIENCES,

    # Humanities
    "history": ThemeType.HUMANITIES,
    "literature": ThemeType.HUMANITIES,
    "philosophy": ThemeType.HUMANITIES,
    "art": ThemeType.HUMANITIES,
    "music": ThemeType.HUMANITIES,
    "languages": ThemeType.HUMANITIES,
    "culture": ThemeType.HUMANITIES,

    # Business
    "business": ThemeType.BUSINESS,
    "economics": ThemeType.BUSINESS,
    "finance": ThemeType.BUSINESS,
    "management": ThemeType.BUSINESS,
    "marketing": ThemeType.BUSINESS,
    "accounting": ThemeType.BUSINESS,
}


def select_theme_for_subject(subject: str) -> ThemeType:
    """
    Select appropriate theme based on subject name.

    Args:
        subject: Subject name

    Returns:
        Appropriate ThemeType

    Example:
        >>> select_theme_for_subject("Data Structures and Algorithms")
        ThemeType.STEM
    """
    subject_lower = subject.lower()

    for keyword, theme in SUBJECT_THEME_MAP.items():
        if keyword in subject_lower:
            return theme

    return ThemeType.DEFAULT


def get_theme_colors(theme: ThemeType) -> dict[str, str]:
    """
    Get color scheme for a theme.

    Args:
        theme: Theme type

    Returns:
        Dictionary of color values

    Example:
        >>> get_theme_colors(ThemeType.STEM)
        {"primary": "#2E5C8A", "secondary": "#4A90E2", ...}
    """
    theme_data = THEMES.get(theme, THEMES[ThemeType.DEFAULT])
    return {
        "primary": theme_data["primary"],
        "secondary": theme_data["secondary"],
        "accent": theme_data["accent"],
        "text": theme_data["text"],
        "background": theme_data["background"],
    }


def get_theme_info(theme: ThemeType) -> dict[str, str]:
    """
    Get full theme information.

    Args:
        theme: Theme type

    Returns:
        Complete theme dictionary
    """
    return THEMES.get(theme, THEMES[ThemeType.DEFAULT])


def list_available_themes() -> list[dict[str, str]]:
    """
    List all available themes with descriptions.

    Returns:
        List of theme info dictionaries
    """
    return [
        {
            "type": theme_type.value,
            "name": theme_data["name"],
            "description": theme_data["description"],
            "aesthetic": theme_data["aesthetic"],
        }
        for theme_type, theme_data in THEMES.items()
    ]


def parse_theme(theme_str: Optional[str]) -> ThemeType:
    """
    Parse theme string to ThemeType.

    Args:
        theme_str: Theme name string or None

    Returns:
        ThemeType enum value
    """
    if not theme_str:
        return ThemeType.DEFAULT

    theme_str_lower = theme_str.lower()

    # Try direct match
    try:
        return ThemeType(theme_str_lower)
    except ValueError:
        pass

    # Try matching theme names
    for theme_type, theme_data in THEMES.items():
        if theme_data["name"].lower() == theme_str_lower:
            return theme_type

    return ThemeType.DEFAULT
