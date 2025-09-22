# WebSocket

_Module: yfinance_

The `WebSocket` module allows you to stream live price data
from Yahoo Finance using both synchronous and asynchronous clients.

## Classes

- `WebSocket` / `AsyncWebSocket`

## Synchronous WebSocket

The `WebSocket` class provides a synchronous interface for
subscribing to price updates.

Sample Code:

``` python
import yfinance as yf

# define your message callback
def message_handler(message):
    print("Received message:", message)

# =======================
# With Context Manager
# =======================
with yf.WebSocket() as ws:
    ws.subscribe(["AAPL", "BTC-USD"])
    ws.listen(message_handler)

# =======================
# Without Context Manager
# =======================
ws = yf.WebSocket()
ws.subscribe(["AAPL", "BTC-USD"])
ws.listen(message_handler)
```

## Asynchronous WebSocket

The `AsyncWebSocket` class provides an asynchronous
interface for subscribing to price updates.

Sample Code:

``` python
import asyncio
import yfinance as yf

# define your message callback
def message_handler(message):
    print("Received message:", message)

async def main():
    # =======================
    # With Context Manager
    # =======================
    async with yf.AsyncWebSocket() as ws:
        await ws.subscribe(["AAPL", "BTC-USD"])
        await ws.listen()

    # =======================
    # Without Context Manager
    # =======================
    ws = yf.AsyncWebSocket()
    await ws.subscribe(["AAPL", "BTC-USD"])
    await ws.listen()

asyncio.run(main())
```

> **Note:** If you're running asynchronous code in a Jupyter notebook, you may
> encounter issues with event loops. To resolve this, you need to import
> and apply `nest_asyncio` to allow nested event loops.
>
> Add the following code before running asynchronous operations:
>
> ``` python
> import nest_asyncio
> nest_asyncio.apply()
> ```

