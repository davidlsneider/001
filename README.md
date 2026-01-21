# Swarm Vault Trading Bot

A Python-based automated trading bot for the [Swarm Vault](https://swarmvault.xyz) platform on Base blockchain. Execute sophisticated trading strategies across multiple member wallets with ease.

## 🚀 Features

- **Multiple Trading Strategies**
  - DCA (Dollar Cost Averaging)
  - Portfolio Rebalancing
  - Price-Based Trading
  - Easily extensible for custom strategies

- **Professional Features**
  - Comprehensive API client wrapper
  - Risk management controls
  - Dry-run mode for testing
  - Detailed logging and monitoring
  - Transaction tracking and history
  - Graceful error handling

- **Production Ready**
  - Type hints and documentation
  - Configuration via YAML and environment variables
  - Modular and maintainable code structure
  - Signal handling for graceful shutdown

## 📋 Requirements

- Python 3.7+
- Swarm Vault account with manager access
- API key from Swarm Vault (get it from Settings)

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd 001
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API key and swarm ID
```

4. **Configure trading strategy**
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your trading parameters
```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# API Configuration
SWARM_VAULT_API_KEY=svk_your_api_key_here
SWARM_VAULT_BASE_URL=https://api.swarmvault.xyz
SWARM_ID=your_swarm_id_here

# Bot Configuration
TRADING_ENABLED=false
DRY_RUN=true
CHECK_INTERVAL_SECONDS=300

# Logging
LOG_LEVEL=INFO
LOG_FILE=trading_bot.log
```

### Getting Your API Key

1. Go to [swarmvault.xyz](https://swarmvault.xyz)
2. Log in with your wallet
3. Navigate to **Settings**
4. Click **Generate API Key**
5. Copy the key immediately (shown only once!)

### Strategy Configuration (config.yaml)

The bot supports three built-in strategies:

#### 1. DCA (Dollar Cost Averaging)

Buys a fixed percentage at regular intervals, regardless of price.

```yaml
active_strategy: dca

dca:
  sell_token: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC
  buy_token: "0x4200000000000000000000000000000000000006"   # WETH
  sell_percentage: 10
  interval_seconds: 86400  # Daily
  slippage_percentage: 1.0
```

#### 2. Rebalancing

Maintains target portfolio allocation by rebalancing when drift exceeds threshold.

```yaml
active_strategy: rebalance

rebalance:
  target_allocation:
    "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE": 30  # ETH: 30%
    "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913": 40  # USDC: 40%
    "0x4200000000000000000000000000000000000006": 30  # WETH: 30%
  drift_threshold: 5
  check_interval_seconds: 3600  # Hourly
  slippage_percentage: 1.0
```

#### 3. Price-Based

Executes trades based on price movements (simplified - for production, integrate price oracles).

```yaml
active_strategy: price_based

price_based:
  sell_token: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC
  buy_token: "0x4200000000000000000000000000000000000006"   # WETH
  rules:
    - condition: "price_drop"
      threshold_percentage: 5
      action: "buy"
      sell_percentage: 20
    - condition: "price_increase"
      threshold_percentage: 10
      action: "sell"
      sell_percentage: 50
  slippage_percentage: 1.0
```

### Common Base Mainnet Tokens

```
ETH:   0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
WETH:  0x4200000000000000000000000000000000000006
USDC:  0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
USDbC: 0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA
DAI:   0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb
```

## 🎯 Usage

### Running the Bot

**Dry-run mode (recommended for testing):**
```bash
python bot.py
```

**Live trading (CAUTION):**
```bash
# Edit .env to set:
# TRADING_ENABLED=true
# DRY_RUN=false
python bot.py
```

### Utility Scripts

**Check current holdings:**
```bash
python scripts/check_holdings.py
```

**Preview a swap (without executing):**
```bash
python scripts/test_swap.py
```

## 📊 Project Structure

```
001/
├── swarm_trading_bot/          # Main package
│   ├── __init__.py
│   ├── client.py               # API client wrapper
│   ├── config.py               # Configuration management
│   ├── logger.py               # Logging setup
│   ├── models.py               # Data models
│   ├── utils.py                # Utility functions
│   └── strategies/             # Trading strategies
│       ├── __init__.py
│       ├── base.py             # Base strategy class
│       ├── dca.py              # DCA strategy
│       ├── rebalance.py        # Rebalancing strategy
│       └── price_based.py      # Price-based strategy
├── scripts/                    # Utility scripts
│   ├── check_holdings.py
│   └── test_swap.py
├── bot.py                      # Main bot runner
├── config.yaml.example         # Example strategy config
├── .env.example                # Example environment config
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔒 Risk Management

The bot includes built-in risk management features:

- **Maximum Trade Percentage**: Limits how much of a token can be traded in one transaction
- **Minimum Trade Interval**: Enforces cooldown between trades
- **Stop Loss**: Can halt trading if portfolio value drops below threshold
- **Dry-run Mode**: Test strategies without executing real trades

Configure in `config.yaml`:

```yaml
risk_management:
  max_trade_percentage: 25
  min_trade_interval: 300
  stop_loss_percentage: 20
```

## 📝 API Client Usage

You can also use the API client directly in your own scripts:

```python
from swarm_trading_bot.client import SwarmVaultClient

# Initialize client
client = SwarmVaultClient(api_key='svk_your_key_here')

# Get swarm holdings
holdings = client.get_holdings('swarm-id')

# Preview a swap
preview = client.preview_swap(
    swarm_id='swarm-id',
    sell_token='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',  # USDC
    buy_token='0x4200000000000000000000000000000000000006',   # WETH
    sell_percentage=10,
    slippage_percentage=1.0
)

# Execute swap
tx_id = client.execute_swap(
    swarm_id='swarm-id',
    sell_token='0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    buy_token='0x4200000000000000000000000000000000000006',
    sell_percentage=10,
    slippage_percentage=1.0
)

# Wait for completion
tx = client.wait_for_transaction(tx_id)
print(f"Transaction status: {tx.status}")
```

## 🔧 Creating Custom Strategies

Extend the `BaseStrategy` class to create your own strategies:

```python
from swarm_trading_bot.strategies.base import BaseStrategy
from swarm_trading_bot.models import Holdings

class MyCustomStrategy(BaseStrategy):
    def should_trade(self, holdings: Holdings) -> bool:
        # Implement your trading logic
        return True  # or False

    def get_trade_params(self, holdings: Holdings) -> dict:
        # Return trade parameters
        return {
            'sell_token': '0x...',
            'buy_token': '0x...',
            'sell_percentage': 10,
            'slippage_percentage': 1.0
        }
```

## 📈 Monitoring

The bot provides comprehensive logging:

- **Console output**: Real-time status updates
- **Log file**: Detailed execution logs (`trading_bot.log`)
- **Trade history**: Track all executed trades

Monitor log files:
```bash
tail -f trading_bot.log
```

## ⚠️ Important Notes

1. **Manager Access Required**: You must be a swarm manager to execute trades
2. **Test First**: Always run in dry-run mode first to test your configuration
3. **Price Feeds**: The price-based strategy uses simplified price tracking. For production, integrate with proper price oracles (Chainlink, Uniswap TWAP, etc.)
4. **Gas Costs**: Each transaction incurs gas fees on Base
5. **Platform Fees**: Swarm Vault charges a 0.5% fee on swaps
6. **Security**: Keep your API key secure. Never commit it to version control

## 🐛 Troubleshooting

**API Key Error:**
- Verify your API key starts with `svk_`
- Make sure you copied the full key from Swarm Vault settings

**Not a Manager Error:**
- Only swarm managers can execute trades
- Verify you created the swarm or were added as a manager

**No Tokens to Trade:**
- Check your swarm holdings with `python scripts/check_holdings.py`
- Ensure members have balances of the tokens you're trying to trade

**Import Errors:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📚 Resources

- [Swarm Vault Website](https://swarmvault.xyz)
- [Swarm Vault API Documentation](https://api.swarmvault.xyz/api/docs)
- [Base Network](https://base.org)

## ⚡ Quick Start Example

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and configure environment
cp .env.example .env
# Edit .env with your API key

# 3. Copy and configure strategy
cp config.yaml.example config.yaml
# Edit config.yaml with your strategy

# 4. Test with holdings check
python scripts/check_holdings.py

# 5. Preview a swap (no execution)
python scripts/test_swap.py

# 6. Run bot in dry-run mode
python bot.py

# 7. When ready for live trading:
# Edit .env: TRADING_ENABLED=true, DRY_RUN=false
python bot.py
```

---

**Built with ❤️ for the Swarm Vault community**
