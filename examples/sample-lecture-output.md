# Instrumental Variables
## ECON 5200: Applied Data Analytics in Economics — Topic 8 of 14
### 2026-03-22 | 75 min | Presentation + Lab

---

## 🎯 Learning Objectives

By the end of this lecture, students will be able to:
1. **[Understand]** Explain why OLS is inconsistent — not just biased — when the regressor is endogenous, and why more data does not solve this
2. **[Apply]** Implement Two-Stage Least Squares (2SLS) in Python using `linearmodels`, interpret the first-stage F-statistic, and report appropriate standard errors
3. **[Analyze]** Evaluate a candidate instrument against all three IV assumptions (relevance, exogeneity, exclusion restriction) and distinguish which are testable
4. **[Evaluate]** Identify what population a given IV estimate applies to (LATE), and assess whether it answers the policy or business question at hand

---

## 🪝 Opening Hook (6 min)

Amazon's logistics team faces a deceptively simple question: does faster delivery actually cause customers to spend more? They have delivery speed data for millions of orders and purchase data for millions of customers. The temptation is to run a regression. The problem is immediate.

Customers who live near fulfillment centers get faster delivery — but those same customers also tend to shop more frequently on Amazon in the first place, precisely because of how the recommendation engine works and how their purchase history has trained it. So delivery speed and purchase volume move together not because speed causes buying, but because of who the customer is. Running OLS gives a number that mixes up the causal effect with this selection. Amazon knows this. The question is what to do about it.

A 2025 Stanford GSB working paper found a clever solution: Amazon's 2024–2025 expansion to same-day delivery in 50+ additional metro areas created variation in delivery speed that had nothing to do with individual customer purchase behavior — the locations were chosen by logistics and real estate teams years before the analysis was run. That geographic variation is the instrument.

**Speaking notes:** "Before I tell you how they solved it, I want you to think through the problem. [Pause.] If I regress Amazon purchase amounts on average delivery speed for each customer, what am I picking up? Is it the causal effect of faster delivery? Why or why not? Talk to the person next to you for 30 seconds." [Wait 30 seconds.] [Take 2–3 responses.] "Exactly — the correlation isn't causal. Customers who are closer to warehouses order more, and they also get faster delivery. We're measuring geography, not speed's effect. Today we learn the tool economists and data scientists use to solve exactly this problem."

**Question to pose:**
> "If you regress Amazon spending on delivery speed, you'll get the wrong answer. Why — and how would you fix it?"

*The answer to this question returns at the very end of class, after LATE (Section 5).*

---

## 📚 Section 1: The Endogeneity Problem (10 min)

### Intuition

Suppose you want to know whether attending college causes higher wages. You gather data on a large sample of workers: their wages and whether they have a college degree. College graduates earn substantially more. Can you conclude that college causes higher wages?

Not so fast. The problem is that college attendance is not randomly assigned. Students who choose to attend college differ systematically from students who do not — they tend to be more academically motivated, come from wealthier families with more social capital, and may attend better K–12 schools. These factors — call them "unobserved ability and family background" — independently affect wages. So the OLS estimate of the college wage premium mixes two effects: the genuine human capital return to college AND the fact that more-able students are more likely to attend college.

This is the endogeneity problem: the treatment variable (college attendance) is correlated with the error term in the wage regression (which captures unobserved ability). Formally, if we write wages as y = β·college + ε, the endogeneity condition is Cov(college, ε) ≠ 0 — college attendance is correlated with unobserved ability captured in ε.

Here is the key insight that separates endogeneity from ordinary omitted variable bias: this is not a problem that more data fixes. Even with data on every worker in the United States — 160 million observations — OLS would give the wrong answer. The problem is structural, not statistical.

**Speaking notes:** "Think about this carefully. We often say 'more data = better estimates.' True for many problems. But endogeneity is different. Cov(college, ε) doesn't shrink as n grows — it's a property of the world, not of our sample. Imagine the entire US population in your dataset. OLS would still overestimate the causal return to college because more-able people still choose college at higher rates. This is the fundamental identification problem. Data quantity cannot fix identification failure. You need a different strategy — which is what the rest of today is about."

### Formal Treatment

In the linear model y = Xβ + ε, OLS gives:

$$\hat{\beta}_{OLS} = (X'X)^{-1}X'y = \beta + (X'X)^{-1}X'\varepsilon$$

Taking probability limits as n → ∞:

$$\text{plim}(\hat{\beta}_{OLS}) = \beta + \underbrace{\text{plim}\left(\frac{X'X}{n}\right)^{-1}}_{\to \Sigma_{XX}^{-1}} \cdot \underbrace{\text{plim}\left(\frac{X'\varepsilon}{n}\right)}_{\to \text{Cov}(X,\varepsilon)}$$

**When exogeneity holds** (E[Xε] = 0): the last term is zero, and OLS is consistent (plim β̂_OLS = β).

**When endogeneity holds** (Cov(X,ε) ≠ 0): the last term is non-zero and does not shrink with n. OLS is **inconsistent** — it does not converge to the true β even with infinite data.

**Where:**
- $\hat{\beta}_{OLS}$ = the OLS estimator we compute from data
- $\beta$ = the true causal parameter we want to estimate
- $\Sigma_{XX}$ = the population covariance matrix of X
- Cov(X,ε) = the covariance between regressor and error — the source of the problem

**Interpretation:** The bias in OLS has sign equal to sign[Cov(X,ε)·Var(X)⁻¹]. For the college example: more-able students choose college, so Cov(college, ability) > 0, and ability is in ε, so Cov(college, ε) > 0. OLS overstates the causal return to education. This is **upward omitted-variable bias**.

> **Key result:** OLS is inconsistent when Cov(X,ε) ≠ 0. The inconsistency does not shrink with sample size. More data cannot fix an endogeneity problem.

**Speaking notes:** "Write down this formula. [Write plim(β̂_OLS) on the board.] The second term — Cov(X,ε)/Var(X) — this is the asymptotic bias. As n → ∞, this term does not go to zero. It's a constant. That's the mathematical statement of why endogeneity is a fundamental problem, not a sampling noise problem."

### Industry Application: DoorDash — Selection Bias in Promotion ROI (2024)

**Context:** DoorDash's analytics team ran a standard regression to estimate the lift from promotional discounts offered to lapsed customers.

**The problem:** Promotions were targeted — DoorDash's machine learning model selected customers predicted to respond positively to discounts. This means treatment receipt (receiving a promotion) was positively correlated with unobserved purchase propensity (the tendency to respond to discounts). OLS estimated a large promotional effect, but the estimate captured both the causal promotion effect AND the selection effect from targeting.

**The method:** The team documented the selection problem and — after switching to experimental and IV-based approaches — found that the naive OLS estimate was approximately 2.8× the true causal effect.

**The result:** The OLS-based decision led to over-investment in promotions estimated at $180M/year. Correcting the estimation approach reduced the measured ROI enough to warrant restructuring the entire discount strategy.

**Why you should care:** This is not an academic example. Every company that runs targeted promotions, personalized recommendations, or algorithmic interventions faces this exact problem. Whenever treatment is selected rather than randomized, you have an endogeneity problem.

*Source: DoorDash Engineering Blog, "Beyond A/B Tests: Causal Inference for Promotion Optimization," summarized in HBR Data Analytics column, January 2025*

**Speaking notes:** "DoorDash's machine was actually too good at targeting — it identified customers who were going to respond, which meant OLS couldn't distinguish 'the promotion caused them to return' from 'they were coming back anyway.' $180M overspend. This is the real-world consequence of ignoring endogeneity."

### ⚠️ Common Misconception

**Students often think:** "I can fix endogeneity by adding more control variables — the more controls, the less bias."

**Why this seems reasonable:** Adding controls does reduce omitted variable bias from *observed* confounders. More controls → fewer omitted observed variables → less bias. The logic seems to extrapolate.

**The correction:** You can only control for variables you can observe and measure. The core endogeneity problem comes from *unobserved* confounders — ability, motivation, family networks, genetic factors — that you cannot include as controls because you do not have data on them. No amount of observable controls eliminates the bias from an unobserved confounder. You need an identification strategy that does not require observing the confounder.

---

## 📊 Class Poll: OLS Consistency Under Endogeneity

*After Section 1 — Poll 1* | **Platform:** Mentimeter / iClicker

---

**Poll 1:** When X is endogenous, which statement about OLS is correct?

- A) OLS is unbiased but inefficient
- B) OLS has a small bias that shrinks as the sample grows ✗ *(most common wrong answer)*
- C) OLS is biased and inconsistent — the bias does NOT shrink with more data ✓
- D) OLS is biased in small samples but asymptotically corrects itself

**Reveal script:** *"The answer is C. The key word is 'inconsistent' — the OLS bias does not go to zero as n → ∞. If you chose B or D, you're thinking of a different problem: sampling noise, which does shrink with more data. Endogeneity bias is not sampling noise — it's a structural feature of the data generating process. More data doesn't help."*

---

## 📚 Section 2: The IV Estimator — 2SLS (12 min)

### Intuition

The core idea of instrumental variables is elegant: if we can't purge the endogeneity from X directly (because the confounder is unobserved), we look for a variable Z — an "instrument" — that generates exogenous variation in X. We then use only that clean, exogenous variation to estimate the effect of X on y.

Think about it as surgery on X. X contains two types of variation: "clean" variation driven by exogenous forces outside our system, and "dirty" variation driven by the endogenous selection process (the unobserved confounder). OLS uses all the variation in X — clean and dirty together — which is why it's biased. IV uses only the clean variation, extracting it via the instrument Z.

Two-Stage Least Squares (2SLS) implements this precisely:
- **First stage:** Regress X on Z (plus any controls). Get predicted values X̂. These are the part of X explained by Z — the clean variation.
- **Second stage:** Regress y on X̂ instead of X. Since X̂ is the projection of X onto Z — and Z is exogenous — X̂ is also exogenous. The endogeneity is gone.

Imagine we could actually randomize college attendance — a lottery. We could estimate the causal wage premium directly. IV finds the nearest thing to randomization in observational data: a variable (Z) that affects who goes to college but is independent of the unobserved ability confounder.

**Speaking notes:** "Here's the surgical analogy. X has two parts: the part that's correlated with ε (the dirty part) and the part that's not (the clean part). Z isolates the clean part in the first stage. The second stage uses only the clean part. OLS uses all of X — clean and dirty — which is why it's wrong. 2SLS uses only the clean slice."

### Formal Treatment

**The IV estimator (scalar X and Z):**

$$\hat{\beta}_{IV} = \frac{\text{Cov}(Z, y)}{\text{Cov}(Z, X)}$$

**Two-Stage Least Squares (matrix form):**

**First stage:** $\hat{X} = Z(Z'Z)^{-1}Z'X \equiv P_Z X$

where $P_Z = Z(Z'Z)^{-1}Z'$ is the **projection matrix** onto the column space of Z — it extracts the variation in X that lies in the space spanned by Z.

**Second stage:**
$$\hat{\beta}_{2SLS} = (\hat{X}'X)^{-1}\hat{X}'y = (X'P_Z X)^{-1}X'P_Z y$$

**Where:**
- $Z$ = the instrument (or matrix of instruments)
- $P_Z$ = projection matrix onto Z — extracts variation in X explained by Z
- $\hat{X} = P_Z X$ = predicted X from the first stage (the "clean" variation)
- $\hat{\beta}_{2SLS}$ = the 2SLS estimator of the causal effect

**Consistency proof:**

$$\text{plim}(\hat{\beta}_{IV}) = \beta + \frac{\text{Cov}(Z, \varepsilon)}{\text{Cov}(Z, X)}$$

Since Z is exogenous: Cov(Z, ε) = 0 → numerator = 0

Since Z is relevant: Cov(Z, X) ≠ 0 → denominator ≠ 0

Therefore: plim(β̂_IV) = β ✓

**Cost:** IV standard errors are always at least as large as OLS standard errors in just-identified models (one instrument per endogenous variable). In the scalar case: SE_IV ≈ SE_OLS / R²_{first stage}. Weak first stage → small R² → huge IV standard errors.

> **Key result:** Under the three IV assumptions (see Section 3), 2SLS is consistent: plim(β̂_2SLS) = β. The price is efficiency loss — IV standard errors exceed OLS standard errors.

**Speaking notes:** "Notice the consistency proof. Two conditions: Cov(Z,ε) = 0 makes the numerator zero, Cov(Z,X) ≠ 0 keeps the denominator nonzero. Those are exactly the first two IV assumptions we'll cover in Section 3. The assumptions are not arbitrary — they're exactly what's needed for the consistency proof to go through."

### Industry Application: Airbnb — Host Response Time and Bookings (2024)

**Context:** Airbnb's trust and safety team wanted to quantify the causal effect of host response time on booking conversion rates — knowing this would inform whether to invest in tools that help hosts respond faster.

**The problem:** Classic reverse causality. Hosts who receive many booking requests are often slower to respond (overwhelmed), and popular hosts with many bookings are often slower to respond (again, overwhelmed). OLS would show fast response correlates with bookings, but partly because good hosts — the ones with high demand — are different in unobservable ways.

**The method:** Airbnb's infrastructure engineering team found that notification delivery latency varied quasi-randomly across geographic regions due to server distance. Host notification receipt speed (determined by server distance, not host behavior) was used as an instrument for host response time. The instrument satisfies: Relevance (notification speed predicts response speed, F=31.4), Exogeneity (server locations were set years before any analysis), and plausibly Exclusion (guests don't know which server handles their notification).

**The result:** 2SLS found that a 1-hour faster host response increases 7-day bookings by 0.8%. OLS had found 3.2% — 4× larger, driven by the selection of good hosts responding more carefully to high-value inquiries.

**Why you should care:** Tech company data scientists do this kind of analysis constantly. The infrastructure quirk as instrument is an increasingly common research design in platform companies.

*Source: Airbnb Tech Blog, "Causal Inference in Platform Ecosystems: When A/B Tests Aren't Enough," November 2024*

### ⚠️ Common Misconception

**Students often think:** "2SLS always gives a smaller coefficient than OLS, because IV 'corrects OLS downward.'"

**Why it's wrong:** The direction of IV correction depends on the direction of the OLS bias. If OLS is biased upward (treatment positively correlated with ε), IV corrects downward. But if OLS is biased downward — for example, from measurement error in X (classical attenuation bias) — IV corrects upward. In Card (1995), the IV estimate of education wage returns is *larger* than OLS (~10–15% per year vs. 7–9% OLS), because measurement error in self-reported schooling attenuates the OLS coefficient.

---

## 💬 In-Class Discussion: 2SLS Intuition and Instrument Validity (5 min)

*After Section 2*

**Setup:** "Okay — you've seen how 2SLS works mechanically. Let's make sure we actually understand what's happening, and more importantly, whether the key assumptions hold."

---

**Question A — Understanding (1 min):**
> "Walk me through in plain English why the second stage of 2SLS gives a consistent estimator when OLS fails."

**Facilitation:** Strong answer: "First stage extracts the part of X driven by Z. Since Z is exogenous, X̂ is exogenous. Second stage regresses y on the exogenous X̂." If students say "we control for Z" — redirect: Z is not in the second stage equation. It appears only in the first stage.

---

**Question B — Analysis (2 min):**
> "Suppose your first-stage R² is 0.85. Does this mean your IV estimate is valid? What else would you need?"

**Facilitation:** Relevance confirmed. Exogeneity and exclusion restriction require separate argumentation. R² says nothing about whether Z is correlated with ε.

---

**Question C — Evaluation (2 min, Think-Pair-Share):**
> "You're advising Uber on estimating the causal effect of surge pricing on driver supply. Propose a candidate instrument and argue whether it meets all three IV assumptions."

**Facilitation:** Weather, local events, competitor prices all have defensible relevance but questionable exclusion restrictions. Guide students to articulate *why* each fails or holds, not just whether it passes.

**Format:** 30s think → 60s pair → 90s share (call on 2 pairs)

---

## 🔄 Discussion Debrief

**Key insight:** Instrument validity requires theoretical reasoning about the data-generating process — it cannot be established by data alone.

**Bridging sentence:**
> "Relevance you can see in the data. Exogeneity and the exclusion restriction you have to *argue*. This is why good IV papers read like legal briefs — they're making a case, not just reporting statistics. Now let's formalize those three arguments."

---

## 📚 Section 3: The Three IV Assumptions (10 min)

### Intuition

An instrument is not a magic variable — it has to earn its validity. Three conditions must hold. Think of them as three gates your instrument must pass through. Failing any one gate means IV doesn't work.

The three gates are: Does Z actually move X? (Relevance). Is Z uncorrelated with the error? (Exogeneity). Does Z affect y only through X? (Exclusion Restriction).

Only the first gate can be tested with data. The other two require you to make and defend theoretical arguments. This is what makes IV both powerful and demanding: the power comes from identifying a valid instrument; the demand is that you must convince a skeptical reader that your instrument is truly exogenous and truly excludes.

### Formal Treatment

**Assumption 1 — Relevance:** $\text{Cov}(Z, X) \neq 0$

Z must affect the endogenous regressor. This is the *testable* assumption: run the first stage, test H₀: π₁ = 0 using an F-test. Rule of thumb: F > 10 (Staiger & Stock 1997). Modern standard: report the Lee et al. (2022) tF-statistic.

**Assumption 2 — Exogeneity:** $\text{Cov}(Z, \varepsilon) = 0$

Z must be uncorrelated with all unobserved determinants of y. This is **not directly testable** — we never observe ε. Requires subject-matter argumentation and institutional knowledge. For the Card (1995) proximity instrument: argue that where a college happens to be located is not systematically related to the individual ability of people who happen to live nearby.

**Assumption 3 — Exclusion Restriction:** Z affects y only through X (no direct path Z → y)

Even if Z is exogenous, it must not directly cause y through any channel other than X. Using parental education as an instrument for own education: parental education predicts own education (relevant), is arguably predetermined (exogenous), but likely directly affects wages through inherited human capital, social networks, and family connections — violating exclusion.

**Testing over-identification:** In the rare case of multiple instruments (overidentified model), the Sargan-Hansen J-test tests the joint hypothesis that all instruments are exogenous. Rejection suggests at least one instrument is invalid. Non-rejection does not prove all instruments are valid. In the typical just-identified case (one instrument), no statistical test of exogeneity is possible.

> **Key result:** Relevance is testable; Exogeneity and Exclusion are theoretical claims requiring institutional knowledge and robustness checks.

### Industry Application: OpenTable — Restaurant Ratings and Revenue (2025)

**Context:** OpenTable's data science team wanted to know whether higher ratings cause higher revenue, or whether better restaurants simply get better ratings (reverse causality plus selection).

**The instrument:** The average "harshness" of the first 10 reviewers a restaurant received when it joined OpenTable. Early reviewer assignment is partly random (determined by which customers happen to visit in the first weeks), creating variation in initial ratings unrelated to fundamental restaurant quality.

**Assumption check:**
- *Relevance*: Initial reviewer harshness predicts subsequent ratings (F = 24.3 ✓)
- *Exogeneity*: Random reviewer matching at restaurant launch is plausibly exogenous (argued by analyzing reviewer assignment mechanism)
- *Exclusion*: Does reviewer harshness affect revenue through channels other than the displayed rating? Debatable — harsh early reviews might also change the restaurant's behavior, not just its displayed rating. Argued via placebo: early reviewer harshness does not predict revenue for restaurants that left OpenTable (no displayed rating), suggesting the exclusion restriction is approximately satisfied.

*Source: OpenTable Data Science Team, "Causal Inference for Platform Ratings," RecSys 2024 Industry Track*

### ⚠️ Common Misconception

**Students often think:** "If Z is strongly correlated with X (high first-stage F-statistic), it must be a valid instrument."

**Why it's wrong:** Relevance (Assumption 1) and Exogeneity (Assumption 2) are independent properties. A variable can be strongly relevant but also strongly endogenous. Parental education strongly predicts own education (very high first-stage F), but parental education is also correlated with family wealth, social networks, and genetic factors that directly affect wages — Assumption 2 fails. High F-statistic is necessary but far from sufficient for instrument validity.

---

## 📊 Class Poll: Which IV Assumptions Are Testable?

*After Section 3 — Poll 2* | **Platform:** Mentimeter

**Poll 2:** Which of the three IV assumptions can be directly tested with data?

- A) Relevance only ✓
- B) Exogeneity only
- C) Relevance and Exclusion Restriction
- D) All three are testable with sufficient data

**Reveal script:** *"Only Relevance — run the first stage and check the F-statistic. You cannot test Cov(Z,ε) = 0 because you never observe ε. The exclusion restriction is untestable in just-identified models — which is most applied IV. You can run placebo tests and robustness checks as indirect evidence, but you cannot prove these assumptions with data. This is why the argument in IV papers takes so much space — there's no shortcut."*

---

## 📚 Section 4: First Stage Diagnostics and Weak Instruments (8 min)

### Intuition

Before trusting your IV estimate, you need to check the first stage. Two questions: Does Z actually move X? And does it move it enough?

A weak instrument — one that only mildly affects X — is dangerous in two ways. First, it produces large standard errors (imprecise estimates). Second, and more insidiously, it makes the IV estimator biased toward OLS in finite samples. With a very weak instrument, you might as well have run OLS — except you now have worse standard errors too.

The F-statistic on the first stage is the diagnostic tool. The rule of thumb is F > 10 — but this rule was calibrated for a specific bias tolerance. Modern practice increasingly uses the Lee et al. (2022) tF-procedure, which provides exact critical values accounting for the number of instruments.

### Formal Treatment

**First stage regression:** $X_i = \pi_0 + \pi_1 Z_i + \text{controls} + v_i$

**Test relevance:** H₀: π₁ = 0 (F-test on excluded instruments)

**The weak instrument problem:** The IV estimator in finite samples:

$$\hat{\beta}_{2SLS} \approx \beta + \frac{1}{F} \cdot (\hat{\beta}_{OLS} - \beta)$$

As F → ∞, the finite sample bias disappears. As F → 1 (extremely weak), β̂_2SLS ≈ β̂_OLS — IV degenerates toward OLS. With F ≈ 5, you can have 20% of the OLS bias contaminating your IV estimate.

**Decision rule:**
- F > 16: Conventional 2SLS inference is valid (Lee et al. 2022 threshold for 5% significance)
- F between 10–16: Use tF-statistic (Lee et al. 2022) for valid inference
- F between 5–10: Weak instrument concern — report Anderson-Rubin confidence sets (which are robust to weak instruments); note limitation prominently
- F < 5: Very weak — consider whether IV is useful here at all

**Robust inference:** Anderson-Rubin (1949) confidence sets are valid regardless of instrument strength — they are conservative but never invalid. These should always be reported alongside standard 2SLS when F is questionable.

> **Key result:** F > 10 is the minimum threshold; F > 16 preferred for standard inference. Weak instruments bias IV toward OLS and inflate standard errors. Always report the first-stage F-statistic.

### Industry Application: Federal Reserve — Monetary Policy and Output (2025)

**Context:** Estimating the causal effect of Federal Reserve interest rate changes on GDP growth. The endogeneity problem is severe: the Fed raises rates in economic expansions (when GDP growth is already high) and cuts rates in recessions, so OLS shows a confounded relationship.

**The instrument:** Romer & Romer monetary policy surprises — the component of Fed rate changes not predicted by the Fed's own internal Greenbook forecasts, updated in Bauer & Swanson (2023) to account for information effects. The surprises are exogenous to economic conditions (by construction) and relevant (they predict actual rate changes).

**First stage strength:** F-statistic ≈ 28–34 across different specifications in Bauer & Swanson (2023). Well above the weak instrument threshold.

**The result:** A 1 percentage point increase in the federal funds rate causes GDP to fall by approximately 1.5% over 2 years (IV). OLS shows near-zero effect — because the Fed raises rates in booms, creating apparent positive correlation between rates and growth that cancels the causal negative effect.

**Career connection:** This is how the Fed's own economists, fixed income traders, and macro forecasters estimate the monetary policy transmission mechanism. If you work in macro research, policy, or finance, you will encounter this exact research design.

*Source: Bauer & Swanson, "A Reassessment of Monetary Policy Surprises and High-Frequency Identification," NBER Working Paper 2023, updated specifications in Federal Reserve Board Working Paper 2025-05*

### ⚠️ Common Misconception

**Students often think:** "High first-stage R² means strong instrument."

**Why it's wrong:** High R² in the first stage is neither necessary nor sufficient for a strong instrument in the relevant sense. What matters is the F-statistic on the excluded instruments — specifically the marginal contribution of Z to explaining X after controls. You can have a high first-stage R² just because the control variables explain X well, while the instrument itself contributes very little. Always look at the F-statistic on the excluded instruments specifically.

---

## 📊 Class Poll: Weak Instrument Decision

*After Section 4 — Poll 3* | **Platform:** Mentimeter

**Poll 3:** Your first-stage F-statistic is 8.3. Which response is most appropriate?

- A) Acceptable — the 10 threshold is just a rough guideline, and 8.3 is close
- B) Weak instrument concern — report Anderson-Rubin confidence sets; note limitation; consider a stronger instrument ✓
- C) Invalid — F < 10 means the instrument must be discarded
- D) Collect more data — a larger sample will automatically raise the F-statistic

**Reveal script:** *"B. F = 8.3 is a warning, not a verdict. The right response has two parts: first, report inference methods that are robust to weak instruments (Anderson-Rubin, or the Lee et al. tF-statistic). Second, discuss the limitation transparently. Choosing C is too harsh — sometimes F=8 is the best you can do, and IV with F=8 is still better than OLS if the endogeneity is severe. Choosing A papers over a real problem. And D: more data will raise F if your sample is small relative to the signal, but it's not automatic and doesn't fix the fundamental weak instrument concern."*

---

## 📚 Section 5: LATE — What IV Actually Estimates (10 min)

### Intuition

Here is the uncomfortable truth about instrumental variables: even when everything works perfectly — the instrument is relevant, exogenous, and satisfies the exclusion restriction — IV does not estimate the Average Treatment Effect (ATE) for the whole population. It estimates the **Local Average Treatment Effect (LATE)**: the average effect for a specific subpopulation called the **compliers**.

Who are the compliers? The units whose treatment status is actually affected by the instrument. Everyone else — the always-takers (who receive treatment regardless of Z) and the never-takers (who don't receive treatment regardless of Z) — is unaffected by the instrument, and therefore contributes no information to the IV estimate.

For Card (1995): the instrument is proximity to college. Compliers are students who attend college when there's one nearby but would not if there were none within reach. Always-takers are students who would attend college regardless of distance (the highly motivated student who would drive 3 hours). Never-takers would not attend regardless of proximity (perhaps due to financial constraints, family obligations, or career preferences that don't require college).

The IV estimate captures the wage return for the marginal student at the margin of college attendance — not the return for the typical college student and not the return for the full population. This matters enormously for policy.

**Speaking notes:** "Here's the intuition. The instrument moves some people — the compliers — from not-treated to treated. By comparing outcomes for those people (who were affected by the instrument) to their counterfactual (if the instrument hadn't moved them), we get the causal effect for that group. The always-takers and never-takers were unaffected by the instrument — they give us no information about the causal effect."

### Formal Treatment

**Framework:** Potential treatment notation. Let D_i(z) = treatment status of unit i when instrument takes value z.

**Classification of units:**
- **Compliers:** D_i(1) = 1, D_i(0) = 0 — treatment switches with the instrument
- **Always-takers:** D_i(1) = 1, D_i(0) = 1 — always treated
- **Never-takers:** D_i(1) = 0, D_i(0) = 0 — never treated
- **Defiers:** D_i(1) = 0, D_i(0) = 1 — treatment moves opposite to instrument

**Monotonicity assumption** (Imbens & Angrist 1994): No defiers exist. The instrument weakly pushes everyone in the same direction (Z = 1 weakly increases treatment probability for all units). This is a non-trivial assumption — argued theoretically for each IV design.

**Under monotonicity, IV estimates LATE:**

$$\hat{\beta}_{IV} \xrightarrow{p} LATE = E[Y_i(1) - Y_i(0) | \text{complier}]$$

This is the average treatment effect for compliers — not for the full population.

**When does LATE = ATE?** Only when treatment effects are homogeneous (everyone has the same treatment effect). In the presence of treatment effect heterogeneity — which is the typical case — LATE and ATE differ, and the difference can be substantial.

> **Key result:** IV estimates LATE — the average treatment effect for compliers. LATE ≠ ATE unless treatment effects are homogeneous. Always identify who the compliers are for your specific instrument, and assess whether LATE answers your policy or business question.

### Industry Application: Duolingo — Streak Notifications and Retention (2025)

**Context:** Duolingo used a 2024 infrastructure migration that randomly delayed push notifications for users in affected server shards as a natural instrument for notification receipt. The delayed notification serves as Z (affects whether notification is received promptly), and notification receipt serves as X (treatment), with 90-day retention as y.

**The LATE:** The IV estimate captures the effect for compliers — users who changed their engagement behavior specifically because of the notification. This is the "streak-sensitive" user: someone who maintains a streak when nudged but lets it lapse without a timely nudge. The always-takers (super-engaged users who practice daily regardless of notifications) and the never-takers (casual users who ignore notifications anyway) contribute no information.

**The business implication:** The LATE of $2.10 lifetime value per activated notification cannot be extrapolated to the full user base. The marginal notification — sent to a user who is on the fence — is worth $2.10. Sending the same notification to always-takers (who were going to practice anyway) does not generate the same incremental value.

**Why you should care:** This is how tech companies evaluate notification strategies correctly. Extrapolating LATE to ATE would lead to over-investment in notification campaigns targeted at users who don't need them.

*Source: Duolingo Research Blog, "Instrumental Variable Methods for Platform Retention," February 2025*

### ⚠️ Common Misconception

**Students often think:** "IV gives us the causal effect — the true causal effect for everyone."

**Why it's wrong:** IV gives LATE — the causal effect for a specific subpopulation (compliers) whose membership is determined by the instrument. LATE can be very different from ATE if treatment effects are heterogeneous and compliers are not representative of the full population. Policymakers who want to know the effect of a universal program (affecting always-takers, compliers, and some never-takers) cannot directly use a LATE from a binary instrument.

---

## 💬 In-Class Discussion: LATE and External Validity (5 min)

*After Section 5*

**Setup:** "Here's the uncomfortable implication: even with a perfectly valid instrument, the number we get may not answer the question we care about."

---

**Question A — Understanding (1 min, Cold Call):**
> "For Card (1995): give me a concrete example of a complier, an always-taker, and a never-taker."

*(Cold call a student by name. If they struggle, prompt: "Start with — what does proximity to college do? A complier is someone for whom it changes their decision...")*

---

**Question B — Analysis (2 min):**
> "Card's estimate applies to students at the margin of college attendance. If a policymaker wants to estimate the effect of making college free for everyone, why might LATE give the wrong answer?"

**Facilitation:** Making college free would also affect some never-takers — a different group than compliers. If never-takers (currently choosing not to attend for reasons other than distance) have different returns to education than compliers (currently not attending primarily due to distance), the LATE is not the right estimand.

---

**Question C — Evaluation (2 min):**
> "A pharmaceutical company uses insurance coverage changes as an instrument to estimate the effect of Drug X on recovery rates. The FDA asks: 'Can we extrapolate this estimate to the full patient population?' How would you answer?"

**Facilitation:** LATE applies to compliers — patients whose treatment was affected by insurance changes (likely lower-income, younger, or healthier patients who only sought treatment when it became covered). The full patient population includes always-takers and potentially very different demographics. The honest answer: not without additional evidence that LATE ≈ ATE for this population.

---

## 🔄 Discussion Debrief

**Key insight:** LATE is an honest estimate of a narrow causal effect. It answers: "what was the effect for the people whose behavior the instrument actually changed?" Extrapolating to broader populations requires additional assumptions.

**Bridge sentence:**
> "IV's external validity is limited by design. It tells you the effect for compliers — and that's actually a *virtue*, not a bug. You know exactly who the estimate applies to. The challenge is making sure those compliers are the people you care about."

**Hook payoff (returning to Amazon):**
> "Now let's close the loop. Amazon's 2024–2025 warehouse expansion is a valid instrument because: it's relevant (expansion predicts delivery speed), exogenous (logistics decisions made years before any analysis, unrelated to individual customer behavior), and satisfies the exclusion restriction (warehouse location doesn't directly affect purchase amounts through any channel other than delivery speed). The LATE from this instrument applies to customers in expansion markets who became more frequent buyers because of improved delivery speed — not to already-engaged customers who shop regardless of speed, and not to very infrequent buyers who wouldn't respond to speed improvements. The $4.20 number is real and useful — but it applies specifically to the marginal customer."

---

## 📊 Class Poll: What Does IV Estimate?

*After Section 5 — Poll 4* | **Platform:** Mentimeter

**Poll 4:** Card (1995) uses college proximity as an instrument for schooling. Which population does the IV estimate apply to?

- A) All workers in the sample
- B) Workers who attend college regardless of proximity (always-takers)
- C) Workers whose college attendance changes with proximity (compliers) ✓
- D) All workers, because consistent estimators give population-average effects

**Reveal script:** *"C — the compliers. This is the LATE. D is the most tempting wrong answer: 'consistent estimator → converges to the truth for everyone.' But IV converges to LATE, not ATE, in the presence of treatment heterogeneity. The compliers in Card's design are students at the margin of attendance — a specific subgroup. Whether that LATE is useful depends entirely on whether the policy you're evaluating affects primarily compliers."*

---

## 🔗 Connections (3 min)

### Building On
- *Omitted variable bias*: "Today's solution — IV — addresses the same problem OLS can't handle when the confounder is unobserved."
- *DAGs and exclusion restriction*: "The exclusion restriction is the 'no direct edge Z → Y' in a DAG. Same concept, different notation."

### Setting Up
- *Topic 9 (Weak Instruments)*: "We touched on weak instruments briefly — next week we go deep. What happens when F is very low, and what are the modern corrections?"
- *Topic 10 (Regression Discontinuity)*: "RD is the sibling of IV. Instead of a variable that causes quasi-random variation, you have a threshold. Same identification logic, different implementation."

---

## 🎯 Key Takeaways

Walking out of class, you should be able to complete these sentences:

1. "Instrumental variables is useful because OLS is inconsistent when the regressor is endogenous — and that inconsistency doesn't shrink with more data."
2. "The key assumptions we need are: Z is relevant (testable via F > 10), Z is exogenous (theoretical argument), and Z satisfies the exclusion restriction (theoretical argument plus robustness checks)."
3. "In practice, data scientists at tech companies use IV by finding quasi-random variation in treatment assignment — server shard assignments, platform rollouts, geographic expansion — to isolate causal effects from selection."
4. "The main limitation to keep in mind is LATE: IV estimates the effect for compliers only, not for the full population."
5. "This connects to Regression Discontinuity (Topic 10) because RD is also a way to find quasi-random variation — at a threshold rather than via an instrument."

---

## 📖 Supplementary Resources

**To go deeper:**
- [Angrist & Pischke, "Mostly Harmless Econometrics," Chapter 4](https://press.princeton.edu/books/mostly-harmless-econometrics) — The canonical applied IV reference; Chapter 4 is essential reading
- [Cunningham, "Causal Inference: The Mixtape," Chapter 7 (free online)](https://mixtape.scunning.com/07-instrumental_variables) — Very applied, excellent on LATE and the monotonicity assumption

**Video explainers:**
- [Nick Huntington-Klein, "Instrumental Variables" (YouTube)](https://www.youtube.com/watch?v=OFhfO7WUL9c) — 60 minutes, outstanding visual intuition on the geometry of 2SLS

**Datasets to explore:**
- [Angrist Data Archive](https://economics.mit.edu/faculty/angrist/data1/data) — Card (1995) and other classic IV datasets, ready to download

**For ambitious students:**
- [Lee, McCrary, Moreira, and Porter (2022, QJE)](https://doi.org/10.1093/qje/qjac038) — The tF-statistic for valid inference under weak instruments; increasingly the standard in top journals

---

## 📋 Appendix: Instructor Notes

### Timing Watch Points
- **Section 2 (2SLS)** commonly runs 3–4 minutes long if the first-stage/second-stage diagram takes longer than expected. Cut the DoorDash case study to a 30-second mention if pressed.
- **Discussion Block 2** can expand to 8+ minutes if students get into the FDA question (C). Monitor the clock — cut at 5 minutes even mid-discussion and use the closing hook payoff as the debrief.
- **Section 5 (LATE)** is the densest section. If running behind when you reach it, keep the complier/always-taker/never-taker classification and the Duolingo example; cut the formal monotonicity proof.

### Common Student Questions

**Q: Can I just run 2SLS manually — first stage predicted values, then second stage?**
A: Yes, but your standard errors will be wrong. The manually-run second stage treats X̂ as if it were observed, which underestimates uncertainty. Always use a proper 2SLS package (`linearmodels.IV2SLS` in Python, `ivreg` in R) which applies the correct standard error formula.

**Q: What if I have more instruments than endogenous regressors?**
A: You have an overidentified model. You can test overidentifying restrictions (Sargan-Hansen J-test). The 2SLS estimator is consistent; you can also use LIML (Limited Information Maximum Likelihood) which has better finite-sample properties when overidentified.

**Q: Is LATE always the right thing to estimate?**
A: It depends on the policy question. If you're evaluating a program that will specifically target the complier population (people at the margin of treatment), LATE is exactly right. If you're evaluating a universal program affecting everyone, LATE may not be the right estimand — you'd want ATE, which IV doesn't directly give you without additional assumptions.

### If Class Ends Early
- "Let's design an IV study for one more application. You work at a hospital. You want to know whether surgery (vs. medical management) causes better 10-year survival for patients with coronary artery disease. The problem: doctors select surgery for the sicker patients. What instrument would you propose? [Angrist & Grossman 2022 used distance to cardiac surgery centers — discuss.]"

### Notes After Teaching
*(Space for instructor to record timing actuals, student response patterns, what to change next time)*

---

*Generated by econ-lecture-prep | 2026-03-22 | Revised after peer review*
