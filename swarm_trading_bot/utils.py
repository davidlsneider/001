"""
Utility functions for the trading bot
"""
from typing import Dict, Any
import json
from pathlib import Path
from datetime import datetime


def format_token_amount(amount: str, decimals: int, precision: int = 4) -> str:
    """
    Format token amount for display

    Args:
        amount: Amount as string (wei)
        decimals: Token decimals
        precision: Decimal places to show

    Returns:
        Formatted string
    """
    value = int(amount) / (10 ** decimals)
    return f"{value:.{precision}f}"


def save_trade_history(history: list, filename: str = "trade_history.json"):
    """
    Save trade history to file

    Args:
        history: List of trade records
        filename: Output filename
    """
    filepath = Path(filename)

    try:
        with open(filepath, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving trade history: {e}")


def load_trade_history(filename: str = "trade_history.json") -> list:
    """
    Load trade history from file

    Args:
        filename: Input filename

    Returns:
        List of trade records
    """
    filepath = Path(filename)

    if not filepath.exists():
        return []

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading trade history: {e}")
        return []


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values

    Args:
        old_value: Original value
        new_value: New value

    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0

    return ((new_value - old_value) / old_value) * 100


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "2h 15m 30s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


# Common token addresses on Base mainnet
BASE_MAINNET_TOKENS = {
    'ETH': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
    'WETH': '0x4200000000000000000000000000000000000006',
    'USDC': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    'USDbC': '0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA',
    'DAI': '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb',
}


def get_token_address(symbol_or_address: str) -> str:
    """
    Get token address from symbol or return address if already provided

    Args:
        symbol_or_address: Token symbol (e.g., 'USDC') or address

    Returns:
        Token address
    """
    # If it's already an address, return it
    if symbol_or_address.startswith('0x'):
        return symbol_or_address

    # Look up by symbol
    symbol = symbol_or_address.upper()
    if symbol in BASE_MAINNET_TOKENS:
        return BASE_MAINNET_TOKENS[symbol]

    raise ValueError(f"Unknown token symbol: {symbol_or_address}")
