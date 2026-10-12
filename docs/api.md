# API

Live, auto-generated docs: http://localhost:8000/docs (Swagger UI) · http://localhost:8000/redoc

## Endpoints (summary)

| Method | Path                     | Purpose                                     |
| ------ | ------------------------ | ------------------------------------------- |
| GET    | `/health`                | Liveness probe                              |
| POST   | `/receipts`              | Upload image, extract + categorize + store  |
| GET    | `/expenses`              | List stored receipts                        |
| PATCH  | `/expenses/{id}`         | Correct a miscategorization                 |
| GET    | `/dashboard/trends`      | Monthly totals for the trend chart          |
| GET    | `/dashboard/anomalies`   | Receipts currently flagged as unusual       |

See `apps/api/src/receiptiq_api/schemas/receipt.py` for request/response shapes.
