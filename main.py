# main.py
import asyncio
from swarm_clones import spawn_clone
from ceo_master import ceo_decision_maker

# கண்காணிக்க வேண்டிய காயின்கள் மற்றும் எக்ஸ்சேஞ்ச்கள்
TARGETS = [
    {"coin": "BTC/USDT", "exchange": "binance"},
    {"coin": "ETH/USDT", "exchange": "bybit"},
    {"coin": "SOL/USDT", "exchange": "htx"}
]

# ஸ்கேனிங் இடைவெளி (நொடிகளில்)
SCAN_INTERVAL = 15

async def main():
    print("✅ Config Loaded: J.A.R.V.I.S Settings Initialized")
    print("🤖 J.A.R.V.I.S 24/7 Autonomous Engine Online...")
    print(f"⏱️ Scanning Interval: Every {SCAN_INTERVAL} seconds\n")
    
    loop_count = 1
    
    try:
        while True:
            print(f"🔄 --- [ CYCLE #{loop_count} INITIATED ] ---")
            
            # அனைத்து குளோன்களையும் ஒரே நேரத்தில் களமிறக்குதல்
            tasks = [spawn_clone(target["coin"], target["exchange"]) for target in TARGETS]
            signals = await asyncio.gather(*tasks)
            
            # CEO முடிவெடுக்கும் பகுதி
            for signal in signals:
                await ceo_decision_maker(signal)
            
            print(f"💤 Sleeping for {SCAN_INTERVAL}s before next market cycle...\n")
            await asyncio.sleep(SCAN_INTERVAL)
            loop_count += 1
            
    except KeyboardInterrupt:
        print("\n🛑 J.A.R.V.I.S System Safely Shutting Down by User...")

if __name__ == "__main__":
    asyncio.run(main())
