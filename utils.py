"""Các hàm tiện ích cho phân tích dữ liệu OHLC"""

import pandas as pd
import numpy as np


def calculate_sma(df, column='Close', period=20):
    """
    Tính Simple Moving Average (SMA)
    
    Args:
        df (pd.DataFrame): Dataframe chứa dữ liệu OHLC
        column (str): Cột dùng để tính SMA (mặc định: 'Close')
        period (int): Số ngày để tính SMA (mặc định: 20)
    
    Returns:
        pd.Series: Giá trị SMA
    """
    return df[column].rolling(window=period).mean()


def calculate_ema(df, column='Close', period=12):
    """
    Tính Exponential Moving Average (EMA)
    
    Args:
        df (pd.DataFrame): Dataframe chứa dữ liệu OHLC
        column (str): Cột dùng để tính EMA (mặc định: 'Close')
        period (int): Số ngày để tính EMA (mặc định: 12)
    
    Returns:
        pd.Series: Giá trị EMA
    """
    return df[column].ewm(span=period, adjust=False).mean()


def calculate_rsi(df, column='Close', period=14):
    """
    Tính Relative Strength Index (RSI)
    
    Args:
        df (pd.DataFrame): Dataframe chứa dữ liệu OHLC
        column (str): Cột dùng để tính RSI (mặc định: 'Close')
        period (int): Số ngày để tính RSI (mặc định: 14)
    
    Returns:
        pd.Series: Giá trị RSI
    """
    delta = df[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_macd(df, column='Close', fast=12, slow=26, signal=9):
    """
    Tính MACD (Moving Average Convergence Divergence)
    
    Args:
        df (pd.DataFrame): Dataframe chứa dữ liệu OHLC
        column (str): Cột dùng để tính MACD (mặc định: 'Close')
        fast (int): Kỳ hạn ngắn (mặc định: 12)
        slow (int): Kỳ hạn dài (mặc định: 26)
        signal (int): Kỳ hạn signal line (mặc định: 9)
    
    Returns:
        tuple: (MACD line, Signal line, Histogram)
    """
    ema_fast = df[column].ewm(span=fast, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow, adjust=False).mean()
    
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(df, column='Close', period=20, std_dev=2):
    """
    Tính Bollinger Bands
    
    Args:
        df (pd.DataFrame): Dataframe chứa dữ liệu OHLC
        column (str): Cột dùng để tính (mặc định: 'Close')
        period (int): Số ngày để tính (mặc định: 20)
        std_dev (int): Số độ lệch chuẩn (mặc định: 2)
    
    Returns:
        tuple: (Upper band, Middle band/SMA, Lower band)
    """
    sma = df[column].rolling(window=period).mean()
    std = df[column].rolling(window=period).std()
    
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    
    return upper_band, sma, lower_band


def calculate_daily_return(df, column='Close'):
    """
    Tính lợi suất hàng ngày
    
    Args:
        df (pd.DataFrame): Dataframe chứa dữ liệu OHLC
        column (str): Cột dùng để tính (mặc định: 'Close')
    
    Returns:
        pd.Series: Lợi suất hàng ngày
    """
    return df[column].pct_change()


def add_technical_indicators(df, column='Close'):
    """
    Thêm các chỉ báo kỹ thuật vào dataframe
    
    Args:
        df (pd.DataFrame): Dataframe chứa dữ liệu OHLC
        column (str): Cột dùng để tính (mặc định: 'Close')
    
    Returns:
        pd.DataFrame: Dataframe với các chỉ báo kỹ thuật
    """
    df = df.copy()
    
    # Thêm các chỉ báo
    df['SMA_20'] = calculate_sma(df, column, 20)
    df['EMA_12'] = calculate_ema(df, column, 12)
    df['RSI_14'] = calculate_rsi(df, column, 14)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = calculate_macd(df, column)
    df['BB_Upper'], df['BB_Middle'], df['BB_Lower'] = calculate_bollinger_bands(df, column)
    df['Daily_Return'] = calculate_daily_return(df, column)
    
    return df


def get_price_statistics(df, column='Close'):
    """
    Lấy thống kê cơ bản về giá
    
    Args:
        df (pd.DataFrame): Dataframe chứa dữ liệu OHLC
        column (str): Cột dùng để tính (mặc định: 'Close')
    
    Returns:
        dict: Thống kê
    """
    return {
        'Min': df[column].min(),
        'Max': df[column].max(),
        'Mean': df[column].mean(),
        'Std': df[column].std(),
        'Latest': df[column].iloc[-1]
    }
