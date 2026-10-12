# MinIO (local S3)

MinIO runs as a Docker service and provides an S3-compatible object store for receipt images.

## Access

- API: http://localhost:9000
- Console: http://localhost:9001 (login: `minioadmin` / `minioadmin`)

## Bucket bootstrap

The API expects a bucket named `receipts` (configurable via `S3_BUCKET`). Create it once after `docker compose up`:

```bash
docker compose exec minio mc alias set local http://localhost:9000 minioadmin minioadmin
docker compose exec minio mc mb local/receipts
```

Or create it via the console at http://localhost:9001.

## Swapping to real S3

Set `S3_ENDPOINT_URL`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, and `S3_BUCKET` in `.env` to AWS values. The `boto3` client in `apps/api/.../services/storage.py` works unchanged.
