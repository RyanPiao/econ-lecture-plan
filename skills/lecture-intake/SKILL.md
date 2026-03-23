---
name: lecture-intake
description: Collect structured inputs for lecture preparation — course title, topic, audience level, class type, and supporting materials. Trigger: /new-lecture (or called automatically by /lecture-prep)
---

# Lecture Intake

Routes:
- `/new-lecture` → Read `intake.md`, collect all required fields, write structured intake form to `output/{slug}/intake.md`

## Required inputs
Collect all of the following (prompt for anything missing):

1. **Course Title** — e.g., "ECON 5200: Applied Data Analytics in Economics"
2. **Topic Title** — e.g., "Ridge and Lasso Regression"
3. **Topic Number / Total** — e.g., "7 / 15"
4. **Class Length** — e.g., "75 minutes"
5. **Class Type** — `presentation` | `lab` | `presentation + lab`
6. **Target Audience Level** — `intro undergrad` | `advanced undergrad` | `masters`
7. **Prerequisites Covered** — optional but improves output quality
8. **Supporting Materials** — uploaded documents, textbook chapters, slides (optional)

## Output
`output/{course-slug}-topic-{N}-{slug}/intake.md` using `templates/intake-form.md`

All detailed methodology in `intake.md`.
