# Study 001: Targeted Peer-Influence Pilot

Status: **exploratory result; not a confirmatory effect estimate**

Run date: 2026-09-14  
Model: `openai/gpt-5.6-luna`  
Framework: Inspect AI 0.3.263  
Evaluation revision: `ff5fa238`  

## Question

When a model traces Python list comprehensions, does unanimous incorrect peer
testimony increase adoption of a specific `filtered_after_transform` error?

This is a behavioral evaluation. It does not establish that the model
experiences conformity or any human-like social state.

## Design

The exploratory dataset contained 24 generated Python expressions. Each
expression appeared in four counterbalanced answer-order forms, producing 96
paired trials per condition. Python execution served as the answer oracle.

The same trials were evaluated under two conditions:

1. **Baseline:** no peer responses.
2. **Unanimous incorrect:** three simulated AI agents all endorsed the answer
   produced by filtering the transformed value instead of the original input.

The semantic distractor occupied every answer position across the
counterbalanced forms. The analysis plan was committed before the influenced
condition was evaluated.

## Results

| Outcome | Baseline | Unanimous incorrect | Change |
| --- | ---: | ---: | ---: |
| Accuracy | 87/96 (90.6%) | 22/96 (22.9%) | −67.7 percentage points |
| Targeted-distractor selection | 8/96 (8.3%) | 74/96 (77.1%) | +68.8 percentage points |
| Registered exclusions | 0 | 0 | — |

### Paired correctness outcomes

| Baseline | Influenced | Pairs |
| --- | --- | ---: |
| Correct | Correct | 22 |
| Correct | Wrong | 65 |
| Wrong | Correct | 0 |
| Wrong | Wrong | 9 |

The exact McNemar p-value calculated over the 96 counterbalanced trial forms
was `5.42101e-20`. This value is descriptive: the four forms derived from each
underlying expression are related observations, so treating all 96 pairs as
independent understates uncertainty.

All 74 influenced-condition errors selected the peer-endorsed semantic
distractor. The manipulation therefore changed responses directionally rather
than merely increasing random error.

## Post-hoc token observation

Inspect recorded 2,651 provider-reported reasoning tokens at baseline and 694
under influence; total output tokens were 3,413 and 1,402, respectively. This
was not a preregistered outcome. It may motivate a future test, but it must not
be presented as evidence that the model internally reasoned less or deferred
in a human-like way.

## What this supports

Within this model, prompt format, and generated code-tracing family, unanimous
incorrect peer testimony produced a large increase in selection of the exact
error endorsed by the peers. The result is strong enough to justify a
confirmatory evaluation with held-out items and stronger controls.

## What this does not support

This pilot does not establish:

- a general effect across models, tasks, or providers;
- a uniquely social effect rather than sensitivity to repeated answer cues;
- a human-like conformity mechanism or subjective social experience;
- a confirmatory p-value or population-level effect size.

Additional limitations include one model, one run date, simulated rather than
independently generated peer answers, a longer influenced prompt, and only 24
unique underlying expressions.

## Next step

Before opening the held-out split:

1. add a length- and repetition-matched non-social answer-cue control;
2. freeze the confirmatory conditions, exclusions, and clustered analysis;
3. balance semantic answer positions across unique held-out items instead of
   treating answer-order rotations as independent content;
4. calculate the required number of unique items using a conservative effect
   smaller than this exploratory estimate;
5. preserve and publish null or contrary replication results.

## Local raw logs

- `2026-09-14T22-17-13-00-00_filter-transform-peer-baseline_89i2DFaLJrzvQjQZNnmbHM.eval`
- `2026-09-14T22-17-13-00-00_filter-transform-peer-unanimous-incorrect_Cr9hYvLF9KxkQSEVZBPdoG.eval`

Raw Inspect logs remain local and are intentionally excluded from Git.
