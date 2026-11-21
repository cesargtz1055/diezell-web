#!/usr/bin/env python3
"""Last.fm — página pública del artista (HTML, sin login).
La página alterna entre la versión real y una de reto anti-bot
(3 KB). Solo se considera éxito si se extraen oyentes/scrobbles.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_text, log, run_main,
                    save_snapshot)


def main():
    status, html, _ = fetch_text("https://www.last.fm/music/Diezell")
    if len(html) < 10000 or "fs-ch" in html:
        log(f"  Last.fm: HTTP {status}, {len(html)} bytes — "
            "página de reto anti-bot, sin datos")
        return False
    save_snapshot("lastfm_public", "page_excerpt.txt",
                  "\n".join(re.findall(
                      r".{0,80}(?:listeners|scrobbles|oyentes).{0,80}",
                      html, re.I))[:8000])
    found = False
    # Cifra del encabezado del artista (oyentes/scrobbles de Last.fm)
    m = re.search(
        r"artist-header-featured-items-item-listeners[^>]*>\s*"
        r"([0-9][0-9,]*)\s+listeners", html)
    if m:
        append_record("Last.fm", "lastfm_listeners",
                      int(m.group(1).replace(",", "")), "oyentes",
                      url="https://www.last.fm/music/Diezell",
                      detail={"key": "artista",
                              "nota": "cifra del encabezado del artista"})
        found = True
    # Scrobbles del encabezado (G9): el bloque real de Last.fm es
    # header-metadata-tnew (título "Scrobbles" + <abbr title="N">);
    # la clase artist-header-featured-items-item-scrobbles ya no
    # existe en la página. El title del abbr lleva la cifra exacta
    # (64,736); el texto visible es abreviado (64.7K).
    m = re.search(
        r"header-metadata-tnew-title\">\s*Scrobbles\s*</h4>"
        r".{0,600}?intabbr[^>]*title=\"([0-9,]+)\"",
        html, re.S)
    if not m:
        m = re.search(
            r"artist-header-featured-items-item-scrobbles[^>]*>\s*"
            r"([0-9][0-9,]*)", html)
    if not m:
        m = re.search(r"([0-9][0-9,]*)\s+scrobbles", html, re.I)
    if m:
        append_record("Last.fm", "lastfm_scrobbles",
                      int(m.group(1).replace(",", "")), "scrobbles",
                      url="https://www.last.fm/music/Diezell",
                      detail={"key": "artista"})
        found = True
    # Total de oyentes del artista (mismo bloque): 2,169 el 18 nov.
    # OJO: el "lastfm_listeners" histórico (15) es en realidad la
    # cifra de la canción "Popular this week", no el total del
    # artista; se registra aparte sin borrar el anterior.
    m = re.search(
        r"header-metadata-tnew-title\">\s*Listeners\s*</h4>"
        r".{0,600}?intabbr[^>]*title=\"([0-9,]+)\"",
        html, re.S)
    if m:
        append_record("Last.fm", "lastfm_listeners_total",
                      int(m.group(1).replace(",", "")), "oyentes",
                      url="https://www.last.fm/music/Diezell",
                      detail={"key": "artista",
                              "nota": "total del artista; el "
                              "lastfm_listeners histórico (15) es "
                              "la cifra semanal de la canción "
                              "popular, no el total"})
        found = True
    # Oyentes por álbum (top de la página)
    albums = re.findall(
        r"artist-top-albums-item-aux-text[^>]*>\s*([0-9][0-9,]*)\s+listeners",
        html)
    titles = re.findall(
        r"artist-top-albums-item-name[^>]*>\s*<a[^>]*>([^<]+)</a>", html)
    for title, num in zip(titles[:5], albums[:5]):
        append_record("Last.fm", "lastfm_album_listeners",
                      int(num.replace(",", "")), "oyentes",
                      url="https://www.last.fm/music/Diezell",
                      detail={"key": f"álbum:{title.strip()}",
                              "title": title.strip()})
        found = True
    if not found:
        log(f"  Last.fm: HTTP {status}, {len(html)} bytes — página real "
            "pero sin cifras de oyentes/scrobbles parseables")
        return False
    log("  Last.fm: cifras extraídas")
    return True


if __name__ == "__main__":
    sys.exit(run_main("lastfm_public", main))
