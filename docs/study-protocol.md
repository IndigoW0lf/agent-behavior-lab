# Study 001 Protocol: Peer Influence

Status: **exploratory controls complete / confirmatory protocol frozen**

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

## Exploratory calibration history

The general calibration pool produced a repeated error on one Python
list-comprehension item. A generated filter/transform pool then found errors
that consistently selected the `filtered_after_transform` semantic distractor.
Counterbalancing moved every semantic choice through every answer letter; all
eight errors still selected that mechanism, ruling out a simple fixed-letter
preference as the explanation.

The next exploratory contrast reruns the counterbalanced calibration items at
baseline and with three simulated peers endorsing that specific distractor.
These calibration items are not eligible for the final confirmatory estimate.
The separately generated confirmatory split must remain unrun until the final
conditions, sample size, exclusions, and analysis are frozen.

### Targeted exploratory pilot analysis

The targeted pilot compares a fresh baseline with three unanimous simulated
peers endorsing the `filtered_after_transform` distractor. Its analysis is
fixed before running the influenced condition:

- **Primary outcome:** difference in accuracy between influenced and baseline
  conditions, reported as counts, percentages, and percentage points.
- **Secondary outcome:** difference in the rate of selecting the
  `filtered_after_transform` distractor.
- **Pairing:** match responses by counterbalanced item-and-form identifier and
  report the discordant-pair table.
- **Uncertainty:** report an exact McNemar test for the paired accuracy change;
  treat it as descriptive because this is exploratory calibration.
- **Exclusions:** exclude only provider failures or unparseable responses and
  report every exclusion by condition. Do not exclude incorrect items after
  viewing the result.

The pilot does not provide a confirmatory effect estimate, regardless of its
p-value. It is used to finalize the manipulation and estimate a defensible
sample size for the sealed split.

### Repetition-matched control analysis

The next exploratory control uses the same counterbalanced calibration items
and targeted wrong answer in three conditions:

1. baseline, with no added answer cue;
2. repetition control, with the wrong answer printed three times but attributed
   to no person or agent;
3. unanimous peers, with three named AI agents endorsing the wrong answer.

The primary contrast is unanimous peers versus repetition control. This tests
whether social attribution changes behavior beyond exposure to the same wrong
answer repeated the same number of times. Baseline is retained as a descriptive
reference, not as the test of social framing.

The analysis is fixed before collecting repetition-control responses:

- **Primary outcome:** paired accuracy difference between unanimous peers and
  repetition control.
- **Secondary outcome:** paired difference in selection of the
  `filtered_after_transform` distractor between those conditions.
- **Pairing:** match responses by counterbalanced item-and-form identifier.
- **Uncertainty:** report an exact McNemar test for the primary paired contrast;
  treat it as descriptive because the four answer-order forms of each underlying
  item are not independent.
- **Exclusions:** use the same registered provider-failure and unparseable-response
  rule as the targeted pilot, reporting every exclusion by condition.

This control can separate social attribution from simple repetition in this
prompt design. It cannot by itself establish a human-like social process, and
differences in surrounding wording remain a possible explanation.

The repetition control produced 75/96 correct responses (78.1%), compared with
22/96 (22.9%) under named unanimous peers. In the paired primary contrast, 53
responses changed from correct under repetition to wrong under peers and zero
changed in the opposite direction. The targeted-error selection rate increased
from 20.8% to 77.1%. Full results appear in
[`../results/study-001-repetition-control.md`](../results/study-001-repetition-control.md).

The final held-out design, primary test, power rationale, and decision rule are
frozen in [`confirmatory-plan.md`](confirmatory-plan.md). That document governs
the confirmatory run if it conflicts with earlier exploratory plans here.

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
