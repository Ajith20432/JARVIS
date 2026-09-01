# app.py
from flask import Flask, render_template, request, redirect, url_for
import threading
import asyncio
import os
from dotenv import load_dotenv
from swarm_clones import spawn_clone
from ceo_master import ceo_decision_maker
from telegram import Bot

load_dotenv()
app = Flask(__name__)

latest_signals = []
bot_status = "RUNNING"
total_profit = 124.50  # ட்ரேடிங் ப்ராஃபிட் டிராக் செய்ய

TARGETS = [
    {"coin": "BTC/USDT", "exchange": "binance"},
    {"coin": "ETH/USDT", "exchange": "bybit"},
    {"coin": "SOL/USDT", "exchange": "htx"}
]

async def send_telegram_alert(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        try:
            bot = Bot(token=token)
            await bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            print(f"Telegram Error: {e}")

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
                # சிக்னல் அப்ரூவ் ஆனால் ப்ராஃபிட்டை கூட்டுவது போல ஒரு சிமுலேஷன் லாஜிக்
                if signal['action'] == 'BUY' and signal['confidence'] > 60:
                    total_profit += 2.45
                    await send_telegram_alert(f"🚨 J.A.R.V.I.S Alert: Executed {signal['action']} for {signal['coin']} on {signal['exchange']} at ${signal['price']}")
            
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

@app.route('/update_config', methods=['POST'])
def update_config():
    # API மற்றும் டெலிகிராம் கீகளை `.env` ஃபைலில் சேமிப்பது
    binance_key = request.form.get('binance_key')
    binance_secret = request.get_data.get('binance_secret') if hasattr(request, 'get_data') else ""
    tg_token = request.form.get('tg_token')
    tg_chat = request.form.get('tg_chat')
    
    with open('.env', 'w') as f:
        f.write(f"BINANCE_API_KEY={binance_key}\n")
        f.write(f"TELEGRAM_TOKEN={tg_token}\n")
        f.write(f"TELEGRAM_CHAT_ID={tg_chat}\n")
        
    load_dotenv(override=True)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    t = threading.Thread(target=run_background_loop, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=False)