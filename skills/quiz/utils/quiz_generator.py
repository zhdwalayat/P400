"""
Quiz generation utilities.

Provides:
- Question distribution across Bloom's levels and CLOs
- Question and rubric template generation
- Quiz structure helpers
"""

from typing import Any, Optional
import random

from skills.quiz.utils.bloom_taxonomy import (
    BloomLevel,
    get_action_verb,
    BLOOM_ORDER,
    parse_bloom_levels,
)


def distribute_questions(
    total_questions: int,
    complexity_levels: list[str],
    clos: list[str],
    mixed: bool = True
) -> list[dict[str, Any]]:
    """
    Distribute questions across Bloom's levels and CLOs.

    Args:
        total_questions: Total number of questions to generate
        complexity_levels: List of Bloom's level names
        clos: List of Course Learning Outcomes
        mixed: If True, distribute evenly; if False, use single level

    Returns:
        List of question specifications with level and CLO assignments

    Example:
        >>> distribute_questions(6, ["Apply", "Analyze"], ["CLO1", "CLO2"])
        [
            {"level": "Apply", "clo_index": 0, "clo_number": 1},
            {"level": "Apply", "clo_index": 1, "clo_number": 2},
            ...
        ]
    """
    if not complexity_levels:
        complexity_levels = ["Apply"]

    levels = parse_bloom_levels(complexity_levels)
    num_levels = len(levels)
    num_clos = len(clos)

    if num_levels == 0:
        levels = [BloomLevel.APPLY]
        num_levels = 1

    if num_clos == 0:
        raise ValueError("At least one CLO is required")

    questions = []

    if mixed and num_levels > 1:
        # Distribute evenly across levels
        base_per_level = total_questions // num_levels
        remainder = total_questions % num_levels

        question_idx = 0
        for level_idx, level in enumerate(levels):
            # Give extra questions to higher levels
            count = base_per_level
            if level_idx >= num_levels - remainder:
                count += 1

            for _ in range(count):
                clo_idx = question_idx % num_clos
                questions.append({
                    "level": level.value,
                    "clo_index": clo_idx,
                    "clo_number": clo_idx + 1,
                    "question_number": question_idx + 1,
                })
                question_idx += 1
    else:
        # Single level for all questions
        level = levels[0]
        for question_idx in range(total_questions):
            clo_idx = question_idx % num_clos
            questions.append({
                "level": level.value,
                "clo_index": clo_idx,
                "clo_number": clo_idx + 1,
                "question_number": question_idx + 1,
            })

    return questions


def generate_question_template(
    question_number: int,
    bloom_level: str,
    clo_number: int,
    clo_text: str,
    topic: str,
    marks: int = 10
) -> dict[str, Any]:
    """
    Generate a question template structure.

    Args:
        question_number: Question sequence number
        bloom_level: Bloom's Taxonomy level
        clo_number: CLO number being assessed
        clo_text: Full CLO text
        topic: Quiz topic
        marks: Total marks for the question

    Returns:
        Question template dictionary

    Example:
        >>> generate_question_template(1, "Analyze", 2, "Evaluate BST efficiency", "BSTs", 15)
        {
            "number": 1,
            "text": "[Question about BSTs using ANALYZE action verb]",
            "bloom_level": "Analyze",
            "clo_number": 2,
            ...
        }
    """
    try:
        level_enum = BloomLevel(bloom_level.capitalize())
    except ValueError:
        level_enum = BloomLevel.APPLY

    action_verb = get_action_verb(level_enum)

    return {
        "number": question_number,
        "text": f"[{action_verb.capitalize()} - Question about {topic} aligned to CLO {clo_number}]",
        "bloom_level": bloom_level,
        "clo_number": clo_number,
        "clo_text": clo_text,
        "marks": marks,
        "action_verb": action_verb,
        "rubric": generate_rubric_template(marks),
    }


def generate_rubric_template(total_marks: int, num_criteria: int = 3) -> dict[str, Any]:
    """
    Generate a rubric template for a question.

    Args:
        total_marks: Total marks for the question
        num_criteria: Number of grading criteria

    Returns:
        Rubric dictionary with criteria and performance levels

    Example:
        >>> generate_rubric_template(10, 3)
        {
            "criteria": [
                {"description": "Criterion 1", "marks": 4},
                {"description": "Criterion 2", "marks": 3},
                {"description": "Criterion 3", "marks": 3},
            ],
            "performance_levels": {...}
        }
    """
    # Distribute marks across criteria
    base_marks = total_marks // num_criteria
    remainder = total_marks % num_criteria

    criteria = []
    for i in range(num_criteria):
        marks = base_marks
        if i < remainder:
            marks += 1
        criteria.append({
            "description": f"[Criterion {i + 1} description]",
            "marks": marks,
        })

    return {
        "criteria": criteria,
        "performance_levels": {
            "Excellent": "[90-100% description - Comprehensive understanding, accurate application]",
            "Good": "[75-89% description - Solid understanding with minor gaps]",
            "Satisfactory": "[60-74% description - Basic understanding, some errors]",
            "Needs Improvement": "[<60% description - Significant gaps in understanding]",
        }
    }


class QuizGenerator:
    """
    Quiz generation helper class.

    Coordinates question distribution, template generation,
    and quiz structure creation.
    """

    def __init__(
        self,
        topic: str,
        subject: str,
        clos: list[str],
        total_questions: int,
        time_duration: int,
        complexity_levels: list[str],
        question_types: Optional[list[str]] = None
    ):
        """
        Initialize quiz generator.

        Args:
            topic: Quiz topic
            subject: Subject name
            clos: List of Course Learning Outcomes
            total_questions: Total number of questions
            time_duration: Duration in minutes
            complexity_levels: Bloom's levels to use
            question_types: Types of questions to include
        """
        self.topic = topic
        self.subject = subject
        self.clos = clos
        self.total_questions = total_questions
        self.time_duration = time_duration
        self.complexity_levels = complexity_levels
        self.question_types = question_types or ["Short Answer", "Problem-Solving"]

    def generate_structure(self) -> dict[str, Any]:
        """
        Generate complete quiz structure.

        Returns:
            Dictionary with quiz metadata and question templates
        """
        # Calculate marks per question
        total_marks = self.total_questions * 10  # Default 10 marks each
        marks_per_question = total_marks // self.total_questions

        # Distribute questions
        distribution = distribute_questions(
            self.total_questions,
            self.complexity_levels,
            self.clos,
            mixed=len(self.complexity_levels) > 1
        )

        # Generate question templates
        questions = []
        for dist in distribution:
            clo_idx = dist["clo_index"]
            clo_text = self.clos[clo_idx] if clo_idx < len(self.clos) else ""

            question = generate_question_template(
                question_number=dist["question_number"],
                bloom_level=dist["level"],
                clo_number=dist["clo_number"],
                clo_text=clo_text,
                topic=self.topic,
                marks=marks_per_question,
            )
            questions.append(question)

        return {
            "version": "v1.0",
            "topic": self.topic,
            "subject": self.subject,
            "time_duration": self.time_duration,
            "total_questions": self.total_questions,
            "total_marks": total_marks,
            "complexity_levels": self.complexity_levels,
            "question_types": self.question_types,
            "clos": self.clos,
            "questions": questions,
        }

    def validate_clo_coverage(self, questions: list[dict]) -> dict[str, Any]:
        """
        Validate that all CLOs are covered by questions.

        Args:
            questions: List of question dictionaries

        Returns:
            Validation result with coverage details
        """
        clo_coverage = {i + 1: 0 for i in range(len(self.clos))}

        for q in questions:
            clo_num = q.get("clo_number", 0)
            if clo_num in clo_coverage:
                clo_coverage[clo_num] += 1

        uncovered = [clo for clo, count in clo_coverage.items() if count == 0]

        return {
            "is_valid": len(uncovered) == 0,
            "coverage": clo_coverage,
            "uncovered_clos": uncovered,
            "message": (
                "All CLOs covered" if len(uncovered) == 0
                else f"Uncovered CLOs: {uncovered}"
            )
        }
