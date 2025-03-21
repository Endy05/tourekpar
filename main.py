import threading
import time
import os
import redis
from api_requests import get_mexc_prices, get_dex_prices
from logger import log_info, log_spread_alert, log_to_file, log_error, log_info_spread
from telegram_bot import send_telegram_alert
from config import TOKENS, SPREAD_THRESHOLD, REDIS_HOST, REDIS_PORT, REDIS_DB, SPREAD_INCREMENT_THRESHOLD

# Підключення до Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Шлях до логів
logs_dir = os.path.join(os.path.dirname(__file__), "logs")

def is_alert_needed(token, current_spread):
    """ Перевіряє, чи потрібно відправляти сповіщення у Telegram """
    if current_spread < SPREAD_THRESHOLD:
        return False

    last_spread = redis_client.get(f"spread_alert:{token}")

    if last_spread is None:
        return True

    last_spread = float(last_spread)

    return (current_spread - last_spread) >= SPREAD_INCREMENT_THRESHOLD

def save_alert(token, spread):
    """ Зберігає спред в Redis """
    redis_client.setex(f"spread_alert:{token}", 60, spread)

def check_spreads():
    while True:
        start_time = time.time()
        log_info("Отримуємо дані з API...")

        try:
            # Отримуємо ціни
            mexc_data = get_mexc_prices()
            dex_data = get_dex_prices(list(TOKENS.values()))  # This returns a dict of prices and urls

            # Перевірка, чи не порожні дані
            mexc_data_status = True if mexc_data else False
            dex_data_status = True if dex_data else False

            # Логування результатів
            log_info(f"Дані з MEXC: {mexc_data_status}")
            log_info(f"Дані з DEX: {dex_data_status}")

            for contract, dex_info in dex_data.items():
                token_name = dex_info['token']
                dex_price = dex_info['price']
                url = dex_info.get('url') 
                address = dex_info.get('contract') # Extracting the URL for the token from dex_data
                mexc_price = mexc_data.get(token_name)

                if mexc_price and dex_price:
                    spread = ((mexc_price - dex_price) / dex_price) * 100
                    log_info_spread(token_name, dex_price, mexc_price, spread)

                    if mexc_price > dex_price and is_alert_needed(token_name, spread):
                        log_info(f"Знайдено арбітраж для {token_name}: {spread:.2f}% (MEXC: ${mexc_price:.6f} > DEX: ${dex_price:.6f})")
                        log_spread_alert(token_name, spread, mexc_price, dex_price)

                        try:
                            chain = dex_info.get('chain', 'bsc')
                            send_telegram_alert(token_name, contract, spread, mexc_price, dex_price, chain, url, address)
                            save_alert(token_name, spread)
                        except Exception as e:
                            log_error(f"Помилка Telegram для {token_name}: {e}")
                else:
                    if not mexc_price:
                        log_info(f"{token_name}: Немає ціни на MEXC")
                    if not dex_price:
                        log_info(f"{token_name}: Немає ціни на DEX")

            execution_time = time.time() - start_time
            log_info(f"Цикл завершено за {execution_time:.2f} секунд")
            
            sleep_time = max(0, 1 - execution_time)
            time.sleep(sleep_time)

        except Exception as e:
            log_error(f"Помилка у check_spreads: {e}")
            time.sleep(1)

def main():
    log_info("Запуск парсера...")
    log_to_file(os.path.join(logs_dir, "general_logs.txt"), "Запуск парсера...")

    thread = threading.Thread(target=check_spreads, daemon=True)
    thread.start()
    
    log_info("Потік check_spreads запущено!")  
    log_to_file(os.path.join(logs_dir, "general_logs.txt"), "Потік check_spreads запущено!")  

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
