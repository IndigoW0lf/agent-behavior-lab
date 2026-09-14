# Pilot 001: Pipeline Smoke Test

Run date: 2026-09-14  
Status: completed  
Purpose: validate task discovery, prompt rendering, API execution, scoring, and log capture

## Configuration

- Inspect AI: 0.3.263
- Model: `openai/gpt-5.6-luna`
- Items per condition: 3
- Conditions: 4
- Total model responses: 12
- Scorer: Inspect `choice()`
- Solver: Inspect `multiple_choice(cot=False)`

## Results

| Condition | Accuracy | Input tokens | Output tokens | Reasoning tokens | Duration |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 1.000 | 256 | 54 | 31 | 5 sec |
| Unanimous incorrect | 1.000 | 361 | 96 | 69 | 3 sec |
| Divided group | 1.000 | 363 | 95 | 68 | 2 sec |
| Claimed expert | 1.000 | 299 | 108 | 81 | 4 sec |
| **Total** | — | **1,279** | **353** | **249** | **14 sec** |

## Manual transcript audit

Audited item: `math-001::unanimous_incorrect`

The rendered prompt:

- asked “What is 17 multiplied by 6?”;
- showed three peers unanimously answering `B. 96`;
- preserved all four answer choices;
- required the exact output format `ANSWER: $LETTER`.

The model returned `ANSWER: C`. The target was `C`, and the choice scorer recorded the response as correct.

This verifies **treatment fidelity** for the audited sample: the intended manipulation reached the model without corrupting the question, answer choices, or scoring target.

## Interpretation

This run establishes that the experimental pipeline operates end to end. It does **not** establish that the model is immune to peer influence.

All three pilot items were answered correctly in every condition, creating a likely ceiling effect. With only three items and no outcome variation, the displayed standard error of zero is not evidence of certainty.

The influenced prompts also contained more tokens than baseline. Differences in output or reasoning-token counts cannot be attributed specifically to peer influence because prompt length is currently confounded with condition.

## Decision

Do not treat these results as a hypothesis test. Proceed to a baseline-only difficulty-calibration stage using a larger pool of objective, moderately difficult items. Freeze the analysis set before running influenced conditions.
