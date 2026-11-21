# Recursos Diezell — todo el material, aunque no se muestre

Rama `muse/recursos-diezell`: el sitio completo descomprimido de la rama `actual`
(37 páginas, CSS, JS, playlist, datos) **más** todo el material de investigación,
datos y auditoría que existe fuera del sitio publicado. Nada aquí se publica
en la web: es material de trabajo para decidir cómo usarlo.

## Dónde está cada cosa

| Recurso | Ubicación | Notas |
|---|---|---|
| Sitio completo (37 páginas) | raíz de esta rama | De `actual`: HTML, `styles.css`, `app.js` |
| Imágenes (12 JPG) | `images/` | Portadas oficiales + fotos en vivo. Ver `recursos/fotos.md` |
| Adelantos de audio (27 previews de 90 s) | `audio/previews/` dentro de `parte-2.zip` y `parte-3.zip` | Con permiso de la banda; solo previews, no masters |
| Lista de reproducción | `audio/playlist.json` | 27 canciones con preview, YouTube, Spotify |
| Datos por canción | `datos/canciones.json` | 27 canciones: duraciones, stats, fragmentos verificados |
| Ledger (histórico append-only) | `datos/ledger/ledger.json` | 643 registros a 20 nov 2026, por fecha de corte y fuente |
| Comentarios y comentaristas | `datos/ledger/comments.json`, `commenters.json` | 439 comentarios, 363 autores (YouTube) |
| Menciones | `datos/ledger/mentions.json` | |
| Investigación de la banda | `recursos/investigacion/diezell-banda-20261108.md` | Verificada 8 nov 2026: historia, integrantes, discos, enlaces oficiales |
| Auditoría de diseño moderno | `recursos/investigacion/diezell-rediseno-moderno-20261108.md` | 8 nov 2026: Sleep Token, BMTH, Bad Omens, Linkin Park, Deftones, etc. |
| Colectores y auditoría | `recursos/automatizacion/` | 26 colectores deterministas, `AUDIT.md`, `NO_SE_PUEDE.md`, `README.md` |
| Logs de cada corte diario | `recursos/datos/ledger-runs/` | Un log por ejecución del ledger |
| Capturas crudas por corte | `recursos/datos/ledger-snapshots/` | Respuestas de Deezer/YouTube/RSS por fecha (2026-11-18/19/20) |
| Proyecto Astro original | `recursos/astro-original/` | `src/`, `public/`, config y preview de una página (sin `node_modules` ni `dist`) |
| Revisiones y coordinación | `recursos/revisiones/` | Revisión del PR #3, comentarios de ChatGPT en Issue #1 y PR #7 |
| Fotos: fuentes y permisos | `recursos/fotos.md` | Las 12 imágenes con autor, fuente, fecha y estado de permiso |
| Capturas de QA | `docs/capturas/` | Antes/después del arreglo móvil (20 PNG) |

## Qué NO está aquí, a propósito

- **Masters de audio completos (`audio/full/`, 91 MB):** la banda dio permiso para
  usar las canciones con límite de 1:30 y botón a la completa en Spotify/YouTube.
  Los masters nunca se publican ni se suben al repo. Solo los previews de 90 s.
- **Notas personales de Cesar** (briefings, validaciones, entrevistas): son del
  propietario, no de la banda. No se suben.
- **Letras completas:** solo fragmentos cortos verificados (8 en `datos/canciones.json`
  y en las fichas). Las letras completas necesitan licencia.

## Reglas que rigen este material

- No inventar datos, letras, permisos ni funciones. Lo dudoso va marcado
  "por confirmar" (ej. bajista: la evidencia apunta a Mau Batarse, pero su
  nombre completo no está publicado; José Aguilar solo aparece en la Wikipedia
  borrada el 17 jul 2026 — no enlazarla).
- Los totales de streams nunca cuadran entre fuentes (Viberate 9.7M vs
  Music Metrics Vault 5.5M): mantener etiquetas de fuente, no promediar.
- Crédito de foto ≠ permiso. Ver `recursos/fotos.md` antes de ampliar usos.
- El ledger es append-only: nunca se reemplaza un dato, siempre se almacena
  con fecha de corte.
