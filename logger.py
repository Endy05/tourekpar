import logging
from datetime import datetime
import os

# Створення папки logs, якщо її немає
logs_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Формат імені лог-файлу (YYYY.MM.DD-HH.MM.log)
log_filename = datetime.now().strftime("%Y.%m.%d-%H.%M") + ".log"
log_path = os.path.join(logs_dir, log_filename)

# Видаляємо всі попередні хендлери, якщо вони були створені
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Налаштування логування
logging.basicConfig(
    format="[{asctime}] - | {levelname} | {message}",
    style="{",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Вивід у консоль
        logging.FileHandler(log_path, mode="a", encoding="utf-8"),  # Запис у файл
    ],
    force=True,  # Примусово перевизначає попередні конфігурації логів
)

# Вивід файлу, куди записуються логи
print(f"🔹 Логи записуються у файл: {log_path}")

def log_to_file(file_path, message):
    """ Записує повідомлення у файл логів """
    try:
        with open(file_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    except Exception as e:
        log_error(f"Помилка запису у файл {file_path}: {e}")


# Функції для логування
def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_spread_alert(symbol, spread, mexc_price, dex_price):
    log_message = f"| {symbol:<15} | DEX: ${dex_price:<10.6f} | MEXC: ${mexc_price:<10.6f} | Spread: {spread:+6.2f}% |"
    logging.warning(log_message)

def log_info_spread(symbol, dex_price, mexc_price, spread):
    log_message = f"| {symbol:<15} | DEX: ${dex_price:<10.6f} | MEXC: ${mexc_price:<10.6f} | Spread: {spread:+6.2f}% |"
    logging.info(log_message)
