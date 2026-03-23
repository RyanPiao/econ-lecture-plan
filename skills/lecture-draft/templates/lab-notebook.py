# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Lab {lab_number}: {topic_title}
# ## {course_title}
#
# **Objectives:** By the end of this lab, you will be able to:
# 1. {hands_on_objective_1}
# 2. {hands_on_objective_2}
# 3. {hands_on_objective_3}
#
# **Estimated time:** {estimated_minutes} minutes
# **Data source:** [{data_source_name}]({data_source_url})
# **Key packages:** {key_packages}

# %% [markdown]
# ---
# ## Setup
#
# Run the cell below to install and import all required packages.
# If running on Google Colab, uncomment the `!pip install` lines.

# %%
# Uncomment to install missing packages:
# !pip install pandas numpy statsmodels scikit-learn plotly fredapi wbgapi yfinance jupytext

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Optional — uncomment based on topic:
# import fredapi
# import wbgapi as wb
# import yfinance as yf
# from sklearn.linear_model import Ridge, Lasso, ElasticNet
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import cross_val_score, KFold

print("Setup complete ✓")

# %% [markdown]
# ---
# ## Part 1: {part_1_title} — Guided
#
# ### Background
#
# {2–3 paragraph connection to lecture theory. Reference the specific concept or equation
# by name. Explain what we expect to find and why. Include the relevant equation in LaTeX:}
#
# $$
# {key_equation}
# $$
#
# Where {term_1} is {interpretation_1}, {term_2} is {interpretation_2}.
#
# ### The Data
#
# We use **{dataset_name}** — {description: what the dataset contains, units, time period}.
# This dataset is appropriate for this lab because {reason it illustrates the concept}.

# %%
# =============================================================================
# STEP 1: Load Data
# =============================================================================
# We use {dataset_name} because {reason it's the right dataset for this concept}.
# Source: {url}

# --- Option A: Load from API ---
# Uncomment and add your API key if using FRED:
# import fredapi
# fred = fredapi.Fred(api_key='YOUR_FRED_API_KEY')
# series_id = '{FRED_series_id}'  # e.g., 'UNRATE' for unemployment rate
# df_raw = fred.get_series(series_id, observation_start='2015-01-01')
# df = pd.DataFrame({'date': df_raw.index, 'value': df_raw.values})

# --- Option B: Load from URL ---
# url = '{dataset_url}'
# df = pd.read_csv(url)

# --- Fallback: Load from local CSV (if API/URL unavailable) ---
# df = pd.read_csv('data/fallback_{topic_slug}.csv')

print(f"Dataset shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")

# %%
# =============================================================================
# STEP 2: Inspect the Data — NEVER skip this step
# =============================================================================
# Before modeling, always look at your data:
# - Check for missing values
# - Check the distribution of key variables
# - Look for obvious outliers or data quality issues

print("=== Summary Statistics ===")
print(df.describe().round(3))

print(f"\n=== Missing Values ===")
print(df.isnull().sum())

# %%
# =============================================================================
# STEP 3: Visualize the Key Relationship
# =============================================================================
# What does the raw data look like? Does it match the economic theory?

fig = px.scatter(
    df,
    x='{x_variable}',
    y='{y_variable}',
    labels={
        '{x_variable}': '{x_label} ({units})',
        '{y_variable}': '{y_label} ({units})'
    },
    title='{Chart title: what relationship does this show?}',
    hover_data=['{additional_info_column}'],
    opacity=0.7
)
fig.update_layout(
    template='plotly_white',
    font=dict(size=12),
    title_font_size=16
)
fig.show()

# %% [markdown]
# ### What do you observe?
#
# {Prompt students to interpret the scatter plot before running any regressions.}
#
# **Question:** Based on the scatter plot, does the relationship appear to be:
# - Positive or negative?
# - Linear or nonlinear?
# - Strong or weak?
#
# Write your answer in the cell below before continuing.

# %%
# Your observation here:
# observation = """
# [Write your answer here]
# """

# %%
# =============================================================================
# STEP 4: Main Estimation — {method_name}
# =============================================================================
# Here we implement the {method} from lecture.
# Recall the estimator: {equation description}
#
# Key decision: We always use HC3 heteroskedasticity-robust standard errors.
# This is the econometrics standard — it's more conservative than OLS standard errors
# and doesn't require homoskedasticity.

# Prepare design matrix
X = sm.add_constant(df[['{regressor_1}', '{regressor_2}']])  # add_constant adds the intercept
y = df['{outcome_variable}']

# Estimate model
model = sm.OLS(y, X).fit(cov_type='HC3')

# Display results
print(model.summary())

# %% [markdown]
# ### Interpreting the Results
#
# Look at the output above. Focus on:
#
# 1. **The coefficient on `{main_variable}`**: It is {expected_sign}. This means {interpretation}.
#    In economic terms: a one-unit increase in {variable} is associated with a {magnitude} change
#    in {outcome}, holding {controls} constant.
#
# 2. **Statistical significance**: The p-value is {expected_significance}, so we {can/cannot}
#    reject the null hypothesis that the coefficient is zero at the 5% level.
#
# 3. **The R²**: It is approximately {expected_R2}, meaning our model explains about {X}% of
#    the variance in {outcome}. Is this high or low for this type of data?
#
# **Does this match your prediction from the scatter plot?**

# %%
# Extract and display key coefficients in a cleaner format
results_df = pd.DataFrame({
    'Coefficient': model.params,
    'Std Error (HC3)': model.bse,
    't-statistic': model.tvalues,
    'p-value': model.pvalues,
    '95% CI Lower': model.conf_int()[0],
    '95% CI Upper': model.conf_int()[1]
}).round(4)

print("=== Key Coefficients ===")
print(results_df)

# %% [markdown]
# ---
# ## Part 2: {part_2_title} — Semi-Guided
#
# ### What we're doing
#
# {2–3 paragraphs introducing the extension. What new question are we asking?
# What limitation of Part 1 does this address?}

# %%
# =============================================================================
# STEP 5: {Extension method or concept}
# =============================================================================
# TODO: Complete the code below following the pattern from Part 1.
# Hint: {specific hint about what needs to change}

def estimate_{method_name}(df, outcome, regressors, {additional_params}):
    """
    {One sentence describing what this function does.}

    Parameters
    ----------
    df : pd.DataFrame
        Dataset
    outcome : str
        Dependent variable name
    regressors : list of str
        Independent variable names
    {additional_params} : {type}
        {description}

    Returns
    -------
    {return_type}
        {description}
    """
    # TODO: Implement this function
    # Step 1: Prepare design matrix
    X = sm.add_constant(df[regressors])
    y = df[outcome]

    # Step 2: ???
    # (Your code here)

    # Step 3: Return results
    pass  # Replace with return statement

# Test your function:
# result = estimate_{method_name}(df, '{outcome}', ['{reg1}', '{reg2}'], {param_value})
# print(result.summary())

# %%
# Compare results across specifications
# TODO: Fill in the coefficients from your different model runs

comparison_data = {
    'Specification': ['Baseline (Part 1)', 'Extension 1', 'Extension 2'],
    'Coefficient on {main_variable}': [
        model.params['{main_variable}'],  # from Part 1
        None,  # TODO: fill in
        None   # TODO: fill in
    ],
    'Standard Error': [
        model.bse['{main_variable}'],
        None,
        None
    ]
}

comparison_df = pd.DataFrame(comparison_data)
print("=== Comparison Across Specifications ===")
print(comparison_df.to_string(index=False))

# %% [markdown]
# ### What does the comparison tell us?
#
# {Prompt for interpretation:}
#
# - Did the coefficient on `{main_variable}` change when you added {control}? By how much?
# - What does the stability (or instability) of the coefficient suggest about {concept}?
# - Which specification do you prefer, and why?

# %% [markdown]
# ---
# ## Part 3: Open-Ended Extensions
#
# Now apply what you've learned independently. These questions don't have a single right answer.
# The goal is to practice making methodological choices and justifying them.

# %% [markdown]
# ### Extension A — Predicted Change
#
# {Guided extension: change one parameter and predict what happens before running.}
#
# **Before you run any code:** Write your prediction in the cell below.
# - I predict that changing {X} will cause the coefficient on {Y} to {increase/decrease/stay similar}
# - My reasoning: ...

# %%
# Your prediction (write it here before running):
prediction = """
I predict...
Because...
"""
print(prediction)

# Your code for Extension A:
# ...

# %% [markdown]
# ### Extension B — New Dataset
#
# Apply the same method to a different dataset.
#
# **Data:** Download the dataset below and repeat the analysis from Part 1.
# Use [{suggested_dataset}]({suggested_dataset_url}).
#
# **Question:** {Specific research question to answer with the new data}
#
# **What to report:** A brief (3–5 sentence) interpretation of your findings.

# %%
# Load the new dataset:
# url_b = '{extension_b_data_url}'
# df_b = pd.read_csv(url_b)

# Your analysis here:
# ...

# %% [markdown]
# ### Extension C — Your Own Research Question
#
# Find a dataset where the method from this lab would be useful.
#
# **Requirements:**
# 1. Find real data from a credible source (FRED, World Bank, Kaggle, BLS, etc.)
# 2. State your research question clearly
# 3. Run the analysis with appropriate controls and robust standard errors
# 4. Interpret your findings in 3–5 sentences
# 5. State one important limitation of your analysis
#
# *This extension is portfolio-worthy — clean it up and put it on GitHub!*

# %%
# Your Extension C here:
# Research question: ...
# Data source: ...
# ...

# %% [markdown]
# ---
# ## Summary
#
# In this lab, you:
# 1. {accomplishment_1}
# 2. {accomplishment_2}
# 3. {accomplishment_3}
#
# **Key takeaway:** {1–2 sentence summary connecting the lab back to the lecture concept}
#
# **Next steps:** In the next lab, we will {foreshadow next lab's topic}.
