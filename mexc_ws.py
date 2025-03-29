import websocket
import json
import logging
import threading
import time
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

# Адреса WebSocket для MEXC Futures
WS_URL = "wss://contract.mexc.com/edge"

class MexcWebSocket:
    """Клас для отримання цін з MEXC через WebSocket"""
    
    def __init__(self):
        self.prices = {}  # Зберігання актуальних цін
        self.ws = None  # Об'єкт WebSocket
        self.lock = threading.Lock()  # Блокування для потокобезпеки
        self.thread = threading.Thread(target=self.start_websocket, daemon=True)
        self.thread.start()

    def on_message(self, ws, message):
        """Обробка вхідних повідомлень"""
        try:
            data = json.loads(message)
            if "channel" in data and data["channel"] == "push.tickers":
                with self.lock:
                    for item in data.get("data", []):
                        symbol = item.get("symbol", "")
                        last_price = item.get("lastPrice", 0)

                        if symbol.endswith("_USDT"):  
                            self.prices[symbol.replace("_USDT", "")] = float(last_price)


                response_mexc = self.prices

                # TOKENS_price = {}

                # # Створюємо список кортежів (токен, ціна), якщо токен є в обох словниках
                # matching_tokens = [(token, response_mexc[token]) for token in TOKENS if token in response_mexc]

                # # Додаємо лог для перевірки
                # print("Matching tokens:", matching_tokens)

                # # Додаємо значення у TOKENS_price, перетворюючи список у словник
                # TOKENS_price = dict(matching_tokens)

                # # Лог для перевірки
                # print("TOKENS_price:", TOKENS_price)


                get_mexc_prices_json = 'false'

                if self.prices is not None:
                    get_mexc_prices_json = "true" 
                else:
                    get_mexc_prices_json = 'false'
                
                

                    
                log_info(f"Оновлені ціни: {get_mexc_prices_json}")

        except json.JSONDecodeError as e:
            log_error(f"Помилка обробки JSON: {e}")

    def on_error(self, ws, error):
        log_error(f"Помилка WebSocket: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        log_info("З'єднання WebSocket закрито, спроба повторного підключення...")
        self.reconnect_ws()

    def on_open(self, ws):
        log_info("Підключено до WebSocket, підписка на тікери...")
        subscribe_msg = {
            "method": "sub.tickers",
            "param": {}
        }
        ws.send(json.dumps(subscribe_msg))

        def ping_loop():
            while True:
                time.sleep(15)
                try:
                    ws.send(json.dumps({"method": "ping"}))
                    log_info("Відправлено ping")
                except Exception as e:
                    log_error(f"Помилка при відправці ping: {e}")
                    break  

        threading.Thread(target=ping_loop, daemon=True).start()

    def reconnect_ws(self):
        time.sleep(5)
        self.start_websocket()

    def start_websocket(self):
        """Запуск WebSocket у потоці"""
        self.ws = websocket.WebSocketApp(
            WS_URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()

    def get_prices(self):
        """Повертає актуальні ціни у вигляді словника"""
        with self.lock:
            return self.prices.copy()

# Глобальний екземпляр WebSocket
mexc_ws = MexcWebSocket()

def get_mexc_prices():
    """Функція для отримання цін (використовується у check_spreads)"""
    return mexc_ws.get_prices()

