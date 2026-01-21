"""
Configuration management for the trading bot
"""
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional


class Config:
    """Manages bot configuration from environment variables and YAML files"""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration

        Args:
            config_file: Path to YAML configuration file (default: config.yaml)
        """
        # Load environment variables
        load_dotenv()

        # API Configuration
        self.api_key = os.getenv('SWARM_VAULT_API_KEY')
        self.base_url = os.getenv('SWARM_VAULT_BASE_URL', 'https://api.swarmvault.xyz')
        self.swarm_id = os.getenv('SWARM_ID')

        # Bot Configuration
        self.trading_enabled = os.getenv('TRADING_ENABLED', 'false').lower() == 'true'
        self.dry_run = os.getenv('DRY_RUN', 'true').lower() == 'true'
        self.check_interval = int(os.getenv('CHECK_INTERVAL_SECONDS', '300'))

        # Logging Configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('LOG_FILE', 'trading_bot.log')

        # Load strategy configuration from YAML
        if config_file is None:
            config_file = 'config.yaml'

        self.strategy_config = {}
        if Path(config_file).exists():
            with open(config_file, 'r') as f:
                self.strategy_config = yaml.safe_load(f)

        # Validate required configuration
        self._validate()

    def _validate(self):
        """Validate required configuration values"""
        if not self.api_key:
            raise ValueError("SWARM_VAULT_API_KEY environment variable is required")

        if not self.swarm_id:
            raise ValueError("SWARM_ID environment variable is required")

        if not self.api_key.startswith('svk_'):
            raise ValueError("Invalid API key format. Must start with 'svk_'")

    def get_strategy_config(self, strategy_name: str) -> Dict[str, Any]:
        """Get configuration for a specific strategy"""
        return self.strategy_config.get(strategy_name, {})

    def get_active_strategy(self) -> str:
        """Get the name of the active strategy"""
        return self.strategy_config.get('active_strategy', 'dca')

    def get_risk_management(self) -> Dict[str, Any]:
        """Get risk management configuration"""
        return self.strategy_config.get('risk_management', {})

    def is_dry_run(self) -> bool:
        """Check if running in dry-run mode"""
        return self.dry_run or not self.trading_enabled

    def __repr__(self):
        return (
            f"Config(swarm_id={self.swarm_id}, "
            f"dry_run={self.dry_run}, "
            f"strategy={self.get_active_strategy()})"
        )
