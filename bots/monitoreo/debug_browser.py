from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)  # headless=False abre navegador
    contexto = navegador.new_context(locale="es-ES")
    pagina = contexto.new_page()

    pagina.goto("https://www.nike.com/launch", timeout=60000)

    print("🟢 Página cargada. Usa las DevTools (clic derecho > Inspeccionar) para probar selectores.")
    
    input("Presiona Enter para cerrar...")
    navegador.close()  # Espera 1 minuto para que puedas inspeccionar
