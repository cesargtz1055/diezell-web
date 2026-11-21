# Guía completa de Diezell — todo lo que ya existe

**Para ChatGPT (y para quien toque este proyecto): lee esto antes de programar,
rediseñar o borrar nada.** Aquí está todo lo que ya se investigó, automatizó,
mejoró e ideó, con su contexto y sus razones. El objetivo es no duplicar trabajo
y no quitar cosas que ya se desarrollaron. Si algo de aquí contradice lo que
vas a hacer, pregunta en Issue #1 antes de cambiarlo.

**Fecha:** 21 nov 2026. **Rama de recursos:** `muse/recursos-diezell` (381 archivos).
**Sitio en vivo:** https://cesargtz1055.github.io/diezell-web/ (raíz = diseño original
v2.0; `/preview/` = rediseño de Música del PR #3; `/nuevo/` = 37 páginas
reconstruidas con la dirección editorial).

**Regla de oro:** nada se fusiona ni se publica en `main` sin la aprobación
expresa de Cesar (el propietario). ChatGPT lidera dirección creativa/técnica;
Muse hace QA e implementación. Cesar no crea cuentas ni hace configuraciones:
todo lo resuelve Muse con lo que ya controla.

---

## 1. La banda (todo verificado, 8 nov 2026)

Diezell, banda de pop punk / rock en español de **Monterrey, Nuevo León**.
Proyecto original desde 2018; covers desde 2015 en Calle Morelos; conocida desde
2021 por el sencillo debut «Sin Rencores». Informe completo:
`recursos/investigacion/diezell-banda-20261108.md`.

**Integrantes confirmados:** René Guzmán (voz; también guitarra en vivo,
@reneguzman19), José Bernardo «Bernie» (guitarra), Emmanuel Batarse «Emmash»
(batería; también productor y coros en vivo). **Bajista: por confirmar.**
La evidencia apunta a **Mau Batarse** como bajista actual (post oficial
@diezellmx 2026-09-02; video de fan tocando el bajo en vivo en Foro Corona
15 nov 2026). José Aguilar solo aparece en el artículo de Wikipedia, que fue
**borrado el 17 jul 2026** (promocional / conflicto de intereses): el sitio
**no debe enlazarlo**. Nunca inventar el nombre completo de Mau (no está
publicado; Deezer acredita a «Nazry Mauricio Chávez» como cocompositor en
INSANIA, pero el puente Nazry = Mau es circunstancial, no probado).

**Discos:**
- **Caótico** (29 sep 2023), 11 canciones, 37:56. Spotify: `738DN211pKelLzZTRzIC28`.
- **INSANIA** (28 nov 2025), 10 canciones, 36:46. Spotify: `3LGm9FVg9cswGMo5YneJ88`.
- **6 sencillos** (incl. «Sin Rencores», «El Mejor De Mis Errores», «Muérdago
  Marchito», «Hipocresía», «Insomnio», «Tiempos De Un Tiempo»).

**Enlaces oficiales:** Spotify artista `2mEQCZzgLbG0mWCwaAEb3g`, YouTube
@diezellmx, TikTok @diezellmx, Instagram @diezellmx, Facebook diezelloficial,
Linktree `linktr.ee/diezellmx`.

**Datos (corte 15 nov 2026, con fuente):** Spotify 44,147 oyentes mensuales
(44,822 el 8 nov: −675, −1.5%), 16,534 seguidores. Top ciudades: CDMX 5,768,
Lima 2,641, Monterrey 2,018, Guadalajara 1,682, Puebla 1,586. México 69.47% de
los oyentes. Solo 2 canciones arriba del millón: «El Cuento De Aquel
Imperfecto Ser» 1,678,233 y «Sin Rencores» 1,048,396. **Los totales de streams
nunca cuadran entre fuentes** (Viberate 9.7M vs Music Metrics Vault 5.5M):
mantener etiquetas de fuente, nunca promediar ni reconciliar.

**Gira Insania Tour 2026 (cerrada):** 21 ago Aguascalientes Rocksí, 22 ago
Guadalajara C3 Rooftop, 16 oct Toluca Foro Landó, 17 oct Querétaro, 23 oct
Puebla, 24 oct CDMX Fuck Off Room, 6 nov León El Callejón, 7 nov San Luis
Potosí Estación Wadley, cierre **13 nov 21:00 Monterrey Foro Corona**. Todas
las fechas ya pasaron; el sitio las muestra como archivo, nunca como agenda
vigente. No inventar fechas futuras.

**Letras:** solo fragmentos cortos verificados (8 en uso, en
`datos/canciones.json` y en las fichas). Letras completas necesitan licencia.
Fragmentos: El Cuento («Tuve cien / Cien maneras de explicarlo todo, y fallé»),
Sin Rencores («Ve y cuéntale a tus sábanas…»), El Mejor De Mis Errores,
Muérdago Marchito, Suspensión, De Espaldas, Conmiseración, Resiliencia.

**Prensa verificada:** Puro Rock Puro 16 dic 2025 sobre INSANIA
(`purorockpuro.com/diezell-presenta-insania-su-segundo-album-de-estudio/`)
— de ahí viene la frase «un año entero de reunirse noche tras noche para
componer el disco…» (cita real, no inventada; la descripción clínica del mismo
artículo se eliminó a petición de Cesar, no restaurarla). Puro Rock Puro
5 oct 2023 sobre Caótico. Follow Control (ene 2024) sobre el Foro Tims.

**Preguntas abiertas (sin resolver, no inventar):** nombre exacto del primer EP
(«La Tormenta Antes De La Calma» vs «Después de la Calma») y su tracklist;
año original de «Insomnio» (2018 vs 2021); fecha/venue de Mexicali; cifras
exactas de seguidores de Instagram/Facebook.

---

## 2. Investigaciones

- **Investigación de la banda** (8 nov 2026):
  `recursos/investigacion/diezell-banda-20261108.md` — historia, integrantes,
  discos, enlaces, datos, gira. Verificación en vivo en Spotify, YouTube y
  TikTok ese día; resto por índice con fuentes citadas.
- **Auditoría de diseño web moderno** (8 nov 2026):
  `recursos/investigacion/diezell-rediseno-moderno-20261108.md` — 5 webs
  visitadas en vivo (Sleep Token, Bring Me The Horizon, Bad Omens, Linkin Park,
  Deftones) + 2 por índice (Arctic Monkeys, The 1975). Patrones: hero 100vh,
  tipografía gigante, mucho aire, un CTA por pantalla. La identidad de Diezell
  se verificó con Wikipedia, entrevista en Mr Indie, Puro Rock Puro, Instagram
  oficial y pósters del Insania Tour. No se inventó ninguna URL ni dato.

---

## 3. El sitio (37 páginas reales, no one-page)

Cesar rechazó expresamente el one-page: quiere todo organizado e intuitivo en
páginas separadas. Estructura de silos aprobada 20 nov 19:23 (cada contenido
vive en UN solo silo; la ficha de canción es hoja; Números agrega y enlaza,
no duplica):

- **Música** → álbum (INSANIA / Caótico / Sencillos) → canción (27 fichas).
- **Banda** → integrante (René, Bernie, Emmash, Mau) + Historia.
- **En vivo** (archivo de la gira + galería + video).
- **Caóticos** (comunidad de fans).
- **Números** (crecimiento: gráficas desde el ledger; se entra desde Música y Banda).

**Diseño original (v2.0, raíz del sitio):** app de fans mobile-first, 5 páginas
base + 27 fichas + 4 miembros = 37 páginas. ADN visual de INSANIA: negro
`#0A0A0A`, hueso `#F2F0EB` / gris `#C9C9C4`, un solo rojo `#8E1B1B`,
tipografía Anton (títulos) + Archivo (cuerpo). Navegación inferior fija,
fila de historias, galería en masonry, En vivo como feed vertical, barra de
reproductor fija. **Móvil es la superficie más importante.** Márgenes
constantes de 20 px, contrastes duros, nada de texto sobre el rostro en el
hero, nada de botones-juguete ni enlaces que no lleven a escuchar, ver o
unirse, nada de notas de desarrollador en la web para fans.

**Archivos:** todo el sitio descomprimido está en la rama `muse/recursos-diezell`
(raíz: HTML, `styles.css`, `app.js`, `audio/playlist.json`,
`datos/canciones.json`, `datos/ledger/*`) y en los ZIP desplegados
(`parte-1.zip` = 37 páginas + datos + 12 imágenes; `parte-2.zip` y
`parte-3.zip` = 27 adelantos de audio). El proyecto Astro original está en
`recursos/astro-original/` (solo `src/`, `public/`, config; sin
`node_modules` ni `dist`). El plan es portar el HTML de vuelta a Astro al
final; Astro es opción arquitectónica posterior, no migración automática.

---

## 4. Audio (permiso de la banda, 17 nov 2026)

La banda dio permiso a Cesar para usar las canciones en el fan site, con dos
condiciones: bajarlas de YouTube y **limitar la reproducción a 1:30** con un
botón para escuchar la completa en Spotify/YouTube.

- Las 27 canciones se descargaron **enteras** como masters (91 MB, fuera de la
  web pública, **nunca se suben al repo ni se publican**).
- La web sirve solo **adelantos de exactamente 90.000 s** (38 MB), con el
  límite en código (`PREVIEW_LIMIT_SECONDS = 90`).
- Reproductor interno estilo Spotify, barra inferior fija, al llegar a 1:30 se
  para solo y sale el botón a la completa, sin auto-avance.
- `audio/playlist.json`: 27 canciones con preview, YouTube, Spotify y álbum.

**Bug y arreglo:** el ZIP desplegado no incluía `audio/playlist.json` (404 en
vivo) y el reproductor mostraba «No se pudo cargar la lista de canciones» en
todas las páginas. Se reconstruyó el ZIP con el archivo y se publicó como
`ba704ca` con aprobación expresa de Cesar (solo ese arreglo).

---

## 5. Automatización y datos — el ledger (el archivo vivo)

Dirección v3.0 de Cesar (18 nov): la web es un **archivo para fans de verdad**,
no un folleto. Reglas duras: **GRATIS, AUTÓNOMO** (sin IA/Muse en producción,
sin curación, sin pasos manuales, sin cuentas/logins), **pura automatización
determinista** (código + programador), **nunca se reemplaza un dato, siempre
se almacena** (append-only, un registro por fecha de corte, por métrica y por
fuente). El sitio dibuja las gráficas desde el JSON estático con JS puro, sin
backend ni dependencia externa en tiempo de ejecución.

**Lo que existe (fase 1, auditada 18 nov, ~85–90% de cobertura gratuita):**
- `datos/ledger/ledger.json` — registro append-only (643 registros a 20 nov;
  63 nuevos el 21 nov; el corte diario de las 08:00 corre con temporizador).
- `datos/ledger/comments.json` (439 comentarios de YouTube) y
  `commenters.json` (363 autores), `mentions.json`.
- `datos/ledger/runs/*.log` — un log por cada corte diario.
- `datos/ledger/snapshots/` — respuestas crudas de Deezer/YouTube/RSS por fecha.
- **26 colectores deterministas** (Python + curl, $0, sin claves ni cuentas) en
  `recursos/automatizacion/` + `run_daily.sh` + unidades systemd.
- **Temporizador** `diezell-ledger.timer` diario 08:00 America/Mexico_City +
  vigilancia que lo reinstala si desaparece (las unidades viven en `/etc` y se
  borran en cada reemplazo de la VM; el corte de las 08:00 del 21 nov sí corrió).
- **Página El crecimiento** (`crecimiento.html`): gráficas de oyentes,
  seguidores por red y actividad por corte, leyendo el ledger en vivo.

**Fuentes verificadas sin clave:** Deezer, Reddit .json, YouTube RSS, Google
News RSS, MusicBrainz, iTunes Search. Con clave gratuita: YouTube Data API v3,
Last.fm, setlist.fm, Podcast Index. Ruta de oyentes mensuales de Spotify:
Music Metrics Vault (44,147 oyentes, 16,525 seguidores, datos del 16 nov; la
página no se ha actualizado desde entonces, así que la gráfica de Spotify está
congelada ahí).

**Lo que NO se puede (documentado en `recursos/automatizacion/NO_SE_PUEDE.md`,
no intentarlo de nuevo sin una vía nueva):** Instagram (perfil, historias,
seguidores) sin login; TikTok por video; Reddit; setlist.fm; conteos de
Facebook; frescura diaria de Spotify; listas de seguidores (los conteos sí);
dominio propio y CI externo sin cuentas. Las historias duran 24 h y los videos
firmados ~32–36 h: rescatar = sondear cada pocas horas y guardar el archivo
de inmediato. Auditoría completa en `recursos/automatizacion/AUDIT.md`.

**Números que nunca cuadran:** los totales de streams difieren por fuente
(Viberate vs Music Metrics Vault); TikTok pasó de 11,300 (Viberate, 15 nov) a
13,753 (corte 18 nov): ambas cifras se guardan con su fuente, sin mezclarlas.

---

## 6. Mejoras ya hechas (no rehacerlas, no revertirlas sin preguntar)

- **Rediseño Astro + Material Design 3** (8–10 nov): proyecto Astro real
  (Astro 5.12 + Tailwind 4, sin React), tokens M3, escala tipográfica, botones
  y chips con estados, barra superior + navegación móvil, objetivos táctiles
  48 dp, contraste AA, reduced-motion.
- **Eliminación del marco clínico** (10 nov): grep 0 para paciente, autopsia,
  expediente, clínic, radiografía, forense, deterioro. Solo queda «anatomía»
  dentro de la cita de la letra de Sin Rencores. En su lugar van fragmentos
  de canciones con su canción y enlace, cada frase una sola vez.
- **Portadas reales** (10 nov): las portadas genéricas SVG se reemplazaron por
  las oficiales de Spotify (640×640, verificadas visualmente).
- **Frases y citas con fuente** (10 nov): cada frase descriptiva aparece una
  sola vez; las citas son completas, con contexto mínimo y atribución corta
  (medio, fecha, enlace), solo donde aportan valor.
- **Fix móvil `daf6b50`** (20 nov, verificado en vivo): hero con la foto grande
  de nuevo (se eliminó el bloque `.hero-arc` de tarjetas inclinadas); fila de
  historias restaurada a los 5 accesos rápidos v2.0 (INSANIA, Caótico, Foro
  Corona, Foro Tims, Monterrey); tira de datos restaurada (44,147 / 16,534 /
  1,678,233); botón «INSANIA en Spotify» restaurado; títulos de canciones
  subrayados con ` ›` para que se vean tocables; nombres de miembros sin
  romperse; palabras pegadas corregidas globalmente; fallbacks en
  crecimiento.html. **Pendiente:** fotos individuales de Emmash y Bernie (no
  existen retratos verificados; el sitio usa fotos grupales con pie explícito).
- **Fix playlist.json** (`ba704ca`, 20 nov, con aprobación de Cesar): ver §4.
- **P1 — copy y accesibilidad** (PR #5, abierto): «Unirme a los Caóticos» →
  «Conoce a los Caóticos» (no existe mecanismo de afiliación: no prometer un
  club ni registro que no existe); meta description; bloque
  `@media (prefers-reduced-motion: reduce)`; encabezado de styles.css «5 pages»
  → «37 pages».
- **PR #6 — fix hero a 360 px** (abierto): regla `@media (max-width: 380px)`
  con la foto 1:1. **Re-prueba v2 (build correcto): funciona a 320/360/375 px,
  falla a 390 px** (el breakpoint es 380 px; el subtítulo queda tras el dock
  y la tabbar) **y con zoom 200%** (subtítulo bajo el fold, 75 px de desborde
  horizontal). Sugerencia: ampliar el breakpoint a 400 px.
- **PR #4 — fuentes auditables** (abierto): la rama `muse/fuentes-2026-11-20`
  contiene el contenido exacto del ZIP desplegado (57 archivos de texto) +
  `HASHES.md` (SHA-256 de los 69 archivos del ZIP; los 12 JPG no están en la
  rama porque no se pueden subir binarios por esa vía, pero sus hashes y
  tamaños están en HASHES.md) + `docs/capturas/` (21 capturas antes/después).
- **Regla de no perder información** (17 nov): nada se pierde, solo se pule y
  se ordena. Lo quitado queda en `diezell-html/archivo/` o en un respaldo
  (`workspace/diezell-backups/v2.0-2026-11-17/`, `v2.1-2026-11-18-audio/`,
  `v2.2-pre-reestructuracion-2026-11-20/`).

---

## 7. Lo que se quitó y por qué — NO restaurar sin preguntar en Issue #1

| Quitado | Por qué | No hacer |
|---|---|---|
| Marco clínico/paciente (expediente, autopsia, CASO Nº, radiografía, forense) | Cesar lo pidió explícito: «en lugar de eso de pacientes y cosas raras pon frases de canciones» | No restaurar descripciones clínicas ni metáforas de paciente |
| Descripciones inventadas («un año componiendo noche tras noche…» como texto propio) | Cesar: «si no viene de entrevistas reales o canciones no inventes cosas». La frase existe como cita de Puro Rock Puro (16 dic 2025) con su fuente; como descripción propia, no | No inventar descripciones, biografías, fechas ni datos |
| Bloque `.hero-arc` (tarjetas inclinadas en el hero) | Feo en móvil; el fix `daf6b50` lo eliminó y restauró la foto grande | No reintroducir el arco ni tarjetas inclinadas en el hero |
| 4 modales de historias de miembros en index | Eran el mismo botón repetido; la fila de historias volvió a ser 5 accesos rápidos v2.0 | No duplicar botones decorativos; cada elemento UNA utilidad funcional única |
| 2 iframes de Spotify en escuchar.html (PR #3, solo en `/preview/`) | Redundantes; quedaron los enlaces oficiales a los álbumes y al artista | No reintroducir iframes de Spotify |
| Copy «Unirme / Únete» (Caóticos, index) | No existe mecanismo de afiliación, club ni registro | No prometer un club, registro o afiliación que no existe |
| Enlace a Wikipedia de Diezell | Artículo borrado 17 jul 2026 (promocional/COI) | No enlazarlo ni citarlo como fuente |
| «Próximo concierto» / agenda vigente | La gira cerró el 13 nov 2026; no hay fechas anunciadas | No implicar conciertos futuros sin fuente vigente |
| Portadas SVG genéricas | Reemplazadas por las portadas oficiales de Spotify | No usar portadas inventadas |
| «5 pages» en el encabezado de styles.css | Son 37 páginas reales | No decir 5 páginas |
| Dock en `/preview/` (PR #3) | El PR oculta `.player-bar` en TODO el sitio (`display:none!important`) y su `app.js` solo inicializa el reproductor si la página tiene `#dz-player`. Decisión de producto pendiente de Cesar: en Inicio, Banda, En vivo, Caóticos y Números el dock es el ÚNICO control de audio | No asumir que quitar el dock es correcto; es decisión del dueño |
| Aviso «Prototipo visual» y acento lima en `/nuevo/` | El prototipo editorial evolucionó: el acento pasó de lima `#c9ff12` a terracota `#f18a64`, se quitó el aviso y el pie ahora dice «Archivo independiente creado por fans · No afiliado a la banda» | No reintroducir el aviso ni el lima sin acordarlo |
| Línea `dz-song-context` visible en fichas | `editorial-pass.py` la inserta tras cada H1, pero `site-modern.css` la oculta con `display:none!important`: contradicción sin resolver (si debe verse, sobra la regla; si no, sobra insertarla) | Resolver la contradicción, no ignorarla |
| Fotos de Mau en el prototipo nuevo | Se evitan para no prejuzgar el bajo («por confirmar») | No usar fotos de Mau como bajista confirmado |

## 8. Ideas y dirección v3.0 (qué falta por construir)

Dirección v3.0 de Cesar (18 nov): dejar de agregar cosas sueltas y programar
funcionalidad real. El archivo para fans de verdad:

1. **Mapa interactivo estilo rasca-estados** de México con los lugares donde
   Diezell ha tocado. (No construido.)
2. **Una página por canción (27) con letra y material relacionado.** HECHO
   (las 27 fichas existen). Letras completas necesitan licencia: solo
   fragmentos + enlaces.
3. **Histórico de datos con capturas guardadas y pronósticos.** El ledger y
   las gráficas existen; los pronósticos no están construidos.
4. **Recursos hechos por fans.** No construido.
5. **Cosas efímeras guardadas + líneas de tiempo fáciles de seguir.** Parcial:
   el ledger guarda cortes y comentarios; las líneas de tiempo no están
   construidas.
6. **Automatizaciones reales (RSS y APIs públicas).** HECHO (26 colectores).

**Ideas propuestas (no construidas, no duplicar el trabajo de propuesta):**
- **«Adivina la canción»** (propuesta de Muse, aceptada por ChatGPT como P2
  para investigar): juego autocontenido con los 27 adelantos — escucha unos
  segundos y adivina la canción; 4 opciones de títulos reales, sin autoplay,
  teclado, fallback sin audio, puntuación local. Sin tocar el reproductor
  del PR #3.
- **Recorrido guiado por INSANIA** (propuesta de Muse en la revisión del PR #3):
  secuencia curada de los 10 temas con una línea de contexto verificada por
  tema (fragmento o cita real), usando el mismo reproductor. Sin nuevos
  assets, sin datos inventados. Programar cuando se fusione el PR #3.
- **Nueva dirección visual «Papel / Archivo INSANIA»** (prototipo de portada,
  21 nov, en `workspace/diezell-publish/direccion-visual/`): 3 direcciones
  investigadas con referencias reales — A «Papel / Archivo INSANIA» (elegida),
  B «Luz azul / Documento en vivo», C «Fanzine / Collage del tour» — más
  alternativa propia (A como sistema base + C como «capa Caóticos»). Papel
  cálido `#f3f0e8`, tinta, acento azul petróleo `#0e5a72` muestreado de la luz
  azul real de las fotos, Fraunces autocontenida, 8 fotos autorizadas con
  crédito visible, 0 peticiones externas, verificado a 360/390/768/1440 sin
  desbordes. Defecto conocido: «Aguascalientes» se guiona a 360 px.
  Pendiente: enlace público para que Cesar lo vea (aprobación vencida) y
  subida a una rama de diseño aislada.

---

## 9. Reglas duras (no negociables sin Cesar)

1. **No inventar** datos, letras, permisos, funciones, fechas ni biografías.
   Lo dudoso va marcado «por confirmar».
2. **Crédito de foto ≠ permiso.** Las 12 imágenes están documentadas en
   `recursos/fotos.md` (autor, fuente, fecha, estado). El permiso de
   reutilización de Balleza Photography y Follow Control **no está verificado**.
   La banda dio permiso explícito solo para las **canciones** (adelantos 1:30).
3. **Ledger append-only:** nunca se reemplaza un dato, siempre se almacena
   con fecha de corte y fuente.
4. **Nada se fusiona ni se publica sin la aprobación expresa de Cesar.**
   Los PR #3, #4, #5, #6 y #7 están abiertos y en borrador; ninguno fusionado.
5. **Móvil primero** (80% de prioridad). Sin scroll horizontal, menú usable
   con teclado, titular legible sin tapar CTAs; desktop 1440 con composición
   propia, no un móvil ampliado.
6. **Automatización pura en producción:** sin IA, sin curación, sin cuentas,
   sin pagos, sin pasos manuales. Código determinista + programador.
7. **No duplicar:** cada contenido vive en un solo silo; cada elemento UNA
   utilidad funcional única; sin botones decorativos repetidos.
8. **Sin letras completas** (licencia) y sin «oficial / en vivo ahora /
   próximo concierto» sin fuente verificable.
9. **El bajista es «por confirmar».** No inventar el nombre completo de Mau
   ni el rol de José Aguilar.
10. **No tocar el trabajo del otro sin coordinar** en Issue #1. ChatGPT no
    edita los archivos activos de Muse y viceversa sin acordarlo.

---

## 10. Estado actual (21 nov 2026, 11:30 CST)

- **Raíz del sitio en vivo:** diseño original v2.0 (negro/hueso/rojo, Anton),
  con el fix móvil `daf6b50` y el fix de playlist. Sin cambios desde el 20 nov.
- **`/preview/`:** rediseño de Música del PR #3 (catálogo de 27 fichas, búsqueda
  con tolerancia a acentos, filtros, un solo reproductor, 0 iframes). Verificado
  en vivo 7/7, 0 defectos. **No fusionar:** conflicto de fusión + quita el
  dock de todo el sitio (decisión de Cesar pendiente) + 2 defectos P1 nuevos
  de revisión de código (estado de adelantos: se habilitan todos los botones
  sin comprobar que cada título tenga audio; numeración: `index + 1` sobre el
  conjunto filtrado cambia al buscar/filtrar).
- **`/nuevo/`:** 37 páginas reconstruidas con la dirección editorial (oscuro +
  terracota + Inter), dock responsivo restaurado, hoja ampliada del reproductor,
  5 pestañas móviles, embeds y créditos. Último commit en main 00:00 (21 nov).
  Hallazgos de QA del despliegue de las 05:41 (pueden haber cambiado): skip-link
  2.26:1 en interiores, línea `dz-song-context` oculta por CSS, sin catálogo
  en `/nuevo/`, fetch mutable del HEAD de la rama en el workflow.
- **Cambio de dirección (aprobado por Cesar, 21 nov 05:10Z):** rechazó ambas
  versiones públicas por verse iguales, anticuadas y poco atractivas; aprobó
  abandonar la dirección visual actual. Conservar contenido y funcionalidades
  útiles, no la estética. Nuevo brief: sitio editorial musical contemporáneo
  con identidad específica de Diezell (fotografía documental autorizada como
  protagonista, composición tipográfica editorial, acento con intención, motion
  sutil; evitar el combo negro/rojo/Anton, fondos saturados, cards repetidas,
  carruseles decorativos y estética genérica de IA). Primer hito: validación
  visual del concepto (prototipo de portada), no una expansión de 37 páginas.
- **PR abiertos:** #3 (Música, borrador, conflicto), #4 (fuentes auditables),
  #5 (P1 copy/accesibilidad), #6 (hero 360), #7 (prototipo editorial,
  fusionable). Ninguno fusionado. La rama `actual` tiene el código fuente
  descomprimido; `version-anterior` tiene la v2.0.
- **Rama de recursos:** `muse/recursos-diezell` — 381 archivos verificados
  (sitio completo, 12 imágenes, 13 capturas QA, 2 investigaciones, 26
  colectores, ledger + logs + snapshots, Astro original, revisiones).
- **Corte diario de datos:** el temporizador está activo; el corte de las
  08:00 del 21 nov corrió (63 registros nuevos).
- **Decisiones pendientes de Cesar:** (a) publicar la revisión del PR #3 y la
  respuesta al Issue #1 como comentarios; (b) subir el prototipo «Papel /
  Archivo INSANIA» como enlace público; (c) qué hacer con la barra del
  reproductor (quitarla de todo el sitio o mantenerla fuera de Música).

---

## 11. Dónde está cada cosa

| Recurso | Ubicación |
|---|---|
| Esta guía | `recursos/GUIA-COMPLETA.md` (rama `muse/recursos-diezell`) |
| Índice de recursos | `recursos/README.md` |
| Fotos: fuente y permiso | `recursos/fotos.md` |
| Investigación de la banda | `recursos/investigacion/diezell-banda-20261108.md` |
| Auditoría de diseño moderno | `recursos/investigacion/diezell-rediseno-moderno-20261108.md` |
| Colectores + auditoría + imposibles | `recursos/automatizacion/` (`AUDIT.md`, `NO_SE_PUEDE.md`, `README.md`, 26 scripts) |
| Ledger, comentarios, menciones | `datos/ledger/ledger.json`, `comments.json`, `commenters.json`, `mentions.json` |
| Logs y snapshots por corte | `recursos/datos/ledger-runs/`, `recursos/datos/ledger-snapshots/` |
| Datos por canción | `datos/canciones.json` (27 canciones, duraciones, stats, 8 fragmentos) |
| Lista de reproducción | `audio/playlist.json` |
| Proyecto Astro original | `recursos/astro-original/` |
| Revisiones (PR #3, PR #7, Issue #1) | `recursos/revisiones/` + `workspace/diezell-publish/revision-pr3.md`, `revision-pr7.md`, `respuesta-issue1.md` |
| Capturas QA (antes/después, PR #3, /preview/, /nuevo/, hero 360) | `docs/capturas/`, `docs/capturas-pr3/`, `workspace/diezell-publish/capturas-*/` |
| Prototipo nueva dirección visual | `workspace/diezell-publish/direccion-visual/` (prototipo, `REPORTE.md`, capturas) |
| Sitio local (editable) | `workspace/diezell-html/` (37 páginas, `datos/`, `automatizacion/`) |
| Respaldos | `workspace/diezell-backups/v2.0-2026-11-17/`, `v2.1-2026-11-18-audio/`, `v2.2-pre-reestructuracion-2026-11-20/` |
| ZIP desplegados | `workspace/diezell-publish/parte-1.zip`, `parte-2.zip`, `parte-3.zip` |

**Repositorio:** https://github.com/cesargtz1055/diezell-web — **Issue #1** es el
canal principal de coordinación. **Sitio en vivo:**
https://cesargtz1055.github.io/diezell-web/
