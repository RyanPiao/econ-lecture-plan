# Best Practices for econ-lecture-prep

## Getting the Best Output

### 1. Provide the Topic Number and Total

`Topic 8 of 14` is far more useful than just `Topic 8`. The position tells Claude how much prior knowledge to assume, how much to cross-reference prior material, and whether to emphasize synthesis or foundations.

### 2. Upload Supporting Materials When You Have Them

If you have existing slides, a textbook chapter, or lecture notes, upload them. Claude will extract the theoretical framework (preserving your preferred notation) and replace only the outdated examples. This is much faster than synthesizing from scratch.

What to upload:
- Your existing lecture slides (PDF, PPTX description, or text)
- Relevant textbook chapter pages (paste text or describe the content)
- Problem sets from prior years (reveals what you've emphasized in the past)

### 3. Specify the Audience Level Precisely

The three levels produce dramatically different output:

| Level | Formalism | Example type | Lab complexity |
|-------|-----------|-------------|----------------|
| `intro_undergrad` | Graphs, basic algebra | Consumer products, everyday decisions | Very guided, minimal code |
| `advanced_undergrad` | OLS notation, calculus | Industry datasets, policy | Guided with extensions |
| `masters` | Full derivations, matrix notation, asymptotics | Research papers, consulting | Semi-guided to open-ended |

Do not use `masters` for an advanced undergrad class — the formalism level will be wrong and students will feel overwhelmed.

### 4. Specify Class Type — It Changes Everything

`presentation + lab` produces two files and a very different brainstorm (lab design, dataset selection, coding exercises). If you choose this, allow extra time in the pipeline (the lab design and drafting adds 10–15 minutes).

### 5. Let the Pipeline Run Without Interruption

`/lecture-prep` is designed to run all 4 stages without stopping. Don't interrupt it between stages unless you see a fundamental problem. The peer review stage will catch errors and improve weak content — trust the process.

If you want to iterate, run individual stages after the pipeline completes:
- `/brainstorm-lecture` — regenerate the brainstorm with different framing
- `/review-lecture` — re-review after you've manually edited the brainstorm
- `/draft-lecture` — re-draft without re-running the whole pipeline

---

## Working With the Output

### Editing Lecture Notes

The output in `output/{slug}/lecture-notes.md` is a starting point, not a final product. Common edits:
- Adjust speaking notes to match your personal teaching style
- Replace an industry example with one more familiar to your specific student population
- Tighten time estimates based on your knowledge of how long your class takes to discuss

### Adding Slides

The lecture notes are not slides — they're the content that goes behind slides. A typical workflow:
1. Generate `lecture-notes.md` via the pipeline
2. Create slides from the notes: each `## Section` becomes a slide deck section; `### Formal Treatment` content goes on 2–4 slides; industry applications get one visual slide each
3. Keep the full notes as your personal reference during lecture

### Using the Lab in Google Colab

If students use Colab rather than local Jupyter:
1. Convert the `.ipynb` to a Colab-shareable link (upload to Google Drive → Get link)
2. Add a first cell with `!pip install` for any non-standard packages
3. Replace FRED API calls with direct URL downloads or pre-loaded CSV (many datasets are available as static URLs)

---

## Common Issues

### "The examples feel generic"

The brainstorm stage searches for industry examples, but the specificity depends on how well-documented the topic is online. For niche topics:
- After the brainstorm, tell Claude: "The example for [concept] feels generic. Search for a more specific 2024 case study from [sector]."
- Or provide a specific example you know from your research and ask Claude to incorporate it.

### "The time allocation doesn't add up"

Generating realistic time allocations for a topic Claude doesn't know your specific students is hard. After your first time teaching from the notes:
- Add a note to the `Appendix: Instructor Notes` section with actual timings
- Use `/brainstorm-lecture` to regenerate with your noted timings as an input

### "The formalism is wrong for my course"

The audience level setting (`intro_undergrad` / `advanced_undergrad` / `masters`) controls formalism, but your course may not fit neatly. In the intake, add:
- "Students have seen OLS but not MLE"
- "This is a practitioner-focused masters, skip proofs but keep rigor"
- "Students are familiar with Python but not econometric packages"

### "I want to re-use a brainstorm but update the examples"

Edit `output/{slug}/brainstorm.md` directly to change or annotate what you want updated. Then run `/draft-lecture` to re-draft from the edited brainstorm without re-running the full pipeline.

---

## Workflow for Recurring Courses

If you teach the same course repeatedly:

1. **First time:** Run `/lecture-prep` for every lecture. Keep all output in `output/`.
2. **Next semester:** For each lecture, run just `/brainstorm-lecture` to refresh examples (the theoretical framework stays stable; examples become one year staler each year). Then run `/draft-lecture` to update the notes.
3. **Quick update:** For a single stale example, use `/class-discussion [topic]` to generate fresh discussion questions, or ask Claude directly: "Update the industry example in section 2 of [file] with a 2025 equivalent."

---

## Tips for Interactive Elements

### Polls
- Load all poll questions into Mentimeter or iClicker before class, not during.
- The "expected % correct" notes in the poll template are rough estimates — your class may differ. Calibrate over time.
- If >60% get a poll question wrong, spend an extra 2 minutes on the reveal — it's a learning moment, not a failure.

### Discussions
- The Bloom's Level 2 question is your safety net if students seem confused or energy is low. It's guaranteed answerable by a prepared student.
- Think-pair-share prevents the "three students talk, everyone else zones out" dynamic. Default to it for Level 4+ questions in large classes.
- Always have the "If no one responds" prompt ready — don't stand in silence for more than 15 seconds before using it.

### Timing
- Add 30% buffer to all discussion time estimates. Discussions almost always take longer than planned.
- Polls typically take 2–3 minutes including launch, response time, and reveal. Budget accordingly.
