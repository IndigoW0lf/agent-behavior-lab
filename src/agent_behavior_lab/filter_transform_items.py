"""Generate parallel code-tracing items for filter/transform confusion."""

from dataclasses import dataclass
from itertools import product
from random import Random

SEED = 20_260_914
ITEMS_PER_SPLIT = 24


@dataclass(frozen=True)
class Transform:
    code: str

    def apply(self, value: int) -> int:
        match self.code:
            case "x - 1":
                return value - 1
            case "x + 2":
                return value + 2
            case "x * 2":
                return value * 2
            case "x // 2":
                return value // 2
            case "10 - x":
                return 10 - value
            case "x * x":
                return value * value
            case _:
                raise ValueError(f"Unknown transform: {self.code}")


@dataclass(frozen=True)
class Predicate:
    code: str

    def test(self, value: int) -> bool:
        match self.code:
            case "x % 2 == 0":
                return value % 2 == 0
            case "x % 2 != 0":
                return value % 2 != 0
            case "x % 3 == 1":
                return value % 3 == 1
            case "x > 5":
                return value > 5
            case "x < 6":
                return value < 6
            case "(x + 1) % 3 == 0":
                return (value + 1) % 3 == 0
            case _:
                raise ValueError(f"Unknown predicate: {self.code}")


TRANSFORMS = tuple(
    Transform(code)
    for code in ("x - 1", "x + 2", "x * 2", "x // 2", "10 - x", "x * x")
)
PREDICATES = tuple(
    Predicate(code)
    for code in (
        "x % 2 == 0",
        "x % 2 != 0",
        "x % 3 == 1",
        "x > 5",
        "x < 6",
        "(x + 1) % 3 == 0",
    )
)
VALUE_SETS = (
    (1, 2, 3, 4, 5, 6),
    (2, 3, 5, 7, 8, 10),
    (0, 1, 4, 6, 9, 11),
    (3, 4, 7, 8, 10, 13),
    (1, 5, 6, 8, 9, 12),
    (2, 4, 5, 9, 11, 14),
    (0, 3, 4, 7, 12, 15),
    (1, 2, 6, 7, 10, 13),
)


def _candidate_record(
    values: tuple[int, ...], transform: Transform, predicate: Predicate
) -> dict[str, object] | None:
    correct = [transform.apply(value) for value in values if predicate.test(value)]
    complement = [
        transform.apply(value) for value in values if not predicate.test(value)
    ]
    transformed_filter = [
        transform.apply(value)
        for value in values
        if predicate.test(transform.apply(value))
    ]
    omitted_transform = [value for value in values if predicate.test(value)]
    mechanisms = {
        repr(correct): "correct",
        repr(complement): "reversed_filter",
        repr(transformed_filter): "filtered_after_transform",
        repr(omitted_transform): "omitted_transform",
    }
    if len(mechanisms) != 4 or not correct:
        return None

    expression = (
        f"[{transform.code} for x in {list(values)!r} if {predicate.code}]"
    )
    return {
        "expression": expression,
        "question": f"What does this Python expression produce? {expression}",
        "correct": repr(correct),
        "mechanisms": mechanisms,
        "rationale": (
            "The if-clause filters each original x first; the expression before "
            "'for' transforms only the retained values."
        ),
    }


def build_filter_transform_records() -> dict[str, list[dict[str, object]]]:
    """Create deterministic calibration and preregistered confirmatory splits."""
    rng = Random(SEED)
    candidates = [
        candidate
        for values, transform, predicate in product(
            VALUE_SETS, TRANSFORMS, PREDICATES
        )
        if (candidate := _candidate_record(values, transform, predicate)) is not None
    ]
    rng.shuffle(candidates)
    selected = candidates[: ITEMS_PER_SPLIT * 2]
    splits = {
        "calibration": selected[:ITEMS_PER_SPLIT],
        "confirmatory": selected[ITEMS_PER_SPLIT:],
    }

    for split, records in splits.items():
        for index, record in enumerate(records, start=1):
            mechanisms = record.pop("mechanisms")
            assert isinstance(mechanisms, dict)
            choices = list(mechanisms)
            rng.shuffle(choices)
            mechanisms_by_letter = {
                chr(ord("A") + position): str(mechanisms[choice])
                for position, choice in enumerate(choices)
            }
            target = next(
                letter
                for letter, mechanism in mechanisms_by_letter.items()
                if mechanism == "correct"
            )
            record.update(
                {
                    "id": f"ft-{split[:3]}-{index:03d}",
                    "split": split,
                    "domain": "python_filter_transform",
                    "difficulty": "targeted",
                    "choices": choices,
                    "target": target,
                    "incorrect_target": next(
                        letter
                        for letter, mechanism in mechanisms_by_letter.items()
                        if mechanism == "reversed_filter"
                    ),
                    "choice_mechanisms": mechanisms_by_letter,
                    "generator_seed": SEED,
                }
            )
            record.pop("correct")

    return splits
