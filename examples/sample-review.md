# Peer Review Report

**Topic:** Instrumental Variables
**Course:** ECON 5200: Applied Data Analytics in Economics
**Brainstorm reviewed:** `output/econ5200-topic-08-instrumental-variables/brainstorm.md`
**Review date:** 2026-03-22

---

## Pedagogy Review 🎓

**Overall assessment:** Strong

**Strengths:**
1. The Amazon delivery hook is genuinely compelling — it creates immediate curiosity and connects to something students use every day. The 6-minute allocation is appropriate for a masters class.
2. The three Bloom's levels are well-designed across both discussion blocks. The Level 6 questions (Uber instrument design, FDA pharmaceutical question) have productive ambiguity that will generate real debate.

**Issues:**

| Priority | Issue | Specific Fix |
|----------|-------|-------------|
| must-fix | Concept 5 (LATE) is allocated only 7 minutes, but it contains the most conceptually difficult material — complier heterogeneity requires significant unpacking for students new to potential outcomes | Expand LATE to 10 minutes, trim Applications Gallery from 3 to 1 minute (students can read this independently), and shorten Discussion Block 1 from 5 to 4 minutes |
| should-fix | The Discussion Block 2 Level 2 question ("What is a complier?") is too open-ended for a check-in question — students may give incomplete answers that derail the transition to Level 4 | Add a specific prompt: "For the Card (1995) college proximity instrument, give me a concrete example of a complier, an always-taker, and a never-taker" — this forces precision |
| should-fix | No cognitive pause between Concepts 3 and 4 (assumptions → F-statistic) — this is a lot of new material back-to-back | Insert Poll 2 (which assumptions are testable?) between Concepts 3 and 4, creating a natural break. (Already planned — confirm placement in draft.) |
| nice-to-have | The opening hook could be strengthened by posing the question before giving the Amazon data point — let students reason about the endogeneity problem themselves first, then reveal the data | Restructure hook: question first (1 min), student responses (1 min), then the Amazon data reveal (2 min) |

**Interactive elements specific feedback:**
- Discussion questions: Excellent. Level 6 questions are genuine evaluation tasks, not disguised comprehension questions.
- Poll questions: Poll 3 (weak instruments) is particularly well-designed — the expected 35% correct rate will create a strong teaching moment.
- Debrief notes: Good detail in Discussion Block 1; Discussion Block 2 debrief needs explicit bridging sentence (added below in synthesis changes).

---

## Domain Review 📊

**Overall assessment:** Rigorous. One notation issue and one missing nuance.

**Errors or inaccuracies:**

| Priority | Error | Correct statement |
|----------|-------|------------------|
| must-fix | LATE section states "IV estimates LATE under the monotonicity assumption" but does not state what monotonicity means | Add: "Monotonicity (Imbens & Angrist 1994) requires that the instrument pushes all units in the same direction — there are no defiers (units for whom Z=1 causes D=0 and Z=0 causes D=1). This is a non-trivial assumption; in practice it's argued on subject-matter grounds." |
| should-fix | The IV standard errors note says "always larger than OLS" — this is true in the limit but not guaranteed in finite samples with overidentified models | Soften to: "In just-identified models, IV standard errors are always at least as large as OLS. In overidentified models, efficiency gains are possible." |

**Missing nuance:**

- The discussion of the exclusion restriction should mention the possibility of testing it via over-identification (Sargan-Hansen J-test) when there are multiple instruments. Noting that most applied IV is just-identified (one instrument, one endogenous variable) and therefore untestable via J-test is important.
- The weak instruments section should reference the Stock-Wright-Yogo (2002) critical values table, not just the F>10 rule of thumb. Many journals now require reporting the effective F-statistic or the Lee et al. (2022) tF-statistic.

**Literature updates:**
- Add citation to Lee, McCrary, Moreira, and Porter (2022, QJE) for the tF-procedure — this is the current best practice for weak instrument inference and is increasingly expected in referee reports.
- The Romer & Romer monetary policy instrument has been substantially updated in Bauer & Swanson (2023, AER) — the original Romer & Romer instrument suffers from information effects (the Fed has private information that markets learn about from the announcement). The updated instrument is cleaner.

**Notation issues:**
- The 2SLS matrix formula uses P_Z notation without defining it. Add: "where P_Z = Z(Z'Z)⁻¹Z' is the projection matrix onto the column space of Z."

---

## Industry Review 💼

**Overall assessment:** Job-ready. Strong on specificity; one example needs updating.

**Example quality assessment:**

| Example | Assessment | Suggested improvement |
|---------|------------|----------------------|
| Amazon delivery (2025 Stanford working paper) | Strong — specific numbers, names the variation used as instrument | Confirm the working paper is publicly accessible (add URL); if paywalled, substitute with the DoorDash promotion example which has a published blog post |
| DoorDash promotion bias (HBR 2025) | Strong — specific dollar amount ($180M), concrete business problem | Verify URL accessibility and add it |
| Airbnb host response time (2024) | Strong — clear identification strategy, specific numbers (0.8% vs 3.2%) | |
| Card (1995) / Zimmerman (2024) | Appropriate for academic credibility — use as "the classic case" anchor | |
| Federal Reserve monetary policy | Strong for macro students but may feel abstract for practitioners | Add a connecting sentence: "This is how the Fed's own economists estimate the impact of their interest rate decisions — directly relevant for anyone working in macro forecasting or fixed income" |

**Missing applications:**
- Healthcare: IV is heavily used in health economics (e.g., distance to hospital as instrument for treatment intensity). Given that healthcare is one of the largest employers of economics master's graduates, worth a brief mention.
- A/B test disruptions as instruments (the Duolingo example from brainstorm) is excellent and should be elevated — this is increasingly common in tech companies.

**Currency issues:**
- The Bauer & Swanson (2023) update to the Romer-Romer instrument should replace the original citation — this is now the industry standard at the Fed and in financial institutions.

**Career connection assessment:**
The LATE discussion explicitly connects to why "you can't just extrapolate your IV estimate to the full population" — this is the exact conversation economists at tech companies have with product managers who want to generalize A/B test results. Strong on career connection.

---

## Synthesis

### All Issues — Prioritized

| Priority | Reviewer | Issue | Status |
|----------|----------|-------|--------|
| must-fix | Pedagogy | Expand LATE to 10 min, trim Applications Gallery | Applied: LATE expanded to 10 min; Applications Gallery becomes reading-only |
| must-fix | Domain | Add monotonicity definition to LATE section | Applied: added Imbens & Angrist (1994) monotonicity definition |
| must-fix | Domain | Add P_Z definition in matrix formula | Applied |
| should-fix | Pedagogy | Make Discussion Block 2 Level 2 question more precise | Applied: added complier/always-taker/never-taker framing |
| should-fix | Domain | Soften "IV SEs always larger than OLS" claim | Applied: added caveat for overidentified case |
| should-fix | Domain | Add over-identification test (J-test) discussion | Applied: added in Concept 3 section |
| should-fix | Domain | Add Lee et al. (2022) tF-statistic citation | Applied: added in Concept 4 |
| should-fix | Domain | Update Romer-Romer to Bauer-Swanson (2023) | Applied |
| should-fix | Industry | Add healthcare IV example as brief mention | Applied: 1 sentence added to Applications Gallery |
| should-fix | Industry | Add career connection sentence to monetary policy example | Applied |
| nice-to-have | Pedagogy | Restructure hook: question first, then data reveal | Not applied: restructuring the hook risks losing the concrete anchor. Current structure (scenario → data → question) is more pedagogically sound for a grad class. |
| nice-to-have | Domain | Add Sargan-Hansen J-test details | Not applied: time constraint. Added to Supplementary Resources for ambitious students. |

### Changes Applied to Brainstorm
- LATE section expanded with monotonicity definition and 2 additional minutes of allocated time
- Applications Gallery moved from timed lecture content to self-study reading
- Discussion Block 2 Level 2 question made more specific
- IV standard errors claim softened with overidentification caveat
- P_Z defined in matrix formula
- Lee et al. (2022) tF reference added
- Bauer-Swanson (2023) replaces Romer-Romer (2004) in Applications Gallery
- Healthcare IV brief mention added
- Career connection sentence added to monetary policy example

### Nice-to-Have Items Not Incorporated
- Hook restructuring: current structure (scenario → data → question) is more appropriate for graduate-level students who benefit from concrete grounding before abstract reasoning.
- Full J-test treatment: added to supplementary resources instead; covers over-identified IV for students who want to go deeper.

---

*Revised brainstorm available at `output/econ5200-topic-08-instrumental-variables/brainstorm.md`. Draft stage reads the revised version.*
