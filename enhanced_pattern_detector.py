"""
Enhanced Pattern detection module for identifying candlestick patterns in stock data.
Updated to include all major Zerodha Varsity patterns with TA-Lib integration.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PatternDetector:
    """Enhanced class for detecting various candlestick patterns in stock data."""

    def __init__(self):
        # All Zerodha Varsity patterns mapped to TA-Lib functions
        self.supported_patterns = {
            # Single Candlestick Patterns
            'marubozu': 'CDLMARUBOZU',
            'doji': 'CDLDOJI',
            'spinning_top': 'CDLSPINNINGTOP',
            'hammer': 'CDLHAMMER',
            'hanging_man': 'CDLHANGINGMAN',
            'shooting_star': 'CDLSHOOTINGSTAR',
            'inverted_hammer': 'CDLINVERTEDHAMMER',
            'dragonfly_doji': 'CDLDRAGONFLYDOJI',
            'gravestone_doji': 'CDLGRAVESTONEDOJI',
            'long_legged_doji': 'CDLLONGLEGGEDDOJI',
            
            # Multiple Candlestick Patterns
            'morning_star': 'CDLMORNINGSTAR',
            'evening_star': 'CDLEVENINGSTAR',
            'morning_doji_star': 'CDLMORNINGDOJISTAR',
            'evening_doji_star': 'CDLEVENINGDOJISTAR',
            'engulfing': 'CDLENGULFING',
            'harami': 'CDLHARAMI',
            'harami_cross': 'CDLHARAMICROSS',
            'piercing_pattern': 'CDLPIERCING',
            'dark_cloud_cover': 'CDLDARKCLOUDCOVER',
            'three_black_crows': 'CDL3BLACKCROWS',
            'three_white_soldiers': 'CDL3WHITESOLDIERS',
            'three_inside': 'CDL3INSIDE',
            'three_outside': 'CDL3OUTSIDE'
        }
        
        # Pattern reliability scores based on market research
        self.pattern_reliability = {
            'three_black_crows': 78,
            'three_white_soldiers': 75,
            'morning_star': 74,
            'evening_star': 72,
            'engulfing': 70,
            'hammer': 68,
            'shooting_star': 68,
            'piercing_pattern': 65,
            'dark_cloud_cover': 65,
            'harami': 63,
            'doji': 60,
            'hanging_man': 58,
            'spinning_top': 55,
            'marubozu': 65,
            'inverted_hammer': 60,
            'three_inside': 68,
            'three_outside': 70,
            'morning_doji_star': 70,
            'evening_doji_star': 69,
            'harami_cross': 62,
            'dragonfly_doji': 58,
            'gravestone_doji': 58,
            'long_legged_doji': 55
        }

    def detect_pattern_talib(self, data: pd.DataFrame, pattern_type: str) -> pd.Series:
        """
        Detect pattern using TA-Lib functions.
        
        Args:
            data: DataFrame with OHLC data
            pattern_type: Type of pattern to detect
            
        Returns:
            Series with pattern detection results
        """
        try:
            import talib
            
            if pattern_type not in self.supported_patterns:
                raise ValueError(f"Pattern {pattern_type} not supported")
                
            # Get the TA-Lib function name
            talib_func_name = self.supported_patterns[pattern_type]
            talib_func = getattr(talib, talib_func_name)
            
            # Prepare data arrays
            open_prices = data['Open'].values.astype(float)
            high_prices = data['High'].values.astype(float)
            low_prices = data['Low'].values.astype(float)
            close_prices = data['Close'].values.astype(float)
            
            # Call the appropriate TA-Lib function
            if pattern_type in ['morning_star', 'evening_star', 'morning_doji_star', 
                              'evening_doji_star', 'dark_cloud_cover', 'piercing_pattern']:
                # These patterns support penetration parameter
                pattern_result = talib_func(open_prices, high_prices, low_prices, close_prices, penetration=0.3)
            else:
                pattern_result = talib_func(open_prices, high_prices, low_prices, close_prices)
            
            return pd.Series(pattern_result, index=data.index, name=pattern_type)
            
        except ImportError:
            logger.error("TA-Lib not installed. Using manual detection fallback.")
            return self.detect_pattern_manual(data, pattern_type)
        except Exception as e:
            logger.error(f"Error in TA-Lib {pattern_type} detection: {e}")
            return pd.Series(0, index=data.index, name=pattern_type)

    def detect_pattern_manual(self, data: pd.DataFrame, pattern_type: str) -> pd.Series:
        """
        Manual pattern detection fallback when TA-Lib is not available.
        Currently implements basic versions of key patterns.
        """
        if pattern_type == 'morning_star':
            return self.detect_morning_star_manual(data)
        elif pattern_type == 'doji':
            return self.detect_doji_manual(data)
        elif pattern_type == 'hammer':
            return self.detect_hammer_manual(data)
        else:
            logger.warning(f"Manual detection for {pattern_type} not implemented")
            return pd.Series(0, index=data.index, name=pattern_type)

    def detect_morning_star_manual(self, data: pd.DataFrame) -> pd.Series:
        """Manual Morning Star pattern detection."""
        if len(data) < 3:
            return pd.Series(0, index=data.index, name='morning_star')

        pattern_signals = pd.Series(0, index=data.index, name='morning_star')

        for i in range(2, len(data)):
            candle1 = data.iloc[i-2]  # First candle (bearish)
            candle2 = data.iloc[i-1]  # Middle candle (small body)
            candle3 = data.iloc[i]    # Third candle (bullish)

            body1 = abs(candle1['Close'] - candle1['Open'])
            body2 = abs(candle2['Close'] - candle2['Open'])
            body3 = abs(candle3['Close'] - candle3['Open'])
            avg_body = (body1 + body2 + body3) / 3

            conditions = [
                candle1['Close'] < candle1['Open'] and body1 > avg_body * 0.7,  # Large bearish
                body2 < body1 * 0.3,  # Small middle body
                candle2['High'] < candle1['Close'],  # Gap down
                candle3['Close'] > candle3['Open'] and body3 > avg_body * 0.7,  # Large bullish
                candle3['Close'] > (candle1['Open'] + candle1['Close']) / 2,  # Closes above midpoint
                candle3['Open'] > candle2['High']  # Gap up
            ]

            if all(conditions):
                pattern_signals.iloc[i] = 100
            elif sum(conditions) >= 4:
                pattern_signals.iloc[i] = 50

        return pattern_signals

    def detect_doji_manual(self, data: pd.DataFrame) -> pd.Series:
        """Manual Doji pattern detection."""
        pattern_signals = pd.Series(0, index=data.index, name='doji')
        
        for i in range(len(data)):
            candle = data.iloc[i]
            body_size = abs(candle['Close'] - candle['Open'])
            total_range = candle['High'] - candle['Low']
            
            # Doji: very small body relative to total range
            if total_range > 0 and body_size / total_range < 0.1:
                pattern_signals.iloc[i] = 100
            elif total_range > 0 and body_size / total_range < 0.2:
                pattern_signals.iloc[i] = 50
                
        return pattern_signals

    def detect_hammer_manual(self, data: pd.DataFrame) -> pd.Series:
        """Manual Hammer pattern detection."""
        pattern_signals = pd.Series(0, index=data.index, name='hammer')
        
        for i in range(len(data)):
            candle = data.iloc[i]
            body_size = abs(candle['Close'] - candle['Open'])
            lower_shadow = min(candle['Open'], candle['Close']) - candle['Low']
            upper_shadow = candle['High'] - max(candle['Open'], candle['Close'])
            
            # Hammer: long lower shadow, small body, small upper shadow
            if (lower_shadow > body_size * 2 and 
                upper_shadow < body_size and
                body_size > 0):
                pattern_signals.iloc[i] = 100
                
        return pattern_signals

    def calculate_pattern_confidence(self, pattern_type: str, pattern_strength: int, 
                                   volume_data: pd.Series, current_idx: int) -> int:
        """
        Calculate confidence score for a detected pattern.
        
        Args:
            pattern_type: Type of pattern detected
            pattern_strength: Raw pattern strength from TA-Lib (-100 to 100)
            volume_data: Volume data for context
            current_idx: Current index in the data
            
        Returns:
            Confidence score (0-100)
        """
        base_reliability = self.pattern_reliability.get(pattern_type, 60)
        
        # Adjust for pattern strength
        if abs(pattern_strength) == 100:
            strength_factor = 1.0
        elif abs(pattern_strength) >= 50:
            strength_factor = 0.8
        else:
            strength_factor = 0.6
            
        # Volume confirmation
        volume_factor = 1.0
        if len(volume_data) > 10:
            avg_volume = volume_data.iloc[-10:].mean()
            current_volume = volume_data.iloc[current_idx]
            if current_volume > avg_volume * 1.5:
                volume_factor = 1.1
            elif current_volume < avg_volume * 0.5:
                volume_factor = 0.9
        
        confidence = min(100, int(base_reliability * strength_factor * volume_factor))
        return confidence

    def detect_pattern(self, data: pd.DataFrame, pattern_type: str = 'morning_star') -> pd.Series:
        """
        Detect specified pattern in stock data.
        
        Args:
            data: DataFrame with OHLC data
            pattern_type: Type of pattern to detect
        
        Returns:
            Series with pattern detection results
        """
        if pattern_type not in self.supported_patterns:
            available_patterns = list(self.supported_patterns.keys())
            raise ValueError(f"Pattern '{pattern_type}' not supported. Available patterns: {available_patterns}")
        
        return self.detect_pattern_talib(data, pattern_type)

    def scan_stocks_for_pattern(self, stocks_data: Dict[str, pd.DataFrame],
                               pattern_type: str = 'morning_star',
                               lookback_days: int = 30) -> List[Dict]:
        """
        Scan multiple stocks for a specific pattern with enhanced confidence scoring.
        
        Args:
            stocks_data: Dictionary mapping symbols to their OHLC data
            pattern_type: Type of pattern to detect
            lookback_days: Number of days to look back for patterns
            
        Returns:
            List of dictionaries containing pattern detection results with confidence scores
        """
        results = []
        logger.info(f"Scanning {len(stocks_data)} stocks for {pattern_type} pattern...")

        for symbol, data in stocks_data.items():
            try:
                # Focus on recent data
                recent_data = data.tail(lookback_days) if len(data) > lookback_days else data
                
                if len(recent_data) < 3:
                    continue
                
                # Detect pattern
                pattern_signals = self.detect_pattern(recent_data, pattern_type)
                
                # Find recent pattern occurrences
                recent_patterns = pattern_signals[pattern_signals != 0]
                
                if not recent_patterns.empty:
                    # Get the most recent pattern
                    latest_pattern_date = recent_patterns.index[-1]
                    pattern_strength = recent_patterns.iloc[-1]
                    
                    # Calculate confidence score
                    pattern_idx = recent_data.index.get_loc(latest_pattern_date)
                    confidence = self.calculate_pattern_confidence(
                        pattern_type, 
                        pattern_strength, 
                        recent_data['Volume'], 
                        pattern_idx
                    )
                    
                    # Get additional context
                    pattern_data = data.loc[latest_pattern_date]
                    
                    # Determine trading recommendation
                    recommendation = self.get_trading_recommendation(pattern_type, pattern_strength, confidence)
                    
                    result = {
                        'symbol': symbol,
                        'pattern_type': pattern_type,
                        'pattern_date': latest_pattern_date.strftime('%Y-%m-%d'),
                        'pattern_strength': int(pattern_strength),
                        'confidence_score': confidence,
                        'recommendation': recommendation,
                        'close_price': float(pattern_data['Close']),
                        'volume': int(pattern_data['Volume']),
                        'high': float(pattern_data['High']),
                        'low': float(pattern_data['Low']),
                        'days_ago': (datetime.now().date() - latest_pattern_date.date()).days
                    }
                    
                    results.append(result)
                    logger.info(f"Found {pattern_type} in {symbol} on {result['pattern_date']} (Confidence: {confidence}%)")

            except Exception as e:
                logger.error(f"Error scanning {symbol}: {e}")
                continue

        # Sort results by confidence score
        results.sort(key=lambda x: x['confidence_score'], reverse=True)
        logger.info(f"Found {len(results)} stocks with {pattern_type} pattern")
        return results

    def get_trading_recommendation(self, pattern_type: str, pattern_strength: int, confidence: int) -> str:
        """
        Generate trading recommendation based on pattern characteristics.
        
        Args:
            pattern_type: Type of pattern
            pattern_strength: Pattern strength (-100 to 100)
            confidence: Confidence score (0-100)
            
        Returns:
            Trading recommendation string
        """
        bullish_patterns = ['morning_star', 'morning_doji_star', 'hammer', 'inverted_hammer',
                           'piercing_pattern', 'three_white_soldiers', 'bullish_engulfing']
        bearish_patterns = ['evening_star', 'evening_doji_star', 'shooting_star', 'hanging_man',
                           'dark_cloud_cover', 'three_black_crows', 'bearish_engulfing']
        
        if confidence >= 70:
            strength_desc = "Strong"
        elif confidence >= 60:
            strength_desc = "Moderate"
        else:
            strength_desc = "Weak"
            
        if pattern_strength > 0:  # Bullish signal
            if any(bp in pattern_type for bp in ['morning', 'hammer', 'piercing', 'white', 'engulfing']):
                action = "BUY"
            else:
                action = "CONSIDER BUY"
        else:  # Bearish signal
            if any(bp in pattern_type for bp in ['evening', 'shooting', 'hanging', 'dark', 'black']):
                action = "SELL"
            else:
                action = "CONSIDER SELL"
                
        return f"{strength_desc} {action} Signal"

    def get_pattern_summary(self, results: List[Dict]) -> Dict:
        """
        Generate a summary of pattern detection results with confidence statistics.
        
        Args:
            results: List of pattern detection results
            
        Returns:
            Dictionary with summary statistics
        """
        if not results:
            return {
                'total_patterns': 0,
                'patterns_by_confidence': {},
                'patterns_by_strength': {},
                'average_confidence': 0,
                'average_volume': 0,
                'average_price': 0,
                'high_confidence_count': 0
            }

        # Calculate statistics
        confidences = [r['confidence_score'] for r in results]
        pattern_strengths = [r['pattern_strength'] for r in results]
        volumes = [r['volume'] for r in results]
        prices = [r['close_price'] for r in results]
        
        # Categorize by confidence
        confidence_categories = {'High (70-100%)': 0, 'Medium (50-69%)': 0, 'Low (0-49%)': 0}
        for conf in confidences:
            if conf >= 70:
                confidence_categories['High (70-100%)'] += 1
            elif conf >= 50:
                confidence_categories['Medium (50-69%)'] += 1
            else:
                confidence_categories['Low (0-49%)'] += 1
        
        # Categorize by strength
        strength_counts = {}
        for strength in pattern_strengths:
            strength_counts[strength] = strength_counts.get(strength, 0) + 1

        summary = {
            'total_patterns': len(results),
            'patterns_by_confidence': confidence_categories,
            'patterns_by_strength': strength_counts,
            'average_confidence': sum(confidences) / len(confidences) if confidences else 0,
            'average_volume': sum(volumes) / len(volumes) if volumes else 0,
            'average_price': sum(prices) / len(prices) if prices else 0,
            'high_confidence_count': confidence_categories['High (70-100%)'],
            'symbols_found': [r['symbol'] for r in results]
        }

        return summary
