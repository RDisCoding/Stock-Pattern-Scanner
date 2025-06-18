# Now let's create a fixed version of the enhanced_stock_scanner.py with better email integration
fixed_scanner_init = '''    def __init__(self, email_config: Dict = None):
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
'''

print("📝 Enhanced scanner initialization method:")
print(fixed_scanner_init)

# Let's also create a configuration helper function
config_helper = '''
def create_email_config_from_json(config_file='config.json'):
    """Helper function to create email config from config.json file."""
    if not os.path.exists(config_file):
        return None
    
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            if 'notification' in config_data and 'email' in config_data['notification']:
                return config_data['notification']['email']
    except Exception as e:
        logger.error(f"Error loading email config from {config_file}: {e}")
    
    return None
'''

print("\\n📝 Configuration helper function:")
print(config_helper)