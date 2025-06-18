"""
Enhanced email notification system for stock pattern alerts.
Includes HTML formatting, confidence-based recommendations, and secure configuration.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailNotificationSystem:
    """Enhanced email notification system with HTML formatting and better security."""
    
    def __init__(self, email_config: Dict = None):
        """
        Initialize email system with configuration.
        
        Args:
            email_config: Email configuration dictionary
        """
        self.config = email_config or self.get_default_config()
        self.validate_config()
    
    def get_default_config(self) -> Dict:
        """Get default email configuration from environment variables."""
        return {
            'enabled': os.getenv('EMAIL_ENABLED', 'False').lower() == 'true',
            'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
            'smtp_port': int(os.getenv('SMTP_PORT', '587')),
            'sender_email': os.getenv('SENDER_EMAIL', ''),
            'sender_password': os.getenv('SENDER_PASSWORD', ''),  # Use App Password for Gmail
            'recipient_email': os.getenv('RECIPIENT_EMAIL', ''),
            'send_summary_only': os.getenv('SEND_SUMMARY_ONLY', 'False').lower() == 'true',
            'min_confidence_threshold': int(os.getenv('MIN_CONFIDENCE_THRESHOLD', '60'))
        }
    
    def validate_config(self):
        """Validate email configuration."""
        required_fields = ['sender_email', 'sender_password', 'recipient_email']
        
        if not self.config.get('enabled', False):
            logger.info("Email notifications are disabled")
            return
            
        for field in required_fields:
            if not self.config.get(field):
                logger.warning(f"Email configuration missing: {field}")
                self.config['enabled'] = False
                return
        
        logger.info("Email configuration validated successfully")
    
    def send_pattern_alert(self, results: List[Dict], scan_summary: Dict) -> bool:
        """
        Send enhanced email alert with pattern detection results.
        
        Args:
            results: List of pattern detection results
            scan_summary: Summary statistics from the scan
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.config.get('enabled', False):
            logger.info("Email notifications disabled - skipping alert")
            return False
            
        if not results:
            logger.info("No patterns found - skipping email alert")
            return False
        
        # Filter results by confidence threshold
        filtered_results = [
            r for r in results 
            if r.get('confidence_score', 0) >= self.config.get('min_confidence_threshold', 60)
        ]
        
        if not filtered_results:
            logger.info(f"No patterns meet confidence threshold of {self.config.get('min_confidence_threshold', 60)}% - skipping email")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['recipient_email']
            
            high_confidence_count = len([r for r in filtered_results if r.get('confidence_score', 0) >= 70])
            msg['Subject'] = f"🚨 Stock Pattern Alert: {len(filtered_results)} patterns found ({high_confidence_count} high confidence)"
            
            # Create both plain text and HTML versions
            text_body = self.create_text_body(filtered_results, scan_summary)
            html_body = self.create_html_body(filtered_results, scan_summary)
            
            # Attach both versions
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            self.send_email(msg)
            logger.info(f"Email alert sent successfully for {len(filtered_results)} patterns")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False
    
    def create_text_body(self, results: List[Dict], summary: Dict) -> str:
        """Create plain text email body."""
        body = f"""
STOCK PATTERN SCANNER ALERT
===========================

Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Patterns Found: {len(results)}
High Confidence Patterns (70%+): {summary.get('high_confidence_count', 0)}
Average Confidence: {summary.get('average_confidence', 0):.1f}%

PATTERN DETAILS:
{'-' * 50}
"""
        
        for i, result in enumerate(results[:15], 1):  # Limit to top 15
            confidence_emoji = "🔥" if result['confidence_score'] >= 80 else "⚡" if result['confidence_score'] >= 70 else "📊"
            
            body += f"""
{i}. {confidence_emoji} {result['symbol']} - {result['pattern_type'].upper()}
   Confidence: {result['confidence_score']}% | Strength: {result['pattern_strength']}
   Price: ₹{result['close_price']:.2f} | Volume: {result['volume']:,}
   Date: {result['pattern_date']} | Recommendation: {result['recommendation']}
   {'-' * 40}
"""
        
        if len(results) > 15:
            body += f"\n... and {len(results) - 15} more patterns\n"
        
        body += f"""

TRADING RECOMMENDATIONS:
{'-' * 25}
• High confidence patterns (70%+): Consider for immediate action
• Medium confidence patterns (50-69%): Monitor closely
• Always verify with additional technical analysis
• Set appropriate stop-losses based on pattern characteristics

Happy Trading! 📈
        """
        
        return body
    
    def create_html_body(self, results: List[Dict], summary: Dict) -> str:
        """Create HTML email body with styling."""
        
        # CSS styles
        styles = """
        <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #ffffff;
        color: #000000;
        margin: 0;
        padding: 20px;
    }

    .container {
        max-width: 800px;
        margin: 0 auto;
        background-color: #ffffff;
        border: 1px solid #000000;
        border-radius: 8px;
    }

    .header {
        background-color: #000000;
        color: #ffffff;
        padding: 20px;
        border-radius: 8px 8px 0 0;
        text-align: center;
    }

    .summary {
        padding: 20px;
        border-bottom: 1px solid #000000;
        background-color: #ffffff;
    }

    .pattern-list {
        padding: 20px;
    }

    .pattern-item {
        border: 1px solid #000000;
        border-radius: 5px;
        margin: 10px 0;
        padding: 15px;
        background-color: #ffffff;
    }

    .pattern-item.high {
        border-left: 5px solid #008000; /* Green */
    }

    .pattern-item.medium {
        border-left: 5px solid #0000ff; /* Blue */
    }

    .pattern-item.low {
        border-left: 5px solid #ff0000; /* Red */
    }

    .pattern-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }

    .symbol {
        font-size: 18px;
        font-weight: bold;
        color: #000000;
    }

    .confidence {
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        color: #ffffff;
    }

    .confidence.high {
        background-color: #008000; /* Green */
    }

    .confidence.medium {
        background-color: #0000ff; /* Blue */
    }

    .confidence.low {
        background-color: #ff0000; /* Red */
    }

    .pattern-details {
        color: #000000;
        font-size: 14px;
    }

    .recommendation {
        margin-top: 10px;
        padding: 8px 12px;
        border-radius: 4px;
        font-weight: bold;
    }

    .recommendation.buy {
        background-color: #d4f5d4; /* Light greenish */
        color: #006400; /* Dark green */
        border: 1px solid #008000;
    }

    .recommendation.sell {
        background-color: #fcdcdc; /* Light red */
        color: #8b0000; /* Dark red */
        border: 1px solid #ff0000;
    }

    .footer {
        padding: 20px;
        background-color: #000000;
        color: #ffffff;
        border-radius: 0 0 8px 8px;
        text-align: center;
    }

    .stats {
        display: flex;
        justify-content: space-around;
        margin: 15px 0;
    }

    .stat {
        text-align: center;
    }

    .stat-value {
        font-size: 22px;
        font-weight: bold;
        color: #0000ff; /* Blue */
    }

    .stat-label {
        font-size: 13px;
        color: #000000;
    }
</style>
        """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Stock Pattern Alert</title>
            {styles}
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚨 Stock Pattern Scanner Alert</h1>
                    <h2>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>
                </div>
                
                <div class="summary">
                    <h3>📊 Scan Summary</h3>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-value">{len(results)}</div>
                            <div class="stat-label">Total Patterns</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{summary.get('high_confidence_count', 0)}</div>
                            <div class="stat-label">High Confidence</div>
                        </div>
                        <div class="stat">
                            <div class="stat-value">{summary.get('average_confidence', 0):.1f}%</div>
                            <div class="stat-label">Avg Confidence</div>
                        </div>
                    </div>
                </div>
                
                <div class="pattern-list">
                    <h3>🎯 Pattern Details</h3>
        """
        
        for i, result in enumerate(results[:15], 1):
            confidence = result['confidence_score']
            confidence_class = 'high' if confidence >= 70 else 'medium' if confidence >= 50 else 'low'
            confidence_emoji = "🔥" if confidence >= 80 else "⚡" if confidence >= 70 else "📊"
            
            recommendation_class = 'buy' if 'BUY' in result['recommendation'] else 'sell'
            
            html += f"""
                    <div class="pattern-item {confidence_class}">
                        <div class="pattern-header">
                            <span class="symbol">{confidence_emoji} {result['symbol']}</span>
                            <span class="confidence {confidence_class}">{confidence}% Confidence</span>
                        </div>
                        <div class="pattern-details">
                            <strong>Pattern:</strong> {result['pattern_type'].replace('_', ' ').title()} | 
                            <strong>Date:</strong> {result['pattern_date']} | 
                            <strong>Price:</strong> ₹{result['close_price']:.2f} | 
                            <strong>Volume:</strong> {result['volume']:,}
                        </div>
                        <div class="recommendation {recommendation_class}">
                            📈 {result['recommendation']}
                        </div>
                    </div>
            """
        
        if len(results) > 15:
            html += f'<p><em>... and {len(results) - 15} more patterns</em></p>'
        
        html += """
                </div>
                
                <div class="footer">
                    <h4>⚠️ Trading Guidelines</h4>
                    <p>• High confidence patterns (70%+): Consider for immediate action<br>
                    • Always verify with additional technical analysis<br>
                    • Set appropriate stop-losses • Risk management is key</p>
                    <p><strong>Happy Trading! 📈</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email(self, msg: MIMEMultipart):
        """Send email using configured SMTP settings."""
        try:
            # Use SMTP_SSL for port 465, otherwise use SMTP with starttls for port 587
            if self.config['smtp_port'] == 465:
                server = smtplib.SMTP_SSL(self.config['smtp_server'], self.config['smtp_port'])
            else:
                server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
                server.starttls()
            
            server.login(self.config['sender_email'], self.config['sender_password'])
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            logger.error(f"SMTP error: {e}")
            raise
    
    def test_email_configuration(self) -> bool:
        """Test email configuration by sending a test email."""
        if not self.config.get('enabled', False):
            print("❌ Email notifications are disabled")
            return False
            
        try:
            msg = MIMEText("This is a test email from your Stock Pattern Scanner. Configuration is working correctly!")
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['recipient_email']
            msg['Subject'] = "📧 Stock Pattern Scanner - Test Email"
            
            self.send_email(msg)
            print("✅ Test email sent successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Test email failed: {e}")
            return False

def setup_email_config():
    """Interactive setup for email configuration."""
    print("\n📧 Email Configuration Setup")
    print("=" * 40)
    
    config = {}
    
    # Basic settings
    config['enabled'] = input("Enable email notifications? (y/n): ").lower().startswith('y')
    
    if not config['enabled']:
        return config
    
    config['sender_email'] = input("Enter your Gmail address: ")
    config['sender_password'] = input("Enter your Gmail App Password: ")
    config['recipient_email'] = input("Enter recipient email address: ")
    
    # Advanced settings with defaults
    config['smtp_server'] = input("SMTP Server (default: smtp.gmail.com): ") or "smtp.gmail.com"
    config['smtp_port'] = int(input("SMTP Port (default: 587): ") or "587")
    config['min_confidence_threshold'] = int(input("Minimum confidence threshold % (default: 60): ") or "60")
    
    return config

def create_env_file(config: Dict):
    """Create .env file with email configuration."""
    env_content = f"""# Stock Pattern Scanner Email Configuration
EMAIL_ENABLED={str(config.get('enabled', False)).lower()}
SMTP_SERVER={config.get('smtp_server', 'smtp.gmail.com')}
SMTP_PORT={config.get('smtp_port', 587)}
SENDER_EMAIL={config.get('sender_email', '')}
SENDER_PASSWORD={config.get('sender_password', '')}
RECIPIENT_EMAIL={config.get('recipient_email', '')}
MIN_CONFIDENCE_THRESHOLD={config.get('min_confidence_threshold', 60)}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Email configuration saved to .env file")
    print("⚠️  Keep your .env file secure and don't share it!")

if __name__ == "__main__":
    # Interactive setup
    config = setup_email_config()
    create_env_file(config)
    
    # Test configuration
    if config.get('enabled', False):
        email_system = EmailNotificationSystem(config)
        email_system.test_email_configuration()
