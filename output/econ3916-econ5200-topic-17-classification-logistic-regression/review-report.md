# Peer Review Report

**Topic:** Classification I — Logistic Regression
**Course:** ECON 3916 / ECON 5200 (dual)
**Brainstorm reviewed:** `output/econ3916-econ5200-topic-17-classification-logistic-regression/brainstorm.md`
**Review date:** 2026-03-22

---

## Pedagogy Review 🎓

**Overall assessment:** Strong

**Strengths:**
1. The NY Fed hook is exceptional — the model is real, the stakes are real, the "wrong" prediction opens a genuine puzzle that only gets resolved in Section 3 and points forward to Topic 18. This will genuinely make students lean in.
2. The three-layer interpretation framework (log-odds → odds ratio → predicted probability) is correctly scaffolded and the misconception about "probability vs. odds" is pre-empted precisely where students will get confused.

**Issues:**

| Priority | Issue | Specific Fix |
|----------|-------|-------------|
| must-fix | Concept 1 is allocated 10 minutes but contains THREE formal problems with LPM (out-of-bounds, heteroskedasticity, non-normal errors). For a dual undergrad/masters audience, the heteroskedasticity argument needs one concrete example or visual — not just the formula. Students who haven't seen White's theorem will not follow the abstract claim. | Add 2-sentence concrete example: "If P(default) is 5% near zero, Var(ε) = 0.05×0.95 = 0.048. If P(default) is 50%, Var(ε) = 0.25. The variance changes with X — heteroskedastic by construction." |
| must-fix | Lab has NO explicit instruction for what `.predict()` vs `.predict_proba()` produces — this is noted in "common errors" but not built into the guided code flow. For 30 minutes, students WILL make this error silently and get a table of 0s and 1s they can't plot as a probability curve. | Add as the first guided code cell comment: "# IMPORTANT: .predict() returns class labels (0/1). Use .predict_proba()[:,1] to get the probability of Y=1. We need the probability for our plot." |
| should-fix | Poll 1 question is clever but risks being confusing for weaker undergrad students. The "NOT a problem" phrasing with four valid-sounding answers requires careful reading under time pressure. | Add explicit instruction before Poll 1: "Read carefully — this asks which is NOT a problem with LPM." Display on slide. |
| should-fix | Discussion Block 2 Level 6 (click-through prediction on 98% imbalanced data) jumps ahead to class imbalance before it's been taught. While it's a good seed, weaker students may not know enough to engage productively. | Keep the question, but add a single sentence setup: "Suppose you know 98% of the outcomes are 0. Think about what 'accuracy' means in that context..." This gives students enough scaffolding to reason about imbalance even without formal knowledge. |
| nice-to-have | The Connections section plants seeds for Topic 18 and 19 but doesn't explicitly connect to the sklearn API continuity (students knowing LogisticRegression() already exists). | Add one sentence: "The sklearn API is identical to what you used for Ridge last week — LogisticRegression().fit(X,y).predict_proba(X). The estimator changes; your code template doesn't." |

**Interactive elements specific feedback:**
- Discussion questions: All three Bloom's levels present and well-calibrated for this audience. The Level 6 question about Fannie Mae is particularly strong — it has genuine ambiguity and forces students to weigh operational vs. regulatory concerns.
- Poll questions: Poll 1 is high-risk-high-reward (conceptually strong but phrasing is tricky). Poll 2 is appropriately easy (confidence reset after the harder LPM material). Poll 3 is excellent — odds ratio interpretation is the most commonly tested concept in applied ML interviews.
- Debrief notes: Good specificity. Bridge sentences are actual sentences, not prompts.

---

## Domain Review 📊

**Overall assessment:** Rigorous. Two precision issues.

**Errors or inaccuracies:**

| Priority | Error | Correct statement |
|----------|-------|------------------|
| must-fix | Concept 3 states "There's no closed-form solution like OLS's (X'X)⁻¹X'y — we use iterative optimization (Newton-Raphson or gradient descent)." This is correct, but should note that sklearn's default solver is 'lbfgs' (Limited-memory BFGS), not Newton-Raphson or standard gradient descent. Students who check sklearn docs will see 'lbfgs' and be confused. | Add: "sklearn uses LBFGS by default — a quasi-Newton method that approximates the Hessian. You don't need to know the details, but if you see solver='lbfgs' in the output, that's why." |
| should-fix | The "binary cross-entropy loss" claim — "identical to what neural networks minimize" — is accurate but may overstate the connection for undergrad students. Cross-entropy in deep learning uses softmax for multi-class; binary logistic is a special case. | Soften to: "This loss function — binary cross-entropy — is the same loss used in the binary classification layer of neural networks. If you ever train a neural net for binary classification, you're minimizing the same thing as logistic regression." |

**Missing nuance:**

- Should mention that logistic regression **assumes linearity in the log-odds** — i.e., the log-odds is a linear function of X. If the true relationship is nonlinear in log-odds, the model is misspecified. This is exactly the motivation for tree-based models (Topic 19). One sentence: "Logistic regression assumes log(P/(1-P)) = Xβ — linear in the log-odds. When this assumption fails (which trees will handle), you need a more flexible model."
- The odds ratio interpretation assumes **ceteris paribus** (holding all other variables constant). This should be made explicit, especially since students know this concept from OLS.

**Literature currency:**
- NY Fed model citation is current and accurate — the model is indeed logistic regression as described.
- Upstart Holdings 10-K citation: verify the specific quote about LPM. The 10-K likely refers to "statistical models" generically; the specific LPM claim may be from analyst commentary rather than the filing itself. Flag as "reported in risk management literature" rather than quoting the 10-K directly.
- JPMorgan 2024 Annual Report: odds ratios as regulatory requirement is accurate per OCC SR 11-7 guidance, which is standard knowledge. Solid citation.

**Notation issues:**
- σ(z) notation is used consistently — good.
- Binary cross-entropy loss formula is correct.
- Odds ratio notation: e^β₁ should clarify this is the exponentiated coefficient from the logistic model, not a standard exponential transformation. Consider: "The odds ratio = exp(β̂₁)" with hat notation to distinguish estimated from true coefficient.

---

## Industry Review 💼

**Overall assessment:** Job-ready. Strong on specificity.

**Example quality assessment:**

| Example | Assessment | Suggested improvement |
|---------|------------|----------------------|
| NY Fed Yield Curve Model | Excellent — live model, public URL, real numbers, directly replicated in lab | Perfect as is |
| JPMorgan Credit Scorecard | Strong — names the regulatory requirement (OCC SR 11-7), gives specific accuracy range | Add that this is a regulatory floor, not the actual production model: "JPMorgan runs more sophisticated internal models but must produce logistic regression outputs for regulatory examination" |
| Stripe Fraud Sigmoid | Strong — $1T volume anchors the scale | Verify that the January 2025 Stripe blog post is publicly accessible (Stripe Engineering Blog posts are sometimes gated) |
| Upstart 10-K | Good concept, but the specific LPM quote may be paraphrased rather than verbatim | Use as "financial model governance literature" rather than quoting the 10-K directly |

**Missing applications:**
- **Healthcare:** Logistic regression is the dominant model for clinical risk scoring (APACHE II, Framingham Risk Score, LACE readmission score). These are real-world high-stakes logistic regressions used daily in hospitals. Worth a 1-sentence mention: "The Framingham Risk Score — the tool your doctor uses to estimate your 10-year cardiovascular disease risk — is a logistic regression model with age, cholesterol, blood pressure, and smoking as inputs."
- **Hiring/HR:** Logistic regression for binary outcomes (hired/not hired, promoted/not promoted) is common in people analytics and controversial due to bias risk. Could be a brief mention in Discussion Block 2 Level 6.

**Currency issues:**
- All examples are 2024-2025. Excellent.
- The yield curve situation is very current (inversion peaked 2022-2023, normalizing through 2025) — students will find this immediately relatable.

**Career connection assessment:**
The JPMorgan odds ratios example is the best career bridge: "When you interview at a bank and they ask you to explain your model's output, you say 'the odds of default increase by X%' — not 'the log-odds changes by X.'" This is the sentence that makes the concept sticky.

---

## Synthesis

### All Issues — Prioritized and Resolved

| Priority | Reviewer | Issue | Resolution |
|----------|----------|-------|-----------|
| must-fix | Pedagogy | Heteroskedasticity needs concrete variance example | Applied: added numerical example in Concept 1 formal treatment |
| must-fix | Pedagogy | `.predict()` vs `.predict_proba()` not explicit in lab flow | Applied: added as first lab code comment |
| must-fix | Domain | sklearn solver 'lbfgs' not mentioned — students will see it in output | Applied: added parenthetical in Concept 3 |
| should-fix | Pedagogy | Poll 1 phrasing — add "Read carefully: which is NOT a problem" slide instruction | Applied |
| should-fix | Pedagogy | Discussion Block 2 Level 6 needs one-sentence scaffolding for imbalance | Applied |
| should-fix | Domain | Cross-entropy/neural network connection overstated | Softened: "same loss used in binary classification neural networks" |
| should-fix | Domain | Linearity in log-odds assumption not mentioned | Applied: added one sentence in Concept 3 |
| should-fix | Industry | JPMorgan example needs "regulatory floor vs. actual production model" clarification | Applied |
| should-fix | Industry | Upstart 10-K quote — soften to "model governance literature" | Applied |
| nice-to-have | Pedagogy | sklearn API continuity sentence | Applied: added in Connections section |
| nice-to-have | Industry | Framingham Risk Score mention | Applied: added as 1-sentence healthcare mention in Applications Gallery |

### Changes Applied to Brainstorm
- Concept 1: Added concrete numerical heteroskedasticity example (Var = P(1−P))
- Lab flow: Added `.predict_proba()[:,1]` instruction as first code comment
- Concept 3: Added sklearn solver note (lbfgs), softened cross-entropy/neural network connection, added linearity-in-log-odds assumption
- Poll 1: Added "Read carefully — NOT a problem" instruction
- Discussion Block 2 Level 6: Added imbalance setup sentence
- JPMorgan example: Added "regulatory floor, not production model" clarification
- Upstart citation: Softened from direct 10-K quote to "model governance literature"
- Applications Gallery: Added Framingham Risk Score sentence
- Connections: Added sklearn API continuity sentence

### Nice-to-Have Items Not Incorporated
- Healthcare/hiring examples: mentioned briefly but not developed into full case studies — time constraints in 60-min theory block.
- Probit model comparison: not included — introducing an alternative link function (probit) in the same lecture risks cognitive overload. Save for optional supplement.

---

*Revised brainstorm: `output/econ3916-econ5200-topic-17-classification-logistic-regression/brainstorm.md`. Draft stage reads the revised version.*
