#!/usr/bin/env python3
"""YouTube — datos por video con yt-dlp (sin clave, sin login).
Videos: los 3 oficiales conocidos + los 15 del RSS + todos los de
la lista de subidas del canal (/videos, 29 en total el 18 nov 2026).
Antes se parseaba el HTML con regex y los likes/duración solo
salían en 9/29. yt-dlp (2026.10.26, ya instalado) devuelve
duration, view_count y like_count completos por video.
Campos por video: título, vistas, likes, duración, fecha de estreno.
Comentarios: van en youtube_comments.py (endpoint youtubei, G5).
Espaciado de 2 s entre videos y cortocircuito tras 3 fallos
seguidos (límite de YouTube para esta IP).
"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_text, load_ledger, log, run_main,
                    save_snapshot)
import re

KNOWN_VIDEOS = [
    ("MuvgZpXqsY8", "El Cuento De Aquel Imperfecto Ser"),
    ("tIEk-WAnrLE", "Sin Rencores"),
    ("yUvkRgX-RC8", "El Monstruo de Gizmo"),
]


def _video_ids_from_rss():
    """Todos los ids del RSS (15), no solo los 5 primeros (G2)."""
    ids = []
    try:
        data = load_ledger()
        for r in data["records"]:
            if r["source"] == "YouTube RSS" and r["metric"] == "youtube_video_new":
                vid = (r.get("detail") or {}).get("video_id")
                if vid and vid not in ids:
                    ids.append(vid)
    except Exception:
        pass
    return ids


def _video_ids_from_uploads():
    """Todos los ids de la lista de subidas del canal.
    Se lee la playlist de subidas (UU + id del canal sin el prefijo
    UC): su HTML trae los 29 videos en una sola página, mientras
    que /videos solo muestra los primeros 17 (G2)."""
    try:
        status, html, _ = fetch_text(
            "https://www.youtube.com/playlist?list=UUwj0Exix_EnCMB7X5ncov1Q")
    except Exception as exc:
        log(f"  lista de subidas: error al descargar: {exc}")
        return []
    ids = []
    for m in re.finditer(r'"videoId":"([A-Za-z0-9_-]{11})"', html):
        if m.group(1) not in ids:
            ids.append(m.group(1))
    log(f"  lista de subidas: {len(ids)} ids")
    return ids


def get_all_video_ids():
    """Unión ordenada: conocidos + RSS + subidas. La usa también
    youtube_comments.py para no duplicar la lógica."""
    ids = []
    for vid, _ in KNOWN_VIDEOS:
        ids.append(vid)
    for vid in _video_ids_from_rss():
        if vid not in ids:
            ids.append(vid)
    for vid in _video_ids_from_uploads():
        if vid not in ids:
            ids.append(vid)
    return ids


def _ytdlp_json(vid):
    """Un video con yt-dlp. Devuelve el dict o None si falla."""
    url = f"https://www.youtube.com/watch?v={vid}"
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--dump-json",
             "--no-download", "--no-warnings", "--no-playlist", url],
            capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        log(f"  video {vid}: yt-dlp timeout")
        return None
    if proc.returncode != 0 or not proc.stdout.strip():
        err = (proc.stderr or "").strip().splitlines()
        log(f"  video {vid}: yt-dlp falló: {err[-1][:120] if err else 'sin salida'}")
        return None
    try:
        return json.loads(proc.stdout.strip().splitlines()[0])
    except Exception as exc:
        log(f"  video {vid}: yt-dlp JSON no parseable: {exc}")
        return None


def main():
    known = dict(KNOWN_VIDEOS)
    vids = [(v, known.get(v, "")) for v in get_all_video_ids()]
    seen_any = False
    fails = 0
    for vid, known_title in vids:
        data = _ytdlp_json(vid)
        time.sleep(2)
        if data is None:
            fails += 1
            if fails >= 3:
                log("  cortocircuito: 3 fallos seguidos, posible límite "
                    "de YouTube — se para aquí")
                break
            continue
        fails = 0
        title = known_title or data.get("title", vid)
        views = data.get("view_count")
        likes = data.get("like_count")
        duration = data.get("duration")
        if views is None and likes is None:
            log(f"  video {vid}: sin vistas ni likes")
            continue
        seen_any = True
        save_snapshot("youtube_video", f"{vid}.json",
                      json.dumps({"title": title, "views": views,
                                  "likes": likes, "duration": duration,
                                  "upload_date": data.get("upload_date")},
                                 ensure_ascii=False))
        url = f"https://www.youtube.com/watch?v={vid}"
        base = {"key": f"video:{vid}", "title": title, "video_id": vid}
        if views is not None:
            append_record("YouTube", "youtube_video_views", views,
                          "vistas", url=url, detail={**base})
        if likes is not None:
            append_record("YouTube", "youtube_video_likes", likes,
                          "likes", url=url, detail={**base})
        if duration is not None:
            append_record("YouTube", "youtube_video_duration_s",
                          duration, "segundos", url=url,
                          detail={**base}, once=True)
        up = data.get("upload_date")  # YYYYMMDD
        if up and len(up) == 8:
            iso = f"{up[:4]}-{up[4:6]}-{up[6:]}"
            append_record("YouTube", "youtube_video_published", 1,
                          "fecha de estreno", url=url,
                          detail={**base, "published": iso,
                                  "published_text": iso},
                          once=True)
        log(f"  video {vid}: views={views} likes={likes} "
            f"duration={duration}")
    if not seen_any:
        log("  ningún video devolvió datos")
        return False
    return True


if __name__ == "__main__":
    sys.exit(run_main("youtube_video", main))
