# tracker.py
import json
import os
from datetime import datetime

LOG_FILE = "trade_history.json"

def log_trade(coin, exchange, action, price, confidence):
    """
    ஒவ்வொரு டிரேடு மற்றும் சிக்னல் விவரங்களையும் துல்லியமாக டிராக் செய்து சேமிக்கும்
    """
    trade_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "coin": coin,
        "exchange": exchange,
        "action": action,
        "price": price,
        "confidence": confidence
    }
    
    # லோக்கல் ஹிஸ்டரி ஃபைலில் சேமித்தல்
    history = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []
            
    history.insert(0, trade_record) # புதிய ரெக்கார்டை முதலில் சேர்த்தல்
    
    # அதிகபட்சம் 50 ரெக்கார்டுகளை மட்டும் சேமித்துக்கொள்ளும் (Performance-க்காக)
    if len(history) > 50:
        history.pop()
        
    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=4)
        
    print(f"📈 [TRACKED] {coin} on {exchange} -> {action} at ${price} (Confidence: {confidence}%)")

def get_trade_history():
    """
    சேமிக்கப்பட்ட டிரேடு ஹிஸ்டரியை ரிட்ரீவ் செய்யும்
    """
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []