# Quick Start Guide

Your Swarm Vault trading bot is ready! Here's what you need to do to get started:

## ✅ What's Been Built

I've created a complete trading bot with:
- ✅ Full API client for Swarm Vault
- ✅ 3 trading strategies (DCA, Rebalancing, Price-Based)
- ✅ Risk management controls
- ✅ Dry-run testing mode
- ✅ Comprehensive logging
- ✅ Utility scripts
- ✅ Complete documentation

## 🚀 Next Steps (What YOU Need to Do)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs: `requests`, `python-dotenv`, and `pyyaml`

### 2. Create Your Configuration Files

```bash
# Copy environment variables template
cp .env.example .env

# Copy strategy configuration template
cp config.yaml.example config.yaml
```

### 3. Configure Your .env File

Edit `.env` with your actual values:

```env
SWARM_VAULT_API_KEY=svk_exeQroSS_y00yfUqufFV2HylfrJnA1YKWMsXcPzZHEc
SWARM_VAULT_BASE_URL=https://api.swarmvault.xyz
SWARM_ID=YOUR_SWARM_ID_HERE  # ⚠️ You need to add this!

TRADING_ENABLED=false
DRY_RUN=true  # Keep true for testing
CHECK_INTERVAL_SECONDS=300

LOG_LEVEL=INFO
LOG_FILE=trading_bot.log
```

**⚠️ IMPORTANT:** Replace `YOUR_SWARM_ID_HERE` with your actual swarm ID!

### 4. Get Your Swarm ID

If you don't know your swarm ID:

Option A: Visit [swarmvault.xyz](https://swarmvault.xyz) and look at the URL when viewing your swarm:
```
https://swarmvault.xyz/swarm/abc123...  <-- This is your swarm ID
```

Option B: Run this Python script after configuring your API key (comment out SWARM_ID validation):
```python
from swarm_trading_bot.client import SwarmVaultClient
client = SwarmVaultClient(api_key='svk_exeQroSS_y00yfUqufFV2HylfrJnA1YKWMsXcPzZHEc')
swarms = client.list_swarms()
for swarm in swarms:
    print(f"Swarm: {swarm.name} - ID: {swarm.id} - Manager: {swarm.is_manager}")
```

### 5. Configure Your Trading Strategy

Edit `config.yaml` and choose one of:
- `dca` - Dollar cost averaging (buy at regular intervals)
- `rebalance` - Maintain portfolio allocation
- `price_based` - Trade based on price movements

Example DCA configuration:
```yaml
active_strategy: dca

dca:
  sell_token: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC
  buy_token: "0x4200000000000000000000000000000000000006"   # WETH
  sell_percentage: 10  # Use 10% of USDC balance
  interval_seconds: 86400  # Trade once per day
  slippage_percentage: 1.0
```

### 6. Test Your Setup

**Check your swarm holdings:**
```bash
python scripts/check_holdings.py
```

This will show you all tokens held by your swarm members.

**Preview a swap (no execution):**
```bash
python scripts/test_swap.py
```

This tests the preview functionality without executing any trades.

### 7. Run the Bot in Dry-Run Mode

```bash
python bot.py
```

This will:
- ✅ Verify your API key
- ✅ Connect to your swarm
- ✅ Run your strategy
- ✅ Show what trades WOULD be executed
- ❌ NOT execute any real trades (dry-run mode)

Monitor the output and logs to ensure everything works correctly.

### 8. When Ready for Live Trading

**⚠️ ONLY when you're confident the bot works correctly:**

Edit `.env`:
```env
TRADING_ENABLED=true
DRY_RUN=false
```

Then run:
```bash
python bot.py
```

**CAUTION:** The bot will now execute REAL trades!

## 📋 Pre-Flight Checklist

Before running live:
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with your API key and swarm ID
- [ ] `config.yaml` created with your trading strategy
- [ ] You are a manager of the swarm (check with `check_holdings.py`)
- [ ] Swarm members have token balances to trade
- [ ] You've tested in dry-run mode and verified the strategy
- [ ] You understand the risks and fees (0.5% platform fee + gas)

## 🛟 Troubleshooting

**"SWARM_ID environment variable is required"**
→ Add your swarm ID to `.env` file

**"You must be a swarm manager"**
→ Only managers can execute trades. Make sure you created the swarm or were added as manager.

**"No balance for sell token"**
→ Your swarm members don't have the token you're trying to sell. Check with `check_holdings.py`

**Import errors**
→ Run `pip install -r requirements.txt`

## 📚 Common Token Addresses (Base Mainnet)

```
ETH:   0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
WETH:  0x4200000000000000000000000000000000000006
USDC:  0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913
USDbC: 0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA
DAI:   0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb
```

## 🔒 Security Reminder

- ✅ `.env` is in `.gitignore` (your API key won't be committed)
- ⚠️ Never share your API key publicly
- ⚠️ Start with small amounts when testing live
- ⚠️ Monitor the bot regularly

## 📖 Need More Help?

Check the full README.md for:
- Detailed strategy explanations
- API client usage examples
- Creating custom strategies
- Advanced configuration

---

**Good luck with your trading bot! Start in dry-run mode and be cautious when going live.**
