# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

ReceiptIQ — upload a receipt photo → Claude vision extracts merchant/date/line-items/total → categorize → store → dashboard shows monthly trends and flags anomalies. Monorepo: FastAPI backend + React/Vite frontend + first-class eval harness. Local dev runs on Docker Compose (no AWS yet).

## Common commands

Everything runs through the stack brought up by `docker compose`. The `Makefile` wraps the common commands.

```bash
cp .env.example .env           # then set ANTHROPIC_API_KEY
make dev                       # up: api:8000, web:5173, postgres:5432, minio:9000 (console :9001)
make down                      # tear down

make migrate                   # alembic upgrade head (inside api container)
make test                      # pytest (api) + vitest (web)
make eval                      # score golden set, write evals/results/<timestamp>.json
make lint                      # ruff + mypy (api) + eslint (web)
```

Direct container access when you need it:

```bash
docker compose exec api pytest tests/unit/test_scoring.py::test_name   # single test
docker compose exec api alembic revision --autogenerate -m "add x"     # new migration
docker compose exec minio mc alias set local http://localhost:9000 minioadmin minioadmin
docker compose exec minio mc mb local/receipts                         # first-time bucket create
```

After the stack is up for the first time, you must create the `receipts` MinIO bucket (see `infra/minio/README.md`).

## Architecture

### Request flow (upload)

```
React UploadReceipt → POST /receipts (multipart)
  → services.storage.upload       (bytes → MinIO, returns image_key)
  → services.extraction.extract   (bytes → Claude vision → ReceiptCreate)
  → services.categorizer.categorize (merchant+line_items → category)
  → services.anomaly.is_anomaly   (amount vs per-category history → bool)
  → ORM persist (Receipt + LineItem rows)
  → ReceiptOut response
```

Dashboard reads via `GET /dashboard/trends` and `/dashboard/anomalies`.

### Layering rules (important)

- **Routers (`apps/api/src/receiptiq_api/routers/`)** are thin — parse request, call services, serialize response.
- **Services (`.../services/`) must not import FastAPI.** This is deliberate: the eval harness in `evals/run_eval.py` imports `extraction.extract` directly (no HTTP) by adding `apps/api/src` to `sys.path`. If services take on FastAPI dependencies, evals break.
- **Models (`.../models/`)** are the SQLAlchemy source of truth. Alembic autogen reads them via `apps/api/alembic/env.py`, which imports `receiptiq_api.models` purely for side effects — removing that import silently breaks migration generation.

### Prompts are first-class, versioned artifacts

Prompts live in `apps/api/src/receiptiq_api/prompts/` as versioned Markdown files (`extract_receipt_v1.md`, `categorize_v1.md`) and are loaded by filename at runtime. Changing a prompt shows up in `git diff`. CI workflow `.github/workflows/eval.yml` runs the eval harness on PRs that touch `services/extraction.py` or any file under `prompts/` — so a prompt change surfaces its accuracy impact before merge.

Bump the version (e.g. `extract_receipt_v2.md`) rather than rewriting the existing file when you make a non-trivial change you want to A/B against the previous one.

### Storage is S3-compatible, not AWS-coupled

`services/storage.py` uses `boto3` with `endpoint_url` pointed at MinIO (`http://minio:9000` in Docker). To ship to real AWS later, change `S3_ENDPOINT_URL`/`S3_ACCESS_KEY`/`S3_SECRET_KEY`/`S3_BUCKET` in `.env`; no code change needed. Don't hardcode AWS-specific calls.

### Shared schema

`packages/schemas/receipt.schema.json` is the intended single source of truth for the extracted-receipt shape, consumed by backend Pydantic (`schemas/receipt.py`) and TS types (future). If you change the extracted shape, update all three.

### Database bootstrap

`infra/postgres/init.sql` runs once on first container start (via `/docker-entrypoint-initdb.d/`) and seeds the fixed 9 categories (`groceries`, `dining`, `travel`, `transport`, `entertainment`, `shopping`, `utilities`, `health`, `other`). The `categorize_v1.md` prompt must stay in sync with this list — if you add a category, add it in both places or extraction output won't map to a FK.

The schema itself is managed by Alembic migrations, **not** `init.sql` — only the categories seed lives there.

## Evals

`evals/` is a portfolio-facing harness, not a test suite. It:

1. Reads image/JSON pairs from `evals/golden_set/`.
2. Calls `receiptiq_api.services.extraction.extract` directly on each image.
3. Scores with `scoring.py` — `merchant_exact`, `date_exact`, `total_within_1c`, `line_item_f1`.
4. Writes `evals/results/<YYYYMMDDTHHMMSSZ>.json`.

Results are git-ignored except for `.gitkeep`; the eval CI workflow uploads them as a build artifact.

## Model choice

Default extraction model is `claude-opus-4-7` (set in `services/extraction.py`). This project is explicitly built as an AI-engineering portfolio piece — when experimenting with cheaper models, keep a Claude variant as the baseline for parity with the README claims.
