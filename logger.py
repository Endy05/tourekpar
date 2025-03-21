import logging
from datetime import datetime
import os

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Налаштування логування
logging.basicConfig(
    format="[{asctime}] - | {levelname} | {message}",
    style="{",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(logs_dir, "system_logs.txt"), mode="a", encoding="utf-8"),
    ],
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_spread_alert(symbol, spread, mexc_price, dex_price):
    log_message = f"| {symbol:<15} | DEX: ${dex_price:<10.6f} | MEXC: ${mexc_price:<10.6f} | Spread: {spread:+6.2f}% |"
    logging.warning(log_message)
    log_to_file(os.path.join(logs_dir, "spread_logs.txt"), log_message)

def log_info_spread(symbol, dex_price, mexc_price, spread):
    log_message = f"| {symbol:<15} | DEX: ${dex_price:<10.6f} | MEXC: ${mexc_price:<10.6f} | Spread: {spread:+6.2f}% |"
    logging.info(log_message)

def log_to_file(filename, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] - {message}\n")
