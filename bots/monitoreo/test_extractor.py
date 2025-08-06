from extractor import extraer_drops_nike

drops = extraer_drops_nike()

for drop in drops:
    print(f"🟢 {drop['nombre']} - {drop['fecha']}")
    print(f"🔗 {drop['link']}")
    print("-----------")
