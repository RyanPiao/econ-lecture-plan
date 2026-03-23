# econ-lecture-prep

A Claude Code skill system for end-to-end economics lecture preparation — from structured intake to polished, textbook-style lecture notes with in-class discussions, class polls, and optional Jupyter labs. Built for economics professors, PhD instructors, and teaching assistants who want research-grade pedagogy without the 6-hour prep time.

**6 skills across 4 stages + standalone interactive tools. Textbook-quality output. Real data only. Always 2024–2026 examples.**

> Companion to [econ-research-os](https://github.com/RyanPiao/econ-research-os). Works standalone.

---

## What this does

```
Intake → Brainstorm → Peer Review → Draft → [Interactive Elements]
```

| Stage | What happens | Command |
|-------|-------------|---------|
| **0. Full pipeline** | Run all 4 stages end-to-end automatically | `/lecture-prep` |
| **1. Intake** | Collect course, topic, audience, class type | `/new-lecture` |
| **2. Brainstorm** | Generate theory + fresh 2024–2026 examples + interactive blueprint | `/brainstorm-lecture` |
| **3. Peer Review** | 3-persona critique: Pedagogy Expert, Domain Economist, Industry Practitioner | `/review-lecture` |
| **4. Draft** | Textbook-style notes with discussions + polls + optional Jupyter lab | `/draft-lecture` |
| **Interactive** | Standalone discussion questions, class polls, facilitation guides | `/class-discussion` `/class-poll` `/discussion-guide` |

### Output for every lecture

```
output/{course}-topic-{N}-{slug}/
├── intake.md              # Structured inputs
├── brainstorm.md          # Full content blueprint (post-review)
├── review-report.md       # 3-reviewer feedback record
├── lecture-notes.md       # Textbook-quality notes with discussions & polls
├── discussion-guide.md    # Instructor facilitation guide (optional)
└── lab.ipynb              # Jupyter lab (if class type includes lab)
```

---

## Quickstart (5 minutes)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/econ-lecture-prep.git
cd econ-lecture-prep
```

### 2. Copy skills to Claude Code

```bash
# macOS / Linux
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/

# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"
Copy-Item -Recurse -Force skills\* "$env:USERPROFILE\.claude\skills\"
```

### 3. Install Python dependencies (for lab component)

```bash
pip install -r requirements.txt
# Or with uv (faster):
uv pip install -r requirements.txt
```

### 4. Open Claude Code in this directory

```bash
claude .
```

### 5. Run the pipeline

```
/lecture-prep
```

Claude will prompt you for:
- Course title and topic
- Class length and type (presentation / lab / both)
- Audience level
- Any supporting materials (optional)

Then it runs everything automatically. Total time: 10–20 minutes for a complete lecture package.

---

## Key Design Decisions

**1. Always fresh.** Every brainstorm searches the web for 2024–2026 examples regardless of whether supporting documents are provided. Examples older than 2024 are flagged and replaced automatically.

**2. Three-reviewer rigor.** Every lecture goes through Pedagogy Expert, Domain Economist, and Industry Practitioner review before drafting. Feedback is categorized as `must-fix`, `should-fix`, or `nice-to-have`.

**3. Textbook quality.** Output reads like a well-written textbook chapter — complete paragraphs, interpreted equations, full speaking notes. Not bullet-point slides.

**4. In-class interactivity is non-negotiable.** Every lecture includes:
- Tiered discussion questions at Bloom's Levels 2 (Understanding), 4 (Analysis), and 6 (Evaluation) for each major concept
- Mentimeter/iClicker-compatible poll questions with 4 options, answer keys, and reveal scripts
- Discussion debrief notes with bridging sentences
- A standalone `/discussion-guide` command for facilitation guides

**5. Consulting-ready labs.** Lab code is portfolio-quality with deep comments explaining both the technical mechanics and the economic intuition. Real data from FRED, World Bank, Kaggle. Always HC3 robust standard errors.

**6. Real data only.** No `np.random.seed(42)` fake data in main exercises. Always source from public institutional datasets.

**7. Student engagement first.** Every topic opens with a hook from 2024–2026. Examples use companies and phenomena students actually care about. Every concept includes how practitioners use it to solve real business problems.

**8. Slim routers, rich methodology.** SKILL.md files are under 50 lines — just metadata and routing. Detailed logic lives in companion .md files loaded on demand.

**9. Plain markdown everywhere.** Git-tracked, portable, works in any editor or IDE.

**10. Pipeline-first, modular-always.** `/lecture-prep` runs everything. Each stage can also be invoked standalone for iteration.

---

## Example Usage

### Preparing a lecture from scratch

```
/lecture-prep

> Course: ECON 5200: Applied Data Analytics in Economics
> Topic: Instrumental Variables
> Topic number: 8 of 14
> Class length: 75 minutes
> Class type: presentation + lab
> Audience: masters
> Supporting materials: [attach slides or paste textbook excerpt]
```

→ Produces `output/econ5200-topic-08-instrumental-variables/` with all files.

### Generating discussion questions for an existing lecture

```
/class-discussion instrumental variables endogeneity
```

→ Produces 9 questions (3 per concept, Bloom's Levels 2/4/6) with facilitation notes.

### Creating a poll set for Mentimeter

```
/class-poll ridge and lasso regression
```

→ Produces 4 poll questions in Mentimeter-ready format with reveal scripts.

### Enhancing an existing lecture's interactive elements

```
/class-discussion --enhance output/econ5200-topic-08-instrumental-variables/lecture-notes.md
```

→ Reads the lecture notes and adds or improves all discussion/poll sections.

---

## Repo Structure

```
econ-lecture-prep/
├── README.md
├── TUTORIAL.md                      # Full walkthrough: IV lecture example
├── LICENSE
├── requirements.txt
│
├── .claude/
│   └── settings.json                # Permissions
│
├── skills/
│   ├── lecture-pipeline/            # /lecture-prep — orchestrator
│   ├── lecture-intake/              # /new-lecture
│   ├── lecture-brainstorm/          # /brainstorm-lecture
│   ├── lecture-review/              # /review-lecture
│   ├── lecture-draft/               # /draft-lecture
│   └── lecture-interactive/         # /class-discussion /class-poll /discussion-guide
│
├── output/                          # Generated lectures go here
│
├── docs/
│   ├── architecture.md              # 10 design principles
│   └── best-practices.md            # Usage guidance
│
└── examples/                        # Full IV lecture example outputs
    ├── sample-intake.md
    ├── sample-brainstorm.md
    ├── sample-review.md
    ├── sample-lecture-output.md
    ├── sample-discussion-guide.md
    └── sample-polls.md
```

---

## Requirements

- Claude Code (claude.ai/claude-code or the CLI)
- Python 3.10+ (for lab component)
- Packages: see `requirements.txt`
- Optional: FRED API key (free at fred.stlouisfed.org) for macroeconomic data in labs

---

## See also

- [TUTORIAL.md](TUTORIAL.md) — Complete walkthrough with a master's-level Instrumental Variables lecture
- [docs/architecture.md](docs/architecture.md) — Design decisions explained
- [docs/best-practices.md](docs/best-practices.md) — Tips for getting the best output
- [econ-research-os](https://github.com/RyanPiao/econ-research-os) — Companion research workflow system
