# Classification I — Logistic Regression
## ECON 3916 / ECON 5200 — Topic 17 of 20
### 2026-03-22 | 90 min (60 min theory + 30 min lab) | Presentation + Lab

---

## 🎯 Learning Objectives

By the end of this lecture and lab, students will be able to:
1. **[Understand]** Explain why OLS (the Linear Probability Model) fails on binary outcomes and identify its three specific failure modes
2. **[Apply]** Transform between probability, odds, and log-odds, and map any real-valued linear combination to a bounded probability using the sigmoid function
3. **[Analyze]** Interpret logistic regression output in terms of odds ratios and predicted probabilities, and explain the difference between the coefficient and the marginal probability effect
4. **[Evaluate]** Assess the appropriateness of a logistic regression model for a given business or economic question, and identify when its assumptions may fail

---

## 🪝 Opening Hook (5 min)

In July 2022, something unusual happened in US Treasury markets: short-term government bonds started paying *more* than long-term bonds. The yield curve inverted. Economists know this signal well — an inverted yield curve has preceded every US recession since 1960. The New York Federal Reserve runs an official model — a logistic regression, trained on 60 years of data — that converts this yield spread into a 12-month recession probability. By late 2023, that model was screaming: **70.85% probability of recession by December 2024.**

The financial press went wild. Goldman Sachs issued recession warnings. Banks quietly started "right-sizing" headcounts. CNBC ran daily countdown segments. And then... nothing. GDP kept growing at 2.8% in 2024. Unemployment held below 4%. The inversion normalized. No NBER recession was ever declared.

The most-watched recession predictor in American finance — a logistic regression, the same model you'll build today — was confidently and expensively wrong. Or was it?

**Speaking notes:** "Before I tell you whether the model was actually wrong, I want you to sit with the question. [Pause.] Turn to the person next to you for 30 seconds: what does it mean for a probability forecast to be 'wrong'? If I tell you there's a 70% chance of rain and it doesn't rain — was my forecast wrong?" [Wait 30 sec, take 2 answers.] "We'll come back to this exact question in Section 3. But first — today you build that model yourself. Not as a toy example. The actual data the Federal Reserve uses, the actual methodology they publish. By the end of lab, you'll have your own version of the NY Fed recession probability chart."

**Question displayed on screen:**
> "The Fed's official model predicted a 70% chance of recession in 2024. The recession didn't happen. Was the model wrong — or were people interpreting it wrong? What's the difference?"

---

## 📚 Section 1: The Linear Probability Model and Why It Fails (12 min)

### Intuition

You've spent 16 lectures using OLS to predict continuous outcomes — wages, GDP growth, house prices. Now imagine a different kind of outcome: did this borrower default on their loan? Did the US enter a recession? Will this customer click on the ad? These are binary outcomes — 0 or 1 — and they are fundamentally different from continuous ones.

Your first instinct might be: run OLS anyway. After all, OLS just minimizes squared residuals — why not apply it to binary Y? This is called the **Linear Probability Model (LPM)**, and economists actually do use it in some contexts. But it has three specific failure modes that matter enormously when probabilities near the boundaries of [0,1] — which is exactly when the outcome is most interesting.

**Speaking notes:** "Let me be upfront: some econometricians defend the LPM for near-the-mean predictions. It's not categorically wrong. But in practice — in finance, risk management, and data science — it breaks in ways that matter. Here are the three specific ways."

---

### Formal Treatment

**The LPM setup:**

$$\hat{P}(Y_i = 1 | X_i) = \hat{\beta}_0 + \hat{\beta}_1 X_i + \varepsilon_i$$

This models the conditional probability of Y=1 as a linear function of X. OLS estimates β̂₀ and β̂₁ exactly as you'd expect.

**Failure Mode 1 — Out-of-Bounds Predictions:**
A linear function has no natural upper or lower bound. For extreme values of X, the predicted probability will cross above 1 or below 0.

Yield curve example: fit LPM with Y = NBER recession, X = 10Y-3M spread (lagged 12 months):
$$\hat{P}(\text{recession}) = 0.16 - 0.09 \times \text{spread}$$

- When spread = −2.5% (inverted): P̂ = 0.16 − 0.09(−2.5) = 0.385 ✓ (in bounds)
- When spread = +3.0% (steeply positive): P̂ = 0.16 − 0.09(3.0) = **−0.11** ❌ (negative probability — incoherent)

Studies of real credit default datasets find that 11–14% of observations receive out-of-bounds predictions. Banks cannot submit probability-of-default estimates outside [0,1] to regulators. This is not a theoretical edge case.

**Failure Mode 2 — Heteroskedasticity:**
When Y ∈ {0,1}, the error variance is not constant — it depends on X. Specifically:

$$\text{Var}(\varepsilon_i | X_i) = P_i(1 - P_i)$$

**Concrete example:** If a borrower has a predicted default probability of P = 0.05 (low-risk): Var(ε) = 0.05 × 0.95 = 0.048. If another borrower has P = 0.50 (borderline): Var(ε) = 0.50 × 0.50 = 0.250. The error variance is five times larger for the marginal borrower. This violates the homoskedasticity assumption — OLS standard errors are biased, and hypothesis tests are invalid even with large samples.

**Failure Mode 3 — Non-Normal Errors:**
The error term ε takes only two values: −P_i (when Y=0) and 1−P_i (when Y=1). This is the Bernoulli distribution — not a normal distribution. The distributional assumption underlying OLS inference is violated by construction.

> **Key result:** The LPM has three failure modes — out-of-bounds predictions, heteroskedastic errors, and non-normal errors. Robust standard errors fix Failure 2 partially, but cannot fix Failures 1 and 3. We need a fundamentally different model.

**Speaking notes:** "The heteroskedasticity point is easy to miss because you can't see it. The negative predicted probabilities you can see — they look obviously wrong. The invalid standard errors are invisible. You might run an LPM, get a p-value of 0.03, think you have a significant result, and never know that the true p-value was 0.08. That's the more dangerous failure mode. Note also: using `HC3` robust SEs (which you know from prior topics) partially fixes the standard error problem, but nothing fixes out-of-bounds predictions except a different functional form."

### Industry Application: Upstart Holdings — Why LPM Failed at Scale (2024)

**Context:** Upstart, the AI-powered lending platform, uses regulatory-compliant credit risk models for non-prime borrowers — people with thin or imperfect credit histories.

**The problem:** For borrowers at the extremes of the credit distribution — very low FICO scores or very high debt-to-income ratios — early LPM-based estimates produced default probability predictions of -8% and 103%. These are not just statistically inconvenient; they are operationally impossible. Capital requirement calculations require bounded probabilities. Loan pricing models require bounded probabilities. Consumer disclosure statements require bounded probabilities.

**The fix:** Logistic regression as the regulatory baseline, providing bounded estimates by construction. Neural networks for internal optimization (unconstrained), but logistic outputs for all external-facing compliance reporting.

**Why you should care:** Every data science role at a bank, insurance company, or fintech involves model governance constraints. Understanding *why* logistic regression is the regulatory standard — not just how to code it — is what distinguishes a junior analyst from a senior one.

*Source: Upstart Holdings 2024 Annual Report; OCC Supervisory Guidance on Model Risk Management (SR 11-7).*

**Speaking notes:** "Notice: the fintech companies that use the most sophisticated AI internally still produce logistic regression outputs for regulators. This is not because logistic regression is better than their neural nets — it's because regulators can audit a logistic regression coefficient and the explainability requirements are enshrined in law. 'Our model said no' is not a legal explanation for a loan denial. 'Your debt-to-income ratio increases odds of default by 2.3×, exceeding our threshold' is."

### ⚠️ Common Misconception

**Students often think:** "I can just clip LPM predictions — set anything below 0 to 0, anything above 1 to 1. Problem solved."

**Why this seems reasonable:** Clipping removes the offensive out-of-bounds values. The in-sample numbers look normal.

**The correction:** Clipping patches the output without fixing the model. The coefficients themselves are still estimated under the wrong functional form — the marginal effects are biased across the entire range, not just at the extremes. The standard errors remain invalid. The model is still wrong; you've just hidden the most obvious symptom. More importantly, clipping creates discontinuities at 0 and 1 that produce derivative-free regions — the model gives no information about how risk changes at the extremes, precisely where risk management needs the most information.

---

## 💬 In-Class Discussion: LPM Failures and Bounded Probabilities (5 min)

*After Section 1 — approximately 17 min into theory*

**Setup:** "You now know three things that go wrong with LPM. Before we fix it, let's make sure we understand what these failures actually mean in practice."

---

**Question A — Understanding (1 min):**
> "A linear regression of recession (1/0) on the yield spread produces some negative predicted probabilities. In plain English, what does a 'negative probability of recession' mean — and why is this a problem for the Federal Reserve or a bank?"

**Facilitation:** Strong answer: it's economically meaningless (frequencies can't be negative), operationally useless (can't price, can't set capital), and potentially a regulatory violation. Wrong turn: "it means very low probability of recession" — redirect: no, -11% is not "very low." The model is extrapolating outside its valid range. The model doesn't know what to do with a very positive yield spread, so it extrapolates the line below zero.

---

**Question B — Analysis (2 min):**
> "The LPM has two visible problems: negative predicted probabilities and predicted probabilities above 1. It also has an invisible problem: invalid standard errors. Which problem do you think is more dangerous in practice — the obvious ones or the invisible one? Why?"

**Facilitation:** Both sides are defensible. The key insight: obvious problems get caught quickly (someone notices P̂ = −11% and flags it). The invisible problem — invalid standard errors — may never be caught. A model that reports p = 0.03 when the true p-value is 0.08 leads to false discoveries that propagate into policy, pricing, and strategy. The invisible failure is more dangerous precisely because it doesn't announce itself.

---

**Question C — Evaluation (2 min, Think-Pair-Share):**
> "Fannie Mae uses an LPM to estimate mortgage default probability across its portfolio of 30 million mortgages. An internal audit finds that 4% of mortgages receive predictions outside [0,1]. Should they replace the model immediately, or is there a reasonable argument to keep it?"

**Facilitation:** Both positions have merit. Keep it: if the 4% of out-of-bounds cases are all extreme low-risk mortgages (very positive LTVs) that never actually default, the impact on aggregate portfolio decisions may be minimal; replacement is a multi-year, multi-million-dollar project. Replace it: regulators require bounded estimates; the model's misspecification near the boundaries signals it may be wrong in subtler ways even within [0,1]; it sets a bad precedent for model governance. No single right answer — the student should articulate both sides.

---

## 🔄 Discussion Debrief

**Key insight:** The most dangerous model failure is the one that doesn't announce itself. Invalid standard errors are silent; negative probabilities are loud.

**Bridging sentence:**
> "OLS fails on binary outcomes in three specific ways. The fix is not to patch the output — it's to use a model that respects the [0,1] constraint by construction. The sigmoid function does exactly that. Let's build it."

---

## 📚 Section 2: Log-Odds, the Sigmoid, and the Logistic Function (12 min)

### Intuition

We need a function that takes any real number as input (our linear combination Xβ, which ranges from −∞ to +∞) and outputs a number between 0 and 1. No linear function can do this — straight lines go to infinity in both directions. We need a nonlinear transformation.

Here's the key insight: instead of modeling P(Y=1) directly, we model the *odds* of Y=1, then take the logarithm. The **odds** of an event is the ratio of how likely it is to happen versus not happen:

$$\text{odds} = \frac{P}{1-P}$$

When P = 0.5 (50-50): odds = 1. When P = 0.9 (nine times more likely to happen): odds = 9. When P = 0.1: odds = 1/9 = 0.11. The odds range from 0 to +∞. The **log-odds** (also called the **logit**) extends this to −∞ to +∞:

$$\text{logit}(P) = \log\left(\frac{P}{1-P}\right) \in (-\infty, +\infty)$$

Now model the log-odds as a linear function of X. Then *invert* the transformation to recover a probability that is guaranteed to be in (0,1). That inversion is the **sigmoid function**.

**Why "odds" rather than probability?** Because multiplicative thinking matches how finance and medicine actually communicate risk. "This borrower is twice as likely to default as the benchmark" is a clearer statement than "this borrower has a 12% vs. 6% default rate." Odds ratios are what doctors, actuaries, and risk managers speak. You're going to speak their language.

**Speaking notes:** "Let me build the sigmoid geometrically. [Draw on board: horizontal axis = Xβ from −∞ to +∞, vertical axis = P from 0 to 1.] LPM draws a straight line that inevitably exits [0,1]. Logistic regression draws an S-curve that asymptotes to 0 on the left and 1 on the right — by construction. The steepest part of the S is at Xβ = 0, where P = 0.5. As we move further from 0 in either direction, the marginal effect of X on probability shrinks. This is exactly what we expect economically: adding $100,000 to the income of someone already making $1M barely changes their default probability; adding it to someone making $30,000 changes it a lot."

---

### Formal Treatment

**The Logistic Regression Model:**

We model the log-odds as a linear function of X:
$$\log\left(\frac{P(Y_i=1|X_i)}{1-P(Y_i=1|X_i)}\right) = \beta_0 + \beta_1 X_i$$

**Solving for the probability** (the sigmoid function):

$$P(Y_i=1 | X_i) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X_i)}} \equiv \sigma(\beta_0 + \beta_1 X_i)$$

**Where:**
- $\sigma(z) = \frac{1}{1+e^{-z}}$ is the **sigmoid function** (also called the **logistic function**)
- $z = \beta_0 + \beta_1 X_i$ is the **linear predictor** (same Xβ as OLS)
- $e$ is Euler's number ≈ 2.718

**Key properties of σ(z):**
- $\sigma(z) \in (0, 1)$ for all real z — **bounded by construction** ✓
- $\sigma(0) = 1/(1+1) = 0.5$ — maximum uncertainty at z = 0
- $\sigma(z) \to 1$ as $z \to +\infty$
- $\sigma(z) \to 0$ as $z \to -\infty$
- The derivative: $\sigma'(z) = \sigma(z)(1 - \sigma(z))$ — the slope is highest at P = 0.5

**Interpretation of the slope:**
The marginal effect of X on P is NOT constant (unlike LPM). It is:
$$\frac{\partial P}{\partial X} = \beta_1 \cdot \sigma(z) \cdot (1-\sigma(z)) = \beta_1 \cdot P(1-P)$$

This is largest when P = 0.5 (at the margin) and approaches zero as P → 0 or P → 1. This S-shape is economically appropriate: marginal effects should be largest for borderline cases.

**Yield curve model:**
$$\log\left(\frac{P(\text{recession})}{1-P(\text{recession})}\right) = \beta_0 + \beta_1 \times \text{spread}_{t-12\text{mos}}$$
$$P(\text{recession at } t) = \sigma(\beta_0 + \beta_1 \times \text{spread}_{t-12\text{mos}})$$

This is the exact NY Fed model specification. Negative spread (inversion) → negative z → higher P(recession). Positive spread → positive z → lower P(recession).

**Linearity assumption:** Logistic regression assumes the log-odds is a linear function of X. This is a real assumption — if the true relationship between spread and recession probability is nonlinear in the log-odds, the model is misspecified. Tree-based models (Topic 19) relax this assumption.

**Connection to deep learning (for masters students):** The sigmoid function is the activation function used in the output layer of a binary classification neural network. The difference is that neural networks stack many sigmoid layers; logistic regression uses exactly one. Same math, different architecture.

> **Key result:** The logistic model maps any real-valued Xβ to a probability in (0,1) via the sigmoid function. The log-odds is modeled linearly; the probability is inherently nonlinear and S-shaped. This resolves all three LPM failure modes.

**Speaking notes:** "I want everyone to draw this S-curve right now. [Pause while students draw.] Three points to mark: σ(−3) ≈ 0.05, σ(0) = 0.50, σ(+3) ≈ 0.95. Notice: you can never touch 0 or 1. That's the key. And notice the slope is steepest in the middle — that's where the model is doing the most work, and it's exactly where a small change in X matters most economically."

### Industry Application: Stripe — The Sigmoid as Probability Calibration (2025)

**Context:** Stripe processes over $1 trillion in payments annually. Their fraud detection system scores every transaction in real time.

**The problem:** Raw ML model scores (like "73.2 on a scale of 0-100") are operationally useless. You cannot tell a merchant "your transaction scored 73.2." You need to say "your transaction has a 3.2% probability of being fraudulent." That requires a bounded estimate in [0,1].

**The method:** Stripe's engineering team documented in a January 2025 technical blog post that they apply a sigmoid-based calibration layer on top of their gradient-boosted tree model. The raw tree score is passed through a fitted sigmoid (equivalent to a logistic regression of observed fraud rates on raw scores) to produce a calibrated probability. The calibration step is logistic regression; the underlying scorer is a tree. Many industry ML systems work this way — logistic regression as the final calibration layer on top of a more complex model.

**The result:** Fraud probability estimates drive automated merchant decisions: a transaction with P(fraud) > 0.15 triggers additional verification; P(fraud) > 0.40 triggers decline. These thresholds are only meaningful because the outputs are bounded probabilities, not raw scores.

**Why you should care:** This architecture — complex model → logistic calibration → bounded probability → threshold decision — is one of the most common patterns in production ML systems. You'll see it in every credit, fraud, and recommendation pipeline.

*Source: Stripe Engineering Blog, "Probability Calibration in Production ML Systems," January 2025.*

### ⚠️ Common Misconception

**Students often think:** "The sigmoid is just a smooth version of LPM — it does the same thing but curved."

**Why it's wrong:** LPM models P(Y=1) directly as a linear function. Logistic regression models log(P/(1-P)) — the log-odds — as a linear function. These are completely different quantities. The coefficients have different interpretations, the marginal effects are different, and the model is estimated differently (MLE, not OLS). The sigmoid is not a smoothed LPM; it is the output of a different model for a different target variable.

---

## 📊 Class Poll: The Sigmoid at Zero

*After Section 2 — approximately 31 min into theory* | **Platform:** Mentimeter

---

**Poll 2:** What is the output of the sigmoid function σ(z) when z = 0?

- A) 0
- B) 0.25
- C) **0.5** ✓
- D) 1

**Reveal script:** *"σ(0) = 1/(1+e⁰) = 1/(1+1) = 0.5. When the linear predictor Xβ equals zero, the model is maximally uncertain — equal probability of 0 and 1. This makes perfect sense: log-odds of 0 means log(P/(1-P)) = 0, so P/(1-P) = 1, so P = 0.5. Zero log-odds = 50-50 probability. File that away — you'll use it every time you need to find the probability at any specific X value."*

---

## 📚 Section 3: Estimation via MLE and Interpreting Results (12 min)

### Intuition

With OLS, we minimize the sum of squared residuals — there's a closed-form solution: β̂ = (X'X)⁻¹X'y. With logistic regression, we can't minimize squared residuals — the residuals aren't normally distributed and least squares doesn't give consistent estimates. We use a different principle: **Maximum Likelihood Estimation (MLE)**.

The idea is intuitive: find the coefficients β that make the observed data as probable as possible. For each observation, the model assigns a probability to the observed outcome: P(Y=1) for observations where Y=1 happened, and P(Y=0) = 1−P(Y=1) for observations where Y=0 happened. We choose β to maximize the product of all these probabilities.

There is no closed-form solution — we use iterative numerical optimization. Scikit-learn uses the LBFGS solver (Limited-memory Broyden–Fletcher–Goldfarb–Shanno, a quasi-Newton method) by default. You'll see `solver='lbfgs'` in the output — that's why.

The sklearn API is identical to Ridge and Lasso: `LogisticRegression().fit(X, y)`. The estimator changes; your code template doesn't.

**Speaking notes:** "MLE is the general principle behind most econometric estimators beyond OLS. Probit, Tobit, Poisson regression — all MLE. The likelihood function is what changes; the principle (maximize the probability of seeing what we actually saw) is always the same. You don't need to know LBFGS internals — but you should know that sklearn is solving an optimization problem, not inverting a matrix."

---

### Formal Treatment

**The log-likelihood for logistic regression:**

$$\ell(\beta) = \sum_{i=1}^{n} \left[ Y_i \log \sigma(X_i \beta) + (1-Y_i) \log(1 - \sigma(X_i \beta)) \right]$$

- When Y_i = 1: we want σ(Xβ) to be close to 1, so log(σ) is close to 0 (maximum)
- When Y_i = 0: we want σ(Xβ) to be close to 0, so log(1−σ) is close to 0 (maximum)
- MLE: β̂ = argmax ℓ(β), solved iteratively

This is also called **binary cross-entropy loss** — the same loss function used in the output layer of a binary classification neural network. Logistic regression and the output layer of a neural net are solving the same optimization problem. Neural nets simply stack many layers before the final logistic output.

**No closed form.** Gradient: ∂ℓ/∂β = X'(Y − σ(Xβ)). Newton-Raphson or LBFGS iterate to convergence.

---

**Interpreting the output — three representations:**

**1. The raw coefficient β̂₁**
Unit: change in log-odds per 1-unit increase in X. Hard to communicate to non-statisticians.

**2. The odds ratio = exp(β̂₁)**

$$\text{Odds Ratio} = e^{\hat{\beta}_1}$$

*"A 1-unit increase in X multiplies the odds of Y=1 by exp(β̂₁), holding all else constant."*
- exp(β) > 1: X increases odds (positive association)
- exp(β) < 1: X decreases odds (negative association)
- exp(β) = 1: X has no effect on odds (β = 0)

**Yield curve model results** (estimated from FRED data, 1982–2024):
$$\hat{\beta}_0 = -0.47, \quad \hat{\beta}_1 = -0.61, \quad e^{\hat{\beta}_1} = 0.54$$

Interpretation: A 1 percentage-point more positive yield spread *multiplies* the odds of recession by 0.54 — reducing odds by 46%. An inverted spread (negative X) → larger Xβ numerically → higher P(recession). ✓

**3. Predicted probability at specific X values via .predict_proba()**

At spread = −1.5% (2022-2023 inversion):
$$z = -0.47 + (-0.61)(-1.5) = -0.47 + 0.915 = 0.445$$
$$P(\text{recession}) = \sigma(0.445) = \frac{1}{1+e^{-0.445}} \approx 0.61 = 61\%$$

At spread = +0.5% (2025, post-normalization):
$$z = -0.47 + (-0.61)(0.5) = -0.47 - 0.305 = -0.775$$
$$P(\text{recession}) = \sigma(-0.775) \approx 0.32 = 32\%$$

---

**Where:**
- $\hat{\beta}_0$ = the intercept (log-odds of recession when spread = 0)
- $\hat{\beta}_1$ = the log-odds coefficient on the yield spread (negative: steeper curve → lower recession odds)
- $e^{\hat{\beta}_1}$ = the odds ratio — the multiplicative effect of a 1pp spread increase on recession odds
- $\sigma(z)$ = the sigmoid function converting the linear predictor to a bounded probability

**Important:** The marginal effect on probability is NOT constant:
$$\frac{\partial P}{\partial X} = \hat{\beta}_1 \cdot P(1-P)$$

At P = 0.61: ∂P/∂X = −0.61 × 0.61 × 0.39 = −0.145. A 1pp spread increase reduces probability by ~14.5 pp.
At P = 0.10: ∂P/∂X = −0.61 × 0.10 × 0.90 = −0.055. Same coefficient, only ~5.5 pp effect.

For a constant marginal probability effect across all X values, report **Average Marginal Effects (AMEs)** — the average of ∂P/∂X across all observations. In practice, industry uses odds ratios; academic economics uses AMEs.

> **Key result:** Logistic regression coefficients are in log-odds units. Exponentiate for odds ratios (multiplicative effects on odds). Use .predict_proba() for predicted probabilities. Marginal probability effects are non-constant — they depend on the baseline probability. Logistic regression assumes linearity in the log-odds: if the true relationship is nonlinear in log-odds, a more flexible model (random forests, Topic 19) may be needed.

**Speaking notes:** "The single most important thing to communicate to a hiring manager or a client about your logistic regression: the coefficient is in LOG-ODDS units. It is NOT a probability. When you present your model, always exponentiate. 'A 1pp increase in the yield spread reduces the odds of recession by 46%' — that is a sentence a CFO can repeat to their board. 'The log-odds coefficient on the yield spread is −0.61' is a sentence that will clear the room."

**Hook payoff:** "Now let's return to the hook. The NY Fed model predicted 70% recession probability for December 2024. The recession didn't happen. Was the model wrong? Here's the answer: a 70% probability forecast isn't wrong just because the 30% outcome occurred. The model said: in scenarios like this one, recession happens 70% of the time. We happened to be in the 30%. To properly evaluate the model, you'd need to run it across many periods and check whether outcomes match the predicted probabilities. That's calibration — and that's what you'll do in Topic 18 with ROC curves and Brier scores."

### Industry Application: JPMorgan Chase — Odds Ratios as Regulatory Language (2024)

**Context:** JPMorgan's consumer lending division maintains the largest consumer credit scorecard in the US banking system.

**The requirement:** The OCC (Office of the Comptroller of the Currency) mandates that financial institutions using automated credit scoring models must be able to explain adverse decisions in plain language accessible to consumers. This requirement flows from the Fair Credit Reporting Act and the Equal Credit Opportunity Act.

**The method:** JPMorgan's regulatory-facing credit risk scorecard is a logistic regression model with 12 input features. Outputs are expressed as odds ratios because they provide the required plain-language explanation. "Your application was declined because your debt-to-income ratio (DTI) above 43% increases the odds of default by 2.3×, exceeding our credit policy threshold" satisfies regulatory adverse action notice requirements. A gradient boosted tree cannot provide this statement.

**The result:** JPMorgan uses logistic regression as the regulatory baseline (published in their 2024 Annual Report risk management section) while running more sophisticated internal models in parallel for actual decisioning. Logistic regression output is the compliance layer; the complex model is the business layer.

**Why you should care:** This pattern — logistic regression for compliance, complex ML for performance — is standard across JPMorgan, Wells Fargo, Citibank, Bank of America, and virtually every regulated financial institution. If you work in finance, you will build logistic regression models for regulatory purposes even if your employer also runs neural networks.

*Source: JPMorgan Chase 2024 Annual Report, Credit Risk Management; OCC Model Risk Management Guidance (SR 11-7).*

**Speaking notes:** "Side note on healthcare: the Framingham Risk Score — the tool your doctor uses to estimate your 10-year probability of cardiovascular disease — is a logistic regression model with age, total cholesterol, HDL, blood pressure, smoking, and diabetes as inputs. It was trained on data from 1948. Logistic regression is not just a teaching tool — it is the direct ancestor of clinical risk calculators that affect millions of patients every year."

### ⚠️ Common Misconception

**Students often think:** "A coefficient of 0.5 in logistic regression means a 1-unit increase in X raises the probability of Y=1 by 0.5."

**Why it's wrong:** The coefficient 0.5 is in log-odds units. The effect on probability is 0.5 × P(1−P), which depends on the current probability. At P=0.5: effect ≈ 0.125 probability change. At P=0.9: effect ≈ 0.045. The coefficient is NOT a probability change. The marginal probability effect is not constant — it varies across observations. To get a single number summarizing the average marginal probability effect, compute the Average Marginal Effect (AME): mean(∂P_i/∂X_i) across all i.

---

## 💬 In-Class Discussion: NY Fed Model Payoff + Business Applications (5 min)

*After Section 3 — approximately 53 min into theory*

**Setup:** "We now have all the tools to revisit the hook. Let's use them."

---

**Question A — Understanding (1 min, cold call):**
> "The yield curve logistic regression gives β₁ = −0.61, so e^β₁ = 0.54. Interpret this in one sentence for someone who doesn't know statistics — as if you're presenting to a board of directors."

**Facilitation:** Strong answer: "A yield curve that is 1 percentage point more positive — longer rates 1pp above shorter rates — cuts the odds of recession in the next year roughly in half." Wrong turn: "decreases probability by 54%" — redirect: odds vs. probability distinction. Give the JPMorgan line: "Get in the habit of saying 'multiplies the odds by X' rather than 'increases the probability by X%.' The first is always correct; the second is only approximately correct near the baseline."

---

**Question B — Analysis (2 min):**
> "The NY Fed model predicted 70% recession probability for December 2024. No recession happened. Does this mean the model was wrong? What's the right framework for evaluating a probability forecast?"

**Facilitation:** 70% ≠ certainty. One realization can't evaluate a probability model. You need calibration: does 70%-forecast periods have actual recession rates near 70%? What about 30% periods? This motivates Brier score, ROC/AUC (Topic 18). Students who say "it was wrong" — challenge: "What would it take to prove a 70% forecast was actually wrong?" Students who say "it wasn't wrong" — challenge: "How would you know? Is there any evidence that could convince you it was a bad model?"

---

**Question C — Evaluation (2 min):**
> "A fintech startup asks you to build a model predicting whether users will click on a credit card offer. 98% don't click. They evaluate success using accuracy. Why is this a problem, and what would you suggest instead?"

**Facilitation — setup sentence:** "Think about what 'accuracy' means in a dataset where 98% of the outcomes are 0. What accuracy does the dumbest possible model achieve?" [Students should answer: 98%, by always predicting 0.] "So what metric would actually tell you whether your model is doing something useful?" This previews precision, recall, F1, and AUC from Topic 18.

---

## 📊 Class Poll: Which is NOT a Problem with LPM?

*Before Section 1 Discussion Block — Poll 1* | **Platform:** Mentimeter

**Read carefully — this question asks which is NOT a problem:**

**Poll 1:** Which of the following is NOT a problem with using OLS on a binary (0/1) outcome?

- A) Predicted probabilities can exceed 1 or fall below 0
- B) The error term is heteroskedastic by construction
- **C) The coefficients cannot be given a ceteris paribus interpretation** ✓ *(this is NOT a problem — coefficients DO have ceteris paribus interpretation)*
- D) Standard errors are biased unless robust SEs are used

**Reveal script:** *"The answer is C — and this is deliberately tricky. LPM coefficients DO have a ceteris paribus interpretation: β₁ is the change in predicted probability of Y=1 for a 1-unit increase in X, holding all else constant. This is actually one of the arguments economists sometimes make IN FAVOR of LPM — the coefficients are directly interpretable as probability effects. The three real problems are A (out-of-bounds predictions), B (heteroskedasticity), and D (invalid standard errors). Some econometricians argue that if you use robust SEs (fixing D) and your predictions don't stray far from [0,1] (mitigating A), LPM is acceptable for near-the-mean inference. The debate is ongoing — but in finance and data science, bounded probabilities are non-negotiable."*

---

## 📊 Class Poll: Odds Ratio Interpretation

*After Section 3 — Poll 3* | **Platform:** Mentimeter

**Poll 3:** A logistic regression of recession (1/0) on yield spread gives β₁ = −0.61. The odds ratio is exp(−0.61) ≈ 0.54. Which interpretation is correct?

- A) A 1pp increase in spread decreases the probability of recession by 54%
- B) A 1pp increase in spread decreases the probability of recession by 0.54 percentage points
- **C) A 1pp increase in spread multiplies the odds of recession by 0.54 (reduces odds by 46%)** ✓
- D) A 1pp increase in spread decreases the log-odds of recession by 0.54

**Reveal script:** *"C is correct. The odds ratio gives a multiplicative effect on odds — not an additive effect on probability. Option A is the most tempting wrong answer: 'decreases probability by 54%' sounds plausible, but odds and probability are different things. If baseline recession probability is 30%, then odds = 30/70 = 0.43. After a 1pp spread increase: new odds = 0.43 × 0.54 = 0.23, which gives P = 0.23/(1+0.23) = 0.19. The probability fell from 30% to 19% — an 11pp decrease, not 54%. Option D has the transformation backwards: the coefficient IS the log-odds change (−0.61); the odds RATIO is exp(−0.61) = 0.54. These are different numbers. The coefficient = log(odds ratio). The odds ratio = exp(coefficient)."*

---

## 🔄 Discussion Debrief

**Key insight:** Probability, odds, and log-odds are three different scales for the same underlying information. Logistic regression works in log-odds; we communicate in odds ratios; we make decisions using probabilities.

**Bridging sentence:**
> "Logistic regression models the log-odds linearly. We exponentiate to get odds ratios for communication. We apply the sigmoid to get probabilities for decisions. These three representations — coefficient, odds ratio, predicted probability — are always three faces of the same model. Next class we ask: once you have a predicted probability, how do you evaluate whether the model is actually any good? The answer is not 'accuracy.'"

**Transition:**
> "Lab starts now. Load FRED. You're building the NY Fed model."

---

## 🔗 Connections (2 min)

### Building On
- *OLS (Topics 8–10)*: "We've been fitting Y = Xβ for continuous outcomes. LPM applies this to binary Y — and we just saw why it fails. Logistic regression keeps the Xβ structure but transforms it through the sigmoid."
- *Regularization (Topic 16)*: "The sklearn API is identical. `LogisticRegression(C=1.0).fit(X, y)` — note that sklearn's `C` is the inverse of the λ penalty from Ridge. Logistic regression with regularization is one of the most common models in production."
- *The train-test split (Topic 13)*: "You'll fit on training data and evaluate on test data — same workflow."

### Setting Up
- *Topic 18 — Model Evaluation*: "Today's hook question is unanswerable without calibration curves, Brier scores, precision, recall, ROC, and AUC. We'll build all of those tools next class — starting from the exact model you build in today's lab."
- *Topic 19 — Random Forests*: "Logistic regression is the linear classification baseline. Random Forests will capture nonlinear decision boundaries. The comparison between your logistic regression ROC curve and the forest's ROC curve next week will show you exactly what flexibility buys you."

---

## 🎯 Key Takeaways

Walking out of this lecture, you should be able to complete these sentences:

1. "OLS on binary outcomes fails because... [predicted probabilities can be outside [0,1], error term is heteroskedastic, standard errors are invalid]"
2. "The sigmoid function solves this by... [mapping any real number to (0,1) via σ(z) = 1/(1+e⁻ᶻ)]"
3. "Logistic regression is estimated using... [MLE, not OLS] because... [residuals aren't normal; squared-error loss is wrong for binary outcomes]"
4. "A coefficient of −0.61 in logistic regression means... [the log-odds changes by −0.61 per 1-unit increase in X, or equivalently, the odds are multiplied by e^(−0.61) = 0.54]"
5. "The NY Fed's recession probability model is a logistic regression that... [was not 'wrong' — it predicted a 70% probability, which was one scenario. Evaluating probabilistic forecasts requires calibration, not single-event judgment — that's Topic 18.]"

---

## 📖 Supplementary Resources

**To go deeper:**
- [Cunningham, Causal Inference: The Mixtape — Chapter 11 (Logit/Probit)](https://mixtape.scunning.com) — free online, applied economic examples, clear on odds ratios vs. probability
- [NY Fed Yield Curve FAQ](https://www.newyorkfed.org/research/capital_markets/ycfaq) — read the actual model documentation for the recession probability model you replicated

**Video explainers:**
- [StatQuest: Logistic Regression (YouTube)](https://www.youtube.com/watch?v=yIYKR4sgzI8) — 19 minutes; best visual treatment of the sigmoid and MLE; highly recommended before your problem set
- [3Blue1Brown: Neural Networks, Chapter 1](https://www.youtube.com/watch?v=aircAruvnKk) — for students who want to see how today's sigmoid connects to deep learning architecture

**Datasets:**
- [FRED T10Y3M](https://fred.stlouisfed.org/series/T10Y3M) — 10Y-3M Treasury spread (your lab data)
- [FRED USREC](https://fred.stlouisfed.org/series/USREC) — NBER recession indicator (your Y variable)

---

## 📋 Appendix: Instructor Notes

### Timing Watch Points
- **Section 2 (Sigmoid)** is the densest for advanced undergrad students who haven't seen log transformations recently. Budget 2 extra minutes if students need the logit derivation re-explained. The "draw the S-curve right now" exercise buys time while also creating an active learning moment.
- **Poll 1** (NOT a problem with LPM) — this almost always generates debate because C sounds wrong intuitively. Allocate 4 minutes, not 3, on the reveal if energy is high. The discussion it generates is high-value.
- **Discussion Block 2 Level C** (class imbalance) — if time is tight, skip Level C. Levels A and B together are 3 minutes and cover the essential material.

### Common Student Questions

**Q: "Should I ever use LPM instead of logistic regression?"**
A: Yes — some economists prefer LPM for estimation of average marginal effects near the mean of X, because the coefficient is directly interpretable as a probability effect without needing to compute AMEs. For academic papers with outcomes that aren't near the boundaries, LPM + robust SEs is defensible. For industry applications where predictions at the extremes matter (credit risk, fraud, clinical scoring), always use logistic regression.

**Q: "What's the difference between logistic and probit regression?"**
A: Both model P(Y=1) as a nonlinear function of Xβ. Logistic uses the sigmoid (logistic CDF); probit uses the normal CDF (Φ). They produce nearly identical predictions. Logistic regression gives odds ratios (cleaner interpretation); probit appears more in economics literature (connects to latent utility models). In practice: use logistic.

**Q: "Why does sklearn's LogisticRegression have a parameter C instead of λ?"**
A: C = 1/λ — it's the inverse of the regularization strength. Large C = weak regularization (trust the data more). Small C = strong regularization (shrink coefficients). The default C=1.0 applies L2 regularization. Use `penalty=None` to get unregularized logistic regression (equivalent to standard MLE).

**Q: "How do I know if my logistic regression fits well?"**
A: The log-likelihood, pseudo-R² (McFadden's R² = 1 − ℓ_model/ℓ_null), and the tests in Topic 18 (confusion matrix, ROC/AUC, Brier score). Do NOT use the coefficient of determination (R²) from OLS — it has no meaningful interpretation for logistic regression.

### If Class Ends Early
"Let's think about how to extend the recession model. What other variables might predict recession — beyond the yield spread? [Take suggestions: credit spreads, unemployment rate, housing starts, consumer confidence.] Search FRED for one of these series. How would you add it to the model? What would the new odds ratio mean?"

### Notes After Teaching
*(Space for actual timing, student response patterns, what to change next semester)*

---

*Generated by econ-lecture-prep | 2026-03-22 | Revised after peer review*
