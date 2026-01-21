"""
Dollar Cost Averaging (DCA) Strategy

Executes regular purchases of a target token at fixed intervals,
regardless of price. This strategy reduces the impact of volatility.
"""
from typing import Dict, Any, Optional
import time

from .base import BaseStrategy
from ..models import Holdings


class DCAStrategy(BaseStrategy):
    """
    DCA Strategy - Buy target token at regular intervals

    Configuration:
        sell_token: Token to sell (source of funds)
        buy_token: Token to buy (target)
        sell_percentage: Percentage of sell_token to use (1-100)
        interval_seconds: Time between purchases
        slippage_percentage: Slippage tolerance
    """

    def __init__(self, client, swarm_id: str, config: Dict[str, Any], dry_run: bool = True):
        super().__init__(client, swarm_id, config, dry_run)

        # Validate required config
        required = ['sell_token', 'buy_token', 'sell_percentage', 'interval_seconds']
        for key in required:
            if key not in config:
                raise ValueError(f"DCAStrategy requires '{key}' in configuration")

        self.sell_token = config['sell_token']
        self.buy_token = config['buy_token']
        self.sell_percentage = config['sell_percentage']
        self.interval = config['interval_seconds']
        self.slippage = config.get('slippage_percentage', 1.0)

        self.logger.info(
            f"DCA Strategy initialized: {self.sell_percentage}% "
            f"{self.sell_token} -> {self.buy_token} every {self.interval}s"
        )

    def should_trade(self, holdings: Holdings) -> bool:
        """
        Check if enough time has passed since last trade

        Args:
            holdings: Current swarm holdings

        Returns:
            True if interval has elapsed
        """
        if self.last_trade_time == 0:
            # First trade
            return True

        elapsed = time.time() - self.last_trade_time
        should_trade = elapsed >= self.interval

        if should_trade:
            self.logger.info(f"DCA interval reached ({elapsed:.0f}s >= {self.interval}s)")
        else:
            remaining = self.interval - elapsed
            self.logger.debug(f"DCA waiting: {remaining:.0f}s until next trade")

        return should_trade

    def get_trade_params(self, holdings: Holdings) -> Optional[Dict[str, Any]]:
        """
        Get DCA trade parameters

        Args:
            holdings: Current swarm holdings

        Returns:
            Trade parameters for DCA purchase
        """
        # Check if we have the sell token
        has_sell_token = False

        # Check ETH balance
        if self.sell_token == "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":
            eth_balance = self.client.wei_to_eth(holdings.eth_balance)
            if eth_balance > 0:
                has_sell_token = True
                self.logger.info(f"ETH balance: {eth_balance:.4f}")
        else:
            # Check token balance
            for token in holdings.tokens:
                if token.address.lower() == self.sell_token.lower():
                    balance = self.client.format_amount(
                        token.total_balance or token.balance,
                        token.decimals
                    )
                    if float(balance) > 0:
                        has_sell_token = True
                        self.logger.info(f"{token.symbol} balance: {balance:.4f}")
                    break

        if not has_sell_token:
            self.logger.warning(f"No balance for sell token: {self.sell_token}")
            return None

        return {
            'sell_token': self.sell_token,
            'buy_token': self.buy_token,
            'sell_percentage': self.sell_percentage,
            'slippage_percentage': self.slippage
        }
