from typing import Optional, Dict, Any
import time
import hmac
import hashlib
import json
import requests

from coinspot.coinspot_types import ApiStatusResponse, BuySellQuoteResponse, CancelOrderResponse, CoinDepositAddressResponse, CoinWithdrawalDetailsResponse, CompletedOrdersResponse, EditOpenMarketBuySellOrderResponse, LatestBuySellPriceResponse, LatestCoinPricesResponse, LatestPricesResponse, MyCoinBalanceResponse, MyCoinBalancesResponse, OpenOrdersResponse, PlaceBuySellNowOrderResponse, PlaceMarketBuySellOrderResponse, PlaceSwapNowOrderResponse, SwapQuoteResponse, WithdrawCoinResponse

# API Classes

class CoinspotApiError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message
        super().__init__(f"API Error: Status - {status}, Message - {message}")

class CoinspotApiBase:
    def __init__(self, key: Optional[str], secret: Optional[str]):
        self.key = key
        self.secret = secret
        self.base_url = "https://www.coinspot.com.au/api/v2"

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            response.raise_for_status()
            response_data = response.json()
            if response_data.get("status") != "ok":
                raise CoinspotApiError(response_data.get("status"), response_data.get("message", "No error message provided"))
            return response_data
        except requests.HTTPError as http_err:
            raise CoinspotApiError(response.status_code, str(http_err))

    def _request(self, path: str, data: Dict[str, Any] = {}, read_only: bool = False) -> Dict[str, Any]:
        nonce = int(time.time()*1000)
        payload = {"nonce": nonce, **data}
        payload_str = json.dumps(payload, separators=(',', ':'))

        digest = hmac.new(self.secret.encode(), payload_str.encode(), hashlib.sha512)
        signature = digest.hexdigest()

        headers = {
            "Content-Type": "application/json",
            "sign": signature,
            "key": self.key,
        }

        url = f"{self.base_url}{'/ro' if read_only else ''}{path}"
        response = requests.post(url, headers=headers, data=payload_str)
        return self._handle_response(response)


class CoinspotPublicApi:
    def __init__(self):
        self.base_url = "https://www.coinspot.com.au/pubapi/v2"

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            response.raise_for_status()
            response_data = response.json()
            if response_data.get("status") != "ok":
                raise CoinspotApiError(response_data.get("status"), response_data.get("message", "No error message provided"))
            return response_data
        except requests.HTTPError as http_err:
            raise CoinspotApiError(response.status_code, str(http_err))

    def _get(self, path: str) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}{path}")
        return self._handle_response(response)

    def get_latest_prices(self) -> LatestPricesResponse:
        return self._get("/latest")

    def get_latest_coin_price(self, cointype: str) -> LatestCoinPricesResponse:
        return self._get(f"/latest/{cointype}")

    def get_latest_coin_market_price(self, cointype: str, markettype: str) -> LatestCoinPricesResponse:
        return self._get(f"/latest/{cointype}/{markettype}")

    def get_latest_buy_price(self, cointype: str) -> LatestBuySellPriceResponse:
        return self._get(f"/buyprice/{cointype}")

    def get_latest_buy_market_price(self, cointype: str, markettype: str) -> LatestBuySellPriceResponse:
        return self._get(f"/buyprice/{cointype}/{markettype}")

    def get_latest_sell_price(self, cointype: str) -> LatestBuySellPriceResponse:
        return self._get(f"/sellprice/{cointype}")

    def get_latest_sell_market_price(self, cointype: str, markettype: str) -> LatestBuySellPriceResponse:
        return self._get(f"/sellprice/{cointype}/{markettype}")

    def get_open_orders(self, cointype: str) -> OpenOrdersResponse:
        return self._get(f"/orders/open/{cointype}")

    def get_open_market_orders(self, cointype: str, markettype: str) -> OpenOrdersResponse:
        return self._get(f"/orders/open/{cointype}/{markettype}")

    def get_completed_orders(self, cointype: str) -> CompletedOrdersResponse:
        return self._get(f"/orders/completed/{cointype}")

    def get_completed_market_orders(self, cointype: str, markettype: str) -> CompletedOrdersResponse:
        return self._get(f"/orders/completed/{cointype}/{markettype}")


class CoinspotReadOnlyApi(CoinspotApiBase):
    
    def check_read_only_api_status(self) -> ApiStatusResponse:
        return self._request("/status", {}, True)

    def get_open_market_orders(self, cointype: Optional[str] = None, markettype: Optional[str] = None) -> OpenOrdersResponse:
        return self._request("/orders/market/open", {"cointype": cointype, "markettype": markettype}, True)

    def get_completed_market_orders(self, cointype: str, markettype: Optional[str] = None, 
                                    startdate: Optional[str] = None, enddate: Optional[str] = None, 
                                    limit: Optional[int] = None) -> CompletedOrdersResponse:
        data = {"cointype": cointype, "markettype": markettype, "startdate": startdate, "enddate": enddate, "limit": limit}
        return self._request("/orders/market/completed", {k: v for k, v in data.items() if v is not None}, True)

    def get_my_coin_balances(self) -> MyCoinBalancesResponse:
        return self._request("/my/balances", {}, True)

    def get_my_coin_balance(self, cointype: str, available: str) -> MyCoinBalanceResponse:
        return self._request(f"/my/balance/{cointype}", {"available": available}, True)

    def get_my_open_market_orders(self, cointype: Optional[str] = None, markettype: Optional[str] = None) -> OpenOrdersResponse:
        return self._request("/my/orders/market/open", {"cointype": cointype, "markettype": markettype}, True)

    def get_my_open_limit_orders(self, cointype: Optional[str] = None) -> OpenOrdersResponse:
        return self._request("/my/orders/limit/open", {"cointype": cointype}, True)

    def get_my_order_history(self, cointype: Optional[str] = None, markettype: Optional[str] = None, 
                             startdate: Optional[str] = None, enddate: Optional[str] = None, 
                             limit: Optional[int] = None) -> CompletedOrdersResponse:
        data = {"cointype": cointype, "markettype": markettype, "startdate": startdate, "enddate": enddate, "limit": limit}
        return self._request("/my/orders/completed", {k: v for k, v in data.items() if v is not None}, True)

    def get_my_market_order_history(self, cointype: Optional[str] = None, markettype: Optional[str] = None, 
                                    startdate: Optional[str] = None, enddate: Optional[str] = None, 
                                    limit: Optional[int] = None) -> CompletedOrdersResponse:
        data = {"cointype": cointype, "markettype": markettype, "startdate": startdate, "enddate": enddate, "limit": limit}
        return self._request("/my/orders/market/completed", {k: v for k, v in data.items() if v is not None}, True)

    def get_my_send_receive_history(self, startdate: Optional[str] = None, enddate: Optional[str] = None) -> Dict[str, Any]:
        return self._request("/my/sendreceive", {"startdate": startdate, "enddate": enddate}, True)

    def get_my_deposit_history(self, startdate: Optional[str] = None, enddate: Optional[str] = None) -> Dict[str, Any]:
        return self._request("/my/deposits", {"startdate": startdate, "enddate": enddate}, True)

    def get_my_withdrawal_history(self, startdate: Optional[str] = None, enddate: Optional[str] = None) -> Dict[str, Any]:
        return self._request("/my/withdrawals", {"startdate": startdate, "enddate": enddate}, True)

    def get_my_affiliate_payments(self) -> Dict[str, Any]:
        return self._request("/my/affiliatepayments", {}, True)

    def get_my_referral_payments(self) -> Dict[str, Any]:
        return self._request("/my/referralpayments", {}, True)


# Authenticated API, methods which do something are in here, unlike read-only API

class CoinspotApi(CoinspotApiBase):
    def check_full_access_api_status(self) -> ApiStatusResponse:
        return self._request("/status")

    def get_coin_deposit_address(self, cointype: str) -> CoinDepositAddressResponse:
        return self._request("/my/coin/deposit", {"cointype": cointype})

    def get_buy_now_quote(self, cointype: str, amount: float, amounttype: str) -> BuySellQuoteResponse:
        return self._request("/quote/buy/now", {"cointype": cointype, "amount": amount, "amounttype": amounttype})

    def get_sell_now_quote(self, cointype: str, amount: float, amounttype: str) -> BuySellQuoteResponse:
        return self._request("/quote/sell/now", {"cointype": cointype, "amount": amount, "amounttype": amounttype})

    def get_swap_now_quote(self, cointypesell: str, cointypebuy: str, amount: float) -> SwapQuoteResponse:
        return self._request("/quote/swap/now", {"cointypesell": cointypesell, "cointypebuy": cointypebuy, "amount": amount})

    def place_market_buy_order(self, cointype: str, amount: float, rate: float, markettype: Optional[str] = None) -> PlaceMarketBuySellOrderResponse:
        return self._request("/my/buy", {"cointype": cointype, "amount": amount, "rate": rate, "markettype": markettype})

    def edit_open_market_buy_order(self, cointype: str, id: str, rate: float, newrate: float) -> EditOpenMarketBuySellOrderResponse:
        return self._request("/my/buy/edit", {"cointype": cointype, "id": id, "rate": rate, "newrate": newrate})

    def place_buy_now_order(self, cointype: str, amounttype: str, amount: float, rate: Optional[float] = None, 
                            threshold: Optional[float] = None, direction: Optional[str] = None) -> PlaceBuySellNowOrderResponse:
        data = {"cointype": cointype, "amounttype": amounttype, "amount": amount, "rate": rate, 
                "threshold": threshold, "direction": direction}
        return self._request("/my/buy/now", {k: v for k, v in data.items() if v is not None})

    def place_market_sell_order(self, cointype: str, amount: float, rate: float, markettype: Optional[str] = None) -> PlaceMarketBuySellOrderResponse:
        return self._request("/my/sell", {"cointype": cointype, "amount": amount, "rate": rate, "markettype": markettype})

    def edit_open_market_sell_order(self, cointype: str, id: str, rate: float, newrate: float) -> EditOpenMarketBuySellOrderResponse:
        return self._request("/my/sell/edit", {"cointype": cointype, "id": id, "rate": rate, "newrate": newrate})

    def place_sell_now_order(self, cointype: str, amounttype: str, amount: float, rate: Optional[float] = None, 
                             threshold: Optional[float] = None, direction: Optional[str] = None) -> PlaceBuySellNowOrderResponse:
        data = {"cointype": cointype, "amounttype": amounttype, "amount": amount, "rate": rate, 
                "threshold": threshold, "direction": direction}
        return self._request("/my/sell/now", {k: v for k, v in data.items() if v is not None})

    def place_swap_now_order(self, cointypesell: str, cointypebuy: str, amount: float, rate: Optional[float] = None, 
                             threshold: Optional[float] = None, direction: Optional[str] = None) -> PlaceSwapNowOrderResponse:
        data = {"cointypesell": cointypesell, "cointypebuy": cointypebuy, "amount": amount, "rate": rate, 
                "threshold": threshold, "direction": direction}
        return self._request("/my/swap/now", {k: v for k, v in data.items() if v is not None})

    def cancel_buy_order(self, id: str) -> CancelOrderResponse:
        return self._request("/my/buy/cancel", {"id": id})

    def cancel_all_buy_orders(self, coin: Optional[str] = None) -> CancelOrderResponse:
        return self._request("/my/buy/cancel/all", {"coin": coin} if coin else {})

    def cancel_sell_order(self, id: str) -> CancelOrderResponse:
        return self._request("/my/sell/cancel", {"id": id})

    def cancel_all_sell_orders(self, coin: Optional[str] = None) -> CancelOrderResponse:
        return self._request("/my/sell/cancel/all", {"coin": coin} if coin else {})

    def get_coin_withdrawal_details(self, cointype: str) -> CoinWithdrawalDetailsResponse:
        return self._request("/my/coin/withdraw/senddetails", {"cointype": cointype})

    def withdraw_coin(self, cointype: str, amount: float, address: str, emailconfirm: Optional[str] = None, 
                      network: Optional[str] = None, paymentid: Optional[str] = None) -> WithdrawCoinResponse:
        data = {"cointype": cointype, "amount": amount, "address": address, "emailconfirm": emailconfirm, 
                "network": network, "paymentid": paymentid}
        return self._request("/my/coin/withdraw/send", {k: v for k, v in data.items() if v is not None})


# A more simplified API, wrapper around the Public, Read-Only and Full Access APIs
class Coinspot:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.public: CoinspotPublicApi = CoinspotPublicApi()
        self.read_only: Optional[CoinspotReadOnlyApi] = CoinspotReadOnlyApi(api_key, api_secret) if api_key and api_secret else None
        self.authenticated: Optional[CoinspotApi] = CoinspotApi(api_key, api_secret) if api_key and api_secret else None
    
    def latest_coin_price(self, coin: str) -> LatestCoinPricesResponse:
        return self.public.get_latest_coin_price(coin)

    def latest_prices(self) -> LatestPricesResponse:
        return self.public.get_latest_prices()

    def latest_buy_price(self, coin: str) -> LatestBuySellPriceResponse:
        return self.public.get_latest_buy_price(coin)

    def latest_sell_price(self, coin: str) -> LatestBuySellPriceResponse:
        return self.public.get_latest_sell_price(coin)

    def open_order_list(self, coin: str) -> OpenOrdersResponse:
        return self.public.get_open_orders(coin)

    def completed_order_list(self, coin: str) -> CompletedOrdersResponse:
        return self.public.get_completed_orders(coin)

    def coin_balance(self, coin: str) -> MyCoinBalanceResponse:
        if not self.read_only:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.read_only.get_my_coin_balance(coin, "yes")

    def balance(self) -> MyCoinBalancesResponse:
        if not self.read_only:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.read_only.get_my_coin_balances()

    def read_only_api_status(self) -> ApiStatusResponse:
        if not self.read_only:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.read_only.check_read_only_api_status()
    
    def full_access_api_status(self) -> ApiStatusResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.check_full_access_api_status()

    def coin_deposit_address(self, coin: str) -> CoinDepositAddressResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.get_coin_deposit_address(coin)

    def market_buy_order(self, coin: str, amount: float, rate: float, market_type: Optional[str] = None) -> PlaceMarketBuySellOrderResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.place_market_buy_order(coin, amount, rate, market_type)

    def market_sell_order(self, coin: str, amount: float, rate: float, market_type: Optional[str] = None) -> PlaceMarketBuySellOrderResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.place_market_sell_order(coin, amount, rate, market_type)

    def cancel_buy_order(self, id: str) -> CancelOrderResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.cancel_buy_order(id)

    def cancel_sell_order(self, id: str) -> CancelOrderResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.cancel_sell_order(id)

    def buy_now_order(self, coin: str, amount_type: str, amount: float, rate: Optional[float] = None, 
                      threshold: Optional[float] = None, direction: Optional[str] = None) -> PlaceBuySellNowOrderResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.place_buy_now_order(coin, amount_type, amount, rate, threshold, direction)

    def sell_now_order(self, coin: str, amount_type: str, amount: float, rate: Optional[float] = None, 
                       threshold: Optional[float] = None, direction: Optional[str] = None) -> PlaceBuySellNowOrderResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.place_sell_now_order(coin, amount_type, amount, rate, threshold, direction)

    def swap_now(self, coin_type_sell: str, coin_type_buy: str, amount: float, rate: Optional[float] = None, 
                 threshold: Optional[float] = None, direction: Optional[str] = None) -> PlaceSwapNowOrderResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.place_swap_now_order(coin_type_sell, coin_type_buy, amount, rate, threshold, direction)

    def buy_now_quote(self, coin: str, amount: float, amount_type: str) -> BuySellQuoteResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.get_buy_now_quote(coin, amount, amount_type)

    def sell_now_quote(self, coin: str, amount: float, amount_type: str) -> BuySellQuoteResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.get_sell_now_quote(coin, amount, amount_type)

    def swap_now_quote(self, sell_coin: str, buy_coin: str, amount: float) -> SwapQuoteResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.get_swap_now_quote(sell_coin, buy_coin, amount)

    def withdrawal_history(self, coin: str) -> CoinWithdrawalDetailsResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.get_coin_withdrawal_details(coin)

    def withdraw_coins(self, coin: str, amount: float, address: str, email_confirm: Optional[str] = None, 
                       network: Optional[str] = None, payment_id: Optional[str] = None) -> WithdrawCoinResponse:
        if not self.authenticated:
            raise ValueError("API key and secret are required for authenticated operations")
        return self.authenticated.withdraw_coin(coin, amount, address, email_confirm, network, payment_id)


def create_coinspot_api(api_key: Optional[str] = None, api_secret: Optional[str] = None) -> Coinspot:
    try:
        return Coinspot(api_key, api_secret)
    except Exception as e:
        raise CoinspotApiError("Initialization Error", str(e))