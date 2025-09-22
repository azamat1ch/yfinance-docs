# Search & Lookup

_Module: yfinance_

## Class

The `Search` module, allows you to access search data in a
Pythonic way.

- `Search`

The `Lookup` module, allows you to look up tickers in a
Pythonic way.

- `Lookup`

## Sample Code

The `Search` module, allows you to access search data in a
Pythonic way.

``` python
import yfinance as yf

# get list of quotes
quotes = yf.Search("AAPL", max_results=10).quotes

# get list of news
news = yf.Search("Google", news_count=10).news

# get list of related research
research = yf.Search("apple", include_research=True).research
```

The `Lookup` module, allows you to look up tickers in a
Pythonic way.

``` python
import yfinance as yf

# Get All
all = yf.Lookup("AAPL").all
all = yf.Lookup("AAPL").get_all(count=100)

# Get Stocks
stock = yf.Lookup("AAPL").stock
stock = yf.Lookup("AAPL").get_stock(count=100)

# Get Mutual Funds
mutualfund = yf.Lookup("AAPL").mutualfund
mutualfund = yf.Lookup("AAPL").get_mutualfund(count=100)

# Get ETFs
etf = yf.Lookup("AAPL").etf
etf = yf.Lookup("AAPL").get_etf(count=100)

# Get Indices
index = yf.Lookup("AAPL").index
index = yf.Lookup("AAPL").get_index(count=100)

# Get Futures
future = yf.Lookup("AAPL").future
future = yf.Lookup("AAPL").get_future(count=100)

# Get Currencies
currency = yf.Lookup("AAPL").currency
currency = yf.Lookup("AAPL").get_currency(count=100)

# Get Cryptocurrencies
cryptocurrency = yf.Lookup("AAPL").cryptocurrency
cryptocurrency = yf.Lookup("AAPL").get_cryptocurrency(count=100)
```

