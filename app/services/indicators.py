from typing import Any, Dict, List

import pandas as pd


def calculate_rsi(data: List[List[Any]], period: int = 14) -> Dict[str, Any]:
    """
    data: [[Date, Open, High, Low, Close, Volume], ...]
    """
    if not data or len(data) < period:
        return {"error": f"Necesitas al menos {period} velas para calcular RSI"}

    # Convertir array de arrays a DataFrame
    df = pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])

    # Asegurar tipo numérico
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Calcular diferencias
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
    # avg_gain = gain.rolling(window=period, min_periods=period).mean()
    # avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df["RSI"] = rsi

    # Devolver solo fecha + RSI
    rsi_data = df[["Date", "RSI"]].dropna().values.tolist()

    return {"period": period, "rsi": rsi_data}


def calculate_macd(
    data: List[List[Any]], fast: int = 12, slow: int = 26, signal: int = 9
) -> Dict[str, Any]:
    """
    data: [[Date, Open, High, Low, Close, Volume], ...]
    """
    if not data or len(data) < slow:
        return {"error": f"Necesitas al menos {slow} velas para calcular MACD"}

    # Convertir a DataFrame
    df = pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Calcular EMAs
    ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line

    df["MACD"] = macd_line
    df["Signal"] = signal_line
    df["Hist"] = hist

    # Exportar a lista de listas
    macd_data = df[["Date", "MACD", "Signal", "Hist"]].dropna().values.tolist()

    return {
        "fast": fast,
        "slow": slow,
        "signal": signal,
        "macd": macd_data,
    }


def calculate_indicators(
    data: List[List[Any]], rsi: bool = True, macd: bool = True
) -> Dict[str, Any]:
    if not data or len(data) < 1:
        return {"error": "At least one indicator is required"}

    indicators = {}
    if rsi:
        indicators["rsi"] = calculate_rsi(data)
    if macd:
        indicators["macd"] = calculate_macd(data)

    return indicators
