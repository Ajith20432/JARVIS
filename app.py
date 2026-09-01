# app.py - J.A.R.V.I.S Master Pro Full Integrated Code
from flask import Flask, render_template, request, redirect, url_for
import threading
import asyncio
import os
import requests
import platform
from dotenv import load_dotenv
from swarm_clones import spawn_clone
from ceo_master import ceo_decision_maker

# .env அல்லது .env.txt ஃபைலை ஆட்டோமேட்டிக்காக லோட் செய்ய
load_dotenv('.env.txt') if os.path.exists('.env.txt') else load_dotenv()

app = Flask(__name__)

latest_signals = []
bot_status = "RUNNING"
total_profit = 124.50

TARGETS = [
    {"coin": "BTC/USDT", "exchange": "binance"},
    {"coin": "ETH/USDT", "exchange": "bybit"},
    {"coin": "SOL/USDT", "exchange": "htx"}
]

# 🚀 Telegram Alert Function with Complete Backend & AI Details
async def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})
            print("✅ Telegram Alert Sent Successfully!")
        except Exception as e:
            print(f"⚠️ Telegram Error: {e}")

async def background_trading_loop():
    global latest_signals, bot_status, total_profit
    while True:
        if bot_status == "RUNNING":
            tasks = [spawn_clone(target["coin"], target["exchange"]) for target in TARGETS]
            signals = await asyncio.gather(*tasks)
            
            temp_signals = []
            for signal in signals:
                await ceo_decision_maker(signal)
                temp_signals.append(signal)
                
                # சர்வர் மற்றும் ஹோஸ்டிங் விபரங்களை எடுப்பது
                server_os = platform.system()
                server_name = platform.node()
                
                # முழுமையான ட்ரேடிங் மற்றும் ஹோஸ்ட் விபரங்களுடன் கூடிய மெசேஜ்
                alert_msg = (
                    f"⚡ *J.A.R.V.I.S TRADE ALERT* ⚡\n\n"
                    f"🖥️ *Backend Host:* `{server_name}` ({server_os})\n"
                    f"🌐 *Active Clone:* `{signal['clone_id']}`\n"
                    f"🪙 *Coin:* {signal['coin']}\n"
                    f"🏢 *Exchange:* {signal['exchange'].upper()}\n"
                    f"💰 *Price:* ${signal['price']}\n"
                    f"🎯 *Action:* {signal['action']}\n"
                    f"🧠 *AI Confidence:* {signal['confidence']}%\n\n"
                    f"📊 *AI Reasoning (Why?):*\n_{signal['reason']}_"
                )
                
                await send_telegram_alert(alert_msg)
            
            latest_signals = temp_signals
        await asyncio.sleep(15)

def run_background_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(background_trading_loop())

@app.route('/')
def dashboard():
    return render_template('index.html', 
                           logs=latest_signals, 
                           status=bot_status, 
                           profit=total_profit,
                           binance_key=os.getenv("BINANCE_API_KEY", ""),
                           telegram_token=os.getenv("TELEGRAM_TOKEN", ""))

@app.route('/control', methods=['POST'])
def control():
    global bot_status
    action = request.form.get('action')
    if action == 'stop':
        bot_status = "STOPPED"
    elif action == 'start':
        bot_status = "RUNNING"
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    t = threading.Thread(target=run_background_loop, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
