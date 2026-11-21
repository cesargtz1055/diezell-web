#!/usr/bin/env python3
"""Bing News RSS — búsqueda de 'Diezell', sin clave.
Campos por noticia: título, enlace, fecha, fuente.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (add_mention, append_record, fetch_text, log,
                    parse_rss_items, run_main, save_snapshot_once)


def main():
    url = "https://www.bing.com/news/search?q=Diezell&format=rss"
    status, xml, _ = fetch_text(url)
    items = parse_rss_items(xml)
    save_snapshot_once("bing_news", "diezell.xml", xml)
    band = [i for i in items
            if "diezell" in i["title"].lower()
            and "kunst" not in i["title"].lower()]
    append_record("Bing News RSS", "news_mentions_raw", len(items),
                  "noticias en el feed (sin filtrar)", url=url,
                  detail={"key": "q:Diezell"})
    append_record("Bing News RSS", "news_mentions", len(band),
                  "noticias sobre la banda", url=url,
                  detail={"key": "q:Diezell"})
    nuevas = 0
    for it in band:
        if add_mention("Bing News", "noticia", it["title"], it["link"]):
            nuevas += 1
    log(f"  Bing News: {len(items)} noticias en el feed, "
        f"{len(band)} sobre la banda, {nuevas} menciones nuevas")
    return True


if __name__ == "__main__":
    sys.exit(run_main("bing_news_rss", main))
