# 🛠️ PRAETOR Chile - Sistema de Bots para Drops Exclusivos

**PRAETOR Chile** es una herramienta modular que automatiza la compra y monitoreo de productos limitados en tiendas online de Chile y otras regiones. Diseñado para escalar, cuenta con 3 componentes principales:

---

## ⚙️ Estructura del Proyecto

```
├── backend
│   ├── api            # (Futuro) API para control externo
│   └── db             # (Futuro) DB o registros locales
├── bots
│   ├── comprar_drops  # Bot para automatizar compras
│   └── monitoreo      # Bot para detectar lanzamientos y productos exclusivos
├── config             # Configuraciones globales (tokens, headers, urls)
├── dashboard          # (Futuro) Panel de control para gestión visual
├── logs               # Logs y errores
├── scripts            # Ejecutores auxiliares o utils
└── README.md          # Este archivo
```

---

## 📦 Requisitos

* Python 3.11+
* Playwright

```bash
pip install playwright
playwright install
```

---

## 🤖 BOT 1: comprar\_drops

Automatiza el proceso de compra en páginas como **MoreDrops.cl**.

### 🔧 Archivo principal:

`bots/comprar_drops/main.py`

### 📌 Funciones actuales:

* Acceder a la URL del producto.
* Elegir talla.
* Agregar al carrito.

### 🏁 Cómo ejecutarlo:

```bash
python bots/comprar_drops/main.py
```

---

## 🛰️ BOT 2: monitoreo

Detecta nuevos productos, drops o lanzamientos desde páginas como **Nike**, y los reporta.

### 🔧 Archivos principales:

* `extractor.py`: obtiene los datos dinámicamente con Playwright.
* `watcher.py`: compara nuevos productos con `db.json` para evitar duplicados.
* `discord_webhook.py`: envía notificaciones a un canal de Discord.

### 🏁 Cómo ejecutarlo:

```bash
python bots/monitoreo/test_extractor.py           # Solo extracción
python bots/monitoreo/watcher.py                  # Monitoreo continuo + Discord
```

### 💬 Webhook Discord

* Usa un archivo `.env` o variable global para configurar el Webhook:

```python
WEBHOOK_URL = "https://discord.com/api/webhooks/..."
```

---

## 📲 BOT 3: Integración con Discord

* Manda mensajes con información de drops en tiempo real.
* Se integra con el bot de monitoreo.
* Ideal para comunidades privadas (como un servidor premium).

### 🏁 Cómo probar un mensaje:

```python
from discord_webhook import enviar_mensaje

enviar_mensaje("🧠 ¡Hola mundo! Drop detectado.")
```

---

## 🧩 Features a implementar (próximamente)

* [ ] Monitoreo multiplataforma (Bold.cl, Drops.cl, TheLine.cl)
* [ ] Soporte a múltiples cuentas / sesiones guardadas
* [ ] Dashboard visual para controlar los bots
* [ ] Compras automáticas desde URLs programadas
* [ ] Filtros personalizados para detectar productos según reglas

---

## ✍️ Autor

* Proyecto desarrollado por Manuel Godoy
* Colaboración con Juan
* Licencia privada ⚠️
