# Architecture

```
┌──────────┐   image    ┌─────────────────────────────────────────┐
│  React   │ ─────────▶ │ FastAPI /receipts                       │
│  (web)   │            │   1. storage.upload → MinIO            │
└──────────┘            │   2. extraction.extract → Claude vision│
      ▲                 │   3. categorizer.categorize             │
      │ JSON            │   4. anomaly.is_anomaly                 │
      │                 │   5. persist Receipt + LineItems        │
      │                 └─────────────────────────────────────────┘
      │                                 │
      │                                 ▼
      │                         ┌──────────────┐
      └──────── /dashboard ─────│  PostgreSQL  │
                                └──────────────┘
```

## Components

- **apps/web** — React + Vite SPA. Upload UI + dashboard (monthly trend, category breakdown, anomaly list).
- **apps/api** — FastAPI. Routers → services → ORM. Services are pure (no FastAPI imports) so they're unit-testable and reusable from `evals/`.
- **PostgreSQL** — receipts, line_items, categories.
- **MinIO** — object store for raw receipt images (S3-compatible; swap endpoint URL for real AWS).
- **Claude vision** — single call `image → structured receipt JSON` using the prompt in `apps/api/src/receiptiq_api/prompts/extract_receipt_v1.md`.
- **evals/** — golden set + scoring harness. Runs on PRs that touch `services/extraction.py` or `prompts/`.

## Request flow (upload)

1. User selects an image in `UploadReceipt.tsx` → `POST /receipts` multipart.
2. `storage.upload` writes raw bytes to MinIO, returns `image_key`.
3. `extraction.extract` sends the image to Claude vision with the extract prompt, parses JSON into `ReceiptCreate`.
4. `categorizer.categorize` assigns a category.
5. `anomaly.is_anomaly` compares against the user's history for that category.
6. ORM persists `Receipt` + `LineItem` rows; response is `ReceiptOut`.
