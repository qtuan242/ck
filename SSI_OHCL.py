"""
SSI FastConnect - Fetch Daily OHLC for multiple symbols
Auto-pagination, rate limiting, CSV export
"""
import os
import time
import argparse
from datetime import datetime, timedelta

import pandas as pd
from ssi_fc_data import fc_md_client, model
import config

# --- Default config ---------------------------------------------------------
# DEFAULT_SYMBOLS = [
#     'FPT', 'VNM', 'HPG', 'MWG', 'SSI',
#     'VCB', 'TCB', 'ACB', 'MSN', 'VIC',
# ]
DEFAULT_SYMBOLS = [
    'FPT', 'VNM'
]
PAGE_SIZE = 100          # Records per page (API max)
REQUEST_DELAY = 1.1      # Seconds between requests (API limit: 1 req/sec)
DATE_FORMAT = '%d/%m/%Y' # Date format for SSI API


# --- Fetch OHLC with pagination ---------------------------------------------
def fetch_daily_ohlc(client, symbol: str, from_date: str, to_date: str) -> list:
    """
    Fetch all Daily OHLC for 1 symbol with auto-pagination.
    Returns: list of dict (each dict = 1 OHLC record)
    """
    all_records = []
    page = 1

    while True:
        req = model.daily_ohlc(symbol, from_date, to_date, page, PAGE_SIZE, True)
        response = client.daily_ohlc(config, req)

        # Check response status
        status = response.get('status', '')
        if status != 'Success':
            msg = response.get('message', 'Unknown error')
            raise RuntimeError(f"API error [{status}]: {msg}")

        data = response.get('data') or []
        total = response.get('totalRecord', 0)
        if not data:
            break

        all_records.extend(data)

        # If data < PAGE_SIZE -> last page
        if len(data) < PAGE_SIZE:
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    return all_records


# --- Main fetch function -----------------------------------------------------
def get_multi_ohlc(symbols: list, from_date: str, to_date: str, output_dir: str):
    """
    Fetch Daily OHLC for multiple symbols, save each symbol as separate CSV.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f'[DATE] Period: {from_date} -> {to_date}')
    print(f'[INFO] Symbols count: {len(symbols)}')
    print(f'[LIST] Symbols: {", ".join(symbols)}')
    print('-' * 50)

    client = fc_md_client.MarketDataClient(config)
    saved = 0
    total_records = 0
    errors = []

    for i, symbol in enumerate(symbols, 1):
        print(f'[{i}/{len(symbols)}] Fetching {symbol}...', end=' ')

        try:
            records = fetch_daily_ohlc(client, symbol, from_date, to_date)

            if records:
                # Add Symbol column
                for r in records:
                    r['Symbol'] = symbol

                # Convert & save immediately
                df = pd.DataFrame(records)
                if 'TradingDate' in df.columns:
                    df['TradingDate'] = pd.to_datetime(
                        df['TradingDate'], format='%d/%m/%Y'
                    ).dt.strftime('%Y-%m-%d')
                    df.sort_values('TradingDate', inplace=True)

                fpath = os.path.join(output_dir, f'{symbol}.csv')
                df.to_csv(fpath, index=False, encoding='utf-8-sig')
                saved += 1
                total_records += len(df)
                print(f'OK - {len(df)} records -> {fpath}')
            else:
                print('WARN - No data')

        except Exception as e:
            print(f'FAIL - {e}')
            errors.append((symbol, str(e)))

        # Delay between symbols
        if i < len(symbols):
            time.sleep(REQUEST_DELAY)

    print('-' * 50)
    print(f'[OK] Saved {saved} files, {total_records} total records -> {output_dir}/')

    # Error report
    if errors:
        print(f'[WARN] {len(errors)} symbol(s) failed:')
        for sym, err in errors:
            print(f'   {sym}: {err}')

    return saved, total_records


# --- CLI ---------------------------------------------------------------------
def parse_args():
    today = datetime.now()
    default_from = (today - timedelta(days=530)).strftime(DATE_FORMAT)
    default_to = today.strftime(DATE_FORMAT)

    parser = argparse.ArgumentParser(
        description='Fetch Daily OHLC for multiple symbols from SSI FastConnect'
    )
    parser.add_argument(
        '-s', '--symbols',
        nargs='+',
        default=DEFAULT_SYMBOLS,
        help=f'Stock symbols (default: {" ".join(DEFAULT_SYMBOLS)})'
    )
    parser.add_argument(
        '-f', '--from-date',
        default=default_from,
        help=f'Start date dd/mm/yyyy (default: {default_from})'
    )
    parser.add_argument(
        '-t', '--to-date',
        default=default_to,
        help=f'End date dd/mm/yyyy (default: {default_to})'
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='ohlc_data',
        help='Output directory for CSV files (default: ohlc_data)'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print('=' * 50)
    print('  SSI FastConnect - Daily OHLC Fetcher')
    print('=' * 50)
    get_multi_ohlc(
        symbols=args.symbols,
        from_date=args.from_date,
        to_date=args.to_date,
        output_dir=args.output_dir,
    )
