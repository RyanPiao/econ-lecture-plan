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

**Speaking notes are sentences, not prompts:** Bad: "Discuss why IV is useful here." Good: "At this point, say: 'So why do we need instrumental variables at all? Here's the problem: if students who attend college are fundamentally different from students who don't — maybe they're more motivated, or come from wealthier families — then just comparing wages for college attendees versus non-attendees tells us about selection, not about the causal return to education. IV solves this by finding variation in college attendance that has nothing to do with those confounders.'"

---

## Document Structure

Use this exact structure for `output/{slug}/lecture-notes.md`:

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
- [ ] Every concept has: intuition, formal treatment, industry application, misconception
- [ ] Every equation has all terms interpreted
- [ ] Every industry example has: company, problem, method, quantified outcome, source URL

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
