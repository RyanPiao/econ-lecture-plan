# Discussion Facilitation Guide: Instrumental Variables

**Course:** ECON 5200: Applied Data Analytics in Economics
**Date:** 2026-03-22 | **Duration:** 75 min | **Type:** Presentation + Lab

---

## Pre-Class Checklist

- [ ] Mentimeter presentation loaded and tested (5 polls ready)
- [ ] Mentimeter join code projected on entry slide
- [ ] "Opening Hook" question written on whiteboard or displayed on second screen
- [ ] Timer visible to instructor (phone or laptop corner clock)
- [ ] `data/acs_iv_sample.csv` uploaded to course Google Drive for lab (share link in chat at 65 min mark)
- [ ] First stage F-statistic interpretation cheat sheet printed for quick reference during Poll 3

---

## Class Flow Map

| Clock | Duration | Activity | Interactive Element | Instructor Note |
|-------|----------|----------|--------------------|--------------------|
| 0:00 | 6 min | Opening Hook | Pose Amazon question after scenario | Wait 30 sec before speaking |
| 0:06 | 10 min | Section 1: Endogeneity | — | Write plim formula on board |
| 0:16 | 3 min | **Poll 1** | OLS consistency question | Expected ~40% correct |
| 0:19 | 12 min | Section 2: IV Estimator (2SLS) | — | Draw 2-stage diagram |
| 0:31 | 5 min | **Discussion Block 1** | 3 tiered questions | Think-pair-share on Q3 |
| 0:36 | 10 min | Section 3: Three Assumptions | — | Draw DAG: Z→X→Y, no Z→Y |
| 0:46 | 3 min | **Poll 2** | Which assumptions are testable? | Expected ~55% correct |
| 0:49 | 8 min | Section 4: First Stage + F-stat | — | Show F-stat table |
| 0:57 | 3 min | **Poll 3** | Weak instrument decision | Expected ~35% correct — big teaching moment |
| 1:00 | 10 min | Section 5: LATE | — | Timeline diagram: complier/always-taker/never-taker |
| 1:10 | 3 min | **Poll 4** | What does IV estimate? | Expected ~65% correct |
| 1:13 | 5 min | **Discussion Block 2** | LATE and external validity | Cold call on Q1 |
| 1:18 | 3 min | Connections + Takeaways | Hook payoff | Payoff: "Here's why Amazon's warehouse expansion works as an IV..." |
| 1:21 | 3 min | Lab introduction | — | Share Google Drive link; open Colab |
| 1:24 | ∞ min | Lab (in class or async) | — | Students begin Part 1 |
| **TOTAL** | **75 min** | | | |

---

## Opening Hook Script

**Display or write on board:**
> "Amazon wants to know: does faster delivery cause customers to spend more? They ran a regression. What's the problem?"

**Wait:** 30 seconds of silence. Resist the urge to fill it. A few students will start murmuring.

**If no response after 30 seconds:** "Someone tell me — if you're trying to estimate the effect of delivery speed on purchases, why would a simple OLS regression give the wrong answer?"

**Expected responses:** "Customers who order more are probably closer to warehouses." "Selection — people who buy a lot already are near distribution centers." These are both pointing at endogeneity.

**The reveal:** "Exactly — delivery speed is correlated with customer purchase behavior through geography. If you just regress purchases on speed, you're picking up this selection effect, not the causal impact of speed. A 2025 Stanford working paper solved this by using Amazon's warehouse expansion as an instrument. We'll come back to exactly how that works at the end of class. First, let's understand why OLS fails."

---

## Discussion Block 1: IV Intuition and Instrument Validity

*After Section 2 (2SLS) — approximately 31 minutes in*

**Setup (say this):**
> "Okay, you've now seen how 2SLS works mechanically. Before we go further, let's make sure we understand what's actually happening — and whether it actually solves the problem."

---

### Question A — Understanding (Bloom's Level 2, ~1 min)

**Pose (display or say):**
> "Walk me through in plain English why the second stage of 2SLS gives a consistent estimator when OLS fails."

**Wait:** 20 seconds. Then cold call if no volunteers.

**Strong answer:** "In the first stage, we project X onto Z. The predicted values X̂ only contain the variation in X that's explained by Z. Since Z is exogenous (uncorrelated with ε), X̂ is also exogenous. So regressing y on X̂ in the second stage is like regressing on an exogenous version of X."

**Partial answer:** "We use Z to predict X and then use the prediction..." → *Prompt:* "And why does that help? What's different about X̂ versus X?"

**If students say "we add Z as a control":** *Redirect immediately.* "That's IV-as-control, which is not the same thing. In 2SLS, Z is not in the second stage equation — it only appears in the first stage. The key is that we *replace* X with X̂, not that we *add* Z."

---

### Question B — Analysis (Bloom's Level 4, ~2 min)

**Pose:**
> "Suppose your first-stage R² is 0.85. Does this mean your IV estimate is valid? What else would you need?"

**Format:** Open class discussion

**Expected response:** Relevance is confirmed (high R²), but exogeneity and exclusion restriction require separate justification. Good answer includes specific mention of the institutional setting or randomization mechanism that makes Z plausibly exogenous.

**Common wrong turn:** "Yes, high R² confirms the instrument is valid." → *Redirect:* "R² tells you about the first assumption. Name the other two assumptions. Are either of them captured by R²?"

---

### Question C — Evaluation (Bloom's Level 6, ~2 min)

**Pose:**
> "You're advising Uber on estimating the causal effect of surge pricing on driver supply. Propose an instrument and argue whether it meets all three IV assumptions."

**Format:** Think-pair-share (30s think, 1min pair, 1min share)

**Expected positions:**
- *Weather events*: Relevant (bad weather increases demand, triggers surge). Exclusion restriction: debatable — does weather directly affect driver supply? Yes! Drivers may stay home in bad weather. Fails exclusion restriction.
- *Large local events (concerts, sports)*: Similar issue — events may directly affect driver behavior independent of surge.
- *Competitor (Lyft) price changes*: Potentially strong — Lyft surge affects Uber surge (platforms track each other), but Lyft-specific surges may not directly affect Uber driver supply decisions beyond the induced price change. Worth discussing.
- *Algorithm changes in a specific city*: Strong if the algorithm change is "as-good-as-random" — exclusion restriction defensible if the change is not correlated with driver characteristics.

**Close the loop:** "There's no perfect instrument here — this is why instrument choice is one of the hardest parts of applied econometrics. The goal is to find the least-bad option and argue for it honestly."

---

### Debrief 1

**Key insight:** The validity of an instrument is not determined by the data alone — it requires theoretical reasoning about the data-generating process.

**Bridge sentence (say this):**
> "Relevance you can see in the data. Exogeneity and the exclusion restriction you have to *argue*. This is why good IV papers read like legal briefs — they're making a case, not just reporting statistics."

**Transition:**
> "Now that we know what makes an instrument valid, let's talk about what makes one *weak* — and why a weak instrument is almost as bad as no instrument at all."

---

## Discussion Block 2: LATE and External Validity

*After Section 5 (LATE) — approximately 1:13 into class*

**Setup:**
> "Here's the uncomfortable truth about IV: even when everything works perfectly, you don't get what you might think you're getting."

---

### Question A — Understanding (~1 min)

**Cold call** a student by name:
> "Tell me: in Card (1995), give me a concrete example of a complier, an always-taker, and a never-taker."

**If the student struggles:** "Start with: what does the instrument (proximity to college) actually do? It raises the probability that someone attends college. Now: a complier is someone for whom it would change their decision..."

**Strong answer:**
- Complier: A student who attends college only because there's one within driving distance; if the nearest college were far away, they wouldn't go.
- Always-taker: A highly motivated student from a wealthy family who would attend regardless of distance.
- Never-taker: A student who won't attend college regardless of proximity (perhaps due to financial constraints, family obligations, or career preferences not served by college).

---

### Question B — Analysis (~2 min)

**Pose:**
> "If Card's estimate tells us the wage return for compliers — students at the margin of college attendance — why might this NOT be the right number for a policymaker who wants to make college free for everyone?"

**Expected response:** Making college free would primarily affect compliers (who currently don't attend due to accessibility/cost), but it would also affect never-takers (some of whom might now attend). The return for never-takers might be different (perhaps lower, since they previously chose not to attend). LATE captures the complier return, not the return for the new entrants that a free-college policy would create.

---

### Question C — Evaluation (~2 min)

**Pose:**
> "A pharmaceutical company uses changes in insurance coverage as an instrument to estimate the effect of Drug X on recovery rates. The FDA reviewer asks: 'Can we extrapolate this estimate to the full patient population?' How would you answer?"

**Expected range:**
- "No — this is LATE for patients whose treatment changed because of insurance coverage changes (compliers). Patients who were always going to get treated (always-takers) or never going to get treated (never-takers) are not represented."
- "It depends on whether compliers look similar to the broader population. We'd want to characterize compliers demographically."
- Strong answer also mentions that compliers in an insurance coverage instrument may be lower-income or younger patients — systematically different from the full patient population.

---

### Debrief 2

**Key insight:** IV's external validity is limited to compliers — this is a feature (clean identification) and a bug (restricted generalizability). Always ask: "Who are the compliers, and are they the population I care about?"

**Bridge sentence:**
> "LATE is the honest answer to a narrow question: 'What is the causal effect for the people whose behavior my instrument actually changed?' Before extrapolating to a broader population, you need to argue that compliers look like that population — and often, they don't."

**Closing — Hook Payoff:**
> "Let's go back to Amazon. The warehouse expansion is a valid instrument because: it's relevant (proximity predicts delivery speed), it's exogenous (warehouse locations were determined by logistics decisions unrelated to individual customer behavior), and the exclusion restriction holds if warehouse location doesn't directly affect purchase behavior except through delivery speed. The LATE estimates the effect for customers whose purchasing behavior was affected by the warehouse expansion — the compliers. Customers in areas where Amazon already had fulfillment centers (always-fast delivery) or customers who only use Amazon for infrequent specific purchases (never-switch) are not the compliers. The $4.20 estimate applies specifically to marginal customers who became more frequent buyers because of improved delivery speed."

---

## Energy Management

**If energy is low entering (flat class atmosphere in first 10 min):**
After posing the hook question, say: "Write down your answer — 30 seconds." This forces engagement before opening the room.

**If Discussion Block 1 is dragging (students giving one-word answers):**
Switch to think-pair-share immediately: "Turn to the person next to you — 60 seconds, share your answer to Question B."

**If Poll 3 (F < 10 decision) produces surprising results (most choose C — discard):**
> "Interesting — most of you are erring on the side of caution. That's actually the right instinct! But there's an important nuance: discarding an instrument with F=8.3 assumes you can find a better one. In many research designs, there IS no better instrument. The right question isn't 'is this instrument perfect?' but 'is this instrument better than OLS?' The answer might still be yes, even with F=8.3."

**If you're running 3–4 minutes over after Discussion Block 2:**
Drop the closing hook payoff and say: "I'll leave you with the IV payoff — read the last section of the lecture notes, it connects everything back to Amazon. Lab link is in the chat."

**If you have 8+ minutes extra (very efficient class):**
Use the opening hook's Level 6 extension: "Now design a IV strategy for DoorDash — they want to know whether restaurant photos on the app cause more orders. What's your instrument? Discuss with the person next to you."

---

*This facilitation guide accompanies `examples/sample-lecture-output.md` and `examples/sample-polls.md`.*
