# bots/monitoreo/test_webhook.py

from discord_webhook import enviar_a_discord

# 🧠 Pega aquí la URL real de tu webhook de Discord
webhook = "https://discord.com/api/webhooks/1402416625613013032/8UEOIIBB_V1gmrvdl4_Zc09POx9tD8LfuOEW4XmImUdU-1ZaN9T7TErkpuB4K964t-5M"

mensaje = "👋 ¡Hola desde PRAETOR Chile! Esto es una prueba."

enviar_a_discord(mensaje, webhook)
