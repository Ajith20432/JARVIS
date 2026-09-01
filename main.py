# main.py
import asyncio
import config
from swarm_clones import spawn_clone
from ceo_master import ceo_decision_maker

async def start_jarvis():
    print("🤖 J.A.R.V.I.S System Online...")
    
    # டம்மியாக 3 குளோன்களை உருவாக்குதல் (Dynamic Swarm)
    tasks = [
        spawn_clone("BTC/USDT", "Binance"),
        spawn_clone("ETH/USDT", "Bybit"),
        spawn_clone("SOL/USDT", "HTX")
    ]
    
    signals = await asyncio.gather(*tasks)
    
    for signal in signals:
        await ceo_decision_maker(signal)

if __name__ == "__main__":
    asyncio.run(start_jarvis())