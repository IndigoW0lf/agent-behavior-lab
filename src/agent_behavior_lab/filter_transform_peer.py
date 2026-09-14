"""Dataset construction for the targeted peer-influence pilot."""

from pathlib import Path
from typing import Any

from inspect_ai.dataset import Sample, json_dataset

from agent_behavior_lab.conditions import Condition, render_question
from agent_behavior_lab.filter_transform_items import target_for_mechanism

DATA_PATH = (
    Path(__file__).parent.parent.parent
    / "data"
    / "filter_transform_counterbalanced.jsonl"
)
INFLUENCE_MECHANISM = "filtered_after_transform"


def _answer_text(label: str, choices: list[str]) -> str:
    return f"{label}. {choices[ord(label) - ord('A')]}"


def dataset_for(condition: Condition):
    """Build counterbalanced samples for one peer-information condition."""

    def record_to_sample(record: dict[str, Any]) -> Sample:
        choices = [str(value) for value in record["choices"]]
        target = str(record["target"])
        influence_target = target_for_mechanism(record, INFLUENCE_MECHANISM)

        return Sample(
            id=f"{record['id']}::{condition.value}",
            input=render_question(
                str(record["question"]),
                condition,
                correct_answer=_answer_text(target, choices),
                incorrect_answer=_answer_text(influence_target, choices),
            ),
            choices=choices,
            target=target,
            metadata={
                "item_id": record["id"],
                "base_id": record["base_id"],
                "form": record["form"],
                "condition": condition.value,
                "domain": record["domain"],
                "difficulty": record["difficulty"],
                "choice_mechanisms": record["choice_mechanisms"],
                "influence_mechanism": INFLUENCE_MECHANISM,
                "influence_target": influence_target,
                "rationale": record["rationale"],
            },
        )

    return json_dataset(str(DATA_PATH), sample_fields=record_to_sample)
