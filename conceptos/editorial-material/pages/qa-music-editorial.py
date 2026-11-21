#!/usr/bin/env python3
"""Regression checks for Diezell editorial rebuild source. Run from any cwd."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
music = (ROOT / "escuchar.html").read_text(encoding="utf-8")
restore = (ROOT / "restore-experience.py").read_text(encoding="utf-8")
dock = (ROOT / "dz-dock.js").read_text(encoding="utf-8")
pages = ("en-vivo.html", "banda.html", "caoticos.html", "crecimiento.html")
assert music.index('id="catalogo"') < music.index('id="discografia"'), "Catalog must appear before albums"
assert music.count('id="dz-lista"') == 1, "One catalog only"
assert music.count('id="dz-player"') == 1, "One contextual player only"
assert len(re.findall(r'<audio\b', music)) == 1, "Only one audio source"
assert 'open.spotify.com/embed/' not in music, "No Spotify iframe on music page"
assert 'data-embed-src' not in restore, "Restore must not recreate Spotify iframe"
assert "createElement('iframe')" not in dock, "Dock must not spawn Spotify iframe"
assert 'dz3-player-sheet' in restore and 'dock-ir' in restore, "Keep expanded dock"
assert 'dz3-sheet-spotify' in restore and 'dz3-sheet-youtube' in restore, "Keep external platforms"
# The audio engine is copied into the built site; check it in built-site QA.
for name in pages:
    html = (ROOT / name).read_text(encoding="utf-8")
    assert len(re.findall(r'<h1\b', html)) == 1, f"{name}: one H1 expected"
    assert 'href="escuchar.html"' in html, f"{name}: Music link missing"
print("PASS: catalog order, unique audio, dock, platforms, editorial pages")

# Expanded-player regression: previous control must work both with and without
# the inline Music player, and rewinding must clear the completion CTA.
assert "byId('dz-anterior')||previous" in dock, "Expanded previous needs inline/dock fallback"
assert "control.click()" in dock, "Expanded previous must delegate to app engine"
assert "audio.currentTime<MAX_SECONDS-.05" in dock, "Rewind should clear completion state"
