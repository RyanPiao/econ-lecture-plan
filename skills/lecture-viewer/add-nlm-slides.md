# Add NLM Slides — Append NotebookLM PNGs to RevealJS Deck

## Purpose

After the NLM auto-chain completes (Stage 6 background), append the generated slide PNGs as bonus review slides to the existing RevealJS `presentation.html`. This lets the instructor present both their crafted slides AND the NLM-generated visual summaries in a single deck.

## Trigger

- `/add-nlm-slides [lecture-dir]` — standalone command after NLM chain finishes
- Can also be called manually anytime NLM PNGs are available

## Inputs

- `{base}/{slug}/presentation.html` — existing RevealJS deck
- `{base}/{slug}/media/slides_part{1,2,3}/page_*.png` — NLM-generated slide PNGs (4K resolution)

## Steps

### 1. Verify NLM PNGs exist

```bash
NLM_PNGS=$(find "{base}/{slug}/media" -path "*/slides_part*/page_*.png" | sort)
COUNT=$(echo "$NLM_PNGS" | wc -l)
```

If no PNGs found: check `nlm-state.json` for chain status. If chain is still running, print "NLM chain still running. Check `media/nlm_chain.log`." and exit.

### 2. Copy NLM PNGs to presentation directory

Copy to a dedicated subdirectory so relative paths work in the HTML:

```bash
mkdir -p "{base}/{slug}/nlm-slides"
cp {base}/{slug}/media/slides_part*/page_*.png "{base}/{slug}/nlm-slides/"
```

Rename for sequential numbering: `nlm_001.png`, `nlm_002.png`, etc.

### 3. Insert divider + image slides into presentation.html

Find the closing `</div>` of the last `<section>` in the RevealJS `.slides` container. Before the closing `</div>` of `.reveal .slides`, insert:

```html
<!-- NLM Review Slides (auto-appended) -->
<section id="nlm-divider" data-background-color="#2D2D2D">
  <h2 style="color: #FAFAF8;">NotebookLM Review Slides</h2>
  <p style="color: #A0A0A0; font-size: 18pt;">AI-generated visual summary for review</p>
</section>

<section id="nlm-001">
  <img src="nlm-slides/nlm_001.png" style="max-height: 85vh; max-width: 95vw; object-fit: contain;" alt="NLM review slide 1">
</section>

<section id="nlm-002">
  <img src="nlm-slides/nlm_002.png" style="max-height: 85vh; max-width: 95vw; object-fit: contain;" alt="NLM review slide 2">
</section>

<!-- ... repeat for all NLM PNGs ... -->
```

### 4. Update slide count

The viewer's `totalSlides` is dynamically read from RevealJS, so no manual update needed. The new slides will appear automatically in the viewer's overview mode and navigation.

### 5. Regenerate PDF (optional)

If the user wants an updated PDF with NLM slides included:

```bash
cd "{base}/{slug}"
npx decktape reveal "presentation.html?export" slides.pdf \
  --screenshots --screenshots-directory screenshots/ --size 1920x1080 --pause 3000
```

### 6. Print summary

```
✅ Added {N} NLM review slides to presentation.html
   NLM slides: nlm-slides/nlm_001.png ... nlm_{N:03d}.png
   Divider slide inserted before NLM section
   Total deck: {original + 1 divider + N NLM} slides

   To remove: delete the <!-- NLM Review Slides --> block from presentation.html
   To re-export PDF: npx decktape reveal "presentation.html?export" slides.pdf --pause 3000
```

## Notes

- NLM slides are image-only (no speaker notes, no transitions)
- They appear AFTER all instructor-crafted slides
- The divider slide makes it clear where instructor content ends and AI review begins
- To edit the deck after adding NLM slides: `node ~/.claude/skills/revealjs/scripts/edit-html.js presentation.html`
- NLM slides can be individually removed by deleting their `<section>` from the HTML
- Re-running `/add-nlm-slides` replaces any previously appended NLM slides (checks for existing `<!-- NLM Review Slides -->` marker)
