# Brainstorm Methodology

## Purpose
Transform the structured intake into a rich, organized brainstorm that serves as the blueprint for the final lecture. The brainstorm must be comprehensive enough that Stage 4 (Draft) can produce polished lecture notes without any additional research.

---

## Process

### Step 1: Read Intake

Load `output/{slug}/intake.md`. Extract:
- `class_type`, `class_length_minutes`, `audience_level`
- `topic_title`, `topic_number`, `total_topics`
- `supporting_docs_summary` and `flagged_outdated_examples`
- `key_prior_concepts_to_activate` and `upcoming_topics_to_seed`

### Step 2: Theory Extraction

**If supporting documents were provided:**
Use the theoretical framework extracted during intake. Preserve the document's logical sequence. Use the same notation as the source material unless it is non-standard or pedagogically confusing.

**If no documents were provided:**
Synthesize the theoretical foundation using authoritative textbook-level treatment. Select the appropriate canonical source for the topic:
- Microeconomics: Mas-Colell/Whinston/Green, Varian
- Macro: Romer, Acemoglu
- Econometrics: Wooldridge, Angrist & Pischke, Hansen
- ML/Statistics: Hastie/Tibshirani/Friedman, Bishop
- Development: Banerjee & Duflo, Deaton
- Labor: Borjas, Card
- Industrial Organization: Tirole, Sutton

For masters-level, include the mathematical derivation. For advanced undergrad, include the result with intuition but skip the full proof. For intro undergrad, use graphical and intuitive treatment only.

### Step 3: Mandatory Web Search (Always Run)

**ALWAYS search the web**, even if supporting documents were provided. This step cannot be skipped.

Search for each of the following, targeting 2024–2026 sources:

**A. Industry case studies**
Query: "{topic_title} industry application case study 2024 OR 2025 site:hbr.org OR site:mckinsey.com OR site:deloitte.com OR site:wsj.com OR site:ft.com"
- Find named companies with concrete applications
- Record: company name, business problem, method used, outcome, source URL

**B. Recent data and statistics**
Query: "{topic_title} data statistics 2024 2025 FRED OR "World Bank" OR BLS OR OECD OR Kaggle"
- Get actual numbers, not hypotheticals
- Include dataset name and access URL

**C. News hook**
Query: "{topic_title} economics news 2024 2025"
- Find a story students would discuss over coffee
- Must be recent enough to feel current in a classroom today

**D. Academic updates**
Query: "{topic_title} NBER working paper 2024 OR 2025"
- Any recent research updating or challenging the standard treatment

**E. If supporting docs had flagged outdated examples:**
For each `flagged_outdated_example`, search for the 2024–2026 equivalent and replace silently.

**Source credibility hierarchy** (use only these sources):
1. Government/institutional data: FRED, BLS, Census, World Bank, OECD, IMF
2. Peer-reviewed journals + NBER/CEPR working papers
3. Industry reports: McKinsey, Deloitte, Fed regional banks, BCG
4. Major financial press: FT, WSJ, Bloomberg, The Economist
5. Company earnings reports, SEC filings, official press releases
6. Quality tech/business press: HBR, MIT Tech Review, Wired (data stories)

**Never use:** Blog posts without institutional backing, Wikipedia as a primary source, social media posts, or unverifiable claims.

### Step 4: Structure the Brainstorm

Produce a document using `templates/brainstorm-output.md` with exactly these sections:

---

#### Section A: Opening Hook (target: 5–8 minutes)
Write a compelling real-world question or scenario that makes students lean in. Requirements:
- Uses 2024–2026 data or events (not hypothetical)
- Connects to students' lives, career aspirations, or current news
- Poses a genuine puzzle that the lecture's content will resolve
- Opens a loop (creates curiosity) that closes at the end of the lecture

Include: the hook narrative, the question posed to students, and the "reveal" timing (when in the lecture the hook pays off).

#### Section B: Core Concepts (non-negotiable content)
List every concept the lecture MUST cover. For each:
- One-sentence plain-language definition
- The key equation, graph, or diagram
- One sentence on WHY it matters (practical stakes)
- Estimated teaching time in minutes
- Prerequisite concept to activate before introducing this one

Order concepts in pedagogical sequence: simple → complex, intuition → formalism.

#### Section C: Detailed Content per Concept
For EACH concept in Section B, provide all four layers:

1. **Intuition first** — Plain-language explanation a smart undergraduate would immediately grasp. Use analogies. Build from what students already know. Write this as if explaining to a curious, intelligent non-economist.

2. **Mathematical mechanics** — The formal treatment appropriate for the audience level:
   - Intro undergrad: graphs, simple algebra, no calculus
   - Advanced undergrad: standard econometric notation, calculus where needed
   - Masters: full derivations, matrix notation, proofs of key results, asymptotic theory

3. **Industry "why"** — Concrete example of how practitioners apply this concept. Must include: company or institution name, the specific business problem, the method applied, the quantified outcome (revenue, accuracy, cost savings, etc.), and a citation.

4. **Common misconceptions** — What do students typically get wrong with this concept? State the misconception, explain why it's wrong, and give the correction.

#### Section D: Interactive Elements Blueprint
Plan the interactive elements BEFORE drafting the lecture (so they can be integrated naturally, not bolted on):

**In-Class Discussion Questions** — for each major concept, write 3 discussion questions at different cognitive levels:
- **Level 2 (Understanding)**: "Can you explain why...?" — tests basic comprehension
- **Level 4 (Analysis)**: "What would happen if...?" "How does X compare to Y?" — tests deeper reasoning
- **Level 6 (Evaluation/Creation)**: "How would you design...?" "Should a firm/policymaker...?" — tests synthesis and judgment

For each question, also write:
- Expected student responses (2–3 good answers and 1–2 common wrong answers)
- Facilitation note: how to guide the discussion to the key insight
- Time allocation: 3–5 minutes per discussion

**Class Poll Questions** — write 3–5 multiple-choice questions for Mentimeter/iClicker:
For each poll question:
- The question text (clear, unambiguous)
- 4 answer options (A, B, C, D) — one clearly correct, others plausibly wrong
- Mark the correct answer with ✓
- Explanation of why each wrong answer is tempting (and why it's wrong)
- Placement in lecture: which concept does this poll follow?
- Purpose: concept check | misconception reveal | discussion trigger | engagement reset

**Discussion Debrief Notes** — for each discussion block, write how to close it:
- The key insight students should have reached
- A "bridging sentence" that connects the discussion back to the formal concept
- How to transition to the next section

#### Section E: Real-World Applications Gallery
Provide 3–5 substantial industry examples with ALL of the following:
- Company/institution name and sector
- The specific business problem or policy question
- The exact econometric or ML method used (not just "regression")
- The quantified outcome: numbers, percentages, dollar amounts
- Why this example is interesting to a 22-year-old student
- Source URL and date

#### Section F: Time Allocation
Break the class length into segments. Account for:
- Opening hook (target 5–8 min)
- Each core concept (estimate from Section B)
- Transition time (1–2 min between major sections)
- Each discussion block (3–5 min per question)
- Each poll (2–3 min including response + brief debrief)
- Lab setup if applicable (5–10 min)
- Q&A buffer (5–10 min at end)

If total estimated time exceeds class length:
- Mark which content is "core" (cannot cut)
- Mark what can move to supplementary reading
- Mark what can be condensed

#### Section G: Connections
**Backward links:** Which prior topics does this build on? List 2–3 specific concepts students should recall. Write a one-sentence "activation" reminder for each.

**Forward links:** What upcoming topics does this set up? Plant 1–2 curiosity seeds at appropriate moments in the lecture.

#### Section H: Supplementary Resources
- 2–3 recommended readings accessible to the audience level (with URLs)
- 1–2 excellent video explainers if they exist (YouTube, Coursera, 3Blue1Brown, etc.)
- Relevant public datasets students can explore independently (with access URLs)
- Optional: a related NBER working paper for ambitious students

#### Section I: Lab Design (only if class_type includes lab)
Pre-plan the Jupyter lab before drafting:
- Dataset: what real data will students use? (FRED, World Bank, Kaggle — include access method)
- Learning arc: what does the student DO at each stage? (guided → semi-guided → open-ended)
- Core coding exercise: what is the main task?
- Extension exercise: what do fast students do?
- Expected outputs: what should the final notebook look like?
- Common errors to anticipate

---

### Step 5: Quality Check

Before writing the brainstorm document, verify:
- [ ] All industry examples are from 2024 or later (unless historically significant)
- [ ] All industry examples name a specific company and include numbers
- [ ] Every core concept has a misconception entry
- [ ] Discussion questions cover all three Bloom's levels
- [ ] At least 3 poll questions are fully written with 4 options each
- [ ] Time allocations sum to class_length_minutes (±5 minutes)
- [ ] All sources are citable (not Wikipedia, not anonymous blogs)

### Step 6: Write Output

Write the completed brainstorm to `output/{slug}/brainstorm.md` using `templates/brainstorm-output.md`.

Confirm: "Brainstorm saved to output/{slug}/brainstorm.md. [If standalone: run /review-lecture to continue. | If pipeline: proceeding to peer review...]"
