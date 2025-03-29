import requests
import json
from logger import log_error, log_info
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from datetime import datetime

def send_telegram_alert(symbol, spread, mexc_price, dex_price, chain, url, address, dex_info):
    try:
        # Оновлюємо час перед відправкою
        time_now = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # Перевіряємо, чи всі значення не є None
        if None in [symbol, spread, mexc_price, dex_price, chain, url, address, dex_info]:
            log_error("❌ Помилка: один із параметрів має значення None!")
            return

        # Calculate direction and format spread
        is_mexc_higher = mexc_price > dex_price
        marker = "🔴 | " if is_mexc_higher else "🟢 | "
        spread_value = -abs(spread) if is_mexc_higher else abs(spread)

        message = f"""<b>{marker} Монета:</b> {symbol}
📊 <b>Спред:</b> {spread_value:.2f}%

🔗 <b>MEXC:</b> https://futures.mexc.com/ru-RU/exchange/{symbol}_USDT
🔗 <b>DEX:</b> {url}

📈 <b>Ціна MEXC:</b> {mexc_price:.6f}
📉 <b>Ціна DEX:</b> {dex_price:.6f}

💎 <b>Обʼєм торгів 24г:</b> ${dex_info.get('volume24h', 0)/1_000_000:.2f}M
💰 <b>Ліквідність:</b> ${dex_info.get('liquidity', 0)/1_000:.0f}K
📝 <b>Контракт:</b> <code>{address}</code>                                                                              
🌐 <b>Мережа:</b> {chain}

🕒 <b>Час:</b> <code>{time_now}</code>"""

        keyboard = {
            "inline_keyboard": [[
                {"text": "📈 DEX", "url": url},
                {"text": "📉 MEXC", "url": f"https://futures.mexc.com/ru-RU/exchange/{symbol}_USDT"}
            ]]
        }

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
            "reply_markup": json.dumps(keyboard)  # JSON-рядок!
        }

        log_info(f"📤 Відправка повідомлення у Telegram: {message}")

        response = requests.post(telegram_url, json=data, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            log_info(f"✅ Відправлено сповіщення для {symbol}")
        else:
            log_error(f"⚠️ Помилка Telegram: Код {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        log_error(f"❌ Помилка запиту в Telegram: {str(e)}")
    except Exception as e:
        log_error(f"❌ Невідома помилка при надсиланні в Telegram: {str(e)}")
