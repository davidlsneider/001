@echo off
REM Swarm Vault Trading Bot - Easy Setup Script for Windows
REM Run this script to set up everything automatically

echo ==================================================
echo Swarm Vault Trading Bot - Setup
echo ==================================================
echo.

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3.7+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%
echo.

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -q requests python-dotenv pyyaml

if %errorlevel% equ 0 (
    echo Dependencies installed successfully
) else (
    echo Failed to install dependencies
    echo Try running manually: pip install requests python-dotenv pyyaml
    pause
    exit /b 1
)
echo.

REM Check for configuration files
echo Checking configuration files...

if not exist ".env" (
    echo .env file not found
    if exist ".env.example" (
        copy .env.example .env >nul
        echo Created .env from .env.example
        echo Please edit .env with your configuration
    )
)

if not exist "config.yaml" (
    echo config.yaml file not found
    if exist "config.yaml.example" (
        copy config.yaml.example config.yaml >nul
        echo Created config.yaml from config.yaml.example
        echo Please edit config.yaml with your strategy
    )
)
echo.

REM Verify files exist
echo Verifying setup...
set READY=true

if exist ".env" (
    echo .env file exists
) else (
    echo .env file missing
    set READY=false
)

if exist "config.yaml" (
    echo config.yaml file exists
) else (
    echo config.yaml file missing
    set READY=false
)

if exist "bot.py" (
    echo bot.py file exists
) else (
    echo bot.py file missing
    set READY=false
)
echo.

REM Final instructions
echo ==================================================
if "%READY%"=="true" (
    echo Setup Complete!
    echo ==================================================
    echo.
    echo Your trading bot is ready to run!
    echo.
    echo Configuration:
    echo    - API Key: Configured in .env
    echo    - Swarm ID: f510fb98-a154-40ab-8e55-614c2061b385
    echo    - Strategy: DCA ^(USDC to WETH^)
    echo    - Mode: DRY RUN ^(safe - no real trades^)
    echo.
    echo To start the bot:
    echo    python bot.py
    echo.
    echo To test utilities:
    echo    python scripts/check_holdings.py
    echo    python scripts/test_swap.py
    echo.
    echo To stop the bot:
    echo    Press Ctrl+C
    echo.
    echo The bot is in DRY-RUN mode ^(no real trades^)
    echo To enable live trading, edit .env:
    echo    DRY_RUN=false
    echo.
) else (
    echo Setup Incomplete
    echo ==================================================
    echo.
    echo Please ensure all required files are present:
    echo    - .env ^(API configuration^)
    echo    - config.yaml ^(trading strategy^)
    echo    - bot.py ^(main bot script^)
    echo.
)

pause
