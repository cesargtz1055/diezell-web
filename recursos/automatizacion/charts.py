#!/usr/bin/env python3
"""Charts — ¿está Diezell en alguna lista? (sin clave).
Deezer chart global top 10 e iTunes México top 25 canciones/álbumes.
Es una comprobación de presencia: si aparece, se registra el puesto;
si no, queda en el log. Verificado 2026-11-18: no está en ninguna.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_json, fetch_text, log, run_main,
                    save_snapshot)


def _check(name, entries, key_fn):
    for i, e in enumerate(entries, start=1):
        if "diezell" in key_fn(e).lower():
            log(f"  Charts: ¡Diezell en {name}, puesto {i}!")
            return i
    log(f"  Charts: Diezell no está en {name}")
    return None


def main():
    status, chart = fetch_json(
        "https://api.deezer.com/chart/0/tracks?limit=10")
    save_snapshot("charts", "deezer_chart.json", chart)
    rank = _check("Deezer chart global (top 10)", chart.get("data", []),
                  lambda t: t["title"] + " " + t["artist"]["name"])
    if rank:
        append_record("Deezer", "deezer_chart_rank", rank, "puesto",
                      url="https://www.deezer.com/charts",
                      detail={"key": "chart_global"})

    status, xml, _ = fetch_text(
        "https://itunes.apple.com/mx/rss/topsongs/limit=25/json")
    data = json.loads(xml)
    entries = data.get("feed", {}).get("entry", [])
    save_snapshot("charts", "itunes_mx_topsongs.json", data)
    rank = _check("iTunes México top canciones (25)",
                  entries, lambda e: e["im:artist"]["label"] + " " +
                  e["im:name"]["label"])
    if rank:
        append_record("iTunes", "itunes_mx_chart_rank", rank, "puesto",
                      url="https://music.apple.com/mx/charts",
                      detail={"key": "top_canciones"})

    status, xml, _ = fetch_text(
        "https://itunes.apple.com/mx/rss/topalbums/limit=25/json")
    data = json.loads(xml)
    entries = data.get("feed", {}).get("entry", [])
    save_snapshot("charts", "itunes_mx_topalbums.json", data)
    rank = _check("iTunes México top álbumes (25)",
                  entries, lambda e: e["im:artist"]["label"] + " " +
                  e["im:name"]["label"])
    if rank:
        append_record("iTunes", "itunes_mx_chart_rank_album", rank,
                      "puesto", url="https://music.apple.com/mx/charts",
                      detail={"key": "top_albumes"})
    return True


if __name__ == "__main__":
    sys.exit(run_main("charts", main))
