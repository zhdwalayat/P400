# PRESENTATION Skill Documentation

## Overview

The PRESENTATION skill generates comprehensive, visually appealing PowerPoint presentations for any subject and topic. Receives subject from PROJECT ORGANIZATION orchestrator and handles all aspects of presentation creation including slide design, content organization, diagram integration, color theming, and professional formatting.

## Purpose

Generate academically-formatted PowerPoint presentations with modern themes, diagrams, color highlights, and topic-related visual design.

## Input Requirements

| Input | Source | Type | Required | Options/Format |
|-------|--------|------|----------|----------------|
| **Subject** | Orchestrator | String | Yes | Auto-received from PROJECT ORGANIZATION |
| **Topic** | User | String | Yes | Any specific topic (e.g., "Binary Search Trees") |
| **Reference Material** | User | Mixed | Yes | Material / Book / URL / NOTES skill output / General |
| **Number of Slides** | User | Integer | Optional | Positive integer or range (system decides if not specified) |
| **Theme Preference** | User | Enum | Optional | Auto-select (default) / Professional / Vibrant / Dark / Custom |

**CRITICAL**: Collect each requirement ONE BY ONE, not all at once.

### Reference Material Options

| Type | Example | Notes |
|------|---------|-------|
| Material | Upload or provide path | User-supplied documents/notes |
| Book | "Introduction to Algorithms" | Page numbers optional |
| URL | "https://example.com/tutorial" | Web links |
| NOTES skill | "Use NOTES for 'Binary Search Trees'" | Check `subjects/{subject}/notes/{topic}/` |
| General | No specific reference | Proceed without reference |

**Storage structure**: See CLAUDE.md §Storage & Organization

## Presentation Generation Process

### Step 1: Topic Directory Check

```
Check: subjects/{subject}/presentations/{topic}/
- IF EXISTS: Load existing, increment version
- IF NOT EXISTS: Create directory with Slides/ subfolder, set v1.0
```

### Step 2: Reference Material Processing

**If NOTES skill requested:**
1. Check `subjects/{subject}/notes/{topic}/` exists
2. Read notes file (`.pdf` or `.md`)
3. Extract concepts, structure, examples, diagrams
4. Use notes structure for presentation outline
5. Note in metadata: presentation based on NOTES skill
6. If not found: Error, request alternative reference

**Storage paths**: See CLAUDE.md §Directory Structure

### Step 3: Presentation Structure

#### Required Components

1. **Title Slide** - Title, Subject, Date, Version, Modern theme
2. **Outline/Agenda Slide** - Overview, main sections, learning objectives
3. **Content Slides** - One concept per slide, max 5-7 bullets, visual hierarchy, diagrams, color highlights
4. **Conclusion/Summary Slide** - Recap, key takeaways, connection to objectives
5. **References Slide** - All materials cited in academic format

**Academic tone requirements**: See CLAUDE.md §Content Generation

### Step 4: Visual Design Requirements

| Element | Guidelines |
|---------|-----------|
| **Academic Tone** | Formal language, scholarly terminology, objective statements, concise bullets |
| **Diagrams** | Flowcharts, trees, networks, blocks, charts/graphs, annotated images (clean, color-coded, consistent) |
| **Color Highlights** | Key terms (bold accent), definitions (subtle highlight), important points (accent/bold), categories (consistent coding) |
| **Fonts** | Headings: Bold sans-serif (32-44pt titles, 24-28pt sections) <br> Body: Clean sans-serif (18-24pt main, 14-16pt supporting) <br> Max 2-3 font families |
| **Slide Layout** | One concept per slide, 5-7 bullets max, generous white space, clear visual hierarchy |

### Step 5: Theme Selection

**Theme by Subject:**

| Subject Type | Color Scheme | Aesthetic |
|--------------|--------------|-----------|
| **STEM** | Blues, teals, grays | Modern tech |
| **Sciences** | Greens, blues | Professional scientific |
| **Humanities** | Warm tones | Elegant, classic academic |
| **Business/Economics** | Blues, grays | Corporate design |
| **Default** | Blue/gray palette | Modern minimalist |

**Modern Theme Characteristics:**
- Clean, uncluttered layouts
- Generous white space
- Flat design elements
- Modern icons and graphics
- Consistent visual language

### Step 6: Version Management

#### NEW Topics (v1.0)
```
Create: subjects/{subject}/presentations/{topic}/Slides/{topic}.pptx
Version: v1.0 (2026-01-08)
Status: Initial creation
```

#### EXISTING Topics (v1.1+)
```
Update: subjects/{subject}/presentations/{topic}/Slides/{topic}.pptx
Version: v1.1+ (2026-01-08)
Action:
1. Read existing presentation
2. Add "UPDATE HIGHLIGHTS" slide after title slide
3. Add/modify slides
4. Preserve design theme (unless user requests change)
5. Increment version, update metadata
```

**Update Highlights Slide:**
```
Title: UPDATE HIGHLIGHTS - v1.1 (2026-01-08)

Changes in this version:
• Added 5 new slides on [topic]
• Enhanced diagrams in Slides X-Y
• Updated examples in Slide Z

Slides Modified:
• Slides X-Y: [Changes]

New Slides:
• Slides A-B: [New content]
```

## Output File Structure

**Storage paths**: See CLAUDE.md §Directory Structure

```
subjects/{subject}/presentations/{topic}/
├── Slides/
│   └── {topic}.pptx
└── metadata.json
```

### Metadata File

```json
{
  "topic": "Binary Search Trees",
  "subject": "Data Structures and Algorithms",
  "current_version": "v1.1",
  "created_date": "2026-01-08",
  "last_updated": "2026-01-08",
  "number_of_slides": 18,
  "reference_material": {
    "type": "notes_skill",
    "source": "subjects/data-structures-and-algorithms/notes/binary-search-trees/binary-search-trees.pdf",
    "notes_version": "v1.0"
  },
  "theme": {
    "type": "auto_selected",
    "name": "Modern Tech Blue",
    "primary_color": "#2E5C8A",
    "secondary_color": "#4A90E2",
    "accent_color": "#FF6B35"
  },
  "features": ["Diagrams", "Color highlights", "Modern theme", "Academic tone"],
  "version_history": [
    {"version": "v1.0", "date": "2026-01-07", "changes": "Initial creation"},
    {"version": "v1.1", "date": "2026-01-08", "changes": "Added balancing slides"}
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
3. Ask user for reference material
   - If NOTES skill: Check subjects/{subject}/notes/{topic}/
   - Material/Book/URL: Use as provided
   ↓
4. Ask user for number of slides (optional)
   ↓
5. Ask user for theme preference (optional, default: auto-select)
   ↓
6. Check if subjects/{subject}/presentations/{topic}/ exists
   ↓
7. Generate presentation with:
   - Modern theme (topic-related)
   - Diagrams and visuals
   - Color highlights
   - Academic tone
   ↓
8. Save .pptx + metadata.json
   ↓
9. Confirm to user with location, version, slides, theme
```

## Quality Checklist

- [ ] Academic tone (formal language throughout)
- [ ] Modern theme (attractive, topic-related design)
- [ ] Diagrams (appropriate for complex concepts)
- [ ] Color highlights (key terms, important points)
- [ ] Professional fonts (headings + body pairing)
- [ ] Consistent color scheme
- [ ] Logical flow (title → content → conclusion → references)
- [ ] One concept per slide (no overcrowding)
- [ ] Bullet limit (5-7 max per slide)
- [ ] Reference material integrated
- [ ] Correct file structure and naming
- [ ] Version info displayed
- [ ] Update highlights (if updating)
- [ ] Metadata created/updated
- [ ] No file duplication (update existing)

**Academic standards**: See CLAUDE.md §Content Generation

## Error Handling

| Scenario | Error | Action |
|----------|-------|--------|
| No topic | "Topic name cannot be empty." | Re-prompt |
| NOTES skill not found | "Notes for '{topic}' not found. Provide alternative?" | Offer options |
| Invalid slide number | "Should be positive. Using auto-determined count." | System decides |
| Reference not accessible | "Could not access reference. Using general knowledge." | Proceed |
| File write error | "Unable to save to {path}. Check permissions." | Report error |
| Version conflict | Use latest + 1, note in highlights | Continue |

## Skill Independence

**CRITICAL**: Operates independently after receiving subject from orchestrator.

- Does NOT call back to PROJECT ORGANIZATION
- Does NOT invoke other skills (NOTES, QUIZ)
- Does NOT expose prompts/logic to other skills
- CAN READ notes from NOTES skill if user requests
- Handles ALL presentation generation autonomously
- Returns completion status to user only
