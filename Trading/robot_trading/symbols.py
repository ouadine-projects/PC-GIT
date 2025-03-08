import websocket
import json
import os
from dotenv import load_dotenv

# Charger les identifiants depuis .env
load_dotenv()
USER_ID = os.getenv("XTB_USER_ID")
PASSWORD = os.getenv("XTB_PASSWORD")
XTB_API_URL = "wss://ws.xtb.com/demo"

# Fonction pour afficher la liste des instruments disponibles
def get_all_symbols():
    request = {"command": "getAllSymbols"}
    ws.send(json.dumps(request))

def on_message(ws, message):
    response = json.loads(message)
    if "returnData" in response:
        for symbol in response["returnData"][:-1]:  # Afficher les 10 premiers
            print(f"📈 Symbole : {symbol['symbol']} - {symbol['description']}")

def on_open(ws):
    """Authentifie et récupère les symboles tradables"""
    auth_request = {
        "command": "login",
        "arguments": {
            "userId": USER_ID,
            "password": PASSWORD
        }
    }
    ws.send(json.dumps(auth_request))
    ws.send(json.dumps({"command": "getAllSymbols"}))

ws = websocket.WebSocketApp(XTB_API_URL, on_message=on_message, on_open=on_open)
ws.run_forever()
