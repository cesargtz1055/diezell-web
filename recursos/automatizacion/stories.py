#!/usr/bin/env python3
"""Rescate de historias — solo vías sin login.
Instagram: las historias exigen sesión; no hay endpoint público
(documentado en README). TikTok: la página pública del perfil
no expone historia activa en su JSON (verificado 2026-11-18).
Si algún día aparece una URL de medio de historia en una página
pública, se descarga el archivo a archivo/stories/YYYY-MM-DD/
(nunca se guarda solo la URL: los enlaces firmados caducan).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import BASE, fetch_text, log, run_main, today_cdmx

STORIES_DIR = os.path.join(BASE, "archivo", "stories")


def main():
    status, html, _ = fetch_text("https://www.tiktok.com/@diezellmx")
    m = re.search(
        r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" '
        r'type="application/json">(.*?)</script>', html, re.S)
    found = False
    if m:
        data = json.loads(m.group(1))
        blob = json.dumps(data)
        if re.search(r'"hasStory"\s*:\s*true', blob):
            log("  TikTok: ¡historia activa detectada! (falta descargar)")
            found = True
        else:
            log("  TikTok: sin indicador de historia activa en la "
                "página pública")
    else:
        log("  TikTok: sin JSON embebido para revisar historias")
    log("  Instagram: rescate imposible sin login (ver README)")
    os.makedirs(os.path.join(STORIES_DIR, today_cdmx()), exist_ok=True)
    return "empty" if not found else True


if __name__ == "__main__":
    sys.exit(run_main("stories", main))
