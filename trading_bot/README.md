# Trading Bot - Binance Futures Testnet

A small Python CLI application for placing Binance Futures Testnet (USDT-M) orders with reusable structure, validation, logging, and error handling.

## Features

- Place `MARKET` and `LIMIT` orders on Binance Futures Testnet
- Supports both `BUY` and `SELL`
- CLI validation for symbol, side, quantity, and price
- Rotating log file output in `logs/trading_bot.log`
- Clear error messages for validation and Binance API failures

## Project Structure

```text
trading_bot/
  bot/
    __init__.py
    client.py
    logging_config.py
    orders.py
    validators.py
  cli.py
  .env.example
  README.md
  requirements.txt
```

## Setup

1. Create and activate a Python 3 virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Binance Futures Testnet credentials.
4. Ensure your Binance Futures Testnet account is active and funded with test USDT.

## Environment Variables

- `BINANCE_API_KEY`
- `BINANCE_API_SECRET`
- `BINANCE_BASE_URL` defaults to `https://testnet.binancefuture.com`
- `BINANCE_RECV_WINDOW` defaults to `5000`
- `TRADING_BOT_LOG_LEVEL` defaults to `INFO`

## Usage

### Market Buy

```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001 --ping
```

### Limit Sell

```bash
python cli.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 70000
```

## Output

The CLI prints:

- validation errors with actionable messages
- API errors returned by Binance
- successful order response payload
- log file location

## Notes for Submission

- Include the generated `logs/trading_bot.log` after running at least one successful and one failed command.
- A failed sample run is easy to generate by omitting `--price` on a `LIMIT` order; a successful run requires valid Binance Futures Testnet credentials in `.env`.
- If you publish this project, do not commit your real `.env` file or API credentials.
