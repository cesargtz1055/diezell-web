# Revisión de Muse — PR #3 "Rediseño radical de Música" (ChatGPT)

**Rama:** `chatgpt/experiencia-musical-ux` → `main` · **head:** `edd70fa` · **Estado:** borrador, abierto, con conflicto de fusión (`mergeable: false`).

Verificación en dos capas: estática (código y datos) + interactiva (Playwright, build local con los ZIP desplegados en main + overlay del PR). 13 capturas en `workspace/diezell-publish/capturas-pr3/`.

## Verificación estática — aprobado

- **Datos íntegros.** Los 27 títulos de `escuchar.html` coinciden exactamente con `playlist.json` viva (0 diferencias). El `DZ_FALLBACK` embebido en `app.js` coincide 0 diferencias con la playlist viva (preview, YouTube, videoId, álbum). Los 27 archivos de preview existen.
- **Un solo reproductor.** 0 iframes de Spotify; 1 solo `id="dz-player"`; enlaces oficiales a Spotify/YouTube conservados (2 álbumes + artista), sin incrustar reproductores.
- **Sin regresiones del fix móvil.** El `styles.css` del PR incluye los arreglos de `daf6b50` (hero-foto visible, sin `hero-arc`, títulos de canción subrayados con `›`) y su propio bloque `prefers-reduced-motion: reduce`. El encabezado sigue diciendo "5 pages" (mi PR #5 lo corrige a "37 pages" — detalle de doc, no funcional).
- **`music-catalog.js` no inventa discografía.** Construye el catálogo desde los enlaces HTML existentes; deduplica Suspensión/Gizmo (aparecen también como sencillos); el filtro Sencillos muestra 8 (6 exclusivos + 2 adelantos de INSANIA), tal como ya documenta tu audit doc.
- **`app.js` del PR es superconjunto del actual** (29,454 vs 27,595 bytes): conserva menú, reveal, popovers y historias; añade `DZ_REPRODUCIR` + evento `diezell:playlist-ready`. Ninguna función se pierde.

## Verificación interactiva — 8/8 puntos aprobados, 0 defectos funcionales

- **Catálogo:** 27 tarjetas; contador "27 CANCIONES · TODO EL ARCHIVO".
- **Filtros:** Todo 27 / INSANIA 10 / Caótico 11 / Sencillos 8; `aria-pressed` correcto.
- **Búsqueda:** "suspension" → 1 resultado; "conmiseracion" sin acento → encuentra "Conmiseración"; "zzzz" → 0 resultados y estado vacío visible.
- **Tarjetas → fichas:** 3/3 abren la ficha correcta (Suspensión…, El Cuento…, Sin Rencores).
- **Adelantos:** 3/3 suenan el audio correcto (preview exacto por canción) y el tiempo avanza; el reproductor muestra el título correcto.
- **Teclado:** orden Tab correcto, foco visible (outline rojo 3 px), Enter activa filtros.
- **Visual 360/390/768/1440:** sin scroll horizontal, 0 px² de solape entre texto del hero y foto, dock oculto, 0 iframes, 1 solo `<audio>`, un solo reproductor visible.
- **Caveat:** Google Fonts está bloqueado en esta VM, así que las capturas muestran tipografía fallback, no Anton/Archivo. La tipografía editorial no se verificó visualmente; el layout sí.

## Hallazgos que necesitan ojos (no son defectos)

1. **El dock se retira en TODO el sitio, no solo en Música** (`styles.css:648`, `.player-bar { display: none !important; }`). Y `app.js` solo inicializa el reproductor si la página tiene `#dz-player` (27 fichas + escuchar.html). Respuesta a tu pregunta: sí, 5 páginas usan el dock como su ÚNICO control de audio: Inicio, Banda, En vivo, Caóticos, Números. Tras el PR, desde esas páginas no hay forma de escuchar nada sin navegar a Música o a una ficha. Verifiqué que no queda audio huérfano (al navegar la página recarga y la reproducción se detiene) y que cada página con reproductor sigue funcionando. Pero es una decisión de producto del dueño, no un detalle: el dock era el "escuchar desde cualquier parte". Mi recomendación: que Cesar lo decida explícitamente antes de fusionar. Alternativa: ocultar el dock solo bajo `.music-page` y mantenerlo en el resto.
2. **Conflicto de fusión.** El PR tiene `mergeable: false` ahora mismo. Además `styles.css` lo tocan 3 PRs abiertos (#3, #5, #6) y el del PR #3 es anterior a mis P1 (encabezado "37 pages") y al fix hero-360 (PR #6). El orden de fusión importa: si #3 se fusiona primero, #5 y #6 necesitan rebase; si se fusionan #5/#6 primero, #3 necesita rebase. Propongo resolver el conflicto y rebasear #3 sobre el `actual` más reciente antes de fusionar.
3. **`DZ_REPRODUCIR` empareja por título exacto.** Hoy los 27 coinciden (verificado), pero un cambio futuro de un título rompería el botón de adelanto en silencio (mostraría "no está disponible"). Sugerencia: emparejar por clave estable (slug o número de canción).
4. **`DZ_FALLBACK` duplica `playlist.json`** (~10 KB dentro de `app.js`). Es un buen seguro — es exactamente el bug que rompió el reproductor en vivo — pero es una segunda fuente de verdad que puede divergir. Sugerencia: generarlo desde `playlist.json` en el build, o documentar que ambos se actualizan juntos. No bloquea.
5. **Los botones de adelanto nacen deshabilitados hasta `playlist-ready`.** Si `playlist.json` fallara, quedarían deshabilitados (el código prevé mensaje de error). Correcto; el CI ya verifica que `playlist.json` existe.

## Respuestas a tus 5 puntos

1. **No crear segundo reproductor ni reintroducir iframes:** confirmado, no lo hice. Revisión arriba.
2. **Preview probado a 360/390/768/1440:** 8/8 aprobados, evidencia en `capturas-pr3/`.
3. **Dock:** sí, 5 páginas lo usan como único audio (ver hallazgo 1). Decisión del dueño pendiente.
4. **Fichas vs merchandising:** fichas de canciones. La evidencia es lo que dijo Cesar: "no encuentro las páginas de las canciones". No hay tienda ni productos de merch en el sitio ni artículos oficiales verificados. No inventar tienda.
5. **Contenido:** sigo investigando sin secciones superficiales ni datos ficticios.

## Mis propuestas

- **P1 — plantilla de ficha individual:** las fichas ya existen y el PR mejora su encabezado. En vez de rediseñar la plantilla ahora, propongo algo que complementa: un **"recorrido guiado por INSANIA"** dentro de Música — una secuencia curada de los 10 temas con una línea de contexto verificada por tema (fragmento o cita real), usando el mismo reproductor. Sin nuevos assets, sin datos inventados. Lo programo cuando se fusione #3.
- **Mejora original adicional:** **"Adivina la canción"** (ya propuesta en Issue #1): juego autocontenido con los 27 adelantos — escucha unos segundos y adivina la canción; sin backend, sin datos nuevos. Complementa Música sin duplicar el reproductor.

## Conclusión

El PR está técnicamente sólido: datos íntegros, 0 defectos funcionales en 8/8 pruebas, CI con validaciones correctas. **No fusionar todavía:** (a) resolver el conflicto de fusión, (b) decisión del dueño sobre el dock global, (c) rebase de `styles.css` con P1 + hero-360. Sigue en borrador, sin publicar — como pide el proceso.
