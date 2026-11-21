#!/usr/bin/env python3
"""YouTube — comentarios por video vía endpoint youtubei (sin login).
La página del video NO incrusta comentarios; Invidious está tras
reto anti-bot y yt.lemnoslife.com no responde desde esta VM
(vacío, probado el 18 nov 2026). La vía que SÍ funciona:

1. POST /youtubei/v1/next {videoId} con cliente WEB → la sección
   de comentarios trae un token de continuación.
2. POST /youtubei/v1/next {continuation} → frameworkUpdates trae
   los comentarios en commentEntityPayload: autor (displayName),
   texto, fecha relativa, likes (likeCountLiked) y respuestas.
Solo primera página (20 comentarios por video).

La clave es la clave pública del cliente web de YouTube (la misma
que usa yt-dlp en su código público): no es una clave personal,
no requiere login ni cuenta.

Nota (18 nov 2026): el endpoint funciona, pero YouTube puede
limitar la IP compartida tras una ráfaga de peticiones (en la
primera corrida por systemd todos los POST dieron timeout de 30 s;
minutos después, con el mismo entorno, volvían en 1 s). Por eso
el colector tiene cortocircuito: 3 errores seguidos y se aborta,
y si ningún video dio comentarios por error, devuelve FAIL (no
"empty") para que el fallo se vea en el log del día.
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_comment, append_record, fetch_post_json, log,
                    parse_compact_number, run_main, save_snapshot)
from youtube_video import KNOWN_VIDEOS, get_all_video_ids

YT_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
NEXT_URL = "https://www.youtube.com/youtubei/v1/next?key=" + YT_KEY
CLIENT = {"clientName": "WEB", "clientVersion": "2.20240111.09.00"}


def _find_comments_token(data):
    """Token de continuación de la sección de comentarios."""
    def walk(o):
        if isinstance(o, dict):
            if "itemSectionRenderer" in o:
                if "commentsHeaderRenderer" in json.dumps(o):
                    for c in o["itemSectionRenderer"].get("contents", []):
                        ci = c.get("continuationItemRenderer", {})
                        tok = (ci.get("continuationEndpoint", {})
                                 .get("continuationCommand", {})
                                 .get("token"))
                        if tok:
                            return tok
            for v in o.values():
                r = walk(v)
                if r:
                    return r
        elif isinstance(o, list):
            for v in o:
                r = walk(v)
                if r:
                    return r
        return None
    return walk(data)


def _parse_comments(data):
    """Extrae comentarios de frameworkUpdates.entityBatchUpdate."""
    muts = (data.get("frameworkUpdates", {})
                .get("entityBatchUpdate", {}).get("mutations", []))
    out = []
    for m in muts:
        p = (m.get("payload") or {}).get("commentEntityPayload")
        if not p:
            continue
        props = p.get("properties", {})
        cid = props.get("commentId", "")
        content = (props.get("content") or {}).get("content", "")
        if not cid or not content:
            continue
        blob = json.dumps(p, ensure_ascii=False)
        am = re.search(r'"displayName":\s*"([^"]+)"', blob)
        author = am.group(1) if am else ""
        lm = re.search(r'"likeCountLiked":\s*"([^"]+)"', blob)
        likes = parse_compact_number(lm.group(1))[0] if lm else None
        if author:
            out.append({
                "id": cid, "author": author, "text": content,
                "likes": likes,
                "published": props.get("publishedTime", ""),
                "reply_level": props.get("replyLevel", 0),
            })
    return out


def main():
    vids = get_all_video_ids()
    log(f"  youtube_comments: {len(vids)} videos a revisar")
    total_new = 0
    videos_ok = 0
    videos_error = 0
    errores_seguidos = 0
    for vid in vids:
        url = f"https://www.youtube.com/watch?v={vid}"
        try:
            _, first = fetch_post_json(
                NEXT_URL, {"context": {"client": CLIENT}, "videoId": vid})
            token = _find_comments_token(first)
            if not token:
                log(f"  video {vid}: sin token de comentarios")
                errores_seguidos = 0
                continue
            _, cont = fetch_post_json(
                NEXT_URL,
                {"context": {"client": CLIENT}, "continuation": token})
        except Exception as exc:
            videos_error += 1
            errores_seguidos += 1
            log(f"  video {vid}: error youtubei: {exc}")
            # Cortocircuito: 3 errores seguidos = YouTube está
            # limitando la IP (cada intento tarda 30 s). No tiene
            # sentido quemar 15 min en 29 videos; se reintenta
            # mañana. Los comentarios ya guardados no se pierden.
            if errores_seguidos >= 3:
                log("  youtube_comments: ABORTADO tras 3 errores "
                    "seguidos (posible límite de YouTube)")
                break
            time.sleep(2)
            continue
        errores_seguidos = 0
        comments = _parse_comments(cont)
        if comments:
            videos_ok += 1
        save_snapshot("youtube_comments", f"{vid}.json", comments)
        new = 0
        for c in comments:
            if append_comment("YouTube", vid, url, c["author"], c["text"],
                              likes=c["likes"], published=c["published"],
                              author_url=""):
                new += 1
        total_new += new
        append_record("YouTube", "youtube_video_comments_saved", new,
                      "comentarios nuevos guardados", url=url,
                      detail={"key": f"video:{vid}",
                              "video_id": vid,
                              "comentarios_en_pagina": len(comments)})
        log(f"  video {vid}: {len(comments)} comentarios en página, "
            f"{new} nuevos")
        time.sleep(1)
    log(f"  youtube_comments: {total_new} comentarios nuevos en "
        f"{videos_ok} videos ({videos_error} errores)")
    if videos_ok == 0 and videos_error > 0:
        # Fallo sistemático de descarga, no "sin comentarios":
        # que el log lo marque FAIL y se vea mañana.
        return False
    if videos_ok == 0:
        return "empty"
    return True


if __name__ == "__main__":
    sys.exit(run_main("youtube_comments", main))
