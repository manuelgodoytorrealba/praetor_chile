from navegador import iniciar_navegador, simular_comportamiento_humano, guardar_sesion, login_si_necesario
from playwright.sync_api import TimeoutError
import time
import random

def esperar_con_reintento(pagina, selector, timeout=3000, reintentos=3):
    """Espera un elemento con reintentos"""
    for i in range(reintentos):
        try:
            pagina.wait_for_selector(selector, timeout=timeout)
            return True
        except TimeoutError:
            if i < reintentos - 1:
                print(f"⏳ Reintentando... ({i+1}/{reintentos})")
                time.sleep(1)
            else:
                return False
    return False

def click_con_comportamiento_humano(pagina, selector, timeout=3000):
    """Hace clic simulando comportamiento humano"""
    try:
        elemento = pagina.locator(selector)
        elemento.wait_for(state="visible", timeout=timeout)
        
        # Simular hover del raton antes del click
        elemento.hover()
        time.sleep(random.uniform(0.3, 0.8))
        
        # Click con comportamiento humano
        elemento.click()
        time.sleep(random.uniform(0.5, 1.5))
        return True
        
    except Exception as e:
        print(f"❌ Error haciendo click en {selector}: {e}")
        return False

def verificar_disponibilidad_stock(pagina):
    """Verifica si hay stock disponible"""
    try:
        sin_stock_selectors = [
            'text="Sin stock"',
            'text="Agotado"', 
            '.out-of-stock',
            '[data-testid="out-of-stock"]'
        ]
        
        for selector in sin_stock_selectors:
            if pagina.locator(selector).is_visible(timeout=2000):
                return False
        return True
    except:
        return True

def encontrar_y_seleccionar_talla(pagina, talla_objetivo):
    """
    Función específica para Footlocker
    Las tallas están como botones con texto simple (40, 42, 44, etc.)
    """
    print(f"👟 Buscando talla {talla_objetivo}...")
    
    # Lista de selectores específicos para Footlocker
    selectores_talla = [
        f'button:has-text("{talla_objetivo}")',  # Botón con texto exacto
        f'button:text("{talla_objetivo}")',      # Selector text de Playwright
        f'[data-testid*="size"] button:has-text("{talla_objetivo}")',
        f'.size-selector button:has-text("{talla_objetivo}")',
        f'.sizes button:has-text("{talla_objetivo}")',
        f'button[aria-label*="{talla_objetivo}"]',
        f'div:has-text("{talla_objetivo}") button',
        f'button:has-text("{talla_objetivo}"):not([disabled])'  # No deshabilitados
    ]
    
    # Esperar que aparezca el texto "Selecciona una talla"
    print("📏 Esperando que cargue la sección de tallas...")
    try:
        pagina.wait_for_selector('text="Selecciona una talla"', timeout=3000)
        print("✅ Sección de tallas cargada")
    except:
        print("⚠️ No se encontró 'Selecciona una talla', continuando...")
    
    # Esperar que los botones de talla estén visibles
    try:
        pagina.wait_for_selector('button', timeout=4000)
        time.sleep(1)  # Pequeña pausa para asegurar carga completa
        print("✅ Botones de talla listos")
    except:
        print("⚠️ Error esperando botones de talla")
    
    # Intentar encontrar la talla con diferentes selectores
    for i, selector in enumerate(selectores_talla):
        try:
            print(f"🔍 Probando selector {i+1}: {selector}")
            elemento_talla = pagina.locator(selector).first
            
            if elemento_talla.is_visible(timeout=3000):
                # Verificar si el elemento está habilitado
                if elemento_talla.is_enabled():
                    print(f"✅ Talla encontrada y disponible: {selector}")
                    
                    # Scroll hasta el elemento si es necesario
                    elemento_talla.scroll_into_view_if_needed()
                    time.sleep(0.5)
                    
                    # Hover y click
                    elemento_talla.hover()
                    time.sleep(random.uniform(0.3, 0.8))
                    elemento_talla.click()
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    # Verificar si la selección fue exitosa
                    if verificar_seleccion_talla(pagina, talla_objetivo):
                        print(f"✅ Talla {talla_objetivo} seleccionada exitosamente")
                        return True
                    else:
                        print(f"⚠️ La talla se clickeó pero no se seleccionó correctamente")
                else:
                    print(f"❌ Talla encontrada pero no está disponible: {selector}")
            else:
                print(f"❌ Talla no visible con selector: {selector}")
                
        except Exception as e:
            print(f"❌ Error con selector {selector}: {e}")
            continue
    
    # Si no se encuentra, mostrar tallas disponibles
    mostrar_tallas_disponibles(pagina)
    return False

def verificar_seleccion_talla(pagina, talla_objetivo):
    """Verifica si la talla fue seleccionada correctamente"""
    try:
        # Buscar indicadores de talla seleccionada
        selectores_seleccionada = [
            f'[class*="selected"]:has-text("{talla_objetivo}")',
            f'[class*="active"]:has-text("{talla_objetivo}")',
            f'[aria-selected="true"]:has-text("{talla_objetivo}")',
            f'.size-selected:has-text("{talla_objetivo}")'
        ]
        
        for selector in selectores_seleccionada:
            if pagina.locator(selector).is_visible(timeout=2000):
                return True
        
        return False
    except:
        return False

def mostrar_tallas_disponibles(pagina):
    """Muestra las tallas disponibles específicas para Footlocker"""
    print("\n📋 Buscando tallas disponibles...")
    
    # Selectores específicos para botones de talla en Footlocker
    selectores_busqueda_tallas = [
        'button:near(:text("Selecciona una talla"))',  # Botones cerca del texto
        'div:has-text("Selecciona una talla") ~ div button',  # Botones hermanos
        'div:has-text("Selecciona una talla") + div button',
        'button:below(:text("Selecciona una talla"))',  # Botones debajo
        'div button:visible',  # Todos los botones visibles
        'button:not([disabled]):visible'  # Botones no deshabilitados
    ]
    
    tallas_encontradas = []
    
    for selector in selectores_busqueda_tallas:
        try:
            elementos = pagina.locator(selector).all()
            print(f"🔍 Probando selector: {selector} - Encontrados: {len(elementos)}")
            
            for elemento in elementos:
                try:
                    # Obtener el texto del botón
                    texto = elemento.inner_text().strip()
                    
                    # Solo tallas que parezcan números de zapato (1-3 dígitos)
                    if texto and len(texto) <= 5 and any(c.isdigit() for c in texto):
                        if texto not in tallas_encontradas:
                            # Verificar si está habilitado
                            esta_habilitado = elemento.is_enabled()
                            estado = "✅" if esta_habilitado else "❌"
                            tallas_encontradas.append(f"{estado} {texto}")
                        
                except Exception as e:
                    continue
        except Exception as e:
            print(f"❌ Error con selector {selector}: {e}")
            continue
    
    if tallas_encontradas:
        print("📏 Tallas disponibles encontradas:")
        for talla in tallas_encontradas:
            print(f"  - {talla}")
    else:
        print("❌ No se pudieron encontrar tallas disponibles")
        # Debug: mostrar todos los botones visibles
        try:
            todos_botones = pagina.locator('button:visible').all()
            print(f"🔍 Debug: Se encontraron {len(todos_botones)} botones en total")
            for i, boton in enumerate(todos_botones[:10]):  # Solo primeros 10
                try:
                    texto = boton.inner_text().strip()
                    if texto:
                        print(f"   Botón {i+1}: '{texto}'")
                except:
                    print(f"   Botón {i+1}: (sin texto)")
        except:
            print("❌ Error en debug de botones")

def main():
    # Configuración del producto
    PRODUCTO_URL = "https://www.footlocker.es/es/product/adidas-adizero-aruku-hombre-zapatillas/314217192104.html"
    TALLA_OBJETIVO = "42"  # Cambiar a formato EU (42 en lugar de US 9)

    navegador, pagina, contexto, perfil_dir = iniciar_navegador(usar_sesion_guardada=True)

    try:
        print("🚀 Iniciando bot de compra...")
        print(f"🎯 Buscando talla EU: {TALLA_OBJETIVO}")
        
        # Ir a la página principal primero
        pagina.goto("https://footlocker.es", timeout=30000)
        simular_comportamiento_humano(pagina)
        
        # Verificar login
        if not login_si_necesario(pagina):
            print("❌ No se pudo verificar/realizar el login")
        
        # Ir al producto específico
        print(f"📦 Navegando al producto...")
        pagina.goto(PRODUCTO_URL, timeout=30000)
        
        # Verificar que la página cargó correctamente
        if not esperar_con_reintento(pagina, 'body', timeout=15000):
            print("❌ Error: La página no cargó correctamente")
            return
        
        simular_comportamiento_humano(pagina)
        
        # Verificar disponibilidad
        if not verificar_disponibilidad_stock(pagina):
            print("❌ Producto sin stock")
            return
        
        # NUEVA LÓGICA DE SELECCIÓN DE TALLA
        if not encontrar_y_seleccionar_talla(pagina, TALLA_OBJETIVO):
            print(f"❌ No se pudo seleccionar la talla {TALLA_OBJETIVO}")
            return
        
        # Esperar a que se actualice el botón de agregar al carrito
        time.sleep(random.uniform(1, 3))
        
        # Agregar al carrito
        print("🛒 Agregando al carrito...")
        boton_carrito_selectors = [
            'button#addToCartButton',
            'button:has-text("Agregar al carro")',
            'button:has-text("Añadir al carrito")',
            'button:has-text("Add to cart")',
            '[data-testid="add-to-cart"]',
            '.add-to-cart-button',
            '.btn-add-to-cart'
        ]
        
        boton_encontrado = False
        for selector in boton_carrito_selectors:
            try:
                elemento = pagina.locator(selector).first
                if elemento.is_visible(timeout=3000) and elemento.is_enabled():
                    print(f"✅ Botón de carrito encontrado: {selector}")
                    if click_con_comportamiento_humano(pagina, selector):
                        print("✅ Producto agregado al carrito")
                        boton_encontrado = True
                        break
            except:
                continue
        
        if not boton_encontrado:
            print("❌ No se encontró el botón de agregar al carrito")
            return
        
        # Verificar confirmación
        confirmacion_selectors = [
            'text="Producto agregado"',
            'text="Agregado al carrito"',
            '.cart-notification',
            '[data-testid="cart-confirmation"]'
        ]
        
        for selector in confirmacion_selectors:
            if pagina.locator(selector).is_visible(timeout=5000):
                print("✅ Confirmación recibida")
                break
        
        # Opcional: proceder al checkout
        proceder_checkout = input("\n¿Quieres proceder al checkout? (s/n): ").lower().strip()
        
        if proceder_checkout == 's':
            print("🛒 Procediendo al carrito...")
            carrito_selectors = [
                'a[href*="cart"]',
                '.cart-button',
                '[data-testid="cart-button"]',
                'text="Ver carrito"'
            ]
            
            for selector in carrito_selectors:
                if pagina.locator(selector).is_visible(timeout=3000):
                    click_con_comportamiento_humano(pagina, selector)
                    print("✅ Navegando al carrito")
                    break
        
        # Guardar sesión
        guardar_sesion(contexto, perfil_dir)

    except TimeoutError as e:
        print(f"❌ Timeout: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    finally:
        input("\nPresiona Enter para cerrar...")
        navegador.close()

if __name__ == "__main__":
    main()