#!/usr/bin/env python3
"""Deezer — API pública sin clave (api.deezer.com).
Campos capturados: artista (id, nombre, fans, álbumes, enlace, imagen),
top tracks (rank, título, duración, enlace, preview, letra explícita),
álbumes (título, fecha, canciones, enlace, fans).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_json, log, run_main,
                    save_snapshot, today_cdmx)

ARTIST_ID = 134263372  # Diezell, verificado por búsqueda


def main():
    status, artist = fetch_json(
        f"https://api.deezer.com/artist/{ARTIST_ID}")
    if artist.get("error"):
        log(f"  Deezer devolvió error: {artist['error']}")
        return False
    if artist.get("name", "").lower() != "diezell":
        log(f"  el id {ARTIST_ID} ya no es Diezell: {artist.get('name')}")
        return False
    save_snapshot("deezer", "artist.json", artist)
    append_record("Deezer", "deezer_fans", artist["nb_fan"], "fans",
                  url=artist["link"], detail={"key": "deezer"})
    append_record("Deezer", "deezer_albums", artist["nb_album"], "álbumes",
                  url=artist["link"], detail={"key": "deezer"})
    append_record("Deezer", "deezer_artist_id", ARTIST_ID, "id",
                  url=artist["link"], detail={"key": "deezer"}, once=True)

    status, top = fetch_json(
        f"https://api.deezer.com/artist/{ARTIST_ID}/top?limit=5")
    save_snapshot("deezer", "top.json", top)
    for t in top.get("data", []):
        append_record("Deezer", "deezer_track_rank", t["rank"], "puesto",
                      url=t.get("link", ""),
                      detail={"key": f"canción:{t['title']}",
                              "title": t["title"],
                              "duration_s": t.get("duration"),
                              "explicit": t.get("explicit_lyrics")})
        append_record("Deezer", "deezer_track_duration_s",
                      t.get("duration"), "segundos", url=t.get("link", ""),
                      detail={"key": f"canción:{t['title']}",
                              "title": t["title"]}, once=True)

    status, albums = fetch_json(
        f"https://api.deezer.com/artist/{ARTIST_ID}/albums?limit=50")
    save_snapshot("deezer", "albums.json", albums)
    for a in albums.get("data", []):
        append_record("Deezer", "deezer_album", 1, "álbum",
                      url=a.get("link", ""),
                      detail={"key": f"álbum:{a['id']}",
                              "title": a.get("title"),
                              "release_date": a.get("release_date"),
                              "nb_tracks": a.get("nb_tracks"),
                              "fans": a.get("fans"),
                              "record_type": a.get("record_type")},
                      once=True)
    # G11: rank y duración de TODAS las canciones (27), no solo el
    # top 5: se recorre la lista de canciones de cada álbum.
    import time
    tracks_seen = 0
    for a in albums.get("data", []):
        try:
            _, tracks = fetch_json(
                f"https://api.deezer.com/album/{a['id']}/tracks?limit=50")
        except Exception as exc:
            log(f"  Deezer álbum {a['id']}: error al listar canciones: "
                f"{exc}")
            continue
        for t in tracks.get("data", []):
            tracks_seen += 1
            append_record("Deezer", "deezer_track_rank", t["rank"],
                          "puesto", url=t.get("link", ""),
                          detail={"key": f"canción:{t['title']}",
                                  "title": t["title"],
                                  "duration_s": t.get("duration"),
                                  "album": a.get("title"),
                                  "explicit": t.get("explicit_lyrics")})
            append_record("Deezer", "deezer_track_duration_s",
                          t.get("duration"), "segundos",
                          url=t.get("link", ""),
                          detail={"key": f"canción:{t['title']}",
                                  "title": t["title"]}, once=True)
        time.sleep(0.2)
    log(f"  Deezer: fans={artist['nb_fan']} álbumes={artist['nb_album']} "
        f"top={len(top.get('data', []))} álbumes_listados="
        f"{len(albums.get('data', []))} canciones_en_albumes="
        f"{tracks_seen}")
    return True


if __name__ == "__main__":
    sys.exit(run_main("deezer", main))
