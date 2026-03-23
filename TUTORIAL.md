# Tutorial: Preparing a Masters-Level IV Lecture in 20 Minutes

This tutorial walks through the complete pipeline using a realistic example: preparing a 75-minute lecture on **Instrumental Variables** for a master's-level Applied Econometrics course (Topic 8 of 14, presentation + lab).

You can follow along in Claude Code with your own version of this topic, or use it as a reference for understanding what each stage produces.

---

## Setup

### Install the skills

```bash
git clone https://github.com/YOUR_USERNAME/econ-lecture-prep.git
cd econ-lecture-prep
cp -R skills/* ~/.claude/skills/
```

### Open Claude Code

```bash
claude .
```

---

## Step 1: Launch the Pipeline

Type:
```
/lecture-prep
```

Claude will begin Stage 1 (Intake) and ask for your course information.

---

## Stage 1: Intake

Claude asks:

> "Let's get your lecture set up. What course is this for, and what's the topic?"

**You respond:**

> "ECON 5200: Applied Data Analytics in Economics. Topic is Instrumental Variables. It's topic 8 of 14. 75 minutes. Masters level. Presentation plus lab. Students have seen OLS, multiple regression, and we introduced DAGs last week. No slides yet — starting fresh."

**Claude parses this and confirms:**

```yaml
course_title: ECON 5200: Applied Data Analytics in Economics
topic_title: Instrumental Variables
topic_number: 8
total_topics: 14
class_length_minutes: 75
class_type: presentation + lab
audience_level: masters
prerequisites_covered:
  - OLS estimation
  - Multiple regression
  - Omitted variable bias
  - Introduction to DAGs
supporting_docs_provided: false
```

**Claude writes:** `output/econ5200-topic-08-instrumental-variables/intake.md`

> "Intake complete. Moving to brainstorm stage..."

---

## Stage 2: Brainstorm

Claude performs the following automatically:

1. **Theory extraction:** Synthesizes IV theory from Angrist & Pischke, Wooldridge, and standard masters-level treatment — appropriate for the audience.

2. **Mandatory web search:** Searches for:
   - Industry IV applications (2024–2026): finds Amazon delivery speed study, Airbnb host response time study, DoorDash promotion selection bias case
   - Recent academic updates: finds Bauer & Swanson (2023) update to Romer-Romer monetary policy IV, Lee et al. (2022) tF-statistic
   - News hooks: finds the 2024–2025 Amazon fulfillment center expansion as the opening hook

3. **Interactive element blueprint:** Designs:
   - Discussion Block 1 (after 2SLS): 3 Bloom's-tiered questions on instrument validity
   - Discussion Block 2 (after LATE): 3 questions on external validity and compliers
   - Poll 1: OLS consistency under endogeneity (expected 40% correct)
   - Poll 2: Which IV assumptions are testable? (55% expected correct)
   - Poll 3: Weak instrument decision with F=8.3 (35% expected correct)
   - Poll 4: What does IV estimate? (65% correct)

4. **Time allocation:** Allocates 75 minutes across 5 concepts, 2 discussion blocks, 4 polls, and the lab introduction.

**Claude writes:** `output/econ5200-topic-08-instrumental-variables/brainstorm.md`

> "Brainstorm complete. Moving to peer review..."

---

## Stage 3: Peer Review

Claude runs three reviewers sequentially. Here's a summary of what each finds:

### Pedagogy Expert 🎓

**Strength:** The Amazon delivery hook is compelling and creates genuine curiosity.

**Must-fix:** LATE is the most conceptually difficult concept and was allocated only 7 minutes — expand to 10.

**Should-fix:** The Level 2 discussion question about compliers needs to be more specific (add: "give me an example of a complier, always-taker, and never-taker").

### Domain Economist 📊

**Must-fix:** The LATE section didn't define monotonicity — add the Imbens & Angrist (1994) definition.

**Should-fix:** Soften the claim that "IV standard errors are always larger than OLS" — add caveat for overidentified models.

**Should-fix:** Update the Romer & Romer (2004) citation to Bauer & Swanson (2023).

### Industry Practitioner 💼

**Overall:** Job-ready.

**Should-fix:** Add a career connection sentence to the monetary policy example.

**Nice-to-have:** Add a brief mention of healthcare IV applications.

### Synthesis

- 3 must-fix items → applied immediately (LATE expanded, monotonicity added, P_Z defined)
- 6 should-fix items → applied
- 2 nice-to-have items → noted but not incorporated (time constraints)

**Claude writes:** `output/econ5200-topic-08-instrumental-variables/review-report.md`
**Claude revises:** `output/econ5200-topic-08-instrumental-variables/brainstorm.md`

> "Review complete. Moving to draft stage..."

---

## Stage 4: Draft

Claude reads the revised brainstorm and produces:

### `lecture-notes.md` — Textbook-style notes

The notes contain:
- **5 sections** with full intuition, formal treatment, industry applications, and misconceptions
- **2 Discussion blocks** with 3 questions each at Bloom's Levels 2, 4, and 6
- **4 Poll questions** with 4 options, correct answers, reveal scripts, and follow-up plans
- **2 Discussion debriefs** with bridging sentences
- **Speaking notes** throughout — actual sentences, not prompts
- **Opening hook** with Amazon delivery speed example (2024–2025 data)
- **Hook payoff** at the end closing the loop

You can see the full output in `examples/sample-lecture-output.md`.

### `lab.ipynb` — Jupyter Lab

The lab uses actual American Community Survey microdata (via IPUMS USA):
- **Part 1 (Guided):** Replicate the Angrist-Krueger quarter-of-birth IV design for returns to education
- **Part 2 (Semi-guided):** Add controls and run first-stage diagnostics
- **Part 3 (Open-ended):** Find a different instrument or apply 2SLS to FRED data

Full lab: `output/econ5200-topic-08-instrumental-variables/lab.ipynb`

**Pipeline completion message:**

```
## ✅ Lecture Prep Complete

Course: ECON 5200: Applied Data Analytics in Economics
Topic: Instrumental Variables (Topic 8 of 14)
Class type: presentation + lab
Duration: 75 minutes

Files created:
- output/econ5200-topic-08-instrumental-variables/intake.md
- output/econ5200-topic-08-instrumental-variables/brainstorm.md
- output/econ5200-topic-08-instrumental-variables/review-report.md
- output/econ5200-topic-08-instrumental-variables/lecture-notes.md
- output/econ5200-topic-08-instrumental-variables/lab.ipynb

Interactive elements generated:
- 2 discussion blocks (6 questions total, Bloom's Levels 2/4/6)
- 4 class poll questions (Mentimeter/iClicker ready)
- 2 discussion debrief sections with bridging sentences

Peer review summary:
- 3 must-fix items addressed
- 6 should-fix items addressed
- 2 nice-to-have items noted, not incorporated
```

---

## Using the Output

### Before class

1. Open `lecture-notes.md` — read the speaking notes for each section
2. Load `examples/sample-polls.md` into Mentimeter (or your polling platform)
3. Create your slides from the section headers and formal treatment boxes
4. Share the Colab link for `lab.ipynb` with students

### During class

1. Start with the hook — display the Amazon question on the projector
2. Follow the time allocation in the Appendix
3. Use `examples/sample-discussion-guide.md` (see `examples/`) as your facilitation reference
4. Run polls via Mentimeter after each major concept

### After class

Edit the `Appendix: Instructor Notes` section with actual timings and notes for next time.

---

## Standalone Commands

### Just need discussion questions for a topic?

```
/class-discussion instrumental variables endogeneity LATE
```

→ Produces 9 questions (3 per concept) with facilitation notes.

### Just need poll questions?

```
/class-poll instrumental variables
```

→ Produces 4–5 Mentimeter-ready questions with reveal scripts.

### Want a facilitation guide for an existing lecture?

```
/discussion-guide output/econ5200-topic-08-instrumental-variables/lecture-notes.md
```

→ Produces a complete facilitation guide with class flow map, facilitation scripts, and energy management notes.

### Want to update an existing lecture's interactive elements?

```
/class-discussion --enhance output/econ5200-topic-08-instrumental-variables/lecture-notes.md
```

→ Reads the notes, identifies weak or missing discussion/poll sections, and improves them.

### Want to regenerate just the brainstorm (e.g., one year later for a new semester)?

```
/brainstorm-lecture
```

→ Re-runs brainstorm using the saved intake form, searching for fresh 2025–2026 examples.

---

## Common Questions

**Q: The lecture notes are very long. Am I supposed to say all of this?**
A: No — the notes are a reference document, not a script. The speaking notes show what to say; the prose in between shows the level of depth you should convey. Teach from the speaking notes and use the prose to fill in if students ask questions.

**Q: The poll questions feel a bit hard for my class — how do I calibrate?**
A: In the intake, describe your class more specifically: "Students have very strong OLS backgrounds but have never seen IV" or "This is a practitioner-focused masters, we want intuition more than formalism." The brainstorm stage will calibrate difficulty accordingly.

**Q: What if the industry examples are behind a paywall?**
A: The brainstorm prioritizes examples with publicly accessible sources. If an example uses a paywalled paper, substitute the one from the Applications Gallery that links to a free working paper or blog post. In the IV example, the Cunningham Mixtape chapter (free online) covers Card (1995) in detail.

**Q: Can I use this for undergraduate courses?**
A: Yes — set `audience_level: advanced_undergrad` or `intro_undergrad` in the intake. The formalism, notation, and lab complexity all adjust automatically.
