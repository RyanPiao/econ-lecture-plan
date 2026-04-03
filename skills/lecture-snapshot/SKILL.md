---
name: lecture-snapshot
description: Save a compact knowledge snapshot of a completed lecture to the course knowledge base. Run automatically at end of /lecture-prep. Can also run standalone with /save-snapshot. Checks for and prevents duplicate snapshots.
---

# Lecture Snapshot — Save to Knowledge Base

Routes:
- `/save-snapshot {output-folder}` → Read completed lecture outputs and save snapshot
- Called automatically by pipeline (Stage 8) after Figure Generation

## What this does

Reads the completed `intake.md`, `brainstorm.md`, and `lecture-notes.md` for a lecture,
extracts a compact knowledge snapshot, saves it to `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/`, and updates `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/KNOWLEDGE.md`.

**Read:** `skills/lecture-snapshot/snapshot.md`
