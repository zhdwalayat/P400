"""
Utility functions for the Educational Material Automation System.

Provides utilities for:
- File management (directory creation, path resolution)
- Version management (version parsing, incrementing)
- Metadata management (metadata.json read/write)
"""

from shared.utils.file_manager import (
    get_material_path,
    get_file_name,
    ensure_directory,
    check_topic_exists,
    get_base_path,
)
from shared.utils.version_manager import (
    parse_version,
    increment_version,
    format_version,
    compare_versions,
)
from shared.utils.metadata_manager import (
    load_metadata,
    save_metadata,
    create_initial_metadata,
    update_metadata_version,
)

__all__ = [
    # File manager
    "get_material_path",
    "get_file_name",
    "ensure_directory",
    "check_topic_exists",
    "get_base_path",
    # Version manager
    "parse_version",
    "increment_version",
    "format_version",
    "compare_versions",
    # Metadata manager
    "load_metadata",
    "save_metadata",
    "create_initial_metadata",
    "update_metadata_version",
]
