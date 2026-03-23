---
name: lecture-brainstorm
description: Generate a structured lecture brainstorm with fresh 2024–2026 examples, industry case studies, and interactive classroom elements. Always performs web search. Trigger: /brainstorm-lecture (or called automatically by /lecture-prep)
---

# Lecture Brainstorm

Routes:
- `/brainstorm-lecture` → Read `brainstorm.md`, generate full brainstorm from intake form, write to `output/{slug}/brainstorm.md`
- `/brainstorm-lecture --brief` → Produce condensed 1-page concept map only (no full speaking notes)

## Input
Reads `output/{slug}/intake.md` (or prompts for intake fields if not found).

## Output
`output/{slug}/brainstorm.md` using `templates/brainstorm-output.md`

All detailed methodology — including the mandatory web search protocol, source credibility hierarchy, and interactive element generation — in `brainstorm.md`.
