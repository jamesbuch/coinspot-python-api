# Coinspot API Wrapper

A Python wrapper for the Coinspot cryptocurrency exchange API, providing easy access to both public and authenticated endpoints.

## Features

- Supports Coinspot API v2
- Access to public, read-only, and full access API endpoints
- Strong typing for improved code completion and error checking
- Comprehensive error handling with custom `CoinspotApiError` exception
- Separate `CoinspotPublicApi` for unauthenticated access
- Full `CoinspotApi` for authenticated operations
- Comprehensive test suite
- Easy-to-use interface for common operations

## Installation

Coming soon (otherwise clone the repository and use it from there).

To install the Coinspot API wrapper, run the following command:

```bash
pip install coinspot-api
```

## Usage

### Public API (No Authentication)

```python
from coinspot import CoinspotPublicApi
from coinspot.coinspot_types import LatestPricesResponse, LatestCoinPricesResponse

public_api = CoinspotPublicApi()

# Get latest prices
latest_prices: LatestPricesResponse = public_api.get_latest_prices()
print(f"Bitcoin price: ${latest_prices['prices']['BTC']['last']}")

# Get latest price for a specific coin
btc_price: LatestCoinPricesResponse = public_api.get_latest_coin_price("BTC")
print(f"Bitcoin bid price: ${btc_price['prices']['bid']}")
```

### Authenticated API

```python
from coinspot import create_coinspot_api, Coinspot
from coinspot.coinspot_types import MyCoinBalancesResponse, PlaceMarketBuySellOrderResponse
from coinspot import CoinspotApiError

# Create an authenticated API instance
api: Coinspot = create_coinspot_api(api_key="your_api_key", api_secret="your_api_secret")

try:
    # Get your account balance
    balance: MyCoinBalancesResponse = api.balance()
    for coin_balance in balance["balances"]:
        for coin, details in coin_balance.items():
            print(f"{coin} balance: {details['balance']}, AUD value: ${details['audbalance']}")

    # Place a market buy order
    buy_order: PlaceMarketBuySellOrderResponse = api.market_buy_order("BTC", amount=0.01, rate=50000)
    print(f"Buy order placed: {buy_order['id']}")

except CoinspotApiError as e:
    print(f"An API error occurred: {e.status} - {e.message}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
```

## Error Handling

The Coinspot API wrapper uses a custom `CoinspotApiError` exception for API-related errors:

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

## API Reference

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
