# ceo_master.py
import asyncio

async def ceo_decision_maker(signal):
    if signal['action'] == "ERROR":
        return

    print(f"🧠 CEO Analyzing Live Signal: {signal['coin']} at ${signal['price']}...")
    await asyncio.sleep(1) # ரிஸ்க் மேனேஜ்மென்ட் நேரம்
    
    if signal['action'] == "BUY":
        print(f"🚀 CEO Approved! Executing BUY order for {signal['coin']} on {signal['exchange']} at ${signal['price']}")
    else:
        print(f"⏳ CEO Decision: HOLDing {signal['coin']}. Market is not favorable right now.")
        
    print("-" * 50)
