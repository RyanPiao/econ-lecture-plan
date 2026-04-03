---
name: lecture-review
description: 3-persona peer review of lecture brainstorm. Reviewers: Pedagogy Expert, Domain Economist, Industry Practitioner. Produces actionable feedback and a revised brainstorm. Trigger: /review-lecture (or called automatically by /lecture-prep)
---

# Lecture Review

Routes:
- `/review-lecture` → Read `peer-review.md`, run all 3 reviewers, write report to `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/review-report.md`, revise brainstorm in place
- `/review-lecture --quick` → Run reviews but skip the brainstorm revision step; report only

## Input
Reads `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/brainstorm.md` and `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/intake.md`.

## Output
- `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/review-report.md` — structured feedback from all 3 reviewers + synthesis
- Revised `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/brainstorm.md` — incorporating all `must-fix` and `should-fix` items

All detailed reviewer logic, checklists, and synthesis methodology in `peer-review.md`.
