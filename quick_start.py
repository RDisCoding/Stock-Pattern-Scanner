#!/usr/bin/env python3
"""
Quick Start Script for Enhanced Stock Pattern Scanner
Run this to get started immediately with default settings.
"""

import os
import sys
import json
from enhanced_stock_scanner import EnhancedStockPatternScanner

def load_email_config():
    """Load email configuration from config.json or environment variables."""
    email_config = {}
    
    # First, try to load from config.json
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                config_data = json.load(f)
                if 'notification' in config_data and 'email' in config_data['notification']:
                    email_config = config_data['notification']['email']
                    print("📧 Email configuration loaded from config.json")
                    return email_config, True
        except Exception as e:
            print(f"⚠️ Error reading config.json: {e}")
    
    # Fallback to environment variables
    env_config = {
        'enabled': os.getenv('EMAIL_ENABLED', 'false').lower() == 'true',
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'sender_email': os.getenv('SENDER_EMAIL', ''),
        'sender_password': os.getenv('SENDER_PASSWORD', ''),
        'recipient_email': os.getenv('RECIPIENT_EMAIL', ''),
        'min_confidence_threshold': int(os.getenv('MIN_CONFIDENCE_THRESHOLD', '60'))
    }
    
    # Check if environment variables are configured
    required_fields = ['sender_email', 'sender_password', 'recipient_email']
    env_configured = (env_config['enabled'] and 
                     all(env_config.get(field) for field in required_fields))
    
    if env_configured:
        print("📧 Email configuration loaded from environment variables")
        return env_config, True
    
    return {}, False

def main():
    print("🚀 Enhanced Stock Pattern Scanner - Quick Start")
    print("=" * 50)
    
    # Load email configuration
    email_config, email_configured = load_email_config()
    
    if not email_configured:
        print("📧 Email not configured properly.")
        print("💡 Options to configure email:")
        print("   1. Update config.json with your email settings")
        print("   2. Set environment variables (EMAIL_ENABLED, SENDER_EMAIL, etc.)")
        print("   3. Run: python enhanced_email_system.py for setup wizard")
        print()
        print("📊 Continuing with pattern scanning (no email alerts)...")
    else:
        print(f"✅ Email configured - alerts will be sent to {email_config.get('recipient_email', 'configured address')}")
    
    # Initialize scanner with email configuration
    print("🔍 Initializing pattern scanner...")
    try:
        scanner = EnhancedStockPatternScanner(email_config if email_configured else None)
    except Exception as e:
        print(f"❌ Error initializing scanner: {e}")
        print("💡 Check if all required dependencies are installed")
        return
    
    # Run quick scan with popular patterns
    print("📊 Running quick scan with popular patterns...")
    popular_patterns = ['morning_star', 'evening_star', 'hammer', 'shooting_star', 'engulfing']
    
    try:
        results = scanner.run_comprehensive_scan(
            patterns=popular_patterns,
            min_confidence=60,
            send_email=email_configured
        )
        
        if results['results']:
            print(f"\n✅ Found {len(results['results'])} patterns!")
            print("📁 Results saved to scan_results/ directory")
            if email_configured:
                print("📧 Email alert sent!")
        else:
            print("\n📝 No patterns found with current criteria")
            print("💡 Try lowering confidence threshold or checking more patterns")
            
    except Exception as e:
        print(f"❌ Error during scan: {e}")
        print("💡 Check the setup guide for troubleshooting tips")
        import traceback
        traceback.print_exc()
        
    print("\n🎯 Quick Start Complete!")
    print("📖 See SETUP_GUIDE.md for advanced usage")

if __name__ == "__main__":
    main()
