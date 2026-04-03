# Textbook-Style Lecture Notes Methodology

## Purpose
Transform the reviewed brainstorm into polished, textbook-quality lecture notes that an instructor can teach directly from. The output should be comprehensive enough that a well-prepared substitute instructor could deliver the lecture without additional preparation.

---

## Voice and Style

**Model:** Think Angrist & Pischke's "Mostly Harmless Econometrics" meets a well-organized graduate lecture. Rigorous but approachable. Engaging but precise.

**The "smart friend" test:** Would a bright student reading these notes alone understand every concept clearly? Every definition? Every equation? If not, the notes are not complete enough.

**Paragraphs, not bullets:** Lecture notes are not slide outlines. Write in complete paragraphs with clear topic sentences. Use bullet lists only for enumerated items (steps, assumptions, examples) not for flowing explanation.

**Intuition → Math → Interpretation:** Never present an equation cold. Always:
1. Explain in plain language what we're about to show
2. Present the equation or formal treatment
3. Interpret every term in plain English
4. Explain what happens when parameters change

**Instructor identity:** This system serves an applied economist who bridges classical econometrics with contemporary ML. The teaching philosophy is "Foundations First, Expansion Second" — students build from manual derivations to computational tools. Every concept should have a numerical worked example before abstraction, a code snippet before the lab, and an explicit career connection. Active learning (simulations, case-based exercises, group decision scenarios) is the default. The pipeline adapts its content based on `course_category` from the intake form.

**Speaking notes are sentences, not prompts:** Bad: "Discuss why IV is useful here." Good: "At this point, say: 'So why do we need instrumental variables at all? Here's the problem: if students who attend college are fundamentally different from students who don't — maybe they're more motivated, or come from wealthier families — then just comparing wages for college attendees versus non-attendees tells us about selection, not about the causal return to education. IV solves this by finding variation in college attendance that has nothing to do with those confounders.'"

---

## Document Structure

Use this exact structure for `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/lecture-notes.md`:

---

```
# {topic_title}
## {course_title} — Topic {topic_number} of {total_topics}
### {date} | {class_length_minutes} min | {class_type}

---

## 🎯 Learning Objectives

By the end of this lecture, students will be able to:
1. [Bloom's Level 2 — Understand]: {objective using verb: explain, describe, identify...}
2. [Bloom's Level 3 — Apply]: {objective using verb: use, implement, calculate...}
3. [Bloom's Level 4 — Analyze]: {objective using verb: compare, distinguish, examine...}
4. [Bloom's Level 5/6 — Evaluate/Create]: {objective using verb: evaluate, design, construct...}

---

## 🪝 Opening Hook ({hook_minutes} min)

{2–4 sentences describing the real-world scenario or question. Written as prose the instructor reads aloud or paraphrases. Must use 2024–2026 data.}

**Speaking notes:** {3–6 sentences of exactly what to say. Include the "why should you care" framing. End with the question posed to students.}

**Question to pose:**
> {The exact question written on the board or displayed — should be genuinely open, not rhetorical}

---

## 📚 Section {N}: {concept_title} ({estimated_minutes} min)

### Intuition

{2–4 paragraph plain-language explanation. Use analogies and concrete examples. Build from what students already know. First paragraph establishes the problem/need. Second paragraph gives the intuition. Third paragraph (if needed) gives an accessible example.}

**Speaking notes:** {Detailed talking points for teaching this intuition. Include:
- Transition from the previous section or hook
- The analogy you'll use and how to set it up
- Anticipated student questions and how to address them
- A natural pause point for students to take notes}

### Formal Treatment

{Full mathematical framework appropriate for the audience level. For masters: complete derivations with all steps shown. For advanced undergrad: key results with proof sketch. For intro undergrad: graphical treatment with algebraic summary.}

$$
{Key equation in LaTeX}
$$

**Where:**
- ${symbol}$ = {plain-language interpretation of each term}
- ${symbol}$ = {interpretation}

**Interpretation:** {2–3 sentences explaining what the equation tells us. What does it mean when the key parameter increases? Decreases? What are the units?}

**Key result:** {State the main theorem, lemma, or empirical regularity in a box or bold text}

**Speaking notes:** {How to present the math. What to write on the board vs. what to just say. Common notation confusions to pre-empt. Where to pause and check for understanding.}

### Industry Application: {Company} — {Problem Title}

**Context:** {1–2 sentences on the company and why this problem mattered}

**The problem:** {Specific business or policy question they faced}

**The method:** {Exactly which technique from this lecture they used, and key implementation details}

**The result:** {Quantified outcome — percentage, dollars, accuracy improvement, policy change — with specific numbers}

**Why students should care:** {1 sentence connecting this to careers or everyday life}

*Source: [{Author/Organization, Year}]({URL})*

**Speaking notes:** {How to present this case study. What to emphasize. Whether to show a chart. What question to pose after: e.g., "What assumption is this company making that we haven't verified yet?"}

### ⚠️ Common Misconception

**Students often think:** {State the misconception precisely}

**Why this seems reasonable:** {Acknowledge why the wrong intuition is plausible}

**Why it's wrong:** {The correction. Be specific.}

**Speaking notes:** {Whether to present this proactively or wait for it to come up. Suggested phrasing for the correction.}

---

### 🔢 Worked Example

Walk through the concept with specific numbers — 5 to 10 data points, every calculation shown. This is not the lab; it's a by-hand exercise the instructor works through on the board.

**Adapt by `course_category`:**

| course_category | What the worked example looks like |
|-----------------|-------------------------------------|
| `ml-stats` | Compute MSE, bias², variance on 5 data points; or fit a 2-feature OLS by hand and interpret |
| `game-theory` | Solve a 2×2 payoff matrix: list strategies, find best responses, circle Nash equilibrium |
| `micro-theory` | Lagrangian optimization with U = x^0.5 · y^0.5, p_x = 2, p_y = 3, I = 120 — solve for x*, y* |
| `principles` | "If price rises from $5 to $7, quantity drops from 100 to 80. Elasticity = ..." |
| `finance` | "A bond pays $50/year for 10 years, face value $1000, market rate 6%. Price = ..." |
| `general` | Numerical example appropriate for the topic using the simplest relevant math |

**Format:**
```
**Data:** {the specific numbers — table or list}
**Step 1:** {first calculation, showing work}
**Step 2:** {next calculation}
...
**Result:** {final answer with plain-language interpretation}
**Check:** {sanity check — does this make sense? What if we changed X?}
```

**Speaking notes:** {How to present this on the board. Where to pause and ask "what do you think the next step is?" before revealing.}

---

### 💻 In Code

A short (2–8 line) code snippet showing how this concept looks computationally. Not a full exercise — just a bridge between the math and the lab.

**Adapt by `course_category`:**

| course_category | Language & tools |
|-----------------|-----------------|
| `ml-stats` | Python: scikit-learn, statsmodels, numpy |
| `game-theory` | Python: nashpy, numpy, or sympy |
| `micro-theory` | Python: sympy for symbolic optimization |
| `principles` | **Excel formulas**: `=SLOPE()`, `=(B2-B1)/(A2-A1)`, `=PV()` |
| `finance` | Python (numpy.pv, numpy.irr) or Excel (`=PV()`, `=RATE()`) |
| `general` | Python with standard libraries |

**Format:**
```python
# {One-line description of what this computes}
{2–8 lines of clean, runnable code}
# Output: {what the student will see}
```

**Speaking notes:** "You don't need to memorize this syntax — you'll use it in the lab. But notice how the equation we just derived maps directly to this code."

---

### 🎯 Decision Scenario (at least 1 per lecture)

A structured scenario where students must choose between 2–3 approaches and justify their choice. Not open-ended discussion — constrained decision with explicit tradeoffs.

**Adapt by `course_category`:**

| course_category | Example scenario type |
|-----------------|-----------------------|
| `ml-stats` | "n=500, p=50, deadline Friday. Use all features + CV, or pre-select 10? Defend your choice." |
| `game-theory` | "Player 1 might cooperate or defect. You move second. What's your strategy and why?" |
| `micro-theory` | "This firm's MC crosses ATC at q=100. A competitor enters. Stay or exit?" |
| `principles` | "You're the Fed chair. Inflation 5%, unemployment 3%. Raise rates, hold, or cut?" |
| `finance` | "Yield curve inverted yesterday. You manage a bank portfolio. What do you change?" |

**Format:**
```
**Scenario:** {2–3 sentences setting up the decision}
**Option A:** {approach 1 — with its tradeoff}
**Option B:** {approach 2 — with its tradeoff}
**Option C (optional):** {approach 3}
**The answer depends on:** {1–2 sentences explaining what makes each option right in different contexts}
```

**Speaking notes:** "I want a show of hands — who would pick A? B? ... Here's why reasonable people disagree..."

---

> 💼 **Interview / Career Callout** (inline, at least 2 per lecture)

Place these inline after key results or misconceptions — not as separate sections. Use this exact format:

> 💼 **Interview alert:** {Specific interview question or career context. E.g., "'Explain bias vs. variance' is the #1 ML screening question at tech companies."}

**Adapt by `course_category`:**

| course_category | Callout style |
|-----------------|---------------|
| `ml-stats` | Data science / ML engineer interview questions |
| `game-theory` | Management consulting case interview connections |
| `micro-theory` | PhD qualifying exam / econ PhD job market signals |
| `principles` | Economic literacy for any professional role |
| `finance` | Investment banking / asset management interview Qs |
| `general` | Consulting or policy analyst interview connections |

---

### ↔️ Before vs. After (transition lectures only)

**When to include:** If the intake flags this as a paradigm-shift or transition topic (check `depth_calibration` or `topic_title` for keywords: "shift," "introduction to," "from X to Y," "vs.").

Show the SAME data or problem analyzed both ways — the method students already know vs. the method they're learning today.

| course_category | Trigger examples |
|-----------------|-----------------|
| `ml-stats` | OLS → regularization, explanation → prediction, parametric → nonparametric |
| `game-theory` | Static → dynamic, complete → incomplete information |
| `micro-theory` | Perfect competition → monopoly, no externality → with externality |
| `principles` | Pre-tax → post-tax, pre-trade → post-trade, before/after price floor |
| `finance` | Before/after Fed intervention, pre/post rate change |

**Format:**
```
**The same problem, two approaches:**
**Before ({old method}):** {analysis + result}
**After ({new method}):** {analysis + result}
**Comparison:** {table showing which metric each method wins on}
**The insight:** {when to use which — not "new is always better" but "it depends on your goal"}
```

---

### 📊 Visual Progression Guidance

When a concept builds incrementally (bias-variance tradeoff, supply-demand equilibrium, game tree expansion), design figures as a **layered sequence** rather than standalone images:

- **Figure N-a:** Base layer only (e.g., just the training error line, or just the supply curve)
- **Figure N-b:** Add second layer (e.g., test error line, or demand curve)
- **Figure N-c:** Add annotation (e.g., shade generalization gap, mark equilibrium point)
- **Figure N-d (optional):** Add comparative shift (e.g., shift demand, mark new equilibrium)

In RevealJS slides, these become a slide sequence that builds. In lecture notes, show the final composite figure with a caption noting the build-up order.

| course_category | Example progression |
|-----------------|---------------------|
| `ml-stats` | training error → + test error → + gap shaded → + sweet spot marked |
| `game-theory` | payoff matrix → + best responses highlighted → + Nash equilibrium circled |
| `micro-theory` | budget constraint → + indifference curves → + tangency → + income effect |
| `principles` | supply curve → + demand curve → + equilibrium → + curve shift → + new equilibrium |
| `finance` | money supply → + money demand → + equilibrium rate → + Fed shifts supply |

---

## 💬 In-Class Discussion: {discussion_topic} ({N} min)

*After Section {N}*

**Setup:** {1–2 sentences setting up the discussion. What mental model should students have activated before this discussion?}

### Discussion Question A — Understanding (Bloom's Level 2)
> {Question that tests whether students understood the core concept}

**Facilitation:** {What to look for in student responses. What's a good answer? How to redirect if students go off-track.}

### Discussion Question B — Analysis (Bloom's Level 4)
> {Question that requires reasoning: comparing, distinguishing, examining}

**Facilitation:** {Expected responses. Common wrong turn and how to redirect. The key insight to draw out.}

### Discussion Question C — Evaluation (Bloom's Level 6)
> {Question that requires judgment: "Should a firm...?" "How would you design...?"}

**Facilitation:** {This question has no single right answer — guide students to consider trade-offs. Expected range of reasonable positions.}

**Time allocation:** {3–5} min | **Format:** {Think-pair-share / Open discussion / Small groups}

---

## 📊 Class Poll: {concept_being_tested}

*After {concept/section}* | **Platform:** Mentimeter / iClicker / show of hands

---

**Poll {N}a:**
{Question text}

- A) {option}
- B) {option} ✓
- C) {option}
- D) {option}

**Reveal script:** "The answer is B. Here's why: {2–3 sentence explanation}. If you chose A, you're thinking about {X} — that's actually what we covered in [prior topic], but here we have [key difference]. If you chose C or D, that's the [name of misconception] — let's unpack that..."

---

**Poll {N}b:** *(optional second poll for this section)*

{repeat pattern}

---

## 🔄 Discussion Debrief

**Key insight:** {1–2 sentences — the main idea students should have articulated or converged on}

**Bridging sentence:** *(say this exactly or paraphrase)*
> "{Sentence that connects the discussion's insight back to the formal concept we just taught. Should feel like a natural conclusion, not an abrupt pivot.}"

**Transition to next section:** "{How to segue forward. Plant a seed for the next concept.}"

---

## [Repeat Section → Discussion → Poll → Debrief pattern for each core concept]

---

## 🔗 Connections ({N} min)

### Building On
{Prior topic 1}: {One sentence reminder of the key idea students should recall. Frame it as an activation: "Remember when we showed that...?"}
{Prior topic 2}: {Activation sentence}

### Setting Up
{Future topic 1}: {1–2 sentence seed. Hint at what's coming without giving it away.}
{Future topic 2}: {Seed sentence}

---

## 🎯 Key Takeaways

Walking out of class, students should be able to complete these sentences:

1. "{Topic} is useful because..."
2. "The key assumption we need is..."
3. "In practice, firms use this method by..."
4. "The main limitation to keep in mind is..."
5. "This connects to [upcoming topic] because..."

---

## 📖 Supplementary Resources

**To go deeper:**
- [{Title}]({URL}) — {why this reading adds value beyond the lecture}
- [{Title}]({URL}) — {why}

**Video explainers:**
- [{Title — YouTube/Coursera}]({URL}) — {brief description}

**Datasets to explore:**
- [{Dataset name}]({URL}) — {what students can investigate}

---

## 📋 Appendix: Instructor Notes

### Timing Watch Points
{Sections that commonly run long and why. What to cut if time is short.}

### Frequently Asked Student Questions

**Q: {common question}**
A: {answer}

**Q: {common question}**
A: {answer}

### If Class Ends Early
{2–3 backup extension questions or deeper examples for the last 5–10 minutes}

### Errata and Updates
{Space for the instructor to note any corrections or updates after teaching}
```

---

## Quality Standards

Before finalizing the draft, verify each of the following:

**Completeness:**
- [ ] Every core concept from the brainstorm appears in the notes
- [ ] Every concept has: intuition, formal treatment, worked example, industry application, misconception
- [ ] Every equation has all terms interpreted
- [ ] Every industry example has: company, problem, method, quantified outcome, source URL
- [ ] At least 1 worked example with real numbers per lecture (🔢)
- [ ] At least 2 code-concept bridges appropriate for the course_category (💻)
- [ ] At least 2 interview/career callouts inline (💼)
- [ ] At least 1 decision scenario with 2–3 options and tradeoffs (🎯)
- [ ] If transition lecture: before/after comparison using same dataset (↔️)

**Interactive elements:**
- [ ] At least 2 Discussion blocks, each with 3 Bloom's-tiered questions
- [ ] At least 3 Poll questions with 4 options, correct answer marked, reveal scripts
- [ ] At least 2 Discussion Debrief sections with bridging sentences
- [ ] Debrief notes are specific (actual sentences, not "connect to theory")

**Sources:**
- [ ] All claims cite a named source
- [ ] All examples are 2024 or later (unless historically significant)
- [ ] All URLs are real and plausibly accessible (do not fabricate URLs)

**Style:**
- [ ] No section is just bullet points — all explanations in prose
- [ ] Speaking notes are actual sentences, not prompts
- [ ] Tone is consistent: rigorous but engaging
- [ ] Math is at the right level for the stated audience

---

## Step 5: Figure Generation

After `lecture-notes.md` is written and passes the quality checklist, generate all charts, tables, and diagrams as PNG files.

### 5.1 — Identify figures to generate

Re-read `lecture-notes.md` and collect every item that is:
- A **markdown table** already present in the notes → render as a styled image
- A **chart or graph** described in prose (e.g., "the following figure shows GDP growth over time")
- A **conceptual diagram** implied by the content (supply/demand curves, IS-LM, causal DAGs, regression scatter plots, ROC curves, confusion matrices, etc.)
- An **equation visualization** where a graph would aid understanding

Assign each a sequential number and a short slug: `figure_001_supply-demand`, `figure_002_ols-coefficients`, etc.

### 5.2 — Generate each figure

For each figure, write and execute a Python script using the project virtualenv:
```bash
VENV='/Users/openclaw/Resilio Sync/Documents/econ-lecture-plan/.venv'
$VENV/bin/python figure_script.py
```

Use these libraries as appropriate:
- **matplotlib** — curves, scatter plots, bar charts, table images (`matplotlib.table`)
- **plotly** (exported as PNG via `plotly.io.write_image`) — interactive-style charts
- **numpy/pandas** — data generation for illustrative examples
- **networkx** — causal DAGs and directed graphs

Save each figure to `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/figures/figure_NNN_slug.png` at 150 dpi minimum, 8×5 inches default size.

Example for a supply-demand diagram:
```python
import matplotlib.pyplot as plt, numpy as np
fig, ax = plt.subplots(figsize=(7, 5))
q = np.linspace(0, 10, 100)
ax.plot(q, 10 - q, label='Demand', color='steelblue', linewidth=2)
ax.plot(q, 2 + q, label='Supply', color='coral', linewidth=2)
ax.set_xlabel('Quantity'); ax.set_ylabel('Price')
ax.legend(); ax.set_title('Supply and Demand Equilibrium')
plt.tight_layout()
plt.savefig('/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/figures/figure_001_supply-demand.png', dpi=150)
plt.close()
```

### 5.3 — Insert figure references into lecture-notes.md

After all figures are generated, update `lecture-notes.md` to embed each figure at the correct location:
```markdown
![Figure 1: Supply and Demand Equilibrium](figures/figure_001_supply-demand.png)
*Figure 1: At equilibrium, quantity supplied equals quantity demanded at price P\*.*
```

Place the image reference immediately after the paragraph or equation it illustrates.

### 5.4 — Output

```
/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/figures/
├── figure_001_supply-demand.png
├── figure_002_ols-table.png
└── ...
```

`lecture-notes.md` is updated in-place with all `![Figure N](figures/...)` references inserted.
