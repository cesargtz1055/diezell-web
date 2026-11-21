#!/usr/bin/env python3
"""Utilidades compartidas de los colectores de Diezell.

Reglas: sin claves, sin logins, sin servicios de pago, sin IA.
El ledger es append-only: nunca se borra ni se modifica un registro.
Un re-corte el mismo día con la misma métrica y clave se salta
(primer corte del día gana). Un fetch fallido no escribe nada.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER_DIR = os.path.join(BASE, "datos", "ledger")
LEDGER_PATH = os.path.join(LEDGER_DIR, "ledger.json")
SNAP_DIR = os.path.join(LEDGER_DIR, "snapshots")
RUNS_DIR = os.path.join(LEDGER_DIR, "runs")
MENTIONS_PATH = os.path.join(LEDGER_DIR, "mentions.json")
COMMENTERS_PATH = os.path.join(LEDGER_DIR, "commenters.json")
COMMENTS_PATH = os.path.join(LEDGER_DIR, "comments.json")
TZ = ZoneInfo("America/Mexico_City")

UA_BROWSER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
UA_BOT = ("DiezellFanArchive/1.0 (archivo no oficial de fans; "
          "contacto: cesar@pulsoscreativos.com)")


def today_cdmx():
    return datetime.now(TZ).strftime("%Y-%m-%d")


def now_iso():
    return datetime.now(TZ).isoformat(timespec="seconds")


def log(msg):
    print(f"[{now_iso()}] {msg}", flush=True)


# ---------------------------------------------------------------- ledger
def load_ledger():
    with open(LEDGER_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_ledger(data):
    data["updated"] = now_iso()
    tmp = LEDGER_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, LEDGER_PATH)


def _dedup_key(rec):
    detail = rec.get("detail") or {}
    key = detail.get("key", "") if isinstance(detail, dict) else ""
    return (rec["date"], rec["source"], rec["metric"], str(key))


def append_record(source, metric, value, unit="", url="", detail=None,
                   date=None, once=False):
    """Añade un registro si no existe ya ese corte. Devuelve True si se añadió.
    once=True: hechos estáticos (duración, fecha de lanzamiento): se guardan
    una sola vez en toda la historia, nunca se re-cortan."""
    data = load_ledger()
    rec = {
        "date": date or today_cdmx(),
        "source": source,
        "metric": metric,
        "value": value,
        "unit": unit,
        "url": url,
        "detail": detail or {},
        "recorded_at": now_iso(),
    }
    seen = {_dedup_key(r) for r in data["records"]}
    if once:
        seen_any = {(r["source"], r["metric"], str((r.get("detail") or {}).get("key", "")))
                    for r in data["records"]}
        if (rec["source"], rec["metric"],
                str((detail or {}).get("key", ""))) in seen_any:
            return False
    if _dedup_key(rec) in seen:
        log(f"  salto (ya existe corte de hoy): {source} / {metric} / "
            f"{(detail or {}).get('key', '')}")
        return False
    data["records"].append(rec)
    save_ledger(data)
    log(f"  + {rec['date']} {source} | {metric} = {value} {unit}")
    return True


# ---------------------------------------------------------------- comentarios
def append_comment(source, post_id, post_url, author, text, likes=None,
                   published="", author_url=""):
    """Un comentario = un registro en comments.json (nunca dentro de un blob).
    Dedup por (fuente, publicación, autor, texto)."""
    if os.path.exists(COMMENTS_PATH):
        data = load_json_file(COMMENTS_PATH)
    else:
        data = {"version": 1, "comments": []}
    for c in data["comments"]:
        if (c.get("source") == source and c.get("post_id") == post_id
                and c.get("author") == author and c.get("text") == text):
            return False
    data["comments"].append({
        "date": today_cdmx(), "source": source, "post_id": post_id,
        "post_url": post_url, "author": author, "author_url": author_url,
        "text": text, "likes": likes, "published": published,
        "recorded_at": now_iso(),
    })
    tmp = COMMENTS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, COMMENTS_PATH)
    return True


# ---------------------------------------------------------------- snapshots
def save_snapshot(source, filename, content):
    """Guarda la respuesta cruda (o un extracto) del día. content: str o dict."""
    date = today_cdmx()
    d = os.path.join(SNAP_DIR, date)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{source}_{filename}")
    if isinstance(content, (dict, list)):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return path


def load_json_file(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_snapshot_once(source, filename, content):
    """Como save_snapshot, pero guarda solo el primer archivo del día:
    si ya existe, no lo sobrescribe (G10: el XML de noticias no debe
    pisarse en cada corrida del mismo día). Devuelve la ruta o None."""
    date = today_cdmx()
    d = os.path.join(SNAP_DIR, date)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"{source}_{filename}")
    if os.path.exists(path):
        return None
    if isinstance(content, (dict, list)):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return path


# ---------------------------------------------------------------- menciones
def normalize_url(url):
    """Normaliza una URL para dedup: desempaqueta los redirects de Bing
    (apiclick.aspx?url=DESTINO), quita query y fragmento. Dos fetches
    del mismo destino con parámetros de tracking distintos deben
    considerarse el mismo enlace (G3: el mismo JamBase se guardó dos
    veces porque el tid de Bing cambiaba)."""
    url = (url or "").strip()
    try:
        parsed = urllib.parse.urlparse(url)
        if "bing.com" in parsed.netloc and "apiclick.aspx" in parsed.path:
            qs = urllib.parse.parse_qs(parsed.query)
            dest = qs.get("url", [None])[0]
            if dest:
                url = urllib.parse.unquote(dest)
                parsed = urllib.parse.urlparse(url)
        clean = urllib.parse.urlunparse(
            (parsed.scheme, parsed.netloc,
             parsed.path.rstrip("/") or "/", "", "", ""))
        return clean
    except Exception:
        return url


def add_mention(source, kind, title, url, date=None):
    """Mención fechada, sin duplicar por URL normalizada ni por
    (fuente, título, fecha). Devuelve True si es nueva."""
    date = date or today_cdmx()
    if os.path.exists(MENTIONS_PATH):
        mentions = load_json_file(MENTIONS_PATH)
    else:
        mentions = {"version": 1, "mentions": []}
    norm = normalize_url(url)
    for m in mentions["mentions"]:
        if normalize_url(m.get("url", "")) == norm:
            return False
        if (m.get("source") == source
                and (m.get("title") or "").strip().lower()
                == (title or "").strip().lower()
                and m.get("date") == date):
            return False
    mentions["mentions"].append({
        "date": date, "source": source, "kind": kind,
        "title": title, "url": url, "seen_first": now_iso(),
    })
    tmp = MENTIONS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(mentions, f, ensure_ascii=False, indent=2)
    os.replace(tmp, MENTIONS_PATH)
    return True


# ---------------------------------------------------------------- fetch
# Transporte: curl (subprocess), NO urllib.
# Motivo verificado 2026-11-18: bajo systemd, Python-urllib se queda
# colgado esperando la respuesta al CONNECT del proxy de salida
# (el proxy nunca responde; curl, en el mismo contexto y con las
# mismas cabeceras, devuelve 200 en <1 s). curl honra solo las
# variables de entorno del proxy, igual que urllib, así que el
# comportamiento es el mismo en el shell y bajo systemd.
import subprocess
import tempfile


class FetchError(Exception):
    def __init__(self, status, url, msg=""):
        super().__init__(f"HTTP {status} {url} {msg}")
        self.status = status
        self.url = url


def fetch(url, ua=UA_BROWSER, timeout=25, headers=None):
    """GET simple vía curl. Devuelve (status, bytes, url_final).
    Lanza FetchError en HTTP >= 400 o en error de red/timeout."""
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    try:
        cmd = ["curl", "-sS", "-L", "--max-time", str(timeout),
               "-A", ua,
               "-H", "Accept: text/html,application/json,application/xml,"
                     "*/*;q=0.8",
               "-H", "Accept-Language: es-MX,es;q=0.9,en;q=0.8",
               "-o", tmp.name,
               "-w", "%{http_code}\n%{url_effective}"]
        for k, v in (headers or {}).items():
            cmd += ["-H", f"{k}: {v}"]
        cmd.append(url)
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout + 10)
        with open(tmp.name, "rb") as f:
            body = f.read()
        out = proc.stdout.strip().splitlines()
        if len(out) < 2:
            raise FetchError(0, url,
                             f"curl salió {proc.returncode}: "
                             f"{proc.stderr.strip()[:200]}")
        status = int(out[0])
        final = out[1]
        if status >= 400:
            raise FetchError(status, url)
        return status, body, final
    except subprocess.TimeoutExpired:
        raise FetchError(0, url, "timeout")
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


def fetch_json(url, ua=UA_BROWSER, timeout=25):
    status, body, _ = fetch(url, ua=ua, timeout=timeout)
    return status, json.loads(body.decode("utf-8", "replace"))


def fetch_post_json(url, payload, ua=UA_BROWSER, timeout=30):
    """POST con cuerpo JSON vía curl. Devuelve (status, dict).
    Lanza FetchError en HTTP >= 400 o error de red/timeout.
    Se usa para el endpoint youtubei de YouTube (G5): la clave es la
    clave pública del cliente web de YouTube (la misma que usa yt-dlp),
    no es una clave personal ni requiere login."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    tmp.close()
    try:
        cmd = ["curl", "-sS", "-L", "--max-time", str(timeout),
               "-A", ua,
               "-H", "Content-Type: application/json",
               "-H", "Accept: application/json",
               "--data-binary", json.dumps(payload),
               "-o", tmp.name,
               "-w", "%{http_code}"]
        cmd.append(url)
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout + 10)
        with open(tmp.name, "rb") as f:
            body = f.read()
        out = proc.stdout.strip().splitlines()
        if not out:
            raise FetchError(0, url,
                             f"curl salió {proc.returncode}: "
                             f"{proc.stderr.strip()[:200]}")
        status = int(out[0])
        if status >= 400:
            raise FetchError(status, url)
        return status, json.loads(body.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        raise FetchError(0, url, "timeout")
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


def fetch_text(url, ua=UA_BROWSER, timeout=25, headers=None):
    status, body, final = fetch(url, ua=ua, timeout=timeout,
                                headers=headers)
    return status, body.decode("utf-8", "replace"), final


def parse_rss_items(xml_text):
    """Devuelve [{title, link, pubDate}] de un RSS 2.0 o Atom."""
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items
    ns = {"atom": "http://www.w3.org/2005/Atom",
          "media": "http://search.yahoo.com/mrss/"}
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        pub = (it.findtext("pubDate") or "").strip()
        if title and link:
            items.append({"title": title, "link": link, "pubDate": pub})
    for e in root.iter("{http://www.w3.org/2005/Atom}entry"):
        title = (e.findtext("atom:title", namespaces=ns) or "").strip()
        link_el = e.find("atom:link", namespaces=ns)
        link = link_el.get("href", "") if link_el is not None else ""
        pub = (e.findtext("atom:published", namespaces=ns) or "").strip()
        if title and link:
            items.append({"title": title, "link": link, "pubDate": pub})
    return items


def parse_compact_number(text):
    """'12.2K' -> (12200, True) ; '1,678,233' -> (1678233, False).
    Devuelve (valor, es_aproximado) o (None, False)."""
    if text is None:
        return None, False
    s = str(text).strip().replace(",", "").replace("\xa0", "")
    m = re.match(r"^([0-9]+(?:\.[0-9]+)?)\s*([KMB])$", s, re.I)
    if m:
        mult = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[m.group(2).upper()]
        return int(float(m.group(1)) * mult), True
    m = re.match(r"^[0-9]+(\.[0-9]+)?$", s)
    if m:
        return int(float(s)), False
    m = re.search(r"([0-9][0-9,]*)", s)
    if m:
        return int(m.group(1).replace(",", "")), True
    return None, False


def run_main(name, fn):
    """Envoltorio estándar: nunca revienta el runner; imprime OK/FAIL.
    Semántica (G14): un colector devuelve True = datos guardados;
    "empty" = la comprobación funcionó pero el hallazgo es negativo
    (ej. MusicBrainz count 0, artículo de Wikipedia inexistente,
    0 menciones en prensa) — eso es OK, no FAIL; FAIL se reserva
    para errores de descarga o de parseo."""
    try:
        ok = fn()
    except Exception as exc:  # noqa: BLE001 - el runner debe seguir
        log(f"FAIL {name}: {type(exc).__name__}: {exc}")
        return 1
    if ok == "empty":
        log(f"OK {name} (verificación OK, sin hallazgos)")
        return 0
    if ok is False:
        log(f"FAIL {name}: sin datos utilizables (ver log)")
        return 1
    log(f"OK {name}")
    return 0
