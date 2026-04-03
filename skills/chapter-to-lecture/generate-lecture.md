# Stage 3: Generate Lecture Notes + Interactive Elements

## Purpose

Transform the chapter extract into polished, textbook-quality lecture notes that an instructor can teach directly from. The textbook chapter provides the content; this stage adapts it for live classroom delivery with interactive elements.

**Key difference from `/lecture-prep` Stage 5:** Content is sourced from the chapter extract (already reviewed textbook material + Presentation Expert recommendations) rather than a brainstorm. Interactive elements are grounded in the chapter's natural debate points, not invented from scratch. The Presentation Expert has already optimized the narrative arc, pacing, and visual flow — this stage executes that plan. More transformation, less creation.

---

## Inputs

- `{base}/{slug}/chapter-extract.md` — structured teaching plan from Stage 2, including Presentation Expert recommendations (already incorporated into the plan)
- Original textbook chapter (path from `intake.md`) — reference for full context
- `{base}/{slug}/intake.md` — course info, category, class type (all auto-derived from textbook + course code)

---

## Voice and Style

Identical to the existing lecture draft methodology. See `skills/lecture-draft/draft-presentation.md` for the full style guide. Key points:

- **Angrist & Pischke meets graduate lecture** — rigorous but approachable
- **Paragraphs, not bullets** — complete prose with topic sentences
- **Intuition → Math → Interpretation** — never present an equation cold
- **Speaking notes are sentences** — not "discuss X" but actual words to say
- **"Smart friend" test** — a student reading alone should understand everything

---

## Document Structure

Based on `skills/lecture-draft/draft-presentation.md` with additions from expert review:

```
# {topic_title}
## {course_title} — Chapter {chapter_number} of {total}
### {date} | {class_duration} min | {class_type}

## 🎯 Learning Objectives (from chapter-extract.md)

## 🔁 Retrieval Practice ({3-4} min)

Quick-fire recall from prerequisite chapters (from `builds_on` in frontmatter).
2-3 questions that activate prior knowledge needed for today's lecture.
Format: verbal, show of hands, or quick poll. NOT graded.

Example for ch14 (builds_on: [4, 5, 8, 10]):
> "Quick check — what does it mean for a good to be 'elastic'? If demand is elastic and price rises 10%, what happens to revenue?"

This is NOT the opening hook. It precedes the hook and warms up the neural pathways.

## 🪝 Opening Hook
## 📚 Section N: {concept} ({minutes} min)
  ### Intuition
  ### Formal Treatment
  ### Industry Application: {Company}
  ### ⚠️ Common Misconception
  ### 🔢 Worked Example
  ### 💻 In Code
  ### 🎯 Decision Scenario
## 📊 Class Poll
## 💬 In-Class Discussion
## 🔄 Discussion Debrief
## 🔗 Connections
## 🎯 Key Takeaways
## 🎫 Exit Ticket (2 min)
## 📖 Supplementary Resources
## 📋 Appendix: Instructor Notes
```

---

## Content Sourcing Rules

### What comes from the chapter (transform, don't create):
- Learning objectives → take from chapter-extract.md, adjust Bloom's levels if needed
- Key concepts and definitions → rewrite for spoken delivery (shorter, punchier)
- Equations → same math, but add spoken interpretation layer
- Industry examples → use the 2-4 selected in chapter-extract.md, expand with speaking notes
- Common misconceptions → from chapter, add correction scripts
- Cross-references → from chapter, frame as "remember when..." and "next time we'll..."

### What is generated fresh for the lecture:
- Opening hook — construct from the chapter's strongest example or opening scenario, adapted for live delivery
- Speaking notes — all new; the textbook doesn't have these
- Discussion questions — grounded in chapter debates but phrased for classroom use
- Poll questions — test comprehension of chapter concepts
- Discussion debriefs — bridge insights back to formal concepts
- Worked examples — may use chapter's examples but reformatted for board work
- Code snippets — 2-8 line bridges adapted by course subcategory
- Decision scenarios — derived from chapter tradeoffs
- Timing and pacing notes — all new

### What is NOT included (moved to textbook pipeline):
- Interview callouts (💼) — NOT generated in this pipeline
- Before/After comparisons (↔️) — only if the chapter naturally contains them

---

## Course Category Adaptations

### Qualitative Courses (principles, micro-theory, game-theory)

| Element | Adaptation |
|---------|-----------|
| **Worked examples** | Graphical + simple algebra. "Price rises from $5 to $7..." |
| **Code bridges** | Excel formulas for principles; SymPy for micro-theory; nashpy for game theory |
| **Discussions** | Policy debates, "What would you advise?", multiple valid positions |
| **Polls** | Opinion-based predictions, "Which matters more?", welfare comparisons |
| **Decision scenarios** | "You're the regulator / firm / consumer. What do you choose?" |
| **Figures** | Supply/demand curves, game matrices, welfare diagrams, flowcharts |
| **Opening hook** | News story, policy debate, "last week at the grocery store..." |

### Quantitative Courses (ml-stats, econometrics, finance)

| Element | Adaptation |
|---------|-----------|
| **Worked examples** | Step-by-step computation with real numbers. Show all intermediate steps. |
| **Code bridges** | Python (scikit-learn, statsmodels, numpy) for ml-stats; R snippets optional |
| **Discussions** | "Which method?", tradeoff analysis, "What goes wrong if assumption X fails?" |
| **Polls** | "Predict the output", estimation challenges, "What's the bias direction?" |
| **Decision scenarios** | "n=500, p=50, deadline Friday. Regularize or feature-select?" |
| **Figures** | Scatter plots, regression surfaces, ROC curves, bias-variance curves |
| **Opening hook** | Data surprise, model failure story, "Netflix/Zillow tried X and..." |

---

## Lab Generation (Conditional)

**Condition:** `class_type` includes `lab` AND `course_category` is `quantitative`

If triggered, follow the existing lab methodology:
- Read `skills/lecture-draft/draft-lab.md` for Jupyter notebook generation
- Read `skills/lecture-draft/draft-lab-html.md` for HTML companion generation

**Lab content is derived from the chapter:**
- Use the chapter's datasets and examples as lab exercises
- Progressive difficulty: Part 1 (guided) → Part 2 (semi-guided) → Part 3 (open-ended)
- Exercise blanks (`___`) for students to fill in
- Solutions notebook with all blanks filled + cells executed

**Lab naming:** `lab_{chapter_number}_{short_name}.ipynb`

---

## Activity Generation (Conditional)

**Condition:** `class_type` includes `activity` AND `course_category` is `qualitative`

If triggered, generate an in-class activity section:

```markdown
## 🎮 In-Class Activity: {title} ({duration} min)

**Setup:** {what students need — handouts, partners, access to device}

**Instructions:**
1. {step 1}
2. {step 2}
3. {step 3}

**Debrief questions:**
- {question connecting activity to theory}
- {question asking what surprised them}

**Instructor notes:** {common issues, how to keep groups on track, what to watch for}
```

Activities are extracted from the textbook chapter if one exists, or constructed from the chapter's case studies (e.g., "Role-play the prisoner's dilemma with your neighbor").

---

### Exit Ticket Format

A 2-minute formative assessment at the end of class. Students write (on paper or device):

1. **One thing I learned:** {prompt tied to a key learning objective}
2. **One thing I'm confused about:** {open-ended}

The instructor collects (or reviews digitally) to identify what landed and what did not. This is the single most evidence-backed active learning strategy for improving retention (Angelo & Cross, 1993).

**Adapt by course category:**
| Category | Exit ticket style |
|----------|-----------------|
| `qualitative` | "Name one market force that explains the teacher-programmer wage gap" |
| `quantitative` | "Write the MRP formula and interpret one term in plain English" |

---

## Quality Standards

Before finalizing, verify:

**Completeness:**
- [ ] Every MUST concept from chapter-extract appears in the notes
- [ ] Every concept has: intuition, formal treatment (if applicable), example
- [ ] Every equation has all terms interpreted
- [ ] Every selected example has: context, problem, method, outcome
- [ ] At least 1 worked example with real numbers (🔢)
- [ ] At least 1 code-concept bridge appropriate for course subcategory (💻)
- [ ] At least 1 decision scenario with 2-3 options (🎯)
- [ ] Every figure has descriptive alt text (not just `![Figure 1]`)

**Interactive elements (duration-scaled):**
- [ ] Total interactions = floor(content_minutes / 10), minimum 3
- [ ] At least 1/3 are discussions (Bloom's L4+)
- [ ] At least 1/3 are polls (Bloom's L2-3)
- [ ] Engagement point every 8-12 minutes
- [ ] Quick-response and deep-processing types alternate (no 2 polls back-to-back)
- [ ] Discussion debrief after every discussion block

**Assessment alignment:**
- [ ] Every learning objective has at least 1 corresponding assessment moment (poll, discussion, or worked example)
- [ ] Retrieval practice section references prerequisite chapters from `builds_on`
- [ ] Exit ticket question tied to a core learning objective

**Style:**
- [ ] No section is just bullet points — all explanations in prose
- [ ] Speaking notes are actual sentences, not prompts
- [ ] Tone: rigorous but engaging
- [ ] Math at the right level for the audience

**Time check:**
- [ ] Total time budget fits within `class_duration`
- [ ] No single section exceeds 15 minutes without an interactive break
- [ ] Retrieval practice (3-4 min) + exit ticket (2 min) included in budget

---

## Output

- `{base}/{slug}/lecture-notes.md` — append sentinel `<!-- pipeline-complete: stage-3 -->` at the end
- `{base}/{slug}/lab_{N}_{short_name}.ipynb` (if applicable)
- `{base}/{slug}/lab_{N}_{short_name}.html` (if applicable)
- `{base}/{slug}/solutions/lab_{N}_{short_name}_solutions.ipynb` (if applicable)

---

## Transition

```
✅ Stage 3 complete — lecture-notes.md ({word_count} words, {section_count} sections)
   Interactive: {N} discussions, {M} polls, {K} decision scenarios
   {Lab: lab_{N}_{name}.ipynb + HTML companion + solutions | Lab: not applicable}
   Moving to figure generation...
```
