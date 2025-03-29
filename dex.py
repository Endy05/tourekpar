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
    
    # Extract token addresses from the new config structure
    addresses = [token_info['address'] for token_info in TOKENS.values()]
    
    try:
        response = requests.get(base_url + ",".join(addresses), timeout=5)
        response.raise_for_status()
        data = response.json()

        if "pairs" not in data:
            log_error("Невірний формат відповіді DEX API: відсутній ключ 'pairs'")
            return {}

        # Create reverse mapping from address to token name
        address_to_token = {info['address'].lower(): name for name, info in TOKENS.items()}

        # Dictionary to track highest liquidity pairs for each token
        token_pairs = {}

        # First pass: group all pairs by token and find highest liquidity
        for pair in data["pairs"]:
            contract = pair.get("baseToken", {}).get("address", "").lower()
            if not contract:
                continue

            token_name = address_to_token.get(contract)
            if not token_name:
                continue

            liquidity = float(pair.get("liquidity", {}).get("usd", 0))
            
            if token_name not in token_pairs or liquidity > token_pairs[token_name]["liquidity"]:
                token_pairs[token_name] = {
                    "pair": pair,
                    "liquidity": liquidity
                }

        # Second pass: create final prices dictionary with highest liquidity pairs
        for token_name, pair_data in token_pairs.items():
            pair = pair_data["pair"]
            price = pair.get("priceUsd")
            
            if price and isinstance(price, (int, float, str)):
                contract = pair.get("baseToken", {}).get("address", "").lower()
                url = pair.get("url")
                chain = pair.get("chainId")
                pair_address = pair.get("pairAddress")
                liquidity = pair_data["liquidity"]

                prices[token_name] = {
                    "price": float(price),
                    "token": token_name,
                    "url": url,
                    "contract": contract,
                    "chain": chain,
                    "pair_address": pair_address,
                    "liquidity": liquidity,
                    "volume24h": float(pair.get("volume", {}).get("h24", 0))
                }

                # Update TOKENS with the highest liquidity pair address
                if pair_address:
                    TOKENS[token_name]['pairAddress'] = pair_address
                    log_info(f"Updated {token_name} pair address with highest liquidity (${liquidity:,.2f})")

        return prices
    except requests.RequestException as e:
        log_error(f"Помилка запиту до DEX API: {e}")
        return {}
