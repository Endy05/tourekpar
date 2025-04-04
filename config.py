import os
from dotenv import load_dotenv

# Завантажуємо змінні з .env
load_dotenv()

# Налаштування токенів
TOKENS = {
    "JELLYJELLY": {"address": "FeR8VBqNRSUD5NtXAj2n3j1dAHkZHfyDktKuLXD4pump", "pairAddress": "3bC2e2RxcfvF9oP22LvbaNsVwoS2T98q6ErCRoayQYdq"},
    "MUBARAK": {"address": "0x5C85D6C6825aB4032337F11Ee92a72DF936b46F6", "pairAddress": "0x90A54475D512B8f3852351611c38faD30a513491"},
    "TUT": {"address": "0xCAAE2A2F939F51d97CdFa9A86e79e3F085b799f3", "pairAddress": "0x6dAfBf0AB4FD72e2a5C0Ad5a1ED277d3bf8a8d1f"},
    "MUBARAKAH": {"address": "0x3199A64Bc8aaBDFd9A3937a346CC59c3d81D8a9a", "pairAddress": "0xacB622435b634e75b61473bE6F839c46E36BD754"},
    "BID": {"address": "0xa1832f7F4e534aE557f9B5AB76dE54B1873e498B", "pairAddress": "0x764cF114f1838c22b138fB4dcDAAD03A65C946a9"},
    "BROCCOLIF3B": {"address": "0x12B4356C65340Fb02cdff01293F95FEBb1512F3b", "pairAddress": "0xdB25C09d96C165B62F6e6F9d9b17174738d897BA"}, 
    "BUBB": {"address": "0xd5369a3CaC0f4448A9A96bb98AF9c887c92fC37B", "pairAddress": "0xc8255e3fA0F4c6e6678807d663f9e2263e23a8E8"},
    "BR": {"address": "0xff7d6a96ae471bbcd7713af9cb1feeb16cf56b41", "pairAddress": "0xF95F84e2baD9C234f93dd66614b82F9A854b452e"},
    "BANANAS31": {"address": "0x3d4f0513e8a29669b960f9dbca61861548a9a760", "pairAddress": "0x7F51BBf34156ba802dEB0E38B7671DC4fa32041d"},
    "SZN": {"address": "TDxL4V5LE6TYSFXSCWJkkSsCYbgmrDnTer", "pairAddress": "TLkhSBpYbgQ4A7nEUaC4cYXmhiZjuks9oX"},
    "BNBCARD" : {"address": "0xDc06717F367e57A16e06CcE0c4761604460da8Fc", "pairAddress": "0x78fc96f3543337cd5393533eA66dC8fe42Ad054d"},
    "GHIBLI" : {"address" : "4TBi66vi32S7J8X1A6eWfaLHYmUXu7CStcEmsJQdpump", "pairAddress" : "H9d3XHfvMGfoohydEpqh4w3mopnvjCRzE9VqaiHKdqs7"},
    "KEYCAT" : {"address" : "0x9a26F5433671751C3276a065f57e5a02D2817973", "pairAddress" : "0x377FeeeD4820B3B28D1ab429509e7A0789824fCA"},
    "KILO" : {"address" : "0x503Fa24B7972677F00C4618e5FBe237780C1df53", "pairAddress" : "0xd3BC30079210bEF8a1f9C7C21e3C5BecCfC1DfCb"},
    "YZYSOL" : {"address" : "9gyfbPVwwZx4y1hotNSLcqXCQNpNqqz6ZRvo8yTLpump", "pairAddress" : "6oi9cUuPCbzK3YKCNnj47Ren7LrSuwcsYA48uMBKemJS"},
    "DRB" : {"address" : "0x3ec2156D4c0A9CBdAB4a016633b7BcF6a8d68Ea2", "pairAddress" : "0x5116773e18A9C7bB03EBB961b38678E45E238923"},
    "ALON" : {"address" : "8XtRWb4uAAJFMP4QQhoYYCWR6XXb7ybcCdiqPwz9s5WS", "pairAddress" : "Eb9qkfiSzKd185KdWLkZrMrejKEbA2ah2BK7spNmoPej"},
    "DOGINME" : {"address" : "0x6921B130D297cc43754afba22e5EAc0FBf8Db75b", "pairAddress" : "0xADE9BcD4b968EE26Bed102dd43A55f6A8c2416df"},
    "GROKCOIN" : {"address" : "3MadWqcN9cSrULn8ikDnan9mF3znoQmBPXtVy6BfSTDB", "pairAddress" : "DsktL4KrnnsupVfjb1uW4aoudgN8ooz4DtepPSAbmdN3"},
    "LUCE" : {"address" : "CBdCxKo9QavR9hfShgpEBG3zekorAeD7W1jfq2o3pump", "pairAddress" : "HQWsAXxH3dGy9DQbryJyDrquKt2eDY6MMHWmpUEKfgZq"},
    "AGIXT" : {"address" : "F9TgEJLLRUKDRF16HgjUCdJfJ5BK6ucyiW8uJxVPpump", "pairAddress" : "iJuiniVZc7rHYKcvEy9Dz5arHjjmrbfYLdY4etGfQXr"},
    "PWEASE" : {"address" : "CniPCE4b3s8gSUPhUiyMjXnytrEqUrMfSsnbBjLCpump", "pairAddress" : "9fmdkQipJK2teeUv53BMDXi52uRLbrEvV38K8GBNkiM7"},
    
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
