#!/usr/bin/env python3
"""Reddit — endpoints .json sin clave (www, api, old) + pullpush.io.
Verificado 2026-11-18: desde esta VM los tres .json devuelven la
página HTML (theme-beta) o redirigen; no hay JSON utilizable.
pullpush.io: api.pullpush.io responde (raíz: "Reddit Search API")
pero TODAS las rutas de búsqueda dan 404 "endpoint not found"
(/search/reddit/submissions/?q=, sin barra final, /api/search/...,
/api/v1/search/...); la documentación en pullpush.io está tras
Cloudflare (403). Sin vía gratuita sin login desde esta VM.
Se intenta en cada corte por si cambia; si falla, se registra y se sigue.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (add_mention, append_record, fetch_text, log, run_main,
                    save_snapshot, UA_BOT)

URLS = [
    "https://www.reddit.com/search.json?q=Diezell&sort=new&limit=25",
    "https://api.reddit.com/search?q=Diezell&sort=new&limit=25",
    "https://old.reddit.com/search.json?q=Diezell&sort=new&limit=25",
]


def main():
    import json
    for url in URLS:
        try:
            status, body, _ = fetch_text(url, ua=UA_BOT)
        except Exception as exc:
            log(f"  Reddit {url}: error: {exc}")
            continue
        if body.lstrip().startswith("{"):
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                log(f"  Reddit {url}: JSON inválido")
                continue
            posts = data.get("data", {}).get("children", [])
            save_snapshot("reddit", "search.json", data)
            append_record("Reddit", "reddit_mentions", len(posts),
                          "posts", url=url, detail={"key": "q:Diezell"})
            for p in posts:
                d = p.get("data", {})
                add_mention("Reddit", "post", d.get("title", ""),
                            "https://www.reddit.com" + d.get("permalink", ""))
            log(f"  Reddit {url}: {len(posts)} posts")
            return True
        log(f"  Reddit {url}: HTTP {status}, devuelve HTML "
            f"({len(body)} bytes) en vez de JSON — bloqueado")
    log("  Reddit: ningún endpoint .json devolvió datos utilizables")
    return False


if __name__ == "__main__":
    sys.exit(run_main("reddit", main))
