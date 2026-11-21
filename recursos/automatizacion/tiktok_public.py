#!/usr/bin/env python3
"""TikTok — página pública del perfil @diezellmx (HTML + JSON embebido).
Campos del perfil: seguidores, seguidos, videos, total de likes (heart),
digg, amigos, verificado, apodo, bio.
Videos individuales: la página NO los incrusta (itemList vacío en el
JSON __UNIVERSAL_DATA_FOR_REHYDRATION__; verificado 18 nov 2026) y
el endpoint interno /api/post/item_list/ devuelve 0 bytes sin
sesión (msToken). Sin vía gratuita sin login para métricas por video.
Historias: la página no expone historia activa sin login.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_text, log, run_main,
                    save_snapshot)

PROFILE_URL = "https://www.tiktok.com/@diezellmx"


def main():
    status, html, _ = fetch_text(PROFILE_URL)
    m = re.search(
        r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" '
        r'type="application/json">(.*?)</script>', html, re.S)
    if not m:
        log("  no se encontró el JSON embebido del perfil")
        return False
    data = json.loads(m.group(1))
    info = (data.get("__DEFAULT_SCOPE__", {})
            .get("webapp.user-detail", {}).get("userInfo", {}))
    if not info:
        log("  el JSON no trae userInfo")
        return False
    user = info.get("user", {})
    # statsV2 trae las cifras EXACTAS (ej. 13752); stats trae la
    # cifra redondeada que muestra la página (13800). Se prefiere la
    # exacta y se anota la fuente del número en el detalle.
    stats = info.get("statsV2") or info.get("stats", {})
    exact = bool(info.get("statsV2"))
    if user.get("uniqueId", "").lower() != "diezellmx":
        log(f"  el perfil no es diezellmx: {user.get('uniqueId')}")
        return False
    save_snapshot("tiktok_public", "profile.json",
                  {"user": user, "stats": stats,
                   "itemList_count": len(info.get("itemList", []))})
    fields = [
        ("followerCount", "tiktok_followers", "seguidores"),
        ("followingCount", "tiktok_following", "seguidos"),
        ("videoCount", "tiktok_videos_total", "videos"),
        ("heartCount", "tiktok_total_likes", "likes totales"),
        ("heart", "tiktok_heart", "corazones"),
        ("diggCount", "tiktok_digg", "diggs"),
        ("friendCount", "tiktok_friends", "amigos"),
    ]
    for field, metric, unit in fields:
        if field in stats:
            append_record("TikTok", metric, int(stats[field]), unit,
                          url=PROFILE_URL,
                          detail={"key": "perfil",
                                  "exacto_statsV2": exact})
    append_record("TikTok", "tiktok_verified", 1 if user.get("verified")
                  else 0, "verificado (1=sí)", url=PROFILE_URL,
                  detail={"key": "perfil",
                          "nickname": user.get("nickname"),
                          "signature": user.get("signature")}, once=True)
    log(f"  TikTok perfil: seguidores={stats.get('followerCount')} "
        f"videos={stats.get('videoCount')} likes={stats.get('heartCount')} "
        f"itemList={len(info.get('itemList', []))} (sin videos incrustados)")
    return True


if __name__ == "__main__":
    sys.exit(run_main("tiktok_public", main))
