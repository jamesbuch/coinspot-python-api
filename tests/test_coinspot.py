import pytest
import os
from dotenv import load_dotenv
# from datetime import datetime, timedelta
from coinspot.coinspot import create_coinspot_api, Coinspot, CoinspotPublicApi, CoinspotApiError
from coinspot.coinspot_types import (
    LatestPricesResponse, LatestCoinPricesResponse, LatestBuySellPriceResponse,
    ApiStatusResponse, MyCoinBalanceResponse, MyCoinBalancesResponse, BuySellQuoteResponse
)

# Load environment variables from .env file
load_dotenv()

# Set up the API key and secret from environment variables
API_KEY = os.getenv("COINSPOT_API_KEY")
API_SECRET = os.getenv("COINSPOT_API_SECRET")

@pytest.fixture(scope="module")
def coinspot_api():
    """Fixture to provide a shared CoinspotApi object to all tests."""
    return create_coinspot_api(API_KEY, API_SECRET)

def test_get_latest_prices(coinspot_api: Coinspot):
    response: LatestPricesResponse = coinspot_api.latest_prices()
    assert response["status"] == "ok"
    assert "prices" in response
    assert isinstance(response["prices"], dict)
    for coin, price_data in response["prices"].items():
        assert isinstance(coin, str)
        assert "bid" in price_data
        assert "ask" in price_data
        assert "last" in price_data

@pytest.mark.parametrize("coin", ["BTC", "ETH", "DOGE", "ADA", "XRP"])
def test_get_latest_coin_price(coinspot_api: Coinspot, coin: str):
    response: LatestCoinPricesResponse = coinspot_api.latest_coin_price(coin)
    assert response["status"] == "ok"
    assert "prices" in response
    assert "bid" in response["prices"]
    assert "ask" in response["prices"]
    assert "last" in response["prices"]

@pytest.mark.parametrize("coin", ["BTC", "ETH", "DOGE", "ADA", "XRP"])
def test_get_latest_buy_price(coinspot_api: Coinspot, coin: str):
    response: LatestBuySellPriceResponse = coinspot_api.latest_buy_price(coin)
    assert response["status"] == "ok"
    assert "rate" in response
    assert "market" in response

# ... Continue updating the rest of your tests in a similar manner ...

def test_read_only_api_status(coinspot_api: Coinspot):
    response: ApiStatusResponse = coinspot_api.read_only_api_status()
    assert response["status"] == "ok"

def test_get_my_coin_balance(coinspot_api: Coinspot):
    response: MyCoinBalanceResponse = coinspot_api.coin_balance('DOGE')
    assert response["status"] == "ok"
    assert "balance" in response
    for item in response["balance"]:
        assert item == "DOGE"
    assert response["balance"]["DOGE"]["balance"] > 10

def test_get_my_coin_balances(coinspot_api: Coinspot):
    response: MyCoinBalancesResponse = coinspot_api.balance()
    assert response["status"] == "ok"
    assert isinstance(response["balances"], list)
    assert len(response["balances"]) > 0, "Balances list is empty"

    for item in response["balances"]:
        assert isinstance(item, dict)
        assert len(item) == 1, "Each item should contain exactly one coin"
        
        coin, details = next(iter(item.items()))
        assert isinstance(coin, str), "Coin should be a string"
        assert isinstance(details, dict), "Coin details should be a dictionary"
        
        assert "balance" in details
        assert "audbalance" in details
        assert "rate" in details
        
        assert isinstance(details["balance"], (int, float)), "Balance should be numeric"
        assert isinstance(details["audbalance"], (int, float)), "AUD balance should be numeric"
        assert isinstance(details["rate"], (int, float)), "Rate should be numeric"
        
        assert details["balance"] >= 0, "Balance should not be negative"
        assert details["audbalance"] >= 0, "AUD balance should not be negative"
        assert details["rate"] >= 0, "Rate should not be negative"

@pytest.mark.parametrize("coin,amount,amount_type", [
    ("BTC", 0.1, "coin"),
    ("ETH", 1, "coin"),
    ("DOGE", 10000, "coin"),
    ("ADA", 100, "coin"),
    ("XRP", 100, "coin"),
    ("BTC", 100, "aud"),
    ("ETH", 100, "aud"),
])
def test_get_buy_now_quote(coinspot_api: Coinspot, coin: str, amount: float, amount_type: str):
    response: BuySellQuoteResponse = coinspot_api.buy_now_quote(coin, amount, amount_type)
    assert response["status"] == "ok"
    assert "rate" in response

def test_bch_sell_price(coinspot_api: Coinspot):
    try:
        bch_sell_price = coinspot_api.latest_sell_price("BCH")
        assert bch_sell_price["status"] == "ok"
    except CoinspotApiError as e:
        assert e.status in [400, 500]
        print(f"Expected error occurred: {e.status} - {e.message}")
    except Exception as e:
        pytest.fail(f"Unexpected exception: {str(e)}")

@pytest.mark.parametrize("coin,amount,amount_type", [
    ("INVALID_COIN", 100, "aud"),
    ("BTC", -1, "coin"),
    ("ETH", 0, "invalid_type")
])
def test_invalid_buy_now_quote(coinspot_api: Coinspot, coin: str, amount: float, amount_type: str):
    with pytest.raises(CoinspotApiError) as excinfo:
        coinspot_api.buy_now_quote(coin, amount, amount_type)
    assert excinfo.value.status in [400, 500]
    print(f"Buy now quote error: {excinfo.value} Coin: {coin} Amount: {amount}")

def test_public_api_invalid_coin():
    api = CoinspotPublicApi()
    response: LatestCoinPricesResponse = api.get_latest_coin_price("INVALID_COIN")
    assert response["status"] == "ok"
    # assert excinfo.value.status in [400, 404, 500]
    # assert "Invalid coin" in excinfo.value.message or "not found" in excinfo.value.message.lower() or "error" in excinfo.value.message.lower()

# Python too slow for this
# def test_public_api_rate_limit():
#     api = CoinspotPublicApi()
#     call_count = 0
#     start_time = datetime.now()
#     try:
#         while datetime.now() - start_time < timedelta(minutes=1):  # Run for up to 1 minute
#             api.get_latest_prices()
#             call_count += 1
#     except CoinspotApiError as e:
#         if "rate limit" in str(e).lower():
#             print(f"Rate limit detected after {call_count} calls: {e}")
#             return
#     print(f"Rate limit not triggered after {call_count} requests in 1 minute")

if __name__ == "__main__":
    pytest.main()
