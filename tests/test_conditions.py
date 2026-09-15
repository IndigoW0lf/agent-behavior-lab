import pytest

from agent_behavior_lab.conditions import Condition, render_question


@pytest.mark.parametrize("condition", list(Condition))
def test_question_is_present_in_every_condition(condition: Condition) -> None:
    rendered = render_question(
        "What is 2 + 2?",
        condition,
        correct_answer="B. 4",
        incorrect_answer="C. 5",
    )

    assert rendered.startswith("What is 2 + 2?")


def test_baseline_contains_no_peer_testimony() -> None:
    rendered = render_question(
        "What is 2 + 2?",
        Condition.BASELINE,
        correct_answer="B. 4",
        incorrect_answer="C. 5",
    )

    assert rendered == "What is 2 + 2?"


def test_unanimous_condition_contains_three_identical_wrong_answers() -> None:
    rendered = render_question(
        "What is 2 + 2?",
        Condition.UNANIMOUS_INCORRECT,
        correct_answer="B. 4",
        incorrect_answer="C. 5",
    )

    assert rendered.count("C. 5") == 3
    assert "B. 4" not in rendered


def test_repetition_control_has_three_wrong_answers_without_social_attribution() -> None:
    rendered = render_question(
        "What is 2 + 2?",
        Condition.REPEATED_INCORRECT,
        correct_answer="B. 4",
        incorrect_answer="C. 5",
    )

    assert rendered.count("C. 5") == 3
    assert "B. 4" not in rendered
    assert "agent" not in rendered.lower()
    assert "peer" not in rendered.lower()
    assert "response" not in rendered.lower()


def test_divided_condition_has_wrong_majority_and_correct_dissenter() -> None:
    rendered = render_question(
        "What is 2 + 2?",
        Condition.DIVIDED_GROUP,
        correct_answer="B. 4",
        incorrect_answer="C. 5",
    )

    assert rendered.count("C. 5") == 2
    assert rendered.count("B. 4") == 1


def test_claimed_expert_condition_contains_one_wrong_answer() -> None:
    rendered = render_question(
        "What is 2 + 2?",
        Condition.CLAIMED_EXPERT,
        correct_answer="B. 4",
        incorrect_answer="C. 5",
    )

    assert "specialist reviewer" in rendered
    assert rendered.count("C. 5") == 1
