#!/usr/bin/env python3
"""
Test Swap

Preview a swap without executing it. Useful for testing your configuration.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from swarm_trading_bot.config import Config
from swarm_trading_bot.client import SwarmVaultClient
from swarm_trading_bot.logger import setup_logger
from swarm_trading_bot.utils import BASE_MAINNET_TOKENS


def main():
    """Preview a test swap"""
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
    logger.info(f"Swarm: {swarm.name} ({swarm.member_count} members)")

    if not swarm.is_manager:
        logger.error("You must be a manager to preview swaps")
        sys.exit(1)

    # Example: Preview swapping 10% USDC -> WETH
    logger.info("\n" + "=" * 60)
    logger.info("SWAP PREVIEW")
    logger.info("=" * 60)

    sell_token = BASE_MAINNET_TOKENS['USDC']
    buy_token = BASE_MAINNET_TOKENS['WETH']
    sell_percentage = 10
    slippage = 1.0

    logger.info(f"\nPreviewing: {sell_percentage}% USDC -> WETH")
    logger.info(f"Sell Token: {sell_token}")
    logger.info(f"Buy Token:  {buy_token}")
    logger.info(f"Slippage:   {slippage}%")

    try:
        preview = client.preview_swap(
            swarm_id=config.swarm_id,
            sell_token=sell_token,
            buy_token=buy_token,
            sell_percentage=sell_percentage,
            slippage_percentage=slippage
        )

        logger.info("\n" + "-" * 60)
        logger.info("PREVIEW RESULTS")
        logger.info("-" * 60)
        logger.info(f"Total Sell Amount:  {preview.total_sell_amount}")
        logger.info(f"Total Buy Amount:   {preview.total_buy_amount}")
        logger.info(f"Total Fee Amount:   {preview.total_fee_amount}")
        logger.info(f"Successful Members: {preview.success_count}/{len(preview.members)}")
        logger.info(f"Errors:             {preview.error_count}")

        if preview.fee:
            logger.info(f"\nPlatform Fee:")
            logger.info(f"  Rate:      {preview.fee['percentage']}")
            logger.info(f"  Recipient: {preview.fee['recipientAddress']}")

        # Show per-member details
        if preview.members:
            logger.info(f"\nPer-Member Details:")
            logger.info("-" * 60)

            for i, member in enumerate(preview.members[:5], 1):  # Show first 5
                logger.info(f"\nMember {i}:")
                logger.info(f"  Agent Wallet: {member.agent_wallet_address}")
                logger.info(f"  Sell Amount:  {member.sell_amount}")
                logger.info(f"  Buy Amount:   {member.buy_amount}")
                logger.info(f"  Fee Amount:   {member.fee_amount}")
                logger.info(f"  Price Impact: {member.estimated_price_impact}")

                if member.error:
                    logger.warning(f"  Error: {member.error}")

            if len(preview.members) > 5:
                logger.info(f"\n... and {len(preview.members) - 5} more members")

        logger.info("\n" + "=" * 60)
        logger.info("This was a PREVIEW only - no trades were executed")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Failed to preview swap: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
