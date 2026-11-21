#!/usr/bin/env python3
"""TikTok — páginas públicas de hashtags (#Diezell, #Caoticos, #INSANIA).
Intenta extraer videos y conteos del HTML/JSON embebido.
Verificado 2026-11-18: la página carga pero no expone conteos
ni lista de videos parseable sin login — queda como hueco.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main

TAGS = ["Diezell", "Caoticos", "INSANIA"]


def main():
    found_any = False
    for tag in TAGS:
        url = f"https://www.tiktok.com/tag/{tag}"
        try:
            status, html, _ = fetch_text(url)
        except Exception as exc:
            log(f"  #{tag}: error al descargar: {exc}")
            continue
        m = re.search(r'"videoCount":\s*([0-9]+)', html)
        vids = re.findall(r'"id":"(\d{15,25})"', html)
        log(f"  #{tag}: HTTP {status}, {len(html)} bytes, "
            f"videoCount={'sí: ' + m.group(1) if m else 'no'}, "
            f"ids de video encontrados: {len(set(vids))}")
        if m or vids:
            found_any = True
    if not found_any:
        log("  ningún hashtag devolvió videos ni conteos parseables")
        return False
    return True


if __name__ == "__main__":
    sys.exit(run_main("tiktok_tag", main))
