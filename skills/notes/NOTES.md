# NOTES Skill Documentation

## Overview

The NOTES skill generates comprehensive, academically-formatted lecture notes for any subject and topic. Receives subject from PROJECT ORGANIZATION orchestrator and handles all aspects of note generation autonomously.

## Purpose

Generate detailed academic notes with complete descriptions, diagrams, tables, and graphs tailored to the specified educational level (Undergraduate/Graduate/Advanced).

## Input Requirements

| Input | Source | Type | Required | Options/Format |
|-------|--------|------|----------|----------------|
| **Subject** | Orchestrator | String | Yes | Auto-received from PROJECT ORGANIZATION |
| **Topic** | User | String | Yes | Any specific topic (e.g., "Binary Search Trees") |
| **Educational Level** | User | Enum | Yes | Undergraduate / Graduate / Advanced |
| **Reference Material** | User | Mixed | Yes | Book / URL / Web search / Material / General knowledge |
| **Output Format** | User | Enum | Yes | PDF (default) / Markdown |

### Reference Material Options

| Type | Example | Notes |
|------|---------|-------|
| Book | "Introduction to Algorithms" | Page numbers optional |
| URL | "https://example.com/tutorial" | Web links |
| Web Search | "Web search" | Auto-searches: {subject} + {topic} |
| Material | Upload or provide path | User-provided documents |
| General | No specific reference | Proceed without reference |

**Storage structure**: See CLAUDE.md §Storage & Organization

## Note Generation Process

### Step 1: Topic Directory Check

```
Check: subjects/{subject}/notes/{topic}/
- IF EXISTS: Load existing, increment version
- IF NOT EXISTS: Create directory, set v1.0
```

### Step 2: Content Structure

#### Required Components

1. **Header Section**
   - Subject, Topic, Educational Level, Date, Version, Reference

2. **Introduction**
   - Overview, relevance, context, learning objectives

3. **Detailed Content Sections**
   - Complete descriptions with academic language
   - Definitions, concepts, examples
   - Diagrams (flowcharts, trees, networks, blocks)
   - Tables (comparisons, properties, summaries)
   - Graphs (performance, statistics, functions)
   - Mathematical notation (LaTeX for equations)

4. **Level-Appropriate Organization**

| Level | Focus | Complexity |
|-------|-------|------------|
| Undergraduate | Foundational concepts, basic examples, clear explanations | Introductory |
| Graduate | Advanced theory, complex examples, research connections | Advanced |
| Advanced | Cutting-edge research, sophisticated analysis, specialized | Research-level |

5. **Summary/Conclusion**
   - Key takeaways, main points, further reading

6. **References**
   - All materials cited in academic format

**Academic tone requirements**: See CLAUDE.md §Content Generation

### Step 3: Diagram/Table/Graph Integration

| Visual Type | Use When | Format |
|-------------|----------|--------|
| Diagrams | Algorithms, data structures, processes, hierarchies | Flowcharts, trees, networks |
| Tables | Comparisons, properties, categorization | Rows/columns with headers |
| Graphs | Performance data, statistics, mathematical functions | Charts, plots |

**Format Considerations:**
- **Markdown**: Mermaid diagrams, ASCII tables, image references
- **PDF**: Formatted diagrams, tables, graphs with rendering

### Step 4: Version Management

#### NEW Topics (v1.0)
```
Create: subjects/{subject}/notes/{topic}/{topic}.pdf or .md
Version: v1.0 (2026-01-08)
Status: Initial creation
```

#### EXISTING Topics (v1.1+)
```
Update: subjects/{subject}/notes/{topic}/{topic}.pdf or .md
Version: v1.1+ (2026-01-08)
Action:
1. Read existing content
2. Add "UPDATE HIGHLIGHTS" section at top
3. Enhance/add sections
4. Preserve previous content
5. Increment version
```

**Update Highlights Format:**
```markdown
---
## UPDATE HIGHLIGHTS - v1.1 (2026-01-08)

### Changes in this version:
- Added section on [topic]
- Enhanced [section] with [additions]
- Updated examples for [level]

### Sections Modified:
- [Section]: [Changes made]
---
```

## Output File Structure

**Storage paths**: See CLAUDE.md §Directory Structure

```
subjects/{subject}/notes/{topic}/
├── {topic}.pdf or .md
└── metadata.json
```

### Metadata File

```json
{
  "topic": "Binary Search Trees",
  "subject": "Data Structures and Algorithms",
  "educational_level": "Graduate",
  "current_version": "v1.1",
  "created_date": "2026-01-08",
  "last_updated": "2026-01-08",
  "format": "pdf",
  "references": [
    {"type": "book", "content": "Introduction to Algorithms"},
    {"type": "web_search", "query": "Data Structures Binary Search Trees"}
  ],
  "version_history": [
    {"version": "v1.0", "date": "2026-01-07", "changes": "Initial creation"},
    {"version": "v1.1", "date": "2026-01-08", "changes": "Added AVL rotations"}
  ]
}
```

**Naming conventions**: See CLAUDE.md §File Management

## Skill Workflow

```
1. Receive subject from ORGANIZER
   ↓
2. Ask user for topic
   ↓
3. Ask user for educational level
   ↓
4. Ask user for reference material
   - Web search: "{subject} {topic}"
   - Book: Use provided title
   - URL/Material: Use as provided
   ↓
5. Ask user for output format (PDF/Markdown)
   ↓
6. Check if subjects/{subject}/notes/{topic}/ exists
   ↓
7. Generate notes aligned to educational level
   ↓
8. Save file + metadata.json
   ↓
9. Confirm to user with file location and version
```

## Quality Checklist

- [ ] Educational level appropriateness (depth, complexity, terminology)
- [ ] Academic tone throughout (no informal language)
- [ ] Completeness (all key concepts for target level)
- [ ] Visual elements (diagrams, tables, graphs where appropriate)
- [ ] Clear structure with proper headings
- [ ] References properly cited
- [ ] Reference material integrated
- [ ] Consistent formatting
- [ ] Version info displayed
- [ ] Update highlights (if updating)
- [ ] Metadata created/updated
- [ ] No file duplication (update existing)

**Academic standards**: See CLAUDE.md §Content Generation

## Error Handling

| Scenario | Error | Action |
|----------|-------|--------|
| No educational level | "Educational level required. Select Undergraduate/Graduate/Advanced." | Re-prompt |
| Invalid topic | "Topic name cannot be empty." | Re-prompt |
| No reference | "No reference provided. Generating from general knowledge." | Proceed |
| Web search fails | "Web search failed for '{subject} {topic}'. Provide alternative?" | Offer options |
| File write error | "Unable to save to {path}. Check permissions." | Report error |
| Version conflict | Use latest + 1, note in highlights | Continue |
| Reference not found | "Could not access reference. Using available resources." | Proceed |

## Skill Independence

**CRITICAL**: Operates independently after receiving subject from orchestrator.

- Does NOT call back to PROJECT ORGANIZATION
- Does NOT invoke other skills (QUIZ, PRESENTATION)
- Does NOT expose prompts/logic to other skills
- Handles ALL note generation autonomously
- Returns completion status to user only
