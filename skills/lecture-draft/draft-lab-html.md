# Lab HTML Companion &mdash; Methodology

## Purpose

Every `.ipynb` lab notebook must have a companion `.html` file: a beautifully styled, student-facing version that works in any browser without Jupyter. The HTML is **not** an `nbconvert` export &mdash; it is a pedagogically enriched document with injected sections (Warning Box, AI-Assisted Expansion, Digital Portfolio) that do not exist in the notebook.

---

## When to Run

- **In pipeline:** Automatically after `.ipynb` is written and validated in Stage 5 (same `class_type` condition as lab generation).
- **Standalone:** `/draft-lab-html {base}/{slug}/` &mdash; reads existing `.ipynb`, generates `.html`.

## Input / Output

- **Input:** `{base}/{slug}/lab_{N}_{short_name}.ipynb`
- **Output:** `{base}/{slug}/lab_{N}_{short_name}.html`

Naming must match: if the notebook is `lab_18_model_evaluation.ipynb`, the HTML is `lab_18_model_evaluation.html`.

---

## Conversion Process

### Step 1: Parse the `.ipynb`

Read the notebook JSON. Walk the `cells` array. For each cell, note `cell_type` (`"markdown"` or `"code"`) and `source` (array of strings, join to get content).

### Step 2: Map Notebook Content to HTML Sections

Follow the content mapping rules below to transform cells into the HTML template sections.

#### Header
- `<h1>`: `Lab {N}: {Title from notebook's first markdown cell}`
- `<p>`: `Computational Laboratory: {Generate a descriptive subtitle from the notebook content}`

#### Section 1 &mdash; Lab Objective
- Pull from the notebook's opening markdown cell (objectives, estimated time, data source, key packages, scenario).
- Write the objective as a narrative paragraph followed by bullet-point learning outcomes.

#### Warning Box (&laquo;The Observational Challenge&raquo;)
- Identify the specific data pitfalls from the notebook (overfitting, multicollinearity, endogeneity, measurement error, imputation, selection bias, etc.).
- Write 3&ndash;5 concrete bullet points **specific to THIS lab's dataset**. Never use generic filler.

#### Section 2 &mdash; Lab Instructions
- Break the notebook into logical `<h4>` steps (Step 1, Step 2, &hellip;).
- Each step gets: a plain-English `<p>` explanation of what the code does and why, followed by the code block.
- **Preserve ALL code exactly as written in the notebook.** Do not modify, simplify, or rewrite any code.
- Observation/interpretation markdown cells from the notebook become styled callout boxes (amber/yellow background with left border).
- Use **section banners** to visually separate lab phases (see Section Banners below).

##### Cell Classification Logic

When parsing `.ipynb` code cells, classify each into one of three types:

**GUIDED** (no `TODO`, no `___`, no `&larr; YOUR CODE HERE`, no `your code here`):
- Show full code
- Style: `background-color: #272822; border-left: 4px solid #27ae60`

**EXERCISE** (contains `TODO`, `___`, `&larr; YOUR CODE HERE`, or `your code here`):
- Show scaffolding WITH `___` blanks &mdash; **NEVER** the completed answers
- Highlight blank lines with `<span style="color: #e74c3c; font-weight: bold;">`
- Add red exercise badge above the code block:
  ```html
  <div style="display: inline-block; background-color: #d41b2c; color: white; padding: 3px 10px; border-radius: 3px; font-size: 0.85em; font-weight: bold; margin-bottom: 5px;">&#9998; EXERCISE</div>
  ```
- Style: `background-color: #1a1a2e; border-left: 4px solid #d41b2c`
- Add a hint box after each exercise cell:
  ```html
  <div style="background-color: #fff3e0; border: 1px solid #ffe0b2; padding: 12px 16px; border-radius: 5px; margin: 10px 0 20px 0; font-size: 0.9em;">
      <strong>&#128161; Hint:</strong> [Function signature or pattern &mdash; NOT the full answer]
  </div>
  ```

**OPTIONAL CHALLENGE** (contains `optional`, `extension`, `challenge`, or `bonus`):
- Show minimal starter code or empty block
- Add purple badge above the code block:
  ```html
  <div style="display: inline-block; background-color: #8e44ad; color: white; padding: 3px 10px; border-radius: 3px; font-size: 0.85em; font-weight: bold; margin-bottom: 5px;">&#11088; OPTIONAL CHALLENGE</div>
  ```
- Style: `background-color: #1a1a2e; border-left: 4px solid #8e44ad`

##### Exercise Design Principle

Exercise blanks should target ONLY the key syntax takeaways:
1. Model creation &mdash; e.g., `RidgeCV(alphas=___, cv=___)`
2. Model fitting &mdash; e.g., `.fit(X_train, y_train)`
3. Metric computation &mdash; e.g., `r2_score(y_test, y_pred)`
4. Key function calls &mdash; e.g., `LassoCV(cv=5, max_iter=10_000)`

Everything else (imports, data wrangling, printing, plotting) stays as guided code. Cognitive load belongs on the econometric concepts, not Python debugging.

##### Section Banners

Add colored banners to visually separate lab phases:

```html
<!-- Guided section (green) -->
<div style="background-color: #eafaf1; border: 1px solid #b7e4c7; padding: 12px 16px; border-radius: 5px; margin: 20px 0 10px 0;">
    <strong style="color: #1e8449;">&#9654; Part N: Guided Code</strong> &mdash; Run these cells as-is. Read the code and study the output.
</div>

<!-- Exercise section (red) -->
<div style="background-color: #fdf0f0; border: 1px solid #e6b0b0; padding: 12px 16px; border-radius: 5px; margin: 30px 0 10px 0;">
    <strong style="color: #c0392b;">&#9998; Part N: Your Code</strong> &mdash; These cells have blanks you must fill in.
</div>

<!-- Written response section (purple) -->
<div style="background-color: #f3e8fd; border: 1px solid #d4b8e8; padding: 12px 16px; border-radius: 5px; margin: 30px 0 10px 0;">
    <strong style="color: #7d3c98;">&#128221; Part N: Written Responses</strong> &mdash; Answer in your notebook in complete sentences.
</div>
```

#### Written Response Questions
- If the notebook contains open-ended questions, wrap each in a light gray box (`background-color: #f9f9f9; border: 1px solid #ddd`).

#### AI-Assisted Expansion Section
- **Always generate this section**, even if the notebook doesn't have one.
- Include the "Foundations First, Expansion Second" policy statement.
- Invent a **specific, ambitious expansion task** that logically scales the lab (e.g., interactive dashboard, additional models, expanded dataset, Streamlit app).
- Write a **complete P.R.I.M.E. prompt** (Prep, Request, Iterate, Mechanism Check, Evaluate) that students can copy-paste directly into an AI assistant.
- The P.R.I.M.E. prompt must reference the specific libraries, data, and model objects from THIS lab.

#### Section 3 &mdash; Digital Portfolio
- Fill in the portfolio prompt with THIS lab's specific objective, data source, tech stack, and expected findings.
- The prompt must instruct the AI to NOT generate Python code.

#### Citations
- **Strip ALL citation markers** (e.g., `[1]`, `[2]`, bracketed numbers/symbols) from the rendered text. None may appear in the final HTML.

### Step 3: Assemble the Full HTML

Use the template at `skills/lecture-draft/templates/lab-html-template.html` as the structural reference. Replace all placeholder markers with generated content. Use **inline styles only** &mdash; no external CSS, no `<style>` blocks.

### Step 4: Write and Verify

Write the `.html` file. Verify it exists and is non-empty.

---

## HTML Template &mdash; Inline Style Reference

All HTML must use these exact inline styles. Reference `templates/lab-html-template.html` for the full skeleton.

### Color Palette
| Token | Hex | Usage |
|-------|-----|-------|
| Dark blue | `#2c3e50` | Header background, heading text, portfolio header |
| Red | `#d41b2c` | Warning border, warning heading, portfolio accent, section headings, exercise badge/border |
| Blue | `#2980b9` | AI-expansion border, AI heading |
| Green | `#27ae60` | Guided code left border |
| Purple | `#8e44ad` | Optional challenge badge/border |
| Guided code bg | `#272822` | Guided `<pre><code>` blocks (Monokai-inspired) |
| Exercise code bg | `#1a1a2e` | Exercise and optional `<pre><code>` blocks |
| Code text | `#f8f8f2` | Text inside code blocks |
| Exercise blank | `#e74c3c` | `___` blank highlight spans |
| Callout background | `#fffbea` | Observation/interpretation boxes |
| Callout border | `#f0ad4e` | Left border on observation boxes |
| Warning background | `#fff0f0` | Warning box fill |
| AI background | `#e8f4f8` | AI-expansion section fill |
| Question background | `#f9f9f9` | Written question boxes |
| Hint background | `#fff3e0` | Hint boxes after exercise cells |
| Hint border | `#ffe0b2` | Hint box border |
| Guided banner bg | `#eafaf1` | Guided section banner |
| Guided banner border | `#b7e4c7` | Guided section banner border |
| Exercise banner bg | `#fdf0f0` | Exercise section banner |
| Exercise banner border | `#e6b0b0` | Exercise section banner border |
| Written banner bg | `#f3e8fd` | Written response section banner |
| Written banner border | `#d4b8e8` | Written response section banner border |

### Font Stack
```
font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
color: #333;
line-height: 1.6;
```

### Special Characters
Use HTML entities: `&mdash;`, `&ndash;`, `&sup2;`, `&lambda;`, `&beta;`, `&alpha;`, `&sigma;`, etc. Do not use raw Unicode that might break in some browsers.

---

## Quality Checklist (run mentally before saving)

- [ ] HTML file has the same base name as the `.ipynb`
- [ ] All code blocks are **exact copies** from the notebook (no modifications)
- [ ] No citation markers (`[1]`, `[2]`, etc.) appear anywhere in the HTML
- [ ] Warning box contains 3&ndash;5 pitfalls **specific to this lab's data**
- [ ] Every code cell has a preceding `<p>` explanation
- [ ] AI-Assisted Expansion section exists with a concrete task and full P.R.I.M.E. prompt
- [ ] Digital Portfolio prompt is filled in with this lab's specific objective, data, tech, and findings
- [ ] All inline styles match the template exactly (colors match table above)
- [ ] HTML uses `&mdash;`, `&ndash;`, `&sup2;`, `&lambda;` etc. for special characters
- [ ] No external CSS, no `<style>` blocks &mdash; inline styles only
- [ ] Token-efficient: no unnecessary whitespace or comments in the HTML output
- [ ] &ldquo;How This Lab Works&rdquo; legend appears right after the header
- [ ] Every GUIDED cell has green left border (`#27ae60`) on `#272822` background
- [ ] Every EXERCISE cell has red left border (`#d41b2c`) on `#1a1a2e` background + red badge
- [ ] Exercise cells show `___` blanks &mdash; NEVER the completed answers
- [ ] Blank lines wrapped in `<span style="color: #e74c3c; font-weight: bold;">`
- [ ] Each exercise cell has a hint box immediately after it
- [ ] Section banners separate Guided / Exercise / Written phases
