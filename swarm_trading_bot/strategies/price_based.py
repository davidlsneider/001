"""
Price-Based Trading Strategy

Executes trades based on price movements and thresholds.
This is a simplified version - in production you'd integrate
with price feeds.
"""
from typing import Dict, Any, Optional, List

from .base import BaseStrategy
from ..models import Holdings


class PriceBasedStrategy(BaseStrategy):
    """
    Price-Based Strategy - Trade based on price thresholds

    Configuration:
        sell_token: Token to sell
        buy_token: Token to buy
        rules: List of trading rules with conditions
        slippage_percentage: Slippage tolerance

    Note: This is a simplified implementation.
    In production, integrate with price oracles or APIs.
    """

    def __init__(self, client, swarm_id: str, config: Dict[str, Any], dry_run: bool = True):
        super().__init__(client, swarm_id, config, dry_run)

        # Validate configuration
        required = ['sell_token', 'buy_token', 'rules']
        for key in required:
            if key not in config:
                raise ValueError(f"PriceBasedStrategy requires '{key}' in configuration")

        self.sell_token = config['sell_token']
        self.buy_token = config['buy_token']
        self.rules = config['rules']
        self.slippage = config.get('slippage_percentage', 1.0)

        # Track reference price (simplified - use first holdings snapshot)
        self.reference_price = None
        self.last_check_holdings = None

        self.logger.info(f"Price-Based Strategy initialized with {len(self.rules)} rules")
        self.logger.warning(
            "Note: This strategy uses simplified price tracking. "
            "For production, integrate with price oracles."
        )

    def _estimate_price(self, holdings: Holdings) -> Optional[float]:
        """
        Estimate current price ratio (simplified)

        In production, you should:
        1. Use DEX price feeds (Uniswap, etc.)
        2. Use oracle services (Chainlink, etc.)
        3. Use external price APIs

        Returns:
            Estimated price or None
        """
        # This is a placeholder - would need real price data
        # For demo purposes, we'll use a random estimation based on holdings

        sell_balance = 0
        buy_balance = 0

        # Get balances
        if self.sell_token == "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":
            sell_balance = self.client.wei_to_eth(holdings.eth_balance)
        else:
            for token in holdings.tokens:
                if token.address.lower() == self.sell_token.lower():
                    sell_balance = self.client.format_amount(
                        token.total_balance or token.balance,
                        token.decimals
                    )
                    break

        if self.buy_token == "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE":
            buy_balance = self.client.wei_to_eth(holdings.eth_balance)
        else:
            for token in holdings.tokens:
                if token.address.lower() == self.buy_token.lower():
                    buy_balance = self.client.format_amount(
                        token.total_balance or token.balance,
                        token.decimals
                    )
                    break

        if sell_balance == 0 or buy_balance == 0:
            return None

        # Simple ratio as proxy for price
        return buy_balance / sell_balance

    def _check_price_conditions(self, current_price: float) -> Optional[Dict[str, Any]]:
        """
        Check if any price-based rules are triggered

        Args:
            current_price: Current estimated price

        Returns:
            Matching rule or None
        """
        if self.reference_price is None:
            self.reference_price = current_price
            self.logger.info(f"Set reference price: {current_price:.6f}")
            return None

        price_change_pct = ((current_price - self.reference_price) / self.reference_price) * 100

        self.logger.info(
            f"Price change: {price_change_pct:+.2f}% "
            f"(ref: {self.reference_price:.6f}, current: {current_price:.6f})"
        )

        # Check each rule
        for rule in self.rules:
            condition = rule.get('condition')
            threshold = rule.get('threshold_percentage', 0)

            triggered = False

            if condition == 'price_drop' and price_change_pct <= -threshold:
                triggered = True
                self.logger.info(f"Price drop triggered: {price_change_pct:.2f}% <= -{threshold}%")
            elif condition == 'price_increase' and price_change_pct >= threshold:
                triggered = True
                self.logger.info(f"Price increase triggered: {price_change_pct:.2f}% >= {threshold}%")

            if triggered:
                # Update reference price after trigger
                self.reference_price = current_price
                return rule

        return None

    def should_trade(self, holdings: Holdings) -> bool:
        """
        Check if price conditions trigger a trade

        Args:
            holdings: Current swarm holdings

        Returns:
            True if price-based conditions are met
        """
        current_price = self._estimate_price(holdings)

        if current_price is None:
            self.logger.warning("Could not estimate current price")
            return False

        triggered_rule = self._check_price_conditions(current_price)

        self.last_check_holdings = holdings

        return triggered_rule is not None

    def get_trade_params(self, holdings: Holdings) -> Optional[Dict[str, Any]]:
        """
        Get trade parameters based on triggered rule

        Args:
            holdings: Current swarm holdings

        Returns:
            Trade parameters
        """
        current_price = self._estimate_price(holdings)

        if current_price is None:
            return None

        triggered_rule = self._check_price_conditions(current_price)

        if not triggered_rule:
            return None

        action = triggered_rule.get('action', 'buy')
        sell_percentage = triggered_rule.get('sell_percentage', 10)

        # Determine tokens based on action
        if action == 'buy':
            sell = self.sell_token
            buy = self.buy_token
        else:  # sell
            sell = self.buy_token
            buy = self.sell_token

        return {
            'sell_token': sell,
            'buy_token': buy,
            'sell_percentage': sell_percentage,
            'slippage_percentage': self.slippage
        }
