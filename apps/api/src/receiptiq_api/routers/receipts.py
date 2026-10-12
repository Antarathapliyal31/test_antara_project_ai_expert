from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from ..db import get_db
from ..schemas import ReceiptOut
from ..services import extraction, storage

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.post("", response_model=ReceiptOut)
async def upload_receipt(file: UploadFile, db: Session = Depends(get_db)) -> ReceiptOut:
    image_bytes = await file.read()
    _image_key = storage.upload(image_bytes, filename=file.filename or "receipt.jpg")
    _extracted = extraction.extract(image_bytes)
    raise NotImplementedError("persist receipt + line items, categorize, flag anomaly, return ReceiptOut")
