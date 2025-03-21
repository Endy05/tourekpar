import requests
from logger import log_error, log_info
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(symbol, contract, spread, mexc_price, dex_price, chain, url):
    try:
        message = f"""<b>💰 Монета:</b> {symbol}

📊 <b>Спред:</b> {spread:.2f}%

🔗 <b>MEXC:</b> https://futures.mexc.com/ru-RU/exchange/{symbol}_USDT"
🔗 <b>DEX:</b> {url}"

📈 <b>Ціна MEXC:</b> {mexc_price:.6f}
📉 <b>Ціна DEX:</b> {dex_price:.6f}

📝 <b>Контракт:</b> <code>{contract}</code>
🌐 <b>Сеть:</b> {chain}"""

        keyboard = {
            "inline_keyboard": [[
                {"text": "📈 DEX", "url": f"{url}"},
                {"text": "📉 MEXC", "url": f"https://futures.mexc.com/ru-RU/exchange/{symbol}_USDT"}
            ]]
        }

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
            "reply_markup": keyboard
        }

        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        log_info(f"✅ Відправлено сповіщення для {symbol}")
    except Exception as e:
        log_error(f"❌ Помилка відправки в Telegram: {str(e)}")
        raise
