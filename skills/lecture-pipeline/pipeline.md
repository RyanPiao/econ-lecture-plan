# Lecture Pipeline — End-to-End Logic

## Purpose
Run all lecture preparation stages as a single, uninterrupted workflow. Each stage reads the output of the previous stage. Do not pause between stages unless a required input is missing.

**Token efficiency:** Once `lecture-notes.md` is produced in Stage 5, keep its content in working memory. Do NOT re-read it in Stages 7–10 — use the in-memory version.

**Skill file reads:** For skill files exceeding ~100 lines, read only the section headers and the section matching current parameters (e.g., skip lab instructions if class type is presentation-only).

**State tracking:** After each stage completes (at every `**→**` transition), update `{base}/{slug}/pipeline-state.json`: set that stage's status to `"completed"` and update `last_completed_stage`. This enables resumption if the pipeline fails mid-run.

---

## Pre-Flight Check

1. New lecture or continuing from saved intake?
2. Any supporting documents attached?
3. `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/` exists? (create if not)

**Resume check:** If `{base}/{slug}/pipeline-state.json` exists, read `last_completed_stage`:
- Print: `"⏩ Resuming from Stage {last_completed_stage + 1}..."`
- Before skipping any stage, verify its output file exists on disk. If a "completed" stage's output is missing, re-run from that stage instead.
- Skip all stages up to and including `last_completed_stage`. Begin execution at the next stage.

If no `pipeline-state.json` exists:
- If `intake.md` exists AND `knowledge-context.md` exists: skip to Stage 3, read existing `intake.md`.
- If `intake.md` exists but NO `knowledge-context.md`: skip to Stage 2 (Knowledge Check), read existing `intake.md`.
- Otherwise: proceed to Stage 1 (fresh start).

**Initialize state file:** At pipeline start (after Pre-Flight Check), create or update `{base}/{slug}/pipeline-state.json`:
```json
{
  "slug": "{slug}",
  "topic_number": {N},
  "topic_title": "{topic_title}",
  "last_completed_stage": 0,
  "stages": {
    "1": {"status": "pending", "output": "intake.md"},
    "2": {"status": "pending", "output": "knowledge-context.md"},
    "3": {"status": "pending", "output": "brainstorm.md"},
    "4": {"status": "pending", "output": "review-report.md"},
    "5": {"status": "pending", "output": "lecture-notes.md"},
    "6": {"status": "pending", "output": "interview-questions.md"},
    "7": {"status": "pending", "output": "figures/"},
    "8": {"status": "pending", "output": "econ-lecture-knowledge/lectures/{slug}.md"},
    "9": {"status": "pending", "output": "presentation.html"},
    "10": {"status": "pending", "output": "nlm-state.json"}
  }
}
```
If resuming, preserve existing completed stages — only initialize pending ones.

---

## Stage 1: Intake

**Read:** `skills/lecture-intake/intake.md`
**Template:** `skills/lecture-intake/templates/intake-form.md`

Collect: Course Title, Topic Title, Topic Number/Total, Class Length, Class Type (`presentation` | `lab` | `presentation + lab`), Audience Level, Prerequisites (optional), Supporting Materials (optional).

**Slug:** `topic-{N:02d}-{course-code}-{kebab-case-topic-title}` (topic number FIRST, zero-padded, e.g., `topic-08-econ5200-instrumental-variables`)

**Output:** Write `{base}/{slug}/intake.md` where `{base}` = `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material`.

**→** "Intake complete. Moving to knowledge check..."

---

## Stage 2: Knowledge Base Check (always run before brainstorm)

**Read:** `skills/lecture-knowledge-check/knowledge-check.md`

- If knowledge-rag MCP connected → semantic queries (`search_knowledge(..., category="lecture")`)
- Otherwise → file scan `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/`

If snapshots exist: write `{base}/{slug}/knowledge-context.md` (Consistency Context Report).
If none: note "First lecture for this course." and proceed.

**Output:** `{base}/{slug}/knowledge-context.md`

**→** "Knowledge check complete. Moving to brainstorm..."

**Checkpoint before Stage 3:** Before proceeding, verify one of the following is true:
- `{base}/{slug}/knowledge-context.md` exists on disk (Stage 2 produced it), **OR**
- No snapshots exist in `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/` for this course code (first lecture — Stage 2 correctly found nothing)

If neither condition is met, **STOP** and re-run Stage 2. Do not proceed to Stage 3.

---

## Stage 3: Brainstorm

**Read:** `skills/lecture-brainstorm/brainstorm.md`, `knowledge-context.md` (treat as hard constraints)
**Template:** `skills/lecture-brainstorm/templates/brainstorm-output.md`

Always web-search: industry case studies (2024–2026), recent data, news hooks, labor market applications.
If supporting docs provided: extract theory, replace pre-2024 examples with 2024–2026 equivalents.
Produce all sections A–I of the brainstorm template.

**Output:** `{base}/{slug}/brainstorm.md`

**→** "Brainstorm complete. Moving to peer review..."

---

## Stage 4: Peer Review

**Read:** `skills/lecture-review/peer-review.md`
**Template:** `skills/lecture-review/templates/review-report.md`

Run 3 reviewers: Pedagogy Expert → Domain Economist → Industry Practitioner.
Categorize: `must-fix` | `should-fix` | `nice-to-have`. Incorporate must-fix and should-fix.

**Output:** `{base}/{slug}/review-report.md`. Pass revised brainstorm to Stage 5.

**→** "Review complete. Moving to draft..."

---

## Stage 5: Draft

**Read:** `skills/lecture-draft/draft-presentation.md`
**Read also (if lab):** `skills/lecture-draft/draft-lab.md`
**Templates:** `skills/lecture-draft/templates/lecture-notes.md` and optionally `lab-notebook.py`

Produce:
1. Textbook-style lecture notes with full speaking notes, `## 💬 In-Class Discussion`, `## 📊 Class Poll`, `## 🔄 Discussion Debrief` per major concept
2. `lab_{N}_{short_name}.ipynb` if class type includes lab (real data, guided → open-ended). `{N}` = topic number; `{short_name}` = brief snake_case descriptor (2-4 words, e.g., `lab_15_polynomial_trap`). Do NOT include course title inside the notebook — it's shared across course sections.

### Stage 5b: Solutions Notebook (conditional — same condition as lab)

After writing the student notebook, produce `solutions/lab_{N}_{short_name}_solutions.ipynb`:
1. Copy the student notebook
2. Fill in all `___` blanks and TODO sections with correct answers
3. Execute all cells so outputs are visible
4. Save to `{base}/{slug}/solutions/`

This is the instructor's answer key — not distributed to students.

### Stage 5c: Lab HTML Companion (conditional — same condition as lab)

**Read:** `skills/lecture-draft/draft-lab-html.md`
**Template:** `skills/lecture-draft/templates/lab-html-template.html`

If lab was produced:
1. Parse the just-written `lab_{N}_{short_name}.ipynb` (use working memory — do not re-read)
2. **Cell classification:** Parse each `.ipynb` code cell. If it contains `TODO`, `___`, or `YOUR CODE HERE`, render as EXERCISE (red border, blanks preserved, hint box). Otherwise render as GUIDED (green border, full code). If it contains `optional`/`extension`/`challenge`, render as OPTIONAL (purple border). The HTML must NOT be an answer key — exercise cells show blanks only.
3. Generate styled HTML following the template and conversion rules in `draft-lab-html.md`
4. Inject pedagogical sections: "How This Lab Works" legend, Warning Box (3–5 data pitfalls specific to this lab), section banners, AI-Assisted Expansion (P.R.I.M.E. prompt), Digital Portfolio
5. Strip all citation markers (`[1]`, `[2]`, etc.)
6. Write `{base}/{slug}/lab_{N}_{short_name}.html`
7. Verify the file was written successfully

**Output:**
- `{base}/{slug}/lecture-notes.md` ← keep in working memory for all subsequent stages
- `{base}/{slug}/lab_{N}_{short_name}.ipynb` (if applicable)
- `{base}/{slug}/lab_{N}_{short_name}.html` (if lab was produced)

**→** "Draft complete. Moving to interview questions..."

---

## Stage 6: Interview Questions (conditional)

**Read:** `skills/lecture-interview/interview-questions.md`

**Condition:** Check `course_title` + `topic_title` for keywords: `econometrics`, `statistics`, `statistical`, `data`, `machine learning`, `ML`, `regression`, `classification`, `causal`, `inference`, `panel`, `time series`, `forecast`, `clustering`, `neural`, `NLP`, `analytics`, `quantitative`

If applicable: generate 12–18 questions across 5 categories (Concept & Intuition, Technical Implementation, Assumptions & Edge Cases, Case Study/Applied, Quick-Fire). Each question: key points to hit, common mistake, difficulty (⭐/⭐⭐/⭐⭐⭐). Write `{base}/{slug}/interview-questions.md`.

If not applicable: note "Interview questions: not applicable." and proceed.

**→** "Interview questions complete. Moving to figure generation..."

---

## Stage 7: Figure Generation

**Read:** `skills/lecture-draft/draft-presentation.md` Step 5 (Figure Generation section)
**Virtualenv:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-plan/.venv`
**Fallback:** If `.venv` fails, use system `python3` (with `--break-system-packages` if needed).

From `lecture-notes.md` (use working memory), identify all tables, charts, diagrams, and equation visualizations. For each:
1. Generate with matplotlib (or plotly/networkx) at **150 dpi**
2. Save to `{base}/{slug}/figures/figure_NNN_{slug}.png`
3. Insert `![Figure N: description](figures/figure_NNN_slug.png)` + italicized caption into `lecture-notes.md`

**Minimum:** 3 figures (aim for 4–6).

**Figure rules (slide compatibility):**
- No baked-in titles: do NOT call `fig.suptitle()`, `ax.set_title()`. Use `ax.text(0.02, 0.96, 'Panel A: ...', transform=ax.transAxes)` for panel labels.
- Single-panel: aspect ratio 1.3–1.6 (e.g., `figsize=(6, 4.5)`)
- Two-panel: vertical stacking `subplots(2, 1)`, NOT horizontal; target `figsize=(5.5, 7.5)`
- Wide tables: portrait `figsize=(5.5, 6.0)` — never landscape for slide use
- Never exceed AR 1.7 for figures embedded in slides

**Output:** `{base}/{slug}/figures/*.png` + updated `lecture-notes.md`

**→** "Figures complete ({N} generated). Moving to snapshot..."

---

## Stage 8: Save Knowledge Snapshot

**Read:** `skills/lecture-snapshot/snapshot.md`

Extract from `intake.md`, `brainstorm.md`, `lecture-notes.md` (use working memory): theory coverage, notation, examples, companies, datasets, job contexts, forward/backward links.
Write `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/topic-{NN}-{course-code}-{slug}.md` + update `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/KNOWLEDGE.md`.
If knowledge-rag MCP connected: push via `add_document(..., category="lecture")`.

**Output:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/topic-{NN}-{course-code}-{slug}.md`

**→** "Snapshot saved. Moving to RevealJS slide deck..."

---

## Stage 9: RevealJS Slide Deck

**Read:** `~/.claude/skills/revealjs/SKILL.md`

**Step 1 — Design:** Analyze content tone (economics/academic), count `##` sections, plan layout variety (title+bullets, two-column, figure, discussion highlight).

**Step 2 — Scaffold:**
```bash
cd "{base}/{slug}"
node ~/.claude/skills/revealjs/scripts/create-presentation.js \
  --title "{topic_title}" \
  --output presentation.html \
  --structure {derived from section count}
```

**Step 3 — Fill from `lecture-notes.md` (working memory):**
- Each `##` section → slides; speaking notes → `<aside>`; discussion/poll prompts → accent slides
- Figures → `<img src="figures/figure_NNN_slug.png" style="max-height:55vh;">`
- Equations → MathJax (`\( \)` inline, `\[ \]` block)
- All text in semantic elements (`<p>`, `<li>`, `<h2>`–`<h4>`); font sizes in `pt`

**Step 4 — Overflow check:**
```bash
node ~/.claude/skills/revealjs/scripts/check-overflow.js "{base}/{slug}/presentation.html"
```
Fix any overflow before proceeding.

**Step 5 — Export + review:**
```bash
cd "{base}/{slug}"
npx decktape reveal "presentation.html?export" slides-revealjs.pdf \
  --screenshots --screenshots-directory screenshots-revealjs/ --size 1920x1080
```
Review every screenshot. Fix visual issues before finalizing.

**Step 6 — Export Canva-ready PNGs:**
```bash
python3 "/Users/openclaw/Resilio Sync/Documents/notebooklm-toolkit/pdf_to_slides_png.py" \
  "{base}/{slug}/slides-revealjs.pdf" \
  -o "{base}/{slug}/slides-png/" --dpi 300
```
This produces high-resolution PNGs (6000×3375px at 300 DPI) for Canva import. One PNG per slide, named `slide_001.png`, `slide_002.png`, etc.

**Output:** `presentation.html`, `styles.css`, `slides-revealjs.pdf`, `screenshots-revealjs/`, `slides-png/`

**→** "Slides complete ({N} slides, Canva PNGs exported). Starting NotebookLM Phase 1..."

---

## Stage 10: NotebookLM Phase 1 (auto-run — always execute)

Run immediately after RevealJS slides. Do NOT skip.

**Slide-deck rules (MANDATORY — applies to all NLM slide generation):**
1. **Style:** Pass as positional DESCRIPTION: `"Academic style, clean, white background, no lines or grid lines in background, Font: Open Sans."`
2. **Source scoping:** Always use `-s $SRC_ID` to scope to ONE transcript part. Never generate from the whole notebook.
3. **Note:** `--append` is NOT a valid CLI flag — style goes in the DESCRIPTION argument.

```bash
notebooklm generate slide-deck \
  "Academic style, clean, white background, no lines or grid lines in background, Font: Open Sans." \
  -s "$SRC_ID" --json -n "$NB"
```

**JSON parsing — always use Python, NOT jq:**
- Create notebook → `.notebook.id`
- Add source → `.source.id`
- Generate audio → `.task_id`

1. From `intake.md` extract `course_title`, `topic_number`, `topic_title`
2. `mkdir -p "{base}/{slug}/media"`
3. Create notebook:
   ```bash
   NB=$(notebooklm create "{course_title} — Topic {N}: {topic_title}" --json \
     | python3 -c "import sys,json; print(json.load(sys.stdin)['notebook']['id'])")
   ```
4. Upload notes + wait:
   ```bash
   SRC=$(notebooklm source add "{base}/{slug}/lecture-notes.md" --json -n $NB \
     | python3 -c "import sys,json; print(json.load(sys.stdin)['source']['id'])")
   notebooklm source wait $SRC -n $NB
   ```
5. **Auto-generate topic-specific audio prompt** from `lecture-notes.md` (in working memory):
   Extract from the notes:
   - Topic title (from `# {title}` header)
   - Core concept names (from `## 📚 Section N: {name}` headers)
   - Industry example companies (from `### Industry Application: {company}` headers)
   - Worked example summaries (from `### 🔢 Worked Example` first line)

   Construct the prompt:
   ```
   "Two hosts have an in-depth discussion about {topic_title}.
   Cover these key concepts: {concept_1}, {concept_2}, {concept_3}, {concept_4}.
   Walk through the worked examples with actual numbers, especially {worked_example_summary}.
   Discuss the {company_1} and {company_2} case studies in detail.
   Debate the tradeoffs and highlight what an economics student needs to understand
   for both exams and job interviews."
   ```

6. Trigger Deep Dive audio with the auto-generated prompt (do NOT wait):
   ```bash
   AUD=$(notebooklm generate audio \
     "{auto_generated_prompt}" \
     --format deep-dive --length long --json -n $NB \
     | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('task_id', d.get('artifact_id','')))")
   ```
7. Write `{base}/{slug}/nlm-state.json`:
   ```json
   { "notebook_id": "<NB>", "audio_artifact_id": "<AUD>", "slug": "<slug>", "topic_title": "<topic_title>", "course_title": "<course_title>", "phase_complete": 1 }
   ```
8. Launch auto-chain (**`disown` required** — without it the background process dies when Claude's shell exits):
   ```bash
   FOLDER="{base}/{slug}"
   LOG="$FOLDER/media/nlm_chain.log"
   nohup bash "/Users/openclaw/Resilio Sync/Documents/notebooklm-toolkit/nlm_auto_chain.sh" "$FOLDER" > "$LOG" 2>&1 &
   disown $!
   ```

Print:
```
🎙️ NLM Phase 1 complete + auto-chain launched.
   Audio generating (~20 min). Transcription, slides, 4K PNGs run automatically.
   Log: {base}/{slug}/media/nlm_chain.log
   macOS notification when all media is ready.
```

**Output:** `{base}/{slug}/nlm-state.json` (phase_complete: 1)

---

## Final Quality Gate (after Stage 10, before completion)

Run these automated checks before declaring the pipeline complete. Print results inline.

**File integrity (all must pass):**
- [ ] `lecture-notes.md` exists and is > 5000 chars
- [ ] `brainstorm.md` exists and is > 3000 chars
- [ ] `review-report.md` exists and is > 1000 chars
- [ ] `figures/` contains ≥ 3 PNG files
- [ ] `presentation.html` exists and is valid HTML (contains `<html` tag)
- [ ] `slides-revealjs.pdf` exists and > 0 bytes
- [ ] [if lab] `.ipynb` is valid JSON
- [ ] [if lab] `.html` companion exists

**Content spot-checks:**
- [ ] `lecture-notes.md` contains "Learning Objectives" section
- [ ] `lecture-notes.md` contains at least 2 "In-Class Discussion" sections (grep for `## 💬`)
- [ ] `lecture-notes.md` contains at least 3 "Class Poll" sections (grep for `## 📊`)
- [ ] All `<img src=` paths in `presentation.html` resolve to files in `figures/`

**Consistency check:**
- [ ] If `knowledge-context.md` exists, extract the "Do Not Reuse" company list and grep `lecture-notes.md` for any matches. Flag any found as ⚠️.

Print results: `✓` for pass, `⚠️` for warning (non-blocking), `❌` for fail (print but don't block).

---

## Pipeline Completion

Print summary after Final Quality Gate:

```
✅ Lecture Prep Complete — {topic_title} (Topic {N} of {Total})

Files: intake.md · knowledge-context.md · brainstorm.md · review-report.md
       lecture-notes.md · figures/*.png · presentation.html · slides-revealjs.pdf
       [interview-questions.md] · [lab.ipynb] · nlm-state.json
Knowledge: econ-lecture-knowledge/lectures/topic-{NN}-{course-code}-{slug}.md

Media pipeline auto-running in background → macOS notification when ready.
Manual fallbacks if needed: /nlm-p2 · /nlm-p3 · /nlm-p4
```

---

## Multimedia Export (manual fallbacks only)

Stage 10 runs NLM automatically. Use `/nlm-p2`, `/nlm-p3`, `/nlm-p4` only if the auto-chain fails.

```
/nlm-p2 {base}/{slug}/   ← download {slug}-podcast.m4a + Whisper transcription
/nlm-p3 {base}/{slug}/   ← upload 3 transcript parts + generate 3 slide decks
/nlm-p4 {base}/{slug}/   ← download PDFs + remove watermarks + export 4K PNGs
```

State carried in `nlm-state.json`. All commands are idempotent — safe to re-run.

---

## Key Rules (enforced at every stage)

1. **No examples older than 2024** (unless historically significant) — always web-search for current data.
2. **No vague claims** — every fact cites a named source (institution, study, report) with URL.
3. **Every equation interpreted** — never present math without plain-language explanation.
4. **Every industry example:** company + problem + method + quantified outcome.
5. **Time allocations realistic** — if content exceeds class time, cut, don't compress.
6. **Interactive elements mandatory** — minimum 2 discussion sets + 3 poll questions per lecture.
7. **Student engagement first** — examples from companies and events students actually know.
