"""Capturas y verificaciones del prototipo de portada Diezell (dirección Papel/Archivo).
Sirve http://127.0.0.1:8940/index.html (python3 -m http.server 8940 en direccion-visual/).
Uso: ~/workspace/.venv-playwright/bin/python test-capturas.py
"""
import json, sys
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8940/index.html"
OUT = "/home/hatch/workspace/diezell-publish/direccion-visual/capturas"
results = {}

with sync_playwright() as p:
    b = p.chromium.launch()
    # --- full page + hero por ancho ---
    for w in (360, 390, 768, 1440):
        pg = b.new_page(viewport={"width": w, "height": 800})
        pg.goto(BASE, wait_until="networkidle")
        pg.wait_for_timeout(400)
        # overflow horizontal
        overflow = pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        results[f"overflow_px_{w}"] = overflow
        # hero visible en primer viewport (360/390): H1 y CTA principal
        if w in (360, 390):
            hero = pg.evaluate("""() => {
              const h1 = document.querySelector('h1').getBoundingClientRect();
              const cta = document.querySelector('.cta-row .btn-solid').getBoundingClientRect();
              const foto = document.querySelector('.hero-foto img').getBoundingClientRect();
              return {h1_top: Math.round(h1.top), h1_bottom: Math.round(h1.bottom),
                      cta_top: Math.round(cta.top), cta_bottom: Math.round(cta.bottom),
                      foto_h: Math.round(foto.height), vh: window.innerHeight};
            }""")
            results[f"hero_viewport_{w}"] = hero
            pg.screenshot(path=f"{OUT}/hero-{w}.png")
        # recorrer la página para activar los .reveal antes de la captura completa
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(500)
        pg.evaluate("window.scrollTo(0, 0)")
        pg.wait_for_timeout(200)
        pg.screenshot(path=f"{OUT}/pagina-{w}.png", full_page=True)
        pg.close()

    # --- menú móvil a 360: abrir con clic, verificar aria y Escape ---
    pg = b.new_page(viewport={"width": 360, "height": 800})
    pg.goto(BASE, wait_until="networkidle")
    pg.click("#menu-btn")
    results["menu_aria_expanded"] = pg.get_attribute("#menu-btn", "aria-expanded")
    results["menu_visible"] = pg.evaluate("getComputedStyle(document.querySelector('.nav')).display")
    pg.screenshot(path=f"{OUT}/menu-abierto-360.png")
    pg.keyboard.press("Escape")
    results["menu_despues_escape"] = pg.get_attribute("#menu-btn", "aria-expanded")
    # teclado: Tab desde el inicio llega al skip-link y al botón de menú
    pg.keyboard.press("Tab")
    results["foco_tras_tab"] = pg.evaluate("document.activeElement.className || document.activeElement.tagName")
    pg.close()

    # --- footer a 1440 ---
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(BASE, wait_until="networkidle")
    pg.evaluate("document.querySelector('footer').scrollIntoView()")
    pg.wait_for_timeout(400)
    pg.screenshot(path=f"{OUT}/footer-1440.png")
    pg.close()

    # --- reduced motion: los .reveal deben ser visibles sin animación ---
    pg = b.new_page(viewport={"width": 390, "height": 800}, reduced_motion="reduce")
    pg.goto(BASE, wait_until="networkidle")
    op = pg.evaluate("getComputedStyle(document.querySelector('.sec-head.reveal')).opacity")
    results["reveal_opacity_reduced_motion"] = op
    pg.close()
    b.close()

print(json.dumps(results, indent=2, ensure_ascii=False))
