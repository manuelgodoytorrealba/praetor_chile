from navegador import iniciar_navegador
from playwright.sync_api import TimeoutError

def main():
    navegador, pagina = iniciar_navegador()

    try:
        # Ir a la página del producto
        pagina.goto("https://moredrops.cl/Drops/Genero/Hombre/Footwear-Men/Sneakers-Men/Mostro-Leather-Zapatilla-Puma-Unisex-Negro/p/PM40227301080", timeout=20000)

        # Esperar a que aparezca la talla US 9 y hacer clic
        pagina.wait_for_selector('a[title="US 9 UNSX"]')
        pagina.click('a[title="US 9 UNSX"]', timeout=5000)
        print("✅ Talla seleccionada")

        # Esperar a que cargue el botón y hacer clic en "Agregar al carro"
        pagina.wait_for_selector('button#addToCartButton', timeout=10000)
        pagina.click('button#addToCartButton')
        print("✅ Producto agregado al carrito")

    except TimeoutError as e:
        print(f"❌ Timeout: {e}")

    input("Presiona Enter para cerrar...")
    navegador.close()

if __name__ == "__main__":
    main()