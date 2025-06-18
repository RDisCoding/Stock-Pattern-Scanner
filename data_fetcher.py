"""
Data fetching module for stock market data.
"""
import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    """Class to fetch stock market data from various sources."""
    
    def __init__(self, data_source: str = "yahoo"):
        self.data_source = data_source
        
    def get_stock_data(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        """
        Fetch stock data for a single symbol.
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            DataFrame with OHLCV data or None if failed
        """
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            # Ensure we have the required columns
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in required_columns):
                logger.error(f"Missing required columns for {symbol}")
                return None
            
            # Add symbol column for identification
            data['Symbol'] = symbol
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_multiple_stocks_data(self, symbols: List[str], period: str = "6mo") -> Dict[str, pd.DataFrame]:
        """
        Fetch stock data for multiple symbols.
        
        Args:
            symbols: List of stock ticker symbols
            period: Time period
        
        Returns:
            Dictionary mapping symbols to their data DataFrames
        """
        stock_data = {}
        total_symbols = len(symbols)
        
        logger.info(f"Fetching data for {total_symbols} symbols...")
        
        for i, symbol in enumerate(symbols, 1):
            logger.info(f"Fetching {symbol} ({i}/{total_symbols})")
            data = self.get_stock_data(symbol, period)
            
            if data is not None:
                stock_data[symbol] = data
            else:
                logger.warning(f"Failed to fetch data for {symbol}")
        
        logger.info(f"Successfully fetched data for {len(stock_data)} out of {total_symbols} symbols")
        return stock_data
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        Get additional stock information.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with stock info or None if failed
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Extract relevant information
            relevant_info = {
                'symbol': symbol,
                'longName': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'marketCap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'averageVolume': info.get('averageVolume', 0),
                'currentPrice': info.get('currentPrice', 0),
                'dayHigh': info.get('dayHigh', 0),
                'dayLow': info.get('dayLow', 0),
                'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh', 0),
                'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow', 0)
            }
            
            return relevant_info
            
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {e}")
            return None
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if a stock symbol is valid and has data.
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            True if valid, False otherwise
        """
        try:
            stock = yf.Ticker(symbol)
            # Try to get recent data
            data = stock.history(period="5d")
            return not data.empty
        except:
            return False
    
    def filter_valid_symbols(self, symbols: List[str]) -> List[str]:
        """
        Filter out invalid symbols from a list.
        
        Args:
            symbols: List of stock ticker symbols
        
        Returns:
            List of valid symbols
        """
        valid_symbols = []
        logger.info(f"Validating {len(symbols)} symbols...")
        
        for symbol in symbols:
            if self.validate_symbol(symbol):
                valid_symbols.append(symbol)
            else:
                logger.warning(f"Invalid symbol: {symbol}")
        
        logger.info(f"Found {len(valid_symbols)} valid symbols")
        return valid_symbols
