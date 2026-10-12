from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import dashboard, expenses, health, receipts


def create_app() -> FastAPI:
    app = FastAPI(title="ReceiptIQ")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health.router)
    app.include_router(receipts.router)
    app.include_router(expenses.router)
    app.include_router(dashboard.router)
    return app


app = create_app()
