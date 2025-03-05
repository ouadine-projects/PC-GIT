import websocket
import json
import os
#from dotenv import load_dotenv

# Charger les identifiants depuis .env
#load_dotenv()
USER_ID = os.getenv("XTB_USER_ID")
PASSWORD = os.getenv("XTB_PASSWORD")
XTB_API_URL = "wss://ws.xtb.com/demo"

def on_message(ws, message):
    """Gère les réponses du serveur XTB"""
    response = json.loads(message)
    
    # Vérifier si la réponse contient des symboles
    if response.get("status") and "returnData" in response:
        symbols = response["returnData"][:-1]  # Afficher seulement 10 symboles
        print("📜 Liste des 10 premiers symboles disponibles :\n")
        for symbol in symbols:
            market_status = "✅ Ouvert" if symbol.get("trading") else "❌ Fermé"
            print(f"📈 {symbol['symbol']} - {symbol['description']} | {market_status}")

def on_open(ws):
    """Authentifie l'utilisateur et demande les symboles"""
    print("🔐 Tentative de connexion...")

    auth_request = {
        "command": "login",
        "arguments": {
            "userId": USER_ID,
            "password": PASSWORD
        }
    }
    ws.send(json.dumps(auth_request))

    # Attendre la connexion avant d'envoyer la requête des symboles
    ws.send(json.dumps({"command": "getAllSymbols"}))

def on_error(ws, error):
    """Gère les erreurs de connexion"""
    print(f"🚨 Erreur WebSocket : {error}")

def on_close(ws, close_status_code, close_msg):
    """Affiche un message quand la connexion est fermée"""
    print("🔴 Connexion WebSocket fermée.")

# Initialisation WebSocket
ws = websocket.WebSocketApp(
    XTB_API_URL,
    on_message=on_message,
    on_open=on_open,
    on_error=on_error,
    on_close=on_close
)

# Exécuter la connexion WebSocket
ws.run_forever()
