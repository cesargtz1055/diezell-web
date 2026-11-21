#!/usr/bin/env python3
"""Prensa — feeds RSS directos de los medios que cubren a Diezell.
Puro Rock Puro, Follow Control, Mr Indie, Punkeando.
Solo se guardan los artículos que mencionan a Diezell (título o texto).
Campos por artículo: título, enlace, fecha, autor, categorías.
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (add_mention, append_record, fetch_text, log, run_main,
                    save_snapshot)

FEEDS = {
    "Puro Rock Puro": "https://purorockpuro.com/feed/",
    "Follow Control": "https://followcontrol.com/feed/",
    "Mr Indie": "https://mrindie.com/feed/",
    "Punkeando": "https://punkeando.com.mx/feed/",
}


def _items(xml_text):
    out = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return out
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        pub = (it.findtext("pubDate") or "").strip()
        creator = (it.findtext(
            "{http://purl.org/dc/elements/1.1/}creator") or "").strip()
        cats = [c.text for c in it.findall("category") if c.text]
        content = (it.findtext(
            "{http://purl.org/rss/1.0/modules/content/}encoded") or "")
        if title and link:
            out.append({"title": title, "link": link, "pubDate": pub,
                        "creator": creator, "categories": cats,
                        "content": content})
    return out


def main():
    total = 0
    for name, url in FEEDS.items():
        try:
            status, xml, _ = fetch_text(url)
        except Exception as exc:
            log(f"  {name}: error al descargar: {exc}")
            continue
        items = _items(xml)
        save_snapshot("press_rss", f"{name.replace(' ', '_')}.xml", xml)
        hits = [i for i in items
                if "diezell" in (i["title"] + " " + i["content"]).lower()]
        append_record("Prensa RSS", "press_mentions", len(hits),
                      "artículos sobre Diezell", url=url,
                      detail={"key": f"medio:{name}",
                              "articulos_totales_en_feed": len(items)})
        for h in hits:
            total += 1
            add_mention(name, "artículo", h["title"], h["link"])
        log(f"  {name}: {len(items)} artículos en el feed, "
            f"{len(hits)} sobre Diezell")
    if total == 0:
        log("  Prensa: ningún artículo sobre Diezell en los feeds de hoy")
        return "empty"
    log(f"  Prensa total: {total} artículos sobre Diezell")
    return True


if __name__ == "__main__":
    sys.exit(run_main("press_rss", main))
