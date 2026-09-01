# swarm_clones.py
import asyncio
import ccxt.async_support as ccxt
from ai_brain import brain  # 🧠 நமது புதிய AI மூளையை இங்கே இணைக்கிறோம்!

async def spawn_clone(coin, exchange_name):
    print(f"🧬 Clone {coin} on {exchange_name}... AI is Analyzing Data...")
    exchange_class = getattr(ccxt, exchange_name.lower())()
    
    try:
        # 1. லைவ் விலையை எடுப்பது
        ticker = await exchange_class.fetch_ticker(coin)
        current_price = ticker['last']
        
        # 2. AI-க்குத் தேவையான கடந்த 20 நிமிட டேட்டாவை எடுப்பது
        candles = await exchange_class.fetch_ohlcv(coin, '1m', limit=20)
        closing_prices = [candle[4] for candle in candles] 
        
        # 3. 🤖 AI-யிடம் கணிப்பைக் கேட்பது! (Predict)
        action, confidence = brain.predict_trend(closing_prices)
        
        print(f"📊 AI Prediction for {coin} ({exchange_name}): {action} | Confidence: {confidence:.2f}% | Live = ${current_price}")
        
        return {"coin": coin, "action": action, "exchange": exchange_name, "price": current_price, "confidence": confidence}
        
    except Exception as e:
        print(f"⚠️ Clone Error on {exchange_name} for {coin}: {e}")
        return {"coin": coin, "action": "ERROR", "exchange": exchange_name, "price": 0, "confidence": 0}
        
    finally:
        await exchange_class.close()
