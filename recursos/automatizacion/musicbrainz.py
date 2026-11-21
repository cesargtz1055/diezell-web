#!/usr/bin/env python3
"""MusicBrainz — API sin clave (1 req/seg, User-Agent propio).
Capa de identidad: MBID del artista, lanzamientos, relaciones.
Verificado 2026-11-18: Diezell NO está en MusicBrainz
(búsqueda de artista y de lanzamiento devuelven count 0).
Se vuelve a comprobar en cada corte por si alguien lo da de alta.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_json, log, run_main, save_snapshot, UA_BOT

BASE = "https://musicbrainz.org/ws/2"


def main():
    status, data = fetch_json(
        f"{BASE}/artist/?query=artist:Diezell&fmt=json", ua=UA_BOT)
    save_snapshot("musicbrainz", "artist_search.json", data)
    if data.get("count", 0) == 0:
        log("  MusicBrainz: artista 'Diezell' no encontrado (count 0)")
        time.sleep(1.2)
        status, rel = fetch_json(
            f"{BASE}/release/?query=release:Ca%C3%B3tico%20AND%20"
            f"artist:Diezell&fmt=json", ua=UA_BOT)
        save_snapshot("musicbrainz", "release_search.json", rel)
        if rel.get("count", 0) == 0:
            log("  MusicBrainz: lanzamiento 'Caótico' tampoco encontrado")
            return "empty"
    log(f"  MusicBrainz: {data.get('count')} artista(s) encontrado(s)")
    return True


if __name__ == "__main__":
    sys.exit(run_main("musicbrainz", main))
