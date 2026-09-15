import json
from pathlib import Path

from agent_behavior_lab.filter_transform_items import (
    CALIBRATION_ITEMS,
    CONFIRMATORY_ITEMS,
    build_counterbalanced_records,
    build_filter_transform_records,
    target_for_mechanism,
)

DATA_DIR = Path(__file__).parent.parent / "data"


def test_splits_are_unique_balanced_and_disjoint() -> None:
    splits = build_filter_transform_records()

    assert set(splits) == {"calibration", "confirmatory"}
    assert len(splits["calibration"]) == CALIBRATION_ITEMS
    assert len(splits["confirmatory"]) == CONFIRMATORY_ITEMS
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

    counterbalanced_path = DATA_DIR / "filter_transform_counterbalanced.jsonl"
    committed = [
        json.loads(line) for line in counterbalanced_path.read_text().splitlines()
    ]
    assert committed == build_counterbalanced_records()


def test_counterbalancing_moves_every_mechanism_through_every_letter() -> None:
    records = build_counterbalanced_records()

    assert len(records) == CALIBRATION_ITEMS * 4
    grouped: dict[str, list[dict[str, object]]] = {}
    for record in records:
        grouped.setdefault(str(record["base_id"]), []).append(record)

    for forms in grouped.values():
        assert len(forms) == 4
        for mechanism in {
            "correct",
            "reversed_filter",
            "filtered_after_transform",
            "omitted_transform",
        }:
            occupied_letters = {
                letter
                for form in forms
                for letter, value in form["choice_mechanisms"].items()
                if value == mechanism
            }
            assert occupied_letters == {"A", "B", "C", "D"}


def test_confirmatory_items_exactly_balance_semantic_answer_orders() -> None:
    records = build_filter_transform_records()["confirmatory"]
    order_counts: dict[tuple[str, ...], int] = {}
    for record in records:
        order = tuple(record["choice_mechanisms"][letter] for letter in "ABCD")
        order_counts[order] = order_counts.get(order, 0) + 1

    assert len(order_counts) == 24
    assert set(order_counts.values()) == {2}


def test_target_for_mechanism_tracks_rotated_choices() -> None:
    for record in build_counterbalanced_records():
        influence_target = target_for_mechanism(record, "filtered_after_transform")
        assert record["choice_mechanisms"][influence_target] == (
            "filtered_after_transform"
        )
