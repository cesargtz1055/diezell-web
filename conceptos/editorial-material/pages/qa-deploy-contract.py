#!/usr/bin/env python3
"""Diezell: verify a built GitHub Pages tree before publishing.

Usage: python3 qa-deploy-contract.py /path/to/site
Read-only, standard-library only. No network, credentials or fan accounts.
"""
from pathlib import Path
import argparse
import re
import sys

def check(root: Path) -> list[str]:
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    root = root.resolve()
    for rel in ("index.html", "escuchar.html", "audio/playlist.json",
                "nuevo/index.html", "nuevo/escuchar.html", "anterior/index.html"):
        require((root / rel).is_file(), f"Missing: {rel}")
    if not (root / "index.html").exists():
        return errors
    # The public root and /nuevo/ must be byte-identical for core pages.
    for rel in ("index.html", "escuchar.html", "banda.html", "en-vivo.html",
                "caoticos.html", "crecimiento.html"):
        current, preview = root / rel, root / "nuevo" / rel
        if current.is_file() and preview.is_file():
            require(current.read_bytes() == preview.read_bytes(),
                    f"Root differs from /nuevo/: {rel}")
        else:
            require(False, f"Missing main section: {rel}")
    pages = sorted((root / "canciones").glob("*.html"))
    require(len(pages) == 27, f"Expected 27 song detail pages, found {len(pages)}")
    for page in [root / "escuchar.html", *pages]:
        if not page.is_file():
            continue
        html = page.read_text(encoding="utf-8")
        require(len(re.findall(r'<audio\b', html)) == 1,
                f"{page.relative_to(root)}: expected exactly one audio engine")
        require("open.spotify.com/embed/" not in html,
                f"{page.relative_to(root)}: embedded Spotify duplicates audio")
        require('id="dz3-player-sheet"' in html,
                f"{page.relative_to(root)}: missing expanded player")
        require('id="dz3-sheet-spotify"' in html and
                'id="dz3-sheet-youtube"' in html,
                f"{page.relative_to(root)}: missing platform links")
    # Every song page must also survive under /nuevo/, not only at the root.
    for page in pages:
        counterpart = root / "nuevo" / "canciones" / page.name
        require(counterpart.is_file(), f"Missing /nuevo/ song page: {page.name}")
        if counterpart.is_file():
            require(page.read_bytes() == counterpart.read_bytes(),
                    f"Song page differs from /nuevo/: {page.name}")
    app = root / "app.js"
    if app.is_file():
        require("PREVIEW_LIMIT_SECONDS = 90" in app.read_text(encoding="utf-8"),
                "Audio preview limit must remain 90 seconds")
    else:
        errors.append("Missing app.js")
    for rel in ("datos/ledger/ledger.json", "audio/playlist.json"):
        require((root / rel).is_file(), f"Missing source data: {rel}")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path, help="Built Pages directory")
    args = parser.parse_args()
    errors = check(args.site)
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    print("PASS: unified root, backup, 27 song pages, single audio, data and 90 s limit")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
