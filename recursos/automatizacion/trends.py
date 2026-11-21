#!/usr/bin/env python3
"""Google Trends — interés por 'Diezell'.
CERRADO como no viable (G16, 18 nov 2026): la API explore devuelve
HTTP 429 sin cookies de sesión y el RSS de tendencias diarias es
genérico (top búsquedas, no por término). No hay vía gratuita sin
login para el interés por término y no se reintenta más: este
colector ya NO está en run_daily.sh. Se conserva el archivo como
registro de lo probado.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main


def main():
    url = ("https://trends.google.com/trends/api/explore?hl=es&tz=-360"
           "&req=%7B%22comparisonItem%22:%5B%7B%22keyword%22:%22Diezell%22"
           "%2C%22geo%22:%22MX%22%2C%22time%22:%22today%2012-m%22%7D%5D"
           "%2C%22category%22:0%2C%22property%22:%22%22%7D")
    try:
        status, body, _ = fetch_text(url)
    except Exception as exc:
        log(f"  Google Trends explore: error: {exc}")
        return False
    if status == 429 or "Too Many Requests" in body:
        log(f"  Google Trends explore: HTTP {status} — bloqueado sin "
            "cookies de sesión (cerrado como no viable, G16)")
        return False
    log(f"  Google Trends explore: HTTP {status}, {len(body)} bytes")
    return True
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main


def main():
    url = ("https://trends.google.com/trends/api/explore?hl=es&tz=-360"
           "&req=%7B%22comparisonItem%22:%5B%7B%22keyword%22:%22Diezell%22"
           "%2C%22geo%22:%22MX%22%2C%22time%22:%22today%2012-m%22%7D%5D"
           "%2C%22category%22:0%2C%22property%22:%22%22%7D")
    try:
        status, body, _ = fetch_text(url)
    except Exception as exc:
        log(f"  Google Trends explore: error: {exc}")
        return False
    if status == 429 or "Too Many Requests" in body:
        log(f"  Google Trends explore: HTTP {status} — bloqueado sin "
            "cookies de sesión")
        return False
    log(f"  Google Trends explore: HTTP {status}, {len(body)} bytes")
    return True


if __name__ == "__main__":
    sys.exit(run_main("trends", main))
