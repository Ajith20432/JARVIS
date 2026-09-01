# ceo_master.py
import asyncio

async def ceo_decision_maker(signal):
    if signal['action'] == "ERROR":
        return

    print(f"👔 CEO Analyzing AI Signal: {signal['coin']} at ${signal['price']} (AI Confidence: {signal['confidence']:.2f}%)...")
    await asyncio.sleep(1)
    
    # AI-ன் நம்பிக்கை 60% க்கு மேல் இருந்தால் மட்டுமே ஆர்டர் போடும் லாஜிக்
    if signal['action'] == "BUY" and signal['confidence'] > 60.0:
        print(f"🚀 CEO Approved! Executing BUY order for {signal['coin']} on {signal['exchange']} at ${signal['price']}")
    elif signal['action'] == "SELL" and signal['confidence'] > 60.0:
        print(f"🛑 CEO Approved! Executing SELL/SHORT order for {signal['coin']} on {signal['exchange']} at ${signal['price']}")
    else:
        print(f"⏳ CEO Decision: HOLDing {signal['coin']}. Market is choppy or AI confidence is too low.")
        
    print("-" * 50)
