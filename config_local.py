"""
Configuration module for the stock pattern scanner.
"""
import json
import os
from typing import Dict, Any

class Config:
    """Configuration management class."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {self.config_file} not found. Using default values.")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}. Using default values.")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "data_source": "yahoo",
            "pattern_types": ["morning_star"],
            "scan_period": "6mo",
            "notification": {"enabled": True},
            "scan_settings": {
                "min_volume": 100000,
                "min_price": 5.0,
                "max_price": 1000.0,
                "pattern_lookback_days": 30
            },
            "output": {
                "save_results": True,
                "output_format": "csv",
                "output_directory": "scan_results"
            }
        }
    
    def get(self, key: str, default=None):
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, {})
            if not isinstance(value, dict) and k != keys[-1]:
                return default
        return value if k == keys[-1] else default
    
    def update(self, key: str, value: Any):
        """Update configuration value."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
    
    def save(self):
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
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

# Global config instance
config = Config()
