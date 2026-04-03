# Deploy to GitHub Pages

## Purpose

Deploy lecture presentations to GitHub Pages so students can access slides via URL. Each course gets a repo, each chapter gets a directory. The instructor edits locally, pushes, and GitHub auto-deploys.

## Trigger

- `/deploy-lecture [lecture-dir]` — push a single lecture to GitHub Pages
- `/deploy-course [course-code]` — push all lectures for a course

## Repo Structure

One GitHub repo per course:

```
econ1116-lectures/              ← GitHub repo
├── index.html                  Course landing page (links to all chapters)
├── ch01/                       Chapter 1 lecture
│   ├── presentation.html
│   ├── styles.css
│   ├── figures/
│   ├── nlm-slides/             (if NLM slides appended)
│   └── viewer/
│       ├── index.html
│       ├── viewer.js
│       ├── viewer.css
│       └── serve.sh
├── ch02/
│   └── ...
└── .github/
    └── workflows/
        └── pages.yml           GitHub Pages deployment (auto on push to main)
```

**Student URL:** `https://{username}.github.io/econ1116-lectures/ch14/viewer/index.html`
**Direct slides:** `https://{username}.github.io/econ1116-lectures/ch14/presentation.html`

## Setup (one-time per course)

### 1. Create the repo

```bash
COURSE="econ1116-lectures"
gh repo create "$COURSE" --public --clone
cd "$COURSE"
```

### 2. Add GitHub Pages workflow

```bash
mkdir -p .github/workflows
cat > .github/workflows/pages.yml << 'EOF'
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - id: deployment
        uses: actions/deploy-pages@v4
EOF
```

### 3. Enable Pages in repo settings

```bash
gh api repos/{owner}/$COURSE/pages -X POST -f source.branch=main -f source.path="/"
```

### 4. Create course landing page

```bash
cat > index.html << 'LANDING'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ECON 1116 — Lecture Slides</title>
  <style>
    body { font-family: 'Inter', system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #2D2D2D; }
    h1 { font-size: 24px; margin-bottom: 8px; }
    .subtitle { color: #666; margin-bottom: 32px; }
    .chapter { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .chapter a { color: #4A7A96; text-decoration: none; font-weight: 500; }
    .chapter a:hover { text-decoration: underline; }
    .links { display: flex; gap: 12px; font-size: 14px; }
    .links a { color: #666; }
  </style>
</head>
<body>
  <h1>ECON 1116 — Principles of Microeconomics</h1>
  <p class="subtitle">Lecture Slides — Northeastern University</p>
  <div id="chapters">
    <!-- Chapters auto-populated by deploy script -->
  </div>
</body>
</html>
LANDING
```

### 5. Initial commit

```bash
git add -A && git commit -m "Initialize course lecture repo" && git push
```

## Per-Lecture Deploy

### 1. Copy lecture files to repo

```bash
COURSE_FOLDER="econ1116-principles-micro"
SLUG="ch14-econ1116-labor-markets-human-capital-inequality"
SRC="/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/$COURSE_FOLDER/$SLUG"
DEST="/path/to/econ1116-lectures/ch14"

mkdir -p "$DEST"
# Copy only what students need (not pipeline artifacts)
cp "$SRC/presentation.html" "$DEST/"
cp "$SRC/styles.css" "$DEST/"
cp -r "$SRC/figures" "$DEST/"
cp -r "$SRC/viewer" "$DEST/"
cp "$SRC/slides.pdf" "$DEST/" 2>/dev/null  # PDF for download
[ -d "$SRC/nlm-slides" ] && cp -r "$SRC/nlm-slides" "$DEST/"
```

**Do NOT copy:** `intake.md`, `chapter-extract.md`, `lecture-notes.md` (instructor-only), `pipeline-state.json`, `nlm-state.json`, `media/` (large audio files), `solutions/`

### 2. Update landing page

Add a chapter entry to `index.html`:
```html
<div class="chapter">
  <a href="ch14/viewer/index.html">Ch 14: Labor Markets, Human Capital, and Inequality</a>
  <div class="links">
    <a href="ch14/presentation.html">Slides</a>
    <a href="ch14/slides.pdf">PDF</a>
  </div>
</div>
```

### 3. Push

```bash
cd /path/to/econ1116-lectures
git add -A
git commit -m "Add Ch 14: Labor Markets"
git push
```

GitHub Pages auto-deploys within 1-2 minutes. Students access at:
`https://{username}.github.io/econ1116-lectures/ch14/viewer/index.html`

## Editing After Deploy

### Edit locally
```bash
# Use RevealJS inline editor
node ~/.claude/skills/revealjs/scripts/edit-html.js /path/to/econ1116-lectures/ch14/presentation.html

# Or edit HTML directly in any editor
code /path/to/econ1116-lectures/ch14/presentation.html
```

### Push changes
```bash
cd /path/to/econ1116-lectures
git add -A && git commit -m "Update Ch 14 slides" && git push
```

Changes go live in 1-2 minutes.

## Notes

- **Viewer works on GitHub Pages** — no file:// issues since it's served over HTTPS
- **No serve.sh needed for students** — GitHub Pages handles serving
- **serve.sh still useful for instructor** — local preview before pushing
- **Large files:** If NLM audio (.m4a) is too large for git, use Git LFS or host audio separately
- **Private repos:** GitHub Pages requires Pro plan for private repos. Use public repos for lecture slides (they contain no sensitive data).
