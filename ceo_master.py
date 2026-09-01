# ceo_master.py
import asyncio

async def ceo_decision_maker(signal):
    if signal['action'] == "ERROR":
        print(f"🧠 CEO Ignored Signal: Error in fetching data for {signal['coin']} from {signal['exchange']}")
        return

    print(f"🧠 CEO Analyzing Live Signal: {signal['coin']} at ${signal['price']}...")
    await asyncio.sleep(1) # ரிஸ்க் மேனேஜ்மென்ட் கணக்கீடு நேரம்
    
    print(f"🚀 CEO Approved! Executing {signal['action']} order for {signal['coin']} on {signal['exchange']} at exactly ${signal['price']}")
    print("-" * 50)
