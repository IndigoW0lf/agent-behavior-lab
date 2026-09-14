import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "questions.jsonl"


def _records() -> list[dict]:
    return [
        json.loads(line)
        for line in DATA_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_dataset_has_unique_ids() -> None:
    records = _records()
    ids = [record["id"] for record in records]

    assert len(records) >= 10
    assert len(ids) == len(set(ids))


def test_answer_labels_are_valid_and_manipulation_is_incorrect() -> None:
    for record in _records():
        valid_labels = {
            chr(ord("A") + index) for index, _ in enumerate(record["choices"])
        }

        assert len(record["choices"]) == 4
        assert record["target"] in valid_labels
        assert record["incorrect_target"] in valid_labels
        assert record["incorrect_target"] != record["target"]


def test_required_fields_are_present() -> None:
    required = {
        "id",
        "domain",
        "question",
        "choices",
        "target",
        "incorrect_target",
    }

    for record in _records():
        assert required <= record.keys()
