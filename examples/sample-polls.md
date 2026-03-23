# Class Poll Questions: Instrumental Variables

**Course:** ECON 5200: Applied Data Analytics in Economics
**Topic:** 8 of 14 — Instrumental Variables
**Date:** 2026-03-22
**Platform:** Mentimeter / iClicker

*Load all five questions before class. In Mentimeter: create a "Quiz" presentation with one Multiple Choice slide per question. In iClicker: create individual questions in the question bank.*

---

## Poll 1: OLS Consistency Under Endogeneity

**Placement:** After Section 1 (Endogeneity Problem) — approximately 16 minutes into class
**Purpose:** Misconception reveal — distinguishing bias from inconsistency
**Expected % correct:** ~40%

---

**Question:**
When the regressor X is endogenous (correlated with the error term), which statement is correct about OLS?

| Option | Text | Correct? |
|--------|------|----------|
| A | OLS is unbiased but inefficient | |
| B | OLS has a small bias that shrinks as the sample grows larger | |
| C | OLS is biased and inconsistent — the bias does NOT shrink with more data | ✓ |
| D | OLS is biased in small samples but asymptotically corrects itself | |

**Why each wrong option is tempting:**
- **A** is wrong because OLS is neither unbiased nor efficient under endogeneity. Students who choose A are confusing "endogeneity" with "heteroskedasticity" (which makes OLS inefficient but unbiased).
- **B** is wrong and is the most common wrong answer (~35% expected). Students know that bias can shrink with sample size (the concept of consistency) and apply this incorrectly to the endogeneity case.
- **D** is a restatement of B with slightly different language — also wrong for the same reason.

**Reveal script:**
> *"The answer is C — and this is worth understanding precisely. OLS endogeneity bias is not a small-sample problem. It's a consistency problem: plim(β̂) ≠ β, no matter how large n gets. Imagine running this regression with the full population — 330 million Americans — you'd still get the wrong answer. That's why endogeneity is a fundamental identification problem, not a data quantity problem. More data cannot fix it. You need a different estimator."*

**Follow-up if >50% choose B or D:**
> *"I see a lot of B's. Let me draw this out. [Sketch plim(β̂_OLS) = β + Cov(X,ε)/Var(X) on the board.] This limit doesn't go to zero as n grows — Cov(X,ε) is a property of the data generating process, not the sample size. That's what makes endogeneity dangerous."*

---

## Poll 2: Which IV Assumptions Are Testable?

**Placement:** After Section 3 (Three IV Assumptions) — approximately 40 minutes into class
**Purpose:** Concept check on testability — critical for research practice
**Expected % correct:** ~55%

---

**Question:**
Which of the three standard IV assumptions — Relevance, Exogeneity, Exclusion Restriction — can be directly tested with data?

| Option | Text | Correct? |
|--------|------|----------|
| A | Relevance only | ✓ |
| B | Exogeneity only | |
| C | Relevance and Exclusion Restriction | |
| D | All three are directly testable with sufficient data | |

**Why each wrong option is tempting:**
- **B** is wrong. Students who choose B may be thinking of tests for instrument quality that involve residuals — but since we don't observe ε, we cannot directly test Cov(Z,ε) = 0.
- **C** is wrong but tempting because students may be thinking of the Sargan-Hansen J-test, which tests over-identifying restrictions. But (1) the J-test only works when you have more instruments than endogenous regressors (overidentified), and (2) it tests a joint hypothesis, not the exclusion restriction directly.
- **D** is wrong for the same reasons as B and C. More data doesn't make untestable assumptions testable.

**Reveal script:**
> *"Only Relevance is directly testable — check the first-stage F-statistic. Exogeneity requires Cov(Z,ε) = 0, but we can't observe ε, so we can't test it directly. The Exclusion Restriction also can't be tested directly — in the typical just-identified case (one instrument, one endogenous variable), there is literally no statistical test available. What we do instead: argue theoretically, run robustness checks, examine the institutional setting. This is why good IV papers spend pages arguing why the instrument is valid — it's not laziness, it's necessity."*

---

## Poll 3: Weak Instrument Decision

**Placement:** After Section 4 (First Stage and F-Statistic) — approximately 53 minutes into class
**Purpose:** Decision-making under weak instrument uncertainty
**Expected % correct:** ~35%

---

**Question:**
Your first-stage F-statistic is 8.3. Which response is most appropriate?

| Option | Text | Correct? |
|--------|------|----------|
| A | F = 8.3 is close to 10 — acceptable; proceed with standard 2SLS | |
| B | Weak instrument concern — report Anderson-Rubin or tF confidence sets; note the limitation; consider strengthening the instrument | ✓ |
| C | F < 10 means the instrument is invalid — discard it and find a new one | |
| D | Collect more data — a larger sample will automatically raise the F-statistic | |

**Why each wrong option is tempting:**
- **A** is tempting because 8.3 is "close" to 10 and students may treat the rule as approximate. But Staiger & Stock show that F < 10 can produce IV estimates with bias up to 10–20% of the OLS bias — not trivial.
- **C** is the overcorrection: F < 10 is a warning, not a death sentence. Many published papers use instruments with F = 7–9 if they report appropriate inference methods.
- **D** is wrong: the F-statistic is approximately the square of the t-statistic divided by the number of instruments — collecting more data does raise the F-statistic, but this is not "automatic" and doesn't solve the structural weak instrument problem in the current data.

**Reveal script:**
> *"B is correct — and it requires two things, not just a note in a footnote. First, report Anderson-Rubin confidence sets or the Lee et al. (2022) tF-statistic, both of which are robust to weak instruments. Second, transparently discuss the limitation. A lot of papers bury F = 8.5 in a footnote and proceed as if everything is fine — reviewers and readers increasingly notice. Option C is too strict: weak instruments don't automatically invalidate a study, they just require more careful inference."*

---

## Poll 4: What Does IV Estimate?

**Placement:** After Section 5 (LATE) — approximately 65 minutes into class
**Purpose:** Synthesis — connecting estimation to interpretation
**Expected % correct:** ~65%

---

**Question:**
Card (1995) uses distance from college as an instrument for years of schooling. Which population does the IV estimate correspond to?

| Option | Text | Correct? |
|--------|------|----------|
| A | All workers in the sample | |
| B | Workers who would attend college regardless of distance (always-takers) | |
| C | Workers whose college attendance is affected by proximity to college (compliers) | ✓ |
| D | The average treatment effect for the population, since IV is consistent | |

**Reveal script:**
> *"C — the compliers. This is LATE: the Local Average Treatment Effect. Card's estimate tells us the wage return for people at the margin of college attendance — those who go to college if there's one nearby but wouldn't if they had to travel far. This is NOT the return for highly motivated students who'd attend regardless (always-takers), and it's not a population average. Why does this matter for policy? If a government uses Card's estimate to justify subsidizing college, they're implicitly assuming that the return for the marginal student (induced by accessibility) equals the return for students who choose college for other reasons. That assumption may be wrong."*

---

## Poll 5: Opening Hook Payoff (Optional — Open-Ended Mentimeter)

**Placement:** At the end of class as closing reflection
**Purpose:** Engagement reset + synthesis
**Platform:** Mentimeter Open-Ended or Word Cloud

---

**Question (display on screen):**
> "Complete this sentence: Amazon can get a valid IV estimate of delivery speed's effect on spending because their 2024 warehouse expansion..."

*Word Cloud mode: students type 3–5 words. Correct answers will cluster around "random," "location," "unrelated to," "buying habits," "exogenous."*

**What to look for:** Students who type "relevance," "exogeneity," "exclusion" are applying the formal vocabulary. Students who type "random location" are getting the intuition right. Both are wins.

**How to use:** Show the word cloud, highlight the key words, then give the closing sentence: *"The warehouse location was determined by logistics and real estate decisions made before Amazon analyzed customer behavior — so it's exogenous to individual purchase habits. That's a valid instrument."*

---

*This poll guide accompanies `examples/sample-lecture-output.md`. For facilitation notes, see `examples/sample-discussion-guide.md`.*
