#!/usr/bin/env python3
"""YouTube RSS — feed público del canal, sin clave.
Canal verificado: UCwj0Exix_EnCMB7X5ncov1Q (canonical de @diezellmx).
El candidato UChJ53mAWy11h1fC0Xb14D3A es OTRO canal (Rene Martínez): NO usar.
Campos por video: id, título, fecha de publicación, enlace.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import re
import xml.etree.ElementTree as ET
from common import (append_record, fetch_text, log, parse_rss_items,
                    run_main, save_snapshot, today_cdmx)

CHANNEL_ID = "UCwj0Exix_EnCMB7X5ncov1Q"
CHANNEL_URL = "https://www.youtube.com/@diezellmx"


def _video_id(link):
    m = re.search(r"[?&]v=([A-Za-z0-9_-]{11})", link or "")
    if m:
        return m.group(1)
    m = re.search(r"/shorts/([A-Za-z0-9_-]{11})", link or "")
    if m:
        return m.group(1)
    return link


def main():
    url = (f"https://www.youtube.com/feeds/videos.xml"
           f"?channel_id={CHANNEL_ID}")
    status, xml, _ = fetch_text(url)
    items = parse_rss_items(xml)
    if not items:
        log("  RSS vacío o sin entradas")
        return False
    save_snapshot("youtube_rss", "feed.xml", xml)
    # título del canal = primer <title> del feed
    root = ET.fromstring(xml)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    ch_title = root.findtext("atom:title", namespaces=ns) or ""
    if ch_title != "Diezell":
        log(f"  el feed ya no es de Diezell (título: {ch_title})")
        return False
    append_record("YouTube RSS", "youtube_video_feed_count", len(items),
                  "videos en el feed", url=CHANNEL_URL,
                  detail={"key": "feed"})
    # Un video solo cuenta como nuevo si se publicó HOY (fecha del
    # corte). Antes se contaba cada video del feed en cada corte y
    # salían 15 "nuevos" todos los días aunque no hubiera ninguno.
    hoy = today_cdmx()
    nuevos = 0
    for it in items:
        vid = _video_id(it["link"])
        pub = (it.get("pubDate", "") or "")[:10]
        if pub != hoy:
            continue
        if append_record("YouTube RSS", "youtube_video_new", 1, "video",
                         url=it["link"],
                         detail={"key": f"video:{vid}",
                                 "title": it["title"],
                                 "published": it.get("pubDate", ""),
                                 "video_id": vid}):
            nuevos += 1
    log(f"  YouTube RSS: {len(items)} videos en el feed, {nuevos} nuevos "
        f"(publicados el {hoy})")
    return True


if __name__ == "__main__":
    sys.exit(run_main("youtube_rss", main))
