# QUIZ Skill Documentation

## Overview

The QUIZ skill generates comprehensive, CLO-aligned assessment quizzes for any subject and topic. Receives subject from PROJECT ORGANIZATION orchestrator and handles all aspects of quiz generation including question creation, rubric definition, complexity level management, and Word document formatting.

## Purpose

Generate academically-rigorous quizzes with rubrics aligned to Course Learning Outcomes (CLOs) using Bloom's Taxonomy framework, delivered in Word document format.

## Input Requirements

| Input | Source | Type | Required | Options/Format |
|-------|--------|------|----------|----------------|
| **Subject** | Orchestrator | String | Yes | Auto-received from PROJECT ORGANIZATION |
| **Topic** | User | String | Yes | Any specific topic (e.g., "Binary Search Trees") |
| **Reference Material** | User | Mixed | Yes | Book / URL / Note/Document / NOTES skill output / General |
| **CLOs** | User | Text List | **MANDATORY** | Numbered list or line-separated learning outcomes |
| **Time Duration** | User | Integer | Yes | Minutes (e.g., 60, 90) |
| **Total Questions** | User | Integer | Yes | Typically 3-20 questions |
| **Complexity Level** | User | Enum | Yes | Single level OR Mixed levels (Bloom's Taxonomy) |
| **Question Types** | User | Multi-select | Yes | Short Answer / Long Answer / Problem-Solving / MCQs (explicit only) |

**CRITICAL**: Collect each requirement ONE BY ONE, not all at once.

### Reference Material Options

| Type | Example | Notes |
|------|---------|-------|
| Book | "Introduction to Algorithms" | Page numbers optional |
| URL | "https://example.com/tutorial" | Web links |
| NOTES skill | "Use NOTES for 'Binary Search Trees'" | Check `subjects/{subject}/notes/{topic}/` |
| Note/Document | Provide path or upload | User-provided materials |
| General | No specific reference | Proceed without reference |

**Storage structure**: See CLAUDE.md §Storage & Organization

### CLO Requirements

**Format Example:**
```
1. Analyze the structure and properties of binary search trees
2. Evaluate the efficiency of BST operations in different scenarios
3. Design and implement balanced tree solutions
4. Apply BST concepts to solve algorithmic problems
```

- **Validation**: At least one CLO required
- **Critical**: ALL quiz questions MUST align with CLOs
- **Confirmation**: Ask "Proceed with implementing these CLOs? (Yes/No)"

### Question Types

**Default**: Short Answer, Long Answer, Problem-Solving
**MCQs**: Only if explicitly requested (NOT default)

## Quiz Generation Process

### Step 1: Topic Directory Check

```
Check: subjects/{subject}/quizzes/{topic}/
- IF EXISTS: Load existing, increment version
- IF NOT EXISTS: Create directory, set v1.0
```

### Step 2: Reference Material Processing

**If NOTES skill requested:**
1. Check `subjects/{subject}/notes/{topic}/` exists
2. Read notes file (`.pdf` or `.md`)
3. Extract concepts, definitions, examples
4. Note in metadata: quiz based on NOTES skill
5. If not found: Error, request alternative reference

**Storage paths**: See CLAUDE.md §Directory Structure

### Step 3: Question Generation with CLO & Bloom's Alignment

#### Quiz Document Structure

**Header:**
```
Subject: [Subject Title]
Topic: [Topic Name]
Duration: [Time] minutes | Questions: [Number]
Date: [Date] | Version: v1.0 (2026-01-08)
Reference: [Material]

Course Learning Outcomes (CLOs):
1. [CLO 1]
2. [CLO 2]
...

Instructions:
- Read all questions carefully
- Answer all questions
- Time limit: [Time] minutes
- Refer to rubric for grading criteria
```

**Question Format:**
```
Question [N]: [Question Text]

CLO Alignment: CLO #[X]
Bloom's Taxonomy Level: [Level]
Marks: [Total]

[Question content with clear instructions]

---
RUBRIC FOR QUESTION [N]:

Criteria:
1. [Criterion]: [Description] - [X] marks
2. [Criterion]: [Description] - [X] marks
...

Excellent (90-100%): [Description]
Good (75-89%): [Description]
Satisfactory (60-74%): [Description]
Needs Improvement (<60%): [Description]
---
```

### Step 4: Bloom's Taxonomy Levels & Keywords

**Use these specialized action verbs in questions:**

| Level | Keywords | Use When |
|-------|----------|----------|
| **Remember** | Define, List, Label, Name, Identify, Recall, State | Recall facts/basic concepts |
| **Understand** | Explain, Describe, Summarize, Interpret, Compare, Contrast | Explain ideas/concepts |
| **Apply** | Apply, Demonstrate, Solve, Use, Execute, Implement, Calculate | Use information in new situations |
| **Analyze** | Analyze, Examine, Compare, Categorize, Differentiate, Investigate | Draw connections among ideas |
| **Evaluate** | Evaluate, Assess, Justify, Critique, Judge, Defend, Recommend | Justify decisions/actions |
| **Create** | Design, Create, Develop, Formulate, Construct, Propose, Generate | Produce new/original work |

**Example CLO Implementation:**
- Remember: "**Define** binary search tree and **list** its key properties (CLO #1)"
- Understand: "**Compare** balanced vs unbalanced BSTs to demonstrate CLO #2"
- Apply: "**Solve** the following problem using BST insertion algorithm (CLO #3)"
- Analyze: "**Examine** time complexity of BST operations in different scenarios (CLO #1)"
- Evaluate: "**Assess** whether BST or hash table is more appropriate. **Justify** your answer (CLO #2)"
- Create: "**Design** a balanced BST implementation maintaining O(log n) complexity (CLO #3)"

**Academic tone requirements**: See CLAUDE.md §Content Generation

### Step 5: Question Distribution Strategy

**Single Complexity Level:**
- All questions at same Bloom's level
- Distributed across all CLOs
- Each CLO addressed at least once

**Mixed Complexity Levels:**
- Questions distributed evenly across selected levels
- Each Bloom's level represented
- CLOs addressed across different complexity levels

**Distribution Formula:**
```
Questions per level = Total Questions / Number of Selected Levels
Remainder → Assign to higher complexity levels
```

**Example**: 10 questions, 3 levels (Understand, Apply, Analyze), 3 CLOs
- Understand: 3 questions (CLOs 1, 2, 3)
- Apply: 4 questions (CLOs 1, 2, 3, mixed)
- Analyze: 3 questions (CLOs 1, 2, 3)

### Step 6: Rubric Definition

Each question MUST have:

- **Specific Criteria**: 3-5 measurable criteria with marks
- **Mark Distribution**: Clear point allocation
- **Performance Levels**: Excellent / Good / Satisfactory / Needs Improvement
- **CLO Alignment**: Explicitly state which CLO(s)
- **Bloom's Level**: Clearly indicate cognitive level

## Output File Structure

**Storage paths**: See CLAUDE.md §Directory Structure

```
subjects/{subject}/quizzes/{topic}/
├── {topic}-quiz.docx
└── metadata.json
```

### Metadata File

```json
{
  "topic": "Binary Search Trees",
  "subject": "Data Structures and Algorithms",
  "current_version": "v1.0",
  "created_date": "2026-01-08",
  "last_updated": "2026-01-08",
  "time_duration": 60,
  "total_questions": 5,
  "complexity_levels": ["Understand", "Apply", "Analyze"],
  "question_types": ["Short Answer", "Problem-Solving"],
  "clos": [
    "Analyze BST structure and properties",
    "Evaluate efficiency of BST operations"
  ],
  "reference": {
    "type": "notes_skill",
    "topic": "Binary Search Trees"
  }
}
```

**Naming conventions**: See CLAUDE.md §File Management

## Skill Workflow

```
1. Receive subject from ORGANIZER
   ↓
2. Ask user for topic
   ↓
3. Ask user for reference material
   - If NOTES skill: Check subjects/{subject}/notes/{topic}/
   ↓
4. Ask user for CLOs (MANDATORY)
   - Confirm: "Proceed with these CLOs? (Yes/No)"
   ↓
5. Ask user for time duration
   ↓
6. Ask user for total questions
   ↓
7. Ask user for complexity level(s)
   - Single or Mixed Bloom's levels
   ↓
8. Ask user for question types
   - Default: Short/Long/Problem-Solving
   - MCQs only if explicitly requested
   ↓
9. Check if subjects/{subject}/quizzes/{topic}/ exists
   ↓
10. Generate quiz with CLO alignment & Bloom's keywords
   ↓
11. Save Word document + metadata.json
   ↓
12. Confirm to user with file location and details
```

## Quality Checklist

- [ ] All questions aligned to CLOs (every question maps to ≥1 CLO)
- [ ] Bloom's Taxonomy keywords used correctly
- [ ] Academic tone throughout
- [ ] Each question has detailed rubric
- [ ] Mark distribution clear for each criterion
- [ ] Performance levels defined
- [ ] Question types match user selection
- [ ] MCQs only if explicitly requested
- [ ] Time duration displayed
- [ ] Reference material integrated
- [ ] Word document formatted correctly
- [ ] Metadata created/updated
- [ ] No file duplication (update existing)

**Academic standards**: See CLAUDE.md §Content Generation

## Error Handling

| Scenario | Error | Action |
|----------|-------|--------|
| No CLOs provided | "CLOs are MANDATORY. Please provide at least one CLO." | Re-prompt |
| Invalid topic | "Topic name cannot be empty." | Re-prompt |
| NOTES skill not found | "Notes for '{topic}' not found. Provide alternative?" | Offer options |
| No complexity level | "Select at least one Bloom's Taxonomy level." | Re-prompt |
| No question types | "Select at least one question type." | Re-prompt |
| Invalid time/questions | "Must be positive integer." | Re-prompt |
| File write error | "Unable to save to {path}. Check permissions." | Report error |

## Skill Independence

**CRITICAL**: Operates independently after receiving subject from orchestrator.

- Does NOT call back to PROJECT ORGANIZATION
- Does NOT invoke other skills (NOTES, PRESENTATION)
- Does NOT expose prompts/logic to other skills
- Handles ALL quiz generation autonomously
- Returns completion status to user only
