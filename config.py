import os
from dotenv import load_dotenv

# Завантажуємо змінні з .env
load_dotenv()

# Налаштування токенів
TOKENS = {
    "YZYSOL": "9gyfbPVwwZx4y1hotNSLcqXCQNpNqqz6ZRvo8yTLpump",
    "JELLYJELLY": "FeR8VBqNRSUD5NtXAj2n3j1dAHkZHfyDktKuLXD4pump",
    "VIVI": "9RUup1LmD5PBsnd23JmTy39wSwALB7JF7xMfUJP8K7je",
    "GANG": "d4VVNcnhYwenMzJJk7QgZsxVbLQSijPSLB8m7gKMGFM",
    "MUBARAK": "0x5C85D6C6825aB4032337F11Ee92a72DF936b46F6",
    "TUT": "0xCAAE2A2F939F51d97CdFa9A86e79e3F085b799f3",
    "MUBARAKAH": "0x3199A64Bc8aaBDFd9A3937a346CC59c3d81D8a9a",
    "BID": "0xa1832f7F4e534aE557f9B5AB76dE54B1873e498B",
    "BROCCOLIF3B": "0x12B4356C65340Fb02cdff01293F95FEBb1512F3b",
    "BUBB": "0xd5369a3CaC0f4448A9A96bb98AF9c887c92fC37B",
    "BR": "0xff7d6a96ae471bbcd7713af9cb1feeb16cf56b41",
    "SIREN": "0xb2af49dbf526054faf19602860a5e298a79f3d05",
    "BANANAS31": "0x3d4f0513e8a29669b960f9dbca61861548a9a760",
    "FARM": "0xa0246c9032bC3A600820415aE600c6388619A14D",
    "SLING": "0x5F8a7c646511A790C53F171891E5d469cA884EdE",
}

# Пороги спреду для алертів
SPREAD_THRESHOLD = float(os.getenv("SPREAD_THRESHOLD", 1.0))
SPREAD_INCREMENT_THRESHOLD = float(os.getenv("SPREAD_INCREMENT_THRESHOLD", 1.0))

# Redis конфігурація
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# API URL
MEXC_API_URL = "https://api.mexc.com/api/v3/ticker/price"
DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex/tokens/"

# Telegram (перевіряємо наявність змінних)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("❌ ERROR: Не задано TELEGRAM_BOT_TOKEN або TELEGRAM_CHAT_ID у .env!")
