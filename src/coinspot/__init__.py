# src/coinspot_api/__init__.py

# Import main classes and functions
from .coinspot import Coinspot, create_coinspot_api, CoinspotPublicApi, CoinspotApiError

# Import all types
from .coinspot_types import (
    ApiStatusResponse,
    BaseApiResponse,
    PriceData,
    LatestPricesResponse,
    LatestCoinPricesResponse,
    LatestBuySellPriceResponse,
    OpenOrder,
    OpenOrdersResponse,
    CompletedOrder,
    CompletedOrdersResponse,
    Network,
    CoinDepositAddressResponse,
    BuySellQuoteResponse,
    SwapQuoteResponse,
    PlaceMarketBuySellOrderResponse,
    EditOpenMarketBuySellOrderResponse,
    PlaceBuySellNowOrderResponse,
    PlaceSwapNowOrderResponse,
    CancelOrderResponse,
    NetworkWithdrawalDetails,
    CoinWithdrawalDetailsResponse,
    WithdrawCoinResponse,
    CoinBalance,
    MyCoinBalancesResponse,
    MyCoinBalanceResponse
)

# Define what should be imported when someone does `from coinspot_api import *`
__all__ = [
    'Coinspot',
    'create_coinspot_api',
    'CoinspotApiError',
    'CoinspotPublicApi',
    'ApiStatusResponse',
    'BaseApiResponse',
    'PriceData',
    'LatestPricesResponse',
    'LatestCoinPricesResponse',
    'LatestBuySellPriceResponse',
    'OpenOrder',
    'OpenOrdersResponse',
    'CompletedOrder',
    'CompletedOrdersResponse',
    'Network',
    'CoinDepositAddressResponse',
    'BuySellQuoteResponse',
    'SwapQuoteResponse',
    'PlaceMarketBuySellOrderResponse',
    'EditOpenMarketBuySellOrderResponse',
    'PlaceBuySellNowOrderResponse',
    'PlaceSwapNowOrderResponse',
    'CancelOrderResponse',
    'NetworkWithdrawalDetails',
    'CoinWithdrawalDetailsResponse',
    'WithdrawCoinResponse',
    'CoinBalance',
    'MyCoinBalancesResponse',
    'MyCoinBalanceResponse'
]

# You can also add metadata about your package
__version__ = "0.1.0"
__author__ = "James Buchanan"
__license__ = "BSD 3 Clause"
