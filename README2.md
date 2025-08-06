🛠️ ¿Cómo lo montamos paso a paso?
FASE 1 – MVP simple:
 Hacer scraping de https://www.nike.com/launch.
 Extraer: nombre del producto, fecha, URL.
 Comparar con lo guardado en db.json.
 Si es nuevo, mandar a Discord.
 Repetir cada 60 segundos.



📌 Objetivo del bot
Este bot está diseñado para monitorear drops exclusivos y productos limitados en tiendas seleccionadas.
Su misión es:
Detectar productos nuevos, cambios de stock o fechas de lanzamiento.
Enviar la información a un canal privado de Discord usando webhooks.
Ayudar a construir una comunidad de reventa informada y actualizada.
⚙️ Estructura del proyecto
bots/monitoreo/
├── watcher.py           → Ejecuta el bucle de monitoreo
├── extractor.py         → Obtiene productos desde sitios web
├── filtro.py            → Compara con histórico para detectar novedades
├── discord_webhook.py   → Envía mensajes al canal de Discord
├── db.json              → Registro de productos ya anunciados
🌐 Sitios web monitoreados (curados)
sneakernews.com
nicekicks.com/sneaker-release-dates
thedropdate.com
highsnobiety.com
kicksonfire.com
nike.com/launch
moredrops.cl
bold.cl
theline.cl
🔁 Funcionamiento básico
El bot revisa los sitios cada X segundos/minutos.
Extrae los productos visibles (nombre, link, precio, ID).
Compara con el histórico (db.json).
Si encuentra un producto nuevo, envía alerta a Discord.
Tu comunidad recibe la información directamente en su canal.
🛠 Próximas mejoras sugeridas
Añadir filtros por marca/modelo (ej: solo Yeezy, Travis, Jordan).
Añadir soporte para embeds enriquecidos en Discord.
Hacer scraping de fechas y horas exactas si están disponibles.
Soporte multitienda y multicategoría.
Crear un panel visual para ver histórico y estadísticas de drops.
