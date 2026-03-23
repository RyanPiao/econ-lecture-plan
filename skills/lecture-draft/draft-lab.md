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

### Cell 1: Title Block (markdown)
```markdown
# Lab {N}: {topic_title}
## {course_title}

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
jupytext --to ipynb templates/lab-notebook.py -o output/{slug}/lab.ipynb
```

When writing `output/{slug}/lab.ipynb`, produce fully executed notebook output (show results of each cell) so students can see expected output before running.
