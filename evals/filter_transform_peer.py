"""Exploratory peer-influence pilot on counterbalanced code-tracing items."""

from inspect_ai import Task, task
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice

from agent_behavior_lab.conditions import Condition
from agent_behavior_lab.filter_transform_peer import dataset_for


def _task_for(condition: Condition) -> Task:
    return Task(
        dataset=dataset_for(condition),
        solver=multiple_choice(cot=False),
        scorer=choice(),
    )


@task
def filter_transform_peer_baseline() -> Task:
    """Fresh no-peer comparison for the targeted pilot."""
    return _task_for(Condition.BASELINE)


@task
def filter_transform_repeated_incorrect() -> Task:
    """Repeat the targeted wrong answer without attributing it to peers."""
    return _task_for(Condition.REPEATED_INCORRECT)


@task
def filter_transform_peer_unanimous_incorrect() -> Task:
    """Three peers endorse the filtered-after-transform distractor."""
    return _task_for(Condition.UNANIMOUS_INCORRECT)
