#!/usr/bin/env python3
"""Facebook — plugin público de la página (sin token, sin login).
Verificado 2026-11-20: facebook.com/plugins/page.php con
href=diezelloficial y tabs=timeline devuelve HTTP 200 (~85 KB) con
JSON embebido real: pageID, pageName y los últimos 5 posts con
message + createdTime (epoch) + attachmentType. No trae seguidores
ni likes (follower_count/fan_count/like_count: 0 coincidencias) ni
paginación: solo los últimos 5 posts. Un registro por post, con la
fecha real del post (no la del corte).
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_text, log, run_main,
                    save_snapshot)

PLUGIN_URL = ("https://www.facebook.com/plugins/page.php"
              "?href=https%3A%2F%2Fwww.facebook.com%2Fdiezelloficial"
              "&tabs=timeline&width=340&height=500")
PAGE_URL = "https://www.facebook.com/diezelloficial"
TZ = ZoneInfo("America/Mexico_City")


def _unescape(s):
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return s.encode("utf-8", "ignore").decode("unicode_escape",
                                                  "ignore")


def parse_posts(html):
    """Devuelve [{ts, date, message, attachment}] de los posts del plugin."""
    posts = []
    pat = re.compile(r'"message":\s*"((?:\\.|[^"\\])*)"\s*,\s*"createdTime":\s*(\d+)')
    for m in pat.finditer(html):
        ts = int(m.group(2))
        date = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(TZ).strftime("%Y-%m-%d")
        tail = html[m.end():m.end() + 400]
        att = re.search(r'"attachmentType":\s*"(\w+)"', tail)
        posts.append({
            "ts": ts,
            "date": date,
            "message": _unescape(m.group(1)),
            "attachment": att.group(1) if att else "",
        })
    return posts


def main():
    status, html, _ = fetch_text(PLUGIN_URL, timeout=60)
    if status != 200 or len(html) < 1000:
        log(f"  Facebook plugin: HTTP {status}, {len(html)} bytes")
        return False
    page_id = re.search(r'"pageID":\s*"?(\d+)"?', html)
    page_name = re.search(r'"pageName":\s*"([^"]+)"', html)
    log(f"  Facebook plugin: pageID="
        f"{page_id.group(1) if page_id else '?'} "
        f"pageName={page_name.group(1) if page_name else '?'} "
        f"({len(html)} bytes)")
    posts = parse_posts(html)
    if not posts:
        log("  Facebook plugin: sin posts parseables")
        return False
    save_snapshot("facebook_plugin",
                  "posts.json",
                  json.dumps(posts, ensure_ascii=False, indent=2))
    nuevos = 0
    for p in posts:
        if append_record("Facebook", "facebook_post", 1, "post",
                         url=PAGE_URL, date=p["date"],
                         detail={"key": f"facebook_post:{p['ts']}",
                                 "message": p["message"][:500],
                                 "attachment": p["attachment"],
                                 "createdTime": p["ts"]}):
            nuevos += 1
    log(f"  Facebook plugin: {len(posts)} posts, {nuevos} nuevos "
        f"(fechas: {', '.join(sorted({p['date'] for p in posts}))})")
    return True


if __name__ == "__main__":
    sys.exit(run_main("facebook_plugin", main))
