import logging
from typing import Any

from bot.client import BinanceFuturesTestnetClient

LOGGER = logging.getLogger(__name__)


class OrderService:
    def __init__(self, client: BinanceFuturesTestnetClient) -> None:
        self.client = client

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str | None = None,
        time_in_force: str = "GTC",
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force

        LOGGER.info(
            "Placing %s order: symbol=%s side=%s quantity=%s",
            order_type,
            symbol,
            side,
            quantity,
        )
        response = self.client.place_order(params)
        LOGGER.info(
            "Order accepted: orderId=%s status=%s symbol=%s",
            response.get("orderId"),
            response.get("status"),
            response.get("symbol"),
        )
        return response
