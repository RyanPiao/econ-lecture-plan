---
name: lecture-viewer
description: Self-contained lecture viewer web app wrapping RevealJS. Presenter mode, dual-monitor sync, timer with pace indicator, laser pointer, 3 WCAG-compliant themes. Slide manager CLI for safe editing. Auto-sync to GitHub Pages. Replaces Canva.
user_invocable:
  - /build-viewer [lecture-dir] — Generate viewer for existing RevealJS presentation
  - /add-nlm-slides [lecture-dir] — Append NotebookLM slide PNGs as review slides
  - /deploy-lecture [lecture-dir] — Push lecture to GitHub Pages repo
  - /deploy-course [course-code] — Push all lectures for a course
---

# Lecture Viewer

Routes:
- `/build-viewer [lecture-dir]` → Generate viewer for an existing RevealJS presentation
- `/add-nlm-slides [lecture-dir]` → Append NotebookLM slide PNGs as bonus review slides
- `/deploy-lecture [lecture-dir]` → Push lecture to GitHub Pages repo
- `/deploy-course [course-code]` → Push all lectures for a course
- Called automatically by `/lfc` Stage 5

## Viewer Features

| Feature | Key | Description |
|---------|-----|-------------|
| Presenter mode | P | 420px panel: speaker notes + next preview + timer + pace |
| Student mode | U | Clean full-width slides |
| Overview mode | O | Thumbnail grid, click to navigate |
| Dual monitor | W | Opens synced student window (BroadcastChannel + direct Reveal) |
| Timer | T | Countdown, pace indicator, pulse at 75%/90%, sessionStorage |
| Laser pointer | L | Red dot follows cursor on slide area |
| Black screen | B | Blanks projection for eye contact |
| Jump to slide | G+num | Press G then type slide number |
| Theme toggle | btn | White Academia → Dark → High Contrast (WCAG AA) |
| Notes font | A+/A- | Adjustable speaker notes size |
| Fullscreen | F | Browser fullscreen |
| Help | ? | Keyboard shortcuts overlay |

## Slide Manager (safe editing without raw HTML)

```bash
./slide-manager.sh list                                  # show all slides
./slide-manager.sh add-png chart.png --after 12          # insert PNG as slide
./slide-manager.sh add content-figure --title "MRP" --image figures/mrp.png
./slide-manager.sh add full-figure --image lorenz.png    # centered image slide
./slide-manager.sh add two-column --title "Before vs After"
./slide-manager.sh add section-divider --title "Part 2"
./slide-manager.sh edit 8                                # edit slide 8 in $EDITOR
./slide-manager.sh remove 14                             # remove (10s timeout confirm)
./slide-manager.sh show 5                                # print slide HTML
```

Uses BeautifulSoup — validates HTML, auto-backup, warns on unreplaced placeholders, prettify output.

**4 Slide Templates:** content-figure, full-figure, two-column, section-divider

## Auto-Sync (live GitHub Pages updates)

```bash
./auto-sync.sh start     # fswatch + git auto-push (2s debounce)
./auto-sync.sh status    # check if running
./auto-sync.sh stop      # pkill -P + kill (macOS compatible)
```

## NLM Slide Append

`/add-nlm-slides` — copies NLM PNGs from `media/slides_part*/` to `nlm-slides/`, inserts as image-only `<section>` elements with divider slide. Re-running replaces previous NLM slides.

## GitHub Pages Deployment

One repo per course, one directory per chapter. Students access:
`https://{username}.github.io/econ1116-lectures/ch14/viewer/index.html`

Edit locally → auto-sync pushes → live in 1-3 min.

## Launch

- **Local:** `./viewer/serve.sh` → http://localhost:8080/viewer/index.html
- **Shared:** GitHub Pages URL (HTTPS, viewer works natively)
- **Fallback:** Direct open shows connection banner if iframe fails on file://

## Technical Details

- iframe loads src from CONFIG.presentationPath (not hardcoded)
- Timer: stale-timestamp guard discards saved state > 2× class duration
- Themes: darkened accents for WCAG AA (#4A7A96 blue, high-contrast uses gold #FFD700)
- Side panel: 420px on 1440px+, 340px on 1200px, 280px on 900px, hidden on 640px

## Output

```
{lecture-dir}/viewer/
├── index.html    Viewer app (3 modes, timer, laser, dual-monitor)
├── viewer.css    3 themes (WCAG AA compliant)
├── viewer.js     RevealJS API, timer, navigation, sync
└── serve.sh      Local server launcher
```

All logic in `build-viewer.md`, `add-nlm-slides.md`, `deploy-github-pages.md`.
Scripts in `scripts/` (slide-manager.sh, slide-manager.py, auto-sync.sh).
Templates in `slide-templates/` (4 HTML fragments).
