"""Phân tích dữ liệu OHLC chứng khoán"""

import pandas as pd
from stock_fetcher import StockDataFetcher
from utils import add_technical_indicators, get_price_statistics
import config


def analyze_stock(symbol, start_date=None, end_date=None):
    """
    Phân tích một mã chứng khoán
    
    Args:
        symbol (str): Mã chứng khoán
        start_date (str): Ngày bắt đầu
        end_date (str): Ngày kết thúc
    """
    print(f"\n{'='*60}")
    print(f"Phân tích: {symbol}")
    print(f"{'='*60}")
    
    # Lấy dữ liệu
    fetcher = StockDataFetcher()
    df = fetcher.get_ohlc(symbol, start_date, end_date)
    
    if df.empty:
        print(f"Không thể lấy dữ liệu {symbol}")
        return
    
    # Thêm các chỉ báo kỹ thuật
    df = add_technical_indicators(df)
    
    # Hiển thị thống kê
    print(f"\nThống kê giá (Close):")
    stats = get_price_statistics(df)
    for key, value in stats.items():
        print(f"  {key}: ${value:.2f}")
    
    # Hiển thị dữ liệu gần đây nhất
    print(f"\nDữ liệu gần đây nhất (5 ngày):")
    print(df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].tail(5).to_string(index=False))
    
    # Hiển thị chỉ báo kỹ thuật
    print(f"\nChỉ báo kỹ thuật (ngày gần nhất):")
    latest = df.iloc[-1]
    print(f"  SMA 20: {latest['SMA_20']:.2f}")
    print(f"  EMA 12: {latest['EMA_12']:.2f}")
    print(f"  RSI 14: {latest['RSI_14']:.2f}")
    print(f"  MACD: {latest['MACD']:.4f}")
    print(f"  BB Upper: {latest['BB_Upper']:.2f}")
    print(f"  BB Lower: {latest['BB_Lower']:.2f}")
    print(f"  Daily Return: {latest['Daily_Return']*100:.2f}%")
    
    # Lưu dữ liệu
    output_file = f"{config.DATA_DIR}/{symbol}_analysis.csv"
    fetcher.save_to_csv(df, output_file)
    
    return df


def compare_stocks(symbols, start_date=None, end_date=None):
    """
    So sánh nhiều mã chứng khoán
    
    Args:
        symbols (list): Danh sách các mã chứng khoán
        start_date (str): Ngày bắt đầu
        end_date (str): Ngày kết thúc
    """
    print(f"\n{'='*60}")
    print(f"So sánh: {', '.join(symbols)}")
    print(f"{'='*60}")
    
    fetcher = StockDataFetcher()
    results = {}
    
    for symbol in symbols:
        df = analyze_stock(symbol, start_date, end_date)
        if not df.empty:
            results[symbol] = {
                'Latest Close': df.iloc[-1]['Close'],
                'Min Price': df['Close'].min(),
                'Max Price': df['Close'].max(),
                'Avg Price': df['Close'].mean(),
                'Daily Return': df.iloc[-1]['Daily_Return'] * 100 if 'Daily_Return' in df.columns else 0
            }
    
    # Tạo bảng so sánh
    comparison_df = pd.DataFrame(results).T
    print(f"\n{'='*60}")
    print("Bảng so sánh:")
    print(f"{'='*60}")
    print(comparison_df.to_string())
    
    # Lưu bảng so sánh
    comparison_df.to_csv(f"{config.OUTPUT_DIR}/stock_comparison.csv")
    print(f"\n✓ Bảng so sánh đã được lưu vào {config.OUTPUT_DIR}/stock_comparison.csv")


if __name__ == "__main__":
    # Ví dụ 1: Phân tích một mã chứng khoán
    print("VÍ DỤ 1: Phân tích Apple (AAPL)")
    analyze_stock('AAPL', start_date='2025-01-01')
    
    # Ví dụ 2: So sánh nhiều mã chứng khoán
    print("\n" + "="*60)
    print("VÍ DỤ 2: So sánh các mã chứng khoán")
    compare_stocks(['AAPL', 'GOOGL', 'MSFT'], start_date='2025-02-01')
