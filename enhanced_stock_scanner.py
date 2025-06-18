"""
Enhanced Stock Pattern Scanner with multiple patterns, confidence scoring, and email alerts.
Supports all Zerodha Varsity patterns with real-time data fetching and automated notifications.
"""

import logging
import sys
import os
import argparse
from datetime import datetime, time
from typing import List, Dict, Set
import schedule
import time as time_module

# Import enhanced modules
from enhanced_pattern_detector import PatternDetector
from enhanced_email_system import EmailNotificationSystem
from data_fetcher import DataFetcher
from config_local import config

# Set up comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pattern_scanner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class EnhancedStockPatternScanner:
    """
    Enhanced Stock Pattern Scanner with multiple pattern support and automation features.
    """
    
    def __init__(self, email_config: Dict = None):
        """Initialize the enhanced scanner with all components."""
        self.config = config
        self.data_fetcher = DataFetcher()
        self.pattern_detector = PatternDetector()

        # Enhanced email system initialization
        if email_config is None:
            # Try to load email config from the main config
            try:
                if hasattr(self.config, 'config') and 'notification' in self.config.config:
                    email_config = self.config.config.get('notification', {}).get('email', {})
                    logger.info("Email configuration loaded from main config")
                else:
                    logger.info("No email configuration provided, using environment variables")
            except Exception as e:
                logger.warning(f"Error loading email config from main config: {e}")

        self.email_system = EmailNotificationSystem(email_config)

        logger.info("Enhanced Stock Pattern Scanner initialized")
        logger.info(f"Supported patterns: {list(self.pattern_detector.supported_patterns.keys())}")
        logger.info(f"Email enabled: {self.email_system.config.get('enabled', False)}")
    
    def load_stock_symbols(self, file_path: str = 'sample_stocks.txt') -> List[str]:
        """
        Load stock symbols from file with support for Indian stocks.
        Automatically adds .NS suffix for NSE stocks if not present.
        """
        symbols = []
        
        if not os.path.exists(file_path):
            logger.warning(f"Stock list file not found: {file_path}")
            # Create sample list with Indian stocks
            default_symbols = [
                'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS',
                'KOTAKBANK.NS', 'HDFCBANK.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS',
                'ASIANPAINT.NS', 'MARUTI.NS', 'TITAN.NS', 'WIPRO.NS', 'ULTRACEMCO.NS'
            ]
            
            with open(file_path, 'w') as f:
                for symbol in default_symbols:
                    f.write(f"{symbol}\n")
            
            logger.info(f"Created sample Indian stock list with {len(default_symbols)} symbols")
            return default_symbols
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    symbol = line.strip().upper()
                    if symbol and not symbol.startswith('#'):
                        # Auto-add .NS for Indian stocks if not present
                        if '.' not in symbol:
                            symbol += '.NS'
                        symbols.append(symbol)
            
            logger.info(f"Loaded {len(symbols)} stock symbols from {file_path}")
            return symbols
            
        except Exception as e:
            logger.error(f"Error loading stock symbols: {e}")
            return []
    
    def scan_for_multiple_patterns(self, symbols: List[str], 
                                  patterns: List[str] = None,
                                  lookback_days: int = 30) -> Dict[str, List[Dict]]:
        """
        Scan stocks for multiple patterns simultaneously.
        
        Args:
            symbols: List of stock symbols to scan
            patterns: List of patterns to detect (default: all patterns)
            lookback_days: Number of days to look back
            
        Returns:
            Dictionary mapping pattern names to their results
        """
        if patterns is None:
            # Use most reliable patterns by default
            patterns = [
                'morning_star', 'evening_star', 'hammer', 'shooting_star',
                'engulfing', 'doji', 'three_black_crows', 'three_white_soldiers'
            ]
        
        logger.info(f"Multi-pattern scan starting for {len(symbols)} stocks")
        logger.info(f"Patterns to detect: {patterns}")
        
        # Fetch data for all stocks
        stocks_data = self.data_fetcher.get_multiple_stocks_data(
            symbols, 
            period='6mo'  # Get enough history for pattern context
        )
        
        if not stocks_data:
            logger.error("No stock data retrieved")
            return {}
        
        # Scan for each pattern
        all_results = {}
        total_patterns_found = 0
        
        for pattern in patterns:
            try:
                logger.info(f"Scanning for {pattern} pattern...")
                results = self.pattern_detector.scan_stocks_for_pattern(
                    stocks_data, pattern, lookback_days
                )
                
                if results:
                    all_results[pattern] = results
                    total_patterns_found += len(results)
                    logger.info(f"Found {len(results)} {pattern} patterns")
                else:
                    logger.info(f"No {pattern} patterns found")
                    
            except Exception as e:
                logger.error(f"Error scanning for {pattern}: {e}")
                continue
        
        logger.info(f"Multi-pattern scan completed: {total_patterns_found} total patterns found")
        return all_results
    
    def scan_single_pattern(self, symbols: List[str], pattern: str, 
                           lookback_days: int = 30) -> List[Dict]:
        """
        Scan stocks for a single pattern (legacy compatibility).
        
        Args:
            symbols: List of stock symbols to scan
            pattern: Pattern name to detect
            lookback_days: Number of days to look back
            
        Returns:
            List of pattern detection results
        """
        logger.info(f"Single pattern scan for {pattern}")
        
        # Fetch stock data
        stocks_data = self.data_fetcher.get_multiple_stocks_data(symbols, '6mo')
        
        if not stocks_data:
            logger.error("No stock data retrieved")
            return []
        
        # Detect patterns
        results = self.pattern_detector.scan_stocks_for_pattern(
            stocks_data, pattern, lookback_days
        )
        
        return results
    
    def run_comprehensive_scan(self, stock_file: str = 'sample_stocks.txt',
                              patterns: List[str] = None,
                              min_confidence: int = 60,
                              send_email: bool = True) -> Dict:
        """
        Run a comprehensive scan with multiple patterns and send results.
        
        Args:
            stock_file: Path to stock symbols file
            patterns: List of patterns to scan (None for default set)
            min_confidence: Minimum confidence threshold for results
            send_email: Whether to send email notifications
            
        Returns:
            Dictionary with scan results and summary
        """
        scan_start_time = datetime.now()
        logger.info("=" * 60)
        logger.info("COMPREHENSIVE STOCK PATTERN SCAN STARTING")
        logger.info("=" * 60)
        
        # Load stock symbols
        symbols = self.load_stock_symbols(stock_file)
        if not symbols:
            logger.error("No valid stock symbols found")
            return {'results': {}, 'summary': {}}
        
        # Run multi-pattern scan
        all_pattern_results = self.scan_for_multiple_patterns(symbols, patterns)
        
        # Consolidate and filter results
        consolidated_results = []
        pattern_summary = {}
        
        for pattern_name, pattern_results in all_pattern_results.items():
            # Filter by confidence
            filtered_results = [
                r for r in pattern_results 
                if r.get('confidence_score', 0) >= min_confidence
            ]
            
            consolidated_results.extend(filtered_results)
            pattern_summary[pattern_name] = {
                'total_found': len(pattern_results),
                'high_confidence': len(filtered_results),
                'avg_confidence': sum(r.get('confidence_score', 0) for r in pattern_results) / len(pattern_results) if pattern_results else 0
            }
        
        # Sort all results by confidence
        consolidated_results.sort(key=lambda x: x.get('confidence_score', 0), reverse=True)
        
        # Generate overall summary
        overall_summary = self.pattern_detector.get_pattern_summary(consolidated_results)
        overall_summary['scan_duration'] = str(datetime.now() - scan_start_time)
        overall_summary['patterns_scanned'] = list(all_pattern_results.keys())
        overall_summary['pattern_breakdown'] = pattern_summary
        
        # Print results summary
        self.print_comprehensive_results(consolidated_results, overall_summary)
        
        # Send email notification
        if send_email and consolidated_results:
            self.email_system.send_pattern_alert(consolidated_results, overall_summary)
        
        # Save results
        self.save_scan_results(consolidated_results, overall_summary)
        
        scan_result = {
            'results': consolidated_results,
            'summary': overall_summary,
            'scan_timestamp': scan_start_time.isoformat(),
            'total_stocks_scanned': len(symbols)
        }
        
        logger.info("=" * 60)
        logger.info("COMPREHENSIVE SCAN COMPLETED")
        logger.info("=" * 60)
        
        return scan_result
    
    def print_comprehensive_results(self, results: List[Dict], summary: Dict):
        """Print comprehensive scan results in a formatted way."""
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE STOCK PATTERN SCAN RESULTS")
        print("=" * 80)
        
        print(f"📅 Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  Duration: {summary.get('scan_duration', 'N/A')}")
        print(f"📊 Total Patterns Found: {len(results)}")
        print(f"🔥 High Confidence (70%+): {summary.get('high_confidence_count', 0)}")
        print(f"📈 Average Confidence: {summary.get('average_confidence', 0):.1f}%")
        
        # Pattern breakdown
        print("\n📋 Pattern Breakdown:")
        print("-" * 50)
        for pattern, stats in summary.get('pattern_breakdown', {}).items():
            print(f"  {pattern.replace('_', ' ').title():20}: {stats['high_confidence']:3d} high confidence / {stats['total_found']:3d} total")
        
        if results:
            print("\n🎯 TOP PATTERN MATCHES:")
            print("-" * 80)
            print(f"{'Rank':<4} {'Symbol':<12} {'Pattern':<18} {'Conf%':<6} {'Price':<10} {'Recommendation':<20}")
            print("-" * 80)
            
            for i, result in enumerate(results[:20], 1):  # Top 20
                confidence_emoji = "🔥" if result['confidence_score'] >= 80 else "⚡" if result['confidence_score'] >= 70 else "📊"
                print(f"{i:<4} {result['symbol']:<12} {result['pattern_type']:<18} "
                      f"{result['confidence_score']:<6}% ₹{result['close_price']:<9.2f} "
                      f"{confidence_emoji} {result['recommendation']}")
        
        print("=" * 80)
    
    def save_scan_results(self, results: List[Dict], summary: Dict):
        """Save scan results to files."""
        if not results:
            return
        
        # Create results directory
        results_dir = "scan_results"
        os.makedirs(results_dir, exist_ok=True)
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save as CSV
        import pandas as pd
        df = pd.DataFrame(results)
        csv_file = os.path.join(results_dir, f"pattern_scan_{timestamp}.csv")
        df.to_csv(csv_file, index=False)
        
        # Save summary as JSON
        import json
        summary_file = os.path.join(results_dir, f"scan_summary_{timestamp}.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Results saved to {results_dir}/")
    
    def schedule_daily_scan(self, scan_time: str = "15:20", patterns: List[str] = None):
        """
        Schedule daily scans at specified time (useful for market close scanning).
        
        Args:
            scan_time: Time to run scan in HH:MM format (default: 15:20 for Indian markets)
            patterns: Patterns to scan for
        """
        logger.info(f"Scheduling daily scans at {scan_time}")
        
        def run_scheduled_scan():
            logger.info("Running scheduled pattern scan...")
            self.run_comprehensive_scan(patterns=patterns)
        
        schedule.every().monday.at(scan_time).do(run_scheduled_scan)
        schedule.every().tuesday.at(scan_time).do(run_scheduled_scan)
        schedule.every().wednesday.at(scan_time).do(run_scheduled_scan)
        schedule.every().thursday.at(scan_time).do(run_scheduled_scan)
        schedule.every().friday.at(scan_time).do(run_scheduled_scan)
        
        logger.info("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time_module.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")

def main():
    """Main CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(description='Enhanced Stock Pattern Scanner')
    
    parser.add_argument('--mode', choices=['single', 'multi', 'schedule', 'test-email'], 
                       default='multi', help='Scanning mode')
    parser.add_argument('--pattern', type=str, help='Pattern to scan for (single mode)')
    parser.add_argument('--patterns', nargs='+', help='Patterns to scan for (multi mode)')
    parser.add_argument('--stocks', type=str, default='sample_stocks.txt', 
                       help='Stock symbols file')
    parser.add_argument('--confidence', type=int, default=60, 
                       help='Minimum confidence threshold')
    parser.add_argument('--no-email', action='store_true', 
                       help='Disable email notifications')
    parser.add_argument('--schedule-time', type=str, default='15:20',
                       help='Time for scheduled scans (HH:MM)')
    parser.add_argument('--lookback', type=int, default=30,
                       help='Days to look back for patterns')
    
    args = parser.parse_args()
    
    # Initialize scanner
    scanner = EnhancedStockPatternScanner()
    
    try:
        if args.mode == 'test-email':
            # Test email configuration
            success = scanner.email_system.test_email_configuration()
            sys.exit(0 if success else 1)
            
        elif args.mode == 'single':
            # Single pattern scan
            if not args.pattern:
                print("Error: --pattern required for single mode")
                sys.exit(1)
            
            symbols = scanner.load_stock_symbols(args.stocks)
            results = scanner.scan_single_pattern(symbols, args.pattern, args.lookback)
            
            if results and not args.no_email:
                summary = scanner.pattern_detector.get_pattern_summary(results)
                scanner.email_system.send_pattern_alert(results, summary)
                
        elif args.mode == 'multi':
            # Multi-pattern comprehensive scan
            scanner.run_comprehensive_scan(
                stock_file=args.stocks,
                patterns=args.patterns,
                min_confidence=args.confidence,
                send_email=not args.no_email
            )
            
        elif args.mode == 'schedule':
            # Scheduled scanning
            scanner.schedule_daily_scan(args.schedule_time, args.patterns)
            
    except KeyboardInterrupt:
        logger.info("Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error during scan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
