.PHONY: dev down test eval migrate lint

dev:
	docker compose up --build

down:
	docker compose down

test:
	docker compose exec api pytest
	docker compose exec web npm test

eval:
	cd evals && python run_eval.py

migrate:
	docker compose exec api alembic upgrade head

lint:
	docker compose exec api ruff check src tests
	docker compose exec api mypy src
	docker compose exec web npm run lint
