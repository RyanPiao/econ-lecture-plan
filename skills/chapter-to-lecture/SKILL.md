---
name: chapter-to-lecture
description: Convert textbook chapters into lecture materials — notes, slides, labs, figures, and viewer app. Auto-detects course type, runs Presentation Expert review, deploys to GitHub Pages. 6-stage pipeline. Trigger: /chapter-to-lecture
user_invocable:
  - /chapter-to-lecture [chapter-path] --course [code] — Run full 6-stage pipeline
---

# Chapter-to-Lecture Pipeline

Routes:
- `/chapter-to-lecture` → Read `pipeline.md`, run ALL 6 stages end-to-end without stopping. Do NOT ask the user what they want to do. Do NOT present options. Just run the pipeline.

## IMPORTANT: Execution Rules

1. **Read `pipeline.md` immediately** — it contains all logic for all 6 stages
2. **Run all 6 stages end-to-end** — do not stop between stages, do not ask "ready to proceed?"
3. **Do NOT ask what the user wants** — the command IS the instruction. `/chapter-to-lecture ch14 --course econ1116` means "run the full 6-stage pipeline on ch14 for econ1116"
4. **Only ask if required inputs are missing** — chapter path and course code. Nothing else.
5. **Auto-derive everything** — class type, audience level, chapter number, topic title all come from textbook frontmatter + course code mapping. Do not ask for these.

## What this does

Takes a textbook chapter and produces a complete lecture package:

1. **Intake + Detect** — resolve chapter path, auto-derive metadata from textbook YAML frontmatter + course code mapping table
2. **Extract + Adapt + Presentation Expert Review** — parse chapter → teaching plan → 8-point expert review
3. **Generate Lecture** — `lecture-notes.md` with retrieval practice, interactive elements, exit ticket. Optional lab for quantitative courses.
4. **Generate Figures** — reuse textbook images / ebook interactive charts / generate new (min 3)
5. **Build Slides + Viewer** — RevealJS deck + lecture viewer web app + slide-manager + sync-slides
6. **Finalize** — knowledge snapshot + quality gate + NLM podcast + watermark removal + 4K PNG export

## Parameters

| Parameter | Required | Default | Example |
|-----------|----------|---------|---------|
| chapter path | Yes | — | `ch14`, `/path/to/ch14-labor-markets.md` |
| `--course` | Yes | — | `econ1116`, `econ3916` |
| `--duration` | No | `75` | `50`, `100` |
| `--type` | No | Auto from course | `"presentation + lab"`, `"presentation + activity"` |

## Output

```
econ-lecture-material/{course_folder}/{slug}/
├── intake.md, chapter-extract.md, lecture-notes.md
├── figures/, presentation.html, styles.css, slides.pdf, screenshots/
├── viewer/ (index.html, viewer.js, viewer.css, serve.sh)
├── extra-slides/, sync-slides.sh, slide-manager.sh, slide-manager.py
├── pipeline-state.json, nlm-state.json, media/
└── [lab_*.ipynb, lab_*.html, solutions/ — if quantitative]
```

All detailed logic in `pipeline.md` and companion files (`intake-detect.md`, `extract-adapt.md`, `generate-lecture.md`, `finalize.md`).
