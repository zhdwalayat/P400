"""
Validators for the Educational Material Automation System.

Provides validation utilities for:
- Name sanitization (subject/topic names to URL-safe slugs)
- CLO validation (Course Learning Outcomes format)
- Content validation (academic tone checking)
"""

from shared.validators.name_validator import sanitize_name, validate_slug

__all__ = [
    "sanitize_name",
    "validate_slug",
]
