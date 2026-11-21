#!/usr/bin/env python3
"""Bandsintown — página pública del artista (HTML, sin login).
Verificado 2026-11-18: HTTP 403 desde esta VM.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main


def main():
    try:
        status, html, _ = fetch_text(
            "https://www.bandsintown.com/a/diezell")
    except Exception as exc:
        log(f"  Bandsintown: error: {exc}")
        return False
    if status == 403:
        log("  Bandsintown: HTTP 403 — bloqueado")
        return False
    log(f"  Bandsintown: HTTP {status}, {len(html)} bytes")
    return True


if __name__ == "__main__":
    sys.exit(run_main("bandsintown_public", main))
