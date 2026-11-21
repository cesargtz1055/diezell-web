#!/usr/bin/env python3
"""SoundCloud — localizar el perfil de Diezell sin login.
Verificado 2026-11-18: soundcloud.com/diezell es OTRO usuario
(Alycyalyna), soundcloud.com/diezellmx da 404, y la búsqueda
web no expone URLs de usuario sin JS. Perfil no localizado.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main

CANDIDATES = [
    "https://soundcloud.com/diezell",
    "https://soundcloud.com/diezellmx",
    "https://soundcloud.com/diezell-oficial",
]


def main():
    for url in CANDIDATES:
        try:
            status, html, final = fetch_text(url)
        except Exception as exc:
            log(f"  SoundCloud {url}: error: {exc}")
            continue
        m = re.search(r'"username":"([^"]+)"', html)
        user = m.group(1) if m else "?"
        log(f"  SoundCloud {url}: HTTP {status} → usuario: {user}")
        if user.lower() in ("diezell", "diezellmx"):
            log("  SoundCloud: perfil de Diezell localizado")
            return True
    log("  SoundCloud: perfil de Diezell no localizado en ningún slug")
    return False


if __name__ == "__main__":
    sys.exit(run_main("soundcloud", main))
