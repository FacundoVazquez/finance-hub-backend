from typing import List

import services.data as data_service
from fastapi import APIRouter, Query

router = APIRouter(prefix="/data", tags=["Data"])


@router.get("/data")
def get_data(
    tickers: List[str] = Query(
        ["BTC-USD", "CRV-USD"],
        description="List of asset tickers. Example: BTC-USD, ETH-USD",
    ),
    period: str = Query("1mo", description="Period: 1d,1mo,1y,max"),
    interval: str = Query("1d", description="Interval: 1m,5m,1h,1d,1wk"),
):
    return data_service.fetch_many_ohlcv(tickers, period, interval)
