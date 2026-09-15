"""Compare baseline, repeated-cue, and peer-attributed Inspect logs."""

import argparse
from pathlib import Path

from inspect_ai.log import read_eval_log_sample_summaries

from agent_behavior_lab.peer_comparison import (
    confirmatory_success,
    exact_mcnemar_p_value,
    index_unique,
    paired_counts,
    parse_trials,
    require_condition,
)


def _percent(numerator: int, denominator: int) -> float:
    return 100 * numerator / denominator if denominator else 0.0


def _metrics(trials):
    total = len(trials)
    correct = sum(trial.correct for trial in trials.values())
    adopted = sum(trial.adopted_influence for trial in trials.values())
    return total, correct, adopted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline_log", type=Path)
    parser.add_argument("repetition_log", type=Path)
    parser.add_argument("peer_log", type=Path)
    parser.add_argument(
        "--confirmatory",
        action="store_true",
        help="Apply the frozen confirmatory decision rule.",
    )
    args = parser.parse_args()

    parsed = {
        "baseline": parse_trials(read_eval_log_sample_summaries(args.baseline_log)),
        "repetition": parse_trials(read_eval_log_sample_summaries(args.repetition_log)),
        "peers": parse_trials(read_eval_log_sample_summaries(args.peer_log)),
    }
    require_condition(parsed["baseline"].trials, "baseline")
    require_condition(parsed["repetition"].trials, "repeated_incorrect")
    require_condition(parsed["peers"].trials, "unanimous_incorrect")
    indexed = {name: index_unique(value.trials) for name, value in parsed.items()}

    # Validate that all three conditions contain the same paired trials.
    paired_counts(indexed["baseline"], indexed["repetition"])
    primary_counts = paired_counts(indexed["repetition"], indexed["peers"])

    metrics = {name: _metrics(trials) for name, trials in indexed.items()}
    repetition_total, repetition_correct, repetition_adopted = metrics["repetition"]
    peer_total, peer_correct, peer_adopted = metrics["peers"]
    if repetition_total != peer_total:
        raise ValueError("Repetition and peer conditions have different sample counts")

    accuracy_change = _percent(peer_correct, peer_total) - _percent(
        repetition_correct, repetition_total
    )
    adoption_change = _percent(peer_adopted, peer_total) - _percent(
        repetition_adopted, repetition_total
    )

    heading = (
        "Confirmatory social-framing comparison"
        if args.confirmatory
        else "Social-framing control comparison"
    )
    print(heading)
    for name in ("baseline", "repetition", "peers"):
        total, correct, adopted = metrics[name]
        print(
            f"  {name} accuracy: {correct}/{total} "
            f"({_percent(correct, total):.1f}%)"
        )
        print(
            f"  {name} targeted-distractor selection: {adopted}/{total} "
            f"({_percent(adopted, total):.1f}%)"
        )

    print("\nPrimary contrast: peers minus repetition")
    print(f"  accuracy change: {accuracy_change:+.1f} percentage points")
    print(f"  targeted-adoption change: {adoption_change:+.1f} percentage points")
    print("\nPaired correctness table: repetition → peers")
    print(f"  correct in both: {primary_counts.both_correct}")
    print(
        "  repetition correct → peers wrong: "
        f"{primary_counts.baseline_correct_influenced_wrong}"
    )
    print(
        "  repetition wrong → peers correct: "
        f"{primary_counts.baseline_wrong_influenced_correct}"
    )
    print(f"  wrong in both: {primary_counts.both_wrong}")
    p_value = exact_mcnemar_p_value(primary_counts)
    print(f"  exact McNemar p-value: {p_value:.6g}")
    print("\nRegistered exclusions")
    for name in ("baseline", "repetition", "peers"):
        print(f"  {name}: {parsed[name].exclusions}")
    if args.confirmatory:
        decision = (
            "SUPPORTED"
            if confirmatory_success(accuracy_change, p_value)
            else "NOT SUPPORTED"
        )
        print(f"\nFrozen primary hypothesis: {decision}")
    else:
        print("\nInterpretation: exploratory control, not a confirmatory effect estimate.")


if __name__ == "__main__":
    main()
