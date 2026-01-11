"""
Shared utilities for the Educational Material Automation System.

This package contains:
- formatters: PDF, DOCX, PPTX generation utilities
- validators: Name sanitization, CLO validation, content validation
- utils: File management, version control, metadata handling
"""

from shared.validators.name_validator import sanitize_name, validate_slug
from shared.utils.file_manager import get_material_path, ensure_directory, check_topic_exists
from shared.utils.version_manager import parse_version, increment_version
from shared.utils.metadata_manager import load_metadata, save_metadata

__all__ = [
    "sanitize_name",
    "validate_slug",
    "get_material_path",
    "ensure_directory",
    "check_topic_exists",
    "parse_version",
    "increment_version",
    "load_metadata",
    "save_metadata",
]
