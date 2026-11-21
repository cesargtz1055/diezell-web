#!/usr/bin/env python3
"""Songkick — página pública del artista (HTML, sin login).
Artista verificado: /artists/10309382-diezell.
Campos: fans que siguen los conciertos, próximos conciertos,
conciertos pasados (gigography: fecha, recinto, ciudad).
Cada concierto pasado queda además como UN registro propio en el
ledger (métrica songkick_event, once=True) con recinto, ciudad,
dirección y enlace — así el futuro mapa lee del ledger, no de la
página (G8).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (append_record, fetch_text, log, run_main,
                    save_snapshot)

ARTIST_URL = "https://www.songkick.com/artists/10309382-diezell"


def _parse_events(html):
    """Extrae los MusicEvent del JSON-LD de la página: nombre, fecha,
    recinto, ciudad, dirección y enlace del concierto."""
    events = []
    for m in re.finditer(
            r'"@type":"MusicEvent",(.*?)"startDate":"([^"]+)"',
            html, re.S):
        block, start = m.group(1), m.group(2)
        name = re.search(r'"name":"([^"]+)"', block)
        url = re.search(r'"url":"([^"]+)"', block)
        city = re.search(r'"addressLocality":"([^"]*)"', block)
        street = re.search(r'"streetAddress":"([^"]*)"', block)
        venue = re.search(
            r'"location":\{"@type":"Place".*?"name":"([^"]+)"',
            block, re.S)
        events.append({
            "name": name.group(1) if name else "",
            "startDate": start,
            "venue": venue.group(1) if venue else "",
            "city": city.group(1) if city else "",
            "address": street.group(1) if street else "",
            "url": url.group(1).replace("\\u0026", "&") if url else "",
        })
    return events


def main():
    status, html, _ = fetch_text(ARTIST_URL)
    if "Diezell" not in html:
        log(f"  Songkick: HTTP {status} — la página ya no es de Diezell")
        return False
    events = _parse_events(html)
    # fallback: solo nombres, sin ubicación
    if not events:
        for m in re.finditer(r'"name":"(Diezell[^"]*)"', html):
            events.append({"name": m.group(1), "startDate": "",
                           "venue": "", "city": "", "address": "",
                           "url": ""})
    save_snapshot("songkick_public", "artist.json",
                  {"events_found": len(events), "events": events[:50]})
    ok = False
    # Un registro propio por concierto (G8): el mapa futuro lee de aquí
    for e in events:
        date = (e["startDate"] or "")[:10]
        venue = e["venue"] or (e["name"].split("@")[-1].strip()
                               if "@" in e["name"] else e["name"])
        if append_record(
                "Songkick", "songkick_event", 1, "concierto",
                url=e["url"] or ARTIST_URL,
                detail={"key": f"evento:{date}:{venue}",
                        "venue": venue, "city": e["city"],
                        "date": date, "address": e["address"],
                        "name": e["name"], "startDate": e["startDate"]},
                date=date or None, once=True):
            log(f"  Songkick evento nuevo: {date} — {venue} "
                f"({e['city']})")
        ok = True
    m = re.search(r"([0-9,]+) fans get concert alerts", html)
    if m:
        append_record("Songkick", "songkick_tracked_fans",
                      int(m.group(1).replace(",", "")), "fans",
                      url=ARTIST_URL, detail={"key": "artista"})
        ok = True
    upcoming = 0 if "No upcoming concerts" in html else None
    if upcoming is not None:
        append_record("Songkick", "songkick_upcoming_events", upcoming,
                      "conciertos próximos", url=ARTIST_URL,
                      detail={"key": "artista"})
        ok = True
    if events:
        append_record("Songkick", "songkick_past_events", len(events),
                      "conciertos pasados (gigography)", url=ARTIST_URL,
                      detail={"key": "artista"})
        ok = True
    log(f"  Songkick: fans={m.group(1) if m else '?'} "
        f"próximos={upcoming} pasados_en_página={len(events)}")
    return ok


if __name__ == "__main__":
    sys.exit(run_main("songkick_public", main))
