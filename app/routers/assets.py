from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

import app.services.assets as assets_service
from app import schemas
from app.database import get_db

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("", response_model=list[schemas.AssetResponse])
def get_many(db: Session = Depends(get_db)):
    return assets_service.get_many_full(db)


@router.post(
    "/{ticker}",
    response_model=schemas.AssetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_one(
    ticker: str = Path(..., description="Asset ticker to create, e.g., BTC-USD"),
    db: Session = Depends(get_db),
):
    return assets_service.create_one(ticker, db)


@router.delete("/{ticker}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
    ticker: str = Path(..., description="Asset ticker to delete, e.g., BTC-USD"),
    db: Session = Depends(get_db),
):
    assets_service.delete_one(ticker, db)
