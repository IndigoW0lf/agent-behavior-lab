"""Compare paired baseline and influenced Inspect logs."""

import argparse
from pathlib import Path

from inspect_ai.log import read_eval_log_sample_summaries

from agent_behavior_lab.peer_comparison import (
    exact_mcnemar_p_value,
    index_unique,
    paired_counts,
    parse_trials,
)


def _percent(numerator: int, denominator: int) -> float:
    return 100 * numerator / denominator if denominator else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline_log", type=Path)
    parser.add_argument("influenced_log", type=Path)
    args = parser.parse_args()

    baseline_parsed = parse_trials(read_eval_log_sample_summaries(args.baseline_log))
    influenced_parsed = parse_trials(read_eval_log_sample_summaries(args.influenced_log))
    baseline = index_unique(baseline_parsed.trials)
    influenced = index_unique(influenced_parsed.trials)
    counts = paired_counts(baseline, influenced)

    baseline_correct = sum(trial.correct for trial in baseline.values())
    influenced_correct = sum(trial.correct for trial in influenced.values())
    baseline_adopted = sum(trial.adopted_influence for trial in baseline.values())
    influenced_adopted = sum(trial.adopted_influence for trial in influenced.values())
    total = len(baseline)
    accuracy_change = _percent(influenced_correct, total) - _percent(
        baseline_correct, total
    )
    adoption_change = _percent(influenced_adopted, total) - _percent(
        baseline_adopted, total
    )

    print("Targeted peer-influence comparison")
    print(
        f"  baseline accuracy: {baseline_correct}/{total} "
        f"({_percent(baseline_correct, total):.1f}%)"
    )
    print(
        f"  influenced accuracy: {influenced_correct}/{total} "
        f"({_percent(influenced_correct, total):.1f}%)"
    )
    print(f"  accuracy change: {accuracy_change:+.1f} percentage points")
    print(
        f"  baseline targeted-distractor selection: {baseline_adopted}/{total} "
        f"({_percent(baseline_adopted, total):.1f}%)"
    )
    print(
        f"  influenced targeted-distractor selection: {influenced_adopted}/{total} "
        f"({_percent(influenced_adopted, total):.1f}%)"
    )
    print(f"  targeted-adoption change: {adoption_change:+.1f} percentage points")
    print("\nPaired correctness table")
    print(f"  correct in both: {counts.both_correct}")
    print(
        "  baseline correct → influenced wrong: "
        f"{counts.baseline_correct_influenced_wrong}"
    )
    print(
        "  baseline wrong → influenced correct: "
        f"{counts.baseline_wrong_influenced_correct}"
    )
    print(f"  wrong in both: {counts.both_wrong}")
    print(f"  exact McNemar p-value: {exact_mcnemar_p_value(counts):.6g}")
    print("\nRegistered exclusions")
    print(f"  baseline: {baseline_parsed.exclusions}")
    print(f"  influenced: {influenced_parsed.exclusions}")
    print("\nInterpretation: exploratory pilot, not a confirmatory effect estimate.")


if __name__ == "__main__":
    main()
