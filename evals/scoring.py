from decimal import Decimal
from typing import Any


def score_receipt(predicted: Any, truth: dict) -> dict:
    pred = predicted.model_dump() if hasattr(predicted, "model_dump") else dict(predicted)

    return {
        "merchant_exact": pred.get("merchant") == truth.get("merchant"),
        "date_exact": str(pred.get("purchase_date")) == str(truth.get("purchase_date")),
        "total_within_1c": _within_cent(pred.get("total"), truth.get("total")),
        "line_item_f1": _line_item_f1(pred.get("line_items") or [], truth.get("line_items") or []),
    }


def _within_cent(a: Any, b: Any) -> bool:
    return abs(Decimal(str(a or 0)) - Decimal(str(b or 0))) <= Decimal("0.01")


def _line_item_f1(predicted: list, truth: list) -> float:
    pred_set = {(li.get("description"), str(li.get("price"))) for li in predicted}
    truth_set = {(li.get("description"), str(li.get("price"))) for li in truth}
    if not pred_set and not truth_set:
        return 1.0
    tp = len(pred_set & truth_set)
    precision = tp / len(pred_set) if pred_set else 0.0
    recall = tp / len(truth_set) if truth_set else 0.0
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)
