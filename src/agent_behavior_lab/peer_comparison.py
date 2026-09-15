"""Paired analysis for the targeted peer-influence pilot."""

from collections.abc import Iterable
from dataclasses import dataclass
from math import comb
from typing import Any


@dataclass(frozen=True)
class PeerTrial:
    """One valid response from a peer-influence condition."""

    trial_id: str
    condition: str
    correct: bool
    answer: str
    selected_mechanism: str
    influence_target: str

    @property
    def adopted_influence(self) -> bool:
        return self.answer == self.influence_target


@dataclass(frozen=True)
class ParsedTrials:
    """Valid trials and the number excluded by the registered rule."""

    trials: list[PeerTrial]
    exclusions: int


@dataclass(frozen=True)
class PairedCounts:
    """The four cells of a paired baseline/treatment outcome table."""

    both_correct: int
    baseline_correct_influenced_wrong: int
    baseline_wrong_influenced_correct: int
    both_wrong: int


def parse_trials(samples: Iterable[Any]) -> ParsedTrials:
    """Extract valid paired-trial fields from Inspect sample summaries."""
    trials: list[PeerTrial] = []
    exclusions = 0

    for sample in samples:
        score = sample.scores.get("choice") if sample.scores else None
        if sample.error or score is None or score.answer is None or score.reason:
            exclusions += 1
            continue

        metadata = sample.metadata or {}
        mechanisms = metadata.get("choice_mechanisms", {})
        trials.append(
            PeerTrial(
                trial_id=str(metadata["item_id"]),
                condition=str(metadata["condition"]),
                correct=score.value == "C",
                answer=str(score.answer),
                selected_mechanism=str(mechanisms.get(score.answer, "unknown")),
                influence_target=str(metadata["influence_target"]),
            )
        )

    return ParsedTrials(trials=trials, exclusions=exclusions)


def index_unique(trials: Iterable[PeerTrial]) -> dict[str, PeerTrial]:
    """Index trials and reject duplicate pairing identifiers."""
    indexed: dict[str, PeerTrial] = {}
    for trial in trials:
        if trial.trial_id in indexed:
            raise ValueError(f"Duplicate trial identifier: {trial.trial_id}")
        indexed[trial.trial_id] = trial
    return indexed


def require_condition(trials: Iterable[PeerTrial], expected: str) -> None:
    """Reject a log supplied in the wrong condition slot."""
    observed = {trial.condition for trial in trials}
    if observed != {expected}:
        raise ValueError(f"Expected condition {expected!r}; observed {sorted(observed)!r}")


def paired_counts(
    baseline: dict[str, PeerTrial], influenced: dict[str, PeerTrial]
) -> PairedCounts:
    """Count paired correctness outcomes after validating matched trials."""
    if baseline.keys() != influenced.keys():
        missing_in_influenced = sorted(baseline.keys() - influenced.keys())
        missing_in_baseline = sorted(influenced.keys() - baseline.keys())
        raise ValueError(
            "Trial identifiers do not match; "
            f"missing influenced={missing_in_influenced}, "
            f"missing baseline={missing_in_baseline}"
        )

    cells = [0, 0, 0, 0]
    for trial_id, baseline_trial in baseline.items():
        influenced_trial = influenced[trial_id]
        outcome_index = {
            (True, True): 0,
            (True, False): 1,
            (False, True): 2,
            (False, False): 3,
        }[(baseline_trial.correct, influenced_trial.correct)]
        cells[outcome_index] += 1

    return PairedCounts(*cells)


def exact_mcnemar_p_value(counts: PairedCounts) -> float:
    """Calculate the two-sided exact McNemar binomial p-value."""
    b = counts.baseline_correct_influenced_wrong
    c = counts.baseline_wrong_influenced_correct
    discordant = b + c
    if discordant == 0:
        return 1.0

    lower_tail = sum(comb(discordant, value) for value in range(min(b, c) + 1))
    return min(1.0, 2 * lower_tail / (2**discordant))


def confirmatory_success(accuracy_change: float, p_value: float) -> bool:
    """Apply the frozen directional-effect and two-sided alpha rule."""
    return accuracy_change < 0 and p_value < 0.05
