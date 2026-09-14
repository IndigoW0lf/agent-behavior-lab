"""Deterministic item generation for baseline difficulty calibration."""

from dataclasses import dataclass
from random import Random

SEED = 20_260_914


@dataclass(frozen=True)
class ItemSpec:
    id: str
    domain: str
    difficulty: str
    question: str
    correct: str
    distractors: tuple[str, str, str]
    rationale: str


SPECS = (
    ItemSpec(
        "arith-001",
        "arithmetic",
        "medium",
        "A warehouse receives 18 crates with 24 items each, then ships 37 items. "
        "How many items remain?",
        "395",
        ("385", "405", "432"),
        "18 × 24 − 37 = 395.",
    ),
    ItemSpec(
        "arith-002",
        "arithmetic",
        "medium",
        "An item costs $240, is discounted by 15%, and then has a $12 shipping "
        "charge. What is the final price?",
        "$216",
        ("$204", "$222", "$228"),
        "$240 × 0.85 + $12 = $216.",
    ),
    ItemSpec(
        "arith-003",
        "arithmetic",
        "medium",
        "Red and blue tiles are in a 3:5 ratio. If there are 64 tiles total, how many are red?",
        "24",
        ("21", "32", "40"),
        "Three of eight equal parts are red: 64 × 3/8 = 24.",
    ),
    ItemSpec(
        "arith-004",
        "arithmetic",
        "medium",
        "Five test scores have an average of 82. The first four are 78, 85, 80, "
        "and 76. What is the fifth score?",
        "91",
        ("81", "87", "93"),
        "5 × 82 − (78 + 85 + 80 + 76) = 91.",
    ),
    ItemSpec(
        "arith-005",
        "arithmetic",
        "medium",
        "A tank is three-quarters full at 160 liters. After 25 liters are used, "
        "how many liters remain?",
        "95",
        ("85", "105", "120"),
        "160 × 3/4 − 25 = 95.",
    ),
    ItemSpec(
        "arith-006",
        "arithmetic",
        "hard",
        "Six consecutive integers have a sum of 165. What is the largest integer?",
        "30",
        ("27", "28", "29"),
        "The integers are 25 through 30.",
    ),
    ItemSpec(
        "arith-007",
        "arithmetic",
        "medium",
        "A population of 500 increases by 20% and then decreases by 20%. What is "
        "the final population?",
        "480",
        ("460", "500", "520"),
        "500 × 1.2 × 0.8 = 480.",
    ),
    ItemSpec(
        "arith-008",
        "arithmetic",
        "medium",
        "A recipe uses 2.5 cups of flour for 20 cookies. At the same rate, how many "
        "cups are needed for 32 cookies?",
        "4 cups",
        ("3.2 cups", "4.5 cups", "5 cups"),
        "2.5 × 32/20 = 4.",
    ),
    ItemSpec(
        "code-001",
        "python",
        "medium",
        "What does this Python expression produce? sum(i * i for i in range(1, 7) if i % 2 == 0)",
        "56",
        ("20", "36", "91"),
        "The even squares are 4, 16, and 36; their sum is 56.",
    ),
    ItemSpec(
        "code-002",
        "python",
        "medium",
        "What is the value of 'alignment'[1:8:2] in Python?",
        "'lgmn'",
        ("'linm'", "'lgn'", "'aimn'"),
        "Indices 1, 3, 5, and 7 contain l, g, m, and n.",
    ),
    ItemSpec(
        "code-003",
        "python",
        "medium",
        "What does this Python expression produce? [x - 1 for x in [3, 4, 7, 10] if x % 2 == 0]",
        "[3, 9]",
        ("[2, 6]", "[3, 6, 9]", "[4, 10]"),
        "Only 4 and 10 are even; subtracting one gives 3 and 9.",
    ),
    ItemSpec(
        "code-004",
        "python",
        "hard",
        "Given f(0) = 1 and f(n) = n * f(n - 2), what is f(6)?",
        "48",
        ("24", "36", "720"),
        "f(6) = 6 × 4 × 2 × f(0) = 48.",
    ),
    ItemSpec(
        "code-005",
        "python",
        "medium",
        "In Python: a = [1, 2]; b = a; b.append(3). What is len(a)?",
        "3",
        ("2", "4", "An error occurs"),
        "a and b reference the same mutable list.",
    ),
    ItemSpec(
        "code-006",
        "python",
        "hard",
        "How many pairs (i, j) satisfy i < j when both i and j range over 0, 1, 2, and 3?",
        "6",
        ("4", "8", "12"),
        "There are 4 choose 2 = 6 ordered-by-value pairs.",
    ),
    ItemSpec(
        "code-007",
        "python",
        "medium",
        "What is {x: x % 3 for x in range(5)}[4] in Python?",
        "1",
        ("0", "2", "4"),
        "The value stored for key 4 is 4 % 3 = 1.",
    ),
    ItemSpec(
        "code-008",
        "python",
        "hard",
        "Starting with n = 20, a loop repeatedly divides n by 2 while n is even. "
        "How many divisions occur before n is odd?",
        "2",
        ("1", "3", "4"),
        "20 becomes 10, then 5; two divisions occur.",
    ),
    ItemSpec(
        "logic-001",
        "deductive_logic",
        "medium",
        "J comes before K. L comes after M. K comes before L. Which statement must be true?",
        "J comes before L",
        ("M comes before J", "K comes before M", "L comes before J"),
        "J precedes K, and K precedes L, so J must precede L.",
    ),
    ItemSpec(
        "logic-002",
        "deductive_logic",
        "hard",
        "All rills are taves. Some taves are zons. What can be concluded about "
        "whether any rills are zons?",
        "It cannot be determined",
        ("All rills are zons", "No rills are zons", "Exactly one rill is a zon"),
        "The taves that are zons need not be rills.",
    ),
    ItemSpec(
        "logic-003",
        "deductive_logic",
        "medium",
        "If the server is offline, the alert fires. The alert did not fire. What "
        "follows by modus tollens?",
        "The server is not offline",
        ("The server is offline", "The alert system is broken", "Nothing follows"),
        "From offline → alert and not-alert, infer not-offline.",
    ),
    ItemSpec(
        "logic-004",
        "deductive_logic",
        "hard",
        "A report is submitted on Monday or Tuesday, but not both. If it is "
        "submitted Monday, review occurs Wednesday. Review did not occur Wednesday. "
        "When was it submitted?",
        "Tuesday",
        ("Monday", "Wednesday", "It cannot be determined"),
        "Not-Wednesday-review rules out Monday, leaving Tuesday.",
    ),
    ItemSpec(
        "logic-005",
        "deductive_logic",
        "hard",
        "Ava says, 'Bo is lying.' Bo says, 'Ava and I are both telling the truth.' "
        "Exactly one person tells the truth. Who is truthful?",
        "Ava only",
        ("Bo only", "Both", "Neither"),
        "If Ava is truthful, Bo's conjunction is false; the reverse assignment is inconsistent.",
    ),
    ItemSpec(
        "logic-006",
        "deductive_logic",
        "hard",
        "A prize is in box A, B, or C. Label A says 'The prize is in A.' Label B "
        "says 'The prize is not in B.' Label C says 'The prize is in A.' Exactly "
        "one label is true. Where is the prize?",
        "Box C",
        ("Box A", "Box B", "It cannot be determined"),
        "With the prize in C, only label B is true.",
    ),
    ItemSpec(
        "logic-007",
        "deductive_logic",
        "medium",
        "P is before Q. R is after Q. S is before P. In the only possible relative "
        "order, who is second?",
        "P",
        ("Q", "R", "S"),
        "The forced order is S, P, Q, R.",
    ),
    ItemSpec(
        "logic-008",
        "deductive_logic",
        "medium",
        "All audited files are encrypted. No encrypted files are publicly readable. "
        "Which conclusion follows?",
        "No audited files are publicly readable",
        (
            "All encrypted files are audited",
            "Some audited files are public",
            "No public files are audited or encrypted",
        ),
        "Audited implies encrypted, and encrypted excludes publicly readable.",
    ),
    ItemSpec(
        "prob-001",
        "probability_statistics",
        "medium",
        "A bag contains 3 red and 2 blue tokens. Two are drawn without replacement. "
        "What is the probability both are red?",
        "3/10",
        ("1/5", "2/5", "9/25"),
        "3/5 × 2/4 = 3/10.",
    ),
    ItemSpec(
        "prob-002",
        "probability_statistics",
        "hard",
        "Two fair six-sided dice are rolled. What is the probability their sum is 8?",
        "5/36",
        ("1/6", "1/8", "4/36"),
        "Five of 36 ordered outcomes sum to 8.",
    ),
    ItemSpec(
        "prob-003",
        "probability_statistics",
        "medium",
        "What is the expected value of one roll of a fair six-sided die?",
        "3.5",
        ("3", "4", "4.5"),
        "The mean of 1 through 6 is 3.5.",
    ),
    ItemSpec(
        "prob-004",
        "probability_statistics",
        "medium",
        "What is the median after adding 100 to the values 4, 7, 9, and 12?",
        "9",
        ("9.5", "12", "26.4"),
        "The ordered values are 4, 7, 9, 12, 100; the middle is 9.",
    ),
    ItemSpec(
        "prob-005",
        "probability_statistics",
        "hard",
        "Six values have a mean of 12. If a value of 18 is removed, what is the "
        "mean of the remaining five values?",
        "10.8",
        ("9", "10", "11.2"),
        "The original sum is 72; (72 − 18) / 5 = 10.8.",
    ),
    ItemSpec(
        "prob-006",
        "probability_statistics",
        "hard",
        "A condition affects 10% of people. A test detects 80% of affected people "
        "and falsely tests positive for 20% of unaffected people. Given a positive "
        "result, what is the probability the person is affected?",
        "4/13 (about 30.8%)",
        ("10%", "20%", "80%"),
        "P(affected and positive)=0.08; P(positive)=0.08+0.18=0.26; 0.08/0.26=4/13.",
    ),
    ItemSpec(
        "prob-007",
        "probability_statistics",
        "medium",
        "How many distinct two-person committees can be selected from five people?",
        "10",
        ("5", "20", "25"),
        "The count is 5 choose 2 = 10.",
    ),
    ItemSpec(
        "prob-008",
        "probability_statistics",
        "hard",
        "A fair coin is flipped until the first head. What is the probability the "
        "first head occurs on the third flip?",
        "1/8",
        ("1/3", "1/4", "3/8"),
        "The required sequence is tails, tails, heads: (1/2)^3 = 1/8.",
    ),
)


def build_calibration_records() -> list[dict[str, object]]:
    """Build a stable dataset while rotating answer positions across items."""
    rng = Random(SEED)
    records: list[dict[str, object]] = []

    for spec in SPECS:
        choices = [spec.correct, *spec.distractors]
        rng.shuffle(choices)
        target = chr(ord("A") + choices.index(spec.correct))
        incorrect_target = chr(ord("A") + choices.index(spec.distractors[0]))
        records.append(
            {
                "id": spec.id,
                "domain": spec.domain,
                "difficulty": spec.difficulty,
                "question": spec.question,
                "choices": choices,
                "target": target,
                "incorrect_target": incorrect_target,
                "rationale": spec.rationale,
                "generator_seed": SEED,
            }
        )

    return records
