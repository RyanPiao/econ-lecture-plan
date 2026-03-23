# Interactive Classroom Elements Methodology

## Purpose
Design high-quality interactive elements that make students think, not just listen. Good discussion questions and polls are not afterthoughts — they are the mechanism by which students build understanding rather than merely receive it.

---

## Philosophy

**Active learning is not optional.** Research consistently shows that students retain more from classes where they actively process material (discuss, answer questions, explain to peers) than from passive lectures. Every 15–20 minutes of pure lecture should be punctuated by an interactive element.

**Questions should have productive tension.** The best discussion questions have no single obvious right answer, or they have a right answer that feels wrong at first. They should make students uncomfortable enough to think but not so confused that they disengage.

**Polls reveal misconceptions, not just comprehension.** The best poll questions are ones where roughly 40–60% of students choose the wrong answer — not because students are unprepared, but because the wrong answers reflect plausible but incorrect intuitions. The reveal becomes a teaching moment.

---

## In-Class Discussion Questions

### Bloom's Taxonomy Framework

Design 3 questions per major concept, one at each cognitive level:

| Level | Bloom's Category | Verb examples | What it tests |
|-------|-----------------|---------------|---------------|
| **2** | Understanding | explain, describe, identify, summarize | Does the student understand the core idea? |
| **4** | Analysis | compare, distinguish, examine, break down | Can the student reason about the concept? |
| **6** | Evaluation/Create | evaluate, design, judge, propose, construct | Can the student apply judgment or build something new? |

### Question Design Rules

**Level 2 — Understanding:**
- Must be answerable using concepts from this lecture only
- Should not be yes/no — require a sentence or two of explanation
- Wrong: "What is OLS?" Right: "Explain in your own words why OLS minimizes squared errors rather than absolute errors. What would change if we minimized absolute errors?"

**Level 4 — Analysis:**
- Should require students to compare, contrast, or trace cause-and-effect
- Ideal structure: "What would happen if...?" or "How does X differ from Y in the context of...?"
- Wrong: "How is IV different from OLS?" Right: "Suppose you run an IV regression and find that your first-stage F-statistic is 8. Walk me through what this means for the reliability of your IV estimates, and what a critic would say about your results."

**Level 6 — Evaluation:**
- Should have genuine ambiguity — reasonable people can disagree
- Ideal structure: "Should a firm/policymaker...?" or "If you were advising [company/government], how would you...?"
- Wrong: "When should you use IV?" Right: "You're a data scientist at Uber. You want to estimate the effect of surge pricing on driver supply, but you suspect drivers who are more price-sensitive also tend to work more hours in general. Design an IV strategy to isolate the causal effect. What tradeoffs does your design make?"

### Facilitation Notes Format

For each discussion question, write:

```markdown
**Question:** {exact question text}

**Cognitive level:** Bloom's Level {2/4/6} — {Understanding/Analysis/Evaluation}

**Setup:** {1 sentence: what mental model should students have activated before this discussion?}

**Expected responses:**
- Strong answer: {what a well-prepared student says}
- Partial answer: {what a struggling student says — and how to help them}
- Common wrong turn: {the plausible mistake} → {how to redirect}

**The key insight to draw out:** {1–2 sentences: what should students understand by the end of this discussion that they might not have at the start?}

**Facilitation moves:**
- If students are silent: {specific prompt to restart conversation}
- If discussion goes off-track: {specific redirect}
- If one student dominates: {how to invite others}
- Closing move: {how to wrap up and transition}

**Time:** {3–5} minutes | **Format:** {Think-pair-share / Open / Small groups}
```

### Think-Pair-Share Protocol

For complex questions (Level 4 and 6), use Think-Pair-Share:
1. **Think (30–60 sec):** Students write their answer individually before talking
2. **Pair (1–2 min):** Students discuss with one neighbor
3. **Share (1–2 min):** Call on 2–3 pairs to share their answer

This structure prevents the "three students talk, everyone else zones out" problem.

---

## Class Poll Questions

### Design Principles

**The 40-60 Rule:** Aim for poll questions where roughly 40–60% of students initially answer incorrectly. If everyone gets it right, the question was too easy (no learning value). If almost everyone gets it wrong, the question was unclear or the concept wasn't taught.

**Four options, not five.** Four options reduces guessing noise while keeping the question tractable. Each wrong option should correspond to a specific, identifiable misconception.

**Distractor design:** Each wrong option should be tempting for a concrete reason:
- Option A: The answer students give if they half-remember the formula but misapply it
- Option C: The answer students give if they confuse this with a related concept from a prior lecture
- Option D: The answer students give if they reverse the direction of an effect

### Poll Question Format

```markdown
## Poll {N}: {concept being tested}

**Placement:** After {concept/section name} | {X} minutes into class

**Purpose:** {concept check | misconception reveal | engagement reset | synthesis}

---

**Question:**
{Clear, unambiguous question text. Avoid double negatives. Keep under 25 words.}

**Options:**
- A) {option_A}
- B) {option_B} ✓
- C) {option_C}
- D) {option_D}

**Why each wrong option is tempting:**
- A is wrong because {explanation}. Students who choose A are thinking {misconception}.
- C is wrong because {explanation}. Students who choose C are confusing this with {related concept}.
- D is wrong because {explanation}. Students who choose D are reversing the direction of {X}.

**Reveal script** *(say this after showing the answer distribution)*:
"{Exact or near-exact wording for the reveal. Should:
1. Acknowledge why wrong options were tempting
2. Explain the correct reasoning
3. Connect back to the formal concept
4. If surprising distribution: turn into discussion}"

**Follow-up:** {If > 40% wrong: pivot to mini-discussion. If results are surprising: "Interesting — let's talk about why half of you chose C..."}

**Platform notes:**
- Mentimeter: Open-ended or Word Cloud option can be used for Level 6 polls
- iClicker: Standard 4-option format
- Show of hands: Works for binary questions; use for quick checks only
```

### Poll Placement Rules

- **Do not poll** before a concept is introduced — that's a cold call, not a poll
- **Poll immediately after** you're done presenting a concept, before moving to the next one
- **Maximum 1 poll per 15 minutes** of lecture to avoid poll fatigue
- **Use polls to reset engagement** at the 45-minute mark in long classes

---

## Discussion Facilitation Guide

When `/discussion-guide` is invoked, produce a complete guide that an instructor can hold in their hand during class. Structure:

```markdown
# Discussion Facilitation Guide: {topic_title}
## {course_title} | {date} | {duration}

---

## Pre-Class Checklist
- [ ] Mentimeter/iClicker link shared with students before class
- [ ] Poll questions loaded and ready to display
- [ ] Discussion prompts available to display (or written on board)
- [ ] Timer visible to instructor

---

## Class Flow Map

| Time | Activity | Prompt/Poll | Notes |
|------|----------|-------------|-------|
| 0:00 | Opening Hook | {question} | Wait 30 sec for student responses before speaking |
| 0:07 | Section 1: {concept} | — | Introduce intuition before formalism |
| 0:20 | Poll 1 | {question} | Expected: {X}% correct |
| 0:23 | Discussion Block 1 | Level 2 → Level 4 | Start with Level 2 if energy is low |
| 0:28 | Debrief 1 | — | Bridge sentence: "{sentence}" |
| ... | ... | ... | ... |

---

## Full Discussion Scripts

### Discussion Block 1: {concept}

{Full facilitation notes for each question — see format above}

### Discussion Block 2: {concept}

{Full facilitation notes}

---

## Full Poll Scripts

### Poll 1: {topic}

{Full poll question with reveal script}

### Poll 2: {topic}

{Full poll question}

---

## Energy Management Notes

{Based on the class length and topic, specific notes on managing energy:}
- If energy drops at {X} minutes: {specific intervention — cold call, quick show of hands, partner discussion}
- If discussion is too slow: {how to accelerate}
- If discussion is too fast and you have extra time: {backup question}

---

## Closing Ritual

{Specific words to close the class with that reinforce the key takeaways and connect to next session}
```

---

## Enhancing Existing Lecture Notes

When `/class-discussion --enhance` is invoked:

1. Read the existing lecture notes file
2. Identify every major concept section (## 📚 Section N)
3. Check if it already has a Discussion block and Poll
4. For any missing or weak interactive elements:
   - Generate new questions at all three Bloom's levels
   - Generate or improve poll questions with full reveal scripts
   - Write debrief notes if missing
5. Insert the enhanced elements in the appropriate location in the notes file
6. Write the updated file back to the same path (confirm with user before overwriting)
