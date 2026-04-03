---
name: lecture-draft
description: Produce textbook-style lecture notes with in-class discussions, class polls, and discussion debriefs. Optionally produce a Jupyter lab notebook and its styled HTML companion. Trigger: /draft-lecture (or called automatically by /lecture-prep)
---

# Lecture Draft

Routes:
- `/draft-lecture` → Read `draft-presentation.md`, produce lecture notes. If class type includes lab, also read `draft-lab.md` and produce Jupyter notebook + HTML companion.
- `/draft-lecture --notes-only` → Produce lecture notes only, skip lab even if class type includes lab
- `/draft-lecture --lab-only` → Produce Jupyter lab only (skips or updates notes)
- `/draft-lab-html` → Read existing `.ipynb`, generate styled HTML companion only. Accepts folder path as argument: `/draft-lab-html {base}/{slug}/`

## Input
Reads the revised `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/brainstorm.md` (post-review).
Also reads `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/intake.md` for class type, audience level, and timing.

## Output
- `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/lecture-notes.md` — textbook-style notes with interactive elements (always)
- `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/lab_{N}_{short_name}.ipynb` — Jupyter notebook (only if class_type includes lab). `{N}` is the topic number, `{short_name}` is a brief snake_case descriptor (e.g., `lab_15_polynomial_trap`).
- `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/lab_{N}_{short_name}.html` — Styled HTML companion for the lab (produced automatically alongside `.ipynb`). Includes Warning Box, AI-Assisted Expansion (P.R.I.M.E.), and Digital Portfolio sections.

## Key rules for this stage
- **Lecture notes are complete documents** — not slide outlines. Full paragraphs, complete sentences, all equations interpreted.
- **In-class discussions, polls, and debriefs are mandatory** — every major concept gets at least one interactive element.
- **Speaking notes must be specific** — actual sentences an instructor says, not "discuss the concept."
- **Every equation must be interpreted** in plain English immediately after it appears.
- **Every industry example must be complete** — company, problem, method, outcome, source.

Detailed methodology in `draft-presentation.md`, `draft-lab.md`, and `draft-lab-html.md`.
