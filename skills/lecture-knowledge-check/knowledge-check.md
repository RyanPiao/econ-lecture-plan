# Knowledge Check — Methodology

## Purpose

Before brainstorming a new lecture, query the course knowledge base to:
1. Prevent reusing the same examples, companies, or datasets
2. Maintain notation consistency across topics
3. Honor forward seeds planted by prior topics
4. Identify backward links this topic should activate

---

## Step 1: Determine retrieval mode

**Check if knowledge-rag MCP is connected** (attempt any MCP call; if it fails, switch to fallback).

- **MCP available → use RAG queries** (Steps 2a–3a below)
- **MCP unavailable → use file scan fallback** (Steps 2b–3b below)

If no snapshots exist for this course in either mode: output "No prior snapshots found for this course. Proceeding with a fresh brainstorm." and skip to Step 4.

---

## Step 2a: RAG queries (when MCP is connected)

Run the following searches against the knowledge-rag MCP, all with `category="lecture"`:

| Purpose | Call |
|---|---|
| All companies/datasets used in this course | `search_knowledge("{course_code} companies datasets examples used", category="lecture", max_results=20)` |
| Detail on adjacent prior topics | `search_knowledge("{course_code} topic {N-1} topic {N-2} topic {N-3}", category="lecture", max_results=6)` |
| Adjacent future topics (avoid stealing their content) | `search_knowledge("{course_code} topic {N+1} topic {N+2}", category="lecture", max_results=4)` |
| Forward seeds pointing to this topic | `search_knowledge("{course_code} forward seed topic {N}", category="lecture", max_results=5)` |
| Notation established in this course | `search_knowledge("{course_code} notation symbol introduced", category="lecture", max_results=10)` |
| Same methodological family | `search_knowledge("{course_code} {topic_methodology}", category="lecture", max_results=5)` |
| Companies/datasets in paper snapshots | `search_knowledge("companies datasets industry examples", category="paper", max_results=10)` |
| Research insights relevant to this topic | `search_knowledge("{topic_title} {topic_methodology}", category="research", max_results=5)` |

Synthesize all results — deduplicate by source document, note which topic/paper/project each item comes from.

---

## Step 2b: File scan fallback (when MCP is unavailable)

**Knowledge base root:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/`

### 2b-i. Lecture snapshots

List all files in `lectures/` matching `{course_code}`.

**Always read:**
- Topics N-1, N-2, N-3 (immediately prior — examples must not repeat)
- Topics N+1, N+2 (immediately following — honor seeds, don't steal content)

**Read if they exist:**
- Any topic whose `forward_seeded` YAML field includes N
- Any topic in the same methodological family

**Skim headers only** (just `companies` and `datasets` YAML fields):
- All other course snapshots

### 2b-ii. Paper snapshots

List all files in `papers/`. For each paper snapshot:
- Extract YAML frontmatter: `citekey`, `tags`, `methodology`
- Skim for company names, datasets, and industry contexts mentioned
- Note any methodological overlap with the current topic (e.g., a paper using Lasso is relevant when preparing a regularization lecture)

### 2b-iii. Research synthesis

List all files in `research/` (recursively). For each synthesis doc:
- Skim section headers and key findings
- Note companies, datasets, or methodologies referenced
- Flag findings that could serve as "cutting-edge research" examples in the lecture

---

## Step 3: Build Consistency Context Report

From either retrieval mode, produce the same structured report:

### 🚫 Do Not Reuse
List all examples, companies, datasets, and discussion framings used in prior topics.
Group by type:
- **Companies/Orgs:** [list] — last used in Topic N
- **Datasets:** [list] — last used in Topic N
- **Example types overused:** [e.g., "Amazon pricing used in Topics 3, 7 — rest this"]
- **Discussion frames to avoid:** [e.g., "gig economy framing used in Topics 4 and 9"]

### 🔔 Honor These Forward Seeds
List any forward seeds planted by prior topics that point to the current topic.
Format: "Topic {N} told students: '{seed text}' — deliver on this promise."

### ✅ Notation Conventions Established
List all notation from prior topics that must be preserved.
Format: `symbol → meaning (introduced Topic N)`
Flag any notation conflicts (same symbol used differently in different topics).

### 🔗 Activate These Backward Links
List concepts from prior topics that the current topic should explicitly recall.
Format: "Topic {N} covered {concept} — students should recall this when you introduce {current concept}."

### 📄 Paper Snapshot Intelligence
Companies/orgs mentioned in paper snapshots (rest if recently cited in lectures):
- [list from papers/ scan, with paper citekey]

Datasets referenced in papers (available for lecture use if appropriate):
- [list from papers/ scan, with access details]

Methodological insights from papers that relate to this topic:
- [e.g., "Noack & Rothe 2024 uses flexible covariate adjustment — relevant if teaching matching"]
- [e.g., "Assad et al. 2024 studies algorithmic pricing — could illustrate prediction-vs-explanation"]

### 🔬 Research Synthesis Insights
Key findings from research/ that could enrich this lecture:
- [e.g., "Gap analysis identifies lack of welfare estimation — could motivate a discussion question"]
- [e.g., "Lit review maps debate on algorithmic collusion — relevant for policy examples"]

Projects with active research in this topic area:
- [project name]: [1-sentence description of relevance]

### 💡 Fresh Territory Available
Note example types, industries, companies, or datasets not yet used in this course (checking across lectures, papers, AND research) and appropriate for the current topic.
Examples: "No policy/Fed examples used yet", "No Boston-specific case studies in last 4 topics", "No consulting framing since Topic 3"

---

## Step 4: Output the report

Print the full Consistency Context Report to the conversation.

Also write it to: `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/knowledge-context.md`

Note at the top of the file whether the report was built from RAG queries or file scan fallback:
```
<!-- Source: knowledge-rag MCP (semantic search) | {date} -->
<!-- or -->
<!-- Source: file scan fallback (MCP unavailable) | {date} -->
```

---

## Step 5: Pass to brainstorm

The brainstorm stage reads `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/knowledge-context.md` as a hard constraint file.

All items in **Do Not Reuse** are **prohibited** in the new lecture.
All items in **Honor These Forward Seeds** must be delivered in the lecture.
All items in **Notation Conventions** must be respected exactly.

---

## Instructor profile constraints (always apply regardless of snapshots)

These apply to every lecture for this course regardless of knowledge base state:

- **Student audience:** Economics, stats, econ ML students at Northeastern University (Boston Back Bay)
- **Job contexts to prioritize:** Business/econ consulting, PM, policy analysis, finance, data analytics
- **Local connection:** Prefer Boston-area examples, local firms, Boston/MA economy data when relevant
- **Example currency:** 2024–2026 only unless historically significant
- **Engagement first:** Lead with what students find surprising, relevant to their career, or personally connected to Boston
- **Avoid:** Generic textbook examples with no job or industry connection
