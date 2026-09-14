"""Summarize Inspect calibration logs without exposing raw logs publicly."""

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CalibrationResult:
    """The fields needed to diagnose one calibration response."""

    sample_id: str
    epoch: int
    domain: str
    difficulty: str
    question: str
    target: str
    answer: str
    rationale: str
    correct: bool


def results_from_samples(samples: Iterable[Any]) -> list[CalibrationResult]:
    """Extract calibration results from Inspect sample summaries."""
    results: list[CalibrationResult] = []

    for sample in samples:
        if not sample.scores or "choice" not in sample.scores:
            raise ValueError(f"Sample {sample.id!r} has no 'choice' score")

        score = sample.scores["choice"]
        metadata = sample.metadata or {}
        results.append(
            CalibrationResult(
                sample_id=str(sample.id),
                epoch=int(sample.epoch),
                domain=str(metadata.get("domain", "unknown")),
                difficulty=str(metadata.get("difficulty", "unknown")),
                question=_question_text(sample.input),
                target=_target_text(sample.target),
                answer=score.answer or "unparseable",
                rationale=str(metadata.get("rationale", "No rationale recorded.")),
                correct=score.value == "C",
            )
        )

    return results


def grouped_accuracy(
    results: Iterable[CalibrationResult], attribute: str
) -> dict[str, tuple[int, int]]:
    """Return correct and total counts grouped by a result attribute."""
    counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])

    for result in results:
        group = str(getattr(result, attribute))
        counts[group][1] += 1
        counts[group][0] += int(result.correct)

    return {group: (values[0], values[1]) for group, values in sorted(counts.items())}


def _question_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return " ".join(str(message.content) for message in value)


def _target_text(value: str | list[str]) -> str:
    return value if isinstance(value, str) else ", ".join(value)
