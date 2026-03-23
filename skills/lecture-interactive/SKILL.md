---
name: lecture-interactive
description: Generate or enhance in-class discussion questions, class polls (Mentimeter/iClicker), and discussion facilitation guides for economics lectures. Trigger: /class-discussion, /class-poll, /discussion-guide
---

# Lecture Interactive Elements

Routes:
- `/class-discussion [topic]` → Read `interactive.md`, generate tiered discussion questions (Bloom's Levels 2/4/6) for a given concept or lecture. Write to `output/{slug}/discussions.md` or print inline.
- `/class-poll [topic]` → Generate Mentimeter/iClicker-ready poll questions with 4 options, answer key, and reveal scripts. Write to `output/{slug}/polls.md` or print inline.
- `/discussion-guide [lecture-notes-path]` → Read an existing lecture notes file and generate a complete facilitation guide covering all discussion blocks and polls. Write to `output/{slug}/discussion-guide.md`.
- `/class-discussion --enhance [lecture-notes-path]` → Read existing lecture notes and improve or add discussion questions to every concept section.

## Input
- `/class-discussion` and `/class-poll`: topic name or description provided inline
- `/discussion-guide` and `--enhance`: path to an existing `lecture-notes.md` file

## Output
- `output/{slug}/discussions.md` — all discussion questions with facilitation notes
- `output/{slug}/polls.md` — all poll questions in Mentimeter/iClicker format
- `output/{slug}/discussion-guide.md` — complete facilitation guide

## Key rules
- All poll questions must have exactly 4 options (A/B/C/D)
- Discussion questions must span Bloom's Levels 2, 4, and 6 for each concept
- All examples and data references must be 2024 or later
- Facilitation notes must be specific (actual sentences, not vague prompts)

All detailed methodology in `interactive.md`.
