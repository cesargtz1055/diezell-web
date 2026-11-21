# Diezell — Archivo automático (pura automatización)

**$0. Sin claves. Sin cuentas. Sin logins. Sin IA en producción.**
Solo código determinista + un timer de systemd.

## Qué es

Un libro de contabilidad de Diezell: cada día un corte guarda los números
de la banda (seguidores, oyentes, videos, noticias, conciertos…) con su
**fecha de corte y su fuente**. Nunca se borra ni se reemplaza nada:
un dato nuevo es una fila nueva. Las gráficas de `crecimiento.html`
se dibujan desde ese archivo.

## Cómo funciona

```
colectores (Python, stdlib) → datos/ledger/ledger.json
                          → datos/ledger/snapshots/<fecha>/<fuente>.*
                          → datos/ledger/mentions.json
                          → datos/ledger/comments.json (1 registro por comentario)
                          → datos/ledger/commenters.json (ranking por mes)
                          → datos/ledger/runs/<fecha-hora>.log
run_daily.sh              → ejecuta todos los colectores, 1 vez al día
systemd timer             → diezell-ledger.timer, diario 08:00 America/Mexico_City
crecimiento.html          → lee ledger.json con JS puro y dibuja las gráficas (SVG hecho a mano)
```

## Archivos

| Archivo | Qué es |
|---|---|
| `datos/ledger/ledger.json` | El libro: un registro por corte, fuente y métrica |
| `datos/ledger/mentions.json` | Menciones (noticias, artículos, posts) con fecha y URL |
| `datos/ledger/comments.json` | Un registro por comentario guardado (autor, texto, fecha) |
| `datos/ledger/commenters.json` | Ranking mensual de quién más comenta |
| `datos/ledger/snapshots/<fecha>/` | Respuestas crudas de cada corte (auditoría) |
| `datos/ledger/runs/<fecha-hora>.log` | Log de cada corte: qué funcionó y qué falló |
| `automatizacion/*.py` | Un colector por fuente |
| `automatizacion/run_daily.sh` | Corre todos los colectores en orden |
| `automatizacion/systemd/` | Copias de las unidades systemd (fuente de verdad) |
| `archivo/stories/YYYY-MM-DD/` | Historias rescatadas (si alguna vez se puede) |

## Esquema del ledger

```json
{
  "date": "2026-11-18",
  "source": "Deezer",
  "metric": "deezer_fans",
  "value": 884,
  "unit": "fans",
  "url": "https://www.deezer.com/artist/134263372",
  "detail": {"key": "deezer"},
  "recorded_at": "2026-11-18T00:36:08-06:00"
}
```

- `date`: fecha del corte (America/Mexico_City).
- `source`: quién dice el número. Las cifras de fuentes distintas
  nunca se mezclan ni se reconcilian.
- `metric`: una métrica = un registro. Nada queda escondido en un blob.
- `detail.key`: distingue registros de la misma métrica
  (ciudad, canción, video, álbum…).
- Hechos estáticos (duración de una canción, fecha de estreno) se
  guardan **una sola vez** (`once=True`); lo demás se corta cada día.
- Un re-corte el mismo día con la misma métrica y clave se salta
  (primer corte del día gana). Un fetch fallido **no escribe nada**.

## Fuentes y estado (primer corte: 18 nov 2026)

### Funcionan — datos reales en el ledger

| Fuente | Método | Qué se captura (todo, por campo) |
|---|---|---|
| Deezer | API pública, sin clave | fans, álbumes (13), rank + duración de TODAS las canciones (32 registros de álbum, 27+ canciones), 13 álbumes (título, fecha, canciones, fans, tipo) |
| YouTube RSS | Feed público del canal UCwj0Exix_EnCMB7X5ncov1Q | 15 videos (id, título, fecha, enlace); videos nuevos por corte |
| YouTube (página del canal) | HTML público | suscriptores (texto aprox. "12.2 mil"), total de videos (29) |
| YouTube (páginas de video) | HTML público, 29 videos | vistas, likes (cuando la página los trae), duración, fecha de estreno por video |
| YouTube (comentarios) | Endpoint youtubei, sin login | 372 comentarios guardados (autor, texto, fecha relativa, likes) en 27 videos; top comentaristas en commenters.json |
| TikTok (perfil) | HTML + JSON embebido | seguidores 13,752 (exacto, statsV2), seguidos, videos 75, likes totales 129,074, heart, digg, amigos, verificado |
| Songkick | Página del artista /artists/10309382-diezell | 764 fans, 0 próximos, 3 pasados + 1 registro por concierto (recinto, ciudad, dirección, fecha) |
| Music Metrics Vault | Página pública del artista | oyentes mensuales de Spotify, seguidores, streams totales — con la fecha del dato de la página ("Last updated") |
| Last.fm | Página pública del artista | oyentes del encabezado (15), oyentes por álbum (INSANIA 1,352; 776; 482; 411). Scrobbles: **64,736** (18 nov, verificado). Total de oyentes del artista: **2,169** (nueva métrica `lastfm_listeners_total`). Nota: el "15" histórico es la cifra semanal de la canción popular, no el total del artista. La página alterna con un reto anti-bot de 3 KB; el colector falla como debe en ese caso. |
| Google News RSS | RSS sin clave | 5 + 2 noticias por búsqueda ("Diezell", "Diezell banda Monterrey") |
| Bing News RSS | RSS sin clave | 1 noticia |
| Prensa RSS | Feeds de Puro Rock Puro, Follow Control, Punkeando | artículos que mencionan a Diezell (0 el 18 nov; Mr Indie falló por conexión) |
| iTunes Search | API sin clave | artista, 13 álbumes (filtrados), 33 canciones (filtradas), 0 podcasts de la banda |
| MusicBrainz | API sin clave | comprobación: artista NO existe (count 0) |
| Wikipedia | API sin clave | comprobación: el artículo NO existe (404) |
| Wayback Machine | CDX API sin clave | inventario: Spotify 3 capturas, Viberate 4, YouTube/Instagram/MMV 0 |
| Charts | Deezer chart + iTunes MX RSS | comprobación: Diezell no está en Deezer top 10 ni iTunes MX top 25 |

### No funcionan (huecos honestos, se reintentan a diario)

| Fuente | Razón exacta |
|---|---|
| Spotify oyentes mensuales | ✅ RESUELTO 18 nov: Music Metrics Vault, URL exacta con slug + id de Spotify. La fecha del registro es la fecha del dato en la página ("Last updated"), no la del corte. |
| Instagram (seguidores, posts, historias) | web_profile_info 429; la página HTML es muro de login; ?__a=1 da 302 a login; /embed/ da 200 pero es cáscara JS sin datos. Sin login no hay vía gratuita. |
| Facebook | 302/400 al muro de login en /diezelloficial y /diezellmx. |
| Reddit | .json devuelve 403 Blocked o HTML en los 3 endpoints (www, api, old). pullpush.io: todas las rutas de búsqueda dan 404 y su documentación está tras Cloudflare. |
| setlist.fm | búsqueda HTTP 202 con cuerpo vacío (anti-bot); Bing/DuckDuckGo no devuelven la página del artista; adivinar el slug redirige a otro artista. |
| Bandsintown | HTTP 403. |
| SoundCloud | soundcloud.com/diezell es OTRO usuario (Alycyalyna); diezellmx y diezell-oficial dan 404. Perfil de la banda no localizado. El registro semilla de 13 seguidores (15 nov) lleva una nota de duda en el detalle. |
| Google Trends | CERRADO como no viable (G16): explore 429 sin cookies; el RSS es genérico. Ya no está en run_daily.sh. |
| Wayback snapshots | CDX funciona; la descarga da 429 incluso con esperas de 45-60 s (la IP de salida está limitada). Se reintenta a diario. |
| TikTok por video | La página del perfil no incrusta videos (itemList vacío) y /api/post/item_list/ devuelve 0 bytes sin sesión. |
| TikTok hashtags | Las páginas #Diezell, #Caoticos, #INSANIA cargan pero no exponen conteos ni videos parseables. |
| Top comentaristas | ✅ FUNCIONA desde el 18 nov: 314 autores en nov 2026 (top: @jesuscruz4855, @blakeivan9676, @KxrasuLoL, 4 comentarios cada uno). |
| Historias | Instagram exige login; TikTok no muestra historia activa en la página pública. Si algún día aparece una, se descarga el archivo a `archivo/stories/YYYY-MM-DD/`. |
| Last.fm scrobbles | El número del encabezado no se pudo extraer con el patrón actual. |
| Wikipedia | Artículo borrado el 17 jul 2026 (promocional/COI). El enlace se quitó de crecimiento.html. Se comprueba a diario por si se recrea. |

### Discrepancias conocidas (no se corrigen, se anotan)

- TikTok: 11.3K (Viberate, 15 nov) vs 13.7K (8 nov, en `diezell.ts`) vs 13,800 (página pública de TikTok, 18 nov, cifra redondeada) vs **13,752** (statsV2 exacto, 18 nov). **A vigilar**: el salto de 11.3K a 13.8K en 3 días es sospechoso — puede ser un dato desactualizado de Viberate (15 nov) o un crecimiento real; el ledger lo mostrará con los próximos cortes. Cada cifra lleva su fuente y su fecha.
- Streams totales: Viberate 9.7M vs Music Metrics Vault 5.5M.
- Cifras del 8 nov en `datos.json` (ranks 3–5 de canciones) vs cifras del 15 nov: se conservan tal cual, con su fecha.
- YouTube suscriptores: "12.2 mil" es texto aproximado del canal, no cifra exacta.
- Last.fm "15 oyentes" es la cifra del encabezado del artista, distinta de los oyentes por álbum (1,352 en INSANIA): Last.fm mide ventanas distintas; se guardan las dos, etiquetadas.

## Correcciones del primer corte (2026-11-18)

Registros eliminados el mismo día por ser de **otro artista** (no de la banda),
detectados al revisar los snapshots:

- 2 álbumes y 2 canciones de **MacDiezell** ("THUG NATION…") en iTunes.
- 2 podcasts de una persona llamada **Diezel** ("Untamed Radio",
  "Mr. Fitness Show"). Los conteos de iTunes se corrigieron a
  13 álbumes, 33 canciones, 0 podcasts.
- El id de un short de YouTube se guardó como URL completa; se corrigió
  a `frybXWNuNFM`.
- 4 menciones eliminadas por no ser de la banda o no estar verificadas:
  2 de "Diezzel Kunst" (artista plástico argentino, otra persona),
  1 de Say Ocean (el título no nombra a Diezell) y 1 listicle de
  Punkeando sin "Diezell" en el título. Las noticias ahora solo se
  guardan si el título nombra a la banda y no es "Kunst".

El colector `itunes.py` ya filtra por nombre de artista
(`_es_diezell()`), así que no volverá a pasar.

## Correcciones de la auditoría (18 nov 2026, G1–G19)

- **G1 Spotify**: Music Metrics Vault SÍ funciona con la URL exacta
  (`/artists/diezell/2mEQCZzgLbG0mWCwaAEb3g`, recuperada de la
  investigación del 15 nov). artist.tools da 403, el embed de
  Spotify no trae el dato, Viberate sigue en 403. El refresh por
  Livewire se quedó colgado 90 s y no se reintentó (ver AUDIT.md).
- **G2 YouTube**: 29/29 videos con vistas y fecha (la playlist de
  subidas UU trae todos; /videos solo muestra 17).
- **G3 menciones**: `add_mention` normaliza URLs (desempaqueta el
  redirect de Bing); se eliminó el único duplicado (JamBase) con
  nota en `runs/2026-11-18-fix-g3.log`. Es la única corrección
  permitida al ledger.
- **G4 TikTok por video**: itemList vacío en el JSON y
  /api/post/item_list/ devuelve 0 bytes sin sesión. Sin vía.
  Mejora colateral: se usan las cifras exactas de statsV2 (13,752).
- **G5 comentarios**: youtubei/v1/next + continuación → 372
  comentarios de 27 videos guardados; top comentaristas funciona.
  Límite detectado en la primera corrida por systemd: YouTube
  limita la IP compartida tras una ráfaga (todos los POST dieron
  timeout de 30 s; minutos después, mismo entorno, volvían en 1 s).
  Añadido cortocircuito (3 errores seguidos → aborta) y FAIL
  honesto si ningún video da comentarios por error.
- **G6 Wayback**: 429 incluso con esperas de 45–60 s; se reintenta
  a diario con esas esperas.
- **G7 Reddit/pullpush**: todas las rutas 404; documentación tras
  Cloudflare. Sin vía.
- **G8 Songkick**: 1 registro por concierto (recinto, ciudad,
  dirección, fecha) en el ledger.
- **G9 Last.fm**: regex de scrobbles ampliado y VERIFICADO en vivo:
  **64,736 scrobbles** y total de oyentes **2,169** (18 nov). La
  clase antigua ya no existe en la página; el dato vive en el
  bloque header-metadata-tnew. De paso se detectó que el
  "lastfm_listeners" histórico (15) es la cifra semanal de la
  canción popular, no el total del artista: se registra aparte
  (`lastfm_listeners_total`) sin borrar el anterior.
- **G10 noticias**: `news_mentions` ahora cuenta solo noticias
  sobre la banda (`news_mentions_raw` guarda el total del feed);
  los XML ya no se sobrescriben (primer snapshot del día).
- **G11 Deezer**: rank + duración de las 32 canciones de álbum.
- **G12 setlist.fm**: sin página de artista localizable (Bing y
  DuckDuckGo no devuelven nada; el slug adivinado era de otro
  artista). Se reintenta a diario.
- **G13**: enlace a Wikipedia eliminado de `crecimiento.html`
  (artículo borrado). **Nota**: el enlace a Google Fonts se
  conserva en `crecimiento.html` — es la convención de todo el
  sitio, no se quita.
- **G14**: `run_main` acepta `"empty"` (verificación OK sin
  hallazgos); FAIL queda solo para errores de descarga/parseo.
  Aplicado a MusicBrainz, Wikipedia, prensa y stories.
- **G15**: ver `AUDIT.md`.
- **G16**: Google Trends cerrado como no viable; fuera de
  `run_daily.sh`.
- **G17/G18**: Facebook /diezellmx → login; Instagram ?__a=1 →
  302 a login, /embed/ → cáscara sin datos. Cerrados.
- **SoundCloud**: nota de duda añadida al registro semilla
  (soundcloud.com/diezell es otro usuario).
- **commenters.py**: el mes ahora es el mes de captura (el texto
  relativo "4 years ago" generaba meses basura).

## El scheduler (systemd)

**GitHub Actions NO está disponible**: `gh auth status` dice que no hay
ninguna sesión de GitHub en esta VM, y no se crean cuentas.

**Timer activo**: `diezell-ledger.timer` — diario a las **14:00 UTC =
08:00 America/Mexico_City** (CDMX es UTC-6 fijo, sin horario de verano
desde 2022). `Persistent=true`: si la VM estaba apagada a esa hora,
el corte se ejecuta al arrancar.

Instalado en `/etc/systemd/system/` (copias en
`automatizacion/systemd/`). Verificar:

```bash
systemctl list-timers --all diezell-ledger.timer
systemctl status diezell-ledger.timer
journalctl -u diezell-ledger.service -n 30
ls -t datos/ledger/runs/ | head -3
```

**Detalle importante 1 — el proxy**: el servicio lleva
`EnvironmentFile=/etc/environment`. Sin eso, el servicio no tiene el
proxy de salida de la VM ni el bundle CA y **todo HTTPS falla** con
`SSL: WRONG_VERSION_NUMBER` (verificado el 18 nov 2026: el primer
arranque por systemd falló en todos los colectores por esto).

**Detalle importante 2 — el transporte es curl, no urllib**:
bajo systemd, Python-urllib se queda colgado esperando la respuesta
al CONNECT del proxy (el proxy nunca responde; probado con CONNECT
manual, con y sin User-Agent, con curl funcionando en el mismo
contexto en <1 s). `common.fetch()` usa `curl` por subprocess por
eso: mismo comportamiento en el shell y bajo systemd. Si algún día
urllib vuelve a funcionar bajo systemd, el cambio es de una función.

**Límites**:

- Las unidades viven en `/etc/systemd/system/`, fuera de `~/workspace`.
  Si la VM se reinicia o se reemplaza, **se pierden** (verificado el
  18 nov 2026: un reinicio del servicio las borró): reinstalar desde
  `automatizacion/systemd/` con:
  ```bash
  cp automatizacion/systemd/diezell-ledger.* /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable --now diezell-ledger.timer
  systemctl list-timers --all diezell-ledger.timer   # debe decir 14:00 UTC
  ```
- Si la VM está apagada más de un día, `Persistent=true` ejecuta
  **un solo** corte atrasado al arrancar, no uno por día perdido
  (los días perdidos quedan sin corte; el ledger lo muestra).
- **Recuperación del corte del 18 nov 2026**: el reinicio de la mañana
  borró el timer y el corte automático de las 08:00 no corrió. Cesar
  aprobó correrlo a mano el mismo día, 18 nov 19:28 CST:
  `systemctl start diezell-ledger.service` (salida 0, ~5 min 29 s),
  log `datos/ledger/runs/2026-11-19-012828.log`. Ledger 297 → **336
  registros** (+36 con fecha de corte 2026-11-18; +3 fechados
  2026-11-15 de Music Metrics Vault, backfill con la fecha de la
  fuente). Timer reinstalado desde `automatizacion/systemd/` y
  verificado: próximo disparo jue 19 nov 08:00 CST. TikTok 13,752
  (statsV2 exacto, corte de la mañana; la cifra "13,753" que se
  escribió en una versión anterior de este README no existe en el
  ledger), Deezer 884 igual, Spotify 44,147 (MMV, dato del
  15 nov). Fallos conocidos sin cambio: youtube_comments (3 errores,
  0 nuevos), Instagram, Facebook, Reddit, setlist.fm, Bandsintown,
  SoundCloud, TikTok por video. Este método detecta y recupera un
  corte perdido; **no impide** que un reinicio vuelva a borrar un
  timer instalado fuera de `~/workspace`.
- **19 nov 2026, 07:09 CST**: tras el reinicio de las 06:33, las
  unidades volvieron solas (copiadas a /etc a las 13:09 UTC;
  mecanismo desconocido, no es ningún cron ni hook de este proyecto
  — posiblemente el doctor horario del runtime). El timer quedó
  activo y el corte de las 08:00 asegurado sin intervención manual.
  No asumir que esto pasará siempre: el arreglo durable sigue
  pendiente de decisión de Cesar.
- **20 nov 2026**: el corte de las 08:00 corrió solo — la máquina
  arrancó a las 07:43, las unidades volvieron solas a las 08:09 y
  `Persistent=true` disparó el corte 9 min tarde (08:09–08:14),
  ledger 297 → 336 (noche del 18) → 473 (19) → **605 (20)**:
  137 registros del 19, 132 del 20. Pero la VM
  se reemplazó otra vez a las 11:44 y las unidades se borraron por
  tercera vez; reinstaladas a mano a las 11:44, próximo corte sáb
  21 nov 08:00. `Persistent=true` salva el corte cuando las
  unidades vuelven tarde, no cuando no vuelven.
- **20 nov 2026, 12:19 CST**: la VM se reemplazó otra vez (4.º
  borrado). Las unidades volvieron solas a las 13:09 (~50 min),
  timer activo, próximo corte sáb 21 nov 08:00. Ya van 2
  restauraciones solas seguidas (19 y 20 nov); la única vez que no
  volvió fue el 18. Patrón compatible con un trabajo horario de
  reparación del runtime, sin confirmar. Reinstalar a mano ya no es
  el problema diario, pero sigue sin ser garantía.
- **20 nov 2026, ~17:46 CST (5.º borrado)**: la VM se reemplazó
  otra vez y el timer no existía a las 18:07 (`systemctl status`
  → "Unit could not be found"). Reinstalado a mano a las 18:48
  desde `automatizacion/systemd/` y verificado: próximo disparo
  sáb 21 nov 08:00 CST (14:00 UTC), timer activo y habilitado.
  **Vigilante creado esa noche**: cron de Muse
  `diezell-ledger-watchdog` (id `diezell-ledger-watchdog`, cada
  30 min, dueño `goal:diezell-website`, próximo disparo 20 nov
  19:14:19 CST). Cada 30 min comprueba si existe
  `diezell-ledger.timer` y SOLO si falta lo reinstala desde
  `automatizacion/systemd/` + `daemon-reload` + `enable --now` y
  lo verifica. Nunca corre colectores ni toca el ledger. Qué
  restauró las unidades solo el 19 y el 20 sigue sin evidencia
  (ningún hook, cron ni systemd de usuario lo hace); el vigilante
  es el arreglo durable elegido mientras no haya cuentas externas.
- El timer no depende de Muse ni de ninguna IA: es systemd puro.
  Si el timer muere, el sitio sigue mostrando el último corte.

## Correr a mano

```bash
cd automatizacion
./run_daily.sh            # corte completo (tarda ~2 min)
python3 deezer.py         # un solo colector
```

## Costo

$0. Todo es gratis y sin clave: APIs públicas, RSS y páginas
públicas. No hay servicios de pago ni cuentas.

## Qué falta (próximos pasos, no bloquean)

1. **Instagram/TikTok por publicación**: sin login no hay vía. Si la
   banda comparte algún día acceso a su cuenta, el Graph API oficial
   cubre sus propios datos.
2. **Backfill de Wayback**: la descarga da 429 incluso con esperas
   largas; se reintenta a diario. Si algún día responde, el inventario
   CDX ya lista qué snapshots existen.
3. **Mapa de conciertos / páginas por canción**: se alimentan de
   este ledger (Songkick ya da los conciertos pasados con recinto
   y ciudad; Deezer ya da el rank de cada canción).

## Actualización 20 nov 2026 (noche) — correcciones aplicadas

Hechas por subagente, sin cuentas, sin borrar historia:

- **Vigilante del timer**: cron de Muse `diezell-ledger-watchdog`
  (cada 30 min, id en la sección del scheduler). Solo reinstala
  si falta.
- **Web (`diezell-html/`)**: Foro Corona → "Ya pasó" (chip y hero);
  6 enlaces a Wikipedia borrados (footers + fuentes de banda.html);
  bajista: Mau Batarse "por confirmar el nombre completo" con
  enlace al post oficial @diezellmx 2 sep 2026 + nota de conflicto;
  "Los números" actualizados al corte 20 nov (TikTok 13,756,
  Deezer 886, Spotify 44,147 / 16,525 MMV dato 16 nov, El Cuento
  576,090 views); duraciones INSANIA según Deezer (3:53, 4:22,
  3:43, 3:02); `crecimiento.html`: SoundCloud fuera de la gráfica,
  Last.fm total (2,170), nota de Spotify corregida a MMV 16 nov,
  deduplicado de puntos y filtro de videos nuevos por `published`.
- **Colectores**: `youtube_video.py` con yt-dlp (29/29 vistas,
  likes y duración); nuevo `facebook_plugin.py` (5 posts reales);
  `wayback.py` reintenta 429/503 con backoff 20/40/60 s;
  `youtube_rss.py` solo cuenta videos publicados el día del corte.
- **Ledger**: 605 → 610 (Facebook, 5 posts) → 614 (yt-dlp, 4
  registros) → **643** (corte completo de verificación 20 nov
  18:55–19:02 CST: 20 OK / 8 FAIL esperados; youtube_comments se
  recuperó: 67 comentarios nuevos, comments.json 372 → 439).
  Ver `AUDIT.md`, sección de actualización del 20 nov.
- **Lo que NO se pudo**: ver `NO_SE_PUEDE.md`.

- **Watchdog 20 nov 20:14 CST**: timer faltante tras reemplazo de VM; reinstalado desde `systemd/` (daemon-reload + enable --now); activo (waiting), próximo disparo sáb 21 nov 08:00 America/Mexico_City (14:00 UTC).

- **Watchdog 20 nov 22:14 CST**: timer faltante tras reemplazo de VM; reinstalado desde `systemd/` (daemon-reload + enable --now); activo (waiting), próximo disparo sáb 21 nov 08:00 America/Mexico_City (14:00 UTC).
