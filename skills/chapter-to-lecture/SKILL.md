---
name: chapter-to-lecture
description: Convert textbook chapters into lecture materials — notes, slides, labs, figures, and viewer app. Auto-detects course type, runs Presentation Expert review, deploys to GitHub Pages. 6-stage pipeline. Trigger: /lecture-from-chapter or /lfc
user_invocable:
  - /lecture-from-chapter [chapter-path] --course [code] — Run full 6-stage pipeline
  - /lfc [chapter-path] --course [code] — Alias for /lecture-from-chapter
---

# Chapter-to-Lecture Pipeline

Routes:
- `/lecture-from-chapter [chapter-path] --course [code]` → Run all 6 stages end-to-end
- `/lfc [chapter-path] --course [code]` → Alias
- `/lfc [chapter-path] --course [code] --duration [min]` → Override 75 min default
- `/lfc [chapter-path] --course [code] --type [class-type]` → Override auto-derived class type

**Only 2 required inputs:** chapter path + course code. Everything else auto-derived from textbook YAML frontmatter and course code mapping.

## 6-Stage Pipeline

1. **Intake + Detect** — resolve chapter, auto-derive all metadata from textbook frontmatter + course code mapping. Course folder created.
2. **Extract + Adapt + Presentation Expert Review** — parse chapter → teaching plan → 8-point expert review (objective feasibility, narrative arc, cognitive load, visual flow, engagement, assessment alignment, content integrity, instructor confidence)
3. **Generate Lecture** — `lecture-notes.md` with retrieval practice, duration-scaled interactions, exit ticket. Optional Jupyter lab for quantitative courses. Sentinel marker appended.
4. **Generate Figures** — batch execution with partial-failure recovery. Reuse textbook images where suitable. Alt text required. Min 3.
5. **Build Slides + Viewer** — RevealJS deck (DeckTape `--pause 3000`) + lecture-viewer web app (presenter/student/overview modes, dual-monitor, timer, laser, themes)
6. **Finalize** — knowledge snapshot + quality gate (checks all new sections) + NLM with PID tracking + failure notification

## Course Category Detection

Auto-derived from course code mapping:
- `qualitative` → `presentation + activity` (principles, micro-theory, game-theory)
- `quantitative` → `presentation + lab` (ml-stats, econometrics, finance)

Override with `--type` when needed (e.g., principles course needs a lab day).

## Output (nested by course)

```
/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{course_folder}/{slug}/
├── intake.md                   Stage 1
├── chapter-extract.md          Stage 2 (with Presentation Expert recommendations)
├── lecture-notes.md            Stage 3 (with retrieval practice + exit ticket + sentinel)
├── lab_*.ipynb                 Stage 3 (if quantitative + lab)
├── lab_*.html                  Stage 3 (HTML companion)
├── solutions/                  Stage 3 (instructor answer key)
├── figures/*.png               Stage 4 (150 DPI, alt text)
├── presentation.html           Stage 5 (RevealJS)
├── styles.css                  Stage 5
├── slides.pdf                  Stage 5 (DeckTape, MathJax-safe)
├── screenshots/                Stage 5
├── viewer/                     Stage 5 (Canva replacement)
│   ├── index.html, viewer.js, viewer.css, serve.sh
├── slide-manager.sh            Edit slides without raw HTML
├── slide-manager.py            BeautifulSoup backend
├── sync-slides.sh              Drop PNGs in extra-slides/, run this
├── extra-slides/               Drop folder for quick PNG slide adds
├── pipeline-state.json         v2 (pending/in_progress/completed)
├── .pipeline-lock              Concurrency protection
├── nlm-state.json              Stage 6 (includes chain PID)
└── media/                      Stage 6 (NLM auto-chain)
```

## Pipeline Engineering

- **State:** 3 statuses (pending/in_progress/completed). In_progress = restart on resume.
- **Lock file:** `.pipeline-lock` with PID. Dead PID = stale (auto-removed).
- **Re-read from disk:** Never rely on working memory across stages.
- **Batch figures:** Write all scripts first, execute in batch, partial failure OK.
- **Deconfliction:** Filtered by course code (not full KB scan).

## Differences from `/lecture-prep`

| Aspect | `/lecture-prep` | `/lfc` |
|--------|----------------|--------|
| Source | Web search + brainstorm | Textbook chapter |
| Stages | 10 | 6 |
| Tokens | ~101K | ~56K |
| Review | 3-persona critique | Single Presentation Expert |
| Interview Qs | Generated here | Moved to textbook pipeline |
| Slides | RevealJS + Canva PNGs | RevealJS + Viewer web app |
| Output | Flat directory | Nested by course folder |
| Interactions | Fixed (2 disc + 3 poll) | Duration-scaled formula |

All detailed logic in `pipeline.md` and companion files.
