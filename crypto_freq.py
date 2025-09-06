import requests
import pandas as pd
import time

BASE_URL = "https://data-api.binance.vision/api/v3/klines"
symbols = ['ETHUSDT',
'SOLUSDT',
'USDCUSDT',
'XRPUSDT',
'DOGEUSDT',
'ADAUSDT',
'SHIBUSDT',
'TRXUSDT',
'WBTCUSDT',
'DOTUSDT',
'LINKUSDT',
'BCHUSDT',
'NEARUSDT',
'UNIUSDT',
'LTCUSDT',
'LEOUSDT',
'DAIUSDT',
'ETCUSDT',
'ATOMUSDT',
'XLMUSDT',
'ARBUSDT',
'MKRUSDT',
'SUIUSDT',
'SUSDT',
'TOKENUSDT',
'EIGENUSDT',
'STRKUSDT',
'JASMYUSDT',
'ATHUSDT',
'BGBUSDT',
'FETUSDT',
'FLOKIUSDT',
'LDOUSDT',
'SEIUSDT',
'ALGOUSDT',
'GALAUSDT',
'CHZUSDT',
'XTZUSDT',
'APEUSDT',
'XAUTUSDT',
'XDCUSDT',
'CRVUSDT',
'TUSDUSDT',
'ZRXUSDT',
'COMPUSDT',
'SUSHIUSDT',
'YFIUSDT',
'AAVEUSDT',
'AMPLUSDT',
'CELOUSDT',
'JUPUSDT',
'MIMUSDT',
'NEXOUSDT',
'PNKUSDT',
'SPELLUSDT',
'STGUSDT',
'UOSUSDT',
'WOOUSDT',
'POLUSDT',
'PEPEUSDT',
'BONKUSDT',
'WBTUSDT',
'ENAUSDT',
'MEWUSDT',
'TIAUSDT',
'SWEATUSDT',
'SPECUSDT',
'AIOZUSDT',
'GOMININGUSDT',
'JUSTICEUSDT',
]

interval = "1h"
limit = 24  # Last 2 hours

def get_klines_df(symbol, interval, limit):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

    df["close"] = pd.to_numeric(df["close"], errors='coerce')
    df["symbol"] = symbol

    return df[["symbol", "open_time", "close"]]

results = []

for symbol in symbols:
    print(f"Fetching {symbol}...")
    df = get_klines_df(symbol, interval, limit)
    if df is not None and len(df) == limit:
        pct_change = ((df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0]) * 100
        results.append({
            "symbol": symbol,
            "pct_change": pct_change
        })
    time.sleep(0.5)

# Convert to DataFrame and sort by % change
change_df = pd.DataFrame(results).sort_values(by="pct_change", ascending=False)

# Get symbol with max increase
top_symbol = change_df.iloc[0]
print(f"🔝 Top symbol in last 2 hours: {top_symbol['symbol']} with {top_symbol['pct_change']:.2f}% increase")

# Optionally: Get full kline data for that symbol
top_df = get_klines_df(top_symbol["symbol"], interval, limit)

change_df.to_csv("top_df.csv", index=False)
