"""
SSI FastConnect - Scan Vietnamese stocks (HOSE)
Find strong momentum stocks
"""

import time
import pandas as pd
from datetime import datetime, timedelta

from ssi_fc_data import fc_md_client, model
import config

REQUEST_DELAY = 1.1
LOOKBACK_DAYS = 60
PAGE_SIZE = 10


# ─────────────────────────────────────────────
# INIT CLIENT
# ─────────────────────────────────────────────

client = fc_md_client.MarketDataClient(config)


# ─────────────────────────────────────────────
# GET SYMBOL LIST (with pagination)
# ─────────────────────────────────────────────

def get_symbols():
    """Fetch all HOSE symbols with auto-pagination."""
    symbols = []
    page = 1

    while True:
        req = model.securities('HOSE', page, PAGE_SIZE)
        res = client.securities(config, req)

        data = res.get('data') if res else None
        if not data:
            break

        for s in data:
            sym = s.get('Symbol', '')
            if sym:
                symbols.append(sym)

        # Last page check
        if len(data) < PAGE_SIZE:
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    return symbols


# ─────────────────────────────────────────────
# FETCH OHLC (with pagination)
# ─────────────────────────────────────────────

def fetch_ohlc(symbol):
    """Fetch OHLC for a single symbol, last LOOKBACK_DAYS days."""
    today = datetime.now()
    from_date = (today - timedelta(days=LOOKBACK_DAYS)).strftime("%d/%m/%Y")
    to_date = today.strftime("%d/%m/%Y")

    all_records = []
    page = 1

    while True:
        req = model.daily_ohlc(symbol, from_date, to_date, page, PAGE_SIZE, True)
        res = client.daily_ohlc(config, req)

        status = res.get('status', '') if res else ''
        if status != 'Success':
            break

        data = res.get('data') or []
        if not data:
            break

        all_records.extend(data)

        if len(data) < PAGE_SIZE:
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    if not all_records:
        return None

    df = pd.DataFrame(all_records)

    if df.empty:
        return None

    # Convert types
    df["TradingDate"] = pd.to_datetime(df["TradingDate"], format="%d/%m/%Y")
    df.sort_values("TradingDate", inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Ensure numeric columns
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ─────────────────────────────────────────────
# CALCULATE INDICATORS
# ─────────────────────────────────────────────

def add_indicators(df):

    df["MA20"] = df["Close"].rolling(20).mean()
    df["VOL20"] = df["Volume"].rolling(20).mean()

    return df


# ─────────────────────────────────────────────
# SCAN LOGIC
# ─────────────────────────────────────────────

def scan_stock(symbol, df):

    if len(df) < 25:
        return None

    last = df.iloc[-1]
    prev = df.iloc[-2]

    if prev["Close"] == 0 or pd.isna(prev["Close"]):
        return None

    change = (last["Close"] - prev["Close"]) / prev["Close"] * 100

    cond1 = last["Close"] > last["MA20"]
    cond2 = last["Volume"] > last["VOL20"] * 2
    cond3 = change > 2

    if cond1 and cond2 and cond3:
        return {
            "Symbol": symbol,
            "Close": last["Close"],
            "Change%": round(change, 2),
            "Volume": int(last["Volume"]),
        }

    return None


# ─────────────────────────────────────────────
# MAIN SCANNER
# ─────────────────────────────────────────────

def run_scanner():

    print("=" * 50)
    print("  SSI FastConnect - Stock Scanner (HOSE)")
    print("=" * 50)

    print("\nFetching symbol list...")
    symbols = get_symbols()
    print(f"Total symbols: {len(symbols)}")
    print("-" * 50)

    if not symbols:
        print("[WARN] No symbols found!")
        return

    results = []

    for i, symbol in enumerate(symbols, 1):
        print(f"[{i}/{len(symbols)}] {symbol}...", end=" ")

        try:
            df = fetch_ohlc(symbol)

            if df is None:
                print("skip (no data)")
                continue

            df = add_indicators(df)
            r = scan_stock(symbol, df)

            if r:
                results.append(r)
                print(f"✓ MATCH  Close={r['Close']}  Chg={r['Change%']}%")
            else:
                print("·")

        except Exception as e:
            print(f"ERR: {e}")

        time.sleep(REQUEST_DELAY)

    # Results
    print("\n" + "=" * 50)

    if results:
        df_result = pd.DataFrame(results)
        df_result = df_result.sort_values("Change%", ascending=False)

        print(f"\n🔥 Strong Stocks ({len(results)} found):\n")
        print(df_result.to_string(index=False))

        df_result.to_csv("scanner_result.csv", index=False, encoding="utf-8-sig")
        print(f"\n[OK] Saved -> scanner_result.csv")
    else:
        print("\n[INFO] No stocks matched the criteria.")


# ─────────────────────────────────────────────

if __name__ == "__main__":
    run_scanner()
