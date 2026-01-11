"""
PDF formatter for lecture notes.

Generates structured PDF files using reportlab with:
- Professional formatting
- Header section
- Structured content
- Tables and figures
"""

from pathlib import Path
from typing import Any, Optional
from datetime import datetime

from shared.formatters.base_formatter import BaseFormatter
from shared.utils.metadata_manager import create_notes_metadata

# Conditional import for reportlab
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, ListFlowable, ListItem
    )
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class PDFFormatter(BaseFormatter):
    """Formatter for generating PDF lecture notes."""

    @property
    def material_type(self) -> str:
        return "notes"

    @property
    def output_format(self) -> str:
        return "pdf"

    def __init__(self, subject: str, topic: str):
        super().__init__(subject, topic)
        if REPORTLAB_AVAILABLE:
            self.styles = getSampleStyleSheet()
            self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        if not REPORTLAB_AVAILABLE:
            return

        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
        ))

        # Heading styles
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceBefore=20,
            spaceAfter=12,
        ))

        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
        ))

        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
        ))

        # Metadata style
        self.styles.add(ParagraphStyle(
            name='Metadata',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
        ))

    def generate(self, content: dict[str, Any]) -> Path:
        """
        Generate PDF lecture notes.

        Args:
            content: Dictionary containing:
                - educational_level: str
                - version: str
                - references: list[dict]
                - introduction: str
                - sections: list[dict]
                - summary: str (optional)

        Returns:
            Path to the generated PDF file
        """
        if not REPORTLAB_AVAILABLE:
            raise ImportError(
                "reportlab is required for PDF generation. "
                "Install with: pip install reportlab"
            )

        self.ensure_output_directory()
        output_path = self.get_output_path()

        # Create document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Build content
        story = []

        # Title
        story.append(Paragraph(self.topic, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))

        # Metadata header
        story.extend(self._build_header(content))
        story.append(Spacer(1, 30))

        # Update highlights (if present)
        if content.get("update_highlights"):
            story.extend(self._build_update_highlights(content))

        # Introduction
        if content.get("introduction"):
            story.extend(self._build_introduction(content))

        # Main sections
        for section in content.get("sections", []):
            story.extend(self._build_section(section))

        # Summary
        if content.get("summary"):
            story.extend(self._build_summary(content))

        # References
        if content.get("references"):
            story.extend(self._build_references(content))

        # Build PDF
        doc.build(story)

        # Save metadata
        metadata = create_notes_metadata(
            topic=self.topic,
            subject=self.subject,
            educational_level=content.get("educational_level", "Undergraduate"),
            output_format="pdf",
            references=content.get("references", [])
        )
        metadata["current_version"] = content.get("version", "v1.0")
        self.save_metadata(metadata)

        return output_path

    def _build_header(self, content: dict[str, Any]) -> list:
        """Build header metadata section."""
        version = content.get("version", "v1.0")
        level = content.get("educational_level", "Undergraduate")

        header_data = [
            ["Subject:", self.subject],
            ["Topic:", self.topic],
            ["Educational Level:", level],
            ["Date:", self._format_date()],
            ["Version:", self._format_version_header(version)],
        ]

        refs = content.get("references", [])
        if refs:
            ref_str = "; ".join([self._format_reference(r) for r in refs])
            header_data.append(["Reference:", ref_str])

        table = Table(header_data, colWidths=[1.5*inch, 4.5*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))

        return [table]

    def _build_update_highlights(self, content: dict[str, Any]) -> list:
        """Build update highlights section."""
        version = content.get("version", "v1.1")
        highlights = content.get("update_highlights", "")

        elements = [
            Paragraph(
                f"UPDATE HIGHLIGHTS - {self._format_version_header(version)}",
                self.styles['CustomHeading1']
            ),
            Paragraph(highlights, self.styles['CustomBody']),
            Spacer(1, 20),
        ]
        return elements

    def _build_introduction(self, content: dict[str, Any]) -> list:
        """Build introduction section."""
        intro = content.get("introduction", "")
        return [
            Paragraph("Introduction", self.styles['CustomHeading1']),
            Paragraph(intro, self.styles['CustomBody']),
            Spacer(1, 15),
        ]

    def _build_section(self, section: dict[str, Any], level: int = 1) -> list:
        """Build a content section."""
        elements = []
        title = section.get("title", "Section")
        section_content = section.get("content", "")

        # Heading
        style = 'CustomHeading1' if level == 1 else 'CustomHeading2'
        elements.append(Paragraph(title, self.styles[style]))

        # Content paragraphs
        for para in section_content.split("\n\n"):
            if para.strip():
                elements.append(Paragraph(para.strip(), self.styles['CustomBody']))

        # Tables
        for table_data in section.get("tables", []):
            elements.extend(self._build_table(table_data))

        # Subsections
        for subsection in section.get("subsections", []):
            elements.extend(self._build_section(subsection, level + 1))

        elements.append(Spacer(1, 10))
        return elements

    def _build_table(self, table_data: dict[str, Any]) -> list:
        """Build a table."""
        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])
        caption = table_data.get("caption", "")

        if not headers or not rows:
            return []

        elements = []

        # Caption
        if caption:
            elements.append(Paragraph(f"<i>{caption}</i>", self.styles['Normal']))
            elements.append(Spacer(1, 5))

        # Table
        data = [headers] + rows
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 15))

        return elements

    def _build_summary(self, content: dict[str, Any]) -> list:
        """Build summary section."""
        summary = content.get("summary", "")
        return [
            Paragraph("Summary", self.styles['CustomHeading1']),
            Paragraph(summary, self.styles['CustomBody']),
            Spacer(1, 15),
        ]

    def _build_references(self, content: dict[str, Any]) -> list:
        """Build references section."""
        refs = content.get("references", [])
        if not refs:
            return []

        elements = [
            Paragraph("References", self.styles['CustomHeading1']),
        ]

        for i, ref in enumerate(refs, 1):
            ref_text = f"{i}. {self._format_reference(ref)}"
            elements.append(Paragraph(ref_text, self.styles['CustomBody']))

        return elements

    def _format_reference(self, ref: dict[str, Any]) -> str:
        """Format a single reference."""
        ref_type = ref.get("type", "general")
        ref_content = ref.get("content", "General knowledge")

        if ref_type == "book":
            return f"<i>{ref_content}</i>"
        elif ref_type == "url":
            return f"<link href='{ref_content}'>{ref_content}</link>"
        elif ref_type == "web_search":
            return f"Web search: {ref_content}"
        else:
            return ref_content
