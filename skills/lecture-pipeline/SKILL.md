---
name: lecture-pipeline
description: End-to-end lecture preparation pipeline for economics courses. Runs intake → brainstorm → peer-review → draft → interactive elements. Produces textbook-style lecture notes with in-class discussions, polls, and optionally Jupyter labs. Trigger: /lecture-prep
---

# Lecture Pipeline Orchestrator

Routes:
- `/lecture-prep` → Read `pipeline.md`, run all 4 stages end-to-end without stopping

## What this does
Runs the full pipeline automatically:
1. **Intake** — collect structured inputs via `lecture-intake/intake.md`
2. **Brainstorm** — generate content + interactive elements via `lecture-brainstorm/brainstorm.md` (always web-searches 2024–2026)
3. **Peer Review** — 3-persona critique via `lecture-review/peer-review.md`
4. **Draft** — textbook-style notes + discussions + polls via `lecture-draft/draft-presentation.md`; Jupyter lab via `lecture-draft/draft-lab.md` if applicable

## Output
```
output/{course-slug}-topic-{N}-{slug}/
├── intake.md
├── brainstorm.md
├── review-report.md
├── lecture-notes.md        ← always produced
└── lab.ipynb               ← if class type is "lab" or "presentation + lab"
```

All detailed logic in `pipeline.md` and the companion skill files.
