# Coinspot API Wrapper

A Python wrapper for the Coinspot cryptocurrency exchange API, providing easy access to both public and authenticated endpoints.

## Features

- Supports Coinspot API v2
- Access to public, read-only, and full access API endpoints
- Type hinting for improved code completion and error checking
- Comprehensive test suite
- Easy-to-use interface for common operations

## Installation

To install the Coinspot API wrapper, run the following command:

```bash
pip install coinspot-api
```

## Usage (General)

Here's a quick example of how to use the Coinspot API wrapper:

```python
from coinspot import create_coinspot_api

# Create an instance of the API (public endpoints only)
api = create_coinspot_api()

# Get latest prices
latest_prices = api.latest_prices()
print(latest_prices)

# For authenticated endpoints, provide your API key and secret
api = create_coinspot_api(api_key="your_api_key", api_secret="your_api_secret")

# Get your account balance
balance = api.balance()
print(balance)
```

## Usage (using Types)

Here are examples of how to use the Coinspot API wrapper, including type annotations for improved code completion and error checking:

```python
from coinspot import create_coinspot_api, Coinspot
from coinspot import (
    LatestPricesResponse,
    LatestCoinPricesResponse,
    LatestBuySellPriceResponse,
    MyCoinBalancesResponse,
    PlaceMarketBuySellOrderResponse
)

# Create an instance of the API (public endpoints only)
api: Coinspot = create_coinspot_api()

# Get latest prices
latest_prices: LatestPricesResponse = api.latest_prices()
print(f"Bitcoin price: ${latest_prices['prices']['BTC']['last']}")

# Get latest price for a specific coin
btc_price: LatestCoinPricesResponse = api.latest_coin_price("BTC")
print(f"Bitcoin bid price: ${btc_price['prices']['bid']}")

# Get latest buy price for a specific coin
eth_buy_price: LatestBuySellPriceResponse = api.latest_buy_price("ETH")
print(f"Ethereum buy price: ${eth_buy_price['rate']}")

# For authenticated endpoints, provide your API key and secret
api = create_coinspot_api(api_key="your_api_key", api_secret="your_api_secret")

# Get your account balance
balance: MyCoinBalancesResponse = api.balance()
for coin_balance in balance["balances"]:
    for coin, details in coin_balance.items():
        print(f"{coin} balance: {details['balance']}, AUD value: ${details['audbalance']}")

# Place a market buy order
buy_order: PlaceMarketBuySellOrderResponse = api.market_buy_order("BTC", amount=0.01, rate=50000)
print(f"Buy order placed: {buy_order['id']}")

# Error handling
try:
    invalid_coin_price = api.latest_coin_price("INVALID_COIN")
except CoinspotApiError as e:
    print(f"An API error occurred: {e.status} - {e.message}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

This example demonstrates how to use the Coinspot API wrapper with type annotations. By specifying the expected return types, you can benefit from better code completion in your IDE and catch potential type-related errors earlier in the development process.

Remember to replace `"your_api_key"` and `"your_api_secret"` with your actual Coinspot API credentials when using authenticated endpoints.

## Error Handling

The Coinspot API wrapper now throws a `CoinspotApiError` exception when an API call doesn't return a status of "ok". You can catch and handle these exceptions in your code:

```python
from coinspot import create_coinspot_api, CoinspotApiError

try:
    api = create_coinspot_api("your_api_key", "your_api_secret")
    latest_prices = api.latest_prices()
    print(latest_prices)
except CoinspotApiError as e:
    print(f"An API error occurred: {e.status} - {e.message}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
```

This allows for more robust error handling in applications using this API wrapper.


## API Reference

The wrapper provides access to the following Coinspot API endpoints:

### Public API

- `latest_prices()`: Get latest prices for all coins
- `latest_coin_price(coin: str)`: Get latest price for a specific coin
- `latest_buy_price(coin: str)`: Get latest buy price for a specific coin
- `latest_sell_price(coin: str)`: Get latest sell price for a specific coin
- `open_order_list(coin: str)`: Get open orders for a specific coin
- `completed_order_list(coin: str)`: Get completed orders for a specific coin

### Read-Only API

- `read_only_api_status()`: Check read-only API status
- `coin_balance(coin: str)`: Get balance for a specific coin
- `balance()`: Get balance for all coins

### Full Access API

- `full_access_api_status()`: Check full access API status
- `coin_deposit_address(coin: str)`: Get deposit address for a specific coin
- `market_buy_order(coin: str, amount: float, rate: float, market_type: Optional[str] = None)`: Place a market buy order
- `market_sell_order(coin: str, amount: float, rate: float, market_type: Optional[str] = None)`: Place a market sell order
- `buy_now_order(coin: str, amount_type: str, amount: float, ...)`: Place a buy now order
- `sell_now_order(coin: str, amount_type: str, amount: float, ...)`: Place a sell now order
- `swap_now(coin_type_sell: str, coin_type_buy: str, amount: float, ...)`: Place a swap order
- `withdraw_coins(coin: str, amount: float, address: str, ...)`: Withdraw coins

For a full list of available methods and their parameters, please refer to the source code or generated documentation.

## Testing

To run the test suite, first set up your API key and secret as environment variables:

```bash
export COINSPOT_API_KEY=your_api_key
export COINSPOT_API_SECRET=your_api_secret
```

Then run the tests using pytest:

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the BSD 3-Clause License.

## Donations

If you find this project helpful, consider supporting its development with a DOGECOIN donation:

Ð: `D8hDbe3YX1umuvKKFukKNEhicDA8of5JCR`

## Disclaimer

This project is not officially associated with or endorsed by Coinspot. Use at your own risk.
