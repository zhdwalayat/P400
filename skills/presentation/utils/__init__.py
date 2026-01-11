"""
Presentation skill utilities.

Provides:
- Theme selection based on subject type
- Slide content generation helpers
"""

from skills.presentation.utils.theme_selector import (
    THEMES,
    select_theme_for_subject,
    get_theme_colors,
    ThemeType,
)
from skills.presentation.utils.slide_generator import (
    SlideGenerator,
    generate_slide_template,
    estimate_slide_count,
)

__all__ = [
    # Theme selector
    "THEMES",
    "select_theme_for_subject",
    "get_theme_colors",
    "ThemeType",
    # Slide generator
    "SlideGenerator",
    "generate_slide_template",
    "estimate_slide_count",
]
