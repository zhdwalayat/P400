"""
Markdown formatter for lecture notes.

Generates structured Markdown files with:
- Header section (subject, topic, level, version, date)
- Introduction
- Content sections with headings
- Tables and code blocks
- Summary and references
"""

from pathlib import Path
from typing import Any, Optional
from datetime import datetime

from shared.formatters.base_formatter import BaseFormatter
from shared.utils.metadata_manager import create_notes_metadata


class MarkdownFormatter(BaseFormatter):
    """Formatter for generating Markdown lecture notes."""

    @property
    def material_type(self) -> str:
        return "notes"

    @property
    def output_format(self) -> str:
        return "md"

    def generate(self, content: dict[str, Any]) -> Path:
        """
        Generate Markdown lecture notes.

        Args:
            content: Dictionary containing:
                - educational_level: str (Undergraduate/Graduate/Advanced)
                - version: str (e.g., "v1.0")
                - references: list[dict] (optional)
                - introduction: str
                - sections: list[dict] with 'title' and 'content'
                - summary: str (optional)
                - update_highlights: str (optional, for updates)

        Returns:
            Path to the generated Markdown file
        """
        self.ensure_output_directory()

        lines = []

        # Header
        lines.extend(self._generate_header(content))

        # Update highlights (if updating)
        if content.get("update_highlights"):
            lines.extend(self._generate_update_highlights(content))

        # Introduction
        lines.extend(self._generate_introduction(content))

        # Main content sections
        for section in content.get("sections", []):
            lines.extend(self._generate_section(section))

        # Summary
        if content.get("summary"):
            lines.extend(self._generate_summary(content))

        # References
        if content.get("references"):
            lines.extend(self._generate_references(content))

        # Write file
        output_path = self.get_output_path()
        output_path.write_text("\n".join(lines), encoding="utf-8")

        # Save metadata
        metadata = create_notes_metadata(
            topic=self.topic,
            subject=self.subject,
            educational_level=content.get("educational_level", "Undergraduate"),
            output_format="md",
            references=content.get("references", [])
        )
        metadata["current_version"] = content.get("version", "v1.0")
        self.save_metadata(metadata)

        return output_path

    def _generate_header(self, content: dict[str, Any]) -> list[str]:
        """Generate the header section."""
        version = content.get("version", "v1.0")
        level = content.get("educational_level", "Undergraduate")

        lines = [
            f"# {self.topic}",
            "",
            "---",
            "",
            f"**Subject**: {self.subject}",
            f"**Topic**: {self.topic}",
            f"**Educational Level**: {level}",
            f"**Date**: {self._format_date()}",
            f"**Version**: {self._format_version_header(version)}",
            "",
        ]

        # Reference if provided
        refs = content.get("references", [])
        if refs:
            ref_strs = [self._format_reference(r) for r in refs]
            lines.append(f"**Reference**: {'; '.join(ref_strs)}")
            lines.append("")

        lines.extend(["---", ""])
        return lines

    def _generate_update_highlights(self, content: dict[str, Any]) -> list[str]:
        """Generate update highlights section for version updates."""
        version = content.get("version", "v1.1")
        highlights = content.get("update_highlights", "")

        return [
            "---",
            f"## UPDATE HIGHLIGHTS - {self._format_version_header(version)}",
            "",
            highlights,
            "",
            "---",
            "",
        ]

    def _generate_introduction(self, content: dict[str, Any]) -> list[str]:
        """Generate introduction section."""
        intro = content.get("introduction", "")
        if not intro:
            return []

        return [
            "## Introduction",
            "",
            intro,
            "",
        ]

    def _generate_section(self, section: dict[str, Any]) -> list[str]:
        """Generate a content section."""
        title = section.get("title", "Section")
        section_content = section.get("content", "")
        level = section.get("level", 2)

        heading = "#" * level
        lines = [
            f"{heading} {title}",
            "",
            section_content,
            "",
        ]

        # Add subsections if present
        for subsection in section.get("subsections", []):
            subsection["level"] = level + 1
            lines.extend(self._generate_section(subsection))

        # Add tables if present
        for table in section.get("tables", []):
            lines.extend(self._generate_table(table))

        # Add code blocks if present
        for code in section.get("code_blocks", []):
            lines.extend(self._generate_code_block(code))

        return lines

    def _generate_table(self, table: dict[str, Any]) -> list[str]:
        """Generate a Markdown table."""
        headers = table.get("headers", [])
        rows = table.get("rows", [])
        caption = table.get("caption", "")

        if not headers or not rows:
            return []

        lines = []
        if caption:
            lines.append(f"*{caption}*")
            lines.append("")

        # Header row
        lines.append("| " + " | ".join(headers) + " |")
        # Separator
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        # Data rows
        for row in rows:
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

        lines.append("")
        return lines

    def _generate_code_block(self, code: dict[str, Any]) -> list[str]:
        """Generate a code block."""
        language = code.get("language", "")
        code_content = code.get("code", "")
        caption = code.get("caption", "")

        lines = []
        if caption:
            lines.append(f"*{caption}*")

        lines.extend([
            f"```{language}",
            code_content,
            "```",
            "",
        ])
        return lines

    def _generate_summary(self, content: dict[str, Any]) -> list[str]:
        """Generate summary section."""
        summary = content.get("summary", "")
        return [
            "## Summary",
            "",
            summary,
            "",
        ]

    def _generate_references(self, content: dict[str, Any]) -> list[str]:
        """Generate references section."""
        refs = content.get("references", [])
        if not refs:
            return []

        lines = [
            "## References",
            "",
        ]

        for i, ref in enumerate(refs, 1):
            lines.append(f"{i}. {self._format_reference(ref)}")

        lines.append("")
        return lines

    def _format_reference(self, ref: dict[str, Any]) -> str:
        """Format a single reference."""
        ref_type = ref.get("type", "general")
        ref_content = ref.get("content", "General knowledge")

        if ref_type == "book":
            return f"*{ref_content}*"
        elif ref_type == "url":
            return f"[{ref_content}]({ref_content})"
        elif ref_type == "web_search":
            return f"Web search: {ref_content}"
        else:
            return ref_content
