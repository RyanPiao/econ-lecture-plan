---
name: lecture-brainstorm
description: Generate a structured lecture brainstorm with fresh 2024–2026 examples, industry case studies, and interactive classroom elements. Always performs web search. Trigger: /brainstorm-lecture (or called automatically by /lecture-prep)
---

# Lecture Brainstorm

Routes:
- `/brainstorm-lecture` → Read `brainstorm.md`, generate full brainstorm from intake form, write to `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/brainstorm.md`
- `/brainstorm-lecture --brief` → Produce condensed 1-page concept map only (no full speaking notes)

## Input
Reads `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/intake.md` (or prompts for intake fields if not found).

## Prerequisite
If prior lecture snapshots exist for this course in `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/`, you **MUST** run `/knowledge-check` first to produce `knowledge-context.md`. The brainstorm will refuse to proceed without it. Only skippable for the very first lecture of a course (no snapshots exist).

## Output
`/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/brainstorm.md` using `templates/brainstorm-output.md`

All detailed methodology — including the mandatory web search protocol, source credibility hierarchy, and interactive element generation — in `brainstorm.md`.
