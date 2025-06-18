#!/usr/bin/env python3
"""
Email Configuration Setup Wizard for Stock Pattern Scanner
This script helps you configure email notifications properly.
"""

import json
import os
import getpass
from enhanced_email_system import EmailNotificationSystem

def setup_email_wizard():
    """Interactive wizard to set up email configuration."""
    print("📧 Email Configuration Setup Wizard")
    print("=" * 50)
    print()

    print("This wizard will help you configure email notifications for your stock pattern scanner.")
    print("You'll need:")
    print("• Gmail account with 2-Factor Authentication enabled")
    print("• Gmail App Password (16 characters)")
    print()

    # Get email configuration from user
    email_config = {}

    print("📝 Enter your email settings:")
    print()

    # Sender email
    sender_email = input("📧 Your Gmail address: ").strip()
    if not sender_email.endswith('@gmail.com'):
        print("⚠️ Warning: This system is configured for Gmail. Other providers may not work.")

    # App password
    print("\n🔑 Gmail App Password:")
    print("   1. Go to Google Account Settings")
    print("   2. Security → 2-Step Verification → App passwords")
    print("   3. Generate a new app password")
    sender_password = getpass.getpass("   Enter 16-character app password: ").strip()

    # Recipient email
    recipient_email = input("\n📨 Email address to receive alerts: ").strip()

    # Additional settings
    print("\n⚙️ Additional Settings:")
    min_confidence = input("   Minimum confidence threshold (60-80, default 65): ").strip()
    if not min_confidence.isdigit():
        min_confidence = "65"

    # Build configuration
    email_config = {
        "enabled": True,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": sender_email,
        "sender_password": sender_password,
        "recipient_email": recipient_email,
        "min_confidence_threshold": int(min_confidence)
    }

    # Test the configuration
    print("\n🧪 Testing email configuration...")
    test_email_system = EmailNotificationSystem(email_config)

    try:
        # Create a test message
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        import smtplib

        msg = MIMEMultipart()
        msg['From'] = email_config['sender_email']
        msg['To'] = email_config['recipient_email']
        msg['Subject'] = "🧪 Stock Pattern Scanner - Test Email"

        body = f"""
        ✅ Email Configuration Test Successful!

        Your stock pattern scanner email notifications are now configured.

        Settings:
        • From: {email_config['sender_email']}
        • To: {email_config['recipient_email']}
        • Min Confidence: {email_config['min_confidence_threshold']}%

        You will receive pattern alerts when the scanner detects
        high-confidence trading opportunities.

        Happy Trading! 📈
        """

        msg.attach(MIMEText(body, 'plain'))

        # Send test email
        server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        server.starttls()
        server.login(email_config['sender_email'], email_config['sender_password'])
        text = msg.as_string()
        server.sendmail(email_config['sender_email'], email_config['recipient_email'], text)
        server.quit()

        print("✅ Test email sent successfully!")

    except Exception as e:
        print(f"❌ Email test failed: {e}")
        print("\nCommon issues:")
        print("• Incorrect app password (should be 16 characters)")
        print("• 2-Factor Authentication not enabled")
        print("• Less secure app access enabled (should be disabled)")
        return False

    # Save configuration
    save_config = input("\n💾 Save this configuration to config.json? (y/n): ").strip().lower()

    if save_config == 'y':
        try:
            # Load existing config or create new one
            config_data = {}
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config_data = json.load(f)

            # Update email configuration
            if 'notification' not in config_data:
                config_data['notification'] = {}
            config_data['notification']['email'] = email_config

            # Save to file
            with open('config.json', 'w') as f:
                json.dump(config_data, f, indent=2)

            print("✅ Configuration saved to config.json")

        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False

    # Also save as environment variables option
    save_env = input("\n🌍 Create .env file for environment variables? (y/n): ").strip().lower()

    if save_env == 'y':
        env_content = f"""# Stock Pattern Scanner Email Configuration
EMAIL_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL={email_config['sender_email']}
SENDER_PASSWORD={email_config['sender_password']}
RECIPIENT_EMAIL={email_config['recipient_email']}
MIN_CONFIDENCE_THRESHOLD={email_config['min_confidence_threshold']}
"""

        with open('.env', 'w') as f:
            f.write(env_content)

        print("✅ Environment variables saved to .env file")

    print("\n🎉 Email configuration complete!")
    print("\n🚀 You can now run the scanner with email notifications:")
    print("   python quick_start.py")
    print("   python enhanced_stock_scanner.py")

    return True

if __name__ == "__main__":
    setup_email_wizard()