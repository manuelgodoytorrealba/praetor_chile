# bots/monitoreo/discord_webhook.py

import requests

def enviar_a_discord(mensaje, webhook_url):
    data = {
        "content": mensaje
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("✅ Mensaje enviado correctamente")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
