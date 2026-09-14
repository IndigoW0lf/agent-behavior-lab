"""Regenerate the committed calibration dataset from its deterministic source."""

import json
from pathlib import Path

from agent_behavior_lab.calibration_items import build_calibration_records

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "calibration_questions.jsonl"


def main() -> None:
    lines = [json.dumps(record, sort_keys=True) for record in build_calibration_records()]
    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} items to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
