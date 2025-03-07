import websocket
import json
import os
#from dotenv import load_dotenv

# Charger les identifiants depuis .env
#load_dotenv()
USER_ID = os.getenv("XTB_USER_ID")
PASSWORD = os.getenv("XTB_PASSWORD")
XTB_API_URL = "wss://ws.xtb.com/demo"

# Paramètres du trade
SYMBOL = "EURUSD"   # Instrument à surveiller
VOLUME = 0.1        # Volume du trade (en lots)
SL = 20             # Stop Loss en pips
TP = 100            # Take Profit en pips
target_price = 1.0800  # 🎯 Prix auquel ouvrir la position

# WebSocket client
ws = None

def open_trade():
    """Ouvre un ordre BUY quand le prix atteint target_price."""
    order_request = {
        "command": "tradeTransaction",
        "arguments": {
            "tradeTransInfo": {
                "cmd": 0,  # 0 = BUY, 1 = SELL
                "symbol": SYMBOL,
                "volume": VOLUME,
                "price": target_price,
                "sl": target_price - SL * 0.0001,  # SL en pips
                "tp": target_price + TP * 0.0001,  # TP en pips
                "type": 0  # Ordre au marché
            }
        }
    }
    ws.send(json.dumps(order_request))
    print(f"🚀 Ordre BUY envoyé à {target_price} pour {SYMBOL}")

def on_message(ws, message):
    """Gère les messages reçus du serveur XTB."""
    response = json.loads(message)
    
    # Vérifie si le message contient un prix
    if "returnData" in response and "bid" in response["returnData"]:
        bid_price = response["returnData"]["bid"]
        print(f"📉 Prix actuel : {bid_price}")

        # Vérifie si le prix atteint le niveau cible
        if bid_price <= target_price:
            print(f"🎯 Prix atteint ({target_price}) ! Envoi de l'ordre...")
            open_trade()

def on_open(ws):
    """Connexion réussie : authentification et abonnement aux prix."""
    print("🟢 Connexion ouverte")

    # 🔹 Authentification
    auth_request = {
        "command": "login",
        "arguments": {
            "userId": USER_ID,
            "password": PASSWORD
        }
    }
    ws.send(json.dumps(auth_request))

    # 🔹 Abonnement aux prix du symbole choisi
    price_request = {
        "command": "subscribePrice",
        "arguments": {"symbol": SYMBOL}
    }
    ws.send(json.dumps(price_request))
    print(f"📡 Abonné aux prix de {SYMBOL}")

def on_error(ws, error):
    print(f"🚨 Erreur : {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔴 Connexion fermée")

# 🔹 Lancer la connexion WebSocket
ws = websocket.WebSocketApp(
    XTB_API_URL, 
    on_message=on_message,
    on_error=on_error, 
    on_close=on_close
)
ws.on_open = on_open
ws.run_forever()
