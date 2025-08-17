import os
from playwright.sync_api import sync_playwright

SESION_PATH = "sesion.json"

def iniciar_navegador(headless: bool = False):
    """
    Inicia Playwright + Chromium y crea un contexto.
    - Si existe sesion.json, la carga (mantiene login entre ejecuciones).
    - Devuelve (playwright, navegador, contexto, pagina, primera_ejecucion)
    """
    playwright = sync_playwright().start()
    navegador = playwright.chromium.launch(headless=headless)

    context_kwargs = dict(
        locale="es-CL",
        user_agent="Mozilla/5.0",
    )

    primera_ejecucion = not os.path.exists(SESION_PATH)
    if not primera_ejecucion:
        # Cargar sesión previamente guardada
        context_kwargs["storage_state"] = SESION_PATH

    contexto = navegador.new_context(**context_kwargs)
    pagina = contexto.new_page()

    return playwright, navegador, contexto, pagina, primera_ejecucion


def guardar_sesion(contexto, ruta: str = SESION_PATH):
    """
    Guarda cookies, localStorage y sessionStorage del contexto en un JSON.
    """
    contexto.storage_state(path=ruta)


def cerrar_todo(playwright, navegador, contexto, guardar_estado: bool = False):
    """
    Cierra ordenadamente. Si guardar_estado=True, persiste la sesión.
    """
    try:
        if guardar_estado:
            guardar_sesion(contexto)
    finally:
        try:
            contexto.close()
        except Exception:
            pass
        try:
            navegador.close()
        except Exception:
            pass
        try:
            playwright.stop()
        except Exception:
            pass