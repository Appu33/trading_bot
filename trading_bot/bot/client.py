import hashlib
import hmac
import logging
import os
import time
from typing import Any
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

LOGGER = logging.getLogger(__name__)


class BinanceAPIError(RuntimeError):
    """Raised when Binance returns an error response."""


class BinanceFuturesTestnetClient:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://testnet.binancefuture.com",
        recv_window: int = 5000,
        timeout: int = 15,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url.rstrip("/")
        self.recv_window = recv_window
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    @classmethod
    def from_env(cls) -> "BinanceFuturesTestnetClient":
        load_dotenv()
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")
        recv_window = int(os.getenv("BINANCE_RECV_WINDOW", "5000"))

        if not api_key or not api_secret:
            raise BinanceAPIError(
                "Missing Binance credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET."
            )

        return cls(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            recv_window=recv_window,
        )

    def _sign_params(self, params: dict[str, Any]) -> dict[str, Any]:
        signed_params = {**params, "timestamp": int(time.time() * 1000), "recvWindow": self.recv_window}
        query_string = urlencode(signed_params, doseq=True)
        signature = hmac.new(
            self.api_secret,
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        signed_params["signature"] = signature
        return signed_params

    def _request(self, method: str, path: str, signed: bool = False, params: dict[str, Any] | None = None) -> dict[str, Any]:
        request_params = params or {}
        if signed:
            request_params = self._sign_params(request_params)

        url = f"{self.base_url}{path}"
        LOGGER.debug("Sending %s request to %s with params=%s", method, url, request_params)
        response = self.session.request(
            method=method,
            url=url,
            params=request_params,
            timeout=self.timeout,
        )

        try:
            payload = response.json()
        except ValueError as exc:
            raise BinanceAPIError(
                f"Binance returned a non-JSON response with status {response.status_code}."
            ) from exc

        if response.status_code >= 400:
            message = payload.get("msg", "Unknown Binance API error")
            code = payload.get("code", "unknown")
            raise BinanceAPIError(f"Binance API error {code}: {message}")

        return payload

    def ping(self) -> dict[str, Any]:
        return self._request("GET", "/fapi/v1/ping")

    def place_order(self, params: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/fapi/v1/order", signed=True, params=params)
