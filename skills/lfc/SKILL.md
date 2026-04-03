---
name: lfc
description: Alias for /lecture-from-chapter. Converts textbook chapters into lecture materials — notes, slides, labs, figures, viewer app. 6-stage pipeline with Presentation Expert review. Trigger: /lfc
user_invocable:
  - /lfc [chapter-path] --course [code] — Convert textbook chapter to lecture (6-stage pipeline)
---

# /lfc — Lecture From Chapter

Read `chapter-to-lecture/pipeline.md` and run ALL 6 stages end-to-end without stopping. Do NOT ask the user what they want to do. Do NOT present options. Just run the pipeline.

## Execution Rules

1. **Read `~/.claude/skills/chapter-to-lecture/pipeline.md` immediately** — it contains all logic
2. **Run all 6 stages end-to-end** — do not stop between stages
3. **Do NOT ask what the user wants** — `/lfc` IS the instruction to execute the full pipeline
4. **Only ask if chapter path or course code is missing**
5. **Auto-derive everything else** from textbook frontmatter + course code mapping in `~/.claude/skills/chapter-to-lecture/intake-detect.md`

## Parameters

| Parameter | Required | Default | Example |
|-----------|----------|---------|---------|
| chapter path | Yes | — | `ch14`, `/path/to/ch14-labor-markets.md` |
| `--course` | Yes | — | `econ1116`, `econ3916` |
| `--duration` | No | `75` | `50`, `100` |
| `--type` | No | Auto from course | `"presentation + lab"` |

## What it produces

```
econ-lecture-material/{course_folder}/{slug}/
├── intake.md, chapter-extract.md, lecture-notes.md
├── figures/, presentation.html, slides.pdf, viewer/
├── sync-slides.sh, slide-manager.sh, extra-slides/
├── pipeline-state.json, nlm-state.json, media/
```

All stage logic in `~/.claude/skills/chapter-to-lecture/pipeline.md`.
