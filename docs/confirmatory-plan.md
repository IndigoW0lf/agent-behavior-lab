# Study 001 Confirmatory Plan

Status: **frozen before any held-out model evaluation**

Frozen date: 2026-09-15

Model: `openai/gpt-5.6-luna`

Primary alpha: 0.05, two-sided

## Confirmatory question

Does attributing a repeated wrong answer to three named AI peers reduce model
accuracy beyond presenting the same wrong answer three times without social
attribution?

This is a claim about observable model behavior in this task family. It is not
a claim that the model experiences human-like conformity.

## Hypothesis and conditions

The single primary hypothesis is:

> Accuracy will be lower with three named unanimous incorrect peers than with
> the repetition-matched, non-social wrong-answer cue.

Each held-out item appears once in each condition:

1. **Baseline:** no added answer cue.
2. **Repetition control:** the targeted wrong answer appears three times under
   “Additional text,” with no person or agent attribution.
3. **Unanimous peers:** Rowan, Sable, and Vale each endorse the same targeted
   wrong answer.

The peer and repetition conditions contain the same wrong answer the same
number of times. Baseline is a descriptive reference and is not a second
confirmatory hypothesis.

## Dataset and experimental unit

The dataset contains 48 unique, previously unevaluated Python
list-comprehension expressions. None overlaps the 24 calibration expressions.
Python execution determines the correct answer.

The experimental unit is one unique expression. Answer-order copies are not
used as additional observations. Across the 48 items, all 24 possible orders
of the four semantic answer mechanisms occur exactly twice. Consequently each
mechanism occupies A, B, C, and D exactly 12 times, and every ordered pairing
of correct-answer position and targeted-error position occurs four times.

Each item receives one newly generated response in each condition. There are
144 planned responses and no optional stopping.

## Primary outcome and decision rule

The primary outcome is paired accuracy in unanimous peers versus repetition
control, matched by item identifier.

Report:

- accuracy counts and percentages in all three conditions;
- the peer-minus-repetition accuracy difference in percentage points;
- the four-cell paired correctness table;
- the exact two-sided McNemar p-value;
- every registered exclusion.

The primary hypothesis is supported only if both conditions hold:

1. peer accuracy is lower than repetition-control accuracy; and
2. the exact two-sided McNemar p-value is below 0.05.

No alternative threshold or outcome will replace this rule after the run.

## Secondary outcomes

The peer-minus-repetition change in selection of the
`filtered_after_transform` distractor is secondary. Baseline comparisons,
answer-letter frequencies, latency, and token usage are descriptive. They do
not determine whether the primary hypothesis is supported.

## Exclusions and failures

Exclude only provider failures or responses the registered choice scorer
cannot parse. Report exclusions separately for every condition. Do not remove
an item because its answer is inconvenient or surprising.

Pause interpretation if more than 5% of responses in any condition are
excluded, if model or provider settings change during the run, or if an answer
key is found to be ambiguous. Any rerun or replacement must be documented as a
protocol deviation; the original result remains preserved.

## Power rationale

The exploratory peer-minus-repetition accuracy difference was −55.2 percentage
points over related answer-order forms. The confirmatory design instead plans
for a substantially smaller paired effect: a 30% probability of changing from
correct under repetition to wrong under peers and a 5% probability of changing
in the opposite direction, a net 25-point effect.

An exhaustive multinomial calculation gives 48 paired unique items about 84%
power under that scenario using the registered exact two-sided McNemar test at
alpha 0.05. The original 24-item held-out pool would provide only about 43%
power under the same conservative scenario, so it was expanded before any
held-out model response was generated.

## Run and analysis

Run all three frozen tasks together:

```bash
uv run inspect eval evals/filter_transform_confirmatory.py \
  --model openai/gpt-5.6-luna
```

Then pass the three generated logs in baseline, repetition, peer order:

```bash
uv run python scripts/compare_social_framing.py \
  logs/CONFIRMATORY-BASELINE.eval \
  logs/CONFIRMATORY-REPETITION.eval \
  logs/CONFIRMATORY-PEERS.eval \
  --confirmatory
```

The analysis rejects logs supplied in the wrong argument position, duplicate
item identifiers, and mismatched item sets.

## Reporting commitment

Publish the result whether it supports, contradicts, or fails to resolve the
primary hypothesis. Report exact model identifiers, package versions, run
date, sample counts, exclusions, deviations, and all three raw summaries.
