from agent_behavior_lab.conditions import Condition
from agent_behavior_lab.filter_transform_peer import dataset_for


def test_peer_pilot_uses_all_counterbalanced_trials() -> None:
    assert len(dataset_for(Condition.BASELINE)) == 96
    assert len(dataset_for(Condition.UNANIMOUS_INCORRECT)) == 96


def test_unanimous_peers_endorse_the_targeted_semantic_error() -> None:
    for sample in dataset_for(Condition.UNANIMOUS_INCORRECT):
        influence_target = sample.metadata["influence_target"]
        choices = sample.choices
        assert choices is not None
        answer_text = f"{influence_target}. {choices[ord(influence_target) - ord('A')]}"

        assert sample.input.count(answer_text) == 3
        assert sample.metadata["choice_mechanisms"][influence_target] == (
            "filtered_after_transform"
        )
        assert influence_target != sample.target


def test_baseline_has_no_peer_responses() -> None:
    for sample in dataset_for(Condition.BASELINE):
        assert "Responses from other AI agents" not in sample.input
