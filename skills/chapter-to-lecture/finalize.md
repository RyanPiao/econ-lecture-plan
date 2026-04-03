# Stage 6: Finalize — Snapshot + NotebookLM + Quality Gate

## Purpose

Complete the pipeline by saving a knowledge snapshot, running quality checks, and launching NotebookLM media generation. Composes existing logic from `lecture-snapshot/snapshot.md` and the NLM auto-chain.

---

## Step 1: Save Knowledge Snapshot

**Read:** `skills/lecture-snapshot/snapshot.md`
**Re-read:** `{base}/{slug}/lecture-notes.md` from disk (do NOT rely on working memory)

Extract from `intake.md`, `chapter-extract.md`, `lecture-notes.md`:
- Theory coverage and key concepts
- Notation and terminology used
- Examples and case studies (company, dataset, method)
- Job contexts framed (if any)
- Forward/backward links to other chapters
- Figures generated

Write to: `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/ch{NN}-{course-code}-{slug}.md`

YAML frontmatter:
```yaml
---
chapter_number: {N}
topic_title: "{title}"
course_code: {code}
course_category: {qualitative|quantitative}
source: "textbook-chapter"
companies: [list]
datasets: [list]
methodology: [list]
notation: {symbol: "meaning"}
forward_seeded: [list]
backward_referenced: [list]
---
```

Update `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/KNOWLEDGE.md` with new entry.

If knowledge-rag MCP connected: push via `add_document(..., category="lecture")`.

---

## Step 2: Quality Gate

Run automated checks. Print results inline.

**File integrity (all must pass):**
- [ ] `lecture-notes.md` exists and > 5000 chars
- [ ] `chapter-extract.md` exists and > 2000 chars
- [ ] `figures/` contains ≥ 3 PNG files
- [ ] `presentation.html` exists and contains `<html` tag
- [ ] `slides.pdf` exists and > 0 bytes
- [ ] `viewer/index.html` exists
- [ ] [if lab] `.ipynb` is valid JSON
- [ ] [if lab] `.html` companion exists

**Content spot-checks:**
- [ ] `lecture-notes.md` contains "Learning Objectives"
- [ ] At least 2 "In-Class Discussion" sections (grep `## 💬`)
- [ ] At least 3 "Class Poll" sections (grep `## 📊`)
- [ ] All `<img src=` paths in `presentation.html` resolve to files in `figures/`
- [ ] Retrieval practice section present (grep `## 🔁`)
- [ ] Exit ticket section present (grep `## 🎫`)
- [ ] Pipeline sentinel present (grep `<!-- pipeline-complete: stage-3 -->`)

**Consistency check:**
- [ ] If prior snapshots exist for this course, extract "Do Not Reuse" companies and check `lecture-notes.md`. Flag matches as ⚠️.

Print: `✓` pass, `⚠️` warning, `❌` fail

---

## Step 3: NotebookLM Phase 1 (auto-run)

**JSON parsing — always use Python, NOT jq.**

### Pre-check dependencies before launch
```bash
VENV="/Users/openclaw/Resilio Sync/Documents/econ-lecture-plan/.venv"
"$VENV/bin/python" -c "import fitz; import cv2" 2>/dev/null || echo "⚠️ NLM dependencies (pymupdf, opencv) not in venv. Auto-chain may fail at PDF→PNG step."
```

1. From `intake.md` extract `course_title`, `chapter_number`, `topic_title`
2. `mkdir -p "{base}/{slug}/media"`
3. Create notebook:
   ```bash
   NB=$(notebooklm create "{course_title} — Ch {N}: {topic_title}" --json \
     | python3 -c "import sys,json; print(json.load(sys.stdin)['notebook']['id'])")
   ```
4. Upload notes + wait:
   ```bash
   SRC=$(notebooklm source add "{base}/{slug}/lecture-notes.md" --json -n $NB \
     | python3 -c "import sys,json; print(json.load(sys.stdin)['source']['id'])")
   notebooklm source wait $SRC -n $NB
   ```
5. Auto-generate topic-specific audio prompt from `lecture-notes.md` (working memory):
   - Extract topic title from `# {title}` header
   - Extract concept names from `## 📚 Section N: {name}` headers
   - Extract company names from `### Industry Application: {company}` headers
   - Construct prompt:
   ```
   "Two hosts have an in-depth discussion about {topic_title}.
   Cover these key concepts: {concept_1}, {concept_2}, {concept_3}.
   Walk through the worked examples with actual numbers.
   Discuss the {company_1} and {company_2} case studies in detail.
   Debate the tradeoffs and highlight what an economics student needs to understand."
   ```
6. Trigger Deep Dive audio (do NOT wait):
   ```bash
   AUD=$(notebooklm generate audio \
     "{auto_generated_prompt}" \
     --format deep-dive --length long --json -n $NB \
     | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('task_id', d.get('artifact_id','')))")
   ```
7. Write `{base}/{slug}/nlm-state.json`:
   ```json
   { "notebook_id": "<NB>", "audio_artifact_id": "<AUD>", "slug": "<slug>", "topic_title": "<title>", "course_title": "<course>", "phase_complete": 1 }
   ```
8. Launch auto-chain (**`disown` required** + **PID tracking** + **failure notification**):
   ```bash
   FOLDER="{base}/{slug}"
   LOG="$FOLDER/media/nlm_chain.log"
   nohup bash -c '
     trap '\''osascript -e "display notification \"Check '"$LOG"'\" with title \"NLM Chain FAILED\" sound name \"Basso\"" 2>/dev/null'\'' ERR
     bash "/Users/openclaw/Resilio Sync/Documents/notebooklm-toolkit/nlm_auto_chain.sh" "'"$FOLDER"'"
   ' > "$LOG" 2>&1 &
   CHAIN_PID=$!
   disown $CHAIN_PID
   ```
   Store PID in state file:
   ```bash
   python3 -c "
   import json
   with open('$FOLDER/nlm-state.json') as f: d = json.load(f)
   d['chain_pid'] = $CHAIN_PID
   with open('$FOLDER/nlm-state.json', 'w') as f: json.dump(d, f, indent=2)
   "
   ```

### What the NLM auto-chain does (background, ~30-45 min total)

The `nlm_auto_chain.sh` script runs these phases automatically after launch:

1. **Phase 2 — Download podcast:** Wait for Deep Dive audio to finish → download `{slug}-podcast.m4a` → Whisper transcription → 3 transcript parts
2. **Phase 3 — Generate NLM slides:** Upload 3 transcript parts as sources → generate 3 slide decks (academic style, white background, Open Sans) → wait for completion
3. **Phase 4 — Download + post-process:**
   - Download 3 slide PDFs from NLM
   - **Remove watermarks** from PDFs (pymupdf)
   - **Export 4K PNGs** from each PDF (`pdf_to_slides_png.py --dpi 300` → 6000×3375px)
   - Output: `media/slides_part{1,2,3}/page_*.png`
4. **macOS notification** on completion (or failure notification via trap)

### After NLM chain finishes

Run `/add-nlm-slides` to append the 4K NLM PNGs as bonus review slides to `presentation.html`. Or use:
```bash
./slide-manager.sh add-png media/slides_part1/page_001.png --after 25
```
to cherry-pick specific NLM slides.

### Manual fallbacks if auto-chain fails

```
/nlm-p2 {base}/{slug}/   ← download podcast + Whisper transcription
/nlm-p3 {base}/{slug}/   ← upload transcripts + generate 3 slide decks
/nlm-p4 {base}/{slug}/   ← download PDFs + remove watermarks + export 4K PNGs
```

---

## Pipeline Completion

Print summary:

```
✅ Chapter-to-Lecture Complete — Ch {N}: {topic_title} ({course_code})

Source:  {chapter_path}
Output: {base}/{course_folder}/{slug}/
Files:  intake.md · chapter-extract.md · lecture-notes.md · figures/*.png
        presentation.html · viewer/ · slides.pdf
        {lab files if applicable}

Knowledge: econ-lecture-knowledge/lectures/ch{NN}-{course-code}-{slug}.md
Quality:   {pass_count}✓ {warn_count}⚠️ {fail_count}❌

Media pipeline auto-running → macOS notification when ready.
Manual fallbacks: /nlm-p2 · /nlm-p3 · /nlm-p4
```

Update `pipeline-state.json`:
```json
{
  "pipeline_version": 2,
  "pipeline_type": "chapter-to-lecture",
  "last_completed_stage": 6,
  "stages": { "1": {"status": "completed"}, ..., "6": {"status": "completed"} }
}
```
