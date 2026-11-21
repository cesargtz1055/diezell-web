#!/usr/bin/env python3
"""Facebook — página pública de Diezell (HTML, sin login).
Verificado 2026-11-18: /diezelloficial da 302 al login y /diezellmx
da 400 y redirige al login. Sin vía gratuita sin login.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main


def main():
    for slug in ("diezelloficial", "diezellmx"):
        try:
            status, html, final = fetch_text(
                f"https://www.facebook.com/{slug}")
        except Exception as exc:
            log(f"  Facebook /{slug}: error: {exc}")
            continue
        if status in (302, 301) or "login" in final:
            log(f"  Facebook /{slug}: HTTP {status} → {final} — "
                "muro de login")
            continue
        log(f"  Facebook /{slug}: HTTP {status}, {len(html)} bytes")
        return True
    log("  Facebook: los dos slugs probados terminan en muro de login")
    return False


if __name__ == "__main__":
    sys.exit(run_main("facebook_public", main))
