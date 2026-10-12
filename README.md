# ReceiptIQ

Turn photos of receipts into organized expense records. Upload a receipt → the app extracts merchant, date, line items, and total using Claude vision, categorizes each expense (groceries, dining, travel, …), and flags unusual charges. A dashboard shows monthly spending trends.

## Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Alembic
- **Frontend**: React 18, Vite, TypeScript, Recharts
- **Database**: PostgreSQL 16
- **Storage**: MinIO (S3-compatible, local)
- **LLM**: Anthropic Claude (vision)
- **Infra**: Docker Compose (local)

## Quick start

1. Copy `.env.example` → `.env` and set `ANTHROPIC_API_KEY`.
2. `make dev` — spins up `api`, `web`, `postgres`, `minio`.
3. Open http://localhost:5173 to upload a receipt. API docs at http://localhost:8000/docs.

## Project layout

```
apps/api        FastAPI backend (receipts, expenses, dashboard)
apps/web        React frontend (upload UI + dashboard)
evals/          Golden-set evaluation harness for extraction accuracy
packages/       Shared JSON schemas
infra/          Local Docker bootstrap (postgres init, minio notes)
```

## Evaluation

`make eval` scores extraction against receipts in `evals/golden_set/`. Results write to `evals/results/<timestamp>.json` with per-field accuracy (merchant exact, date exact, total ±$0.01, line-item F1).
