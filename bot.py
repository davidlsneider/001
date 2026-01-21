#!/usr/bin/env python3
"""
Swarm Vault Trading Bot

Main entry point for running the trading bot with various strategies.
"""
import sys
import time
import signal
from pathlib import Path

from swarm_trading_bot.config import Config
from swarm_trading_bot.client import SwarmVaultClient
from swarm_trading_bot.logger import setup_logger
from swarm_trading_bot.strategies import (
    DCAStrategy,
    RebalanceStrategy,
    PriceBasedStrategy
)


class TradingBot:
    """Main trading bot orchestrator"""

    def __init__(self, config_file: str = 'config.yaml'):
        """
        Initialize trading bot

        Args:
            config_file: Path to configuration file
        """
        # Load configuration
        self.config = Config(config_file)

        # Setup logging
        self.logger = setup_logger(
            log_file=self.config.log_file,
            log_level=self.config.log_level
        )

        self.logger.info("=" * 60)
        self.logger.info("Swarm Vault Trading Bot Starting")
        self.logger.info("=" * 60)
        self.logger.info(f"Configuration: {self.config}")

        # Initialize API client
        self.client = SwarmVaultClient(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )

        # Verify API connection
        try:
            user = self.client.verify_api_key()
            self.logger.info(f"Connected as: {user.get('walletAddress', 'Unknown')}")
        except Exception as e:
            self.logger.error(f"Failed to verify API key: {e}")
            sys.exit(1)

        # Get swarm info
        try:
            swarm = self.client.get_swarm(self.config.swarm_id)
            self.logger.info(f"Trading on swarm: {swarm.name} (ID: {swarm.id})")
            self.logger.info(f"Members: {swarm.member_count}")
            self.logger.info(f"Manager: {swarm.is_manager}")

            if not swarm.is_manager:
                self.logger.error("You must be a swarm manager to run the trading bot")
                sys.exit(1)

        except Exception as e:
            self.logger.error(f"Failed to get swarm info: {e}")
            sys.exit(1)

        # Initialize strategy
        self.strategy = self._create_strategy()

        # Bot state
        self.running = False
        self.iteration_count = 0

    def _create_strategy(self):
        """Create trading strategy based on configuration"""
        strategy_name = self.config.get_active_strategy()
        strategy_config = self.config.get_strategy_config(strategy_name)

        # Add risk management to strategy config
        risk_config = self.config.get_risk_management()
        strategy_config.update(risk_config)

        self.logger.info(f"Initializing strategy: {strategy_name}")

        if strategy_name == 'dca':
            return DCAStrategy(
                client=self.client,
                swarm_id=self.config.swarm_id,
                config=strategy_config,
                dry_run=self.config.is_dry_run()
            )
        elif strategy_name == 'rebalance':
            return RebalanceStrategy(
                client=self.client,
                swarm_id=self.config.swarm_id,
                config=strategy_config,
                dry_run=self.config.is_dry_run()
            )
        elif strategy_name == 'price_based':
            return PriceBasedStrategy(
                client=self.client,
                swarm_id=self.config.swarm_id,
                config=strategy_config,
                dry_run=self.config.is_dry_run()
            )
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")

    def run(self):
        """Run the trading bot main loop"""
        self.running = True

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        if self.config.is_dry_run():
            self.logger.warning("=" * 60)
            self.logger.warning("RUNNING IN DRY-RUN MODE - NO REAL TRADES WILL BE EXECUTED")
            self.logger.warning("=" * 60)

        self.logger.info(f"Bot running with {self.config.check_interval}s check interval")
        self.logger.info("Press Ctrl+C to stop")

        try:
            while self.running:
                self.iteration_count += 1
                self.logger.info(f"\n--- Iteration {self.iteration_count} ---")

                # Run strategy iteration
                try:
                    self.strategy.run_iteration()
                except Exception as e:
                    self.logger.error(f"Error in strategy iteration: {e}", exc_info=True)

                # Wait for next iteration
                if self.running:
                    self.logger.debug(f"Sleeping for {self.config.check_interval}s...")
                    time.sleep(self.config.check_interval)

        except KeyboardInterrupt:
            self.logger.info("\nReceived keyboard interrupt")
        finally:
            self.shutdown()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"\nReceived signal {signum}, shutting down...")
        self.running = False

    def shutdown(self):
        """Graceful shutdown"""
        self.logger.info("=" * 60)
        self.logger.info("Trading Bot Shutting Down")
        self.logger.info(f"Total iterations: {self.iteration_count}")
        self.logger.info(f"Total trades executed: {len(self.strategy.trade_history)}")

        # Print strategy state
        state = self.strategy.get_strategy_state()
        self.logger.info(f"Final state: {state}")

        self.logger.info("=" * 60)


def main():
    """Main entry point"""
    # Check for config file
    config_file = 'config.yaml'

    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    if not Path(config_file).exists():
        print(f"Error: Configuration file '{config_file}' not found")
        print("\nPlease create config.yaml from config.yaml.example:")
        print("  cp config.yaml.example config.yaml")
        print("\nAnd create .env from .env.example:")
        print("  cp .env.example .env")
        print("\nThen edit both files with your configuration.")
        sys.exit(1)

    # Check for .env file
    if not Path('.env').exists():
        print("Warning: .env file not found")
        print("Please create .env from .env.example:")
        print("  cp .env.example .env")
        print("\nThen edit it with your API key and configuration.")
        sys.exit(1)

    try:
        bot = TradingBot(config_file)
        bot.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
