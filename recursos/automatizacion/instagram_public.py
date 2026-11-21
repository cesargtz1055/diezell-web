#!/usr/bin/env python3
"""Instagram — perfil público @diezellmx sin login.
Vías probadas: endpoint web_profile_info (HTTP 429), página HTML
(200 pero muro de login, sin datos del perfil), ?__a=1 (302 a
login, probado 18 nov 2026) y /diezellmx/embed/ (200 pero cáscara
JS sin datos del perfil, probado 18 nov 2026).
Verificado 2026-11-18: no hay vía gratuita sin login desde esta VM.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main, UA_BROWSER


def main():
    try:
        status, body, _ = fetch_text(
            "https://www.instagram.com/api/v1/users/web_profile_info/"
            "?username=diezellmx",
            headers={"X-IG-App-ID": "936619743392459"})
    except Exception as exc:
        log(f"  Instagram web_profile_info: error: {exc}")
        status = 0
    else:
        log(f"  Instagram web_profile_info: HTTP {status}")
        if status == 200 and "diezellmx" in body:
            log("  Instagram: perfil obtenido por web_profile_info")
            return True
    for url, label in (
            ("https://www.instagram.com/diezellmx/?__a=1", "?__a=1"),
            ("https://www.instagram.com/diezellmx/embed/", "embed")):
        try:
            status, html, _ = fetch_text(url)
        except Exception as exc:
            log(f"  Instagram {label}: error: {exc}")
            continue
        log(f"  Instagram {label}: HTTP {status}, {len(html)} bytes")
        if "edge_followed_by" in html or "followerCount" in html:
            log(f"  Instagram: datos del perfil en {label}")
            return True
    try:
        status, html, _ = fetch_text(
            "https://www.instagram.com/diezellmx/")
    except Exception as exc:
        log(f"  Instagram página: error: {exc}")
        return False
    if "edge_followed_by" in html:
        log("  Instagram: datos del perfil en el HTML")
        return True
    log(f"  Instagram página: HTTP {status}, {len(html)} bytes — "
        "muro de login, sin datos del perfil")
    return False
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fetch_text, log, run_main, UA_BROWSER


def main():
    try:
        status, body, _ = fetch_text(
            "https://www.instagram.com/api/v1/users/web_profile_info/"
            "?username=diezellmx",
            headers={"X-IG-App-ID": "936619743392459"})
    except Exception as exc:
        log(f"  Instagram web_profile_info: error: {exc}")
        status = 0
    else:
        log(f"  Instagram web_profile_info: HTTP {status}")
        if status == 200 and "diezellmx" in body:
            log("  Instagram: perfil obtenido por web_profile_info")
            return True
    try:
        status, html, _ = fetch_text(
            "https://www.instagram.com/diezellmx/")
    except Exception as exc:
        log(f"  Instagram página: error: {exc}")
        return False
    if "edge_followed_by" in html:
        log("  Instagram: datos del perfil en el HTML")
        return True
    log(f"  Instagram página: HTTP {status}, {len(html)} bytes — "
        "muro de login, sin datos del perfil")
    return False


if __name__ == "__main__":
    sys.exit(run_main("instagram_public", main))
