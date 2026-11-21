#!/usr/bin/env python3
"""Offline integrity checks for Diezell music metadata and player markup.
Usage: python3 tools/music-integrity.py site
Requires only Python 3.9+; site is the extracted deployment directory.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

def audit(root):
    errors, warnings = [], []
    playlist = root / "audio/playlist.json"
    if not playlist.is_file():
        return ["Missing audio/playlist.json"], warnings
    try:
        tracks = json.loads(playlist.read_text(encoding="utf-8")).get("canciones", [])
    except (ValueError, UnicodeError) as exc:
        return [f"Invalid playlist: {exc}"], warnings
    if len(tracks) != 27:
        errors.append(f"Expected 27 songs, got {len(tracks)}")
    seen = set()
    for i, track in enumerate(tracks, 1):
        label = f"Song {i} ({track.get('titulo', 'untitled')})"
        number = track.get("n")
        if number in seen:
            errors.append(f"{label}: repeated song number {number}")
        seen.add(number)
        if not track.get("titulo") or not track.get("album"):
            errors.append(f"{label}: title or album missing")
        for key in ("preview", "cover"):
            value = track.get(key)
            if not value:
                warnings.append(f"{label}: {key} missing")
            elif urlparse(value).scheme or value.startswith("/") or ".." in Path(value).parts:
                errors.append(f"{label}: unsafe {key} path {value}")
            elif not (root / value).is_file():
                warnings.append(f"{label}: {key} file missing in build: {value}")
        for key, host in (("spotify", "open.spotify.com"), ("youtube", "youtube.com")):
            value = track.get(key)
            if not value:
                warnings.append(f"{label}: {key} link missing")
                continue
            parsed = urlparse(value)
            if parsed.scheme != "https" or parsed.hostname not in (host, "www." + host):
                errors.append(f"{label}: invalid {key} destination: {value}")
            if key == "spotify" and parsed.path.startswith("/album/"):
                warnings.append(f"{label}: Spotify opens album, not specific song")
        if track.get("previewLimitSegundos", 90) > 90:
            errors.append(f"{label}: preview exceeds 90-second limit")
    music = root / "escuchar.html"
    if music.is_file():
        html = music.read_text(encoding="utf-8")
        audio_count = len(re.findall(r"<audio\\b", html, re.I))
        if audio_count > 1:
            errors.append(f"Music page has {audio_count} audio elements")
        if "open.spotify.com/embed/" in html:
            warnings.append("Embedded Spotify player may duplicate local player")
        if 'id="dz-lista"' in html and 'id="dz-player"' in html:
            warnings.append("Legacy player and secondary song list coexist; inspect UX")
    else:
        warnings.append("Music page missing from build")
    return errors, warnings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 tools/music-integrity.py <unpacked-site-dir>")
    failures, cautions = audit(Path(sys.argv[1]))
    for message in failures:
        print("ERROR:", message)
    for message in cautions:
        print("WARN:", message)
    print(f"Music audit: {len(failures)} errors; {len(cautions)} warnings")
    sys.exit(1 if failures else 0)
