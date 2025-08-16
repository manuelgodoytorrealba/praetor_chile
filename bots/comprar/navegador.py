from playwright.sync_api import sync_playwright
import random
import time
import json
import os
from pathlib import Path
import platform

def obtener_ruta_brave():
    """
    Obtiene la ruta de instalación de Brave según el sistema operativo
    """
    sistema = platform.system()
    
    if sistema == "Windows":
        # Rutas comunes en Windows
        rutas_posibles = [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Users\{}\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe".format(os.getenv("USERNAME")),
        ]
    elif sistema == "Darwin":  # macOS
        rutas_posibles = [
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ]
    else:  # Linux
        rutas_posibles = [
            "/usr/bin/brave-browser",
            "/usr/bin/brave",
            "/snap/bin/brave",
            "/opt/brave.com/brave/brave-browser",
        ]
    
    # Verificar qué ruta existe
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            return ruta
    
    # Si no encuentra ninguna, devolver None
    return None

def iniciar_navegador(usar_sesion_guardada=True, perfil_usuario="default"):
    """
    Inicializa el navegador Brave con configuración anti-detección y sesión persistente
    """
    playwright = sync_playwright().start()
    
    # Directorio para guardar datos del perfil
    perfil_dir = Path(f"perfil_{perfil_usuario}")
    perfil_dir.mkdir(exist_ok=True)
    
    # Obtener la ruta de Brave
    ruta_brave = obtener_ruta_brave()
    
    if not ruta_brave:
        print("⚠️ No se encontró Brave Browser instalado. Usando Chromium por defecto...")
        # Fallback a Chromium si no encuentra Brave
        navegador = playwright.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--no-first-run',
                '--no-default-browser-check',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
            ]
        )
    else:
        print(f"🦁 Iniciando Brave Browser desde: {ruta_brave}")
        # Configuración del navegador Brave para parecer humano
        navegador = playwright.chromium.launch(
            executable_path=ruta_brave,
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--no-first-run',
                '--no-default-browser-check',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                # Argumentos específicos para Brave
                '--disable-brave-update',
                '--disable-brave-wayback-machine',
                '--disable-brave-google-url-tracking',
            ]
        )
    
    # User agents reales rotatorios (manteniendo los mismos)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ]
    
    # Crear contexto con configuración anti-detección (sin cambios)
    contexto = navegador.new_context(
        locale="es-CL",
        timezone_id="America/Santiago",
        user_agent=random.choice(user_agents),
        viewport={"width": 1366, "height": 768},
        screen={"width": 1366, "height": 768},
        storage_state=str(perfil_dir / "storage_state.json") if usar_sesion_guardada and (perfil_dir / "storage_state.json").exists() else None,
        extra_http_headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    )
    
    pagina = contexto.new_page()
    
    # Inyectar script para ocultar automatización (sin cambios)
    pagina.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        Object.defineProperty(navigator, 'languages', {
            get: () => ['es-CL', 'es', 'en'],
        });
        
        window.chrome = {
            runtime: {},
        };
        
        Object.defineProperty(navigator, 'permissions', {
            get: () => ({
                query: () => Promise.resolve({ state: 'granted' }),
            }),
        });
    """)
    
    return navegador, pagina, contexto, perfil_dir

def simular_comportamiento_humano(pagina):
    """Simula comportamiento humano con movimientos de mouse y delays"""
    # Movimiento aleatorio del mouse
    pagina.mouse.move(
        random.randint(100, 800), 
        random.randint(100, 600)
    )
    
    # Delay aleatorio
    time.sleep(random.uniform(0.5, 2.0))

def guardar_sesion(contexto, perfil_dir):
    """Guarda el estado de la sesión (cookies, localStorage, etc.)"""
    try:
        contexto.storage_state(path=str(perfil_dir / "storage_state.json"))
        print("✅ Sesión guardada exitosamente")
    except Exception as e:
        print(f"⚠️ Error guardando sesión: {e}")

def login_si_necesario(pagina, email=None, password=None):
    """
    Verifica si necesita hacer login y lo realiza si es necesario
    """
    try:
        # Verificar si ya está logueado (buscar elemento que indica usuario logueado)
        if pagina.locator('[data-testid="user-menu"], .user-account, .mi-cuenta').is_visible(timeout=3000):
            print("✅ Ya está logueado")
            return True
            
        # Si no está logueado, ir a login
        print("🔑 Necesita hacer login...")
        
        # Buscar botón de login/registro
        login_button = pagina.locator('a:has-text("Ingresar"), a:has-text("Login"), .login-button')
        if login_button.is_visible(timeout=5000):
            simular_comportamiento_humano(pagina)
            login_button.click()
            
            # Aquí agregarías la lógica específica de login para footlocker.es
            # Por ahora solo esperamos a que el usuario haga login manual
            print("👤 Por favor, haz login manualmente...")
            input("Presiona Enter después de hacer login...")
            
            return True
        else:
            print("⚠️ No se encontró botón de login")
            return False
            
    except Exception as e:
        print(f"❌ Error en login: {e}")
        return False