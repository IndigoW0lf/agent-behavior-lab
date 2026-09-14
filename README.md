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

- 12 objective multiple-choice questions
- Four controlled prompt conditions
- Inspect task definitions
- Exact-answer scoring
- Unit tests for condition generation and dataset integrity
- A preregistered study protocol

This is the experiment scaffold, not a completed empirical result. No claims should be made until real model runs, validation, and analysis are complete.

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
uv run inspect eval evals/peer_influence.py --model openai/gpt-5 --limit 3
```

Run the full set only after inspecting the smoke-test prompts and logs:

```bash
uv run inspect eval evals/peer_influence.py --model openai/gpt-5
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

## Research stance

We will distinguish measured behavior from claims about internal mental states, publish negative results, preserve raw logs, and document deviations from the protocol.

## License

MIT
