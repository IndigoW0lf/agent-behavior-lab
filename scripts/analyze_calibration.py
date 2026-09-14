"""Print a diagnostic summary from an Inspect calibration log."""

import argparse
from pathlib import Path

from inspect_ai.log import read_eval_log_sample_summaries

from agent_behavior_lab.calibration_analysis import (
    CalibrationResult,
    grouped_accuracy,
    results_from_samples,
)


def _percentage(correct: int, total: int) -> str:
    return f"{correct / total:.1%}" if total else "n/a"


def _print_group(title: str, results: list[CalibrationResult], attribute: str) -> None:
    print(f"\n{title}")
    for group, (correct, total) in grouped_accuracy(results, attribute).items():
        print(f"  {group}: {correct}/{total} ({_percentage(correct, total)})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log_file", type=Path, help="Path to an Inspect .eval log")
    args = parser.parse_args()

    samples = read_eval_log_sample_summaries(args.log_file)
    results = results_from_samples(samples)
    correct = sum(result.correct for result in results)

    print("Calibration summary")
    print(f"  overall: {correct}/{len(results)} ({_percentage(correct, len(results))})")
    _print_group("By domain", results, "domain")
    _print_group("By difficulty", results, "difficulty")

    by_item = grouped_accuracy(results, "sample_id")
    nonperfect_items = {
        sample_id: counts
        for sample_id, counts in by_item.items()
        if counts[0] < counts[1]
    }
    print(f"\nNon-perfect items ({len(nonperfect_items)})")
    for sample_id, (item_correct, item_total) in nonperfect_items.items():
        print(
            f"  {sample_id}: {item_correct}/{item_total} "
            f"({_percentage(item_correct, item_total)})"
        )

    misses = [result for result in results if not result.correct]
    print(f"\nIncorrect attempts ({len(misses)})")
    for result in misses:
        print(
            f"\n  {result.sample_id}, epoch {result.epoch} "
            f"[{result.domain}; {result.difficulty}]"
        )
        print(f"  Question: {result.question}")
        print(f"  Model answer: {result.answer}; target: {result.target}")
        print(f"  Rationale: {result.rationale}")


if __name__ == "__main__":
    main()
