# 📈 Dự Án Chứng Khoán Python

Dự án này cung cấp các công cụ để lấy, phân tích và xử lý dữ liệu OHLC (Open, High, Low, Close) từ các sàn giao dịch chứng khoán.

## ✨ Tính năng

- ✅ Lấy dữ liệu OHLC từ Yahoo Finance
- ✅ Hỗ trợ nhiều mã chứng khoán và tiền điện tử
- ✅ Tính toán các chỉ báo kỹ thuật (SMA, EMA, RSI, MACD, Bollinger Bands)
- ✅ Phân tích thống kê cơ bản
- ✅ Lưu dữ liệu vào file CSV
- ✅ So sánh nhiều chứng khoán

## 📋 Cấu trúc thư mục

```
ck/
├── stock_fetcher.py      # Lấy dữ liệu OHLC
├── analysis.py           # Phân tích dữ liệu
├── utils.py              # Hàm tiện ích
├── config.py             # Cấu hình
├── requirements.txt      # Thư viện cần thiết
├── data/                 # Dữ liệu đã lưu
├── output/               # Kết quả phân tích
└── logs/                 # File log
```

## 🚀 Cài đặt

### 1. Clone hoặc tải dự án
```bash
cd /workspaces/ck
```

### 2. Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### 3. Sử dụng dự án

#### A. Lấy dữ liệu OHLC cơ bản
```python
from stock_fetcher import StockDataFetcher

fetcher = StockDataFetcher()

# Lấy dữ liệu Apple từ 30 ngày trước đến hôm nay
df = fetcher.get_ohlc('AAPL')

# Lấy dữ liệu từ ngày cụ thể
df = fetcher.get_ohlc('AAPL', start_date='2025-01-01', end_date='2025-03-03')

# Hiển thị thông tin
fetcher.display_info(df)

# Lưu vào file CSV
fetcher.save_to_csv(df, 'data/aapl_data.csv')
```

#### B. Lấy dữ liệu nhiều chứng khoán
```python
from stock_fetcher import StockDataFetcher

fetcher = StockDataFetcher()

# Danh sách các mã chứng khoán
stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# Lấy dữ liệu
df = fetcher.get_multiple_stocks(stocks, start_date='2025-02-01')

# Lưu dữ liệu
fetcher.save_to_csv(df, 'data/multiple_stocks.csv')
```

#### C. Phân tích kỹ thuật
```python
from stock_fetcher import StockDataFetcher
from utils import add_technical_indicators, get_price_statistics

fetcher = StockDataFetcher()
df = fetcher.get_ohlc('AAPL', start_date='2025-01-01')

# Thêm các chỉ báo kỹ thuật
df = add_technical_indicators(df)

# Lấy thống kê
stats = get_price_statistics(df)
print(stats)

# Xem dữ liệu với các chỉ báo
print(df[['Date', 'Close', 'SMA_20', 'EMA_12', 'RSI_14', 'MACD']])
```

#### D. Chạy các ví dụ có sẵn
```bash
# Lấy dữ liệu
python stock_fetcher.py

# Phân tích
python analysis.py
```

## 📊 Các chỉ báo kỹ thuật được hỗ trợ

| Chỉ báo | Ký hiệu | Mô tả |
|---------|---------|-------|
| Simple Moving Average | SMA | Trung bình động đơn giản |
| Exponential Moving Average | EMA | Trung bình động có trọng số |
| Relative Strength Index | RSI | Độ mạnh tương đối |
| MACD | MACD | Đường hội tụ phân kỳ trung bình động |
| Bollinger Bands | BB | Dải Bollinger |
| Daily Return | - | Lợi suất hàng ngày |

## 📝 Các mã chứng khoán được hỗ trợ

### Stock Market (Mỹ)
- AAPL, GOOGL, MSFT, AMZN, TSLA
- Và bất kỳ mã nào có trên Yahoo Finance

### Tiền điện tử
- BTC-USD (Bitcoin)
- ETH-USD (Ethereum)
- BNB-USD (Binance Coin)

## 🔧 Cấu hình

Chỉnh sửa file `config.py` để tùy chỉnh:

```python
# Danh sách mã chứng khoán mặc định
DEFAULT_STOCKS = ['AAPL', 'GOOGL', 'MSFT']

# Khoảng thời gian mặc định (1d = 1 ngày)
YFINANCE_CONFIG = {
    'interval': '1d',
    'progress': False,
}

# Cấu hình kỹ thuật
TECHNICAL_CONFIG = {
    'SMA_periods': [20, 50, 200],
    'EMA_periods': [12, 26],
    'RSI_period': 14,
}
```

## 📁 Đầu ra

Dữ liệu được lưu trong các thư mục:
- `data/`: Dữ liệu OHLC gốc
- `output/`: Kết quả phân tích
- `logs/`: File log

## 💡 Ví dụ sử dụng nâng cao

### Lấy dữ liệu intraday (theo giờ)
```python
fetcher = StockDataFetcher()
df = fetcher.get_ohlc('AAPL', interval='1h', start_date='2025-03-01', end_date='2025-03-03')
```

### Lấy dữ liệu hàng tuần
```python
df = fetcher.get_ohlc('BTC-USD', interval='1w', start_date='2024-01-01')
```

### Lọc dữ liệu có giá trị RSI > 70 (quá bán)
```python
df = add_technical_indicators(df)
overbought = df[df['RSI_14'] > 70]
```

## ⚠️ Lưu ý

- Yahoo Finance có thể giới hạn số lượng request. Hãy thêm delay khi lấy dữ liệu từ nhiều chứng khoán.
- Một số mã chứng khoán quốc tế có thể không có dữ liệu đầy đủ.
- Dữ liệu trong quá khứ có thể bị ảnh hưởng bởi các sự kiện như tách cổ phiếu (stock split).

## 📚 Tài liệu tham khảo

- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Technical Analysis Indicators](https://www.investopedia.com/terms/t/technicalanalysis.asp)

---

**Cập nhật lần cuối:** March 3, 2026