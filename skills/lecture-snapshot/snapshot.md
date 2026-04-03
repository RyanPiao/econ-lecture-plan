# Lecture Snapshot — Save Methodology

## Purpose

After each lecture is drafted, extract a compact record of what was covered and save it to the course knowledge base. This record will be loaded in future lectures to prevent example overlap, maintain notation consistency, and enable cross-topic coherence.

---

## Step 1: Locate completed lecture outputs

Read from `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/`:
- `intake.md` — topic metadata
- `brainstorm.md` — examples, companies, datasets, forward/backward links
- `lecture-notes.md` — notation, poll questions, discussion prompts

Extract the following fields:
- `topic_number`, `topic_title`, `course_code`, `course_title`
- `audience_level`, `class_type`, `date_prepared` (today's date)

---

## Step 2: Extract snapshot fields

Scan the lecture materials and extract:

**Theory Coverage** — What concepts, theorems, or derivations were taught? List as bullets.

**Notation Used** — What symbols were introduced or used? List each as `symbol → meaning`. This is critical: if β was used for OLS coefficient here, all future topics must use the same symbol.

**Examples Used** — For each example, record:
- Type: `[industry]`, `[academic]`, `[local-boston]`, `[dataset]`, `[policy]`, `[simulation]`
- Name/source
- One-sentence description of how it was used

**Companies and Organizations Named** — List all named companies, agencies, or institutions. These should be rested before reuse in adjacent topics.

**Datasets Referenced** — Name + URL. Note whether it was used in a lab or just cited.

**Job Contexts Framed** — Which career paths were examples tied to? (consulting, PM, policy, finance, data analytics, etc.)

**Concepts Backward-Referenced** — Which prior topics were explicitly recalled? Note topic number if known.

**Concepts Forward-Seeded** — Which future topics were teased? Note topic number if known.

**Poll Questions Used** — Brief summary of each poll (the key conceptual test, not the full wording).

**Discussion Questions Used** — Brief summary of each discussion prompt.

**Avoid in Adjacent Topics** — Flag anything overused or heavily emphasized that should be rested: specific companies, datasets, example types, or framing approaches.

---

## Step 3: Write snapshot file

**File path:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/topic-{NN}-{course-code}-{kebab-slug}.md`
**Knowledge base root:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/`
- Pad topic number with leading zero: topic 8 → `08`, topic 16 → `16`

**Check for duplicate first:** If a snapshot for this topic already exists, ask the user whether to overwrite or append a revision section.

Write the file with **YAML frontmatter followed by markdown sections**. The YAML frontmatter is required — it enables semantic filtering in the RAG system.

```markdown
---
topic_number: {N}
topic_title: "{Topic Title}"
course_code: {course_code}
course_title: "{Course Title}"
date_prepared: {YYYY-MM-DD}
audience_level: {intro_undergrad | advanced_undergrad | masters}
class_type: {presentation | lab | presentation + lab}
category: lecture
companies: [{Company1}, {Company2}]
datasets: [{Dataset1}, {Dataset2}]
methodology: [{method1}, {method2}]
job_contexts: [{consulting}, {PM}, {policy}, {finance}, {data-analytics}]
notation: {symbol1: "meaning", symbol2: "meaning"}
examples_used: ["{example 1 brief}", "{example 2 brief}"]
forward_seeded: [{topic_N+1}, {topic_N+2}]
backward_referenced: [{topic_N-1}, {topic_N-2}]
---

## Theory Coverage
...

## Notation Used
...

## Examples Used
...

## Companies and Organizations Named
...

## Datasets Referenced
...

## Job Contexts Framed
...

## Concepts Backward-Referenced
...

## Concepts Forward-Seeded
...

## Poll Questions Used
...

## Discussion Questions Used
...

## Avoid in Adjacent Topics
...
```

---

## Step 4: Index into knowledge-rag RAG system

After saving the file, push it to the knowledge-rag MCP server so it is available for semantic search in future lectures.

**If knowledge-rag MCP is connected:**

Call: `add_document(content={full snapshot markdown}, filepath="lecture-snapshots/{filename}", category="lecture")`

- If the document already exists (update case): call `update_document(filepath=..., content=...)` instead
- Confirm: report how many chunks were indexed

**If knowledge-rag MCP is not connected:**

Skip RAG indexing gracefully. Note:
> "RAG indexing skipped — snapshot saved to disk only. Run `/rag-status` to check MCP connection, then `/save-snapshot {slug}` to re-index."

The file-based knowledge base (`/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/`) is always updated regardless of MCP status, so the system degrades gracefully to file scanning.

---

## Step 5: Update knowledge index

Append to `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/KNOWLEDGE.md` under the correct course section:

```markdown
## {Course Title} ({course_code})

- [Topic {N}: {Topic Title}](lectures/{filename}.md) — {date_prepared}
```

If the course section already exists, add the new entry in topic-number order. If it does not exist, create the section.

---

## Step 6: Confirm

Output a one-line confirmation:
```
📚 Snapshot saved: /Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/{filename}.md | RAG: {N chunks indexed | indexing skipped}
```
