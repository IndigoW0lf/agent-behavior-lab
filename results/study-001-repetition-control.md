# Study 001: Repetition-Matched Social-Framing Control

Status: **exploratory control result; not a confirmatory effect estimate**

Run date: 2026-09-15  
Model: `openai/gpt-5.6-luna`  
Framework: Inspect AI 0.3.263

## Question

Does attributing a repeated wrong answer to three named AI peers change model
behavior beyond presenting the same wrong answer three times without social
attribution?

This evaluation measures observable answer changes. It does not establish that
the model experiences human-like conformity or any subjective social state.

## Design

The exploratory dataset contained 24 generated Python list-comprehension
expressions. Each appeared in four counterbalanced answer-order forms, producing
96 paired trials per condition. Python execution served as the answer oracle.

The same trials appeared in three conditions:

1. **Baseline:** no added answer cue.
2. **Repetition control:** the targeted wrong answer appeared three times under
   the neutral heading “Additional text,” without attribution to a person or
   agent.
3. **Unanimous peers:** three named AI agents each endorsed that same wrong
   answer.

The primary contrast—unanimous peers versus repetition control—was committed
before the repetition-control responses were collected.

## Results

| Outcome | Baseline | Repetition | Named peers |
| --- | ---: | ---: | ---: |
| Accuracy | 87/96 (90.6%) | 75/96 (78.1%) | 22/96 (22.9%) |
| Targeted-distractor selection | 8/96 (8.3%) | 20/96 (20.8%) | 74/96 (77.1%) |
| Registered exclusions | 0 | 0 | 0 |

Relative to baseline, repeating the wrong answer without social attribution
reduced accuracy by 12.5 percentage points. Relative to repetition, naming
three unanimous AI peers reduced accuracy by a further 55.2 percentage points
and increased selection of the targeted error by 56.2 points.

### Primary paired contrast

| Repetition control | Named peers | Pairs |
| --- | --- | ---: |
| Correct | Correct | 22 |
| Correct | Wrong | 53 |
| Wrong | Correct | 0 |
| Wrong | Wrong | 21 |

The exact two-sided McNemar p-value over the 96 counterbalanced forms was
`2.22045e-16`. This is descriptive rather than confirmatory because the four
answer-order forms derived from each underlying expression are related
observations.

The zero wrong-to-correct switches and 53 correct-to-wrong switches show a
strongly directional change. The increase in the exact peer-endorsed semantic
distractor indicates that the peer prompt pulled responses toward a specific
error rather than merely adding random noise.

## Interpretation

Simple repetition influenced the model, but it did not account for most of the
observed peer-condition effect. Within this model, prompt format, and item
family, attributing the repeated answer to unanimous AI peers produced a much
larger behavioral change than repetition without attribution.

This supports advancing to a held-out confirmatory test of the narrower claim:

> Named unanimous peer attribution reduces accuracy relative to an otherwise
> repeated, non-social answer cue.

## Limitations

This result does not establish:

- a general effect across models, tasks, or providers;
- a human-like psychological conformity mechanism;
- which specific part of the social wording caused the effect;
- an effect size that generalizes beyond this generated code-tracing family.

The peer and repetition prompts still differ in surrounding wording and length.
The study used one model, one run per condition, simulated peer testimony, and
24 unique expressions expanded into 96 related answer-order forms.

## Confirmatory-design consequence

The unique question—not an answer-order copy—must be the confirmatory unit of
analysis. A power audit found that the original 24-item held-out pool would be
underpowered for a deliberately smaller effect. Before any held-out model run,
the confirmatory protocol should therefore:

1. use 48 unique, untouched expressions;
2. balance semantic answer positions exactly across those unique items;
3. compare named peers with the repetition control as the single primary test;
4. retain baseline as a descriptive reference;
5. freeze the exclusion rule, significance threshold, and analysis code;
6. run each unique item once per condition without optional stopping.

## Local raw logs

- `2026-09-14T22-17-13-00-00_filter-transform-peer-baseline_89i2DFaLJrzvQjQZNnmbHM.eval`
- `2026-09-15T04-34-02-00-00_filter-transform-repeated-incorrect_QArd6hDni5e4qC6L7dh4CJ.eval`
- `2026-09-14T22-17-13-00-00_filter-transform-peer-unanimous-incorrect_Cr9hYvLF9KxkQSEVZBPdoG.eval`

Raw Inspect logs remain local and are intentionally excluded from Git.
