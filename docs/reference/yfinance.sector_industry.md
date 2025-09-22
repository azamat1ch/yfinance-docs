# Sector and Industry

_Module: yfinance_

## Sector class

The `Sector` and `Industry` modules provide
access to the Sector and Industry information.

- `Sector` / `Industry`

> **See also:** `Sector.industries (yfinance.Sector.industries)` Map of sector and industry ## Sample Code To initialize, use the relevant sector or industry key as below. ``` python
import yfinance as yf

tech = yf.Sector('technology')
software = yf.Industry('software-infrastructure')

# Common information
tech.key
tech.name
tech.symbol
tech.ticker
tech.overview
tech.top_companies
tech.research_reports

# Sector information
tech.top_etfs
tech.top_mutual_funds
tech.industries

# Industry information
software.sector_key
software.sector_name
software.top_performing_companies
software.top_growth_companies

```

The modules can be chained with Ticker as below.

``` python
import yfinance as yf
# Ticker to Sector and Industry
msft = yf.Ticker('MSFT')
tech = yf.Sector(msft.info.get('sectorKey'))
software = yf.Industry(msft.info.get('industryKey'))

# Sector and Industry to Ticker
tech_ticker = tech.ticker
tech_ticker.info
software_ticker = software.ticker
software_ticker.history()
```

