---
name: lecture-pipeline
description: End-to-end lecture preparation pipeline for economics courses. Runs intake → brainstorm → peer-review → draft → figures → snapshot → RevealJS slides. Produces textbook-style lecture notes with figures, RevealJS slide deck (HTML + PDF via DeckTape), in-class discussions, polls, and optionally Jupyter labs. Trigger: /lecture-prep
---

# Lecture Pipeline Orchestrator

Routes:
- `/lecture-prep` → Read `pipeline.md`, run all 10 stages end-to-end without stopping
- `/nlm-p2`, `/nlm-p3`, `/nlm-p4` → Manual fallbacks if NLM auto-chain (Stage 10) fails

## What this does
Runs the full pipeline automatically:
1. **Intake** — collect structured inputs via `lecture-intake/intake.md`
2. **Knowledge Check** — scan `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/` (lectures, papers, research) for prior content; build Consistency Context Report via `lecture-knowledge-check/knowledge-check.md`
3. **Brainstorm** — generate content respecting knowledge-context.md hard constraints via `lecture-brainstorm/brainstorm.md` (always web-searches 2024–2026)
4. **Peer Review** — 3-persona critique via `lecture-review/peer-review.md`
5. **Draft** — textbook-style notes + discussions + polls via `lecture-draft/draft-presentation.md`; Jupyter lab + styled HTML companion via `lecture-draft/draft-lab.md` and `lecture-draft/draft-lab-html.md` if applicable
6. **Interview Questions** *(conditional — data/econ/stat/ML courses)* — generates `interview-questions.md` with 12–18 technical interview questions
7. **Figure Generation** *(mandatory)* — generates matplotlib/plotly/networkx figures for all charts, tables, and diagrams in the notes → `figures/figure_NNN_slug.png`; inserts refs into `lecture-notes.md`
8. **Save Snapshot** — extract and save compact knowledge snapshot to `econ-lecture-knowledge/lectures/` via `lecture-snapshot/snapshot.md`
9. **RevealJS Slides** *(mandatory)* — converts `lecture-notes.md` to RevealJS deck; speaking notes → `<aside>`; figures embedded as `<img>`; overflow checked; exports `presentation.html` + `slides-revealjs.pdf` (DeckTape) + `screenshots-revealjs/`
10. **NotebookLM Phase 1** *(auto-run)* — creates NotebookLM notebook, uploads lecture notes, triggers Deep Dive audio, launches auto-chain for transcription + NLM slides + 4K PNGs

## Output
```
/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/
├── KNOWLEDGE.md            ← index of all snapshots
├── lectures/               ← one snapshot per completed lecture
├── papers/                 ← paper snapshots from /read-paper
└── research/               ← synthesis docs from /lit-review etc.

/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/topic-{N}-{course-code}-{slug}/
├── intake.md
├── knowledge-context.md    ← consistency constraints loaded from knowledge base
├── brainstorm.md
├── review-report.md
├── lecture-notes.md        ← always produced (includes embedded figure references)
├── interview-questions.md  ← if data/econ/stat/ML course (Stage 6)
├── lab_{N}_{short_name}.ipynb ← student version with blanks (e.g., lab_18_model_evaluation.ipynb)
├── lab_{N}_{short_name}.html  ← styled HTML companion (e.g., lab_18_model_evaluation.html)
├── solutions/
│   └── lab_{N}_{short_name}_solutions.ipynb ← instructor answer key (all blanks filled, cells executed)
├── pipeline-state.json     ← tracks last completed stage for resumption
├── figures/                ← matplotlib PNGs at 150 dpi (mandatory, Stage 7)
│   └── figure_NNN_slug.png
├── presentation.html       ← RevealJS deck (open directly in browser, no build step)
├── styles.css              ← custom theme
├── slides-revealjs.pdf     ← DeckTape PDF export (mandatory, Stage 9)
├── screenshots-revealjs/   ← visual review PNGs from DeckTape (mandatory, Stage 9)
├── slides-png/             ← Canva-ready high-res PNGs (6000×3375px, 300 DPI, Stage 9)
│   └── slide_001.png ... slide_NNN.png
└── media/                  ← produced by Stage 10 auto-chain
    ├── {slug}-podcast.m4a
    ├── podcast_transcript_001.txt
    ├── podcast_transcript_002.txt
    ├── podcast_transcript_003.txt
    ├── slides_part1.pdf
    ├── slides_part2.pdf
    ├── slides_part3.pdf
    ├── slides_part1/page_001.png ...
    ├── slides_part2/page_001.png ...
    └── slides_part3/page_001.png ...
```

**Resumption:** If the pipeline fails mid-run, re-invoke `/lecture-prep` — it will detect `pipeline-state.json` and resume from the last completed stage. No need to restart from scratch.

All detailed logic in `pipeline.md` and the companion skill files.
