# Stage 1: Intake + Course Category Detection

## Purpose

Collect minimal inputs for the chapter-to-lecture conversion. Everything else is auto-derived from the textbook chapter metadata and course code. The textbook already defines the content, audience, and depth — this stage just identifies the source and detects course type.

---

## Inputs to Collect

| Field | Required | Default | Example |
|-------|----------|---------|---------|
| `chapter_path` | Yes | — | `/path/to/ch14-labor-markets-human-capital-inequality.md` |
| `course_code` | Yes | — | `econ1116`, `econ3916`, `econ5200` |
| `class_duration` | No | `75` | `50`, `75`, `100` |
| `class_type` | No | Auto-derived | Override: `presentation`, `lab`, `presentation + lab`, `presentation + activity` |

**Class type override:** If the user provides `--type`, use it. Otherwise auto-derive from course category. This handles edge cases like a principles course needing a lab day or a stats course needing a debate.

**Everything else is auto-derived:**
- `chapter_number` → from chapter YAML frontmatter (`chapter:` field) or filename `ch{NN}-`
- `topic_title` → from chapter `# ` heading or frontmatter `title:` field
- `total_topics` → from frontmatter `cross_refs_to:` array length or course mapping
- `audience_level` → from course code mapping (see table below)
- `class_type` → auto-determined by course category:
  - `qualitative` → `presentation + activity` (discussions, simulations, debates)
  - `quantitative` → `presentation + lab` (Jupyter labs, code exercises)
- `builds_on` → from frontmatter `builds_on:` array
- `recurring_threads` → from frontmatter `recurring_threads:` array

**No manual input needed for class_type or audience_level** — the textbook and course code contain all the information.

---

## Chapter Path Resolution

Accept any of:
- Full path: `/Users/openclaw/Resilio Sync/documents/econ-project-book/principles-of-microeconomics/chapters/ch14-labor-markets-human-capital-inequality.md`
- Short form: `ch14` → scan known textbook directories for matching chapter
- Relative: `ch14-labor-markets-human-capital-inequality.md` → resolve relative to CWD

**Known textbook directories (scan in order):**
1. `/Users/openclaw/Resilio Sync/documents/econ-project-book/principles-of-microeconomics/chapters/`
2. `/Users/openclaw/Resilio Sync/documents/econ-project-book/` (any subdirectory matching `chapters/`)

If no match found: ask the user for the full path.

---

## Chapter Metadata Extraction

Read the chapter's YAML frontmatter to extract:
```yaml
chapter: 14
title: "Labor Markets, Human Capital, and Inequality"
status: first-draft
word_count_target: 9500
learning_outcomes: [LO14.1, LO14.2, LO14.3, LO14.4, LO14.5]
builds_on: [4, 5, 8, 10]
cross_refs_to: [1, 3, 9, 15, 16, 19]
recurring_threads: ["Your Career", "AI Everywhere", "Uber & Gig Economy"]
```

These fields inform:
- `builds_on` → connections section ("Building On" in lecture notes)
- `cross_refs_to` → forward seeds ("Setting Up" in lecture notes)
- `recurring_threads` → which narrative threads to weave into the lecture
- `learning_outcomes` → learning objectives for the lecture

---

## Course Category Detection

### Step 1: Check known course code mappings

| Course Code | Category | Sub-category | Audience | Auto class_type | Course Folder |
|------------|----------|-------------|----------|----------------|---------------|
| `econ1115` | `qualitative` | `principles` | `intro_undergrad` | `presentation + activity` | `econ1115-principles-macro` |
| `econ1116` | `qualitative` | `principles` | `intro_undergrad` | `presentation + activity` | `econ1116-principles-micro` |
| `econ1916` | `qualitative` | `game-theory` | `intro_undergrad` | `presentation + activity` | `econ1916-game-theory-intro` |
| `econ2316` | `qualitative` | `micro-theory` | `advanced_undergrad` | `presentation + activity` | `econ2316-micro-theory` |
| `econ3442` | `quantitative` | `finance` | `advanced_undergrad` | `presentation + lab` | `econ3442-finance` |
| `econ3916` | `quantitative` | `ml-stats` | `advanced_undergrad` | `presentation + lab` | `econ3916-applied-data-analytics` |
| `econ4681` | `qualitative` | `game-theory` | `advanced_undergrad` | `presentation + activity` | `econ4681-game-theory-advanced` |
| `econ5200` | `quantitative` | `ml-stats` | `masters` | `presentation + lab` | `econ5200-applied-data-analytics` |
| `econ2560` | `quantitative` | `econometrics` | `advanced_undergrad` | `presentation + lab` | `econ2560-econometrics` |

### Step 2: If course code not in table, scan chapter content

Count keyword density in the chapter text:

**Quantitative keywords:** regression, classification, estimation, hypothesis, probability, forecast, sampling, OLS, logistic, bias, variance, MSE, cross-validation, regularization, gradient, optimization, matrix, coefficient, p-value, confidence interval, standard error, R-squared, AIC, BIC, LASSO, ridge, random forest, neural network, clustering, PCA, time series, panel data, instrumental variable, difference-in-differences, causal inference, bootstrap, Monte Carlo

**Qualitative keywords:** market structure, welfare, externalities, consumer choice, trade, behavioral, policy, institutions, monopoly, oligopoly, competition, equilibrium, surplus, deadweight loss, elasticity, supply, demand, utility, indifference, budget constraint, game theory, Nash, prisoner's dilemma, public goods, commons, moral hazard, adverse selection, regulation, antitrust, labor market, inequality, growth, inflation, fiscal, monetary

If quantitative keywords ≥ 1.5× qualitative: `quantitative`
If qualitative keywords ≥ 1.5× quantitative: `qualitative`
Otherwise: ask user to confirm.

---

## Slug Generation

Format: `ch{NN:02d}-{course-code}-{kebab-case-title}`

Examples:
- `ch01-econ1116-economics-is-everywhere`
- `ch14-econ1116-labor-markets-human-capital-inequality`
- `ch15-econ3916-bias-variance-tradeoff`

---

## Output Path

**Base path:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/`
**Course folder:** `{course_folder}` from the mapping table above (e.g., `econ1116-principles-micro`)
**Full output:** `{base}/{course_folder}/{slug}/`

Example: `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/econ1116-principles-micro/ch14-econ1116-labor-markets-human-capital-inequality/`

For unknown course codes, generate the course folder as `{course_code}-{kebab-course-title}` (ask user for course title if not in mapping).

Create the course folder if it doesn't exist: `mkdir -p "{base}/{course_folder}"`

## Output

Write `{base}/{course_folder}/{slug}/intake.md` using the template at `templates/intake-form.md`.

The intake file must include:
- `course_code`, `course_category`, `course_subcategory`, `course_folder`
- `chapter_number`, `topic_title`, `chapter_source_path`, `chapter_word_count`
- `class_duration`, `class_type` (auto-derived)
- `audience_level` (auto-derived)
- `detection_method`: `known_mapping` or `keyword_scan` or `user_confirmed`
- `builds_on`, `cross_refs_to`, `recurring_threads` (from frontmatter)
- `learning_outcomes` (from frontmatter)
- `output_dir`: full path to the lecture output directory

---

## Transition

After writing `intake.md`:
```
✅ Stage 1 complete — {course_code} detected as {course_category} ({course_subcategory})
   Chapter: ch{NN} "{topic_title}" ({word_count} words)
   Auto-derived: {audience_level}, {class_type}, {class_duration} min
   Builds on chapters: {builds_on}
   Threads: {recurring_threads}
   Moving to extract + adapt...
```
