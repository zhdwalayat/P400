# Project Overview

Role-based, subject-agnostic workflow automation system for university lecturers to automate creation of educational materials. Uses modular skill-based architecture with intelligent routing to generate notes, quizzes, and presentations for any subject or course.

## Technology Stack

| Component | Technology |
|-----------|------------|
| **Platform** | Claude Skill Framework |
| **LLM** | Anthropic Claude API |
| **Skills** | 4 specialized (PROJECT ORGANIZATION, NOTES, QUIZ, PRESENTATION) |
| **Storage** | Local file system, subject-based organization |
| **Output Formats** | Notes: PDF/Markdown; Quizzes: Word (.docx); Presentations: PPT (.pptx) |

## Directory Structure

```
Project1/
├── skills/
│   ├── project-organization/     # Main orchestrator skill
│   ├── notes/                    # Note generation skill
│   ├── quiz/                     # Quiz generation skill
│   └── presentation/             # Presentation generation skill
├── subjects/                     # All generated content (by subject)
│   └── {subject-name}/           # Subject folder
│       ├── notes/{topic}/        # Notes for this subject
│       ├── presentations/{topic}/Slides/  # Presentations
│       └── quizzes/{topic}/      # Quizzes
├── shared/                       # Shared utilities
│   ├── formatters/               # Output format converters
│   └── validators/               # Input validation
└── CLAUDE.md                     # This file
```

## Storage & Organization

### Storage Hierarchy
1. **Subject Level**: `subjects/{subject-name}/` (sanitized)
2. **Material Type**: `notes/`, `presentations/`, `quizzes/` within each subject
3. **Topic Level**: `{topic-name}/` within each material type
4. **Files**: Generated content + `metadata.json` in each topic folder

### Storage Paths (Authoritative Reference)

| Material | Path |
|----------|------|
| **Notes** | `subjects/{subject}/notes/{topic}/{topic}.pdf or .md` |
| **Quizzes** | `subjects/{subject}/quizzes/{topic}/{topic}-quiz.docx` |
| **Presentations** | `subjects/{subject}/presentations/{topic}/Slides/{topic}.pptx` |

## File Management

### Naming Conventions (Authoritative Reference)

**Sanitization Rules:**
1. Convert to lowercase
2. Replace spaces with hyphens
3. Remove special characters (keep only alphanumeric and hyphens)
4. Trim leading/trailing hyphens

**Examples:**
- "Data Structures and Algorithms" → `data-structures-and-algorithms`
- "The French Revolution (1789-1799)" → `the-french-revolution-1789-1799`
- "Alkene Reactions & Mechanisms" → `alkene-reactions-mechanisms`

### Version Management
- **Update, Not Duplicate**: Always check if `subjects/{subject}/{material-type}/{topic}/` exists before creating
- **When Updating**: Increment version number (v1.0 → v1.1), add update highlights
- **When Creating**: Set version to v1.0

## Coding Conventions

| Principle | Implementation |
|-----------|----------------|
| **Skill Isolation** | Each skill independent with own directory/resources |
| **Subject-Based Storage** | All outputs organized by subject first |
| **Update Strategy** | Check existence, update instead of duplicate |
| **Orchestrator Pattern** | PROJECT ORGANIZATION routes only, never generates content |
| **Subject-Agnostic Design** | No hardcoded subject-specific logic |
| **Consistent Interfaces** | All skills follow same input/output contract |

## Content Generation

### Academic Tone (MANDATORY - Authoritative Reference)

**ALL generated content MUST adhere to:**
- Formal academic language
- Scholarly terminology appropriate to subject
- Objective, evidence-based presentation
- No colloquialisms or casual expressions
- Proper academic structure with clear hierarchy
- Third-person perspective (avoid "you", "we" unless pedagogically appropriate)
- Precise and technical language

**Examples:**
- ✓ CORRECT: "Binary search trees exhibit logarithmic time complexity for search operations in balanced configurations."
- ✗ INCORRECT: "BSTs are pretty fast when you search for stuff if they're balanced."

### CLO Alignment

| Material | CLO Requirement |
|----------|-----------------|
| **QUIZ** | MANDATORY - All questions MUST align with user-supplied CLOs. Every question maps to ≥1 CLO. Use Bloom's Taxonomy keywords. |
| **NOTES** | NO CLO - Content based on educational level (Undergraduate/Graduate/Advanced) |
| **PRESENTATION** | NO CLO - Content based on reference material and topic |

### Subject Neutrality
- Skills must work for ANY subject (Math, History, Art, Science, etc.)
- Topic specificity: Use user-supplied topic as primary context
- Format compliance: Notes (PDF/Markdown), Quizzes (Word with rubrics), Presentations (PowerPoint with modern themes)

## Key Commands

```bash
# Activate PROJECT ORGANIZATION skill (main entry point)
claude run project-organization

# Direct skill invocation (testing/debugging)
claude run notes
claude run quiz
claude run presentation

# List/validate skills
claude skills list
claude skills validate
```

## Skill Architecture

| Rule | Description |
|------|-------------|
| **PROJECT ORGANIZATION is orchestrator** | ONLY asks "What do you want?" and routes to NOTES/QUIZ/PRESENTATION |
| **Specialized skills are autonomous** | Once handed task, each skill handles everything independently |
| **No cross-skill dependencies** | Skills cannot reference or call each other directly |
| **Skill descriptions are private** | Keep implementation details within each skill's directory |

**User interaction flow**: See README.md §Basic Usage

## Common Pitfalls

### DO NOT
- ❌ Duplicate routing logic (only PROJECT ORGANIZATION routes)
- ❌ Hardcode subjects (never assume specific subject)
- ❌ Overwrite files (always check if topic exists and update intelligently)
- ❌ Expose skill internals (keep within skill boundaries)
- ❌ Skip format validation (ensure files match specification)
- ❌ Use informal tone (academic tone is non-negotiable)
- ❌ Mix storage locations (always use `subjects/{subject}/{material-type}/{topic}/`)
- ❌ For QUIZ: NEVER generate without CLOs (invalid without CLO alignment)

## Testing Strategy

**Test Coverage:**
- Diverse subjects (Math, Literature, Chemistry, History, Art)
- Subject/topic name edge cases (special chars, long names, Unicode)
- Update scenarios (same topic twice, verify no duplication)
- All format outputs (PDF, Markdown, Word, PowerPoint)
- Orchestrator routing correctness
- Storage structure verification
- Academic tone compliance
- Cross-subject organization
- For QUIZ: CLO alignment and Bloom's Taxonomy keyword usage

## Development Workflow

1. Start with PROJECT ORGANIZATION skill (orchestrator first)
2. Build one specialized skill fully (NOTES end-to-end)
3. Replicate pattern (use NOTES as template for QUIZ and PRESENTATION)
4. Test each skill independently (standalone before integration)
5. Test full workflow (PROJECT ORGANIZATION → specialized skill → output verification)
6. Iterate on prompts (refine based on output quality)
