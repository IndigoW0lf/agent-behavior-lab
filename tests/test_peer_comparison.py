from types import SimpleNamespace

import pytest

from agent_behavior_lab.peer_comparison import (
    PairedCounts,
    exact_mcnemar_p_value,
    index_unique,
    paired_counts,
    parse_trials,
    require_condition,
)


def _sample(
    trial_id: str,
    condition: str,
    *,
    correct: bool,
    answer: str,
    reason: str | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        error=None,
        scores={
            "choice": SimpleNamespace(
                value="C" if correct else "I", answer=answer, reason=reason
            )
        },
        metadata={
            "item_id": trial_id,
            "condition": condition,
            "influence_target": "D",
            "choice_mechanisms": {"A": "correct", "D": "filtered_after_transform"},
        },
    )


def test_parse_trials_tracks_influence_adoption_and_exclusions() -> None:
    parsed = parse_trials(
        [
            _sample("one", "baseline", correct=True, answer="A"),
            _sample(
                "two",
                "baseline",
                correct=False,
                answer="D",
                reason="invalid_response_format",
            ),
        ]
    )

    assert len(parsed.trials) == 1
    assert parsed.exclusions == 1
    assert parsed.trials[0].adopted_influence is False


def test_paired_counts_classify_all_four_outcomes() -> None:
    baseline = index_unique(
        parse_trials(
            [
                _sample("one", "baseline", correct=True, answer="A"),
                _sample("two", "baseline", correct=True, answer="A"),
                _sample("three", "baseline", correct=False, answer="D"),
                _sample("four", "baseline", correct=False, answer="D"),
            ]
        ).trials
    )
    influenced = index_unique(
        parse_trials(
            [
                _sample("one", "influenced", correct=True, answer="A"),
                _sample("two", "influenced", correct=False, answer="D"),
                _sample("three", "influenced", correct=True, answer="A"),
                _sample("four", "influenced", correct=False, answer="D"),
            ]
        ).trials
    )

    assert paired_counts(baseline, influenced) == PairedCounts(1, 1, 1, 1)


def test_exact_mcnemar_uses_two_sided_binomial_test() -> None:
    assert exact_mcnemar_p_value(PairedCounts(0, 3, 0, 0)) == pytest.approx(0.25)
    assert exact_mcnemar_p_value(PairedCounts(4, 0, 0, 2)) == 1.0


def test_pairing_rejects_mismatched_trial_ids() -> None:
    baseline = index_unique(
        parse_trials([_sample("one", "baseline", correct=True, answer="A")]).trials
    )
    influenced = index_unique(
        parse_trials([_sample("two", "influenced", correct=True, answer="A")]).trials
    )

    with pytest.raises(ValueError, match="do not match"):
        paired_counts(baseline, influenced)


def test_condition_validation_rejects_log_in_wrong_argument_position() -> None:
    trials = parse_trials(
        [_sample("one", "unanimous_incorrect", correct=False, answer="D")]
    ).trials

    with pytest.raises(ValueError, match="Expected condition 'repeated_incorrect'"):
        require_condition(trials, "repeated_incorrect")
