# Diezell — sitio de fans

Sitio de fans de Diezell (Monterrey), 37 páginas reales, sin una sola página.

- **Vivo:** https://cesargtz1055.github.io/diezell-web/ (rama `main`, deploy con GitHub Actions)
- **Ramas:** `main` = versión actual (reestructura del 20 nov 2026, 37 páginas). `version-anterior` = v2.0, 5 páginas, el diseño que le gustaba a Cesar (historias de accesos rápidos, tira de datos en inicio, botón de Spotify). `actual` = versión actual descomprimida (HTML/CSS/JS legibles, commit `8417cef`) para auditoría.
- **Comparar vieja → nueva:** https://github.com/cesargtz1055/diezell-web/compare/version-anterior...main
- **Coordinación:** Issue #1 — https://github.com/cesargtz1055/diezell-web/issues/1

## Coordinación Muse ↔ ChatGPT

Cesar pidió que Muse y ChatGPT se coordinen por este repo. Reglas:

- Nadie empuja directo a `main` sin revisar. ChatGPT trabaja en ramas `chatgpt/<tema>`; Muse revisa e integra.
- La comunicación entre ambos es por mensajes de commit, ramas, issues y este archivo.
- El sitio vivo se publica desde los zips (`parte-1/2/3.zip`) con el workflow `.github/workflows/deploy.yml`. Texto (HTML/CSS/JS/JSON) se puede subir por push; binarios (MP3/JPG) solo por zip en la web de GitHub.

## Último arreglo (20 nov 2026, commit `daf6b50`)

Hero móvil con la foto grande (se quitó el abanico de tarjetas inclinadas), títulos de canciones visiblemente tocables (subrayado + ›), historias de accesos rápidos de v2.0, tira de datos en inicio (44,147 / 16,534 / 1,678,233), botón de Spotify en INSANIA, palabras pegadas corregidas con `&nbsp;`, nombres de integrantes sin partirse, y mensaje de error si no cargan los datos en Números.

## Defectos conocidos en móvil (verificados 20 nov 2026)

1. ~~Hero: en móvil la foto grande se oculta y sale un abanico de 5 tarjetas inclinadas y recortadas.~~ **Arreglado en `daf6b50`.**
2. ~~Páginas de canciones no se encuentran: en Música los títulos parecen texto normal.~~ **Arreglado en `daf6b50`.**
3. ~~Historias: en móvil es una tira horizontal con scroll, no se ven las 4 juntas.~~ **Arreglado en `daf6b50` (vuelven los accesos rápidos).**
4. ~~Palabras pegadas en títulos: "SERÁNVENCIDOS", "JOSÉ BERNARDO"BERNIE"", "EMMANUEL BATARSE("EMMASH")", "Foro Tims.Puro Rock Puro".~~ **Arreglado en `daf6b50`.**
5. **Integrantes sin foto, solo iniciales (RG, JB, EB, MB).** Sigue abierto: no hay retrato individual verificado de Emmash ni de Bernie.
6. ~~Modal de historia: el pie con el crédito queda cortado.~~ **Sin efecto en `daf6b50` (se quitaron los modales del inicio).**
7. ~~Números: la página muestra "Cargando…" hasta que cargan los datos; sin red queda vacía.~~ **Arreglado en `daf6b50` (mensaje de error si falla la carga).**

## Reglas duras

- Adelantos de audio: máximo 90 segundos por canción (`PREVIEW_LIMIT_SECONDS = 90`). Los masters completos NUNCA van al repo ni al sitio público.
- No inventar datos ni descripciones. Solo entrevistas/prensa real o las canciones mismas. Letras: solo fragmentos cortos.
- No enlazar Wikipedia (el artículo de Diezell fue borrado). El bajista es Mau Batarse "por confirmar"; no inventar su nombre completo.
- Nunca reemplazar datos: el ledger es append-only, un registro por fecha de corte.
