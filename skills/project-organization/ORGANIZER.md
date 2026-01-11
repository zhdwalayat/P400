# ORGANIZER Skill Documentation

## Overview

The ORGANIZER skill is the main orchestrator responsible for routing user requests to specialized content generation skills (NOTES, QUIZ, PRESENTATION). This skill serves as the entry point for the entire educational material automation system.

## Purpose

1. Collect user requirements and preferences
2. Route tasks to appropriate specialized skills
3. Monitor task completion and quality
4. Ensure all requested materials are generated correctly

## Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **User Interaction** | Present clear options, collect subject information |
| **Task Routing** | Route to NOTES, QUIZ, or PRESENTATION skills |
| **Quality Monitoring** | Verify specialized skills complete their tasks |
| **Workflow Coordination** | Handle single/multiple task requests, maintain consistency |

## User Interaction Flow

### Step 1: Initial Prompt

```
Welcome! What would you like to create today?

Please select from the following options:

1. NOTES - Generate lecture notes
2. QUIZ - Generate assessment quiz
3. PRESENTATION - Generate slide presentation
4. NOTES + QUIZ - Generate notes and quiz
5. NOTES + PRESENTATION - Generate notes and presentation
6. QUIZ + PRESENTATION - Generate quiz and presentation
7. ALL THREE - Generate notes, quiz, and presentation

Enter your choice (1-7):
```

**For detailed option descriptions**: See README.md §7 Options

### Step 2: Subject Collection

```
Please provide the subject for your educational materials:

Example: "Data Structures and Algorithms"
Example: "Organic Chemistry"
Example: "European History"

Subject:
```

**Validation:**
- Subject name must not be empty
- **Naming rules**: See CLAUDE.md §File Management

### Step 3: Task Routing

| Option | Routes To | Execution Order | Verification Path |
|--------|-----------|-----------------|-------------------|
| 1 | NOTES | - | `subjects/{subject}/notes/{topic}/` |
| 2 | QUIZ | - | `subjects/{subject}/quizzes/{topic}/` |
| 3 | PRESENTATION | - | `subjects/{subject}/presentations/{topic}/Slides/` |
| 4 | NOTES, QUIZ | Sequential | Both paths above |
| 5 | NOTES, PRESENTATION | Sequential | Both paths above |
| 6 | QUIZ, PRESENTATION | Sequential | Both paths above |
| 7 | NOTES, QUIZ, PRESENTATION | Sequential | All three paths above |

**Sequential Execution Rationale:**
- NOTES first → QUIZ/PRESENTATION can reference notes
- Allows subsequent materials to leverage earlier content

**Storage structure**: See CLAUDE.md §Storage & Organization

## Routing Strategy

### Passing Subject Information

```
When routing to any specialized skill:
1. Pass subject name as parameter
2. Skill receives subject automatically
3. Skill uses subject for storage: subjects/{subject}/{material-type}/
4. Skill does NOT ask user for subject
```

## Monitoring and Verification

### Task Completion Checks

For each routed task, verify:

- [ ] Skill execution completed without errors
- [ ] File exists at expected path (see table above)
- [ ] Metadata created (`metadata.json` in topic folder)
- [ ] Topic name captured from skill output

**Storage paths**: See CLAUDE.md §Storage & Organization

## Output Reporting

### Completion Report Template

```
✓ All requested materials generated successfully!

Subject: [Subject Name]

Generated Materials:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If NOTES was requested:]
📝 NOTES:
   Topic: [Topic Name]
   File: subjects/{subject}/notes/{topic}/{topic}.pdf
   Version: v1.0 (2026-01-08)
   Educational Level: [Level]

[If QUIZ was requested:]
📋 QUIZ:
   Topic: [Topic Name]
   File: subjects/{subject}/quizzes/{topic}/{topic}-quiz.docx
   Version: v1.0 (2026-01-08)
   Questions: [Count] | Duration: [Time] min | CLOs: [Count]

[If PRESENTATION was requested:]
📊 PRESENTATION:
   Topic: [Topic Name]
   File: subjects/{subject}/presentations/{topic}/Slides/{topic}.pptx
   Version: v1.0 (2026-01-08)
   Slides: [Count] | Theme: [Theme Name]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All materials are stored in: subjects/{subject}/

Would you like to create more materials? (Yes/No)
```

## Error Handling

| Scenario | Error Message | Action |
|----------|---------------|--------|
| Invalid option selected | "Invalid choice. Please select 1-7." | Re-prompt for valid option |
| Empty subject name | "Subject name cannot be empty." | Re-prompt for subject |
| Skill execution failure | "Failed to generate [type]. Error: [details]" | Report error, ask to retry |
| Partial completion | Report successes and failures separately | Offer retry for failed tasks only |
| File verification failed | "Generated file not found at expected location." | Report to user, suggest checking logs |

## Workflow Example

### Example: Multiple Materials (NOTES + QUIZ)

```
ORGANIZER: "What would you like to create today?" [Shows options 1-7]
USER: "4" (NOTES + QUIZ)

ORGANIZER: "Please provide the subject:"
USER: "Organic Chemistry"

ORGANIZER: → Step 1/2: Routing to NOTES skill with subject="Organic Chemistry"
[NOTES skill executes autonomously]
NOTES: Generates notes for "Alkene Reactions"

ORGANIZER: ✓ Verified NOTES generated successfully
ORGANIZER: → Step 2/2: Routing to QUIZ skill with subject="Organic Chemistry"
[QUIZ skill executes autonomously]
QUIZ: Generates quiz (may reference notes from NOTES skill)

ORGANIZER: ✓ Verified QUIZ generated successfully
ORGANIZER: ✓ Displays completion report for both materials
```

## Implementation Rules

| Rule | Description |
|------|-------------|
| **Never Generate Content** | ORGANIZER only routes and monitors, never creates content |
| **Subject Consistency** | Collect subject once, pass same subject to all skills |
| **Skill Autonomy** | Each skill handles its own user interactions |
| **Sequential Execution** | Generate NOTES before QUIZ/PRESENTATION (if both requested) |
| **Complete Monitoring** | Track every invoked skill, verify file generation |
| **Accurate Reporting** | If any task fails, clearly indicate what succeeded/failed |

**Academic tone requirements**: See CLAUDE.md §Content Generation

## State Management

### Task Status Tracker

```json
{
  "subject": "Data Structures and Algorithms",
  "requested_tasks": ["NOTES", "QUIZ", "PRESENTATION"],
  "completed_tasks": [],
  "failed_tasks": [],
  "task_outputs": {
    "NOTES": {
      "status": "completed",
      "topic": "Binary Search Trees",
      "file_path": "subjects/data-structures-and-algorithms/notes/binary-search-trees/binary-search-trees.pdf",
      "version": "v1.0"
    },
    "QUIZ": {"status": "in_progress"},
    "PRESENTATION": {"status": "pending"}
  }
}
```

## Skill Independence

**CRITICAL**: This skill operates as orchestrator only.

- Does NOT generate content (notes, quizzes, presentations)
- Does NOT call back to specialized skills after routing
- Does NOT expose skill prompts or logic
- Only monitors completion and reports to user
