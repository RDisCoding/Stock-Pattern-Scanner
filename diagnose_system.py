#!/usr/bin/env python3
"""
Stock Pattern Scanner - System Diagnostic Tool
This script checks your system setup and identifies configuration issues.
"""

import os
import sys
import json
import importlib
from datetime import datetime

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def check_dependencies():
    """Check if all required dependencies are installed."""
    print_header("DEPENDENCY CHECK")

    dependencies = {
        'yfinance': 'Market data fetching',
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computations',
        'talib': 'Technical analysis patterns',
        'schedule': 'Task scheduling',
        'smtplib': 'Email functionality (built-in)',
        'email': 'Email composition (built-in)',
        'json': 'Configuration parsing (built-in)'
    }

    results = {}
    for package, description in dependencies.items():
        try:
            if package in ['smtplib', 'email', 'json']:
                # Built-in modules
                importlib.import_module(package)
                results[package] = {"status": "✅", "version": "built-in"}
            else:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'unknown')
                results[package] = {"status": "✅", "version": version}
            print(f"✅ {package:12} {version:10} - {description}")
        except ImportError:
            results[package] = {"status": "❌", "version": "not installed"}
            print(f"❌ {package:12} {'MISSING':10} - {description}")

    missing = [pkg for pkg, info in results.items() if info["status"] == "❌"]
    if missing:
        print(f"\n⚠️ Missing dependencies: {', '.join(missing)}")
        print("💡 Run: pip install " + " ".join(missing))
    else:
        print("\n🎉 All dependencies are installed!")

    return len(missing) == 0

def check_project_files():
    """Check if all required project files exist."""
    print_header("PROJECT FILES CHECK")

    required_files = {
        'config.json': 'Main configuration file',
        'enhanced_stock_scanner.py': 'Main scanner module',
        'enhanced_email_system.py': 'Email notification system',
        'enhanced_pattern_detector.py': 'Pattern detection engine',
        'data_fetcher.py': 'Market data fetcher',
        'config_local.py': 'Local configuration module',
        'sample_stocks.txt': 'Stock symbols list',
        'requirements.txt': 'Python dependencies list'
    }

    optional_files = {
        'fixed_quick_start.py': 'Fixed quick start script',
        'setup_email.py': 'Email setup wizard',
        '.env': 'Environment variables file'
    }

    missing_required = []
    for file, description in required_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file:30} ({size:,} bytes) - {description}")
        else:
            print(f"❌ {file:30} {'MISSING':>12}  - {description}")
            missing_required.append(file)

    print("\n📄 Optional Files:")
    for file, description in optional_files.items():
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file:30} ({size:,} bytes) - {description}")
        else:
            print(f"⚪ {file:30} {'optional':>12}  - {description}")

    if missing_required:
        print(f"\n⚠️ Missing required files: {', '.join(missing_required)}")
        return False
    else:
        print("\n🎉 All required project files are present!")
        return True

def check_email_configuration():
    """Check email configuration in all possible locations."""
    print_header("EMAIL CONFIGURATION CHECK")

    email_configs = []

    # Check config.json
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                config_data = json.load(f)
                if 'notification' in config_data and 'email' in config_data['notification']:
                    email_config = config_data['notification']['email']
                    email_configs.append(("config.json", email_config))
                    print("✅ Email configuration found in config.json")

                    # Validate required fields
                    required_fields = ['enabled', 'sender_email', 'sender_password', 'recipient_email']
                    for field in required_fields:
                        if field in email_config and email_config[field]:
                            if field == 'sender_password':
                                print(f"✅   {field}: *** (hidden)")
                            else:
                                print(f"✅   {field}: {email_config[field]}")
                        else:
                            print(f"❌   {field}: missing or empty")
                else:
                    print("⚠️ config.json exists but no email configuration found")
        except Exception as e:
            print(f"❌ Error reading config.json: {e}")
    else:
        print("⚪ config.json not found")

    # Check environment variables
    env_vars = ['EMAIL_ENABLED', 'SENDER_EMAIL', 'SENDER_PASSWORD', 'RECIPIENT_EMAIL']
    env_config = {}

    print("\n🌍 Environment Variables:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            env_config[var] = value
            if 'PASSWORD' in var:
                print(f"✅   {var}: *** (hidden)")
            else:
                print(f"✅   {var}: {value}")
        else:
            print(f"⚪   {var}: not set")

    if env_config:
        email_configs.append(("environment variables", env_config))

    # Check .env file
    if os.path.exists('.env'):
        print("\n📄 .env file found:")
        try:
            with open('.env', 'r') as f:
                env_content = f.read()
                if 'EMAIL_ENABLED' in env_content:
                    print("✅ Email configuration found in .env file")
                else:
                    print("⚠️ .env file exists but no email configuration")
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    else:
        print("\n⚪ .env file not found")

    if not email_configs:
        print("\n❌ No email configuration found!")
        print("💡 Run: python setup_email.py to configure email")
        return False
    else:
        print(f"\n🎉 Found {len(email_configs)} email configuration(s)")
        return True

def check_stock_list():
    """Check stock list configuration."""
    print_header("STOCK LIST CHECK")

    stock_files = ['sample_stocks.txt', 'stocks.txt']

    for file in stock_files:
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    lines = f.readlines()
                    symbols = [line.strip() for line in lines if line.strip() and not line.startswith('#')]

                print(f"✅ {file} found with {len(symbols)} symbols")
                print("   Sample symbols:")
                for symbol in symbols[:5]:
                    print(f"   • {symbol}")
                if len(symbols) > 5:
                    print(f"   ... and {len(symbols) - 5} more")

                # Check for Indian stock suffixes
                indian_stocks = [s for s in symbols if '.NS' in s or '.BO' in s]
                if indian_stocks:
                    print(f"   📈 {len(indian_stocks)} Indian stocks detected")
                else:
                    print("   ⚠️ No Indian stock suffixes (.NS/.BO) found")
                    print("       System will auto-add .NS suffix")

                return True

            except Exception as e:
                print(f"❌ Error reading {file}: {e}")
        else:
            print(f"⚪ {file} not found")

    print("\n❌ No stock list file found!")
    print("💡 Create sample_stocks.txt with your preferred stock symbols")
    return False

def check_data_fetching():
    """Test data fetching functionality."""
    print_header("DATA FETCHING TEST")

    try:
        # Test import
        from data_fetcher import DataFetcher
        print("✅ DataFetcher module imported successfully")

        # Test data fetching with a sample stock
        fetcher = DataFetcher()
        print("✅ DataFetcher initialized")

        # Test with a reliable Indian stock
        test_symbol = "RELIANCE.NS"
        print(f"🧪 Testing data fetch for {test_symbol}...")

        data = fetcher.get_stock_data(test_symbol, period="5d")
        if data is not None and not data.empty:
            print(f"✅ Successfully fetched {len(data)} days of data")
            print(f"   Latest close price: ₹{data['Close'].iloc[-1]:.2f}")
            print(f"   Latest volume: {data['Volume'].iloc[-1]:,}")
            return True
        else:
            print("❌ No data retrieved")
            return False

    except Exception as e:
        print(f"❌ Data fetching test failed: {e}")
        return False

def test_pattern_detection():
    """Test pattern detection functionality."""
    print_header("PATTERN DETECTION TEST")

    try:
        from enhanced_pattern_detector import PatternDetector
        print("✅ PatternDetector module imported successfully")

        detector = PatternDetector()
        print("✅ PatternDetector initialized")
        print(f"   Available patterns: {len(detector.supported_patterns)}")

        # Show some patterns
        patterns = list(detector.supported_patterns.keys())[:5]
        print(f"   Sample patterns: {', '.join(patterns)}")

        return True

    except Exception as e:
        print(f"❌ Pattern detection test failed: {e}")
        return False

def test_email_system():
    """Test email system functionality."""
    print_header("EMAIL SYSTEM TEST")

    try:
        from enhanced_email_system import EmailNotificationSystem
        print("✅ EmailNotificationSystem module imported successfully")

        # Initialize with default config
        email_system = EmailNotificationSystem()
        print("✅ EmailNotificationSystem initialized")
        print(f"   Email enabled: {email_system.config.get('enabled', False)}")

        if email_system.config.get('enabled', False):
            sender = email_system.config.get('sender_email', 'Not configured')
            recipient = email_system.config.get('recipient_email', 'Not configured')
            print(f"   From: {sender}")
            print(f"   To: {recipient}")

            # Test email sending capability
            test_send = input("\n🧪 Send test email? (y/n): ").strip().lower()
            if test_send == 'y':
                try:
                    # Create dummy results for testing
                    test_results = [{
                        'symbol': 'TEST.NS',
                        'pattern_type': 'morning_star',
                        'confidence_score': 75,
                        'pattern_date': datetime.now().strftime('%Y-%m-%d'),
                        'close_price': 100.50,
                        'recommendation': 'Strong BUY Signal'
                    }]

                    test_summary = {
                        'total_patterns': 1,
                        'high_confidence_count': 1,
                        'average_confidence': 75.0
                    }

                    success = email_system.send_pattern_alert(test_results, test_summary)
                    if success:
                        print("✅ Test email sent successfully!")
                    else:
                        print("❌ Test email failed to send")
                        return False

                except Exception as e:
                    print(f"❌ Email test error: {e}")
                    return False
        else:
            print("⚠️ Email is disabled in configuration")

        return True

    except Exception as e:
        print(f"❌ Email system test failed: {e}")
        return False

def generate_report():
    """Generate a comprehensive diagnostic report."""
    print_header("SYSTEM DIAGNOSTIC REPORT")
    print(f"🕒 Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python Version: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")

    # Run all checks
    checks = {
        "Dependencies": check_dependencies(),
        "Project Files": check_project_files(),
        "Email Configuration": check_email_configuration(),
        "Stock List": check_stock_list(),
        "Data Fetching": check_data_fetching(),
        "Pattern Detection": test_pattern_detection(),
        "Email System": test_email_system()
    }

    # Summary
    print_header("DIAGNOSTIC SUMMARY")

    passed = sum(checks.values())
    total = len(checks)

    for check_name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")

    print(f"\n📊 Overall Score: {passed}/{total} ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 SYSTEM READY!")
        print("Your stock pattern scanner is properly configured and ready to use.")
        print("\n🚀 Next Steps:")
        print("   python fixed_quick_start.py")
    else:
        print("\n⚠️ ISSUES DETECTED")
        print("Please fix the failed checks above before using the scanner.")
        print("\n💡 Common Solutions:")
        print("   • Install missing dependencies: pip install -r requirements.txt")
        print("   • Configure email: python setup_email.py")
        print("   • Create stock list: sample_stocks.txt")

if __name__ == "__main__":
    generate_report()