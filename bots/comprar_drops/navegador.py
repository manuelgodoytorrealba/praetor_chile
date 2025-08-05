from playwright.sync_api import sync_playwright


def iniciar_navegador():
   playwright = sync_playwright().start()
   navegador = playwright.chromium.launch(headless=False, )
   contexto = navegador.new_context(locale="es-CL", user_agent="Mozilla/5.0")
   pagina = contexto.new_page()
   return navegador, pagina