import requests

def enviar_a_discord(mensaje, webhook_url):
    data = {
        "content": mensaje
    }
    requests.post(webhook_url, json=data)