from typing import Any, Dict, List

import yfinance as yf

# yf.enable_debug_mode()

# Constants
RATE_LIMIT_SLEEP = 1  # seconds to sleep to avoid hitting rate limits


def fetch_one_ohlcv(
    ticker: str,
    period: str = "1mo",
    interval: str = "1d",
) -> Dict[str, Any]:
    df = yf.download(
        ticker, period=period, interval=interval, auto_adjust=True, rounding=True
    )

    if df is None or df.empty:
        return {"error": f"Data not found for asset: {ticker}"}

    df = df.reset_index()
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    df["Date"] = df["Date"].astype(str)

    data: List[List[Any]] = df.values.tolist()

    return {
        "ticker": ticker,
        "period": period,
        "interval": interval,
        "data": data,
    }


def fetch_many_ohlcv(
    tickers: List[str], period: str = "1mo", interval: str = "1d"
) -> Dict[str, Any]:
    results: Dict[str, Any] = {
        "tickers": tickers,
        "period": period,
        "interval": interval,
    }
    # for ticker in tickers:
    #     results[ticker] = fetch_one_ohlcv(ticker, period, interval).get("data", [])
    #     sleep(RATE_LIMIT_SLEEP)  # To avoid hitting rate limits
    # return results
    df = yf.download(
        tickers,
        period=period,
        interval=interval,
        auto_adjust=True,
        rounding=True,
        group_by="ticker",
    )

    if df is None or df.empty:
        return {"error": f"Data not found for asset: {tickers}"}

    if isinstance(tickers, str):
        tickers = [tickers]

    for ticker in tickers:
        try:
            sub_df = df[ticker].reset_index()
            sub_df["Date"] = sub_df["Date"].astype(str)
            sub_df = sub_df.dropna(subset=["Open", "High", "Low", "Close", "Volume"])
            results[ticker] = sub_df[
                ["Date", "Open", "High", "Low", "Close", "Volume"]
            ].values.tolist()
        except KeyError:
            results[ticker] = []

    return results


def fetch_assets_info(tickers: List[str]) -> Dict[str, Any]:
    assets_info: Dict[str, Any] = {}

    for ticker in tickers:
        info = yf.Ticker(ticker).info
        assets_info[ticker] = {
            "name": info.get("longName", ticker),
            "ticker": ticker,
            "price": info.get("currentPrice"),
            "change %": info.get("regularMarketChangePercent"),
            "volume": info.get("volume"),
        }

    return assets_info
