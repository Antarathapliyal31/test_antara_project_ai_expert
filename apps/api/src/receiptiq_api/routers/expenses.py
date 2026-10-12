from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import ReceiptOut

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=list[ReceiptOut])
def list_expenses(db: Session = Depends(get_db)) -> list[ReceiptOut]:
    raise NotImplementedError


@router.patch("/{expense_id}", response_model=ReceiptOut)
def update_expense_category(expense_id: int, category: str, db: Session = Depends(get_db)) -> ReceiptOut:
    raise NotImplementedError
