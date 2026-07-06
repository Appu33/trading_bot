from decimal import Decimal, InvalidOperation

VALID_ORDER_TYPES = {"MARKET", "LIMIT"}
VALID_SIDES = {"BUY", "SELL"}


class ValidationError(ValueError):
    """Raised when CLI input fails validation."""


def normalize_symbol(symbol: str) -> str:
    cleaned = symbol.strip().upper()
    if not cleaned or not cleaned.endswith("USDT"):
        raise ValidationError("Symbol must be a non-empty USDT-M pair such as BTCUSDT.")
    return cleaned


def normalize_side(side: str) -> str:
    cleaned = side.strip().upper()
    if cleaned not in VALID_SIDES:
        raise ValidationError("Side must be BUY or SELL.")
    return cleaned


def normalize_order_type(order_type: str) -> str:
    cleaned = order_type.strip().upper()
    if cleaned not in VALID_ORDER_TYPES:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return cleaned


def parse_positive_decimal(value: str, field_name: str) -> str:
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, TypeError) as exc:
        raise ValidationError(f"{field_name} must be a valid number.") from exc

    if decimal_value <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")
    return format(decimal_value.normalize(), "f")


def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: str, price: str | None, stop_price: str | None) -> dict:
    normalized_type = normalize_order_type(order_type)
    normalized_price = None

    if normalized_type == "LIMIT":
        if price is None:
            raise ValidationError("Limit orders require --price.")
        normalized_price = parse_positive_decimal(price, "Price")

    return {
        "symbol": normalize_symbol(symbol),
        "side": normalize_side(side),
        "order_type": normalized_type,
        "quantity": parse_positive_decimal(quantity, "Quantity"),
        "price": normalized_price,
        "stop_price": None,
    }
