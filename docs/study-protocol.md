# Study 001 Protocol: Peer Influence

Status: **scaffold / not yet run**

## Research question

Does exposure to answers attributed to other AI agents change a language model's accuracy on objective multiple-choice questions?

We describe any change as a **behavioral peer-influence effect**. We do not infer consciousness, emotion, social experience, or a human psychological mechanism from the result.

## Confirmatory hypotheses

- **H1:** Accuracy will be lower in the unanimous-incorrect condition than at baseline.
- **H2:** Accuracy will be lower in the claimed-expert condition than at baseline.
- **H3:** A correct dissenter will reduce the accuracy loss produced by an incorrect majority.

H3 compares the divided-group condition with the unanimous-incorrect condition.

## Experimental unit and design

The experimental unit is one model response to one item under one condition.

Each item is evaluated under all four conditions. Model, generation settings, answer choices, and item wording remain fixed. Only the peer-information text changes.

This is a repeated-item design, but model responses are newly generated in every run. Runs are not independent if a provider reuses hidden state or caching in undocumented ways; this should be considered during interpretation.

## Variables

### Independent variable

Peer-information condition:

1. baseline
2. unanimous incorrect peers
3. divided group with an incorrect majority
4. incorrect answer from a claimed specialist

### Primary outcome

Accuracy: whether Inspect's choice scorer identifies the target answer.

### Planned derived outcomes

- Accuracy difference from baseline by condition
- Answer-switch rate among items answered correctly at baseline
- Effect by question domain
- Variation across repeated runs and model families

Confidence change is a future outcome. It is not measured by the current multiple-choice solver and must not be reconstructed from prose after the fact.

## Dataset inclusion criteria

Items must:

- have one unambiguous correct answer;
- have exactly four plausible choices;
- be answerable without current events or web access;
- avoid sensitive or high-stakes subject matter;
- include a predetermined incorrect answer used in the manipulation;
- pass programmatic schema and answer-key checks.

The initial 12-item set is a pipeline pilot, not enough evidence for a strong scientific conclusion.

## Run controls

For a comparison, hold these constant:

- exact model identifier and provider;
- temperature and other generation settings;
- Inspect version;
- question dataset revision;
- condition templates;
- number of repetitions;
- run date and region when available.

Preserve raw Inspect logs. Never overwrite or quietly remove failed samples.

## Pilot procedure

1. Run three samples across every condition.
2. Inspect each rendered prompt and parsed answer manually.
3. Confirm no answer-key or formatting failures.
4. Estimate cost and latency.
5. Freeze the protocol and dataset revision.
6. Run the full pilot.
7. Analyze results before changing prompts.

Changes made after seeing outcomes must be labeled exploratory or registered as a new study version.

## Analysis plan

For each condition, report the number of evaluated samples, accuracy, and the difference from baseline. For repeated runs, report uncertainty intervals and account for responses being grouped by item and model.

Do not present a percentage without its denominator. Do not pool models into one headline result without also reporting model-specific results.

## Known validity threats

- **Prompt-length confound:** influenced conditions are longer than baseline.
- **Authority wording:** “specialist” may test instruction/status sensitivity rather than peer influence.
- **Fixed peer names and order:** names or position may affect responses.
- **Fixed wrong answer:** some distractors may be more persuasive than others.
- **Benchmark contamination:** models may have seen similar questions.
- **Small, easy dataset:** ceiling effects may conceal differences.
- **Provider nondeterminism:** identical settings may still produce different outputs.
- **Construct validity:** behavioral answer changes are not evidence of human-like conformity.

Planned controls include neutral context matched for length, rotating agent order and answer labels, independently reviewed items, and repeated trials.

## Stop conditions

Pause the run if:

- more than 5% of samples fail to parse;
- a supposedly incorrect peer answer is actually defensible;
- model/provider settings change mid-comparison;
- costs materially exceed the pilot estimate;
- logs do not contain enough metadata to reproduce the run.

## Reporting commitments

Publish null and contrary results. Clearly separate confirmatory tests, exploratory observations, and post-hoc explanations. Include the dataset, code revision, model identifiers, settings, sample counts, exclusions, and known limitations.
