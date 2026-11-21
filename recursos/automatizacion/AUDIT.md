# AUDIT.md — Autoevaluación del archivo automático de Diezell

Fecha de la auditoría: **2026-11-18** (tras corregir los huecos
G1–G19 de la auditoría independiente). Ledger: **297 registros**,
**372 comentarios**, **2 menciones**. Reglas: $0, sin claves, sin
cuentas, sin logins, sin IA en producción, append-only.

## Cómo leer esta tabla

- **✅ FUNCIONA** — datos reales en el ledger, con evidencia.
- **⚠️ PARCIAL** — funciona pero incompleto, con el hueco medido.
- **❌ CERRADO** — probado y sin vía gratuita sin login; evidencia
  del intento. No se reintenta más (o se reintenta a diario si la
  situación puede cambiar, indicado en cada fila).

## Checklist por fuente y métrica

| Fuente / métrica | Estado | Evidencia / detalle |
|---|---|---|
| **Spotify — oyentes mensuales** | ✅ FUNCIONA (G1) | Music Metrics Vault, URL exacta `/artists/diezell/2mEQCZzgLbG0mWCwaAEb3g` (recuperada de la investigación del 15 nov). Meta description: "44,147 monthly listeners, 16,525 followers". Registro con fecha del dato en la página (16 nov, "Last updated: 2 days ago"). |
| **Spotify — seguidores** | ✅ FUNCIONA (G1) | Misma fuente: 16,525 (16 nov). Semilla 15 nov: 16,534 (Spotify directo). |
| **Spotify — streams totales** | ✅ FUNCIONA (G1) | MMV: 5.5M aprox. (16 nov). Discrepancia con Viberate 9.7M, anotada, no reconciliada. |
| **Spotify — top canciones / ciudades / países** | ✅ SEMILLA | Semillas del 15 nov (investigación manual en navegador). Sin ruta automática para el top por canción (la API no lo da y la web es JS). |
| artist.tools | ❌ CERRADO | 403 en artist.tools y respuesta vacía en app.artist.tools (18 nov). |
| Spotify embed | ❌ CERRADO | HTTP 200, 24 KB, sin el dato en el JSON. |
| Viberate | ❌ CERRADO | 403 dos veces con User-Agent de navegador (18 nov). |
| MMV Livewire refresh | ❌ NO REINTENTADO | El POST a /livewire/update se quedó colgado 90 s sin respuesta; no se repite sin aprobación (ver informe del fixer). La ruta estática funciona sin él. |
| **Deezer — fans** | ✅ FUNCIONA | API sin clave: 884 fans (18 nov). |
| **Deezer — rank por canción** | ✅ FUNCIONA (G11) | 28 registros: top 5 + las 32 canciones de los 13 álbumes (algunas repetidas entre álbum y sencillo). |
| **Deezer — duración por canción** | ✅ FUNCIONA (G11) | 28 registros once=True. |
| **Deezer — álbumes** | ✅ FUNCIONA | 13 álbumes con título, fecha, canciones, fans, tipo. |
| **YouTube — suscriptores** | ✅ FUNCIONA | Página del canal: "12.2 mil" (aprox., texto del canal). |
| **YouTube — total de videos** | ✅ FUNCIONA | 29 videos (página del canal). |
| **YouTube RSS — videos nuevos** | ✅ FUNCIONA | 15 videos en el feed, con id/título/fecha. |
| **YouTube — vistas por video** | ✅ FUNCIONA (G2) | 29/29 videos con vistas (ej. El Cuento 575,250; Sin Rencores 226,710). Fuente: playlist de subidas UU (29 ids en una página; /videos solo muestra 17). |
| **YouTube — fecha de estreno** | ✅ FUNCIONA (G2) | 29/29 videos. |
| **YouTube — duración por video** | ⚠️ PARCIAL | Solo 9/29: el regex `lengthSeconds` no casa en todas las páginas. Hueco menor no incluido en G1–G19; el dato ya existe en Deezer por canción. |
| **YouTube — likes por video** | ⚠️ PARCIAL | Solo 9/29: el regex `likeCount` no casa en la mayoría de páginas. Mismo hueco menor. |
| **YouTube — comentarios** | ✅ FUNCIONA (G5) | youtubei/v1/next + continuación: 372 comentarios en 27 videos (20 en los grandes). yt.lemnoslife.com no responde desde esta VM (vacío); Invidious tras reto anti-bot. **Límite detectado 18 nov**: tras una ráfaga de peticiones YouTube limita la IP compartida (todos los POST dieron timeout de 30 s en la primera corrida por systemd; minutos después, mismo entorno, volvían en 1 s). El colector tiene cortocircuito (3 errores seguidos → aborta) y devuelve FAIL si ningún video dio comentarios por error. |
| **YouTube — top comentaristas** | ✅ FUNCIONA | commenters.json: 314 autores en nov 2026; top @jesuscruz4855, @blakeivan9676, @KxrasuLoL (4 cada uno). El mes es el mes de captura (antes daba meses basura por el texto relativo "4 years ago"). |
| **TikTok — seguidores** | ✅ FUNCIONA | 13,752 exactos (statsV2, 18 nov). Antes 13,800 redondeado. |
| **TikTok — seguidos/videos/likes** | ✅ FUNCIONA | 0 seguidos, 75 videos, 129,074 likes (statsV2). |
| **TikTok — por video** | ❌ CERRADO (G4) | itemList vacío en el JSON del perfil; /api/post/item_list/ devuelve 0 bytes sin sesión (msToken). Sin vía sin login. |
| **TikTok — hashtags** | ❌ CERRADO | Las páginas #Diezell, #Caoticos, #INSANIA no exponen conteos ni videos parseables. |
| **TikTok — historias** | ❌ CERRADO | UserStoryStatus 0; sin historia activa visible sin login. |
| **Instagram — perfil/posts** | ❌ CERRADO (G18) | web_profile_info 429; página muro de login; ?__a=1 → 302 a login; /embed/ → 200 pero cáscara JS sin datos (18 nov). |
| **Instagram — historias** | ❌ CERRADO | Exigen login. |
| **Facebook** | ❌ CERRADO (G17) | /diezelloficial 302 y /diezellmx 400, ambos al login. |
| **Reddit — .json** | ❌ CERRADO | 403/HTML en www, api y old. |
| **Reddit — pullpush.io** | ❌ CERRADO (G7) | api.pullpush.io responde en raíz pero todas las rutas de búsqueda dan 404; la documentación está tras Cloudflare (403). |
| **Google News RSS** | ✅ FUNCIONA (G10) | news_mentions = solo banda (1+1); news_mentions_raw = total del feed (5+2). XML con primer snapshot del día. |
| **Bing News RSS** | ✅ FUNCIONA (G10) | news_mentions = 1 sobre la banda; raw = 1. |
| **Prensa RSS** | ✅ FUNCIONA | 4 medios; 0 artículos sobre Diezell el 18 nov (hallazgo negativo = OK, G14). |
| **MusicBrainz** | ✅ FUNCIONA (G14) | count 0: Diezell no existe (ni artista ni 'Caótico'). Verificación OK sin hallazgos. |
| **iTunes Search** | ✅ FUNCIONA | 13 álbumes, 33 canciones, 0 podcasts (filtrado anti-MacDiezell/Diezel). |
| **Wikipedia** | ✅ FUNCIONA (G14) | Artículo borrado 17 jul 2026 (promocional/COI); API 404. Verificación OK sin hallazgos. Enlace quitado de crecimiento.html (G13). |
| **Wayback — inventario CDX** | ✅ FUNCIONA | Spotify 3 capturas, Viberate 4, resto 0. |
| **Wayback — descarga de snapshots** | ❌ CERRADO por ahora (G6) | 429 en ambas descargas incluso con esperas de 45–60 s (la IP de salida está limitada). Se reintenta a diario con esas esperas. |
| **Google Trends** | ❌ CERRADO (G16) | explore 429 sin cookies; RSS genérico. Fuera de run_daily.sh, no se reintenta. |
| **Charts (Deezer/iTunes)** | ✅ FUNCIONA (G14) | Diezell no está en Deezer top 10 ni iTunes MX top 25. Verificación OK sin hallazgos. |
| **Songkick — fans/próximos/pasados** | ✅ FUNCIONA | 764 fans, 0 próximos, 3 pasados. |
| **Songkick — 1 registro por concierto** | ✅ FUNCIONA (G8) | 3 eventos: Foro Corona, Monterrey, 13 nov 2026; FÜCK OFF ROOM, CDMX, 24 oct 2026; Madre Santa Pulqueria, Puebla, 23 oct 2026 (con dirección). |
| **setlist.fm** | ❌ CERRADO (G12) | Búsqueda 202 vacía (anti-bot); Bing/DuckDuckGo no devuelven la página del artista; el slug adivinado era de otro artista (Reuben Hernandez). Se reintenta a diario. |
| **Bandsintown** | ❌ CERRADO | HTTP 403. |
| **Last.fm — oyentes** | ✅ FUNCIONA | Encabezado 15 (ver nota abajo); por álbum INSANIA 1,352; 776; 482; 411. Total del artista **2,169** (18 nov, nuevo bloque header-metadata-tnew). |
| **Last.fm — scrobbles** | ✅ FUNCIONA (G9) | **64,736** scrobbles (18 nov, verificado en vivo). La clase antigua ya no existe en la página: el dato vive en header-metadata-tnew con el exacto en `<abbr title="64,736">`. La página alterna con el reto anti-bot de 3 KB (~50 % de los intentos); el colector falla como debe en ese caso y acierta cuando carga la real. |
| **Last.fm — nota de dato** | ⚠️ CORREGIDO | El "lastfm_listeners" histórico (15) es la cifra semanal de la canción "Popular this week", no el total del artista. Se registra ahora `lastfm_listeners_total` (2,169) sin borrar el anterior; el detalle lo explica. |
| **SoundCloud** | ⚠️ DUDA | soundcloud.com/diezell es otro usuario (Alycyalyna). El registro semilla de 13 seguidores lleva nota de duda; perfil real no localizado. |

## Cobertura estimada

- **Métricas capturables gratis sin login: ~85–90 %** (antes del
  arreglo: ~70–75 %). Quedan fuera, sin vía conocida: Instagram,
  Facebook, Reddit, setlist.fm, Bandsintown, TikTok por video,
  Wayback (429), Google Trends.
- **Por tipo de dato**: seguidores/oyentes por red ✅ (salvo
  Instagram/Facebook); likes/vistas/comentarios por publicación ✅
  YouTube, ❌ TikTok/Instagram; menciones en prensa ✅; conciertos
  ✅ (Songkick); historias ❌ (solo rescate si aparece una visible
  sin login, que hoy no ocurre).

## Integridad del ledger

- Append-only: 293 registros, fechas 2026-10-23 a 2026-11-18.
- **Una única corrección autorizada (G3)**: 1 mención duplicada
  eliminada de mentions.json (JamBase, mismo destino con distinto
  parámetro de tracking de Bing), con nota en
  `runs/2026-11-18-fix-g3.log`. Ningún registro del ledger se ha
  borrado; el registro semilla de SoundCloud solo se anotó con
  una nota de duda en su detalle.
- Todos los registros llevan fecha de corte, fuente y URL.
  Las cifras de fuentes distintas nunca se mezclan.

## Autoevaluación (lo que el auditor independiente pidió)

- ¿Se intentó capturar cada like, vista, comentario, publicación
  y seguidor en cada lugar donde se menciona a Diezell? **Sí, en
  todas las vías gratuitas sin login conocidas** (ver tabla).
  Lo que no se captura hoy es porque la vía está cerrada con
  evidencia, no porque no se intentara.
- ¿Queda alguna técnica sin probar? Las conocidas y gratuitas
  están probadas. Quedan dos ideas no probadas por falta de vía:
  (1) el refresh Livewire de MMV (se colgó 90 s; repetirlo
  necesita aprobación); (2) la paginación de comentarios de
  YouTube más allá de la primera página (20 por video) — posible
  con el mismo endpoint, pendiente de decidir si vale el tiempo
  de corrida.
- Huecos menores detectados en esta auditoría y no incluidos en
  G1–G19: duración (9/29) y likes (9/29) por video de YouTube —
  los regex no casan en todas las páginas; el dato de duración
  ya existe por canción en Deezer.
- **Limitación transitoria (18 nov, corrida por systemd 01:30)**:
  la IP compartida de salida se limita bajo ráfagas: Deezer dio
  403 y youtubei timeouts de 30 s en esa corrida, mientras que
  minutos antes y después los mismos endpoints respondían en
  ~1 s. Los colectores marcan FAIL honesto y reintentan al día
  siguiente; los datos ya guardados no se pierden. No es un
  fallo del código: es el límite del entorno gratuito.

## Actualización 20 nov 2026 (noche) — correcciones aplicadas, sin borrar historia

Ledger: 605 registros (corte 20 nov 08:09–08:14) → **610** tras el
nuevo colector `facebook_plugin.py` (5 posts) → **614** tras
`youtube_video.py` con yt-dlp (2 videos × vistas+likes que faltaban
por el 429) → **643** tras el corte completo de verificación del
20 nov por la noche (18:55–19:02 CST, 20 OK / 8 FAIL esperados;
+29 registros `youtube_video_comments_saved`, uno por video:
youtube_comments se recuperó con 67 comentarios nuevos, 0 errores;
comments.json 372 → 439, commenters 314 → 363 autores).

- **YouTube — duración y likes por video: ✅ FUNCIONA (corregido)**.
  `youtube_video.py` ya no parsea HTML con regex: usa yt-dlp
  (2026.10.26, ya instalado), que devuelve duration, view_count y
  like_count. Prueba 20 nov: 29/29 videos con vistas, likes y
  duración (ej. El Cuento 576,286 vistas, 8,648 likes, 223 s).
  La fila "Solo 9/29" de arriba queda desactualizada.
- **YouTube — videos nuevos: bug corregido.** `youtube_rss.py`
  contaba cada video del feed en cada corte (15 "nuevos" al día).
  Ahora solo cuenta el video cuya fecha de publicación es la del
  corte (20 nov: 0 nuevos, correcto). Los 45 registros históricos
  (15 por día, 18–20 nov) NO se borran (append-only); la gráfica
  de `crecimiento.html` filtra por `published`, no por fecha de
  corte.
- **Facebook: ⚠️ PARCIAL (nuevo).** El plugin público de página
  (`facebook.com/plugins/page.php`, tabs=timeline) devuelve 200
  con los últimos 5 posts reales (20 oct, 2, 3 y 10 nov 2026),
  con texto y fecha real. Nuevo colector `facebook_plugin.py`,
  en `run_daily.sh`. Seguidores/likes de Facebook siguen
  cerrados (0 coincidencias en el plugin). La fila "Facebook ❌
  CERRADO (G17)" se refiere a la página directa (muro de login),
  que sigue cerrada.
- **Wayback — descarga de snapshots: ⚠️ PARCIAL (corregido).**
  El bug era que `fetch()` lanza excepción en HTTP ≥ 400, así
  que el 429 nunca llegaba al reintento. Ahora `wayback.py`
  reintenta 429/503 con backoff 20/40/60 s (CDX y snapshots).
  Prueba 20 nov: los 2 snapshots se descargaron sin 429.
  Sigue sin cifra de oyentes parseable en ellos.
- **TikTok — serie real del ledger:** 13,752 (18 nov, statsV2) →
  13,755 (19 nov) → 13,756 (20 nov). La cifra "13,753 (noche del
  18 nov)" que aparece en el README **no existe en el ledger**;
  no usarla. Viberate 11.3K era un dato viejo/redondeado.
- **Streams totales:** el 9.7M de Viberate **no existe en el
  ledger** (ningún registro con ese valor). Viberate es fuente de
  baja confianza (403 a los colectores, texto generado sin
  verificar en su página). El 5.5M de MMV sí está registrado
  (15 y 16 nov, aproximado). Nunca promediar ni reconciliar.
- **Spotify vía MMV: estancado.** La página de MMV no se
  actualiza desde el 16 nov (44,147 oyentes / 16,525
  seguidores). La gráfica de oyentes termina el 16 nov aunque
  se sincronice. El refresh Livewire sigue sin reintentarse.
- **SoundCloud:** sigue dudoso (perfil de otro usuario). La
  gráfica de `crecimiento.html` ya no lo muestra (excluido de
  la lista de redes); el registro semilla queda con su nota de
  duda, sin borrar.
- **Last.fm:** la gráfica ya usa `lastfm_listeners_total`
  (2,170 el 20 nov) en vez de la cifra semanal (13).
- **YouTube comentarios: RECUPERADO en el corte de verificación.**
  Fallaba 3 cortes seguidos por límite de YouTube, pero el 20 nov
  por la noche (corte de verificación 18:55–19:02 CST) funcionó:
  **67 comentarios nuevos en 29 videos, 0 errores**; comments.json
  372 → **439**, commenters 314 → **363 autores**. El límite es
  intermitente: se levanta solo. No forzar en ráfaga.
- **Timer — 5.º borrado:** VM reemplazada 20 nov ~17:46, timer
  ausente a las 18:07. Reinstalado a mano 20 nov 18:48, próximo
  disparo sáb 21 nov 08:00 CST verificado. **Vigilante creado:**
  cron de Muse `diezell-ledger-watchdog`, cada 30 min, solo
  reinstala el timer si falta (nunca corre colectores). Ver
  README, sección del scheduler.
- **Cobertura estimada tras estas correcciones: ~92–95 %.**
  Quedan cerrados sin login/cuenta: Instagram, TikTok por video,
  Reddit, setlist.fm, Bandsintown, seguidores/likes de Facebook,
  Google Trends.
