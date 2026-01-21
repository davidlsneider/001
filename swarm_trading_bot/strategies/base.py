"""
Base class for trading strategies
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import time

from ..client import SwarmVaultClient
from ..models import Holdings, SwapPreview
from ..logger import get_logger


class BaseStrategy(ABC):
    """Base class for all trading strategies"""

    def __init__(
        self,
        client: SwarmVaultClient,
        swarm_id: str,
        config: Dict[str, Any],
        dry_run: bool = True
    ):
        """
        Initialize strategy

        Args:
            client: SwarmVaultClient instance
            swarm_id: Swarm ID to trade on
            config: Strategy-specific configuration
            dry_run: If True, only preview trades without executing
        """
        self.client = client
        self.swarm_id = swarm_id
        self.config = config
        self.dry_run = dry_run
        self.logger = get_logger()
        self.last_trade_time = 0
        self.trade_history = []

    @abstractmethod
    def should_trade(self, holdings: Holdings) -> bool:
        """
        Determine if a trade should be executed

        Args:
            holdings: Current swarm holdings

        Returns:
            True if trade conditions are met
        """
        pass

    @abstractmethod
    def get_trade_params(self, holdings: Holdings) -> Optional[Dict[str, Any]]:
        """
        Get parameters for the trade to execute

        Args:
            holdings: Current swarm holdings

        Returns:
            Dictionary with trade parameters or None if no trade
            {
                'sell_token': str,
                'buy_token': str,
                'sell_percentage': float,
                'slippage_percentage': float
            }
        """
        pass

    def check_risk_limits(self, trade_params: Dict[str, Any]) -> bool:
        """
        Verify trade doesn't violate risk management rules

        Args:
            trade_params: Proposed trade parameters

        Returns:
            True if trade is within risk limits
        """
        # Check minimum trade interval
        min_interval = self.config.get('min_trade_interval', 300)
        time_since_last = time.time() - self.last_trade_time

        if time_since_last < min_interval:
            self.logger.warning(
                f"Trade blocked: minimum interval not met "
                f"({time_since_last:.0f}s < {min_interval}s)"
            )
            return False

        # Check maximum trade percentage
        max_trade_pct = self.config.get('max_trade_percentage', 100)
        sell_pct = trade_params.get('sell_percentage', 100)

        if sell_pct > max_trade_pct:
            self.logger.warning(
                f"Trade blocked: percentage too high ({sell_pct}% > {max_trade_pct}%)"
            )
            return False

        return True

    def execute_trade(self, trade_params: Dict[str, Any]) -> Optional[str]:
        """
        Execute a trade with the given parameters

        Args:
            trade_params: Trade parameters

        Returns:
            Transaction ID if executed, None otherwise
        """
        try:
            # Preview the swap first
            preview = self.client.preview_swap(
                swarm_id=self.swarm_id,
                sell_token=trade_params['sell_token'],
                buy_token=trade_params['buy_token'],
                sell_percentage=trade_params['sell_percentage'],
                slippage_percentage=trade_params['slippage_percentage']
            )

            self.logger.info(f"Swap Preview:")
            self.logger.info(f"  Total Sell: {preview.total_sell_amount}")
            self.logger.info(f"  Total Buy: {preview.total_buy_amount}")
            self.logger.info(f"  Total Fee: {preview.total_fee_amount}")
            self.logger.info(f"  Success: {preview.success_count}/{len(preview.members)}")

            if preview.error_count > 0:
                self.logger.warning(f"  Errors: {preview.error_count} members cannot execute")

            # Check if we should proceed
            if preview.success_count == 0:
                self.logger.error("No members can execute this swap")
                return None

            if self.dry_run:
                self.logger.info("[DRY RUN] Would execute swap, but dry_run=True")
                return None

            # Execute the swap
            tx_id = self.client.execute_swap(
                swarm_id=self.swarm_id,
                sell_token=trade_params['sell_token'],
                buy_token=trade_params['buy_token'],
                sell_percentage=trade_params['sell_percentage'],
                slippage_percentage=trade_params['slippage_percentage']
            )

            # Update trade history
            self.last_trade_time = time.time()
            self.trade_history.append({
                'timestamp': datetime.now().isoformat(),
                'transaction_id': tx_id,
                'params': trade_params,
                'preview': {
                    'total_sell': preview.total_sell_amount,
                    'total_buy': preview.total_buy_amount,
                    'success_count': preview.success_count
                }
            })

            return tx_id

        except Exception as e:
            self.logger.error(f"Failed to execute trade: {e}")
            return None

    def run_iteration(self):
        """
        Run one iteration of the strategy

        This is called periodically by the bot main loop
        """
        try:
            self.logger.debug(f"Running {self.__class__.__name__} iteration")

            # Get current holdings
            holdings = self.client.get_holdings(self.swarm_id)

            # Log current state
            self.logger.info(f"Current Holdings:")
            self.logger.info(f"  ETH: {self.client.wei_to_eth(holdings.eth_balance):.4f}")
            for token in holdings.tokens[:5]:  # Show first 5 tokens
                amount = self.client.format_amount(token.total_balance or token.balance, token.decimals)
                self.logger.info(f"  {token.symbol}: {amount:.4f}")

            # Check if we should trade
            if not self.should_trade(holdings):
                self.logger.debug("Trade conditions not met")
                return

            # Get trade parameters
            trade_params = self.get_trade_params(holdings)
            if not trade_params:
                self.logger.debug("No trade parameters generated")
                return

            # Check risk limits
            if not self.check_risk_limits(trade_params):
                self.logger.warning("Trade blocked by risk management")
                return

            # Execute trade
            tx_id = self.execute_trade(trade_params)

            if tx_id:
                self.logger.info(f"Trade executed successfully: {tx_id}")

                # Wait for completion (if not dry run)
                if not self.dry_run:
                    try:
                        tx = self.client.wait_for_transaction(tx_id, timeout=300)
                        self.logger.info(f"Transaction completed: {tx.status}")
                    except Exception as e:
                        self.logger.error(f"Error waiting for transaction: {e}")

        except Exception as e:
            self.logger.error(f"Error in strategy iteration: {e}", exc_info=True)

    def get_strategy_state(self) -> Dict[str, Any]:
        """Get current strategy state for monitoring"""
        return {
            'strategy': self.__class__.__name__,
            'swarm_id': self.swarm_id,
            'dry_run': self.dry_run,
            'last_trade_time': self.last_trade_time,
            'total_trades': len(self.trade_history),
            'config': self.config
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(swarm_id={self.swarm_id}, dry_run={self.dry_run})"
