---
name: lecture-draft
description: Produce textbook-style lecture notes with in-class discussions, class polls, and discussion debriefs. Optionally produce a Jupyter lab notebook. Trigger: /draft-lecture (or called automatically by /lecture-prep)
---

# Lecture Draft

Routes:
- `/draft-lecture` → Read `draft-presentation.md`, produce lecture notes. If class type includes lab, also read `draft-lab.md` and produce Jupyter notebook.
- `/draft-lecture --notes-only` → Produce lecture notes only, skip lab even if class type includes lab
- `/draft-lecture --lab-only` → Produce Jupyter lab only (skips or updates notes)

## Input
Reads the revised `output/{slug}/brainstorm.md` (post-review).
Also reads `output/{slug}/intake.md` for class type, audience level, and timing.

## Output
- `output/{slug}/lecture-notes.md` — textbook-style notes with interactive elements (always)
- `output/{slug}/lab.ipynb` — Jupyter notebook (only if class_type includes lab)

## Key rules for this stage
- **Lecture notes are complete documents** — not slide outlines. Full paragraphs, complete sentences, all equations interpreted.
- **In-class discussions, polls, and debriefs are mandatory** — every major concept gets at least one interactive element.
- **Speaking notes must be specific** — actual sentences an instructor says, not "discuss the concept."
- **Every equation must be interpreted** in plain English immediately after it appears.
- **Every industry example must be complete** — company, problem, method, outcome, source.

Detailed methodology in `draft-presentation.md` and `draft-lab.md`.
