# Enhanced Stock Pattern Scanner Setup Guide

## 🚀 Features

Your enhanced stock pattern scanner now includes:

### 📊 Pattern Detection
- **15+ Candlestick Patterns** from Zerodha Varsity
- **Single Patterns**: Marubozu, Doji, Hammer, Shooting Star, Spinning Top, etc.
- **Multiple Patterns**: Morning Star, Evening Star, Engulfing, Harami, Three Black Crows, etc.
- **Confidence Scoring**: 0-100% reliability scores based on market research
- **Indian Stock Support**: Automatic .NS/.BO suffix handling

### 📧 Email Notifications
- **HTML Formatted Emails** with professional styling
- **Confidence-based Filtering** (only high-quality patterns)
- **Trading Recommendations** for each pattern
- **Secure Gmail Integration** with App Passwords

### ⚙️ Automation Features
- **Multi-pattern Scanning** in a single run
- **Scheduled Scanning** (run before market close)
- **Real-time Data Fetching** with yfinance
- **Comprehensive Logging** and result saving

## 📋 Installation Requirements

```bash
# Install required Python packages
pip install -r requirements.txt

# Additional requirements for enhanced features
pip install schedule python-dotenv
```

### 📄 requirements.txt
```
yfinance>=0.2.25
pandas>=1.5.0
numpy>=1.24.0
TA-Lib>=0.4.28
schedule>=1.2.0
python-dotenv>=1.0.0
```

## 🔧 Setup Instructions

### 1. Install TA-Lib

**Windows:**
```bash
# Download TA-Lib wheel for your Python version from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl
```

**macOS:**
```bash
brew install ta-lib
pip install TA-Lib
```

**Linux:**
```bash
sudo apt-get install build-essential
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install TA-Lib
```

### 2. Configure Email (Gmail)

1. **Enable 2-Factor Authentication** in your Google Account
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification
   - App passwords → Generate password
   - Save this 16-character password

3. **Run Email Setup**:
```bash
python enhanced_email_system.py
```

### 3. Set Up Stock List

Create `sample_stocks.txt` with your preferred stocks:
```
# Indian Stocks (NSE)
RELIANCE.NS
TCS.NS
INFY.NS
HDFCBANK.NS
ICICIBANK.NS

# Or just use symbols (auto-adds .NS)
TATAMOTORS
WIPRO
ITC
```

## 🎯 Usage Examples

### Quick Multi-Pattern Scan
```bash
# Run comprehensive scan with default patterns
python enhanced_stock_scanner.py

# Scan specific patterns
python enhanced_stock_scanner.py --patterns morning_star evening_star hammer

# Set minimum confidence threshold
python enhanced_stock_scanner.py --confidence 70
```

### Single Pattern Scan (Legacy Mode)
```bash
# Scan for morning star only
python enhanced_stock_scanner.py --mode single --pattern morning_star

# Scan with custom stock list
python enhanced_stock_scanner.py --mode single --pattern hammer --stocks my_stocks.txt
```

### Scheduled Scanning
```bash
# Schedule daily scans at 3:20 PM (before market close)
python enhanced_stock_scanner.py --mode schedule --schedule-time 15:20

# Schedule with specific patterns
python enhanced_stock_scanner.py --mode schedule --patterns morning_star engulfing --schedule-time 15:25
```

### Test Email Configuration
```bash
# Test your email setup
python enhanced_stock_scanner.py --mode test-email
```

## 📊 Available Patterns

### Single Candlestick Patterns
- `marubozu` - Strong directional movement
- `doji` - Market indecision
- `hammer` - Bullish reversal (downtrend)
- `hanging_man` - Bearish reversal (uptrend)
- `shooting_star` - Bearish reversal
- `inverted_hammer` - Potential bullish reversal
- `spinning_top` - Market uncertainty
- `dragonfly_doji` - Bullish reversal
- `gravestone_doji` - Bearish reversal

### Multiple Candlestick Patterns
- `morning_star` - Strong bullish reversal
- `evening_star` - Strong bearish reversal
- `engulfing` - Trend reversal pattern
- `harami` - Potential reversal
- `piercing_pattern` - Bullish reversal
- `dark_cloud_cover` - Bearish reversal
- `three_black_crows` - Strong bearish continuation
- `three_white_soldiers` - Strong bullish continuation

## 📧 Email Configuration

Create a `.env` file in your project directory:
```bash
# Email Settings
EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=alerts@yourdomain.com
MIN_CONFIDENCE_THRESHOLD=60
```

## 🔄 Daily Workflow

### Manual Usage (Recommended)
Run a few minutes before market close:
```bash
# 3:20 PM - Run comprehensive scan
python enhanced_stock_scanner.py --confidence 65

# Review email alerts
# Make trading decisions based on high-confidence patterns
```

### Automated Usage
```bash
# Set up daily automation
python enhanced_stock_scanner.py --mode schedule --schedule-time 15:20 --confidence 70
```

## 📈 Understanding Results

### Confidence Scores
- **80-100%**: Exceptional reliability - Strong trading signals
- **70-79%**: High confidence - Good trading opportunities  
- **60-69%**: Medium confidence - Requires additional confirmation
- **50-59%**: Low confidence - Monitor only
- **<50%**: Very low confidence - Avoid trading

### Trading Recommendations
- **Strong BUY/SELL**: High confidence + favorable market conditions
- **Moderate BUY/SELL**: Medium confidence patterns
- **CONSIDER BUY/SELL**: Lower confidence, needs confirmation

## 🛠️ Troubleshooting

### Common Issues

**1. TA-Lib Installation Error**
```bash
# Try manual installation or use conda
conda install -c conda-forge ta-lib
```

**2. Email Not Sending**
- Verify App Password (not regular Gmail password)
- Check 2-Factor Authentication is enabled
- Test with: `python enhanced_stock_scanner.py --mode test-email`

**3. Indian Stocks Not Working**
- Ensure symbols have .NS suffix (auto-added if missing)
- For BSE stocks, use .BO suffix manually

**4. No Patterns Found**
- Lower confidence threshold: `--confidence 50`
- Increase lookback period: `--lookback 60`
- Check if stocks have sufficient data

### Data Sources
- **yfinance**: Real-time data from Yahoo Finance
- **Daily Timeframe**: 1-day candles for pattern detection
- **6-Month History**: Sufficient context for pattern analysis

## 🎯 Best Practices

1. **Run Before Market Close**: 15:15-15:25 for Indian markets
2. **Focus on High Confidence**: Use 70%+ threshold for trading
3. **Verify with Volume**: High volume confirms pattern strength
4. **Risk Management**: Always set stop-losses
5. **Multiple Confirmation**: Don't rely solely on patterns

## 📁 Output Files

The scanner creates:
- `pattern_scanner.log` - Detailed execution logs
- `scan_results/pattern_scan_YYYYMMDD_HHMMSS.csv` - Pattern results
- `scan_results/scan_summary_YYYYMMDD_HHMMSS.json` - Scan statistics

## 🔮 Next Steps

Your system is now ready for:
1. Daily pattern scanning
2. Automated email alerts  
3. Multiple pattern detection
4. Confidence-based filtering

Happy Trading! 📈
