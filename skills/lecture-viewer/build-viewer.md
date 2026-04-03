# Build Viewer — Assembly Logic

## Purpose

Generate the viewer web app files for a lecture directory that already has a RevealJS `presentation.html`.

---

## Inputs

- Lecture directory path (e.g., `{base}/{slug}/`)
- `intake.md` — for lecture title and class duration
- `presentation.html` — the RevealJS deck to wrap

---

## Steps

### 1. Validate prerequisites

- Confirm `presentation.html` exists in the lecture directory
- Confirm `styles.css` exists
- Read `intake.md` to extract: `topic_title`, `course_code`, `class_duration`

### 2. Create viewer directory

```bash
mkdir -p "{base}/{slug}/viewer"
```

### 3. Generate viewer files

Copy templates from `skills/lecture-viewer/templates/` and inject lecture-specific config:

**viewer/index.html** — from `templates/viewer-template.html`
- Replace `{{LECTURE_TITLE}}` with topic title
- Replace `{{COURSE_CODE}}` with course code

**viewer/viewer.js** — from `templates/viewer.js`
- Replace `{{PRESENTATION_PATH}}` with `../presentation.html`
- Replace `{{CLASS_DURATION}}` with duration in minutes
- Replace `{{LECTURE_TITLE}}` with topic title

**viewer/viewer.css** — copy `templates/viewer.css` as-is (no modifications needed)

**viewer/serve.sh** — copy `templates/serve.sh` as-is (make executable)

### 4. Post-build validation

```bash
# Verify no unreplaced template tokens
grep -r '{{' "{base}/{slug}/viewer/" && echo "ERROR: unreplaced template tokens found" || echo "OK: all tokens replaced"
```

### 5. Print launch instructions

```
Viewer ready at: {base}/{slug}/viewer/

Launch options:
  1. Local server (recommended): cd "{base}/{slug}" && ./viewer/serve.sh
  2. Direct open (limited features): open "{base}/{slug}/viewer/index.html"

Keyboard: Right/Space (next), Left (prev), P/U/O (modes), W (dual monitor), T (timer), L (laser), B (black), ? (help)
```

---

## Output

```
{base}/{slug}/viewer/
├── index.html    Main viewer app
├── viewer.css    Styles (3 themes: light, dark, high-contrast)
├── viewer.js     RevealJS integration + timer + laser + dual-monitor sync
└── serve.sh      Local server launcher (python3 -m http.server)
```

**Primary launch method:** `./viewer/serve.sh` (opens at http://localhost:8080/viewer/index.html)
**Fallback:** Direct open (viewer shows connection banner with instructions if iframe fails)
