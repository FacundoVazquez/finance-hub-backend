from typing import List

import yfinance as yf
from sqlalchemy.orm import Session

import app.services.indicators as indicators_service
from app import models
from app.services.data import fetch_many_ohlcv


def get_many(db: Session) -> List[models.Asset]:
    return db.query(models.Asset).all()


def get_many_full(db: Session):
    assets = db.query(models.Asset).all()

    if len(assets) == 0:
        return []

    tickers: list[str] = [str(asset.ticker) for asset in assets]

    data = fetch_many_ohlcv(
        tickers, period="6mo"
    )  # period >= 5mo is required for indicators to work properly

    # print(data)

    for asset in assets:
        ticker = str(asset.ticker)
        sub = data[ticker].iloc[-1]
        prev = data[ticker].iloc[-2]
        change_pct = ((sub["Close"] - prev["Close"]) / prev["Close"]) * 100

        indicators = indicators_service.calculate_indicators(data[ticker])

        # print(ticker, data[ticker][-1])
        # asset.price = df[ticker][-1][4]
        # asset.price: round(sub["Close"], 2),
        # asset.change_pct: round(change_pct, 2),
        # asset.volume: int(sub["Volume"])
        asset.indicators = {
            "rsi": indicators["rsi"]["rsi"][-1][1],
            "macd": indicators["macd"]["macd"][-1][3],
        }

    return assets


def create_one(ticker: str, db: Session) -> models.Asset:
    ticker = ticker.strip().upper()
    exists = db.query(models.Asset).filter(models.Asset.ticker == ticker).first()

    if exists:
        raise ValueError(f"Ticker {ticker} already exists")

    data = yf.Ticker(ticker)
    info = data.info or {}
    asset_name = info.get("name") or info.get("shortName") or info.get("longName")

    if asset_name is None:
        raise ValueError(f"Ticker {ticker} not found")

    asset = models.Asset(ticker=ticker, name=asset_name)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def delete_one(ticker: str, db: Session) -> None:
    asset = db.query(models.Asset).filter(models.Asset.ticker == ticker).first()

    if not asset:
        raise ValueError(f"Asset with ticker {ticker} not found")

    db.delete(asset)
    db.commit()
