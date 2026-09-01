# config.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
# இதைப் போல மற்ற கீகளையும் செட் செய்து கொள்ளலாம்.

print("✅ Config Loaded: J.A.R.V.I.S Settings Initialized")