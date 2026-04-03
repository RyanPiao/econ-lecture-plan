# Intake Methodology

## Purpose
Collect and validate all inputs needed for the lecture preparation pipeline. Produce a structured intake document that every downstream stage will read.

---

## Process

### Step 1: Prompt for Required Fields

Ask the user for each field. Accept natural language and parse into structured format. Be conversational — this is a quick intake, not an interrogation. If the user provides everything in a single message, parse it directly without asking follow-up questions.

**Required fields** (block pipeline if missing):
- `course_title` — Full course name including number if available
- `topic_title` — The lecture topic
- `topic_number` and `total_topics` — Used to calibrate depth and cross-references
- `class_length_minutes` — Parse "75 min", "1.5 hours", "90 minutes" etc.
- `class_type` — One of: `presentation`, `lab`, `presentation + lab`

**Optional fields** (request but do not block pipeline if absent):
- `audience_level` — Default to `advanced_undergrad` if not specified
- `prerequisites_covered` — List of prior topics
- `supporting_docs_provided` — Boolean
- Any attached files or described content

### Step 2: Validate Completeness

If any required field is missing, ask the user specifically for that field before proceeding. Do not proceed with placeholders for required fields.

### Step 3: Infer Context from Topic Number

Use the topic number relative to the total to calibrate depth and tone:

| Position | Range | Calibration |
|----------|-------|-------------|
| Early | Topics 1–3 | Foundational — assume minimal prior knowledge, establish intuition before formalism |
| Middle | Topics 4 to N–3 | Building — can reference prior topics, increase formalism progressively |
| Late | Topics N–2 to N | Advanced — assume strong foundation, emphasize synthesis, integration, and real-world application |

### Step 3b: Detect Course Category

Infer `course_category` from `course_title` keywords (case-insensitive match). This field controls which content adaptations are active in all downstream stages.

| Keywords in course_title | course_category |
|--------------------------|-----------------|
| machine learning, ML, statistical learning, data analytics, econometrics | `ml-stats` |
| game theory, strategic, information economics | `game-theory` |
| microeconomic theory, optimization, equilibrium analysis | `micro-theory` |
| principles, introduction, intro | `principles` |
| money, banking, monetary, financial | `finance` |
| (no keyword match) | `general` |

If multiple keywords match, prefer the more specific category (e.g., "Statistical & Machine Learning" → `ml-stats`, not `general`).

Write `course_category` into the intake form YAML block. All downstream stages read this field.

### Step 4: Process Supporting Documents

If supporting documents (slides, textbook chapters, PDFs, notes) are provided:
1. Read them immediately and thoroughly
2. Extract: core theoretical framework, key definitions and equations, example datasets or case studies, pedagogical sequence
3. Note the document's original structure — preserve the logical flow
4. **Flag any examples using pre-2024 data** — record these in `flagged_outdated_examples` for replacement in the brainstorm stage
5. Summarize in 3–5 sentences for `supporting_docs_summary`

If no documents are provided, leave `supporting_docs_provided: false` and `supporting_docs_summary: ""`. The brainstorm stage will synthesize theory from first principles.

### Step 5: Generate Output Slug

Construct the output directory name:
- Pattern: `topic-{N:02d}-{course-code}-{kebab-case-topic}` (topic number FIRST)
- Topic number: zero-padded to 2 digits
- Course code: extract or infer from course title (e.g., "ECON 5200" → "econ5200")
- Topic slug: lowercase, spaces replaced with hyphens, remove special characters
- Example: `topic-08-econ5200-instrumental-variables`

### Step 6: Write Intake Form

Write the completed intake form to `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/intake.md` using `templates/intake-form.md`.

Confirm to the user: "Intake saved to /Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/intake.md. [If called standalone: run /brainstorm-lecture to continue. | If called from pipeline: proceeding to brainstorm stage...]"

---

## Audience Level Guide

| Level | Description | Formalism | Examples |
|-------|-------------|-----------|---------|
| `intro_undergrad` | Freshman/sophomore, first exposure to economics | Minimal math, heavy intuition | Consumer-facing companies, everyday decisions |
| `advanced_undergrad` | Junior/senior, some econometrics | Standard OLS notation, basic calculus | Industry datasets, policy applications |
| `masters` | Graduate level, strong quantitative background | Full derivations, matrix notation, proofs | Research papers, consulting cases, frontier applications |

---

## Common Parsing Examples

"I need a lecture on IV for my grad metrics class, topic 8 of 14, 75 minutes, presentation + lab" →
```yaml
topic_title: "Instrumental Variables"
audience_level: masters
topic_number: 8
total_topics: 14
class_length_minutes: 75
class_type: presentation + lab
```

"Can you help me prep a 90-minute intro undergrad lecture on supply and demand? It's the first lecture of 12." →
```yaml
topic_title: "Supply and Demand"
audience_level: intro_undergrad
topic_number: 1
total_topics: 12
class_length_minutes: 90
class_type: presentation
```
