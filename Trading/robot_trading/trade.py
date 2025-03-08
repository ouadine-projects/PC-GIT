import websocket
import json
import time
import os
#from dotenv import load_dotenv

# Charger les identifiants depuis .env
#load_dotenv()
USER_ID = os.getenv("XTB_USER_ID")
PASSWORD = os.getenv("XTB_PASSWORD")
XTB_API_URL = "wss://ws.xtb.com/demo"

# Paramètres du trade
SYMBOL = "EURUSD"
VOLUME = 0.1  # 0.1 lot
SL_PIPS = 20   # Stop Loss (pips)
TP_PIPS = 100  # Take Profit (pips)

# Fonction pour récupérer le prix actuel du marché
def get_price():
    """Envoie une requête pour obtenir le prix actuel du marché"""
    price_request = {
        "command": "getSymbol",
        "arguments": {"symbol": SYMBOL}
    }
    ws.send(json.dumps(price_request))

# Fonction pour ouvrir un trade
def open_trade(price):
    """Ouvre un trade au marché avec SL et TP"""
    sl_price = price - (SL_PIPS * 0.0001)  # Convertir pips en prix
    tp_price = price + (TP_PIPS * 0.0001)  # Convertir pips en prix

    trade_request = {
        "command": "tradeTransaction",
        "arguments": {
            "tradeTransInfo": {
                "cmd": 0,  # 0 = BUY, 1 = SELL
                "symbol": SYMBOL,
                "volume": VOLUME,
                "sl": round(sl_price, 5),
                "tp": round(tp_price, 5),
                "type": 0,  # 0 = Ordre au marché
                "price": price,
                "customComment": "Trade API",
                "expiration": 0
            }
        }
    }
    ws.send(json.dumps(trade_request))
    print(f"📈 Position BUY sur {SYMBOL} envoyée ! SL: {sl_price} | TP: {tp_price}")

# Fonction de gestion des messages reçus
def on_message(ws, message):
    """Gère les messages reçus du serveur"""
    response = json.loads(message)
    print("Réponse reçue:", response)

    if "ask" in response.get("returnData", {}):  # Vérifier si on reçoit le prix
        price = response["returnData"]["ask"]
        print(f"💲 Prix actuel EUR/USD: {price}")
        open_trade(price)

    if response.get("status") and response.get("returnData"):
        print("✅ Trade confirmé !")

# Fonction d'authentification
def on_open(ws):
    """Authentifie l'utilisateur et lance la requête de prix"""
    auth_request = {
        "command": "login",
        "arguments": {
            "userId": USER_ID,
            "password": PASSWORD
        }
    }
    ws.send(json.dumps(auth_request))
    time.sleep(2)  # Attendre la connexion

    # Récupérer le prix actuel avant d'ouvrir la position
    get_price()

# Connexion WebSocket
ws = websocket.WebSocketApp(XTB_API_URL, on_message=on_message, on_open=on_open)
ws.run_forever()
