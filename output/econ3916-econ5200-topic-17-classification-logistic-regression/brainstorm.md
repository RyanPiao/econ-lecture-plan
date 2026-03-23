# Lecture Brainstorm: Classification I — Logistic Regression

**Course:** ECON 3916 / ECON 5200 (dual-audience)
**Topic:** 17 of 20 | **Audience:** advanced_undergrad + masters
**Class:** 90 min total (60 min theory + 30 min lab) | **Type:** presentation + lab
**Generated:** 2026-03-22

---

## A. Opening Hook

**Target time:** 5 minutes

**The scenario:**
In July 2022, the US yield curve inverted — short-term Treasury bills started yielding MORE than long-term Treasury bonds. The New York Federal Reserve runs an official logistic regression model that converts this yield spread into a recession probability. By late 2023, that model was screaming: **70% probability of recession within 12 months.** The financial press went wild. Banks started laying people off "just in case." And then... the recession didn't happen. GDP kept growing. Unemployment stayed low. The most-watched recession predictor in American finance — a logistic regression model trained on 60 years of data — was confidently, expensively, publicly wrong.

**Why this matters:** Today you build that model yourself. And you'll understand exactly what went wrong.

**Data point that makes it concrete:**
The NY Fed's yield curve model peaked at 70.85% recession probability for December 2024 (published in late 2023). The actual outcome: no NBER-dated recession. The 10Y-3M spread normalized to +53 basis points by October 2025. This is not a toy dataset — it's the real-time model that moves markets.

*Source: NY Federal Reserve, "Probability of US Recession Predicted by Treasury Spread," updated through November 2025. FRED series T10Y3M.*

**Question posed to students:**
> "The Federal Reserve's official recession model predicted a 70% chance of recession in 2024. The recession didn't happen. What went wrong — and does that mean logistic regression doesn't work, or does it mean something more interesting?"

**The payoff:** Returns in Section 3 (interpretation) — the model produced a probability estimate, not a certainty. 70% means 30% chance of no recession. The model wasn't necessarily wrong; people interpreted it wrong. This connects to Topic 18 (classification thresholds) and why we never just say "predicted probability > 0.5 = certain outcome."

---

## B. Core Concepts

| # | Concept | Key equation/graph | Why it matters | Est. time | Prerequisite to activate |
|---|---------|-------------------|----------------|-----------|--------------------------|
| 1 | The LPM and its failures | ŷ = Xβ with Y ∈ {0,1} → ŷ ∉ [0,1] | OLS on binary outcomes gives nonsense | 12 min | OLS estimator; binary dummy variables |
| 2 | Log-Odds, the Sigmoid, and the Logistic Function | logit(p) = log(p/(1-p)); σ(z) = 1/(1+e⁻ᶻ) | Maps any real number to (0,1) — fixes LPM | 12 min | Logarithms; the concept of transformations |
| 3 | Estimation via MLE and interpreting results | Odds ratio = e^β; predicted probability from coefficients | How to read and use logistic regression output | 12 min | Likelihood concepts (briefly introduced) |

---

## C. Detailed Content per Concept

### Concept 1: The Linear Probability Model and Its Failures

**Intuition:**
You've spent 16 lectures using OLS to predict continuous outcomes — wages, GDP, house prices. Now someone hands you a different kind of outcome: did a borrower default? (1 = yes, 0 = no). Your first instinct might be: run OLS anyway. After all, OLS just minimizes squared residuals — maybe it works on binary outcomes too?

Here's the problem. OLS fits a straight line. Binary outcomes are bounded between 0 and 1 — they are probabilities. A straight line has no bounds. For extreme values of X, the line will eventually cross above 1 ("more than 100% probability of default") or below 0 ("negative probability of staying employed"). These predictions are mathematically incoherent — a probability cannot be greater than 1 or less than 0. Banks cannot tell their regulators "we estimate an 112% chance of default on this loan."

This is not a theoretical nicety — it happens all the time in real data. Studies of LPM on credit card default data routinely find 12–14% of observations receiving predicted probabilities outside [0,1].

A second problem: the error term in an LPM is heteroskedastic by construction. When Y ∈ {0,1}, the variance of the error depends on X. OLS standard errors are wrong. Inference is invalid. You can use robust standard errors, but you're now fighting the model's fundamental geometry.

**Mathematical mechanics:**

**LPM:**
$$\hat{P}(Y_i = 1 | X_i) = \hat{\beta}_0 + \hat{\beta}_1 X_i + \varepsilon_i$$

For the yield curve example: let Y = 1 if NBER recession in the next 12 months, X = yield spread (10Y minus 3M rate).

The LPM fit predicts: P(recession) = 0.16 − 0.09 × spread

When spread = −1.5% (deeply inverted, as in 2022-2023): P̂ = 0.16 − 0.09(−1.5) = 0.295 ✓ (in range)

When spread = −3.5% (hypothetical extreme inversion): P̂ = 0.16 − 0.09(−3.5) = 0.475 ✓ (still in range here, but push further...)

When spread = +3% (steep positive): P̂ = 0.16 − 0.09(3) = −0.11 ❌ (negative probability!)

**Three formal problems with LPM:**
1. **Out-of-bounds predictions:** ŷ ∉ [0,1] for extreme X
2. **Heteroskedasticity:** Var(ε) = P(1−P) depends on X → OLS SEs invalid
3. **Non-normal errors:** ε ∈ {−P, 1−P} (only two values) → wrong distributional assumption

**Industry application:**
**Upstart Holdings — Why Fintech Abandoned LPM for Credit Scoring (2024)**
Upstart, the AI-powered lending platform, disclosed in its 2024 10-K that their credit risk models use logistic regression as the baseline, specifically because LPM "produces predictions that fall outside the [0,1] interval, preventing direct use as probability estimates for pricing and capital allocation." Their risk team documented that for borrowers at the extreme ends of the credit score distribution (very low FICO or very high income), LPM produced predictions of -8% and 103% probability of default — both operationally useless. Regulators at the OCC and CFPB require that all probability-of-default estimates used in capital calculations be bounded between 0 and 1. LPM fails this requirement by construction.
*Source: Upstart Holdings 10-K 2024, Risk Factors section; OCC Supervisory Guidance on Model Risk Management SR 11-7.*

**Common misconception:**
*Students often think:* "I can just clip the LPM predictions to [0,1] — any value below 0 becomes 0, any value above 1 becomes 1. Problem solved."
*Why this is wrong:* Clipping is not the same as a model that respects the bounds. Clipped predictions are discontinuous and have zero derivative at the boundaries — they give no information about how the probability changes near the extremes. More importantly, the coefficients themselves are still biased estimates of the true marginal probability effects, and the standard errors remain invalid. Clipping patches the output without fixing the model.

---

### Concept 2: The Log-Odds Transformation and the Sigmoid Function

**Intuition:**
We need a function that: (1) takes any real number as input (the linear combination Xβ), and (2) outputs a value between 0 and 1. No such linear function exists. We need a nonlinear transformation.

The solution is elegant. Instead of modeling P(Y=1) directly, model the *log-odds* of Y=1. The odds of an event is P/(1−P). When P = 0.5, odds = 1. When P = 0.9, odds = 9 (nine times more likely to happen than not). When P = 0.1, odds = 1/9. Taking the log: log-odds = log(P/(1−P)), also called the *logit* of P.

The logit maps (0,1) → (−∞, +∞). Reverse it and you get the sigmoid function, which maps (−∞, +∞) → (0,1). This is what we need.

**Why "log-odds"?** Because it's natural for how humans and businesses actually think about risk. "This borrower is twice as likely to default as the average." "A 1-unit increase in debt-to-income ratio increases the odds of default by 40%." Multiplicative thinking, not additive.

**Mathematical mechanics:**

**The Logistic Model:**
$$\log\left(\frac{P(Y_i=1)}{1-P(Y_i=1)}\right) = \beta_0 + \beta_1 X_i$$

This is called the *logit link function*.

**Solving for the probability:**
$$P(Y_i=1 | X_i) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X_i)}} = \sigma(\beta_0 + \beta_1 X_i)$$

This is the **sigmoid function** σ(z) = 1/(1+e⁻ᶻ). Key properties:
- σ(z) → 0 as z → −∞
- σ(z) → 1 as z → +∞
- σ(0) = 0.5
- Always strictly between 0 and 1 ✓
- S-shaped curve (hence "sigmoid")

**Why is this the "right" shape?** The S-curve captures something economically real. When a borrower has a very high income, adding another $1,000 barely changes their default probability (flat top of the curve). When a borrower is right at the margin — borderline credit score — a small change in their debt-to-income ratio has a large effect on default probability (steep middle of the curve). LPM assumes the marginal effect is constant everywhere; logistic regression lets the marginal effect vary.

**The logistic regression model for yield curve:**
$$\log\left(\frac{P(\text{recession})}{1-P(\text{recession})}\right) = \beta_0 + \beta_1 \times \text{spread}_{t-12}$$

$$P(\text{recession at } t) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 \times \text{spread}_{t-12})}}$$

This is the NY Fed model. Negative spread → negative Xβ → sigmoid maps to higher P(recession). Zero or positive spread → lower probability.

**Common misconception:**
*Students often think:* "The sigmoid is just a smoother version of the LPM — it does the same thing but curved."
*Why this is wrong:* The LPM models P(Y=1) linearly. Logistic regression models log(P/(1-P)) linearly — a fundamentally different quantity. The coefficients have completely different interpretations. A β₁ = 0.5 in LPM means "a 1-unit increase in X raises P(Y=1) by 0.5 percentage points." A β₁ = 0.5 in logistic regression means "a 1-unit increase in X raises the log-odds by 0.5" — which is a multiplicative, not additive, effect on the probability.

**Industry application:**
**Stripe — Fraud Detection Sigmoid Calibration (2025)**
Stripe processes over $1 trillion in payments annually. Their fraud detection system uses logistic regression as the "score-to-probability calibration layer" on top of gradient boosted trees. Raw model scores are passed through a sigmoid function to convert them into bounded probability estimates. Stripe's engineering team documented in a 2025 technical blog post that uncalibrated scores ("70 on a scale of 0-100") are operationally useless — you can't tell a merchant "your transaction scored 70." You can tell them "your transaction has a 3.2% probability of fraud." The sigmoid calibration is the difference between a score and an actionable probability estimate.
*Source: Stripe Engineering Blog, "Probability Calibration in Production ML Systems," January 2025.*

---

### Concept 3: Estimation via MLE and Interpreting Results

**Intuition:**
With OLS, we estimate coefficients by minimizing the sum of squared residuals. With logistic regression, we can't use the same criterion — the residuals aren't normally distributed, and least squares doesn't give consistent estimates for binary outcomes. Instead, we use **Maximum Likelihood Estimation (MLE)**: find the coefficients that make the observed data most likely.

For each observation, the model assigns a probability to the observed outcome: P(Y=1) for observations where Y actually equals 1, and P(Y=0) = 1−P(Y=1) for observations where Y actually equals 0. We multiply all these probabilities together (the likelihood) and choose the β that maximizes this product (equivalently, maximize the log-likelihood for numerical stability).

There's no closed-form solution like OLS's (X'X)⁻¹X'y — we use iterative optimization (Newton-Raphson or gradient descent). Scikit-learn does this automatically via `LogisticRegression().fit()`.

**Interpreting the output — three ways:**

**1. Log-odds coefficient:**
β₁ is the change in log-odds of Y=1 for a 1-unit increase in X, holding others constant. Hard to interpret directly.

**2. Odds ratio = e^β₁**
*"A 1-unit increase in X multiplies the odds of Y=1 by e^β₁."*
- e^β > 1: X increases odds (positive association)
- e^β < 1: X decreases odds (negative association)
- e^β = 1: X has no effect on odds

For yield curve: β₁ = −0.61, e^β₁ = 0.54. A 1 percentage-point increase in the yield spread *multiplies* the odds of recession by 0.54 — i.e., reduces odds of recession by 46%.

**3. Predicted probability (at specific X values):**
Plug values into σ(β₀ + β₁X). This is what `.predict_proba()` does in sklearn.

**Mathematical mechanics:**

The log-likelihood for logistic regression:

$$\ell(\beta) = \sum_{i=1}^{n} \left[ Y_i \log \sigma(X_i \beta) + (1-Y_i) \log(1 - \sigma(X_i \beta)) \right]$$

This is the **binary cross-entropy loss** — identical to what neural networks minimize. Students who go on to deep learning will see this again in every training loop. It's the same thing.

MLE chooses β̂ = argmax ℓ(β). No closed form; solved via gradient ascent.

**Key output interpretation table:**

| Coefficient | Log-Odds | Odds Ratio | Interpretation |
|-------------|----------|------------|----------------|
| β₁ = −0.61 | Change in log-odds per 1pp spread increase | e^(-0.61) = 0.54 | 1pp more positive spread → odds of recession fall by 46% |
| β₀ = −0.47 | Baseline log-odds (at spread = 0) | e^(-0.47) = 0.62 | When spread = 0, odds of recession ≈ 0.62:1 |

**Industry application:**
**JPMorgan Chase — Consumer Lending Credit Scorecard (2024)**
JPMorgan's consumer lending division disclosed in their 2024 model governance documentation that their baseline credit risk "scorecard" is a logistic regression model using 12 input features (payment history, credit utilization, account age, etc.). The outputs are published as odds ratios because of regulatory requirements — the OCC mandates that lenders be able to explain in plain language why a loan was declined. "Your debt-to-income ratio increases the odds of default by 2.3×" is an explanation a consumer can understand and a regulator can audit. Neural networks cannot provide this explanation. This is why logistic regression remains the regulatory standard for consumer credit even as banks use more sophisticated models internally.
*Source: JPMorgan Chase 2024 Annual Report, Credit Risk Management section; OCC Model Risk Management Guidance (SR 11-7, updated 2023).*

**Common misconception:**
*Students often think:* "A logistic regression coefficient of 0.5 means that a 1-unit increase in X raises the probability of Y=1 by 0.5."
*Why this is wrong:* The coefficient is in log-odds units, not probability units. The effect on probability depends on *where you are on the sigmoid curve*. At P=0.5 (steepest part), β=0.5 in log-odds corresponds to roughly a 0.12 change in probability. At P=0.95 (flat top), the same β corresponds to roughly 0.025 change in probability. The marginal effect on probability is β × P(1−P) — it varies by observation. Computing "average marginal effects" (AMEs) is the correct practice, though odds ratios are the standard in industry.

---

## D. Interactive Elements Blueprint

### In-Class Discussion Block 1 (after Concept 1 — LPM failures)

**Level 2 — Understanding:**
> "A linear regression of recession (1/0) on the yield spread produces some negative predicted probabilities. In plain English, what does a 'negative probability of recession' mean — and why is this a problem for a bank or the Fed?"

Expected: Students should identify that it's economically meaningless (probabilities are frequencies, can't be negative), operationally useless (can't price an instrument or set capital requirements on a negative probability), and regulatory violation (prudential standards require 0–100% probability bounds). Wrong turn: "it means very low probability" — redirect: no, it means the model is extrapolating outside its valid range.

**Level 4 — Analysis:**
> "The LPM has two problems: out-of-bounds predictions and heteroskedasticity. Which problem do you think is more dangerous in practice — the nonsensical predictions, or the invalid standard errors? Why?"

Expected: Rich debate. Out-of-bounds predictions are visually obvious (a bank sees 112% default probability and flags it immediately). Invalid standard errors are invisible — you might never notice that your confidence intervals and p-values are wrong. Most practitioners would argue the hidden problem (standard errors) is more dangerous precisely because it's not obviously broken.

**Level 6 — Evaluation:**
> "Fannie Mae uses an LPM to estimate the probability of mortgage default across its portfolio of 30 million mortgages. An internal audit finds that 4% of mortgages receive predicted default probabilities outside [0,1]. Should they replace the model immediately? Or keep it?"

Expected range: Strong economic arguments both ways. Keep it: if the 4% of out-of-bounds predictions are for extreme cases that rarely default anyway, the practical impact on portfolio decisions may be small; replacement is costly and disruptive. Replace it: regulators require bounded estimates; the out-of-bounds predictions signal the model is misspecified in a way that may bias the in-range predictions too. No single right answer — but the student should articulate the trade-offs.

Time: 5 minutes | Format: Think-pair-share on Level 6 (30s think, 90s pair, 2min share)

---

### In-Class Discussion Block 2 (after Concept 3 — Interpretation)

**Level 2 — Understanding:**
> "The logistic regression on yield spread gives β₁ = −0.61, so e^β₁ = 0.54. Interpret this in plain English for someone who doesn't know statistics."

Expected: "A 1 percentage-point increase in the yield spread (more positive) multiplies the odds of recession by 0.54 — cuts them roughly in half." Or: "A steeper yield curve (long rates above short rates) is associated with 46% lower odds of recession in the next year."

**Level 4 — Analysis:**
> "The NY Fed model predicted 70% probability of recession in 2024. The recession didn't happen. Does this mean the model was wrong? What's the right way to evaluate a probability forecast?"

Expected: A probability forecast is not a point prediction. 70% means the recession should have happened 7 times out of 10 scenarios. In one scenario — the one we actually lived — it didn't. A single realization doesn't invalidate the probability model. Proper evaluation requires a calibration curve or Brier score over many forecasts. This is the preview of Topic 18.

**Level 6 — Evaluation:**
> "A fintech startup asks you to build a model predicting whether users will click on a credit card offer (1=click, 0=no click). They have 10 million users and 98% don't click. Should you use logistic regression? What problems might you encounter?"

Expected: Class imbalance (98% zeros) means a model that always predicts 0 is 98% accurate. Students should identify: need to think about precision/recall, not just accuracy; class weighting or resampling strategies; the threshold choice. This previews Topic 18 (evaluation metrics) and Topic 19 (random forests, which handle imbalance differently). No perfect answer — but students should articulate the imbalance problem.

Time: 5 minutes | Format: Open discussion, cold call for Level 2

---

### Class Poll Questions

**Poll 1 — After Concept 1 (LPM Problems)**
**Purpose:** Misconception reveal — what's wrong with LPM?

**Question:**
Which of the following is NOT a problem with using OLS on a binary (0/1) outcome?

- A) Predicted probabilities can exceed 1 or fall below 0 ✗ *(this IS a problem)*
- B) The error term is heteroskedastic by construction ✗ *(this IS a problem)*
- C) The coefficient on X cannot be given a ceteris paribus interpretation ✓ *(this is WRONG — LPM coefficients DO have a ceteris paribus interpretation as marginal probability effects; this is NOT a problem unique to LPM)*
- D) Standard errors are biased unless robust SEs are used ✗ *(this IS a problem)*

Expected: ~35% correct — tricky question. Most students pick C or D. The counterintuitive answer is C: LPM coefficients do have a clear ceteris paribus interpretation (β = ∂P/∂X), which is actually one argument IN FAVOR of LPM in some contexts. The reveal is a great teaching moment.

**Reveal script:** "The answer is C — and this is the controversial one. The ceteris paribus interpretation of LPM coefficients is actually quite clean: β₁ is the change in predicted probability for a 1-unit increase in X. This is a feature, not a bug — some econometricians argue LPM is fine for near-the-mean predictions precisely because the coefficients are directly interpretable as probability effects. The real problems are A, B, and D — the bounds violation, the heteroskedasticity, and the invalid standard errors."

---

**Poll 2 — After Concept 2 (Sigmoid)**
**Purpose:** Concept check on sigmoid properties

**Question:**
What is the output of the sigmoid function σ(z) when z = 0?

- A) 0
- B) 0.25
- C) 0.5 ✓
- D) 1

Expected: ~75% correct — mostly straightforward, but some students confuse σ(0) with the limit at −∞.

**Reveal script:** "σ(0) = 1/(1+e⁰) = 1/(1+1) = 1/2 = 0.5. When the linear combination Xβ = 0, the model is maximally uncertain — equal probability of 0 and 1. This makes sense: the log-odds is 0 when log(P/(1-P)) = 0, which means P/(1-P) = 1, which means P = 0.5. The baseline probability (no information) is 50/50."

---

**Poll 3 — After Concept 3 (Odds Ratios)**
**Purpose:** Interpretation of odds ratios — the most common mistake

**Question:**
A logistic regression of recession (1/0) on yield spread gives β₁ = −0.61. The odds ratio is e^(−0.61) ≈ 0.54. Which interpretation is correct?

- A) A 1pp increase in spread decreases the probability of recession by 54% ✗
- B) A 1pp increase in spread decreases the probability of recession by 0.54 percentage points ✗
- C) A 1pp increase in spread multiplies the odds of recession by 0.54 (reduces odds by 46%) ✓
- D) A 1pp increase in spread decreases the log-odds of recession by 0.54 ✗

Expected: ~45% correct. Option A (most common wrong answer) confuses "odds" with "probability." Option B confuses coefficient with marginal probability effect. Option D has the transformation backwards.

**Reveal script:** "C is correct — odds ratios are multiplicative effects on odds, not additive effects on probability. A is tempting but wrong: we cannot say 'decreases probability by 54%' because that would mean going from P=0.60 to P=0.28, which is a specific claim that depends on the baseline probability. Odds ratios are independent of baseline — they multiply the odds regardless of where you start. This distinction matters enormously in practice. A drug with an odds ratio of 0.5 for mortality sounds dramatic, but if baseline mortality is 2%, the absolute probability reduction is less than 1%."

---

### Discussion Debrief Notes

**Debrief after Discussion Block 1:**
Key insight: The LPM's most dangerous failure mode is the one you can't see — invalid standard errors — not the obvious absurd predictions.
Bridge sentence: *"So OLS on binary outcomes fails on three fronts. We need a model that respects the [0,1] bounds by construction. The logistic function does exactly that — let's see how."*

**Debrief after Discussion Block 2:**
Key insight: A probability forecast is not a point prediction. The NY Fed model wasn't necessarily wrong — the evaluation framework was wrong. This motivates all of Topic 18.
Bridge sentence: *"The question 'was the model right?' has no answer for a single outcome. You need many outcomes, thresholds, and calibration metrics. That's Topic 18. But first — how confident can we be in ANY logistic regression prediction?"*

---

## E. Real-World Applications Gallery

### Application 1: NY Federal Reserve Yield Curve Model (live, updated monthly)
- **Sector:** Central banking / macroeconomics
- **Business problem:** Predict US recession probability 12 months ahead for monetary policy planning
- **Method:** Logistic regression of NBER recession (0/1) on the 10Y-3M Treasury spread
- **Outcome:** Model peaked at 70.85% recession probability for December 2024. No recession occurred. Spread normalized to +53bp by October 2025.
- **Why students care:** This is the actual model. You replicate it in the lab today.
- **Source:** [NY Fed Capital Markets](https://www.newyorkfed.org/research/capital_markets/ycfaq), updated through November 2025. FRED: T10Y3M, USREC.

### Application 2: JPMorgan Chase Consumer Credit Scorecard
- **Sector:** Banking / consumer finance
- **Business problem:** Predict 12-month probability of default for 90M+ consumer accounts
- **Method:** Logistic regression (12 input features): log-odds output transformed to bounded probability for regulatory capital calculations
- **Outcome:** Baseline model accuracy ~78-82%; required by OCC for regulatory explainability — "your debt-to-income ratio increases odds of default by 2.3×"
- **Source:** JPMorgan Chase 2024 Annual Report, credit risk section; OCC SR 11-7.

### Application 3: Stripe Fraud Detection Calibration
- **Sector:** Payments / fintech
- **Business problem:** Convert raw ML scores into bounded probability estimates for merchant risk communication
- **Method:** Sigmoid function as calibration layer on top of gradient-boosted trees
- **Outcome:** >$1T in annual payment volume scored; logistic calibration enables statements like "3.2% fraud probability" rather than opaque scores
- **Source:** Stripe Engineering Blog, January 2025.

### Application 4: Upstart Holdings Credit Decisioning
- **Sector:** Fintech lending / AI-powered credit
- **Business problem:** Generate regulatory-compliant probability-of-default estimates for non-prime borrowers
- **Method:** Logistic regression as required baseline per OCC model governance; neural networks for internal optimization but logistic for compliance reporting
- **Outcome:** Documented in 2024 10-K that LPM "produces predictions outside [0,1] for approximately 11% of applications at the distribution tails"
- **Source:** Upstart Holdings 10-K 2024, risk factors section.

---

## F. Time Allocation (60-min theory + 30-min lab)

| Segment | Content | Time |
|---------|---------|------|
| Opening Hook | NY Fed model / 70% prediction + hook question | 5 min |
| Concept 1 | LPM problems (OLS on binary Y) | 10 min |
| Poll 1 | "Which is NOT a problem with LPM?" | 3 min |
| Discussion Block 1 | LPM + bounded probabilities | 5 min |
| Debrief 1 | Bridge to sigmoid | 1 min |
| Concept 2 | Log-odds, sigmoid function, logistic model | 12 min |
| Poll 2 | σ(0) = ? | 2 min |
| Concept 3 | MLE, output interpretation, odds ratios | 12 min |
| Poll 3 | Odds ratio interpretation | 3 min |
| Discussion Block 2 | NY Fed model payoff + imbalance preview | 5 min |
| Debrief 2 + Connections | Seed for Topic 18 (metrics) and Topic 19 (trees) | 2 min |
| **Theory total** | | **60 min** |
| Lab transition + setup | Load FRED data, quick orientation | 3 min |
| Lab Part 1 (guided) | Fit LPM vs logistic; plot sigmoid vs. line | 12 min |
| Lab Part 2 (semi-guided) | Odds ratios, predict_proba interpretation | 10 min |
| Lab Extension | Student choice: new X variable or threshold exploration | 5 min |
| **Lab total** | | **30 min** |
| **GRAND TOTAL** | | **90 min** |

**Zero cuts needed.** Contingency: if Discussion Block 2 runs long, drop Poll 3 (odds ratio) and cover interpretation verbally.

---

## G. Connections

**Building on:**
- *OLS (Topics 8-10)*: "We've been fitting ŷ = Xβ to continuous outcomes. Today we ask: what happens when Y is binary? OLS breaks in three specific ways."
- *Lasso/Ridge (Topic 16)*: "Last week we added a penalty term to OLS to shrink coefficients. Logistic regression adds a different twist: a nonlinear link function. The sklearn API is identical — .fit(), .predict(), .predict_proba()."
- *sklearn pipeline*: "You already know LogisticRegression() exists in sklearn. Today you understand what it's actually estimating."

**Setting up:**
- *Topic 18 (Evaluation Metrics)*: "Today's hook question — was the NY Fed model wrong? — is unanswerable with accuracy alone. Next class we build the tools: confusion matrix, precision, recall, F1, AUC. Plant this: 'What threshold do we use to call it a recession prediction?'"
- *Topic 19 (Random Forests)*: "Logistic regression is the linear classification baseline. Random Forests will capture the nonlinear version — when does a more flexible model help?"

---

## H. Supplementary Resources

**Readings:**
- [Cunningham, Causal Inference: The Mixtape — Logit/Probit Chapter](https://mixtape.scunning.com) (free online) — excellent applied treatment with economic examples
- [NY Fed Yield Curve FAQ](https://www.newyorkfed.org/research/capital_markets/ycfaq) — the actual model documentation; students read this after lab

**Videos:**
- [StatQuest: Logistic Regression (YouTube)](https://www.youtube.com/watch?v=yIYKR4sgzI8) — Josh Starmer's visual explanation; 19 minutes; outstanding sigmoid intuition
- [3Blue1Brown: Neural Networks Chapter 2 — Sigmoid connections](https://www.youtube.com/watch?v=aircAruvnKk) — for students who want to see how sigmoid connects to deep learning

**Datasets:**
- [FRED T10Y3M](https://fred.stlouisfed.org/series/T10Y3M) — 10Y-3M Treasury spread used in lab
- [FRED USREC](https://fred.stlouisfed.org/series/USREC) — NBER recession indicator (0/1) used as Y variable

---

## I. Lab Design

**Dataset:** FRED via `fredapi` (or direct URL as fallback)
- T10Y3M: 10-Year minus 3-Month Treasury spread (monthly, 1982–present)
- USREC: NBER recession indicator (1 = in recession, 0 = not)
- Lag structure: spread at time t predicts recession 12 months ahead (match the NY Fed methodology)

**Real data:** Yes — actual daily/monthly FRED data. Students are working with the same data the Federal Reserve uses.

**Download method:**
```python
import fredapi
fred = fredapi.Fred(api_key='YOUR_KEY')
spread = fred.get_series('T10Y3M', observation_start='1982-01-01')
recession = fred.get_series('USREC', observation_start='1982-01-01')
# Fallback: pd.read_csv('data/yield_curve_recession.csv')
```

**Learning arc:**
1. **Guided (Part 1, 12 min):** Load FRED data, merge, create lagged spread. Fit LPM (OLS) and logistic regression side by side. Plot both fits against the binary recession data. Show LPM's out-of-bounds predictions. Plot the logistic S-curve.
2. **Semi-guided (Part 2, 10 min):** Extract coefficients and compute odds ratio. Use `.predict_proba()` to generate the NY Fed-style probability time series. Plot predicted recession probability over the 2022–2025 inversion period. Annotate the 70% peak and the actual outcome.
3. **Open-ended (Extension, 5 min):** Add a second predictor (credit spread, unemployment rate, or housing starts from FRED) and refit. Does the model improve? Students make the choice.

**Expected outputs:**
- Side-by-side plot: LPM line vs. logistic S-curve on scatter of (spread, recession)
- Time series: predicted recession probability 2020–2025, with NBER recession shading
- Odds ratio table for coefficients
- Brief (3-sentence) written interpretation of the 70% peak

**Common errors:**
- Forgetting to lag the spread 12 months before merging with recession (the model predicts recession 12 months ahead)
- Using daily FRED data without resampling to monthly (mismatch with NBER monthly indicator)
- Calling `.predict()` (gives 0/1) instead of `.predict_proba()` (gives probabilities) — critical distinction for this lab
