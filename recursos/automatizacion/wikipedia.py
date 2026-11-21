#!/usr/bin/env python3
"""Wikipedia — artículo y visitas (API pública, sin clave).
Verificado 2026-11-18: el artículo es.wikipedia.org/wiki/Diezell
devuelve 404 (no existe) y la API de pageviews devuelve 404 para
cualquier rango. Se comprueba en cada corte por si se crea el artículo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_json, fetch_text, log, run_main,
                    save_snapshot)


def main():
    status, data = fetch_json(
        "https://es.wikipedia.org/w/api.php?action=query&format=json"
        "&titles=Diezell&prop=info&inprop=url")
    save_snapshot("wikipedia", "article_check.json", data)
    pages = data.get("query", {}).get("pages", {})
    exists = not any("missing" in p for p in pages.values())
    log(f"  Wikipedia: artículo 'Diezell' existe: {exists}")
    if not exists:
        return "empty"
    status, pv = fetch_json(
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/"
        "per-article/es.wikipedia/all-access/user/Diezell/"
        "daily/20261101/20261117")
    save_snapshot("wikipedia", "pageviews.json", pv)
    items = pv.get("items", [])
    for it in items:
        append_record("Wikipedia", "wikipedia_pageviews", it["views"],
                      "visitas", url="https://es.wikipedia.org/wiki/Diezell",
                      detail={"key": f"día:{it['timestamp'][:8]}",
                              "timestamp": it["timestamp"]},
                      date=f"{it['timestamp'][:4]}-{it['timestamp'][4:6]}"
                      f"-{it['timestamp'][6:8]}")
    log(f"  Wikipedia: {len(items)} días de visitas")
    return bool(items)


if __name__ == "__main__":
    sys.exit(run_main("wikipedia", main))
