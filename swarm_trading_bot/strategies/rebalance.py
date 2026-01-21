"""
Portfolio Rebalancing Strategy

Maintains a target allocation of tokens by rebalancing when
the portfolio drifts beyond a threshold.
"""
from typing import Dict, Any, Optional

from .base import BaseStrategy
from ..models import Holdings


class RebalanceStrategy(BaseStrategy):
    """
    Rebalancing Strategy - Maintain target portfolio allocation

    Configuration:
        target_allocation: Dict of {token_address: target_percentage}
        drift_threshold: Rebalance when allocation drifts by this %
        check_interval_seconds: How often to check for drift
        slippage_percentage: Slippage tolerance
    """

    def __init__(self, client, swarm_id: str, config: Dict[str, Any], dry_run: bool = True):
        super().__init__(client, swarm_id, config, dry_run)

        # Validate configuration
        if 'target_allocation' not in config:
            raise ValueError("RebalanceStrategy requires 'target_allocation' in configuration")

        self.target_allocation = config['target_allocation']
        self.drift_threshold = config.get('drift_threshold', 5.0)
        self.check_interval = config.get('check_interval_seconds', 3600)
        self.slippage = config.get('slippage_percentage', 1.0)

        # Validate allocations sum to 100%
        total = sum(self.target_allocation.values())
        if abs(total - 100) > 0.01:
            raise ValueError(f"Target allocations must sum to 100%, got {total}%")

        self.logger.info(f"Rebalancing Strategy initialized:")
        for token, pct in self.target_allocation.items():
            self.logger.info(f"  {token}: {pct}%")

    def _calculate_portfolio_value(self, holdings: Holdings) -> Dict[str, float]:
        """
        Calculate current portfolio value and allocation

        Returns:
            Dict with 'total_value', 'allocations', 'values'
        """
        # For simplicity, we'll use a rough estimation
        # In production, you'd want to fetch real prices

        values = {}

        # ETH
        eth_balance = self.client.wei_to_eth(holdings.eth_balance)
        eth_addr = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
        values[eth_addr] = eth_balance

        # Tokens (using balance as proxy for value - simplified)
        for token in holdings.tokens:
            balance = self.client.format_amount(
                token.total_balance or token.balance,
                token.decimals
            )
            values[token.address] = float(balance)

        total_value = sum(values.values())

        if total_value == 0:
            return {'total_value': 0, 'allocations': {}, 'values': values}

        # Calculate current allocations
        allocations = {
            addr: (value / total_value * 100)
            for addr, value in values.items()
        }

        return {
            'total_value': total_value,
            'allocations': allocations,
            'values': values
        }

    def should_trade(self, holdings: Holdings) -> bool:
        """
        Check if portfolio has drifted beyond threshold

        Args:
            holdings: Current swarm holdings

        Returns:
            True if rebalancing is needed
        """
        portfolio = self._calculate_portfolio_value(holdings)

        if portfolio['total_value'] == 0:
            self.logger.warning("Portfolio has zero value")
            return False

        current_alloc = portfolio['allocations']

        # Check drift for each target token
        max_drift = 0
        drift_details = []

        for token, target_pct in self.target_allocation.items():
            current_pct = current_alloc.get(token, 0)
            drift = abs(current_pct - target_pct)
            max_drift = max(max_drift, drift)

            drift_details.append(
                f"{token[:10]}... Target:{target_pct}% Current:{current_pct:.1f}% Drift:{drift:.1f}%"
            )

        self.logger.info("Portfolio Status:")
        for detail in drift_details:
            self.logger.info(f"  {detail}")

        if max_drift > self.drift_threshold:
            self.logger.info(
                f"Rebalancing needed: max drift {max_drift:.1f}% > {self.drift_threshold}%"
            )
            return True

        self.logger.debug(
            f"Portfolio balanced: max drift {max_drift:.1f}% <= {self.drift_threshold}%"
        )
        return False

    def get_trade_params(self, holdings: Holdings) -> Optional[Dict[str, Any]]:
        """
        Calculate rebalancing trade

        This is simplified - it finds the most overweight and underweight
        tokens and trades between them.

        Args:
            holdings: Current swarm holdings

        Returns:
            Trade parameters for rebalancing
        """
        portfolio = self._calculate_portfolio_value(holdings)
        current_alloc = portfolio['allocations']

        # Find most overweight and underweight tokens
        max_over = None
        max_over_diff = 0
        max_under = None
        max_under_diff = 0

        for token, target_pct in self.target_allocation.items():
            current_pct = current_alloc.get(token, 0)
            diff = current_pct - target_pct

            if diff > max_over_diff:
                max_over = token
                max_over_diff = diff
            elif diff < -max_under_diff:
                max_under = token
                max_under_diff = -diff

        if not max_over or not max_under:
            self.logger.warning("Could not determine rebalancing trade")
            return None

        # Calculate how much to trade
        # Simplified: trade to bring overweight token closer to target
        sell_percentage = min(50, max_over_diff * 2)  # Conservative

        self.logger.info(
            f"Rebalancing: Sell {sell_percentage:.1f}% of {max_over[:10]}... "
            f"to buy {max_under[:10]}..."
        )

        return {
            'sell_token': max_over,
            'buy_token': max_under,
            'sell_percentage': sell_percentage,
            'slippage_percentage': self.slippage
        }
