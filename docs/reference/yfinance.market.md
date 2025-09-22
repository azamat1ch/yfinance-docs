# Market

_Module: yfinance_

## Class

The `Market` class, allows you to access market data in a
Pythonic way.

- `Market`

## Market Sample Code

``` python
import yfinance as yf

EUROPE = yf.Market("EUROPE")

status = EUROPE.status
summary = EUROPE.summary
```

## Markets

There are 8 different markets available in Yahoo Finance.

- US
- GB

- ASIA
- EUROPE

- RATES
- COMMODITIES
- CURRENCIES
- CRYPTOCURRENCIES
