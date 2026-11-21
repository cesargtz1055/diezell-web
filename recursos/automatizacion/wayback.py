#!/usr/bin/env python3
"""Wayback Machine — CDX API (sin clave) + recuperación de snapshots.
El CDX lista las capturas archivadas de páginas públicas (Spotify,
Viberate, YouTube, Instagram). La descarga de snapshots está
limitada por Wayback (HTTP 429 frecuente desde esta VM): se reintenta
con espera y, si no se puede, se guarda solo el inventario CDX.
Solo se guardan como registros los números verificables en el
contenido archivado; nunca se inventa un corte.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (FetchError, append_record, fetch_text, log, run_main,
                    save_snapshot)

TARGETS = {
    "Spotify": "open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g",
    "Viberate": "www.viberate.com/artist/diezell/",
    "YouTube": "youtube.com/@diezellmx",
    "Instagram": "instagram.com/diezellmx",
    "Music Metrics Vault": "musicmetricsvault.com/artists/diezell",
}

# Snapshots concretos que se intentan descargar y parsear (timestamp, url)
SNAPSHOT_TRIES = [
    ("20250815145512", "https://www.viberate.com/artist/diezell/"),
    ("20241007105455",
     "https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g"),
]


def _cdx(url):
    """Inventario CDX con reintentos: Wayback devuelve 429/503
    frecuentes desde esta IP y fetch_text lanza FetchError en
    HTTP >= 400 (antes el intento se perdía sin reintentar)."""
    q = ("https://web.archive.org/cdx/search/cdx?url=" + url +
         "&output=json&limit=50&filter=statuscode:200&collapse=digest")
    waits = [20, 40, 60]
    for attempt in range(3):
        try:
            status, body, _ = fetch_text(q)
        except FetchError as exc:
            if exc.status in (429, 503) and attempt < 2:
                log(f"  Wayback CDX: HTTP {exc.status}, esperando "
                    f"{waits[attempt]} s (intento {attempt + 1}/3)")
                time.sleep(waits[attempt])
                continue
            raise
        rows = json.loads(body)
        if not rows:
            return []
        header = rows[0]
        return [dict(zip(header, r)) for r in rows[1:]]
    return []


def main():
    inventory = {}
    for name, url in TARGETS.items():
        try:
            rows = _cdx(url)
        except Exception as exc:
            log(f"  Wayback CDX {name}: error: {exc}")
            continue
        inventory[name] = rows
        log(f"  Wayback CDX {name}: {len(rows)} capturas "
            f"(primera: {rows[0]['timestamp'] if rows else '-'}, "
            f"última: {rows[-1]['timestamp'] if rows else '-'})")
        time.sleep(1)
    save_snapshot("wayback", "cdx_inventory.json", inventory)

    got = False
    # fetch_text ya sigue redirecciones (curl -L). Lo que faltaba era
    # reintentar el 429/503: antes la excepción cortaba la descarga.
    waits = [20, 40, 60]
    for i, (ts, url) in enumerate(SNAPSHOT_TRIES):
        if i > 0:
            log(f"  Wayback: esperando 45 s antes de la siguiente "
                f"descarga")
            time.sleep(45)
        snap_url = f"https://web.archive.org/web/{ts}id_/{url}"
        status = None
        html = ""
        for attempt in range(3):
            try:
                status, html, _ = fetch_text(snap_url, timeout=120)
            except FetchError as exc:
                if exc.status in (429, 503) and attempt < 2:
                    log(f"  Wayback snapshot {ts}: HTTP {exc.status}, "
                        f"esperando {waits[attempt]} s "
                        f"(intento {attempt + 1}/3)")
                    time.sleep(waits[attempt])
                    continue
                log(f"  Wayback snapshot {ts}: error: {exc}")
                status = None
                break
            except Exception as exc:
                log(f"  Wayback snapshot {ts}: error: {exc}")
                status = None
                break
            break
        if status != 200 or len(html) < 1000:
            log(f"  Wayback snapshot {ts}: HTTP {status}, "
                f"{len(html)} bytes — sin contenido útil")
            continue
        save_snapshot("wayback", f"snapshot_{ts}.html", html[:20000])
        m = re.search(r"([0-9][0-9,]{3,})\s*monthly listeners", html, re.I)
        if m:
            log(f"  Wayback snapshot {ts}: oyentes mensuales en el "
                f"archivo: {m.group(1)}")
            got = True
        else:
            log(f"  Wayback snapshot {ts}: descargado, sin cifra de "
                "oyentes parseable")
    log("  Wayback: inventario CDX guardado; snapshots: "
        f"{'alguna cifra recuperada' if got else 'ninguna cifra verificable'}")
    return True


if __name__ == "__main__":
    sys.exit(run_main("wayback", main))
