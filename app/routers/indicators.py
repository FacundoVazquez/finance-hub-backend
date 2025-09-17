from typing import Any, List

from fastapi import APIRouter, Body

import app.services.indicators as indicators_service

router = APIRouter(prefix="/indicators", tags=["Indicators"])


@router.post("")
def get_indicators(
    data: List[List[Any]] = Body(
        ..., description="OHLCV array [[Date,Open,High,Low,Close,Volume],...]"
    ),
    rsi: bool = Body(True, description="Calculate or not RSI indicator"),
    macd: bool = Body(True, description="Calculate or not MACD indicator"),
):
    return indicators_service.calculate_indicators(data, rsi, macd)


@router.post("/rsi")
def get_rsi(
    data: List[List[Any]] = Body(
        ..., description="OHLCV array: [[Date, Open, High, Low, Close, Volume], ...]"
    ),
    period: int = 14,
):
    return indicators_service.calculate_rsi(data, period)


@router.post("/macd")
def get_macd(
    data: List[List[Any]] = Body(
        ..., description="OHLCV array [[Date,Open,High,Low,Close,Volume],...]"
    ),
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
):
    return indicators_service.calculate_macd(data, fast, slow, signal)
