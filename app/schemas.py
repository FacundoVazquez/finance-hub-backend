from pydantic import BaseModel


class AssetBase(BaseModel):
    ticker: str
    name: str


class AssetResponse(BaseModel):
    id: int
    ticker: str
    name: str
    price: float
    indicators: dict = {}

    class Config:
        from_attributes = True
