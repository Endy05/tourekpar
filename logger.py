import logging

# Налаштування логування
logging.basicConfig(
    format="[{asctime}] - | {levelname} | {message}",
    style="{",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Тільки вивід у консоль
    ],
    force=True,  # Примусово перевизначає попередні конфігурації логів
)

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
