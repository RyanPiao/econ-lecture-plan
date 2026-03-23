# Peer Review Methodology

## Purpose
Critically evaluate the brainstorm from three expert perspectives and produce actionable, prioritized improvements before the draft stage. The review should be rigorous enough to catch real problems — not a rubber stamp.

---

## Setup

Read both:
- `output/{slug}/intake.md` — to understand the constraints (audience level, class time, class type)
- `output/{slug}/brainstorm.md` — the document being reviewed

Run the three reviews **sequentially** in the order listed below. Each reviewer reads the full brainstorm with fresh eyes.

---

## Reviewer 1: Pedagogy Expert 🎓

**Persona:** An award-winning economics professor who studies cognitive load, active learning, and course design. Has taught classes from 30 to 300 students. Deeply practical — cares about what actually works in a room full of students.

### Review Checklist

**Cognitive Load:**
- [ ] Is the number of core concepts realistic for the class length? (Rule of thumb: no more than 1 new concept per 15 minutes for masters, 20 minutes for undergrad)
- [ ] Are there natural "cognitive pause" moments between dense sections?
- [ ] Is the working memory demand appropriate (not too many new terms introduced simultaneously)?

**Scaffolding:**
- [ ] Do concepts build properly from simple → complex?
- [ ] Is the prerequisite activation realistic? (Will students actually remember these things?)
- [ ] Is each concept's intuition established BEFORE the formalism?

**Active Learning:**
- [ ] Are there at least 2 substantive discussion blocks?
- [ ] Are poll questions at genuinely different difficulty levels?
- [ ] Are there moments where students DO something (not just listen)?
- [ ] Is the timing for discussion/polls realistic? (Discussion always takes longer than planned)

**Opening Hook:**
- [ ] Does it create genuine curiosity, or is it just a scene-setting statement?
- [ ] Does it connect to something students actually care about?
- [ ] Is the payoff (when the hook is resolved) clearly planned?

**Time Allocation:**
- [ ] Is the total estimated time within 5 minutes of the class length?
- [ ] Is Q&A buffer included (minimum 5 minutes)?
- [ ] Are transition times accounted for?

**Assessment Alignment:**
- [ ] Could a student demonstrate understanding of every listed concept after this lecture?
- [ ] Do the discussion questions actually test the learning objectives?

**Interactive Elements Quality:**
- [ ] Are discussion questions genuinely open-ended (not yes/no)?
- [ ] Do Bloom's levels 2, 4, and 6 all appear?
- [ ] Are debrief notes specific (not just "connect back to theory")?
- [ ] Are poll questions unambiguous? Could a well-prepared student answer them confidently?

### Output Format

```
## Pedagogy Review

**Overall assessment:** [Strong / Needs revision / Major concerns]

**Strengths:**
1. [Specific thing done well]
2. [Specific thing done well]

**Issues:**
| Priority | Issue | Specific Fix |
|----------|-------|-------------|
| must-fix | [issue] | [exact change needed] |
| should-fix | [issue] | [exact change needed] |
| nice-to-have | [issue] | [suggestion] |

**Interactive elements specific feedback:**
- Discussion questions: [assessment]
- Poll questions: [assessment]
- Debrief notes: [assessment]
```

---

## Reviewer 2: Domain Economist 📊

**Persona:** A PhD research economist who publishes in top general-interest journals and referee referees for AER, QJE, and ReStat. Cares deeply about precision and rigor. Impatient with hand-waving.

### Review Checklist

**Theoretical Accuracy:**
- [ ] Are all definitions correct and consistent with standard usage?
- [ ] Are all equations stated correctly?
- [ ] Are all key results stated with appropriate conditions/assumptions?
- [ ] Are proofs or derivations correct (if included)?

**Econometric Rigor:**
- [ ] If causal claims are made, is the identification strategy explained?
- [ ] Are assumptions stated before being invoked?
- [ ] Are limitations and caveats of methods mentioned?
- [ ] Is the distinction between correlation and causation maintained?

**Mathematical Level:**
- [ ] Is the formalism appropriate for the stated audience level?
- [ ] For masters: are asymptotic results stated correctly? Is matrix notation used appropriately?
- [ ] For undergrad: is the intuition precise even if the math is simplified?

**Literature Currency:**
- [ ] Are the cited papers/findings still the consensus view?
- [ ] Has the literature moved significantly since the cited work?
- [ ] Are there important recent papers (2022–2025) that should be mentioned?

**Common Misconceptions:**
- [ ] Are the listed misconceptions the ones students actually fall into?
- [ ] Are the corrections accurate?

**Notation:**
- [ ] Is notation consistent throughout?
- [ ] Does it follow field conventions?

### Output Format

```
## Domain Review

**Overall assessment:** [Rigorous / Minor issues / Needs correction]

**Errors or inaccuracies:**
| Priority | Error | Correct statement |
|----------|-------|------------------|
| must-fix | [specific error] | [corrected version] |
| should-fix | [imprecision] | [more precise version] |

**Missing nuance or caveats:**
- [Important caveat not mentioned]

**Literature updates:**
- [Paper or finding that should be referenced]

**Notation issues:**
- [Inconsistency or non-standard usage]
```

---

## Reviewer 3: Industry Practitioner 💼

**Persona:** A senior economic consultant at a top firm (McKinsey, Deloitte, Federal Reserve, tech company research team) who actively hires economics graduates. Sees hundreds of resumes. Cares about what actually differentiates candidates.

### Review Checklist

**Relevance:**
- [ ] Would a hiring manager find these examples compelling?
- [ ] Do the examples reflect how industry actually uses this method?
- [ ] Are any examples condescending or oversimplified in a way that misrepresents practice?

**Specificity:**
- [ ] Does every industry example name a specific company (not "a major tech company")?
- [ ] Do examples include specific numbers (revenue, accuracy %, cost savings)?
- [ ] Are methods described specifically (not just "machine learning" but "XGBoost with SHAP values")?

**Currency:**
- [ ] Are all examples from 2024 or later?
- [ ] Are the described tools/methods still current practice, or have they been superseded?

**Career Connection:**
- [ ] Does the lecture help students see how this topic connects to job functions?
- [ ] Is there any content that would make a student say "now I know why this matters for my career"?

**Tool Alignment (for labs):**
- [ ] Are the tools and packages ones actually used in industry?
- [ ] Is the code style professional enough to be portfolio-ready?

**Missing Applications:**
- [ ] Are there obvious industry applications that were overlooked?
- [ ] Are there sectors or use cases that would resonate strongly with this audience?

### Output Format

```
## Industry Review

**Overall assessment:** [Job-ready / Needs real-world grounding / Too academic]

**Example quality assessment:**
| Example | Assessment | Suggested improvement |
|---------|------------|----------------------|
| [Company] | [Strong/Weak/Vague] | [specific improvement] |

**Missing applications:**
- [Overlooked industry or use case]

**Currency issues:**
- [Example or tool that is outdated]

**Career connection assessment:**
- [Specific feedback on whether students will see the career relevance]
```

---

## Synthesis

After all three reviews:

### Step 1: Compile All Feedback
Aggregate all issues across the three reviewers. Assign final priority:
- `must-fix`: Any error, any accuracy issue, any content that would confuse students or misrepresent the field. If any reviewer flagged something as must-fix, it is must-fix.
- `should-fix`: Pedagogical improvements, stronger examples, better timing. Apply all of these.
- `nice-to-have`: Optional enhancements. Note but do not necessarily implement.

### Step 2: Revise the Brainstorm
Apply all `must-fix` and `should-fix` changes directly to `output/{slug}/brainstorm.md`. Track changes by adding a brief note at the top of the brainstorm:
```
<!-- Revised after peer review: {date}. Applied {N} must-fix, {N} should-fix changes. -->
```

### Step 3: Write the Review Report
Write `output/{slug}/review-report.md` using `templates/review-report.md`. Include:
- Full text of all three reviews
- Synthesis table with all issues categorized
- Summary of changes made to brainstorm
- List of `nice-to-have` items not incorporated (with brief rationale)

### Step 4: Handoff
Pass the revised brainstorm to Stage 4 (Draft). The review report is a permanent record — do not modify it after this point.
