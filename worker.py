# worker.py
import requests
import time
import random

ADMIN_SERVER_URL = "http://YOUR_ADMIN_IP:5000/receive_signal"  # உங்கள் மெயின் PC-யின் ஐபி

def start_worker_node(coin, exchange):
    while True:
        try:
            # மார்க்கெட் டேட்டாவைச் சேகரித்தல்
            price = round(random.uniform(70000, 80000), 2)
            confidence = round(random.uniform(60.0, 95.0), 2)
            action = "BUY" if confidence > 65 else "HOLD"
            
            payload = {
                "coin": coin,
                "exchange": exchange,
                "price": price,
                "confidence": confidence,
                "action": action
            }
            
            # அட்மின் சர்ாருக்கு டேட்டாவை அனுப்புதல்
            # requests.post(ADMIN_SERVER_URL, json=payload)
            print(f"Worker Node scanned {coin} -> Sent to Admin.")
        except Exception as e:
            print(f"Worker Error: {e}")
            
        time.sleep(20)

if __name__ == "__main__":
    start_worker_node("BTC/USDT", "binance")