from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/trends")
def monthly_trends(db: Session = Depends(get_db)) -> list[dict]:
    raise NotImplementedError


@router.get("/anomalies")
def anomalies(db: Session = Depends(get_db)) -> list[dict]:
    raise NotImplementedError
