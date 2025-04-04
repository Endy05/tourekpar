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

# Отримання даних з Dexscreener API
def get_dex_prices(token_addresses):
    prices = {}
    base_url = "https://api.dexscreener.com/latest/dex/tokens/"
    BATCH_SIZE = 28  # Максимальна кількість токенів на запит
    
    try:
        # Отримуємо всі адреси токенів
        addresses = [token_info['address'] for token_info in TOKENS.values()]
        
        # Розбиваємо адреси на групи по 50
        for i in range(0, len(addresses), BATCH_SIZE):
            batch_addresses = addresses[i:i + BATCH_SIZE]
            log_info(f"Обробка batch {i//BATCH_SIZE + 1} ({len(batch_addresses)} токенів)")
            
            response = requests.get(base_url + ",".join(batch_addresses), timeout=5)
            response.raise_for_status()
            data = response.json()

            if "pairs" not in data:
                log_error(f"Невірний формат відповіді DEX API для batch {i//BATCH_SIZE + 1}")
                continue

            # Створюємо маппінг адрес до імен токенів
            address_to_token = {info['address'].lower(): name for name, info in TOKENS.items()}
            token_pairs = {}

            # Обробка пар
            for pair in data.get("pairs", []):
                contract = pair.get("baseToken", {}).get("address", "").lower()
                if not contract:
                    continue

                token_name = address_to_token.get(contract)
                if not token_name:
                    continue

                pair_address = pair.get("pairAddress", "").lower()
                config_pair_address = TOKENS[token_name].get('pairAddress', '').lower()
                liquidity = float(pair.get("liquidity", {}).get("usd", 0))

                # Логіка обробки токена в залежності від наявності pairAddress
                if config_pair_address:
                    # Якщо є конфігурований pairAddress, використовуємо тільки відповідну пару
                    if pair_address == config_pair_address:
                        token_pairs[token_name] = {"pair": pair, "liquidity": liquidity}
                else:
                    # Якщо немає конфігурованого pairAddress, беремо пару з найбільшою ліквідністю
                    if token_name not in token_pairs or liquidity > token_pairs[token_name]["liquidity"]:
                        token_pairs[token_name] = {"pair": pair, "liquidity": liquidity}

            # Обробка результатів
            for token_name, pair_data in token_pairs.items():
                pair = pair_data["pair"]
                price = pair.get("priceUsd")
                
                if price and isinstance(price, (int, float, str)):
                    prices[token_name] = {
                        "price": float(price),
                        "token": token_name,
                        "url": pair.get("url"),
                        "contract": pair.get("baseToken", {}).get("address", "").lower(),
                        "chain": pair.get("chainId"),
                        "pair_address": pair.get("pairAddress"),
                        "liquidity": pair_data["liquidity"],
                        "volume24h": float(pair.get("volume", {}).get("h24", 0))
                    }

                    # Зберігаємо pairAddress тільки якщо його не було в конфігурації
                    if not TOKENS[token_name].get('pairAddress'):
                        TOKENS[token_name]['pairAddress'] = pair.get("pairAddress", "")
                        log_info(f"Found new pairAddress for {token_name}: {pair.get('pairAddress', '')}")
                    
                    log_info(f"Processed {token_name} with {'configured' if TOKENS[token_name].get('pairAddress') else 'best liquidity'} pair")

        return prices
    except requests.RequestException as e:
        log_error(f"Помилка запиту до DEX API: {e}")
        return {}
