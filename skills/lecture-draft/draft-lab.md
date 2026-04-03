# Jupyter Lab Methodology

## Purpose
Create a hands-on computational lab that reinforces the lecture concepts through real data and real code. The lab should be independent enough that students can complete it outside class, but guided enough that they don't get lost.

---

## Lab Design Principles

1. **Theory → Code → Interpretation cycle.** Every code block is surrounded by:
   - *Before*: A markdown cell explaining what we're about to do and why (connecting to lecture theory)
   - *After*: A markdown cell interpreting the results (connecting back to concepts)

2. **Real data only.** The main exercises must use actual datasets. Simulations are acceptable only for illustrating statistical properties (e.g., bias, consistency, power), not for the primary analysis.

3. **Progressive difficulty:**
   - Part 1: Fully guided — all code provided, students run and interpret
   - Part 2: Semi-guided — function stubs and scaffolding, students complete the logic
   - Part 3: Open-ended — a question that requires independent choices of method, dataset, or interpretation

4. **Portfolio-ready code.** Clean variable names, proper docstrings on custom functions, publication-quality figures. A student should be able to put this notebook in their GitHub portfolio.

5. **Stack selection:**
   - Default: Python + Jupyter (pandas, statsmodels, scikit-learn, plotly, matplotlib)
   - Use Plotly for all interactive figures; matplotlib/seaborn for static/publication figures
   - Include Streamlit only when the topic specifically benefits from real-time parameter exploration (e.g., bias-variance tradeoff, regularization paths)

---

## Data Sourcing Protocol

Choose the most appropriate data source for the topic. Include the full download code in the notebook so the lab is self-contained.

```python
# Priority order:
# 1. FRED API (macroeconomic time series)
import fredapi
fred = fredapi.Fred(api_key='YOUR_FRED_API_KEY')

# 2. World Bank API (cross-country data)
import wbgapi as wb

# 3. Direct URL download (Kaggle, government portals, research data)
import requests, io
url = "https://..."
df = pd.read_csv(io.StringIO(requests.get(url).text))

# 4. yfinance (financial market data)
import yfinance as yf

# 5. Fallback: include a CSV in the repo (for when APIs are down during class)
# df = pd.read_csv('data/fallback_{topic}.csv')
```

**Always include a fallback CSV path**, commented out, in case APIs are unavailable during class.

---

## Notebook Structure

### Lab Filename Convention
`lab_{N}_{short_name}.ipynb` — where `{N}` is the topic number and `{short_name}` is a brief snake_case descriptor (2-4 words max).

Examples: `lab_15_polynomial_trap.ipynb`, `lab_17_logistic_regression.ipynb`, `lab_18_model_evaluation.ipynb`

The HTML companion uses the same name: `lab_{N}_{short_name}.html`

### Solutions Notebook

After writing the student version, produce a **solutions key** with all `___` blanks filled in and all cells executed:

- **Filename:** `solutions/lab_{N}_{short_name}_solutions.ipynb`
- **Content:** Identical to student version but with all TODO/blanks completed with correct answers
- **Outputs:** All cells executed so expected outputs are visible
- **Location:** `{base}/{slug}/solutions/` subfolder (not distributed to students)

The solutions notebook is the instructor's answer key for grading and in-class walkthroughs.

### Cell 1: Title Block (markdown)
**IMPORTANT:** Do NOT include the course title (e.g., "ECON 3916" or "ECON 5200") in the notebook. The same lab is used across multiple course sections. Use only the topic title.

```markdown
# Lab {N}: {topic_title}

**Objectives:** By the end of this lab, you will be able to:
1. {hands-on objective 1 — implement/calculate/estimate}
2. {hands-on objective 2 — interpret/visualize/compare}
3. {hands-on objective 3 — extend/apply independently}

**Estimated time:** {X} minutes
**Data source:** {source name with URL}
**Key packages:** {list}
```

### Cell 2: Setup
```python
# -----------------------------------------------------------
# SETUP — Run this cell first. Install any missing packages.
# -----------------------------------------------------------

# Uncomment if running for the first time:
# !pip install pandas numpy statsmodels scikit-learn plotly fredapi wbgapi yfinance

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression, Ridge, Lasso
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

print("Setup complete ✓")
```

### Cells 3+: Part 1 — Guided Walkthrough

**Pattern for each sub-section:**

```python
# ============================================================
# PART 1: {Concept from Lecture}
# ============================================================
```

*Markdown before code cell:*
```markdown
## Part 1: {concept_title}

### What we're doing and why

{2–3 paragraphs connecting this exercise to the lecture theory.
Reference the specific equation or concept by name.
Explain what we expect to find and why.}

### The data

{Description of the dataset: what each variable represents,
units, time period, source. Why is this dataset appropriate
for illustrating this concept?}
```

*Code cell — deeply commented:*
```python
# Step 1: Load data
# We use {dataset} because {reason it's appropriate for this concept}
df = pd.read_csv(...)  # or API call

# Step 2: Inspect the data
# Always look at your data before modeling — never skip this
print(df.describe())
print(f"\nObservations: {len(df)}")
print(f"\nMissing values:\n{df.isnull().sum()}")

# Step 3: {Main estimation/calculation}
# Here we're implementing {equation from lecture, e.g., "the OLS estimator β = (X'X)^{-1}X'y"}
# Note that statsmodels includes an intercept automatically when using 'add_constant'
X = sm.add_constant(df[['var1', 'var2']])  # Design matrix
y = df['outcome']
model = sm.OLS(y, X).fit(cov_type='HC3')  # HC3 robust standard errors (always)
print(model.summary())
```

*Markdown after code cell (interpretation):*
```markdown
### What we found

{2–4 sentences interpreting the output. Connect back to theory.
Do the numbers make sense? What's the economic magnitude?
What would this coefficient mean in practice?}

**Key number to focus on:** The coefficient on `{variable}` is {value},
meaning {plain-language interpretation with units}.

**Does this match our intuition?** {Yes/No/Partially, and why}
```

### Final Cells: Part 3 — Open-Ended Extensions

```markdown
## Part 3: Try It Yourself

Now apply what you've learned independently. These extensions don't have a single right answer —
the goal is to practice making methodological choices and justifying them.

### Extension A (Guided)
*Change one thing and predict what happens before you run the code.*

{Specific instruction: e.g., "Rerun the regression in Part 2 but add [control variable].
Does the coefficient on [main variable] change? Why or why not?"}

### Extension B (Semi-guided)
*Apply the same method to a different context.*

{Dataset suggestion and question: e.g., "Use the World Bank data below to examine
[related question]. You'll need to decide how to handle [methodological choice]."}

```python
# Starter code for Extension B — complete the TODO sections
import wbgapi as wb
df_wb = wb.data.DataFrame(...)  # Fill in the indicator codes

# TODO: Apply {method} to this new dataset
# TODO: Interpret your findings
```

### Extension C (Open-ended)
*Bring your own data.*

{Open question: e.g., "Find a dataset where you would want to use [this method].
What business or policy question would you answer?
What challenges would you face?
Submit your notebook with at least one complete analysis."}
```

---

## Code Style Standards

**Variable naming:**
```python
# Good: descriptive, snake_case
wage_data = pd.read_csv(...)
ols_results = sm.OLS(y, X).fit()
iv_first_stage = sm.OLS(X_endog, Z).fit()

# Bad: cryptic abbreviations
d = pd.read_csv(...)
r = sm.OLS(y, X).fit()
```

**Standard errors:**
Always use HC3 heteroskedasticity-robust standard errors for OLS:
```python
model = sm.OLS(y, X).fit(cov_type='HC3')
# Or for clustered SEs:
model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': df['group_var']})
```

**Figure standards (Plotly):**
```python
fig = px.scatter(
    df, x='xvar', y='yvar',
    labels={'xvar': 'X variable label (units)', 'yvar': 'Y variable label (units)'},
    title='Descriptive title: what this shows',
    trendline='ols'
)
fig.update_layout(
    template='plotly_white',
    font=dict(size=12),
    title_font_size=16
)
fig.show()
```

**Docstrings for custom functions:**
```python
def estimate_iv(df, outcome, endog, instrument, controls=None):
    """
    Estimate a 2SLS instrumental variables regression.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset containing all variables
    outcome : str
        Name of the dependent variable
    endog : str
        Name of the endogenous regressor
    instrument : str
        Name of the excluded instrument
    controls : list of str, optional
        Names of exogenous control variables

    Returns
    -------
    RegressionResultsWrapper
        Fitted IV model with HC3 robust standard errors
    """
```

---

## Lab → Jupyter Conversion

The lab skeleton is written as `templates/lab-notebook.py` using jupytext format (percent format: `# %%` cells). Convert to `.ipynb` with:

```bash
jupytext --to notebook lab-notebook.py
# Or directly:
jupytext --to ipynb templates/lab-notebook.py -o /Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/lab_{N}_{short_name}.ipynb
```

When writing `/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/lab_{N}_{short_name}.ipynb`, produce fully executed notebook output (show results of each cell) so students can see expected output before running.

## ⚠️ Critical: Validate JSON after writing lab_{N}_{short_name}.ipynb

Jupyter notebooks are JSON files. Any literal `"` double-quote inside a markdown cell source string MUST be escaped as `\"`, or the file will be corrupted and unopenable in VS Code and Colab.

**Common failure:** markdown cells with quoted speech inside italics, e.g.:
```
*"Your model proves X is irrelevant"*   ← the " breaks the JSON string
```

**After writing lab_{N}_{short_name}.ipynb, always run:**
```bash
python3 -c "import json; json.load(open('/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/{slug}/lab_{N}_{short_name}.ipynb')); print('✓ valid JSON')"
```

If invalid, the error message shows the exact line number. Fix by escaping bare `"` as `\"` inside the JSON string. Re-validate before proceeding.

## ⚠️ Lab Execution Validation

After JSON validation passes, execute the notebook end-to-end to verify all cells run without errors:

```bash
cd "{base}/{slug}"
jupyter nbconvert --to notebook --execute lab_{N}_{short_name}.ipynb \
  --output lab_{N}_{short_name}_executed.ipynb \
  --ExecutePreprocessor.timeout=120 \
  --ExecutePreprocessor.kernel_name=python3 2>&1
```

**If execution succeeds:** Replace the original with the executed version (which includes cell outputs). Students will see expected outputs before running. Print: "✓ Lab notebook executed successfully — all cells ran, outputs embedded."

**If execution fails:** Print the error, identify the failing cell, fix the code, and re-execute. Do not proceed to the HTML companion until the notebook runs cleanly.

**If `jupyter nbconvert --execute` is unavailable** (missing package): Note "⚠️ Lab not auto-executed. Manual execution required before teaching." and proceed — do not block the pipeline.

**Exercise cells with `___` blanks:** These will fail during execution (by design — students fill them in). Before executing, temporarily replace `___` with valid placeholder values, execute, then restore the blanks. Or skip execution of exercise cells by marking them with `# SKIP_EXECUTION` and using `--ExecutePreprocessor.allow_errors=True`.
