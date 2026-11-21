#!/usr/bin/env python3
"""YouTube — página pública del canal @diezellmx (HTML, sin login).
Campos: id del canal (verificado contra el esperado), título,
suscriptores (texto aproximado del canal, ej. '12.2K'), total de videos.
Si la página cambia de estructura o bloquea, falla y se registra.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_text, log, parse_compact_number,
                    run_main, save_snapshot)

CHANNEL_ID = "UCwj0Exix_EnCMB7X5ncov1Q"
CHANNEL_URL = "https://www.youtube.com/@diezellmx"


def main():
    status, html, _ = fetch_text(CHANNEL_URL)
    m = re.search(r'<link rel="canonical" href="https://www\.youtube\.com'
                  r'/channel/(UC[^"]+)"', html)
    if not m:
        log("  no se encontró el enlace canónico del canal")
        return False
    if m.group(1) != CHANNEL_ID:
        log(f"  el canal cambió de id: {m.group(1)} (esperado {CHANNEL_ID})")
        return False
    save_snapshot("youtube_public", "channel_excerpt.txt",
                  "\n".join(re.findall(
                      r".{0,60}(?:subscriber|videos|Diezell).{0,60}",
                      html))[:3000])
    ok = False
    # La página en español dice "12.2 mil suscriptores"; en inglés "12.2K"
    ms = re.search(
        r"([0-9][0-9.,]*)\s*(K|mil)?\s*(?:subscribers|suscriptores)", html)
    if ms:
        val = float(ms.group(1).replace(",", ""))
        mult = 1000 if ms.group(2) in ("K", "mil") else 1
        val = int(val * mult)
        append_record("YouTube", "youtube_subscribers", val,
                      "suscriptores (texto aproximado del canal)",
                      url=CHANNEL_URL,
                      detail={"key": "canal",
                              "texto_original": ms.group(0),
                              "aproximado": True})
        ok = True
    mv = re.search(r'"videosCountText":\{"runs":\[\{"text":"([0-9,]+)"',
                   html)
    if not mv:
        mv = re.search(r"([0-9]+) videos", html)
    if mv:
        append_record("YouTube", "youtube_videos_total",
                      int(mv.group(1).replace(",", "")), "videos",
                      url=CHANNEL_URL, detail={"key": "canal"})
        ok = True
    if not ok:
        log("  no se pudo extraer ni suscriptores ni total de videos")
        return False
    log("  YouTube canal: suscriptores y total de videos extraídos")
    return True


if __name__ == "__main__":
    sys.exit(run_main("youtube_public", main))
