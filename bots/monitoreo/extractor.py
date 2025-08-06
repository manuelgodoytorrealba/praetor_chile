from playwright.sync_api import sync_playwright

def extraer_drops_nike():
    productos = []

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        contexto = navegador.new_context(locale="es-ES")
        pagina = contexto.new_page()

        pagina.goto("https://www.nike.com/launch", timeout=30000)
        pagina.wait_for_timeout(5000)  # Espera fija para carga JS

        # También puedes guardar HTML para inspección si falla
        with open("nike_debug.html", "w", encoding="utf-8") as f:
            f.write(pagina.content())

        # Probar nuevos selectores (ajustables si cambia el HTML)
        cards = pagina.query_selector_all("div[data-qa='product-card-info']")

        for card in cards:
            nombre = card.query_selector("h3")
            fecha = card.query_selector("p")
            link_tag = card.evaluate_handle("el => el.closest('a')")

            producto = {
                "nombre": nombre.inner_text().strip() if nombre else "Sin nombre",
                "fecha": fecha.inner_text().strip() if fecha else "Sin fecha",
                "link": link_tag.get_attribute("href") if link_tag else "Sin link"
            }

            if producto["link"].startswith("/"):
                producto["link"] = f"https://www.nike.com{producto['link']}"

            productos.append(producto)

        navegador.close()

    return productos
