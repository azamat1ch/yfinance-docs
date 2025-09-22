# Ticker and Tickers

_Module: yfinance_

## Class

The `Ticker` module, allows you to access ticker data in a
Pythonic way.

- `Ticker` / `Tickers`

## Ticker Sample Code

The `Ticker` module, allows you to access ticker data in a
Pythonic way.

``` python
import yfinance as yf

dat = yf.Ticker("MSFT")

# get historical market data
dat.history(period='1mo')

# options
dat.option_chain(dat.options[0]).calls

# get financials
dat.balance_sheet
dat.quarterly_income_stmt

# dates
dat.calendar

# general info
dat.info

# analysis
dat.analyst_price_targets

# websocket
dat.live()
```

To initialize multiple `Ticker` objects, use

``` python
import yfinance as yf

tickers = yf.Tickers('msft aapl goog')

# access each ticker using (example)
tickers.tickers['MSFT'].info
tickers.tickers['AAPL'].history(period="1mo")
tickers.tickers['GOOG'].actions

# websocket
tickers.live()
```

For tickers that are ETFs/Mutual Funds, `Ticker.funds_data`
provides access to fund related data.

Funds' Top Holdings and other data with category average is returned as
`pd.DataFrame`.

``` python
import yfinance as yf
spy = yf.Ticker('SPY')
data = spy.funds_data

# show fund description
data.description

# show operational information
data.fund_overview
data.fund_operations

# show holdings related information
data.asset_classes
data.top_holdings
data.equity_holdings
data.bond_holdings
data.bond_ratings
data.sector_weightings
```

If you want to use a proxy server for downloading data, use:

``` python
import yfinance as yf

msft = yf.Ticker("MSFT")

msft.history(..., proxy="PROXY_SERVER")
msft.get_actions(proxy="PROXY_SERVER")
msft.get_dividends(proxy="PROXY_SERVER")
msft.get_splits(proxy="PROXY_SERVER")
msft.get_capital_gains(proxy="PROXY_SERVER")
msft.get_balance_sheet(proxy="PROXY_SERVER")
msft.get_cashflow(proxy="PROXY_SERVER")
msft.option_chain(..., proxy="PROXY_SERVER")
...
```

To initialize multiple `Ticker` objects, use
`Tickers` module

``` python
import yfinance as yf

tickers = yf.Tickers('msft aapl goog')

# access each ticker using (example)
tickers.tickers['MSFT'].info
tickers.tickers['AAPL'].history(period="1mo")
tickers.tickers['GOOG'].actions

# websocket
tickers.live()
```

