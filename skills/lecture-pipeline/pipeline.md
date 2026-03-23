# Lecture Pipeline — End-to-End Logic

## Purpose
Run all four lecture preparation stages as a single, uninterrupted workflow. Each stage reads the output of the previous stage. Do not pause between stages unless a required input is missing.

---

## Pre-Flight Check

Before starting, confirm:
1. Is the user invoking `/lecture-prep` for a new lecture or continuing from a saved intake?
2. Are any supporting documents (slides, textbook chapters, notes) attached to the conversation?
3. Does an `output/` directory exist? (It should — if not, create it.)

If invoking fresh: proceed to Stage 1.
If continuing from saved intake: skip to Stage 2 and read the existing `intake.md`.

---

## Stage 1: Intake

**Read:** `skills/lecture-intake/intake.md`
**Template:** `skills/lecture-intake/templates/intake-form.md`

Collect all required fields:
- Course Title
- Topic Title
- Topic Number / Total Topics
- Class Length (minutes)
- Class Type: `presentation` | `lab` | `presentation + lab`
- Target Audience Level: `intro_undergrad` | `advanced_undergrad` | `masters`
- Prerequisites Covered (optional)
- Supporting Materials (optional — upload or describe)

**Slug generation rule:** `{course-code}-topic-{N}-{kebab-case-topic-title}`
Example: `econ5200-topic-08-instrumental-variables`

**Output:** Write `output/{slug}/intake.md` using the intake form template.

**Transition:** Announce "Intake complete. Moving to brainstorm stage..." then immediately proceed.

---

## Stage 2: Brainstorm

**Read:** `skills/lecture-brainstorm/brainstorm.md`
**Template:** `skills/lecture-brainstorm/templates/brainstorm-output.md`

**Always perform web search** regardless of whether supporting documents were provided. Search for:
- Industry case studies using this concept (2024–2026)
- Recent academic findings or data releases
- News hooks relevant to college students
- Current labor market / business applications

If supporting documents were provided:
- Extract the theoretical framework
- Flag any examples using pre-2024 data — replace them silently with 2024–2026 equivalents

Produce all sections A through I of the brainstorm template (A = Opening Hook through I = Interactive Classroom Elements).

**Output:** Write `output/{slug}/brainstorm.md`.

**Transition:** Announce "Brainstorm complete. Moving to peer review..." then immediately proceed.

---

## Stage 3: Peer Review

**Read:** `skills/lecture-review/peer-review.md`
**Template:** `skills/lecture-review/templates/review-report.md`

Run three reviewers sequentially:
1. **Pedagogy Expert** — cognitive load, scaffolding, active learning, timing
2. **Domain Economist** — theoretical accuracy, rigor, literature currency
3. **Industry Practitioner** — real-world relevance, example specificity, career connection

After all three reviews:
- Categorize feedback: `must-fix` | `should-fix` | `nice-to-have`
- Revise brainstorm incorporating all `must-fix` and `should-fix` items
- Note skipped `nice-to-have` items with reasons

**Output:** Write `output/{slug}/review-report.md`. Pass the revised brainstorm to Stage 4.

**Transition:** Announce "Review complete. Moving to draft stage..." then immediately proceed.

---

## Stage 4: Draft

**Read:** `skills/lecture-draft/draft-presentation.md` (always)
**Read:** `skills/lecture-draft/draft-lab.md` (only if class type is `lab` or `presentation + lab`)
**Templates:** `skills/lecture-draft/templates/lecture-notes.md` and optionally `lab-notebook.py`

Transform the reviewed brainstorm into:
1. **Textbook-style lecture notes** with complete paragraphs, full speaking notes, and mandatory interactive sections:
   - `## 💬 In-Class Discussion` — per major concept, tiered by Bloom's taxonomy
   - `## 📊 Class Poll` — Mentimeter/iClicker compatible questions
   - `## 🔄 Discussion Debrief` — facilitation closure notes
2. **Jupyter lab notebook** (if applicable) — real data, consulting-ready code, guided → open-ended progression

**Output:**
- Write `output/{slug}/lecture-notes.md`
- Write `output/{slug}/lab.ipynb` (if applicable, convert from Python script via jupytext format)

---

## Pipeline Completion

After Stage 4, output a summary:

```
## ✅ Lecture Prep Complete

**Course:** {Course Title}
**Topic:** {Topic Title} (Topic {N} of {Total})
**Class type:** {presentation | lab | presentation + lab}
**Duration:** {X} minutes

**Files created:**
- output/{slug}/intake.md
- output/{slug}/brainstorm.md
- output/{slug}/review-report.md
- output/{slug}/lecture-notes.md
[- output/{slug}/lab.ipynb]

**Interactive elements generated:**
- {N} in-class discussion question sets
- {N} class poll questions (Mentimeter/iClicker ready)
- {N} discussion debrief guides

**Peer review summary:**
- {N} must-fix items addressed
- {N} should-fix items addressed
- {N} nice-to-have items noted but not incorporated
```

---

## Key Rules (enforced at every stage)

1. **Never use examples older than 2024** unless historically significant. Always web-search for the most recent credible data.
2. **No vague claims.** Every factual claim must cite a named source (institution, study, report) with URL when available.
3. **Every equation must be interpreted.** Never present math without plain-language interpretation.
4. **Every industry example must name the company, the problem, the method, and the quantified outcome.**
5. **Time allocations must be realistic.** If content exceeds class time, cut — don't compress.
6. **Interactive elements are non-negotiable.** Every lecture must have at least 2 discussion question sets and 3 poll questions.
7. **Student engagement first.** Examples should use companies, industries, and events students actually care about.
