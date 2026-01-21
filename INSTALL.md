# Easy Installation Guide

Get your Swarm Vault trading bot running in 3 simple steps!

## 🚀 Quick Install

### For Mac/Linux:
```bash
./setup.sh
```

### For Windows:
```bash
setup.bat
```

That's it! The script will:
- ✅ Check Python installation
- ✅ Install all dependencies
- ✅ Verify configuration files
- ✅ Show you how to run the bot

## 📋 What Gets Installed

The setup script installs these Python packages:
- `requests` - For API calls
- `python-dotenv` - For environment variables
- `pyyaml` - For configuration files

## 🎯 After Installation

**Run the bot:**
```bash
python bot.py
```

**Check your swarm holdings:**
```bash
python scripts/check_holdings.py
```

**Preview a swap:**
```bash
python scripts/test_swap.py
```

## ⚙️ Your Configuration

The bot is already configured with:
- ✅ API Key: svk_exeQroSS_y00yfUqufFV2HylfrJnA1YKWMsXcPzZHEc
- ✅ Swarm ID: f510fb98-a154-40ab-8e55-614c2061b385
- ✅ Strategy: DCA (Buy WETH with 10% of USDC every 5 minutes)
- ✅ Mode: DRY-RUN (no real trades - safe for testing)

## 🔒 Safety Features

The bot starts in **DRY-RUN mode** which means:
- ✅ Shows what trades it WOULD execute
- ✅ Previews all swaps
- ✅ Logs everything
- ❌ Does NOT execute real trades

## 🚦 To Enable Live Trading

Only when you're ready:

1. Edit `.env` file
2. Change `DRY_RUN=true` to `DRY_RUN=false`
3. Run `python bot.py`

## 🐛 Troubleshooting

**"Python not found"**
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**"Permission denied" (Mac/Linux)**
```bash
chmod +x setup.sh
./setup.sh
```

**"pip: command not found"**
```bash
python -m pip install requests python-dotenv pyyaml
```

**Still having issues?**
- Check QUICKSTART.md for detailed instructions
- Check README.md for full documentation

## 📚 Next Steps

1. Run `./setup.sh` (or `setup.bat` on Windows)
2. Run `python bot.py` to start in dry-run mode
3. Watch the logs and verify it works
4. When ready, enable live trading in `.env`

---

**Ready? Run the setup script now!**

```bash
# Mac/Linux
./setup.sh

# Windows
setup.bat
```
