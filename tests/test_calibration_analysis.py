from types import SimpleNamespace

import pytest

from agent_behavior_lab.calibration_analysis import grouped_accuracy, results_from_samples


def _sample(
    sample_id: str, domain: str, difficulty: str, value: str, answer: str
) -> SimpleNamespace:
    return SimpleNamespace(
        id=sample_id,
        epoch=1,
        input="Question text",
        target="B",
        metadata={
            "domain": domain,
            "difficulty": difficulty,
            "rationale": "Because B is correct.",
            "choice_mechanisms": {"A": "reversed_filter", "B": "correct"},
        },
        scores={"choice": SimpleNamespace(value=value, answer=answer)},
    )


def test_results_extract_choice_scores_and_metadata() -> None:
    results = results_from_samples([_sample("one", "logic", "hard", "C", "B")])

    assert len(results) == 1
    assert results[0].sample_id == "one"
    assert results[0].epoch == 1
    assert results[0].correct is True
    assert results[0].answer == "B"
    assert results[0].selected_mechanism == "correct"
    assert results[0].rationale == "Because B is correct."


def test_grouped_accuracy_counts_correct_and_total() -> None:
    results = results_from_samples(
        [
            _sample("one", "logic", "hard", "C", "B"),
            _sample("two", "logic", "hard", "I", "A"),
            _sample("three", "python", "medium", "C", "B"),
        ]
    )

    assert grouped_accuracy(results, "domain") == {
        "logic": (1, 2),
        "python": (1, 1),
    }


def test_missing_choice_score_is_rejected() -> None:
    sample = SimpleNamespace(id="one", scores=None)

    with pytest.raises(ValueError, match="no 'choice' score"):
        results_from_samples([sample])
