# API Reference

## Overview

The `yfinance` package provides easy access to Yahoo!
Finance's API to retrieve market data. It includes classes and
functions for downloading historical market data, accessing ticker
information, managing cache, and more.

### Public API

The following are the publicly available classes, and functions exposed
by the `yfinance` package:

- `Ticker (yfinance.Ticker)`: Class for
    accessing single ticker data.
- `Tickers (yfinance.Tickers)`: Class
    for handling multiple tickers.
- `Market (yfinance.Market)`: Class for
    accessing market summary.
- `download (yfinance.download)`:
    Function to download market data for multiple tickers.
- `Search (yfinance.Search)`: Class for
    accessing search results.
- `Lookup (yfinance.Lookup)`: Class for
    looking up tickers.
- `WebSocket (yfinance.WebSocket)`:
    Class for synchronously streaming live market data.
- `AsyncWebSocket (yfinance.AsyncWebSocket)`: Class for asynchronously streaming live market data.
- `Sector (yfinance.Sector)`: Domain
    class for accessing sector information.
- `Industry (yfinance.Industry)`:
    Domain class for accessing industry information.
- `EquityQuery (yfinance.EquityQuery)`:
    Class to build equity query filters.
- `FundQuery (yfinance.FundQuery)`:
    Class to build fund query filters.
- `screen (yfinance.screen)`: Run
    equity/fund queries.
- `enable_debug_mode (yfinance.enable_debug_mode)`: Function to enable debug mode for logging.
- `set_tz_cache_location (yfinance.set_tz_cache_location)`: Function to set the timezone cache location.

- [yfinance.ticker_tickers](yfinance.ticker_tickers.md)
- [yfinance.stock](yfinance.stock.md)
- [yfinance.market](yfinance.market.md)
- [yfinance.financials](yfinance.financials.md)
- [yfinance.analysis](yfinance.analysis.md)
- [yfinance.search](yfinance.search.md)
- `yfinance.lookup`
- [yfinance.websocket](yfinance.websocket.md)
- [yfinance.sector_industry](yfinance.sector_industry.md)
- [yfinance.screener](yfinance.screener.md)
- [yfinance.functions](yfinance.functions.md)
- [yfinance.funds_data](yfinance.funds_data.md)
- [yfinance.price_history](yfinance.price_history.md)

