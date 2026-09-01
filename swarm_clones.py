# swarm_clones.py
import asyncio
import ccxt.async_support as ccxt

async def spawn_clone(coin, exchange_name):
    print(f"🧬 Clone Spawned for {coin} on {exchange_name}... Connecting to Live Market...")
    
    # எக்ஸ்சேஞ்சை டைனமிக்காக உருவாக்குதல் (ex: Binance, Bybit)
    exchange_class = getattr(ccxt, exchange_name.lower())()
    
    try:
        # நிஜமான லைவ் மார்க்கெட் விலையை எடுப்பது
        ticker = await exchange_class.fetch_ticker(coin)
        current_price = ticker['last']
        
        print(f"⚡ Live Data by Clone: {coin} on {exchange_name} is currently ${current_price}")
        
        # இப்போதைக்கு சிம்பிளான ஒரு லாஜிக் (பிற்காலத்தில் RSI, MACD சேர்க்கலாம்)
        action = "BUY"
        
        return {"coin": coin, "action": action, "exchange": exchange_name, "price": current_price}
        
    except Exception as e:
        print(f"⚠️ Clone Error on {exchange_name} for {coin}: {e}")
        return {"coin": coin, "action": "ERROR", "exchange": exchange_name, "price": 0}
        
    finally:
        # மெமரி லீக் வராமல் இருக்க கனெக்ஷனை மூடுதல்
        await exchange_class.close()
