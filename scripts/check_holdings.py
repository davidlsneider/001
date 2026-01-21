#!/usr/bin/env python3
"""
Check Swarm Holdings

Utility script to view current holdings across all swarm members.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm_trading_bot.config import Config
from swarm_trading_bot.client import SwarmVaultClient
from swarm_trading_bot.logger import setup_logger


def main():
    """Check and display swarm holdings"""
    # Load config
    config = Config()

    # Setup logger
    logger = setup_logger(log_level='INFO')

    # Create client
    client = SwarmVaultClient(config.api_key, config.base_url)

    # Verify connection
    user = client.verify_api_key()
    logger.info(f"Connected as: {user.get('walletAddress')}")

    # Get swarm info
    swarm = client.get_swarm(config.swarm_id)
    logger.info(f"\nSwarm: {swarm.name}")
    logger.info(f"Members: {swarm.member_count}")
    logger.info(f"Manager: {swarm.is_manager}")

    # Get holdings
    logger.info("\n" + "=" * 60)
    logger.info("CURRENT HOLDINGS")
    logger.info("=" * 60)

    holdings = client.get_holdings(config.swarm_id)

    # Display ETH
    eth_balance = client.wei_to_eth(holdings.eth_balance)
    logger.info(f"\nETH: {eth_balance:.6f}")

    # Display tokens
    if holdings.tokens:
        logger.info(f"\nTokens ({len(holdings.tokens)}):")
        logger.info("-" * 60)

        for token in sorted(holdings.tokens, key=lambda t: t.symbol):
            balance = client.format_amount(
                token.total_balance or token.balance,
                token.decimals
            )
            logger.info(
                f"  {token.symbol:10s} {float(balance):>15,.4f}  "
                f"({token.holder_count or 0} holders)"
            )
    else:
        logger.info("\nNo tokens found")

    # Display common tokens
    if holdings.common_tokens:
        logger.info(f"\nCommon tokens (held by all {holdings.member_count} members):")
        for token in holdings.common_tokens:
            logger.info(f"  - {token['symbol']} ({token['name']})")

    logger.info("\n" + "=" * 60)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
