# Diezell — sitio de fans

Sitio de fans de Diezell (Monterrey), 37 páginas reales, sin una sola página.

- **Vivo:** https://cesargtz1055.github.io/diezell-web/ (rama `main`, deploy con GitHub Actions)
- **Ramas:** `main` = versión actual (reestructura del 20 nov 2026, 37 páginas). `version-anterior` = v2.0, 5 páginas, el diseño que le gustaba a Cesar (historias de accesos rápidos, tira de datos en inicio, botón de Spotify).
- **Comparar vieja → nueva:** https://github.com/cesargtz1055/diezell-web/compare/version-anterior...main

## Coordinación Muse ↔ ChatGPT

Cesar pidió que Muse y ChatGPT se coordinen por este repo. Reglas:

- Nadie empuja directo a `main` sin revisar. ChatGPT trabaja en ramas `chatgpt/<tema>`; Muse revisa e integra.
- La comunicación entre ambos es por mensajes de commit, ramas y este archivo.
- El sitio vivo se publica desde los zips (`parte-1/2/3.zip`) con el workflow `.github/workflows/deploy.yml`. Texto (HTML/CSS/JS/JSON) se puede subir por push; binarios (MP3/JPG) solo por zip en la web de GitHub.

## Defectos conocidos en móvil (verificados 20 nov 2026)

1. **Hero:** en móvil la foto grande se oculta y sale un abanico de 5 tarjetas inclinadas y recortadas. Es lo que más se ve mal.
2. **Páginas de canciones no se encuentran:** en Música los títulos parecen texto normal (el subrayado solo aparece con hover, y en teléfono no hay hover). Hay que hacerlos visiblemente tocables.
3. **Historias:** en móvil es una tira horizontal con scroll, no se ven las 4 juntas.
4. **Palabras pegadas en títulos:** "SERÁNVENCIDOS", "JOSÉ BERNARDO"BERNIE"", "EMMANUEL BATARSE("EMMASH")", "Foro Tims.Puro Rock Puro". Falta espacio en el marcado.
5. **Integrantes:** los nombres en Anton gigante se parten en 2-3 líneas y no tienen foto, solo iniciales (RG, JB, EB, MB).
6. **Modal de historia:** el pie con el crédito queda cortado, hay que desplazar dentro del diálogo.
7. **Números:** la página muestra "Cargando…" hasta que cargan los datos; sin red queda vacía.

## Reglas duras

- Adelantos de audio: máximo 90 segundos por canción (`PREVIEW_LIMIT_SECONDS = 90`). Los masters completos NUNCA van al repo ni al sitio público.
- No inventar datos ni descripciones. Solo entrevistas/prensa real o las canciones mismas. Letras: solo fragmentos cortos.
- No enlazar Wikipedia (el artículo de Diezell fue borrado). El bajista es Mau Batarse "por confirmar"; no inventar su nombre completo.
- Nunca reemplazar datos: el ledger es append-only, un registro por fecha de corte.
