import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_to_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # டேட்டா சரியாக உள்ளே வருகிறதா என்று பார்க்க
    print(f"🔍 Token Checking: {'Found' if token else 'Missing!'}")
    print(f"🔍 Chat ID Checking: {chat_id}")
    
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        try:
            response = requests.post(url, json={"chat_id": chat_id, "text": message})
            # டெலிகிராம் என்ன சொல்கிறது என்பதை அப்படியே காட்டும்
            print(f"📡 Telegram Response: {response.json()}") 
        except Exception as e:
            print(f"⚠️ Error: {e}")
    else:
        print("❌ Token or Chat ID is missing in .env file!")

# இந்த ஃபைலை மட்டும் ரன் செய்தால் இது இயங்கும்
if __name__ == "__main__":
    print("🚀 Sending Test Message to Boss...")
    send_to_telegram("✅ JARVIS Test Message: Boss, I am Online!")
