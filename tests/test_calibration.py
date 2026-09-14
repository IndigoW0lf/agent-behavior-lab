import json
from pathlib import Path

from agent_behavior_lab.calibration_items import SEED, build_calibration_records

DATA_PATH = Path(__file__).parent.parent / "data" / "calibration_questions.jsonl"


def test_calibration_pool_is_balanced_and_unique() -> None:
    records = build_calibration_records()
    ids = [record["id"] for record in records]
    domain_counts: dict[str, int] = {}

    for record in records:
        domain = str(record["domain"])
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

    assert len(records) == 32
    assert len(ids) == len(set(ids))
    assert set(domain_counts.values()) == {8}


def test_calibration_answers_and_metadata_are_valid() -> None:
    for record in build_calibration_records():
        assert len(record["choices"]) == 4
        assert record["target"] in {"A", "B", "C", "D"}
        assert record["incorrect_target"] in {"A", "B", "C", "D"}
        assert record["incorrect_target"] != record["target"]
        assert record["difficulty"] in {"medium", "hard"}
        assert record["generator_seed"] == SEED
        assert record["rationale"]


def test_committed_dataset_matches_generator() -> None:
    committed = [
        json.loads(line)
        for line in DATA_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    assert committed == build_calibration_records()
