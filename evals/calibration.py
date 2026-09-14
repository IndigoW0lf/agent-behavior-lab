"""Baseline-only task for selecting an informative study difficulty range."""

from pathlib import Path
from typing import Any

from inspect_ai import Task, task
from inspect_ai.dataset import Sample, json_dataset
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice

DATA_PATH = Path(__file__).parent.parent / "data" / "calibration_questions.jsonl"


def _record_to_sample(record: dict[str, Any]) -> Sample:
    return Sample(
        id=str(record["id"]),
        input=str(record["question"]),
        choices=[str(value) for value in record["choices"]],
        target=str(record["target"]),
        metadata={
            "domain": record["domain"],
            "difficulty": record["difficulty"],
            "rationale": record["rationale"],
            "generator_seed": record["generator_seed"],
        },
    )


@task
def difficulty_calibration() -> Task:
    """Measure baseline accuracy before any social-information manipulation."""
    return Task(
        dataset=json_dataset(str(DATA_PATH), sample_fields=_record_to_sample),
        solver=multiple_choice(cot=False),
        scorer=choice(),
    )
