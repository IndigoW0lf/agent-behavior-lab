import json
from pathlib import Path

from agent_behavior_lab.filter_transform_items import (
    ITEMS_PER_SPLIT,
    build_filter_transform_records,
)

DATA_DIR = Path(__file__).parent.parent / "data"


def test_splits_are_unique_balanced_and_disjoint() -> None:
    splits = build_filter_transform_records()

    assert set(splits) == {"calibration", "confirmatory"}
    assert all(len(records) == ITEMS_PER_SPLIT for records in splits.values())
    calibration_expressions = {record["expression"] for record in splits["calibration"]}
    confirmatory_expressions = {record["expression"] for record in splits["confirmatory"]}
    assert calibration_expressions.isdisjoint(confirmatory_expressions)


def test_targets_match_python_oracle_and_choices_are_distinct() -> None:
    for records in build_filter_transform_records().values():
        for record in records:
            choices = record["choices"]
            target_index = ord(str(record["target"])) - ord("A")
            oracle_result = eval(str(record["expression"]), {"__builtins__": {}})

            assert len(choices) == len(set(choices)) == 4
            assert choices[target_index] == repr(oracle_result)
            assert record["choice_mechanisms"][record["target"]] == "correct"
            assert (
                record["choice_mechanisms"][record["incorrect_target"]]
                == "reversed_filter"
            )


def test_committed_datasets_match_generator() -> None:
    for split, generated in build_filter_transform_records().items():
        path = DATA_DIR / f"filter_transform_{split}.jsonl"
        committed = [json.loads(line) for line in path.read_text().splitlines()]
        assert committed == generated
