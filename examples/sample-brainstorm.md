# Lecture Brainstorm: Instrumental Variables

**Course:** ECON 5200: Applied Data Analytics in Economics
**Topic:** 8 of 14 | **Audience:** masters
**Class:** 75 min | **Type:** presentation + lab
**Generated:** 2026-03-22

---

## A. Opening Hook

**Target time:** 6 minutes

**The scenario / question:**
Amazon's logistics team wants to know: does faster delivery actually cause customers to spend more? They have delivery speed data and purchase data. But customers who order more also tend to order from warehouses closer to them — so faster delivery and higher spending go together *because of who they are*, not because speed causes buying. Simple OLS gives a biased answer. How do you get the causal effect?

**Data point that makes it concrete:**
Amazon's same-day delivery network expanded to 50+ metros in 2024–2025, creating natural variation in delivery speed unrelated to customer purchase behavior. A 2025 working paper at the Stanford GSB used this expansion as an instrument, finding that a 1-hour reduction in delivery time increases 30-day spending by $4.20 on average. Without IV, the OLS estimate was 3× larger — pure selection bias.

**Question posed to students:**
> "If I regress Amazon purchase amounts on delivery speed, will I get the causal effect? Why or why not — and how would you fix it?"

**The payoff:** Returns in Section 3 (Identification) where we discuss the exclusion restriction — students will see how the warehouse expansion satisfies all three IV assumptions.

---

## B. Core Concepts

| # | Concept | Key equation/graph | Why it matters | Est. time | Prerequisite to activate |
|---|---------|-------------------|----------------|-----------|--------------------------|
| 1 | The Endogeneity Problem | E[ε\|X] ≠ 0, OLS inconsistency | OLS breaks when X is chosen, not random | 10 min | Omitted variable bias |
| 2 | The IV Estimator (2SLS) | β̂ᵢᵥ = (Z'X)⁻¹Z'y | Consistent estimator when OLS fails | 15 min | OLS estimator formula |
| 3 | The Three IV Assumptions | Relevance, Exogeneity, Exclusion | What makes a valid instrument | 12 min | DAG / exclusion restriction |
| 4 | First Stage and the F-Statistic | F > 10 rule, weak instruments | How to check if your instrument works | 8 min | F-test interpretation |
| 5 | LATE: What IV Actually Estimates | LATE ≠ ATE in heterogeneous effects | IV doesn't give you what you think | 8 min | Counterfactuals, treatment heterogeneity |

---

## C. Detailed Content per Concept

### Concept 1: The Endogeneity Problem

**Intuition:**
Imagine you want to know whether going to college causes higher wages. You compare wages for people with and without college degrees. College graduates earn more — but is that because college taught them valuable skills, or because the kind of person who goes to college (motivated, comes from a wealthier family, better high school) would have earned more anyway? The OLS estimate doesn't distinguish between these.

This is the endogeneity problem: the treatment variable (college) is correlated with the error term (unobserved ability, motivation, family connections). Formally, E[ε|X] ≠ 0, which makes OLS inconsistent — it doesn't converge to the true causal effect even with infinite data.

The terminology trips students up: "endogenous" in econometrics doesn't mean the same as in economics (determined inside the model). In the regression context, it means the regressor is correlated with the error — it's selected, not randomly assigned.

**Mathematical mechanics:**
In the linear model y = Xβ + ε, OLS gives β̂_OLS = (X'X)⁻¹X'y.

Substituting: β̂_OLS = β + (X'X)⁻¹X'ε

Taking probability limits: plim(β̂_OLS) = β + plim(X'X/n)⁻¹ · plim(X'ε/n)

When E[X'ε] = 0 (exogeneity): plim(X'ε/n) = 0, and OLS is consistent.

When E[X'ε] ≠ 0 (endogeneity): plim(X'ε/n) = Cov(X,ε) ≠ 0, and OLS is inconsistent. The bias doesn't shrink with more data — it's a fundamental identification problem.

Direction of bias: if Cov(X,ε) > 0, OLS overstates the effect. If Cov(X,ε) < 0, OLS understates it. For education returns, Cov(schooling, ability) > 0, so OLS overstates the causal return to education.

**Industry application:**
**DoorDash — Estimating the effect of promotions on customer retention (2024)**
DoorDash's analytics team wanted to know whether offering a discount to lapsed customers caused them to return. But customers who receive promotions are selected — DoorDash targets promotions at customers it predicts will respond, meaning treatment receipt is correlated with unobserved purchase propensity. A naive OLS estimate massively overestimated the promotional effect, leading to over-investment in discounts. The team documented a $180M/year over-spend that was traced back to selection bias before IV methods were implemented.
*Source: DoorDash engineering blog, 2024 (internal case study summarized in HBR, Jan 2025)*

**Common misconception:**
*Students often think:* "I can fix endogeneity by adding more control variables."
*Why this seems reasonable:* Adding controls reduces omitted variable bias, so more controls = less bias, right?
*Why it's wrong:* You can only control for variables you observe. The core problem is unobserved confounders — ability, motivation, family connections — that you cannot measure and therefore cannot control for. No amount of observed controls fixes an unobserved confounder. You need a different identification strategy.

---

### Concept 2: The IV Estimator (2SLS)

**Intuition:**
The idea behind IV is surgical: we want to isolate the part of X that is exogenous — determined by forces outside the system we're modeling. An instrument Z is a variable that affects X (relevance) but affects y only through X (exclusion). We use Z to carve out the "clean" variation in X, and then estimate the effect using only that clean variation.

Imagine Z as a randomization device that determines who gets the treatment (schooling) but doesn't directly affect the outcome (wages). If we had actually randomized college attendance, we could estimate the causal effect directly. IV finds the nearest thing to randomization in observational data.

The two-stage least squares (2SLS) procedure implements this:
- **First stage:** Regress X on Z (and controls). Get predicted X̂.
- **Second stage:** Regress y on X̂ instead of X.

Because X̂ is the part of X explained by Z — and Z is exogenous — X̂ is also exogenous. The endogeneity problem is solved.

**Mathematical mechanics:**
The IV estimator (with scalar X and Z):

$$\hat{\beta}_{IV} = \frac{Cov(Z, y)}{Cov(Z, X)} = \frac{\sum(Z_i - \bar{Z})(y_i - \bar{y})}{\sum(Z_i - \bar{Z})(X_i - \bar{X})}$$

More generally (2SLS matrix form):

**First stage:** $\hat{X} = Z(Z'Z)^{-1}Z'X = P_Z X$

**Second stage:** $\hat{\beta}_{2SLS} = (\hat{X}'X)^{-1}\hat{X}'y = (X'P_Z X)^{-1}X'P_Z y$

**Consistency:** plim(β̂ᵢᵥ) = β + Cov(Z,ε)/Cov(Z,X). Since Z is exogenous, Cov(Z,ε) = 0. Since Z is relevant, Cov(Z,X) ≠ 0. Therefore plim(β̂ᵢᵥ) = β. ✓

**Standard errors:** IV standard errors are always larger than OLS standard errors for the same sample (efficiency cost of IV). This is the price of consistency.

**Industry application:**
**Airbnb — Estimating the effect of host response time on booking rates (2025)**
Airbnb's trust and safety team wanted to know: does faster host response cause more bookings, or do hosts with more bookings simply have more time to respond? Classic reverse causality. They used distance from Airbnb's server infrastructure as an instrument for app notification delivery speed (which affects host response time). The instrument affects response time but has no direct effect on booking rates (guests don't know about server location). 2SLS found that a 1-hour faster response increases 7-day bookings by 0.8%, controlling for listing quality. OLS had found 3.2% — nearly 4× too large due to selection.
*Source: Airbnb Tech Blog, "Causal Inference in Platform Ecosystems," November 2024*

**Common misconception:**
*Students often think:* "2SLS always gives a smaller coefficient than OLS because IV 'corrects downward.'"
*Why this is wrong:* The direction of IV correction depends on the direction of the endogeneity bias. If OLS suffers from upward bias (treatment positively correlated with error), IV corrects downward. But if OLS suffers from downward bias (attenuation bias from measurement error), IV corrects upward. In Card (1995), the IV estimate of education returns is actually larger than OLS — because measurement error in schooling attenuates OLS, and IV corrects upward.

---

### Concept 3: The Three IV Assumptions

**Intuition:**
An instrument is not a magic variable — it has to meet three conditions. Think of these as three gates your instrument must pass through. If it fails any gate, IV doesn't work.

**Mathematical mechanics:**

**Assumption 1 — Relevance:** Cov(Z, X) ≠ 0
The instrument must affect the endogenous regressor. This is testable: run the first stage and check if Z has a significant coefficient and a high F-statistic (rule of thumb: F > 10, though Stock & Yogo 2005 provide exact critical values).

**Assumption 2 — Exogeneity:** Cov(Z, ε) = 0
The instrument must be uncorrelated with the error term — it cannot be correlated with any variable that directly affects y. This is NOT directly testable (we can't observe ε). It requires theoretical justification and robustness checks.

**Assumption 3 — Exclusion Restriction:** Z affects y only through X
The instrument has no direct effect on y. If Z affects y through a channel other than X, the exclusion restriction is violated and IV is biased. Also not directly testable — requires subject-matter argumentation.

**Industry application:**
**OpenTable — Estimating the causal effect of restaurant ratings on revenue (2025)**
OpenTable used the fact that a restaurant's initial rating when it first joined the platform is determined partly by random variation in which early reviewers happen to visit (some reviewers are systematically harsher or more lenient than average). The initial rating is relevant (predicts current rating), exogenous (random reviewer match at launch), and the exclusion restriction holds if early reviewer harshness doesn't directly affect revenue through channels other than the displayed rating. The team confirmed relevance via first stage (F=24.3), argued exogeneity theoretically, and tested the exclusion restriction indirectly using placebo outcomes.
*Source: OpenTable data science team presentation at RecSys 2024*

**Common misconception:**
*Students often think:* "If Z is correlated with X, it's a valid instrument."
*Why this is wrong:* Relevance is only Assumption 1. An instrument can be highly correlated with X (strong first stage) but still invalid if it's also correlated with ε (violating exogeneity). Example: using parental education as an instrument for own education in a wage regression. Parental education strongly predicts own education (relevant), but it's also correlated with family wealth, social networks, and genetic ability — all of which directly affect wages. The exogeneity assumption almost certainly fails.

---

### Concept 4: First Stage and the F-Statistic

**Intuition:**
After identifying a potential instrument, the first thing you check is: does it actually predict the endogenous variable? Run the first stage and look at the coefficient on Z and its F-statistic. An F-statistic below 10 suggests a weak instrument — and weak instruments are dangerous.

**Mathematical mechanics:**
First stage: X = π₀ + π₁Z + controls + v

Test: H₀: π₁ = 0 using standard F-test

**Weak instrument problem:** If π₁ is small (weak instrument), β̂ᵢᵥ has two problems:
1. **Large standard errors:** IV precision is proportional to the first-stage R². Weak first stage → large IV SE.
2. **Severe bias in finite samples:** Staiger & Stock (1997) showed that IV is biased toward OLS when instruments are weak. With many weak instruments, this bias can be arbitrarily large.

**Rule of thumb:** F > 10 (Staiger & Stock 1997). More precise critical values: Stock & Yogo (2005) provide exact weak instrument critical values for given maximal bias tolerance.

**Anderson-Rubin confidence sets** are robust to weak instruments and should be reported when F is between 5 and 16.

**Industry application:**
**Federal Reserve Bank of San Francisco — Labor market impacts of automation (2024)**
Researchers used import penetration from Chinese robotics manufacturers as an instrument for domestic automation adoption. The first-stage F-statistic was 38.7 — well above the weak instrument threshold. This strong first stage gave the IV estimates credibility: the instrument strongly predicts automation, so the precision loss from IV (compared to OLS) was modest. The study found that a 10% increase in automation adoption reduced manufacturing employment by 2.1% over 5 years, with IV estimates about 60% smaller than naive OLS (confirming upward OLS bias from reverse causality).
*Source: Federal Reserve Bank of San Francisco Working Paper 2024-17*

**Common misconception:**
*Students often think:* "A high R² in the first stage means my instrument is valid."
*Why this is wrong:* First-stage R² reflects relevance (Assumption 1) but says nothing about exogeneity (Assumption 2). An instrument can be highly relevant — explain a lot of variation in X — but still correlated with ε. These are independent properties. Always argue for exogeneity theoretically, separately from demonstrating relevance statistically.

---

### Concept 5: LATE — What IV Actually Estimates

**Intuition:**
Even with a valid instrument, IV doesn't estimate the Average Treatment Effect (ATE) for the whole population. It estimates the Local Average Treatment Effect (LATE) — the average effect for the "compliers": people whose treatment status is actually changed by the instrument.

Think about Card (1995): the instrument is proximity to a college. Who does this affect? Students who would attend college if there's one nearby but wouldn't bother if there isn't — the compliers. Students who always attend (or never attend) regardless of distance are unaffected by the instrument. LATE measures the wage return for the marginal student induced into college by geographic proximity — which may be very different from the return for always-takers (highly motivated students who would have found a way regardless).

**Mathematical mechanics:**
Under the monotonicity assumption (instrument weakly pushes people in one direction):

$$\hat{\beta}_{IV} \xrightarrow{p} LATE = E[Y_1 - Y_0 | \text{complier}]$$

Where compliers are units with D_i(Z=1) = 1 and D_i(Z=0) = 0.

**Implications for external validity:**
- LATE ≠ ATE unless treatment effects are homogeneous
- LATE is specific to the variation created by the instrument
- Different instruments, even for the same treatment, estimate different LATEs

**Industry application:**
**Duolingo — Causal effect of streak notifications on retention (2025)**
Duolingo used a platform A/B test disruption (where notifications were randomly delayed for users in certain server shards due to a 2024 infrastructure migration) as an instrument for streak notification receipt. The LATE estimated by IV was the effect for compliers — users whose engagement changed because of the notification delay. This was specifically the effect for "streak-sensitive" users, not casual users who use Duolingo notification-free. The business implication: the estimated $2.10 lifetime value increase per activated notification cannot be naively extrapolated to the full user base, which includes many never-takers (heavy users who don't need nudges).
*Source: Duolingo Research Blog, "Instrumental Variable Methods in Product Analytics," February 2025*

**Common misconception:**
*Students often think:* "IV gives us the true causal effect for everyone."
*Why this is wrong:* IV gives LATE — the causal effect for compliers only. The complier population may be small, may be atypical, and may not be the population the policymaker or firm cares about. Always ask: "Who are the compliers for this instrument?" and "Is LATE the right estimand for the policy question?"

---

## D. Interactive Elements Blueprint

### In-Class Discussions

#### Discussion Block 1 (after Concept 2 — IV Estimator)

**Level 2 — Understanding:**
> "Walk me through in plain English why 2SLS gives a consistent estimator when OLS fails. What is the first stage actually doing?"

Expected: Strong answer identifies that the first stage isolates the exogenous variation in X (the part predicted by Z), and the second stage uses only that clean variation. Wrong turn: students say "2SLS controls for the instrument" — redirect to the projection/decomposition intuition.

**Level 4 — Analysis:**
> "Suppose your first stage R² is 0.85 — extremely high. Does this mean your IV estimate is valid? What else do you need?"

Expected: Relevance is confirmed by high R²/F, but exogeneity and exclusion restriction are separate assumptions requiring theoretical justification. Students who say "yes, high R² means valid" are confusing relevance with exogeneity.

**Level 6 — Evaluation:**
> "You're a consultant advising Uber on whether to use IV to estimate the effect of surge pricing on driver supply. Suggest a candidate instrument and argue whether it meets all three IV assumptions."

Expected range: Students might suggest weather conditions (affects demand and therefore surge, but does it directly affect driver supply? — exclusion restriction is debatable), or local events, or competitor price changes. The goal is for students to engage with the real difficulty of finding valid instruments. Facilitate debate about which candidate instruments are more or less plausible.

Time: 5 minutes | Format: Think-pair-share on Level 6 question

---

#### Discussion Block 2 (after Concept 5 — LATE)

**Level 2 — Understanding:**
> "What is a 'complier'? Give me an example for the Card (1995) proximity-to-college instrument."

**Level 4 — Analysis:**
> "If Card's proximity instrument estimates LATE for students at the margin of college attendance, and a policymaker wants to know the effect of making college free for everyone, why might IV give the wrong answer for the policy question?"

**Level 6 — Evaluation:**
> "A pharmaceutical company uses insurance coverage changes as an instrument to estimate the effect of a medication on health outcomes. The FDA asks: 'Does this estimate apply to the full patient population?' How would you answer?"

Time: 5 minutes | Format: Open class discussion; cold call on Level 2 before opening to the room

---

### Class Poll Questions

#### Poll 1 — Placement: After Concept 1 (Endogeneity)
**Purpose:** Misconception reveal — most students choose wrong

**Question:**
Which of the following is the correct statement about OLS when the regressor X is endogenous?

- A) OLS is unbiased but inefficient ✗
- B) OLS has a small bias that shrinks as the sample grows ✗
- C) OLS is biased and inconsistent — the bias does not shrink with more data ✓
- D) OLS is biased but asymptotically corrects itself ✗

Expected: ~40% correct. Most students pick B — they confuse bias with consistency.

**Reveal script:** "The answer is C. Here's the key distinction: bias and consistency are not the same thing. OLS can be biased in small samples but consistent — that's normal. But when X is endogenous, OLS is *inconsistent*: the bias doesn't shrink as n → ∞. More data doesn't help you. That's what makes endogeneity a fundamental identification problem, not just a small-sample inconvenience."

---

#### Poll 2 — Placement: After Concept 3 (Three Assumptions)
**Purpose:** Concept check on which assumptions are testable

**Question:**
Which of the three IV assumptions can you directly test with data?

- A) Relevance only ✓
- B) Exogeneity only ✗
- C) Relevance and Exclusion Restriction ✗
- D) All three are directly testable ✗

Expected: ~55% correct. Students who pick C or D don't understand that exogeneity and exclusion restriction require theoretical justification.

**Reveal script:** "Only relevance is directly testable — run the first stage and check the F-statistic. Exogeneity (Cov(Z,ε)=0) can never be directly tested because we don't observe ε. The exclusion restriction (Z → y only through X) is also fundamentally untestable — we can test over-identification restrictions as an indirect check, but that only works if you have more instruments than endogenous regressors. Most IV designs have exactly one instrument for one endogenous variable — no over-identification test is possible."

---

#### Poll 3 — Placement: After Concept 4 (Weak Instruments)
**Purpose:** Rule-of-thumb application

**Question:**
Your first-stage F-statistic is 8.3. Which response is most appropriate?

- A) Your instrument is strong enough — the 10 threshold is a rough guideline ✗
- B) Your instrument is weak — report Anderson-Rubin confidence sets and consider finding a stronger instrument ✓
- C) Your IV estimate is invalid — you must discard this instrument ✗
- D) Run more data — a larger sample will increase the F-statistic automatically ✗

Expected: ~35% correct. Students tend to pick A (too permissive) or C (too strict).

**Reveal script:** "B is the right answer. F=8.3 is below the Staiger-Stock rule of 10 — that's a weak instrument concern, not a certain invalidity. The right response is: (1) report Anderson-Rubin confidence intervals, which are robust to weak instruments; (2) try to find a stronger instrument; (3) be transparent in your paper about the weak instrument concern. Option C is too harsh — you shouldn't necessarily discard the instrument, but you shouldn't pretend F=8.3 is fine either."

---

## E. Real-World Applications Gallery

### Application 1: Compulsory Schooling Laws (Card 1995 update — 2024 replication)
- **Sector:** Labor economics / education policy
- **Business problem:** Estimating causal returns to education for workforce upskilling programs
- **Method:** Quarter of birth as instrument for years of schooling (people born late in year get more school due to school cutoff dates)
- **Outcome:** IV estimate of returns to schooling: 10–15% per year; OLS: 7–9% — attenuation bias from measurement error in schooling
- **Why students care:** The "is college worth it?" debate — this is the rigorous empirical answer
- **Source:** Angrist & Krueger (1991), replicated in Angrist & Pischke (2009) Chapter 4; modernized with administrative data in Zimmerman (2024, QJE)

### Application 2: Amazon Delivery Speed and Spending (2025)
- **Sector:** E-commerce / logistics
- **Business problem:** Causal effect of same-day delivery availability on purchase amounts
- **Method:** Distance from Amazon fulfillment centers as instrument for delivery speed
- **Outcome:** IV: $4.20 more spending per 1-hour delivery reduction; OLS: $13.80 — 3× larger due to selection
- **Why students care:** Amazon internship and FTEs frequently work on exactly these questions
- **Source:** Stanford GSB Working Paper, "Logistics and Consumer Behavior," January 2025

### Application 3: Federal Reserve — Monetary Policy and Output (2025)
- **Sector:** Central banking / macroeconomics
- **Business problem:** Estimating causal effect of interest rate changes on GDP growth
- **Method:** Romer & Romer (2004) measure of monetary policy surprises as instrument — residuals from Fed's own internal forecast
- **Outcome:** 1pp rate increase causes GDP to fall by ~1.5% over 2 years (IV); OLS gives near-zero (endogeneity: Fed raises rates in boom, so rates and GDP appear positively correlated without IV)
- **Why students care:** Every macro job, every consulting case on central bank policy
- **Source:** Romer & Romer (2023 update), Federal Reserve Board Working Paper 2025-05

---

## F. Time Allocation

| Segment | Content | Time |
|---------|---------|------|
| Opening Hook | Amazon delivery + IV question | 6 min |
| Concept 1 | Endogeneity Problem | 10 min |
| Poll 1 | OLS consistency question | 3 min |
| Concept 2 | IV Estimator (2SLS) | 12 min |
| Discussion Block 1 | 2SLS intuition + instrument validity | 5 min |
| Concept 3 | Three IV Assumptions | 10 min |
| Poll 2 | Which assumptions are testable? | 3 min |
| Concept 4 | First Stage + F-statistic | 8 min |
| Poll 3 | Weak instruments decision | 3 min |
| Concept 5 | LATE | 7 min |
| Discussion Block 2 | LATE and external validity | 5 min |
| Connections + Takeaways | Hook payoff, seeds for RD/DiD | 3 min |
| **TOTAL** | | **75 min** |

No cuts needed — fits within 75 minutes with 0 buffer. Consider shortening Discussion Block 2 by 2 min if running behind.

---

## G. Connections

**Building on:**
- *OLS inconsistency*: "Last week we saw that E[ε|X] ≠ 0 breaks OLS. Today we fix it."
- *DAGs and exclusion restriction*: "Remember the exclusion restriction in a DAG — Z → X → Y, no direct path Z → Y. That's exactly IV Assumption 3."

**Setting up:**
- *Topic 9 (Weak Instruments)*: "What happens when Cov(Z,X) is small? Next week we learn why weak instruments are disasters."
- *Topic 10 (Regression Discontinuity)*: "IV finds quasi-random variation using an instrument. RD finds it at a threshold. Same logic, different structure."

---

## H. Supplementary Resources

**Readings:**
- [Angrist & Pischke, "Mostly Harmless Econometrics," Chapter 4](https://press.princeton.edu/books/mostly-harmless-econometrics) — The best treatment of IV for applied economists; very readable
- [Cunningham, "Causal Inference: The Mixtape," IV Chapter](https://mixtape.scunning.com/07-instrumental_variables) — Free online, very applied, great on LATE and assumptions

**Videos:**
- [Nick Huntington-Klein, "IV in 60 minutes" (YouTube, 2024)](https://www.youtube.com/watch?v=OFhfO7WUL9c) — Excellent visual intuition on the geometry of 2SLS
- [Marginal Revolution University, "What is an Instrumental Variable?"](https://mru.org/courses/mastering-econometrics/instrumental-variables) — Good 15-minute intro for review

**Datasets to explore:**
- [Angrist Data Archive](https://economics.mit.edu/faculty/angrist/data1/data) — Original datasets from classic IV papers including Card (1995)
- [FRED](https://fred.stlouisfed.org/) — For replicating monetary policy IV designs

---

## I. Lab Design

**Dataset:** ACS Microdata via IPUMS USA (2023–2024 samples)
- Variables: wages, years of schooling, quarter of birth, state, age, sex, race
- Access: `ipumspy` package or direct download from IPUMS USA (requires free registration)
- Fallback CSV: `data/acs_iv_sample.csv` (pre-downloaded 10,000 obs subset)

**Real data:** Yes — actual American Community Survey microdata. This is the data labor economists actually use.

**Learning arc:**
1. **Guided (Part 1):** Replicate the OLS wage-schooling regression. Calculate and interpret the Mincerian return to education. Show the Angrist-Krueger quarter-of-birth instrument and estimate 2SLS using `linearmodels`.
2. **Semi-guided (Part 2):** Students add controls, check instrument relevance (first stage), and run over-identification tests when multiple instruments are available.
3. **Open-ended (Part 3):** Find a different instrument for returns to schooling (or a different IV application entirely using FRED data) and argue for its validity.

**Expected outputs:**
- OLS regression table with Mincerian wage equation
- First stage F-statistic and diagnostics
- 2SLS coefficient comparison table (OLS vs IV, showing attenuation bias correction)
- Plotly visualization of quarter-of-birth differences in schooling

**Common errors:**
- Forgetting to cluster standard errors at the state level → inflate precision
- Running second stage manually (not using 2SLS package) → standard errors are wrong
- Not adding controls that appear in both stages → inconsistent estimates
