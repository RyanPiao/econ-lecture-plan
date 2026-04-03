# econ-lecture-plan

A Claude Code skill system for economics lecture preparation. Two pipelines: convert textbook chapters into lecture materials (`/lfc`) or build lectures from scratch (`/lecture-prep`). Includes a lecture viewer web app (replaces Canva), slide manager CLI, and auto-deploy to GitHub Pages.

> Companion to [econ-research-os](https://github.com/RyanPiao/econ-research-os). Works standalone.

---

## Two Pipelines

### `/lfc` — Textbook to Lecture (recommended)

Converts a completed textbook chapter into a full lecture package. Only 2 inputs required.

```
/lfc ch14 --course econ1116
```

| Stage | What happens |
|-------|-------------|
| 1. Intake + Detect | Auto-derive metadata from textbook frontmatter + course code |
| 2. Extract + Adapt | Parse chapter, build teaching plan, Presentation Expert review |
| 3. Generate Lecture | Textbook-quality notes + retrieval practice + exit ticket + optional lab |
| 4. Generate Figures | Reuse textbook images / ebook interactive charts / generate new (min 3) |
| 5. Build Slides + Viewer | RevealJS deck + viewer web app + slide-manager + sync-slides drop folder |
| 6. Finalize | Quality gate + NLM podcast + watermark removal + 4K PNG export |

### `/lecture-prep` — From Scratch (legacy)

Builds lectures with web search, brainstorming, and 3-persona peer review. Use when no textbook exists.

```
/lecture-prep
```

| Stage | What happens |
|-------|-------------|
| 1-2 | Intake + Knowledge check |
| 3-4 | Web search brainstorm + 3-persona review |
| 5-6 | Draft notes + Interview questions |
| 7-10 | Figures + Snapshot + RevealJS + NotebookLM |

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/RyanPiao/econ-lecture-plan.git
cd econ-lecture-plan

# Symlink skills to Claude Code
mkdir -p ~/.claude/skills
for skill in skills/*/; do
  ln -sf "$(pwd)/$skill" ~/.claude/skills/"$(basename $skill)"
done

# Python dependencies (for labs + figures)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Open Claude Code

```bash
claude .
```

### 3. Prepare a lecture from a textbook chapter

```
/lfc /path/to/ch14-labor-markets.md --course econ1116
```

That's it. The pipeline runs all 6 stages automatically and produces everything in `econ-lecture-material/econ1116-principles-micro/ch14-econ1116-labor-markets-human-capital-inequality/`.

---

## Using It for Different Classes

### Course Code Mapping

The pipeline auto-detects course type and adapts all output:

| Course Code | Course Name | Type | Class Format |
|-------------|-------------|------|-------------|
| `econ1115` | Principles of Macroeconomics | Qualitative | Presentation + Activity |
| `econ1116` | Principles of Microeconomics | Qualitative | Presentation + Activity |
| `econ1916` | Game Theory (Intro) | Qualitative | Presentation + Activity |
| `econ2316` | Microeconomic Theory | Qualitative | Presentation + Activity |
| `econ2560` | Econometrics | Quantitative | Presentation + Lab |
| `econ3442` | Finance | Quantitative | Presentation + Lab |
| `econ3916` | Applied Data Analytics | Quantitative | Presentation + Lab |
| `econ4681` | Game Theory (Advanced) | Quantitative | Presentation + Activity |
| `econ5200` | Applied Data Analytics (Masters) | Quantitative | Presentation + Lab |

### What Changes by Course Type

| Element | Qualitative | Quantitative |
|---------|------------|-------------|
| Worked examples | Graphical + simple algebra | Step-by-step computation |
| Code bridges | Excel formulas | Python (sklearn, statsmodels) |
| Discussions | Policy debates, multiple valid positions | Method tradeoffs, "what goes wrong if?" |
| Labs | None (activities instead) | Jupyter + HTML companion + solutions |
| Figures | Supply/demand, game matrices | Scatter plots, ROC curves |

### Override Auto-Detection

```bash
# Principles course needs a lab day
/lfc ch05 --course econ1116 --type "presentation + lab"

# Stats course needs a debate day
/lfc ch12 --course econ3916 --type "presentation + activity"

# Longer class
/lfc ch14 --course econ1116 --duration 100
```

### New Course Not in the Mapping Table

The pipeline will scan the chapter for keyword density (qualitative vs quantitative) and ask you to confirm. To add a permanent mapping, edit `skills/chapter-to-lecture/intake-detect.md`.

---

## Next Session Guide

When you start a new Claude Code session in this project:

### Prepare a lecture

```
/lfc /path/to/chapter.md --course econ1116
```

The pipeline runs end-to-end. If interrupted, re-run the same command — it resumes from where it stopped.

### After the pipeline finishes

```bash
# Present locally
cd econ-lecture-material/econ1116-principles-micro/ch14-econ1116-labor-markets/
./viewer/serve.sh
# Open http://localhost:8080/viewer/index.html
```

### Add slides (quickest way — drop folder)

```bash
# Drop PNGs into extra-slides/ — they display full 16:9 edge-to-edge
cp ~/Downloads/new-diagram.png extra-slides/01-labor-demand.png
cp ~/Downloads/canva-export.png extra-slides/02-wage-gap.png

# One command — done
./sync-slides.sh
```

Name files to control order (`01-xxx.png`, `02-xxx.png`). Re-run to update. Delete PNGs and re-run to remove.

### Add NLM review slides (after podcast finishes ~30 min)

```bash
# Copy NLM 4K PNGs to drop folder
cp media/slides_part1/page_*.png extra-slides/
./sync-slides.sh
```

Or use `/add-nlm-slides .` for the full NLM append with divider slide.

### Edit existing slides (structured editing)

```bash
# List all slides
./slide-manager.sh list

# Add a template slide (text + image, two-column, divider)
./slide-manager.sh add content-figure --title "MRP Curve" --image figures/mrp.png --after 5

# Edit a specific slide's HTML
./slide-manager.sh edit 8

# Remove a slide
./slide-manager.sh remove 14
```

### Deploy to GitHub Pages for students

```bash
# First time: set up the course repo
# (see skills/lecture-viewer/deploy-github-pages.md)

# Start auto-sync: any edit auto-pushes to GitHub Pages
./auto-sync.sh start

# Now any save you make appears at:
# https://yourusername.github.io/econ1116-lectures/ch14/viewer/index.html

# Stop when done
./auto-sync.sh stop
```

### Which tool for what

| Need | Tool | Command |
|------|------|---------|
| Add PNGs quickly (NLM, Canva, screenshots) | **sync-slides.sh** | Drop in `extra-slides/` → `./sync-slides.sh` |
| Add structured slide (text+image, comparison) | **slide-manager.sh** | `./slide-manager.sh add content-figure ...` |
| Edit existing slide text | **slide-manager.sh** | `./slide-manager.sh edit 8` |
| NLM review slides with divider | **/add-nlm-slides** | `/add-nlm-slides .` |
| Live deploy to students | **auto-sync.sh** | `./auto-sync.sh start` |

### Keyboard shortcuts in the viewer

| Key | Action |
|-----|--------|
| Right / Space | Next slide |
| Left | Previous slide |
| G + number | Jump to slide |
| P | Presenter mode (notes + timer) |
| U | Student mode (clean) |
| O | Overview (thumbnail grid) |
| W | Open student window (dual monitor) |
| T | Toggle timer |
| L | Laser pointer |
| B | Black screen |
| F | Fullscreen |
| ? | Help |

---

## Output Structure

Output is organized by course:

```
econ-lecture-material/
├── econ1116-principles-micro/
│   └── ch14-econ1116-labor-markets-human-capital-inequality/
│       ├── intake.md                   Inputs + auto-derived metadata
│       ├── chapter-extract.md          Teaching plan + Expert recommendations
│       ├── lecture-notes.md            Textbook-quality notes
│       ├── figures/                    PNGs (150 DPI, alt text)
│       ├── presentation.html           RevealJS slides
│       ├── styles.css                  Slide theme
│       ├── slides.pdf                  PDF export
│       ├── screenshots/               Visual review
│       │
│       ├── viewer/                     Lecture viewer web app
│       │   ├── index.html             (presenter/student/overview modes)
│       │   ├── viewer.js
│       │   ├── viewer.css
│       │   └── serve.sh               Launch: ./viewer/serve.sh
│       │
│       ├── extra-slides/              ← DROP FOLDER: put PNGs here
│       │   ├── 01-labor-demand.png
│       │   └── 02-wage-gap.png
│       ├── sync-slides.sh            Run after adding PNGs to extra-slides/
│       ├── slide-manager.sh          Structured slide editing CLI
│       ├── slide-manager.py          (BeautifulSoup backend)
│       │
│       ├── pipeline-state.json        Resumption tracking
│       └── media/                     NotebookLM outputs (auto-chain)
│           ├── *-podcast.m4a          Deep Dive audio
│           ├── podcast_transcript_*.txt
│           ├── slides_part{1,2,3}.pdf  NLM slides (watermarks removed)
│           └── slides_part{1,2,3}/    4K PNGs (6000×3375px)
├── econ3916-applied-data-analytics/
│   └── ...
```

---

## All Commands

| Command | Description |
|---------|-------------|
| `/lfc [chapter] --course [code]` | Textbook → lecture (6 stages) |
| `/lecture-prep` | From-scratch lecture (10 stages) |
| `/build-viewer [dir]` | Generate viewer for existing slides |
| `/add-nlm-slides [dir]` | Append NLM PNGs as review slides |
| `/deploy-lecture [dir]` | Push to GitHub Pages |
| `/class-discussion [topic]` | Standalone discussion questions |
| `/class-poll [topic]` | Standalone poll questions |
| `/discussion-guide [path]` | Facilitation guide from notes |

---

## Skills (11 total)

```
skills/
├── chapter-to-lecture/         /lfc — 6-stage textbook→lecture pipeline
├── lecture-viewer/             Viewer + slide manager + deploy
├── lecture-pipeline/           /lecture-prep — 10-stage legacy pipeline
├── lecture-intake/             /new-lecture
├── lecture-knowledge-check/    Knowledge base deconfliction
├── lecture-brainstorm/         /brainstorm-lecture
├── lecture-review/             /review-lecture (3-persona)
├── lecture-draft/              /draft-lecture + lab generation
├── lecture-interactive/        /class-discussion /class-poll
├── lecture-interview/          Interview questions (legacy)
└── lecture-snapshot/           Knowledge snapshots
```

---

## Requirements

- [Claude Code](https://claude.ai/code) (CLI, desktop app, or VS Code extension)
- Python 3.10+ with virtualenv
- Node.js (for RevealJS scaffold + overflow checker)
- `beautifulsoup4` (for slide manager)
- `fswatch` (for auto-sync, macOS built-in)
- Optional: `notebooklm-py` (for podcast generation)
- Optional: FRED API key (for macro data in labs)

---

## See also

- [econ-research-os](https://github.com/RyanPiao/econ-research-os) — Research workflow system
- `skills/lecture-viewer/deploy-github-pages.md` — GitHub Pages setup guide
- `skills/chapter-to-lecture/pipeline.md` — Detailed pipeline logic
