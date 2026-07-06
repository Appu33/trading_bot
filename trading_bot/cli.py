import argparse
import logging
import os
import sys
from pprint import pformat

from bot.client import BinanceAPIError, BinanceFuturesTestnetClient
from bot.logging_config import configure_logging
from bot.orders import OrderService
from bot.validators import ValidationError, validate_order_inputs

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place Binance Futures Testnet orders from the command line."
    )
    parser.add_argument("--symbol", required=True, help="USDT-M symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"])
    parser.add_argument(
        "--order-type",
        required=True,
        choices=["MARKET", "LIMIT", "market", "limit"],
        help="Order type to place",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Limit price")
    parser.add_argument(
        "--time-in-force",
        default="GTC",
        choices=["GTC", "IOC", "FOK"],
        help="Time in force for LIMIT orders",
    )
    parser.add_argument(
        "--ping",
        action="store_true",
        help="Check connectivity to Binance Futures Testnet before placing the order",
    )
    return parser


def main() -> int:
    log_level = os.getenv("TRADING_BOT_LOG_LEVEL", "INFO")
    log_file = configure_logging(log_level)
    parser = build_parser()
    args = parser.parse_args()

    try:
        validated = validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=None,
        )
        client = BinanceFuturesTestnetClient.from_env()
        if args.ping:
            client.ping()
            print("Connectivity check succeeded.")

        service = OrderService(client)
        response = service.place_order(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["order_type"],
            quantity=validated["quantity"],
            price=validated["price"],
            time_in_force=args.time_in_force,
        )
    except ValidationError as exc:
        LOGGER.error("Validation failed: %s", exc)
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    except BinanceAPIError as exc:
        LOGGER.error("Binance request failed: %s", exc)
        print(f"API error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        LOGGER.exception("Unexpected failure")
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

    print("Order placed successfully.")
    print(pformat(response))
    print(f"Log file: {log_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
