#!/usr/bin/env python3
"""setlist.fm — páginas públicas (HTML, sin clave; la API exige clave).
Verificado 2026-11-18: la búsqueda devuelve HTTP 202 con cuerpo vacío
(cola anti-bot), tanto en /search?query=Diezell como en
/search?artist=Diezell. Tampoco se localizó la página del artista:
una búsqueda en Bing y en DuckDuckGo de site:setlist.fm Diezell no
devuelve ningún enlace, y adivinar el slug es inviable (un slug
probado redirigió a otro artista, Reuben Hernandez). Se reintenta
en cada corte por si el anti-bot se levanta.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main


def main():
    try:
        status, html, _ = fetch_text(
            "https://www.setlist.fm/search?query=Diezell")
    except Exception as exc:
        log(f"  setlist.fm: error: {exc}")
        return False
    if status == 202 or len(html) < 1000:
        log(f"  setlist.fm: HTTP {status}, {len(html)} bytes — "
            "respuesta vacía (anti-bot)")
        return False
    log(f"  setlist.fm: HTTP {status}, {len(html)} bytes")
    return True


if __name__ == "__main__":
    sys.exit(run_main("setlistfm_public", main))
