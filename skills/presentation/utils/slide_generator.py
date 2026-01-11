"""
Slide generation utilities for presentations.

Provides:
- Slide content structure generation
- Slide count estimation
- Content organization helpers
"""

from typing import Any, Optional
import math


def estimate_slide_count(
    content_length: int,
    include_intro: bool = True,
    include_conclusion: bool = True,
    include_references: bool = True
) -> int:
    """
    Estimate number of slides based on content length.

    Args:
        content_length: Approximate word count of content
        include_intro: Include title and outline slides
        include_conclusion: Include conclusion slide
        include_references: Include references slide

    Returns:
        Estimated slide count

    Example:
        >>> estimate_slide_count(1000, True, True, True)
        15
    """
    # Estimate content slides (roughly 100 words per slide)
    content_slides = max(3, math.ceil(content_length / 100))

    # Add structural slides
    extra_slides = 0
    if include_intro:
        extra_slides += 2  # Title + Outline
    if include_conclusion:
        extra_slides += 1
    if include_references:
        extra_slides += 1

    return content_slides + extra_slides


def generate_slide_template(
    title: str,
    content_type: str = "bullets",
    max_bullets: int = 7
) -> dict[str, Any]:
    """
    Generate a slide template.

    Args:
        title: Slide title
        content_type: Type of content (bullets, diagram, table)
        max_bullets: Maximum bullet points

    Returns:
        Slide template dictionary
    """
    template = {
        "title": title,
        "bullets": [],
        "notes": "",
        "content_type": content_type,
    }

    if content_type == "bullets":
        template["bullets"] = [f"[Bullet point {i + 1}]" for i in range(min(5, max_bullets))]
    elif content_type == "diagram":
        template["diagram"] = {
            "type": "placeholder",
            "description": f"[Diagram for {title}]"
        }
    elif content_type == "table":
        template["table"] = {
            "headers": ["Column 1", "Column 2", "Column 3"],
            "rows": [["Data", "Data", "Data"]],
        }

    return template


class SlideGenerator:
    """
    Slide generation helper class.

    Coordinates slide structure generation for presentations.
    """

    def __init__(
        self,
        topic: str,
        subject: str,
        theme: str = "default",
        num_slides: Optional[int] = None,
        references: Optional[list[dict]] = None
    ):
        """
        Initialize slide generator.

        Args:
            topic: Presentation topic
            subject: Subject name
            theme: Theme name
            num_slides: Target number of slides (auto if None)
            references: Reference materials
        """
        self.topic = topic
        self.subject = subject
        self.theme = theme
        self.num_slides = num_slides
        self.references = references or []

    def generate_structure(self) -> dict[str, Any]:
        """
        Generate complete presentation structure.

        Returns:
            Dictionary with presentation metadata and slides
        """
        # Auto-determine slide count if not specified
        target_slides = self.num_slides or estimate_slide_count(500)

        # Calculate content slides (subtract intro, conclusion, references)
        content_slides_count = max(3, target_slides - 4)

        return {
            "version": "v1.0",
            "topic": self.topic,
            "subject": self.subject,
            "theme": self.theme,
            "outline": self._generate_outline(content_slides_count),
            "slides": self._generate_content_slides(content_slides_count),
            "conclusion": self._generate_conclusion(),
            "references": self.references,
            "features": ["Academic tone", "Modern theme", "Visual hierarchy"],
        }

    def _generate_outline(self, num_sections: int) -> list[str]:
        """Generate outline points."""
        base_outline = [
            f"Introduction to {self.topic}",
            f"Key Concepts",
            f"Detailed Analysis",
            f"Applications",
            f"Summary",
        ]
        return base_outline[:num_sections]

    def _generate_content_slides(self, count: int) -> list[dict[str, Any]]:
        """Generate content slides."""
        slides = []

        # Introduction section
        slides.append(generate_slide_template(
            f"What is {self.topic}?",
            content_type="bullets"
        ))
        slides[-1]["bullets"] = [
            f"[Definition of {self.topic}]",
            "[Key characteristics]",
            "[Relevance and importance]",
            "[Historical context]",
        ]

        # Core concepts
        slides.append(generate_slide_template(
            "Core Concepts",
            content_type="bullets"
        ))
        slides[-1]["bullets"] = [
            "[Concept 1: Description]",
            "[Concept 2: Description]",
            "[Concept 3: Description]",
            "[Concept 4: Description]",
        ]

        # Detailed content slides
        remaining = count - 2
        section_titles = [
            f"{self.topic}: Deep Dive",
            "Key Properties",
            "Analysis Framework",
            "Practical Applications",
            "Case Studies",
            "Best Practices",
            "Common Challenges",
            "Future Trends",
        ]

        for i in range(remaining):
            title = section_titles[i % len(section_titles)]
            slides.append(generate_slide_template(title))

        return slides

    def _generate_conclusion(self) -> dict[str, Any]:
        """Generate conclusion content."""
        return {
            "key_points": [
                f"[Key takeaway 1 about {self.topic}]",
                "[Key takeaway 2]",
                "[Key takeaway 3]",
                "[Key takeaway 4]",
            ]
        }

    def get_recommended_slide_count(self) -> tuple[int, int]:
        """
        Get recommended slide count range.

        Returns:
            Tuple of (minimum, maximum) recommended slides
        """
        # Based on topic complexity and presentation standards
        return (8, 20)

    def validate_structure(self, slides: list[dict]) -> dict[str, Any]:
        """
        Validate presentation structure.

        Args:
            slides: List of slide dictionaries

        Returns:
            Validation result
        """
        issues = []

        # Check slide count
        if len(slides) < 5:
            issues.append("Too few slides for comprehensive coverage")
        elif len(slides) > 30:
            issues.append("Too many slides may lose audience attention")

        # Check bullet counts
        for i, slide in enumerate(slides, 1):
            bullets = slide.get("bullets", [])
            if len(bullets) > 7:
                issues.append(f"Slide {i}: Too many bullets ({len(bullets)} > 7)")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "slide_count": len(slides),
        }
