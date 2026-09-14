"""Baseline calibration for the targeted filter/transform item family."""

from pathlib import Path
from typing import Any

from inspect_ai import Task, task
from inspect_ai.dataset import Sample, json_dataset
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice

DATA_PATH = (
    Path(__file__).parent.parent / "data" / "filter_transform_calibration.jsonl"
)
COUNTERBALANCED_PATH = (
    Path(__file__).parent.parent / "data" / "filter_transform_counterbalanced.jsonl"
)


def _record_to_sample(record: dict[str, Any]) -> Sample:
    return Sample(
        id=str(record["id"]),
        input=str(record["question"]),
        choices=[str(value) for value in record["choices"]],
        target=str(record["target"]),
        metadata={
            "domain": record["domain"],
            "difficulty": record["difficulty"],
            "split": record["split"],
            "base_id": record.get("base_id", record["id"]),
            "form": record.get("form", 1),
            "choice_mechanisms": record["choice_mechanisms"],
            "rationale": record["rationale"],
            "generator_seed": record["generator_seed"],
        },
    )


@task
def filter_transform_calibration() -> Task:
    """Measure baseline error rates for parallel filter/transform questions."""
    return Task(
        dataset=json_dataset(str(DATA_PATH), sample_fields=_record_to_sample),
        solver=multiple_choice(cot=False),
        scorer=choice(),
    )


@task
def filter_transform_position_check() -> Task:
    """Separate answer-content errors from multiple-choice position bias."""
    return Task(
        dataset=json_dataset(str(COUNTERBALANCED_PATH), sample_fields=_record_to_sample),
        solver=multiple_choice(cot=False),
        scorer=choice(),
    )
