import websocket
import json
import threading
import time
import os
#from dotenv import load_dotenv

# Charger les identifiants depuis le fichier .env
#load_dotenv()
USER_ID = os.getenv("XTB_USER_ID")
PASSWORD = os.getenv("XTB_PASSWORD")

XTB_API_URL = "wss://ws.xtb.com/demo"

ws = None  

def on_message(ws, message):
    """Gère les messages reçus du serveur."""
    response = json.loads(message)
    print("Réponse reçue:", response)

    # Vérifie si la réponse contient le solde
    if "balance" in response:
        print(f"💰 Solde disponible : {response['balance']}")
        print(f"📊 Marge utilisée : {response['margin']}")

def on_error(ws, error):
    """Gère les erreurs de connexion."""
    print("🚨 Erreur:", error)

def on_close(ws, close_status_code, close_msg):
    """Gère la fermeture de connexion."""
    print("🔴 Connexion fermée")

def on_open(ws):
    """S'exécute une fois la connexion WebSocket ouverte."""
    print("🟢 Connexion ouverte")

    # 🔹 Requête d'authentification
    auth_request = {
        "command": "login",
        "arguments": {
            "userId": USER_ID,
            "password": PASSWORD
        }
    }
    ws.send(json.dumps(auth_request))

    # 🔹 Lancer la récupération du solde après 2 secondes
    time.sleep(2)
    get_balance()

    # 🔹 Lancer le "ping" automatique pour garder la connexion ouverte
    threading.Thread(target=keep_alive, daemon=True).start()

def get_balance():
    """Récupère le solde et la marge disponible du compte XTB."""
    balance_request = {
        "command": "getMarginLevel"
    }
    ws.send(json.dumps(balance_request))

def keep_alive():
    """Envoie un ping toutes les 25 secondes pour garder la connexion ouverte."""
    while True:
        time.sleep(25)
        ping_request = {"command": "ping"}
        ws.send(json.dumps(ping_request))
        print("📡 Ping envoyé pour garder la connexion active")

# 🔹 Vérification avant exécution
if not USER_ID or not PASSWORD:
    print("🚨 Erreur : Identifiants XTB non définis.")
else:
    ws = websocket.WebSocketApp(
        XTB_API_URL, 
        on_message=on_message,
        on_error=on_error, 
        on_close=on_close
    )
    ws.on_open = on_open

    ws.run_forever()
