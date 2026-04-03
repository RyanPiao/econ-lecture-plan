# Lecture Intake Form

**Generated:** {date}
**Output slug:** `{slug}`

---

## Course Information

```yaml
course_title: "{course_title}"
course_code: "{course_code}"
topic_title: "{topic_title}"
topic_number: {topic_number}
total_topics: {total_topics}
position_context: "{early | middle | late}"
course_category: "{ml-stats | game-theory | micro-theory | principles | finance | general}"
```

## Class Parameters

```yaml
class_length_minutes: {class_length_minutes}
class_type: "{presentation | lab | presentation + lab}"
audience_level: "{intro_undergrad | advanced_undergrad | masters}"
```

## Prerequisites

```yaml
prerequisites_covered:
{- "prerequisite_1"}
{- "prerequisite_2"}
{- "prerequisite_3"}
```
*(Leave empty list `[]` if not specified)*

## Supporting Materials

```yaml
supporting_docs_provided: {true | false}
supporting_docs_summary: >
  {3–5 sentence summary of provided materials — or "" if none}
flagged_outdated_examples:
{- "Example description (source year)"}
```

## Inferred Context

```yaml
depth_calibration: >
  {One sentence describing how topic position should affect depth and pacing.
   E.g., "Late-course topic — assume strong OLS and probability foundation,
   focus on synthesis and research-grade applications."}
key_prior_concepts_to_activate:
{- "concept_1"}
{- "concept_2"}
upcoming_topics_to_seed:
{- "topic_1"}
{- "topic_2"}
```

## Pipeline Flags

```yaml
interactive_elements_required: true
min_discussion_sets: 2
min_poll_questions: 3
lab_required: {true | false}
web_search_required: true
min_example_year: 2024
```

---

*This intake form is read by all downstream pipeline stages. Do not edit manually — re-run `/new-lecture` to regenerate.*
