#!/usr/bin/env python3
"""Spotify oyentes mensuales — vía Music Metrics Vault (página pública).
URL EXACTA, recuperada de la investigación manual del 15 nov 2026
(ver AUDIT.md): https://musicmetricsvault.com/artists/diezell/
2mEQCZzgLbG0mWCwaAEb3g — el slug lleva el nombre Y el id de Spotify;
las variantes /artists/diezell, /artist/diezell y /artists/{id} dan 404.

La página trae las cifras en su meta description
("44,147 monthly listeners, 16,525 followers") y el total de
streams ("5.5 million"). La fecha del dato NO es hoy: la página
dice "Last updated: X days ago" — esa fecha se usa como fecha del
registro, con el rezago anotado en el detalle. Si la página se
actualiza, el corte siguiente recoge el cambio.

Otras vías probadas el 18 nov 2026 (ver AUDIT.md, todas fallan):
- artist.tools: 403 y respuesta vacía en app.artist.tools.
- open.spotify.com/embed/artist/{id}: HTTP 200 pero sin el dato.
- Viberate: 403 dos veces con User-Agent de navegador.
- Livewire refreshData de MMV: el POST se quedó colgado 90 s sin
  respuesta; NO se reintenta (requiere aprobación para repetirlo).
"""
import os
import re
import sys
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_text, log, run_main,
                    save_snapshot, today_cdmx)

ARTIST_ID = "2mEQCZzgLbG0mWCwaAEb3g"
MMV_URL = ("https://musicmetricsvault.com/artists/diezell/"
           f"{ARTIST_ID}")


def _data_date(html):
    """Fecha a la que corresponde el dato de la página, según su
    'Last updated: X days/hours ago'. Devuelve (fecha, texto)."""
    m = re.search(r"Last updated:\s*([0-9]+)\s*(day|hour|minute|second)s?"
                  r"\s*ago", html, re.I)
    if not m:
        return today_cdmx(), "sin fecha de actualización en la página"
    n, unit = int(m.group(1)), m.group(2).lower()
    from datetime import datetime
    from zoneinfo import ZoneInfo
    now = datetime.now(ZoneInfo("America/Mexico_City"))
    if unit == "day":
        d = now - timedelta(days=n)
    elif unit == "hour":
        d = now - timedelta(hours=n)
    else:
        d = now
    return d.strftime("%Y-%m-%d"), m.group(0)


def main():
    try:
        status, html, _ = fetch_text(MMV_URL)
    except Exception as exc:
        log(f"  Music Metrics Vault: error: {exc}")
        return False
    if "monthly listeners" not in html.lower():
        log(f"  Music Metrics Vault: HTTP {status}, {len(html)} bytes — "
            "sin cifras de oyentes")
        return False
    save_snapshot("mmv", "artist_page_excerpt.txt",
                  "\n".join(re.findall(
                      r".{0,80}(?:monthly listeners|followers|"
                      r"Total Streams|Last updated).{0,80}",
                      html, re.I))[:4000])
    date, updated_txt = _data_date(html)
    detail_base = {"fuente_pagina": MMV_URL,
                   "actualizacion_pagina": updated_txt,
                   "nota": "fecha del registro = fecha del dato en la "
                           "página, no fecha del corte"}
    ok = False
    m = re.search(r"([0-9][0-9,]*)\s*monthly listeners,\s*"
                  r"([0-9][0-9,]*)\s*followers", html)
    if m:
        append_record("Music Metrics Vault", "spotify_monthly_listeners",
                      int(m.group(1).replace(",", "")),
                      "oyentes mensuales", url=MMV_URL,
                      detail={**detail_base}, date=date)
        append_record("Music Metrics Vault", "spotify_followers",
                      int(m.group(2).replace(",", "")),
                      "seguidores", url=MMV_URL,
                      detail={**detail_base}, date=date)
        log(f"  MMV: oyentes={m.group(1)} seguidores={m.group(2)} "
            f"(dato del {date})")
        ok = True
    m = re.search(r"Total Streams.{0,200}?([0-9]+(?:\.[0-9]+)?)\s*million",
                  html, re.S)
    if m:
        append_record("Music Metrics Vault", "spotify_total_streams",
                      int(float(m.group(1)) * 1_000_000),
                      "streams totales (aprox.)", url=MMV_URL,
                      detail={**detail_base, "aproximado": True,
                              "texto_original": m.group(0)[-40:]},
                      date=date)
        log(f"  MMV: streams totales ≈ {m.group(1)}M (dato del {date})")
        ok = True
    if not ok:
        log("  MMV: página cargada pero sin cifras parseables")
        return False
    return True


if __name__ == "__main__":
    sys.exit(run_main("spotify_public", main))
