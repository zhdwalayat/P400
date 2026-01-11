"""
Content validation utilities for academic tone.

Validates content follows academic writing standards:
- Formal language
- No colloquialisms
- Third-person perspective
- Scholarly terminology
"""

import re
from typing import Any


# Informal words/phrases to avoid (from CLAUDE.md academic tone requirements)
INFORMAL_PATTERNS = [
    # Contractions
    r"\b(won't|can't|don't|doesn't|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|couldn't|wouldn't|shouldn't)\b",
    r"\b(it's|that's|there's|here's|what's|who's|how's|let's)\b",
    r"\b(I'm|you're|we're|they're|he's|she's)\b",
    r"\b(I've|you've|we've|they've)\b",
    r"\b(I'll|you'll|we'll|they'll|he'll|she'll)\b",

    # Casual expressions
    r"\b(gonna|wanna|gotta|kinda|sorta|dunno|lemme)\b",
    r"\b(yeah|yup|nope|ok|okay|cool|awesome|great)\b",
    r"\b(stuff|things|a lot|lots of|tons of)\b",
    r"\b(pretty much|kind of|sort of|basically)\b",

    # Slang and colloquialisms
    r"\b(like|so|well|actually|literally|totally)\b",  # filler words
    r"\b(super|really|very|extremely)\b",  # intensifiers often overused
]

# First/second person pronouns (prefer third person)
PERSONAL_PRONOUNS = [
    r"\bI\b",
    r"\bme\b",
    r"\bmy\b",
    r"\bmine\b",
    r"\bwe\b",
    r"\bus\b",
    r"\bour\b",
    r"\bours\b",
    r"\byou\b",
    r"\byour\b",
    r"\byours\b",
]


def check_academic_tone(text: str) -> tuple[bool, list[dict[str, Any]]]:
    """
    Check if text follows academic tone guidelines.

    Args:
        text: Text to validate

    Returns:
        Tuple of (is_academic, list of issues found)

    Example:
        >>> check_academic_tone("BSTs are pretty fast when balanced")
        (False, [{"type": "informal", "text": "pretty", "suggestion": "..."}])
    """
    issues = []

    # Check for informal patterns
    for pattern in INFORMAL_PATTERNS:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            issues.append({
                "type": "informal",
                "text": match.group(),
                "position": match.start(),
                "suggestion": "Use formal academic language"
            })

    # Check for personal pronouns (warn, not error)
    for pattern in PERSONAL_PRONOUNS:
        matches = re.finditer(pattern, text)
        for match in matches:
            issues.append({
                "type": "personal_pronoun",
                "text": match.group(),
                "position": match.start(),
                "suggestion": "Consider using third-person perspective"
            })

    is_academic = len([i for i in issues if i["type"] == "informal"]) == 0
    return is_academic, issues


def get_formal_alternative(informal_text: str) -> str:
    """
    Suggest formal alternative for informal text.

    Args:
        informal_text: Informal word or phrase

    Returns:
        Suggested formal alternative
    """
    alternatives = {
        # Contractions
        "won't": "will not",
        "can't": "cannot",
        "don't": "do not",
        "doesn't": "does not",
        "isn't": "is not",
        "aren't": "are not",
        "it's": "it is",
        "that's": "that is",

        # Casual words
        "gonna": "going to",
        "wanna": "want to",
        "gotta": "have to",
        "kinda": "somewhat",
        "sorta": "somewhat",

        # Vague language
        "stuff": "material / content / elements",
        "things": "aspects / factors / elements",
        "a lot": "numerous / substantial / considerable",
        "lots of": "numerous / many",

        # Intensifiers
        "pretty": "relatively / fairly / somewhat",
        "really": "particularly / especially / significantly",
        "super": "highly / extremely / remarkably",

        # Filler words
        "basically": "fundamentally / essentially",
        "actually": "in fact / indeed",
        "literally": "[remove or use 'precisely']",
    }

    return alternatives.get(informal_text.lower(), "[use formal alternative]")


def validate_sentence_structure(text: str) -> list[dict[str, Any]]:
    """
    Validate sentence structure for academic writing.

    Args:
        text: Text to validate

    Returns:
        List of structure issues
    """
    issues = []

    sentences = re.split(r'[.!?]+', text)

    for i, sentence in enumerate(sentences):
        sentence = sentence.strip()
        if not sentence:
            continue

        # Check for very short sentences
        word_count = len(sentence.split())
        if word_count < 3:
            issues.append({
                "type": "short_sentence",
                "sentence": sentence,
                "suggestion": "Consider expanding for clarity"
            })

        # Check for very long sentences (potential run-ons)
        if word_count > 50:
            issues.append({
                "type": "long_sentence",
                "sentence": sentence[:50] + "...",
                "suggestion": "Consider breaking into shorter sentences"
            })

        # Check for starting with lowercase (after first sentence)
        if sentence and sentence[0].islower():
            issues.append({
                "type": "capitalization",
                "sentence": sentence[:20] + "...",
                "suggestion": "Sentences should start with capital letters"
            })

    return issues


def score_academic_quality(text: str) -> dict[str, Any]:
    """
    Score text for academic quality.

    Args:
        text: Text to score

    Returns:
        Dictionary with score and breakdown
    """
    is_academic, issues = check_academic_tone(text)
    structure_issues = validate_sentence_structure(text)

    # Count different issue types
    informal_count = len([i for i in issues if i["type"] == "informal"])
    pronoun_count = len([i for i in issues if i["type"] == "personal_pronoun"])
    structure_count = len(structure_issues)

    # Calculate score (0-100)
    # Start at 100, deduct points for issues
    score = 100
    score -= min(40, informal_count * 5)  # Max 40 point deduction
    score -= min(20, pronoun_count * 2)  # Max 20 point deduction
    score -= min(20, structure_count * 3)  # Max 20 point deduction

    # Determine grade
    if score >= 90:
        grade = "Excellent"
    elif score >= 75:
        grade = "Good"
    elif score >= 60:
        grade = "Acceptable"
    else:
        grade = "Needs Improvement"

    return {
        "score": max(0, score),
        "grade": grade,
        "is_academic": is_academic,
        "issues": {
            "informal_language": informal_count,
            "personal_pronouns": pronoun_count,
            "structure_issues": structure_count,
        },
        "details": issues + structure_issues,
    }
