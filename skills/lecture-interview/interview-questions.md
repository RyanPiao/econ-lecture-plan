# Interview Questions — Methodology

## Purpose

Generate a bank of technical interview questions that a student who mastered this lecture topic should be able to answer confidently. Questions must reflect what is actually asked in interviews at the jobs Northeastern economics/data students take: data science, business/econ consulting, quant research, ML engineering, PM (technical), and policy analysis roles.

---

## Step 1: Detect applicability

Check `course_title` and `topic_title` from `intake.md` for keywords:
`econometrics`, `statistics`, `statistical`, `data`, `machine learning`, `ML`, `regression`, `classification`, `causal`, `inference`, `panel`, `time series`, `forecast`, `clustering`, `neural`, `NLP`, `analytics`, `quantitative`

If no keywords match: output "Interview questions: not applicable for this topic." and stop.

---

## Step 2: Extract core concepts from lecture-notes.md

Read `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/lecture-notes.md`.

Extract:
- The 3–5 most important concepts covered (the ones that appear in section headings + equations)
- Key formulas, estimators, or algorithms introduced
- The main assumption(s) the method relies on
- The canonical real-world use case(s) shown in the lecture
- The most common student misconceptions flagged in Discussion Debriefs

---

## Step 3: Generate questions in 5 categories

Produce 12–18 questions total distributed across these categories. Every question must follow the format below.

---

### Question format

```
**Q{N}: {The exact question as asked in an interview}**
*Difficulty:* ⭐ Screener | ⭐⭐ Onsite | ⭐⭐⭐ Senior
*Applicable roles:* {subset of: Data Scientist · Economist/Analyst · Quant Researcher · ML Engineer · Consulting Analyst · PM (Technical) · Policy Analyst}

**Key points to hit:**
- {Point 1}
- {Point 2}
- {Point 3}
- {Point 4 if needed}

**Common mistake:** {What a weak candidate says — the typical wrong or incomplete answer}
```

---

### Category A: Concept & Intuition (3–4 questions) ⭐–⭐⭐

Questions that test whether the candidate can explain the core idea clearly without jargon. The "explain it to a PM / non-technical stakeholder" category.

Examples of question types:
- "Walk me through how [method] works in plain English."
- "What is the difference between [X] and [Y]?"
- "Why would you use [method] instead of [simpler alternative]?"
- "What does [key quantity] actually tell you?"

---

### Category B: Technical Implementation (3–4 questions) ⭐⭐–⭐⭐⭐

Questions that test mathematical or coding depth. Expect Masters-level answer quality.

Examples:
- "Derive [estimator] from first principles."
- "Write pseudocode / Python code to implement [method]."
- "How do you interpret the output of [model/table]?"
- "What does the coefficient on [variable] mean in this context?"
- "How do you choose [hyperparameter / bandwidth / lag length]?"

---

### Category C: Assumptions & Edge Cases (3–4 questions) ⭐⭐–⭐⭐⭐

Questions that test whether the candidate knows when the method breaks and how to diagnose problems.

Examples:
- "What are the key assumptions of [method]? Which is hardest to satisfy?"
- "What happens to your estimates if [assumption] is violated?"
- "How would you test whether [assumption] holds in practice?"
- "Your [estimator] is giving unexpected results. What do you check first?"
- "When should you NOT use [method]?"

---

### Category D: Case Study / Applied (3–4 questions) ⭐⭐–⭐⭐⭐

Scenario-based questions connecting the method to a business, policy, or research problem. Tie to the job contexts from this course (consulting, data science, policy, PM).

Examples:
- "A company wants to know if [intervention] caused [outcome]. How would you design the analysis?"
- "You have [messy real-world dataset]. How do you apply [method] here?"
- "Your manager says the model is predicting well but the coefficients don't make sense. What's going on?"
- "How would you explain the result of this analysis to a non-technical client?"

Use Boston/local context where natural (e.g., Boston Fed, Massachusetts policy, local firms).

---

### Category E: Quick-Fire Screener (3–5 short Q&A pairs) ⭐

Short answer Q&A pairs that appear in 30-minute phone screens. Answer in 1–2 sentences maximum.

Format:
```
**Q:** {Question}
**A:** {Model answer — 1–2 sentences}
```

---

## Step 4: Write output file

**Path:** `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/interview-questions.md`

**File header:**
```markdown
# Technical Interview Questions: {topic_title}

**Course:** {course_title}
**Applicable roles:** Data Scientist · Economist/Analyst · Quant Researcher · ML Engineer · Consulting Analyst · PM (Technical) · Policy Analyst
**Generated:** {date}

> These questions reflect what is actually asked in technical interviews at firms hiring Northeastern economics and data graduates: consulting (McKinsey, Cornerstone, Analysis Group), tech (Meta, Amazon, Google), finance (Two Sigma, Citadel, Goldman), and policy (Fed, CBO, state agencies).
```

Then output all 5 categories in order (A through E).

---

## Step 5: Confirm

Print: `📋 Interview questions saved: interview-questions.md ({N} questions across 5 categories)`
