# Architecture: econ-lecture-prep

## The 10 Design Principles

---

### 1. Always Fresh — No Stale Examples

Every brainstorm stage runs a mandatory web search for 2024–2026 content regardless of whether supporting documents are provided. If documents are uploaded, the theoretical framework is extracted from them, but all examples are searched fresh. Examples older than 2024 are automatically flagged in the intake stage and replaced during brainstorm.

**Why:** Professors often teach from the same slides year after year. Students notice when examples are stale. A 2018 "recent development" actively undermines credibility.

---

### 2. Three-Reviewer Rigor

Every lecture brainstorm goes through three sequential expert reviews before drafting:
- **Pedagogy Expert** — cognitive load, scaffolding, active learning, timing
- **Domain Economist** — theoretical accuracy, rigor, literature currency
- **Industry Practitioner** — real-world relevance, example specificity, career connection

Each reviewer produces a structured report with issues categorized as `must-fix`, `should-fix`, or `nice-to-have`. The brainstorm is revised before drafting.

**Why:** A single-pass workflow produces lectures that are accurate but poorly timed, or engaging but imprecise, or rigorous but irrelevant. The three-reviewer structure catches problems across all three dimensions.

---

### 3. Textbook Quality, Not Slide Bullets

Lecture notes are complete documents — full paragraphs, interpreted equations, complete speaking notes. They are not slide outlines or bullet-point summaries. The target quality is Angrist & Pischke's "Mostly Harmless Econometrics" meets a well-organized graduate lecture.

**Why:** Instructors who teach from slides tend to skip intuition and jump to formalism. Instructors who teach from complete notes can calibrate on the fly — they know what to skip and what's essential.

---

### 4. In-Class Interactivity is Non-Negotiable

Every lecture must include:
- At least 2 Discussion blocks, each with 3 questions at Bloom's Levels 2 (Understanding), 4 (Analysis), 6 (Evaluation)
- At least 3 class poll questions in Mentimeter/iClicker format with reveal scripts
- Discussion debrief notes with bridging sentences
- A facilitation guide available on demand via `/discussion-guide`

The `lecture-interactive` skill handles standalone generation and enhancement of interactive elements.

**Why:** Research on learning science is unambiguous: students retain more from classes where they actively process material. The design forces this to be a first-class output, not an afterthought.

---

### 5. Consulting-Ready Lab Code

Lab notebooks use real data from FRED, World Bank, or Kaggle. Code is portfolio-quality: clean variable names, docstrings on custom functions, publication-quality Plotly figures. Always HC3 heteroskedasticity-robust standard errors. Comments explain both the technical mechanics AND the economic intuition.

**Why:** Students who submit clean, well-documented notebooks to GitHub get interviews. Students who submit `data = pd.read_csv('data.csv')` with no comments do not.

---

### 6. Real Data Only

The main exercises in every lab must use actual datasets. Simulations are acceptable only for illustrating statistical properties (bias, consistency, power) as supplements. No `np.random.seed(42)` fake data for primary analysis.

**Why:** Fake data teaches students to analyze fake data. Real data teaches them to handle the messiness of actual research and industry work — missing values, seasonal patterns, weird outliers, units that need conversion.

---

### 7. Student Engagement First

Every lecture opens with a hook that uses 2024–2026 data and creates genuine curiosity. Examples must use companies, industries, and events students actually care about. The test: would a student share this in a group chat or mention it over coffee?

**Why:** An engaged student who is slightly confused learns more than a bored student who "follows along." The hook creates the curiosity that makes confusion productive rather than discouraging.

---

### 8. Slim Routers, Rich Methodology

SKILL.md files are under 50 lines — just YAML metadata and routing instructions. All detailed methodology lives in separate companion .md files (`intake.md`, `brainstorm.md`, etc.) that are loaded on demand. This keeps the router lightweight and the methodology updatable without touching the router.

**Why:** Fat SKILL.md files are hard to maintain and create a wall of text that obscures what the skill actually does. Slim routers are scannable at a glance; the methodology files can be updated independently.

---

### 9. Plain Markdown Everywhere

All output is plain markdown. Git-tracked. Portable across any editor, IDE, or platform. No proprietary formats, no database dependencies.

**Why:** Markdown outputs can be version-controlled, diffed, shared, converted to PDF/Word/HTML, and opened without any special software. They survive technology changes.

---

### 10. Pipeline-First, Modular-Always

`/lecture-prep` runs everything end-to-end without stopping. But every stage — intake, brainstorm, review, draft, interactive — can also be invoked standalone. This means:
- Fresh lectures: use `/lecture-prep` for a one-command complete package
- Iterating on an existing lecture: use individual stage commands
- Adding interactive elements to legacy slides: use `/class-discussion --enhance`
- Just need polls for a topic: use `/class-poll [topic]`

**Why:** Rigid pipelines break at the first exception. Modular stages allow instructors to start midway, iterate on one stage, or use only the parts they need.

---

## File Organization

```
skills/{skill-name}/
├── SKILL.md         # Router: YAML metadata + routing rules (< 50 lines)
├── {method}.md      # Methodology: detailed logic for each command
└── templates/       # Output templates with {placeholder} variables
```

Output files are written to `output/{slug}/` where slug = `{course-code}-topic-{N:02d}-{topic-kebab-case}`.

## How Skills Are Loaded

When a user types `/lecture-prep`, Claude Code:
1. Matches the command to `lecture-pipeline/SKILL.md`
2. Reads the router, which instructs it to read `pipeline.md`
3. `pipeline.md` instructs it to read the stage-specific methodology files as it progresses
4. Each methodology file instructs it to use the corresponding template

The templates have `{placeholder}` syntax that gets replaced with actual content during execution.

## Data Flow

```
User input
    ↓
intake.md → output/{slug}/intake.md
    ↓
brainstorm.md (reads intake.md) → output/{slug}/brainstorm.md
    ↓
peer-review.md (reads brainstorm.md + intake.md) → output/{slug}/review-report.md
                                                  → revised output/{slug}/brainstorm.md
    ↓
draft-presentation.md (reads revised brainstorm.md) → output/{slug}/lecture-notes.md
draft-lab.md (reads revised brainstorm.md)          → output/{slug}/lab.ipynb
```
