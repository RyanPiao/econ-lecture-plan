# Chapter-to-Lecture Pipeline — End-to-End Logic

## Purpose

Run all 6 stages as a single, uninterrupted workflow. Each stage reads the output of the previous stage. Do not pause between stages unless a required input is missing.

**Token efficiency:** Re-read `lecture-notes.md` from disk at each stage that needs it (Stages 4, 5, 6). Do NOT rely on working memory across stages — context compression may silently drop content. The real token savings come from reading skill files selectively (see below).

**Skill file reads:** For skill files exceeding ~100 lines, read only the section matching current parameters (e.g., skip lab instructions if class type is presentation-only).

**State tracking:** After each stage completes, update `{base}/{slug}/pipeline-state.json`. Use three statuses: `pending`, `in_progress`, `completed`. Write `in_progress` at stage entry, `completed` at stage exit. On resume, treat `in_progress` as "restart this stage."

**Concurrency lock:** Before starting, check for `{base}/{slug}/.pipeline-lock`. If it exists and the PID inside is alive, abort with: "Another pipeline run is active (PID {N}). Wait or remove .pipeline-lock." Otherwise, write your PID to the lock file. Remove the lock file when the pipeline finishes or fails.

---

## Pre-Flight Check

1. Was a chapter path provided? If not, ask for it.
2. Was a course code provided? If not, ask for it. (Only 2 required inputs — everything else is auto-derived)
3. Resolve `{course_folder}` from the course code mapping in `intake-detect.md` (e.g., `econ1116` → `econ1116-principles-micro`)
4. `{base}` = `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{course_folder}` — create if not exists
5. All `{base}/{slug}/` references throughout the pipeline use this course-nested path

**Resume check:** If `{base}/{slug}/pipeline-state.json` exists with `pipeline_type: "chapter-to-lecture"`, scan stages:
- Any stage marked `in_progress` → restart from that stage (partial completion detected)
- All stages `completed` up to N → resume from stage N+1
- Before skipping any `completed` stage, verify its output file exists on disk. If missing, re-run from that stage.
- Print: `"⏩ Resuming chapter-to-lecture from Stage {N}..."`

If no state file exists:
- If `intake.md` exists AND `chapter-extract.md` exists: skip to Stage 3
- If `intake.md` exists but NO `chapter-extract.md`: skip to Stage 2
- Otherwise: fresh start at Stage 1

**Initialize state file:**
```json
{
  "pipeline_version": 2,
  "pipeline_type": "chapter-to-lecture",
  "slug": "{slug}",
  "course_folder": "{course_folder}",
  "chapter_number": {N},
  "chapter_source": "{chapter_path}",
  "course_category": "{detected_category}",
  "last_completed_stage": 0,
  "stages": {
    "1": {"status": "pending", "output": "intake.md"},
    "2": {"status": "pending", "output": "chapter-extract.md"},
    "3": {"status": "pending", "output": "lecture-notes.md"},
    "4": {"status": "pending", "output": "figures/"},
    "5": {"status": "pending", "output": "viewer/"},
    "6": {"status": "pending", "output": "nlm-state.json"}
  }
}
```

**Stage entry/exit protocol:** At the start of each stage:
1. Write `"status": "in_progress"` for that stage in `pipeline-state.json`
2. Execute the stage
3. On success: write `"status": "completed"` and update `last_completed_stage`
4. For Stage 3: append sentinel `<!-- pipeline-complete: stage-3 -->` at the end of `lecture-notes.md`. On resume, check for this sentinel before skipping.

---

## Stage 1: Intake + Detect

**Read:** `skills/chapter-to-lecture/intake-detect.md`
**Template:** `skills/chapter-to-lecture/templates/intake-form.md`

Collect: chapter path, course code, class duration (optional, default 75 min).
**Everything else is auto-derived** from textbook frontmatter and course code mapping:
- chapter_number, topic_title → from YAML frontmatter
- audience_level, class_type → from course code mapping
- builds_on, recurring_threads → from frontmatter

Resolve chapter path. Detect course category (qualitative vs quantitative) and sub-category.
Generate slug: `ch{NN:02d}-{course-code}-{kebab-title}`

**Output:** `{base}/{slug}/intake.md`

**→** Update state (stage 1 → completed). "Intake complete. Moving to extract + adapt..."

---

## Stage 2: Extract + Adapt + Presentation Expert Review

**Read:** `skills/chapter-to-lecture/extract-adapt.md`
**Read:** The textbook chapter file (full read)
**Scan:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/` for deconfliction

1. Parse the chapter — extract all teachable elements (concepts, examples, equations, activities, misconceptions)
2. Plan the lecture — time budget, example selection, interactive element anchors
3. **Presentation Expert Review** — evaluate the plan for narrative arc, pacing, visual flow, audience engagement, and instructor confidence. Incorporate must-fix and should-fix recommendations.
4. Knowledge deconfliction — scan prior snapshots for companies/datasets to avoid
5. Write the chapter extract

**Output:** `{base}/{slug}/chapter-extract.md`

**→** Update state (stage 2 → completed). "Extract + presentation review complete. Moving to lecture generation..."

---

## Stage 3: Generate Lecture Notes

**Read:** `skills/chapter-to-lecture/generate-lecture.md`
**Read also (if lab):** `skills/lecture-draft/draft-lab.md`, `skills/lecture-draft/draft-lab-html.md`

Transform chapter extract into textbook-quality lecture notes. Generate interactive elements (discussions, polls, debriefs, decision scenarios). If class type includes lab and course is quantitative: generate Jupyter lab + HTML companion + solutions notebook.

**Output:**
- `{base}/{slug}/lecture-notes.md` ← **keep in working memory for Stages 4-6**
- `{base}/{slug}/lab_*.ipynb` (if applicable)
- `{base}/{slug}/lab_*.html` (if applicable)
- `{base}/{slug}/solutions/lab_*_solutions.ipynb` (if applicable)

**→** Update state (stage 3 → completed). "Lecture draft complete. Moving to figures..."

---

## Stage 4: Generate Figures

**Read:** `skills/lecture-draft/draft-presentation.md` (Step 5 — Figure Generation section only)
**Re-read:** `{base}/{slug}/lecture-notes.md` from disk (do NOT rely on working memory)
**Virtualenv:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-plan/.venv`
**Fallback:** System `python3`

From `lecture-notes.md`, identify all tables, charts, diagrams, equation visualizations.

**Check for reusable textbook figures:**
- Scan `ebook/public/images/chapters/ch{NN}/` for existing images
- If a figure matches (correct subject, white background, aspect ratio 1.3-1.6): reuse it (copy to `figures/`)
- Otherwise: generate new with matplotlib/plotly/networkx at 150 dpi

**Batch execution (prevents one failure from blocking all):**
1. Write ALL figure scripts to `{base}/{slug}/figures/` first
2. Execute in batch, capturing individual success/failure:
   ```bash
   for script in "{base}/{slug}/figures/"*.py; do
     "$VENV/bin/python" "$script" 2>"${script%.py}.err" && echo "OK: $script" || echo "FAILED: $script"
   done
   ```
3. If 2+ figures succeed (of 3 minimum), continue. Quality gate in Stage 6 will flag the deficit.
4. Track in state: `"figures_generated": N, "figures_failed": M`

For each successful figure:
- Save to `{base}/{slug}/figures/figure_NNN_{slug}.png`
- Insert `![Figure N: description](figures/figure_NNN_slug.png)` into `lecture-notes.md`
- **Alt text required:** `![MRP curve showing diminishing returns — each additional worker adds less revenue](figures/figure_001_mrp.png)`

**Figure rules:**
- No baked-in titles
- Single-panel: aspect ratio 1.3-1.6 (e.g., `figsize=(6, 4.5)`)
- Two-panel: vertical stacking, `figsize=(5.5, 7.5)`
- Never exceed AR 1.7

**Output:** `{base}/{slug}/figures/*.png` + updated `lecture-notes.md`

**→** Update state (stage 4 → completed). "Figures complete ({N} generated, {M} failed). Moving to slides..."

---

## Stage 5: Build Slides + Viewer

### Step 5a: RevealJS Slide Deck

**Read:** `~/.claude/skills/revealjs/SKILL.md`
**Re-read:** `{base}/{slug}/lecture-notes.md` from disk

**Figure reference validation:** Before generating slides, scan `lecture-notes.md` for all `![Figure` references. Verify each referenced PNG exists in `figures/`. If missing, omit the `<img>` tag from the slide (never produce broken image references).

1. Analyze content from `lecture-notes.md`
2. Scaffold:
   ```bash
   cd "{base}/{slug}"
   node ~/.claude/skills/revealjs/scripts/create-presentation.js \
     --title "{topic_title}" \
     --output presentation.html \
     --structure {derived from section count}
   ```
3. Fill slides: each `##` section → slides; speaking notes → `<aside>`; figures → `<img>`; equations → MathJax
4. Overflow check:
   ```bash
   node ~/.claude/skills/revealjs/scripts/check-overflow.js "{base}/{slug}/presentation.html"
   ```
5. Export PDF + screenshots (with MathJax wait):
   ```bash
   cd "{base}/{slug}"
   npx decktape reveal "presentation.html?export" slides.pdf \
     --screenshots --screenshots-directory screenshots/ --size 1920x1080 --pause 3000
   ```

### Step 5b: Lecture Viewer

**Read:** `skills/lecture-viewer/build-viewer.md`

1. Create `{base}/{slug}/viewer/` directory
2. Copy viewer template files from `skills/lecture-viewer/templates/`
3. Inject lecture-specific config into `viewer.js`:
   - `presentationPath`: relative path to `../presentation.html`
   - `lectureTitle`: from intake
   - `classDuration`: from intake (for timer)
   - `slideCount`: from DeckTape screenshot count
4. Verify `viewer/index.html` loads correctly

**Output:** `presentation.html`, `styles.css`, `slides.pdf`, `screenshots/`, `viewer/`

**→** Update state (stage 5 → completed). "Slides + viewer complete ({N} slides). Moving to finalize..."

---

## Stage 6: Finalize

**Read:** `skills/chapter-to-lecture/finalize.md`

1. Save knowledge snapshot
2. Run quality gate
3. Launch NotebookLM Phase 1 + auto-chain

**Output:** Knowledge snapshot + `nlm-state.json` + quality report

**→** Update state (stage 6 → completed). Print completion summary.

---

## Pipeline Cleanup

**On completion (success) or failure at any stage:**
1. Remove `{base}/{slug}/.pipeline-lock` — always, even on error
2. Update `pipeline-state.json` with final statuses (failed stage stays `in_progress`)

**If the pipeline crashes unexpectedly** (e.g., Claude session ends), the stale lock file will have a dead PID. The pre-flight check detects this: if the PID in `.pipeline-lock` is not alive, the lock is removed and the pipeline proceeds.

---

## Key Rules (enforced at every stage)

1. **Textbook is the source** — do not web-search for new content. The chapter provides everything.
2. **Every equation interpreted** — never present math without plain-language explanation.
3. **Every example complete** — company/context + problem + method + outcome.
4. **Time allocations realistic** — if content exceeds class time, cut cleanly.
5. **Interactive elements duration-scaled** — `floor(content_minutes / 10)` interactions, min 3. At least 1/3 discussions, 1/3 polls.
6. **No pausing between stages** — run end-to-end. Only stop if a required input is missing.
7. **Re-read from disk** — always re-read `lecture-notes.md` from disk at Stages 4, 5, 6. Do NOT rely on working memory across stages.
8. **Alt text for all figures** — every `![Figure]()` must have descriptive alt text.
9. **Assessment alignment** — every learning objective must have a corresponding assessment moment.
10. **Lock file discipline** — acquire at start, release at end. Never run two pipelines on the same slug.
