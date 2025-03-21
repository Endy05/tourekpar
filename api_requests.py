import requests
import logging
from config import TOKENS

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

# Отримання даних з MEXC API
def get_mexc_prices():
    url = "https://api.mexc.com/api/v3/ticker/price"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        prices = {}
        for item in data:
            symbol = item.get("symbol", "")
            price = item.get("price", "0")
            
            if symbol.endswith("USDT"):
                prices[symbol.replace("USDT", "")] = float(price)
        
        return prices
    except requests.RequestException as e:
        log_error(f"Помилка запиту до MEXC API: {e}")
        return {}

# Отримання даних з Dexscreener API
def get_dex_prices(token_addresses):
    prices = {}
    base_url = "https://api.dexscreener.com/latest/dex/tokens/"

    try:
        response = requests.get(base_url + ",".join(token_addresses), timeout=5)
        response.raise_for_status()
        data = response.json()


        if "pairs" not in data:
            log_error("Невірний формат відповіді DEX API: відсутній ключ 'pairs'")
            return {}

        for pair in data["pairs"]:
            contract = pair.get("baseToken", {}).get("address", "")
            price = pair.get("priceUsd")
            url = pair.get("url")

            if contract and isinstance(price, (int, float, str)):
                # Пошук назви токена за контрактом з config.TOKENS
                for token, token_contract in TOKENS.items():
                    if token_contract.lower() == contract.lower():
                        prices[token] = {"price": float(price), "token": token, "url" : url, "contract" : contract}

        return prices
    except requests.RequestException as e:
        log_error(f"Помилка запиту до DEX API: {e}")
        return {}
