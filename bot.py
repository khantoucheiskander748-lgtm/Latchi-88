import asyncio
import random
from datetime import datetime

from pyquotex.stable_api import Quotex
from telethon import TelegramClient

# ================= CONFIG =================
EMAIL = "wagife9306@mugstock.com"
PASSWORD = "latchi23@@"

API_ID = 33567199
API_HASH = "3fdd30ef25043c39d8cc897d6251b8f1"
CHANNEL = "@latchidz0"

ASSETS = ["NZDCHF_otc", "USDINR_otc", "USDBDT_otc", "USDARS_otc", "USDPKR_otc"]
BASE_AMOUNT = 1

# ================= CONNECT =================
async def connect_quotex():
    while True:
        try:
            client = Quotex(email=EMAIL, password=PASSWORD)
            client.set_account_mode("PRACTICE")

            check, reason = await client.connect()

            if check:
                print("✅ Connected")
                return client
            else:
                print("❌ Failed:", reason)

        except Exception as e:
            print("⚠️ Error:", e)

        await asyncio.sleep(5)

# ================= TRADE =================
async def trade(client, asset, direction):
    try:
        print(f"🚀 TRY: {asset} {direction}")

        ok, order = await client.buy(BASE_AMOUNT, asset, direction, 60)

        if not ok:
            print("❌ Buy failed")
            return "fail"

        order_id = order.get("id", None)

        await asyncio.sleep(70)

        history = await client.get_history()

        if history and "data" in history:
            for trade in history["data"]:
                if str(trade.get("id")) == str(order_id):
                    profit = float(trade.get("profit", 0))
                    return "win" if profit > 0 else "loss"

        # fallback
        return "unknown"

    except Exception as e:
        print("TRADE ERROR:", e)
        return "fail"

# ================= MAIN =================
async def main():
    tg = TelegramClient("session", API_ID, API_HASH)
    await tg.start()

    await tg.send_message(CHANNEL, "🚀 BOT STARTED (RAILWAY VERSION)")

    client = await connect_quotex()

    while True:
        try:
            asset = random.choice(ASSETS)
            direction = random.choice(["call", "put"])

            result = await trade(client, asset, direction)

            msg = f"📊 {asset} | {direction.upper()} | {result.upper()}"

            await tg.send_message(CHANNEL, msg)

        except Exception as e:
            print("MAIN ERROR:", e)
            client = await connect_quotex()

        await asyncio.sleep(15)

asyncio.run(main())
