"""Write deterministic filter/transform calibration and confirmatory datasets."""

import json
from pathlib import Path

from agent_behavior_lab.filter_transform_items import build_filter_transform_records

DATA_DIR = Path(__file__).parent.parent / "data"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for split, records in build_filter_transform_records().items():
        output_path = DATA_DIR / f"filter_transform_{split}.jsonl"
        with output_path.open("w", encoding="utf-8") as output:
            for record in records:
                output.write(json.dumps(record, sort_keys=True) + "\n")
        print(f"Wrote {len(records)} items to {output_path}")


if __name__ == "__main__":
    main()
