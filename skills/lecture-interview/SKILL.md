---
name: lecture-interview
description: Generate technical interview questions for data/econometrics/stat/ML lecture topics. Produces interview-questions.md with concept, implementation, assumptions, case study, and quick-fire question banks. Called automatically by /lecture-prep when course is data/econ/stat/ML. Trigger: /interview-questions
---

# Lecture Interview Questions

Routes:
- `/interview-questions {slug}` → Generate interview questions for an existing lecture folder
- Called automatically by pipeline (Stage 6) after Draft when course is data/econ/stat/ML

## What this does

Reads `lecture-notes.md` for a completed lecture and generates a `interview-questions.md` file containing the most important technical interview questions on the topic — the kind asked in phone screens and onsite rounds at data science, econ consulting, quant research, PM, and policy analyst roles.

**Read:** `skills/lecture-interview/interview-questions.md`

## When it applies

Triggered when `course_title` or `topic_title` contains ANY of these keywords (case-insensitive):
`econometrics`, `statistics`, `statistical`, `data`, `machine learning`, `ML`, `regression`, `classification`, `causal`, `inference`, `panel`, `time series`, `forecast`, `clustering`, `neural`, `NLP`, `analytics`, `quantitative`, `econ ML`

If not applicable: skip, note "Interview questions: not applicable for this topic type."
