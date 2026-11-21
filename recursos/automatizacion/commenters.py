#!/usr/bin/env python3
"""Top comentaristas — agrega comments.json por mes y por autor.
Solo nombres públicos, con enlace al comentario original.
Si no hay comentarios guardados, el ranking queda vacío (honesto).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (COMMENTS_PATH, COMMENTERS_PATH, load_json_file, log,
                    run_main, today_cdmx)


def main():
    if not os.path.exists(COMMENTS_PATH):
        log("  commenters: no existe comments.json")
        return False
    data = load_json_file(COMMENTS_PATH)
    by_month = {}
    for c in data.get("comments", []):
        # El mes es el MES DE CAPTURA (c["date"]), no el texto relativo
        # de publicación ("4 years ago" no es una fecha: cortarlo
        # daba meses basura como "4 years" o "1 day a").
        month = (c.get("date", "") or "")[:7] or today_cdmx()[:7]
        m = by_month.setdefault(month, {})
        a = m.setdefault(c["author"], {
            "count": 0, "sources": [], "example_url": c.get("post_url", ""),
        })
        a["count"] += 1
        if c["source"] not in a["sources"]:
            a["sources"].append(c["source"])
    out = {"version": 1, "updated": today_cdmx(), "by_month": by_month}
    tmp = COMMENTERS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    os.replace(tmp, COMMENTERS_PATH)
    total = sum(len(m) for m in by_month.values())
    log(f"  commenters: {total} autores en {len(by_month)} mes(es)")
    return True


if __name__ == "__main__":
    sys.exit(run_main("commenters", main))
