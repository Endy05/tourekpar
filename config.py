import os
from dotenv import load_dotenv

# Завантажуємо змінні з .env
load_dotenv()

# Налаштування токенів
TOKENS = {
    "JELLYJELLY": {"address": "FeR8VBqNRSUD5NtXAj2n3j1dAHkZHfyDktKuLXD4pump", "pairAddress": "3bC2e2RxcfvF9oP22LvbaNsVwoS2T98q6ErCRoayQYdq"},
    "MUBARAK": {"address": "0x5C85D6C6825aB4032337F11Ee92a72DF936b46F6", "pairAddress": "0x90A54475D512B8f3852351611c38faD30a513491"},
    "TUT": {"address": "0xCAAE2A2F939F51d97CdFa9A86e79e3F085b799f3", "pairAddress": "0x6dAfBf0AB4FD72e2a5C0Ad5a1ED277d3bf8a8d1f"},
    "MUBARAKAH": {"address": "0x3199A64Bc8aaBDFd9A3937a346CC59c3d81D8a9a", "pairAddress": "0x3199A64Bc8aaBDFd9A3937a346CC59c3d81D8a9a"},
    "BID": {"address": "0xa1832f7F4e534aE557f9B5AB76dE54B1873e498B", "pairAddress": "0x764cF114f1838c22b138fB4dcDAAD03A65C946a9"},
    "BROCCOLIF3B": {"address": "0x12B4356C65340Fb02cdff01293F95FEBb1512F3b", "pairAddress": "0xdB25C09d96C165B62F6e6F9d9b17174738d897BA"}, 
    "BUBB": {"address": "0xd5369a3CaC0f4448A9A96bb98AF9c887c92fC37B", "pairAddress": "0xd5369a3CaC0f4448A9A96bb98AF9c887c92fC37B"},
    "BR": {"address": "0xff7d6a96ae471bbcd7713af9cb1feeb16cf56b41", "pairAddress": "0xF95F84e2baD9C234f93dd66614b82F9A854b452e"},
    "SIREN": {"address": "0x997A58129890bBdA032231A52eD1ddC845fc18e1", "pairAddress": "0xb2AF49dBF526054FAf19602860A5E298a79F3D05"},
    "BANANAS31": {"address": "0x3d4f0513e8a29669b960f9dbca61861548a9a760", "pairAddress": "0x7F51BBf34156ba802dEB0E38B7671DC4fa32041d"},
    "SLING": {"address": "0x5F8a7c646511A790C53F171891E5d469cA884EdE", "pairAddress": "0x9Ba33d5D5CBC8F271D2518E47e048C63B61138dc"},
    "CAPTAINBNB": {"address": "0x47A1EB0b825b73e6A14807BEaECAFef199d5477c", "pairAddress": "0x07F071AA224e2FC2Cf03cA2e6558Ec6181d66a90"},
    "PWEASE": {"address": "CniPCE4b3s8gSUPhUiyMjXnytrEqUrMfSsnbBjLCpump", "pairAddress": "9fmdkQipJK2teeUv53BMDXi52uRLbrEvV38K8GBNkiM7"},
    "SZN": {"address": "TDxL4V5LE6TYSFXSCWJkkSsCYbgmrDnTer", "pairAddress": "TLkhSBpYbgQ4A7nEUaC4cYXmhiZjuks9oX"},
    "GROKCOIN": {"address": "3MadWqcN9cSrULn8ikDnan9mF3znoQmBPXtVy6BfSTDB", "pairAddress": "DsktL4KrnnsupVfjb1uW4aoudgN8ooz4DtepPSAbmdN3"},
    "TIBBIR": {"address": "0xA4A2E2ca3fBfE21aed83471D28b6f65A233C6e00", "pairAddress": "0x0c3b466104545efa096b8f944c1e524E1d0D4888"},
    "BNBCARD" : {"address": "0xDc06717F367e57A16e06CcE0c4761604460da8Fc", "pairAddress": "0x78fc96f3543337cd5393533eA66dC8fe42Ad054d"},
    "TAT" : {"address": "0x996D1b997203a024E205069a304161ba618d1c61", "pairAddress": "0x71cD938b95aD63cb724b986bD7628558A6aF5Bb1"},
}


# Пороги спреду для алертів
SPREAD_THRESHOLD = float(os.getenv("SPREAD_THRESHOLD", 4.0))
SPREAD_INCREMENT_THRESHOLD = float(os.getenv("SPREAD_INCREMENT_THRESHOLD", 1.5))

# Redis конфігурація
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
# Час зберігання алертів в Redis (в секундах)
# 900 секунд = 15 хвилин
# Якщо потрібно змінити час зберігання, змініть це значення
# або встановіть змінну REDIS_ALERT в .env файлі
REDIS_ALERT = int(os.getenv("REDIS_ALERT", 120))

# API URL
MEXC_API_URL = "https://api.mexc.com/api/v3/ticker/price"
DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex/tokens/"

# Telegram (перевіряємо наявність змінних)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("❌ ERROR: Не задано TELEGRAM_BOT_TOKEN або TELEGRAM_CHAT_ID у .env!")
