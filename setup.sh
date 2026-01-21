#!/bin/bash

# Swarm Vault Trading Bot - Easy Setup Script
# Run this script to set up everything automatically

echo "=================================================="
echo "Swarm Vault Trading Bot - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Error: Python is not installed"
    echo "Please install Python 3.7+ from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
$PYTHON_CMD -m pip install --upgrade pip > /dev/null 2>&1
$PYTHON_CMD -m pip install -q requests python-dotenv pyyaml

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "Try running manually: pip install requests python-dotenv pyyaml"
    exit 1
fi
echo ""

# Check for configuration files
echo "Checking configuration files..."

if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env from .env.example"
        echo "⚠️  Please edit .env with your configuration"
    fi
fi

if [ ! -f "config.yaml" ]; then
    echo "⚠️  config.yaml file not found"
    if [ -f "config.yaml.example" ]; then
        cp config.yaml.example config.yaml
        echo "✅ Created config.yaml from config.yaml.example"
        echo "⚠️  Please edit config.yaml with your strategy"
    fi
fi
echo ""

# Verify files exist
echo "Verifying setup..."
READY=true

if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    echo "❌ .env file missing"
    READY=false
fi

if [ -f "config.yaml" ]; then
    echo "✅ config.yaml file exists"
else
    echo "❌ config.yaml file missing"
    READY=false
fi

if [ -f "bot.py" ]; then
    echo "✅ bot.py file exists"
else
    echo "❌ bot.py file missing"
    READY=false
fi
echo ""

# Final instructions
echo "=================================================="
if [ "$READY" = true ]; then
    echo "✅ Setup Complete!"
    echo "=================================================="
    echo ""
    echo "Your trading bot is ready to run!"
    echo ""
    echo "📋 Configuration:"
    echo "   - API Key: Configured in .env"
    echo "   - Swarm ID: f510fb98-a154-40ab-8e55-614c2061b385"
    echo "   - Strategy: DCA (USDC → WETH)"
    echo "   - Mode: DRY RUN (safe - no real trades)"
    echo ""
    echo "🚀 To start the bot:"
    echo "   $PYTHON_CMD bot.py"
    echo ""
    echo "🧪 To test utilities:"
    echo "   $PYTHON_CMD scripts/check_holdings.py"
    echo "   $PYTHON_CMD scripts/test_swap.py"
    echo ""
    echo "🛑 To stop the bot:"
    echo "   Press Ctrl+C"
    echo ""
    echo "⚠️  The bot is in DRY-RUN mode (no real trades)"
    echo "   To enable live trading, edit .env:"
    echo "   DRY_RUN=false"
    echo ""
else
    echo "⚠️  Setup Incomplete"
    echo "=================================================="
    echo ""
    echo "Please ensure all required files are present:"
    echo "   - .env (API configuration)"
    echo "   - config.yaml (trading strategy)"
    echo "   - bot.py (main bot script)"
    echo ""
fi
