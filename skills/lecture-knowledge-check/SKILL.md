---
name: lecture-knowledge-check
description: Check the course knowledge base before brainstorming a new lecture. Uses knowledge-rag MCP (semantic search) if connected, falls back to file scan if not. Produces a Consistency Context Report of example constraints, notation, and forward seeds. Also supports /lecture-kb for ad-hoc knowledge base queries. Called automatically at the start of /lecture-prep Stage 2.
---

# Lecture Knowledge Check

Routes:
- `/knowledge-check {course-code} {topic-number}` → Run standalone check, print context report
- `/lecture-kb {natural-language query}` → Ad-hoc query of the lecture knowledge base
- Called automatically by pipeline before Stage 2 (Brainstorm)

## What this does

Queries the lecture knowledge base (via knowledge-rag MCP if connected, file scan if not) and produces a **Consistency Context Report** fed directly into the brainstorm as hard constraints.

**Read:** `skills/lecture-knowledge-check/knowledge-check.md`

---

## /lecture-kb — Ad-hoc knowledge base queries

Run at any time to query what you've already taught across the semester.

**How it works:**
1. Call `search_knowledge({query}, category="lecture", max_results=10)` via knowledge-rag MCP
2. Synthesize results into a direct answer with source topic references
3. If MCP unavailable: grep `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/` YAML frontmatter for the answer

**Example queries:**
- `/lecture-kb what Boston examples have I used in econ5200?`
- `/lecture-kb what notation is established for regression in this course?`
- `/lecture-kb have I used the Boston Fed as a source yet?`
- `/lecture-kb what topics forward-seeded DiD?`
- `/lecture-kb what companies have appeared more than twice?`
- `/lecture-kb what job contexts have I covered least?`

**Output format:**
```
## Knowledge Base: {query}

{Direct answer synthesized from retrieved chunks}

**Sources:**
- Topic {N}: {Title} — "{relevant excerpt}"
- Topic {N}: {Title} — "{relevant excerpt}"

**Gaps:** {anything the KB doesn't have a clear answer for}
```
