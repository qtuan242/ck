"""Cấu hình cho dự án"""

# Danh sách các mã chứng khoán mặc định
DEFAULT_STOCKS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']

# Crypto coins
CRYPTOCURRENCIES = ['BTC-USD', 'ETH-USD', 'BNB-USD']

# Cấu hình yfinance
YFINANCE_CONFIG = {
    'interval': '1d',           # Khoảng thời gian mặc định (1 ngày)
    'progress': False,          # Không hiển thị progress bar
    'prepost': False,           # Không lấy dữ liệu pre/post market
    'threads': True,            # Sử dụng threads
    'proxy': None               # Proxy (nếu cần)
}

# Cấu hình thư mục
DATA_DIR = 'data'
OUTPUT_DIR = 'output'
LOGS_DIR = 'logs'

# Cấu hình kỹ thuật (Technical Analysis)
TECHNICAL_CONFIG = {
    'SMA_periods': [20, 50, 200],
    'EMA_periods': [12, 26],
    'RSI_period': 14,
    'MACD_fast': 12,
    'MACD_slow': 26,
    'MACD_signal': 9,
    'BB_period': 20,
    'BB_std_dev': 2
}
