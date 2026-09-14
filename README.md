# Agent Behavior Lab

Reproducible experiments studying social influence and behavioral stability in AI systems.

## Study 001: Peer Influence

**Research question:** When a language model sees answers attributed to other AI agents, how often does it abandon a correct answer?

This first study adapts a classic social-influence design to model evaluation. It does **not** claim that language models experience human conformity. It measures a behavioral analogue: whether peer testimony changes an observable answer.

### Experimental conditions

| Condition | Information shown before answering |
| --- | --- |
| Baseline | No peer responses |
| Unanimous incorrect | Three peers give the same incorrect answer |
| Divided group | Two peers are incorrect and one is correct |
| Claimed expert | A purported specialist gives an incorrect answer |

Every question appears in every condition. This repeated-item design helps separate the effect of the condition from differences in question difficulty.

### Current milestone

- Completed an exploratory targeted peer-influence pilot
- Observed accuracy fall from 90.6% to 22.9% under unanimous incorrect peers
- Counterbalanced answer positions and tracked semantic error mechanisms
- Preserved a separate, unrun confirmatory split
- Added paired analysis with registered exclusions and an exact McNemar test
- Documented results and validity limits in
  [`results/study-001-exploratory-peer-pilot.md`](results/study-001-exploratory-peer-pilot.md)

The observed effect is exploratory. It motivates a controlled confirmatory
study but is not itself a general estimate of model behavior.

## Quick start

Requirements: Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone git@github.com:IndigoW0lf/agent-behavior-lab.git
cd agent-behavior-lab
uv sync --extra dev
cp .env.example .env
```

Add one model-provider API key to `.env`, then run a cheap three-question smoke test:

```bash
uv run inspect eval evals/peer_influence.py --model openai/gpt-5.6-luna --limit 3
```

Run the full set only after inspecting the smoke-test prompts and logs:

```bash
uv run inspect eval evals/peer_influence.py --model openai/gpt-5.6-luna
uv run inspect view
```

Inspect supports many hosted and local providers; replace the model identifier with one you have access to. API calls may incur costs.

Run the deterministic tests without calling a model:

```bash
uv run pytest
uv run ruff check .
```

## Repository map

```text
data/questions.jsonl                 Objective question set
docs/study-protocol.md               Hypotheses, variables, and validity limits
evals/peer_influence.py              Inspect evaluation tasks
src/agent_behavior_lab/conditions.py Prompt-condition implementation
tests/                               Deterministic integrity tests
```

## Why Inspect?

An Inspect evaluation is built from a **dataset**, a **solver**, and a **scorer**:

- The dataset defines what is tested.
- The solver defines how the model is prompted and invoked.
- The scorer turns the response into a measurement.

That separation is valuable research engineering: changing a prompt should not silently change the answer key, and changing a model should not require rewriting the experiment.

## Roadmap

1. Run and manually audit a small pilot.
2. Add paired-run analysis and uncertainty intervals.
3. Expand and independently review the question set.
4. Add neutral-context and label-order controls.
5. Compare multiple models and repeated stochastic runs.
6. Replace simulated peers with actual model-generated peer responses.
7. Publish a short technical report with data and limitations.

## Difficulty calibration

Before running the social-information conditions at scale, calibrate baseline
difficulty using a separate 32-item pool:

```bash
uv run inspect eval evals/calibration.py --model openai/gpt-5.6-luna
```

Summarize the resulting log by domain and difficulty, including each missed
item:

```bash
uv run python scripts/analyze_calibration.py logs/YOUR-CALIBRATION-LOG.eval
```

For a stability check, run five independent epochs and analyze the new log:

```bash
uv run inspect eval evals/calibration.py --model openai/gpt-5.6-luna --epochs 5
```

The calibration pool is generated deterministically from reviewed item
specifications. Regenerate it with:

```bash
uv run python scripts/build_calibration_dataset.py
```

Calibration results select an informative difficulty range; they are not part
of the confirmatory peer-influence analysis.

### Targeted filter/transform calibration

Repeated baseline runs isolated a systematic filter-direction error in a
Python list-comprehension item. The targeted follow-up uses generated parallel
items to test whether that mechanism generalizes:

```bash
uv run inspect eval evals/filter_transform.py \
  --model openai/gpt-5.6-luna \
  --epochs 3
```

The generator creates separate calibration and confirmatory splits. Do not run
the confirmatory split while developing or selecting the manipulation.

Run the counterbalanced position check before attributing errors to a reasoning
mechanism. It rotates each semantic answer through all four letter positions:

```bash
uv run inspect eval evals/filter_transform.py@filter_transform_position_check \
  --model openai/gpt-5.6-luna
```

Run the exploratory targeted peer-influence contrast on the counterbalanced
calibration items:

```bash
uv run inspect eval evals/filter_transform_peer.py \
  --model openai/gpt-5.6-luna
```

This runs a fresh baseline and a unanimous-incorrect condition in which three
simulated peers endorse the `filtered_after_transform` semantic distractor.
The confirmatory split remains unused.

Compare the two resulting logs with the prespecified paired analysis:

```bash
uv run python scripts/compare_peer_influence.py \
  logs/BASELINE.eval \
  logs/UNANIMOUS-INCORRECT.eval
```

```bash
uv run python scripts/build_filter_transform_dataset.py
```

## Research stance

We will distinguish measured behavior from claims about internal mental states, publish negative results, preserve raw logs, and document deviations from the protocol.

## License

MIT
