"""Inspect tasks for Study 001: Peer Influence."""

from pathlib import Path
from typing import Any

from inspect_ai import Task, task
from inspect_ai.dataset import Sample, json_dataset
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice

from agent_behavior_lab.conditions import Condition, render_question

DATA_PATH = Path(__file__).parent.parent / "data" / "questions.jsonl"


def _answer_text(label: str, choices: list[str]) -> str:
    index = ord(label) - ord("A")
    if index < 0 or index >= len(choices):
        raise ValueError(f"Answer label {label!r} is outside the available choices")
    return f"{label}. {choices[index]}"


def _dataset_for(condition: Condition):
    def record_to_sample(record: dict[str, Any]) -> Sample:
        choices = [str(value) for value in record["choices"]]
        target = str(record["target"])
        incorrect_target = str(record["incorrect_target"])

        return Sample(
            id=f"{record['id']}::{condition.value}",
            input=render_question(
                str(record["question"]),
                condition,
                correct_answer=_answer_text(target, choices),
                incorrect_answer=_answer_text(incorrect_target, choices),
            ),
            choices=choices,
            target=target,
            metadata={
                "item_id": record["id"],
                "condition": condition.value,
                "domain": record["domain"],
                "incorrect_target": incorrect_target,
            },
        )

    return json_dataset(str(DATA_PATH), sample_fields=record_to_sample)


def _peer_influence_task(condition: Condition) -> Task:
    return Task(
        dataset=_dataset_for(condition),
        solver=multiple_choice(cot=False),
        scorer=choice(),
    )


@task
def peer_influence_baseline() -> Task:
    """Measure performance without peer testimony."""
    return _peer_influence_task(Condition.BASELINE)


@task
def peer_influence_unanimous_incorrect() -> Task:
    """Measure performance after three peers give the same wrong answer."""
    return _peer_influence_task(Condition.UNANIMOUS_INCORRECT)


@task
def peer_influence_divided_group() -> Task:
    """Measure performance when a two-agent wrong majority includes one dissenter."""
    return _peer_influence_task(Condition.DIVIDED_GROUP)


@task
def peer_influence_claimed_expert() -> Task:
    """Measure performance after a purported specialist gives a wrong answer."""
    return _peer_influence_task(Condition.CLAIMED_EXPERT)
