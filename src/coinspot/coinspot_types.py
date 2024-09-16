from typing import Optional, Dict, Any, List, Union

# Type definitions for API responses
class ApiStatusResponse:
    status: str

class BaseApiResponse(Dict[str, Any]):
    status: str
    message: Optional[str]

class PriceData(Dict[str, float]):
    bid: float
    ask: float
    last: float

class LatestPricesResponse(BaseApiResponse):
    prices: Dict[str, PriceData]

class LatestCoinPricesResponse(BaseApiResponse):
    prices: PriceData

class LatestBuySellPriceResponse(BaseApiResponse):
    rate: str
    market: str

class OpenOrder(Dict[str, Union[float, str]]):
    amount: float
    rate: float
    total: float
    coin: str
    market: str

class OpenOrdersResponse(BaseApiResponse):
    buyorders: List[OpenOrder]
    sellorders: List[OpenOrder]

class CompletedOrder(OpenOrder):
    solddate: str

class CompletedOrdersResponse(BaseApiResponse):
    buyorders: List[CompletedOrder]
    sellorders: List[CompletedOrder]

class Network(Dict[str, str]):
    name: str
    network: str
    address: str
    memo: str

class CoinDepositAddressResponse(BaseApiResponse):
    networks: List[Network]

class BuySellQuoteResponse(BaseApiResponse):
    rate: float

class SwapQuoteResponse(BaseApiResponse):
    rate: float

class PlaceMarketBuySellOrderResponse(BaseApiResponse):
    coin: str
    market: str
    amount: float
    rate: float
    id: str

class EditOpenMarketBuySellOrderResponse(BaseApiResponse):
    updated: bool
    id: str
    coin: str
    rate: float
    newrate: float
    amount: float
    total: float

class PlaceBuySellNowOrderResponse(BaseApiResponse):
    coin: str
    amount: float
    market: str
    total: float

class PlaceSwapNowOrderResponse(BaseApiResponse):
    coin: str
    amount: float
    rate: float
    market: str
    total: float

class CancelOrderResponse(BaseApiResponse):
    pass

class NetworkWithdrawalDetails(Dict[str, Union[str, float, bool]]):
    network: str
    paymentid: str
    fee: float
    minsend: float
    default: bool

class CoinWithdrawalDetailsResponse(BaseApiResponse):
    networks: List[NetworkWithdrawalDetails]

class WithdrawCoinResponse(BaseApiResponse):
    pass

class CoinBalance(Dict[str, float]):
    balance: float
    audbalance: float
    rate: float

class MyCoinBalancesResponse(BaseApiResponse):
    balances: List[Dict[str, CoinBalance]]

class MyCoinBalanceResponse(BaseApiResponse):
    balance: Dict[str, Union[CoinBalance, Dict[str, Union[float, int]]]]