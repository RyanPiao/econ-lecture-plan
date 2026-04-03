# Stage 2: Extract + Adapt + Presentation Expert Review

## Purpose

Read the textbook chapter, extract all teachable elements, then run a **Presentation Expert review** to optimize the material for live classroom delivery. The textbook provides the content; this stage plans *how to present it* — pacing, storytelling, audience engagement, and visual flow.

---

## Inputs

- `{base}/{slug}/intake.md` — course info, category, chapter path, audience level, class type (all auto-derived)
- The textbook chapter file itself (read in full)
- `econ-lecture-knowledge/lectures/` — existing snapshots for deconfliction (lightweight scan)

---

## Step 1: Parse the Chapter

Read the full textbook chapter and extract:

### A. Structure
- Chapter title and subtitle
- All `##` section headings with hierarchy
- Estimated content density per section (short / medium / long)

### B. Learning Objectives
- From chapter frontmatter or `## Learning Objectives` section
- If not explicit, infer 4 objectives at Bloom's Levels 2-6 from the content

### C. Key Concepts
- Every bold definition, `> **Key Concept**` block, or `<Definition>` MDX component
- For each: concept name, one-sentence definition, prerequisite concepts

### D. Examples and Applications
- Every industry example, case study, real-world application
- For each: company/entity, problem, method, outcome, source
- Rate each for lecture suitability: ⭐ (mention briefly) / ⭐⭐ (discuss) / ⭐⭐⭐ (deep dive)

### E. Equations and Formal Treatment
- Every equation block (`$$...$$` or `$...$` inline)
- For each: the equation, its plain-language meaning, which section it belongs to
- Rate for lecture inclusion: MUST / SHOULD / SKIP

### F. Figures and Visualizations
- Every figure reference or chart description in the chapter
- Note if source images exist in `ebook/public/images/chapters/ch{NN}/`
- Rate: reuse-as-is / adapt-for-slides / generate-new

### G. Activities and Simulations
- Any experiential learning elements from the chapter
- Case-based exercises, simulations, group activities
- Note estimated time to run in class

### H. Common Misconceptions
- Every `> **Common Misconception**` block or explicit correction
- For each: the misconception, why it's wrong, how to address it

### I. Cross-References
- References to other chapters (backward and forward)
- Recurring narrative threads (Campus Coffee Shop, Your Career, etc.)

---

## Step 2: Plan the Lecture

Using the extraction, build a time-budgeted teaching plan:

### Time Allocation Rules

| Section Type | Min Time | Max Time | Notes |
|-------------|----------|----------|-------|
| Opening hook | 3 min | 5 min | From the chapter's opening scenario or construct from its strongest example |
| Core concept section | 8 min | 15 min | Include intuition + formal + example |
| Discussion block | 4 min | 6 min | Think-pair-share or open |
| Class poll | 2 min | 3 min | Including reveal script |
| Discussion debrief | 2 min | 3 min | Bridge to next section |
| Worked example | 5 min | 8 min | Board work with specific numbers |
| Code snippet bridge | 2 min | 3 min | Not a full exercise — just a bridge |
| Activity / simulation | 8 min | 15 min | Only if class_type includes activity |
| Closing + takeaways | 3 min | 5 min | Key sentences + forward seeds |

**Total must fit within `class_duration` from intake.** If content exceeds time, prioritize by:
1. MUST concepts (core learning objectives)
2. ⭐⭐⭐ examples (deep dives)
3. Interactive elements (min 2 discussions + 3 polls)
4. SHOULD concepts
5. ⭐⭐ examples

Cut from the bottom up. Never compress — cut entire sections cleanly.

### Example Selection

The chapter may have 4-8 examples. Select 2-4 for the lecture:
- At least 1 that students personally relate to (consumer experience, campus life, career)
- At least 1 with quantified outcomes (real numbers, real impact)
- Prefer diversity across industries/contexts
- Avoid any company/dataset in the "Do Not Reuse" list from knowledge deconfliction

### Interactive Element Anchors

Place engagement points every 8-12 minutes. **Use a duration-scaled formula** instead of fixed minimums:

| Class Duration | Total Interactions | Min Discussions (Bloom's L4+) | Min Polls (Bloom's L2-3) | Flex |
|---------------|-------------------|------------------------------|-------------------------|------|
| 50 min | 3 | 1 | 1 | 1 |
| 75 min | 5 | 2 | 2 | 1 |
| 100 min | 7 | 2-3 | 2-3 | 1 |

**Define `content_minutes`:** `content_minutes = class_duration × 0.7` (approximately 30% of class time goes to interactions).
- 50 min class → ~35 min content → 3 interactions
- 75 min class → ~52 min content → 5 interactions
- 100 min class → ~70 min content → 7 interactions

**Formula:** `interactions = floor(content_minutes / 10)`, minimum 3. At least 1/3 discussions, at least 1/3 polls, remainder is instructor's choice.

**Rhythm check:** Alternate between quick-response (polls, show of hands) and deep-processing (discussions, decision scenarios). Never place 2+ interactions of the same cognitive demand back-to-back.

Placement rules:
- After each major concept: discussion OR poll (alternate)
- After the strongest industry example: decision scenario
- Before formal treatment: prediction poll ("What do you think happens when X?")

**Adapt by course category:**

| Category | Discussion style | Poll style |
|----------|-----------------|-----------|
| `qualitative` | Policy debate, "What would you advise?", multiple valid positions | Prediction, opinion, "Which matters more?" |
| `quantitative` | "Which method would you choose?", tradeoff analysis | "Predict the output", estimation, "What goes wrong if?" |

---

## Step 3: Presentation Expert Review

After extraction and lecture planning, run a **Presentation Expert** review of the teaching plan. This is a single focused reviewer (not the 3-persona review from the old pipeline) who specializes in transforming written content into compelling live presentations.

### Reviewer Persona: Presentation Expert

**Role:** An experienced university lecturer and instructional designer who has delivered 500+ lectures. Specializes in audience engagement, cognitive load management, and visual storytelling in economics education.

**Review the extracted teaching plan and evaluate:**

#### 1. Objective Feasibility (check first)
- For each learning objective, estimate the minimum time for a student to move from "hasn't seen this" to "can demonstrate it."
- Sum the minimum times. If the sum exceeds `class_duration` minus interactive time (subtract ~20 min for discussions/polls/debriefs), either:
  - Split the lecture across two sessions, or
  - Downgrade one objective from "mastery" to "exposure" (note it in the extract)
- Flag any objective that has no corresponding assessment moment (discussion, poll, or worked example that tests it).

**Recommendation format:** "LO 14.3 requires ~15 min for mastery (Lorenz curve + Gini calculation). With 4 other LOs, this exceeds the 55 min content budget. Recommend: split Gini calculation to IF TIME."

#### 2. Narrative Arc
- Does the lecture tell a story? Is there a clear beginning (hook), middle (build), and end (payoff)?
- Are sections connected by transitions, or do they feel like separate topics?
- Is the opening hook strong enough to grab attention in the first 30 seconds?
- Does the closing create a "so what?" moment that students remember?

**Recommendation format:** "Move {section} before {section} because..." or "Strengthen the hook by..."

#### 3. Cognitive Load & Pacing
- Are dense sections followed by lighter interactive breaks?
- Is there too much new content between engagement points? (Max 12 min without interaction)
- Are worked examples placed *after* intuition but *before* formal treatment? (Students need numbers before abstraction)
- Is the time budget realistic? Flag any section that's overloaded.

**Recommendation format:** "Split Section 2 — students need a poll between MRP definition and the worked example" or "Cut {concept} to IF TIME — 5 MUST concepts in 75 min is too many"

#### 4. Visual Flow for Slides
- Which concepts need a figure or diagram to land? (Don't just describe — show)
- Where should progressive builds be used? (Layer-by-layer reveal instead of full diagram at once)
- Are there text-heavy sections that should become a table, chart, or comparison layout on slides?
- Which figures from the textbook work on slides vs need to be regenerated at slide-friendly aspect ratio?

**Recommendation format:** "Add progressive build for MRP table — show one row at a time" or "The Lorenz curve needs a slide-optimized version (textbook image is too detailed)"

#### 5. Audience Engagement Strategy
- Are discussions placed at natural debate points (not forced)?
- Do poll questions have genuinely tempting wrong answers (not obvious)?
- Is there at least one moment where students are physically active (stand up, move, raise hands)?
- For activities: is the setup clear enough that students can start within 30 seconds?

**Recommendation format:** "The discrimination discussion works better as a 'stand on a spectrum' activity" or "Poll Q2's wrong answers are too obviously wrong — make option C more tempting"

#### 6. Assessment Alignment
- For each learning objective, identify which interactive element (discussion, poll, worked example) provides evidence that the objective was met.
- If an objective has no corresponding assessment moment, flag as must-fix.
- Verify poll wrong answers are genuinely tempting (not obviously wrong).

**Recommendation format:** "LO 14.2 (wage differentials) has no assessment moment. Add a poll after Section 3 testing compensating differentials vs human capital."

#### 7. Content Integrity
- Check all equations for dimensional consistency.
- Verify definitions are standard (not idiosyncratic to the textbook's first draft).
- Flag any claim stated without conditions or assumptions.
- If the chapter's `status` field is `first-draft`, flag any equation or statistic that should be double-checked.

**Recommendation format:** "The Gini formula in Section 4 omits the '1 -' prefix. Verify against standard definition."

#### 8. Instructor Confidence
- Are there any sections where the speaking notes would leave an instructor guessing?
- Are transitions between sections explicit? ("Now that we know X, let's ask: what happens when Y?")
- Are there backup plans for if an activity falls flat or runs long?

**Recommendation format:** "Add a cut point at 0:45 — if the simulation runs long, skip Section 4 and go straight to takeaways"

### Review Output

The presentation expert produces actionable recommendations categorized as:
- `must-fix` — pacing or engagement problems that will hurt the lecture
- `should-fix` — improvements that make the lecture noticeably better
- `nice-to-have` — polish items

**Incorporate all `must-fix` and `should-fix` items into the chapter extract before writing it.** Log `nice-to-have` items in the "Adaptation Notes" section.

---

## Step 4: Knowledge Deconfliction (Lightweight)

**Filter by course code first** to prevent O(n) growth as the knowledge base scales:
```bash
ls "/Users/openclaw/Resilio Sync/Documents/econ-lecture-knowledge/lectures/"*${course_code}* 2>/dev/null
```

Only read snapshots matching the current course code. Ignore snapshots for other courses.

If matching snapshots exist, extract:
- Companies and datasets used → "Do Not Reuse" list
- Notation established → maintain consistency
- Forward seeds planted → honor if this chapter delivers on them

If no prior snapshots: note "First lecture for this course" and proceed.

This is lighter than the full knowledge-check stage — no MCP semantic search, just file scan and YAML frontmatter parsing.

---

## Step 5: Write the Chapter Extract

Output: `{base}/{slug}/chapter-extract.md`

Use the template at `templates/chapter-extract.md`. The extract must include:

```markdown
# Chapter Extract: {chapter_title}

**Source:** {chapter_path} ({word_count} words)
**Course:** {course_code} | **Category:** {course_category} ({course_subcategory})
**Duration:** {class_duration} min | **Type:** {class_type}

---

## Learning Objectives
1. [Bloom's L2]: {from chapter}
2. [Bloom's L3]: {from chapter}
3. [Bloom's L4]: {from chapter}
4. [Bloom's L5/6]: {from chapter}

---

## Lecture Time Budget

| Time | Section | Content | Interactive |
|------|---------|---------|------------|
| 0:00–0:04 | Opening Hook | {description} | — |
| 0:04–0:16 | Section 1: {title} | {key concepts} | Poll at 0:12 |
| 0:16–0:22 | Discussion 1 | {topic} | Think-pair-share |
| ... | ... | ... | ... |
| {end}–{close} | Takeaways | 5 key sentences | — |

**Total: {sum} min** (fits / exceeds by {N} min — cut {section})

---

## Key Concepts (Prioritized)

### MUST (core to learning objectives)
1. **{concept}** — {one-line definition}. Formal treatment: {equation or "graphical only"}
2. ...

### SHOULD (important but cuttable if time-short)
1. **{concept}** — {one-line definition}
2. ...

### IF TIME (enrichment)
1. **{concept}** — {one-line definition}
2. ...

---

## Examples Selected for Lecture

| # | Company/Context | Problem | Method | Outcome | Suitability | Source |
|---|----------------|---------|--------|---------|-------------|--------|
| 1 | {company} | {problem} | {method} | {quantified} | ⭐⭐⭐ deep dive | {source} |
| 2 | {company} | {problem} | {method} | {quantified} | ⭐⭐ discuss | {source} |
| 3 | {company} | {problem} | {method} | {quantified} | ⭐ mention | {source} |

**Not selected:** {list examples from chapter that were cut, with reason}

---

## Equations to Present

| # | Equation | Section | Priority | Interpretation Plan |
|---|----------|---------|----------|-------------------|
| 1 | $...$ | Section 1 | MUST | {how to explain it} |
| 2 | $...$ | Section 2 | SHOULD | {how to explain it} |

---

## Interactive Element Anchors

| Time | Type | Topic | Format |
|------|------|-------|--------|
| ~0:12 | Poll | {prediction question before formal treatment} | 4-option MC |
| ~0:20 | Discussion | {debate/analysis after Section 1} | Think-pair-share |
| ~0:28 | Decision Scenario | {choose between approaches} | Show of hands |
| ~0:36 | Poll | {concept check after Section 2} | 4-option MC |
| ~0:44 | Discussion | {evaluation question} | Open discussion |
| ~0:50 | Poll | {application question} | 4-option MC |

---

## Figures Needed

| # | Description | Source | Action |
|---|------------|--------|--------|
| 1 | {description} | Textbook `fig_01.png` | Reuse (correct aspect) |
| 2 | {description} | — | Generate new |
| 3 | {description} | Textbook `fig_03.png` | Adapt (crop for slides) |

---

## Deconfliction Constraints

**Do Not Reuse (companies):** {list from prior snapshots, or "None — first lecture"}
**Do Not Reuse (datasets):** {list}
**Notation to maintain:** {symbol: meaning, or "None established"}
**Forward seeds to honor:** {from prior lectures, or "None"}

---

## Presentation Expert Recommendations

### Applied (must-fix / should-fix)
1. {recommendation that was incorporated into the plan above}
2. ...

### Noted (nice-to-have)
1. {polish item for the instructor to consider}
2. ...

---

## Adaptation Notes ({course_subcategory})

{2-3 sentences on how to adapt this chapter for lecture delivery, specific to the course sub-category. E.g., "For principles: emphasize graphical intuition over algebra. Use the Campus Coffee Shop thread. Excel formula bridges instead of Python."}
```

---

## Transition

```
✅ Stage 2 complete — extracted {N} concepts, selected {M} examples, planned {K} interactive elements
   Time budget: {sum} min / {class_duration} min allocated
   Moving to lecture generation...
```
