#!/usr/bin/env python3
"""iTunes Search API — sin clave (itunes.apple.com/search).
Campos: artista (id, nombre, género), álbumes (título, fecha, canciones,
precio, género, enlace), canciones (título, duración, nº de pista,
precio, fecha), podcasts que mencionan a Diezell (título, feed, enlace).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_json, log, run_main,
                    save_snapshot)

BASE = "https://itunes.apple.com/search"


def _es_diezell(artist_name):
    """True si el artista es Diezell (o una colaboración con Diezell).
    Excluye parecidos como 'MacDiezell' (otro artista)."""
    name = (artist_name or "").lower()
    if "macdiezell" in name:
        return False
    return "diezell" in name


def main():
    status, artist = fetch_json(
        f"{BASE}?term=Diezell&entity=musicArtist&limit=5")
    save_snapshot("itunes", "artist.json", artist)
    if artist.get("resultCount", 0) == 0:
        log("  iTunes: artista no encontrado")
        return False
    a = artist["results"][0]
    append_record("iTunes", "itunes_artist_id", a["artistId"], "id",
                  url=a.get("artistLinkUrl", ""),
                  detail={"key": "artista", "name": a.get("artistName"),
                          "genre": a.get("primaryGenreName")}, once=True)

    status, albums = fetch_json(
        f"{BASE}?term=Diezell&entity=album&limit=200")
    save_snapshot("itunes", "albums.json", albums)
    kept_albums = [al for al in albums.get("results", [])
                   if _es_diezell(al.get("artistName", ""))]
    append_record("iTunes", "itunes_albums", len(kept_albums),
                  "álbumes", url="https://music.apple.com/mx/artist/diezell/"
                  f"{a['artistId']}", detail={"key": "artista"})
    for al in kept_albums:
        append_record("iTunes", "itunes_album", 1, "álbum",
                      url=al.get("collectionViewUrl", ""),
                      detail={"key": f"álbum:{al.get('collectionId')}",
                              "title": al.get("collectionName"),
                              "release_date": al.get("releaseDate"),
                              "track_count": al.get("trackCount"),
                              "price": al.get("collectionPrice"),
                              "genre": al.get("primaryGenreName")},
                      once=True)

    status, songs = fetch_json(
        f"{BASE}?term=Diezell&entity=song&limit=200")
    save_snapshot("itunes", "songs.json", songs)
    kept_songs = [s for s in songs.get("results", [])
                  if _es_diezell(s.get("artistName", ""))]
    append_record("iTunes", "itunes_songs", len(kept_songs),
                  "canciones", detail={"key": "artista"})
    for s in kept_songs:
        append_record("iTunes", "itunes_song", 1, "canción",
                      url=s.get("trackViewUrl", ""),
                      detail={"key": f"canción:{s.get('trackId')}",
                              "title": s.get("trackName"),
                              "duration_ms": s.get("trackTimeMillis"),
                              "track_number": s.get("trackNumber"),
                              "disc_number": s.get("discNumber"),
                              "release_date": s.get("releaseDate"),
                              "price": s.get("trackPrice")}, once=True)

    status, pods = fetch_json(
        f"{BASE}?term=Diezell&entity=podcast&limit=20")
    save_snapshot("itunes", "podcasts.json", pods)
    # La búsqueda es difusa: "Diezell" también casa con "Diezel"
    # (otra persona). Solo valen podcasts con "Diezell" en el título
    # o en el autor.
    kept_pods = [p for p in pods.get("results", [])
                 if "diezell" in ((p.get("collectionName", "") + " " +
                                   p.get("artistName", "")).lower())]
    append_record("iTunes", "itunes_podcasts", len(kept_pods),
                  "podcasts", detail={"key": "búsqueda"})
    for p in kept_pods:
        append_record("iTunes", "itunes_podcast", 1, "podcast",
                      url=p.get("collectionViewUrl", ""),
                      detail={"key": f"podcast:{p.get('collectionId')}",
                              "title": p.get("collectionName"),
                              "artist": p.get("artistName"),
                              "feed_url": p.get("feedUrl"),
                              "genres": p.get("genres")}, once=True)
        if p.get("feedUrl"):
            log(f"  podcast con feed RSS directo: {p.get('feedUrl')}")
    log(f"  iTunes: álbumes={len(kept_albums)} "
        f"canciones={len(kept_songs)} "
        f"podcasts={len(kept_pods)} (filtrados: sin MacDiezell ni Diezel)")
    return True


if __name__ == "__main__":
    sys.exit(run_main("itunes", main))
