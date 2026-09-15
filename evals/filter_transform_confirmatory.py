"""Frozen confirmatory social-framing evaluation on held-out unique items."""

from inspect_ai import Task, task
from inspect_ai.scorer import choice
from inspect_ai.solver import multiple_choice

from agent_behavior_lab.conditions import Condition
from agent_behavior_lab.filter_transform_peer import confirmatory_dataset_for


def _task_for(condition: Condition) -> Task:
    return Task(
        dataset=confirmatory_dataset_for(condition),
        solver=multiple_choice(cot=False),
        scorer=choice(),
    )


@task
def confirmatory_baseline() -> Task:
    """Held-out performance without an added answer cue."""
    return _task_for(Condition.BASELINE)


@task
def confirmatory_repeated_incorrect() -> Task:
    """Held-out performance after a non-social repeated wrong cue."""
    return _task_for(Condition.REPEATED_INCORRECT)


@task
def confirmatory_unanimous_incorrect_peers() -> Task:
    """Held-out performance after three named peers endorse the wrong cue."""
    return _task_for(Condition.UNANIMOUS_INCORRECT)
