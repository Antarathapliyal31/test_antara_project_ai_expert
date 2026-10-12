import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "apps" / "api" / "src"))
sys.path.insert(0, str(ROOT))

from receiptiq_api.services import extraction  # noqa: E402

from scoring import score_receipt  # noqa: E402

GOLDEN_DIR = ROOT / "golden_set"
RESULTS_DIR = ROOT / "results"


def main() -> None:
    examples = sorted(GOLDEN_DIR.glob("*.jpg"))
    if not examples:
        print(f"no examples found in {GOLDEN_DIR}")
        return

    scores: list[dict] = []
    for image_path in examples:
        truth = json.loads(image_path.with_suffix(".json").read_text())
        predicted = extraction.extract(image_path.read_bytes())
        scores.append({"example": image_path.stem, **score_receipt(predicted, truth)})

    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out = RESULTS_DIR / f"{stamp}.json"
    out.write_text(json.dumps(scores, indent=2, default=str))
    print(f"wrote {out} ({len(scores)} examples)")


if __name__ == "__main__":
    main()
