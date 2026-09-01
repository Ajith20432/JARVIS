# swarm_clones.py
import asyncio
import ccxt.async_support as ccxt

async def spawn_clone(coin, exchange_name):
    print(f"🧬 Clone {coin} on {exchange_name}... Fetching Candle Data...")
    exchange_class = getattr(ccxt, exchange_name.lower())()
    
    try:
        # 1. லைவ் விலையை எடுப்பது
        ticker = await exchange_class.fetch_ticker(coin)
        current_price = ticker['last']
        
        # 2. கேண்டில்ஸ்டிக் டேட்டாவை எடுப்பது (OHLCV: 1-minute timeframe, last 10 candles)
        candles = await exchange_class.fetch_ohlcv(coin, '1m', limit=10)
        
        # 3. Simple Moving Average (SMA) கணக்கிடுதல்
        closing_prices = [candle[4] for candle in candles] # 4th Index தான் Closing Price
        sma_10 = sum(closing_prices) / len(closing_prices)
        
        print(f"📊 {coin} ({exchange_name}): Live = ${current_price}, 10-Min SMA = ${sma_10:.4f}")
        
        # 4. Strategy: SMA Breakout லாஜிக்
        if current_price > sma_10:
            action = "BUY"
            print(f"📈 UPTREND DETECTED for {coin}! Generating BUY signal.")
        else:
            action = "HOLD"
            print(f"📉 DOWNTREND / CHOPPY for {coin}. Generating HOLD signal.")
        
        return {"coin": coin, "action": action, "exchange": exchange_name, "price": current_price}
        
    except Exception as e:
        print(f"⚠️ Clone Error on {exchange_name} for {coin}: {e}")
        return {"coin": coin, "action": "ERROR", "exchange": exchange_name, "price": 0}
        
    finally:
        await exchange_class.close()
