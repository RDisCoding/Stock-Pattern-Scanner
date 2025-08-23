# 📈 Stock Pattern Scanner

A comprehensive, automated stock pattern detection system built for Indian stock markets. This advanced scanner identifies 23+ candlestick patterns from Zerodha Varsity, provides confidence-based scoring, and sends automated email alerts with trading recommendations.

## 🚀 Key Features

### 📊 **Advanced Pattern Detection**
- **23+ Candlestick Patterns** including all major Zerodha Varsity patterns
- **Single Patterns**: Marubozu, Doji, Hammer, Shooting Star, Spinning Top, Inverted Hammer, etc.
- **Multi-Candle Patterns**: Morning Star, Evening Star, Engulfing, Harami, Three Black Crows, etc.
- **TA-Lib Integration** for accurate technical analysis
- **Confidence Scoring** (0-100%) based on market research and pattern reliability

### 🔔 **Smart Email Notifications**
- **HTML-formatted emails** with professional styling
- **Confidence-based filtering** (only high-quality patterns sent)
- **Trading recommendations** with BUY/SELL signals
- **Secure Gmail integration** with App Password support
- **Pattern summary** with scan statistics

### ⚡ **Automation & Scheduling**
- **Multi-pattern scanning** in a single execution
- **Scheduled daily scans** (perfect for market close analysis)
- **Real-time data fetching** using Yahoo Finance
- **Comprehensive logging** and result tracking
- **CSV/JSON output** for further analysis

### 🇮🇳 **Indian Market Optimized**
- **NSE/BSE support** with automatic .NS/.BO suffix handling
- **Large-cap stock lists** included
- **Market timing awareness** (scheduled scans at 15:20 before market close)
- **Volume and price filtering** for quality stocks

---

## 📁 Project Structure

```
📦 Stock-Pattern-Scanner/
├── 🔧 Core Modules
│   ├── enhanced_stock_scanner.py      # Main scanner with CLI interface
│   ├── enhanced_pattern_detector.py   # Pattern detection engine
│   ├── enhanced_email_system.py       # Email notification system
│   ├── data_fetcher.py               # Stock data retrieval
│   └── config_local.py               # Configuration management
│
├── ⚙️ Configuration
│   ├── config.json                   # Main configuration file
│   ├── requirements.txt              # Python dependencies
│   └── .env                         # Environment variables (created during setup)
│
├── 📊 Stock Lists
│   ├── sample_stocks.txt            # Default Indian large-cap stocks
│   ├── large_cap_stocks.txt         # Extended large-cap list
│   └── (your custom stock lists)
│
├── 📈 Results & Logs
│   ├── scan_results/                # Scan output directory
│   │   ├── pattern_scan_*.csv      # Pattern detection results
│   │   └── scan_summary_*.json     # Scan statistics
│   └── pattern_scanner.log         # Execution logs
│
├── 📚 Documentation
│   ├── README.md                    # This file
│   ├── SETUP_GUIDE.md              # Detailed setup instructions
│   └── example_usage.py            # Usage examples
│
└── 🔧 Utilities
    ├── setup_email.py              # Email configuration helper
    ├── quick_start.py              # Quick setup script
    └── diagnose_system.py          # System diagnostics
```

---

## 🛠️ Installation & Setup

### 1. **Prerequisites**
```bash
# Python 3.8+ required
python --version

# Git (for cloning)
git --version
```

### 2. **Clone Repository**
```bash
git clone https://github.com/RDisCoding/Stock-Pattern-Scanner.git
cd Stock-Pattern-Scanner
```

### 3. **Install Dependencies**
```bash
# Install required packages
pip install -r requirements.txt

# Note: TA-Lib requires additional setup on Windows
# Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
```

### 4. **Configure Email (Optional)**
```bash
# Interactive email setup
python setup_email.py

# Manual configuration - edit config.json:
{
  "notification": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "sender_email": "your-email@gmail.com",
      "sender_password": "your-app-password",
      "recipient_email": "recipient@email.com",
      "min_confidence_threshold": 65
    }
  }
}
```

---

## 🎯 Usage Examples

### **Quick Start - Multi-Pattern Scan**
```bash
# Run comprehensive scan with default patterns
python enhanced_stock_scanner.py

# Scan specific patterns
python enhanced_stock_scanner.py --patterns morning_star evening_star hammer

# Set confidence threshold
python enhanced_stock_scanner.py --confidence 70
```

### **Single Pattern Analysis**
```bash
# Focus on one pattern
python enhanced_stock_scanner.py --mode single --pattern morning_star

# Use custom stock list
python enhanced_stock_scanner.py --mode single --pattern hammer --stocks large_cap_stocks.txt
```

### **Automated Scheduling**
```bash
# Schedule daily scans at market close (3:20 PM)
python enhanced_stock_scanner.py --mode schedule --schedule-time 15:20

# Schedule with specific patterns
python enhanced_stock_scanner.py --mode schedule --patterns engulfing hammer --schedule-time 15:25
```

### **Email Testing**
```bash
# Test email configuration
python enhanced_stock_scanner.py --mode test-email
```

---

## 📊 Supported Patterns

### **Single Candlestick Patterns**
| Pattern | Reliability | Signal | Description |
|---------|-------------|--------|-------------|
| Marubozu | 65% | Trend Continuation | Long body, minimal shadows |
| Doji | 60% | Trend Reversal | Equal open/close prices |
| Hammer | 68% | Bullish Reversal | Small body, long lower shadow |
| Shooting Star | 68% | Bearish Reversal | Small body, long upper shadow |
| Spinning Top | 55% | Indecision | Small body, long shadows |
| Hanging Man | 58% | Bearish Reversal | Hammer at uptrend top |

### **Multi-Candlestick Patterns**
| Pattern | Reliability | Signal | Description |
|---------|-------------|--------|-------------|
| Three Black Crows | 78% | Strong Bearish | Three consecutive bearish candles |
| Three White Soldiers | 75% | Strong Bullish | Three consecutive bullish candles |
| Morning Star | 74% | Bullish Reversal | Three-candle bullish reversal |
| Evening Star | 72% | Bearish Reversal | Three-candle bearish reversal |
| Engulfing | 70% | Trend Reversal | Second candle engulfs first |
| Harami | 63% | Trend Reversal | Small candle inside large candle |

*And 11 more patterns with varying reliability scores...*

---

## 📧 Email Notifications

The system sends beautifully formatted HTML emails containing:

### **Email Content**
- **Scan Summary**: Total patterns found, confidence distribution
- **Top Patterns**: Highest confidence matches with recommendations
- **Pattern Breakdown**: Count by pattern type
- **Trading Signals**: Clear BUY/SELL recommendations
- **Risk Warnings**: Appropriate disclaimers

### **Sample Email Output**
```
🎯 STOCK PATTERN ALERT - 15 High-Confidence Patterns Found

📊 Scan Summary:
• Total Patterns: 47
• High Confidence (70%+): 15
• Average Confidence: 68.2%

🔥 Top Matches:
1. RELIANCE.NS - Morning Star (78%) - Strong BUY Signal
2. TCS.NS - Hammer (76%) - Moderate BUY Signal
3. INFY.NS - Engulfing (74%) - Strong BUY Signal
```

---

## 🔧 Configuration Options

### **Main Configuration (`config.json`)**
```json
{
  "data_source": "yahoo",
  "pattern_types": ["morning_star", "evening_star", "hammer"],
  "scan_period": "6mo",
  "notification": {
    "email": {
      "enabled": true,
      "min_confidence_threshold": 65
    }
  },
  "scan_settings": {
    "min_volume": 100000,
    "min_price": 5.0,
    "max_price": 1000.0,
    "pattern_lookback_days": 30
  },
  "output": {
    "save_results": true,
    "output_format": "csv",
    "output_directory": "scan_results"
  }
}
```

### **Command Line Arguments**
```bash
Options:
  --mode {single,multi,schedule,test-email}  Scanning mode
  --pattern PATTERN                          Single pattern to scan
  --patterns PATTERN [PATTERN ...]           Multiple patterns
  --stocks STOCKS                            Stock symbols file
  --confidence CONFIDENCE                    Minimum confidence (0-100)
  --no-email                                Disable email notifications
  --schedule-time TIME                       Schedule time (HH:MM)
  --lookback DAYS                           Historical days to analyze
```

---

## 📈 Output Files

### **CSV Results (`scan_results/pattern_scan_YYYYMMDD_HHMMSS.csv`)**
```csv
symbol,pattern_type,detection_date,signal_strength,confidence_score,recommendation,close_price,volume,high,low,days_since_pattern
RELIANCE.NS,morning_star,2024-08-23,100,78,Strong BUY Signal,2456.75,1234567,2465.0,2440.0,0
TCS.NS,hammer,2024-08-23,100,76,Moderate BUY Signal,3245.20,987654,3250.0,3230.0,1
```

### **JSON Summary (`scan_results/scan_summary_YYYYMMDD_HHMMSS.json`)**
```json
{
  "total_patterns_found": 47,
  "high_confidence_count": 15,
  "average_confidence": 68.2,
  "scan_duration": "0:02:45",
  "patterns_scanned": ["morning_star", "evening_star", "hammer"],
  "pattern_breakdown": {
    "morning_star": {"total_found": 12, "high_confidence": 8},
    "hammer": {"total_found": 18, "high_confidence": 5}
  }
}
```

---

## 🚀 Advanced Features

### **1. Confidence-Based Filtering**
The system uses research-backed reliability scores:
- **High Confidence (70%+)**: Strong trading signals
- **Medium Confidence (60-69%)**: Moderate signals
- **Low Confidence (<60%)**: Weak signals, use with caution

### **2. Smart Stock Selection**
- **Volume filtering**: Minimum 100K daily volume
- **Price filtering**: ₹5 - ₹1000 range
- **Market cap focus**: Large and mid-cap stocks
- **Liquidity checks**: Active trading verification

### **3. Market Timing**
- **Pre-market analysis**: Schedule at 15:20 before market close
- **Intraday patterns**: Real-time detection capability
- **Historical validation**: 30-day lookback for context

### **4. Risk Management**
- **Pattern reliability scoring**: Evidence-based confidence levels
- **Multiple confirmation**: Scan multiple patterns simultaneously
- **Volume validation**: High volume confirms pattern strength
- **Trend analysis**: Pattern context within larger trends

---

## 🛠️ Troubleshooting

### **Common Issues**

#### **1. Email Not Working**
```bash
# Check configuration
python enhanced_stock_scanner.py --mode test-email

# Verify config.json has correct email settings
# Ensure Gmail App Password (not regular password)
```

#### **2. TA-Lib Installation Error**
```bash
# Windows: Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
pip install TA_Lib-0.4.28-cp311-cp311-win_amd64.whl

# Linux/Mac:
brew install ta-lib  # Mac
sudo apt-get install libta-lib-dev  # Ubuntu
```

#### **3. No Data Retrieved**
```bash
# Check internet connection
# Verify stock symbols in your .txt file
# Ensure .NS suffix for Indian stocks
```

#### **4. Module Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.8+
```

---

## 📊 Performance & Scalability

### **Scanning Performance**
- **Speed**: ~2-3 seconds per stock per pattern
- **Capacity**: 100+ stocks in 5-10 minutes
- **Memory**: ~50MB RAM for 100 stocks
- **Storage**: ~1MB per day of results

### **Optimization Tips**
1. **Limit patterns**: Focus on 3-5 high-reliability patterns
2. **Filter stocks**: Use volume/price filters effectively
3. **Schedule wisely**: Run during low-activity periods
4. **Archive results**: Clean old scan results periodically

---

## 🤝 Contributing

### **How to Contribute**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-pattern`)
3. Commit changes (`git commit -am 'Add new pattern detection'`)
4. Push to branch (`git push origin feature/new-pattern`)
5. Create Pull Request

### **Development Setup**
```bash
# Clone for development
git clone https://github.com/RDisCoding/Stock-Pattern-Scanner.git
cd Stock-Pattern-Scanner

# Install development dependencies
pip install -r requirements.txt
pip install pytest flake8 black

# Run tests
python -m pytest tests/

# Format code
black *.py
```

---

## 📜 License & Disclaimer

### **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### **Important Disclaimer**
⚠️ **This software is for educational and research purposes only.**

- **Not Financial Advice**: Results should not be considered as financial advice
- **Risk Warning**: Trading involves substantial risk of loss
- **Validation Required**: Always validate patterns with additional analysis
- **No Guarantees**: Past performance does not guarantee future results
- **Professional Advice**: Consult qualified financial advisors before trading

---

## 📞 Support & Contact

### **Getting Help**
- **Issues**: [GitHub Issues](https://github.com/RDisCoding/Stock-Pattern-Scanner/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RDisCoding/Stock-Pattern-Scanner/discussions)
- **Documentation**: Check `SETUP_GUIDE.md` for detailed instructions

### **Feature Requests**
Have an idea for improvement? Create an issue with the `enhancement` label!

---

## 🎯 Roadmap

### **Upcoming Features**
- [ ] **Options pattern detection**
- [ ] **Sector-wise analysis**
- [ ] **Backtesting module**
- [ ] **Web dashboard interface**
- [ ] **Mobile app notifications**
- [ ] **Advanced ML pattern recognition**
- [ ] **Real-time scanning**
- [ ] **Portfolio integration**

### **Version History**
- **v1.2** - Multi-pattern scanning, email alerts
- **v1.1** - TA-Lib integration, confidence scoring
- **v1.0** - Basic pattern detection

---

## 🙏 Acknowledgments

- **Zerodha Varsity** for comprehensive pattern education
- **TA-Lib** for technical analysis functions
- **Yahoo Finance** for reliable market data
- **Python Community** for excellent libraries
- **Contributors** who help improve this project

---

## 🚀 Get Started Today!

1. **Clone the repository**
2. **Install dependencies**
3. **Configure email (optional)**
4. **Run your first scan**
5. **Start finding profitable patterns!**

```bash
git clone https://github.com/RDisCoding/Stock-Pattern-Scanner.git
cd Stock-Pattern-Scanner
pip install -r requirements.txt
python enhanced_stock_scanner.py
```

**Happy Pattern Hunting! 📈**

---

*Made with ❤️ for the trading community*
