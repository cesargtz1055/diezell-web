#!/usr/bin/env python3
"""Google News RSS — búsqueda de 'Diezell', sin clave.
Campos por noticia: título, enlace, fecha, fuente.
Cada noticia nueva queda como mención fechada con su URL.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (add_mention, append_record, fetch_text, log,
                    parse_rss_items, run_main, save_snapshot_once)

QUERIES = ["Diezell", "Diezell banda Monterrey"]

# La búsqueda es difusa: "Diezell Kunst" es un artista plástico
# argentino (Sebastián Dávalos), no la banda. Solo valen noticias
# cuyo título nombra a la banda.
DENYLIST = ["kunst"]


def _es_de_la_banda(title):
    t = (title or "").lower()
    if "diezell" not in t:
        return False
    return not any(w in t for w in DENYLIST)


def main():
    total = 0
    nuevas = 0
    for q in QUERIES:
        url = ("https://news.google.com/rss/search?q="
               + q.replace(" ", "%20")
               + "&hl=es-419&gl=MX&ceid=MX:es-419")
        try:
            status, xml, _ = fetch_text(url)
        except Exception as exc:
            log(f"  Google News '{q}': error: {exc}")
            continue
        items = parse_rss_items(xml)
        save_snapshot_once("google_news", f"q_{q.split()[0]}.xml", xml)
        band = [i for i in items if _es_de_la_banda(i["title"])]
        append_record("Google News RSS", "news_mentions_raw", len(items),
                      "noticias en el feed (sin filtrar)", url=url,
                      detail={"key": f"q:{q}"})
        append_record("Google News RSS", "news_mentions", len(band),
                      "noticias sobre la banda", url=url,
                      detail={"key": f"q:{q}"})
        for it in band:
            total += 1
            if add_mention("Google News", "noticia", it["title"],
                           it["link"], date=None):
                nuevas += 1
        log(f"  Google News '{q}': {len(items)} noticias en el feed, "
            f"{len(band)} sobre la banda")
    if total == 0:
        log("  Google News: sin resultados en ninguna búsqueda")
        return False
    log(f"  Google News total: {total} noticias, {nuevas} menciones nuevas")
    return True


if __name__ == "__main__":
    sys.exit(run_main("google_news_rss", main))
