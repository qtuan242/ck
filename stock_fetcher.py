import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


class StockDataFetcher:
    """Lớp để lấy dữ liệu OHLC từ Yahoo Finance"""
    
    def __init__(self):
        pass
    
    def get_ohlc(self, symbol, start_date=None, end_date=None, interval='1d'):
        """
        Lấy dữ liệu OHLC cho một mã chứng khoán
        
        Args:
            symbol (str): Mã chứng khoán (VD: 'BTC-USD', 'AAPL', 'GOOGL')
            start_date (str): Ngày bắt đầu (định dạng: YYYY-MM-DD). Mặc định: 30 ngày trước
            end_date (str): Ngày kết thúc (định dạng: YYYY-MM-DD). Mặc định: hôm nay
            interval (str): Khoảng thời gian ('1m', '5m', '15m', '1h', '1d', '1w', '1mo')
        
        Returns:
            pd.DataFrame: Dữ liệu OHLC
        """
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"Đang lấy dữ liệu {symbol} từ {start_date} đến {end_date}...")
        
        # Lấy dữ liệu từ Yahoo Finance
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        
        # Thêm thông tin cơ bản
        df['Symbol'] = symbol
        df = df.reset_index()
        
        return df
    
    def get_multiple_stocks(self, symbols, start_date=None, end_date=None):
        """
        Lấy dữ liệu cho nhiều mã chứng khoán
        
        Args:
            symbols (list): Danh sách các mã chứng khoán
            start_date (str): Ngày bắt đầu
            end_date (str): Ngày kết thúc
        
        Returns:
            pd.DataFrame: Dữ liệu OHLC hợp nhất
        """
        all_data = []
        
        for symbol in symbols:
            try:
                df = self.get_ohlc(symbol, start_date, end_date)
                all_data.append(df)
                print(f"✓ Đã lấy dữ liệu {symbol}")
            except Exception as e:
                print(f"✗ Lỗi lấy dữ liệu {symbol}: {e}")
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def save_to_csv(self, df, filename):
        """Lưu dữ liệu OHLC vào file CSV"""
        df.to_csv(filename, index=False)
        print(f"✓ Đã lưu dữ liệu vào {filename}")
    
    def display_info(self, df):
        """Hiển thị thông tin cơ bản về dữ liệu"""
        print(f"\nThông tin dữ liệu:")
        print(f"Số hàng: {len(df)}")
        print(f"Số cột: {len(df.columns)}")
        print(f"\nCác cột: {list(df.columns)}")
        print(f"\nDữ liệu đầu tiên:")
        print(df.head())


if __name__ == "__main__":
    # Khởi tạo fetcher
    fetcher = StockDataFetcher()
    
    # Ví dụ 1: Lấy dữ liệu một cổ phiếu (VD: Apple)
    print("=== VÍ DỤ 1: Lấy dữ liệu một cổ phiếu ===")
    df_apple = fetcher.get_ohlc('AAPL', start_date='2025-01-01')
    fetcher.display_info(df_apple)
    fetcher.save_to_csv(df_apple, 'data/apple_ohlc.csv')
    
    # Ví dụ 2: Lấy dữ liệu nhiều cổ phiếu
    print("\n=== VÍ DỤ 2: Lấy dữ liệu nhiều cổ phiếu ===")
    stocks = ['AAPL', 'GOOGL', 'MSFT']
    df_multiple = fetcher.get_multiple_stocks(stocks, start_date='2025-02-01')
    fetcher.display_info(df_multiple)
    fetcher.save_to_csv(df_multiple, 'data/multiple_stocks_ohlc.csv')
    
    # Ví dụ 3: Lấy dữ liệu Bitcoin
    print("\n=== VÍ DỤ 3: Lấy dữ liệu Bitcoin ===")
    df_btc = fetcher.get_ohlc('BTC-USD', start_date='2025-01-01')
    fetcher.display_info(df_btc)
    fetcher.save_to_csv(df_btc, 'data/bitcoin_ohlc.csv')
