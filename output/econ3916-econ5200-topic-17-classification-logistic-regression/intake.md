# Lecture Intake Form

**Generated:** 2026-03-22
**Output slug:** `econ3916-econ5200-topic-17-classification-logistic-regression`

---

## Course Information

```yaml
course_title: "ECON 3916: Statistical & Machine Learning for Economics / ECON 5200: Applied Data Analytics in Economics"
course_code: "econ3916-econ5200"
topic_title: "Classification I — Logistic Regression"
topic_number: 17
total_topics: 20
position_context: "late"
```

## Class Parameters

```yaml
class_length_minutes: 90
theory_minutes: 60
lab_minutes: 30
class_type: "presentation + lab"
audience_level: "advanced_undergrad + masters (mixed)"
```

## Prerequisites

```yaml
prerequisites_covered:
  - "OLS regression (estimation, interpretation, Gauss-Markov)"
  - "Multiple regression, multicollinearity, heteroskedasticity"
  - "Hypothesis testing: t-tests, F-tests, p-values"
  - "Train-test split and cross-validation (sklearn pipeline)"
  - "Regularization: Lasso (L1) and Ridge (L2), LassoCV"
  - "Bias-variance tradeoff"
  - "Python/sklearn workflow: fit, predict, score"
  - "FRED API (fredapi) and wbgapi data access"
  - "Topic 16 (just covered): Regularization with Lasso/Ridge on GDP prediction"
```

## Supporting Materials

```yaml
supporting_docs_provided: true
supporting_docs_summary: >
  Full course curriculum document (ECON 3916 Lecture Plans.docx) covering all 25 topics.
  Topic 17 is specified as: Theory — LPM flaws, Log-Odds transformation, Sigmoid function,
  Odds Ratios, likelihoods. Lab — "Predicting Recession" using FRED Yield Curve (10Y-3M
  Treasury spread) and NBER recession dates. Libraries: scikit-learn.
  Course philosophy: "Manual Mastery then AI Co-Pilot" — Part A (no AI), Part B (AI-assisted).
  PRIME prompting framework taught alongside technical content.
flagged_outdated_examples:
  - "Yield Curve / Recession lab content — ensure 2024-2025 data used (yield curve inverted 2022-2024, normalizing in 2025)"
```

## Inferred Context

```yaml
depth_calibration: >
  Late-course topic (17 of 20) — students have strong OLS + sklearn foundation and just
  completed Lasso/Ridge. They know the ML pipeline deeply. This lecture pivots from
  regression (continuous Y) to classification (binary Y). Can reference OLS shortcomings
  directly. Must be accessible to both advanced undergrad (ECON 3916) and masters (ECON 5200)
  simultaneously — intuition-first, then formalism, with masters-level detail in speaking notes.
  Next lecture (Topic 18) covers Model Evaluation Metrics — plant seeds for precision/recall/AUC.
key_prior_concepts_to_activate:
  - "OLS: linear function maps X to predicted Y — what happens when Y is 0/1?"
  - "Sigmoid/softmax appears in neural network activations (planted in Topic 16 discussion)"
  - "sklearn .fit() / .predict() / .predict_proba() pattern students know from Ridge/Lasso"
upcoming_topics_to_seed:
  - "Topic 18 (Model Evaluation): accuracy is not enough — precision, recall, ROC/AUC"
  - "Topic 19 (Random Forests): logistic regression is the linear classification baseline; trees capture nonlinearities"
```

## Pipeline Flags

```yaml
interactive_elements_required: true
min_discussion_sets: 2
min_poll_questions: 3
lab_required: true
lab_minutes: 30
web_search_required: true
min_example_year: 2024
dual_course: true
note: "Lecture notes must serve both ECON 3916 (advanced undergrad) and ECON 5200 (masters)"
```

---

*This intake form is read by all downstream pipeline stages.*
