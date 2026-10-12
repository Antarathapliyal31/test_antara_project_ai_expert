# ReceiptIQ Evals

Field-level accuracy harness for the receipt extractor.

## Layout

```
golden_set/     ground-truth pairs: receipt_###.jpg + receipt_###.json
run_eval.py     entrypoint — runs extraction over the set, scores each example
scoring.py      field-level metrics (merchant exact, date exact, total within $0.01, line-item F1)
results/        timestamped JSON per run (git-ignored except .gitkeep)
```

## Ground-truth format

Each `receipt_###.json` mirrors `ReceiptCreate`:

```json
{
  "merchant": "Trader Joe's",
  "purchase_date": "2026-03-14",
  "total": 42.17,
  "line_items": [
    { "description": "Bananas", "quantity": 1, "price": 1.29 }
  ]
}
```

## Running

```
cd evals
pip install -r requirements.txt
python run_eval.py
```

Writes `results/<YYYYMMDDTHHMMSSZ>.json`. Compare across runs to track regressions when the prompt or model changes.

## Metrics

- `merchant_exact` — case-sensitive string match
- `date_exact` — ISO date match
- `total_within_1c` — numeric match within $0.01
- `line_item_f1` — F1 over `(description, price)` pairs
