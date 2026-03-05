"""
Configuration management for the WhatsApp Reporter
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Manages application configuration."""
    
    CONFIG_DIR = Path.home() / '.whatsapp_reporter'
    CONFIG_FILE = CONFIG_DIR / 'config.json'
    
    DEFAULT_CONFIG = {
        'phone': '',
        'language': 'en',
        'log_level': 'INFO',
        'report_delay': 2,
        'batch_enabled': True,
        'auto_backup': True
    }
    
    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = self.CONFIG_DIR
        self.config_file = self.CONFIG_FILE
        self._ensure_config_exists()
        self.config = self._load_config()
    
    def _ensure_config_exists(self):
        """Ensure config directory and file exist."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            if not self.config_file.exists():
                self._save_config(self.DEFAULT_CONFIG)
                logger.info(f'Created default configuration at {self.config_file}')
        
        except Exception as e:
            logger.error(f'Error creating config directory: {str(e)}')
    
    def _load_config(self) -> dict:
        """Load configuration from file."""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                logger.info('Configuration loaded successfully')
                return config
        
        except json.JSONDecodeError:
            logger.warning('Invalid JSON in config file, using defaults')
            return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f'Error loading config: {str(e)}')
            return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: dict):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
                logger.info('Configuration saved')
        
        except Exception as e:
            logger.error(f'Error saving config: {str(e)}')
    
    def set_value(self, key: str, value) -> bool:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        
        Returns:
            bool: True if successful
        """
        try:
            self.config[key] = value
            self._save_config(self.config)
            return True
        except Exception as e:
            logger.error(f'Error setting config value: {str(e)}')
            return False
    
    def get_value(self, key: str):
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
        
        Returns:
            Configuration value or None if not found
        """
        return self.config.get(key)
    
    def get_all(self) -> dict:
        """
        Get all configuration values.
        
        Returns:
            dict: All configuration
        """
        return self.config.copy()
    
    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to defaults.
        
        Returns:
            bool: True if successful
        """
        try:
            self.config = self.DEFAULT_CONFIG.copy()
            self._save_config(self.config)
            logger.info('Configuration reset to defaults')
            return True
        except Exception as e:
            logger.error(f'Error resetting config: {str(e)}')
            return False