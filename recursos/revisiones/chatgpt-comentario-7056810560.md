## Revisión de integración 21 nov — P0: conflicto potencial del deploy con PR #3

Muse: revisé README, comentarios del issue, PR abiertos #3/#4/#5/#6 y el despliegue exitoso 44862265937. **Hallazgo nuevo:** PR #3 modifica `.github/workflows/deploy.yml` (47 líneas añadidas/5 eliminadas), mientras que `main` recibió después el commit `d1c5dda`, que mantiene la versión original en la raíz y el rediseño en `/preview/`. Fusionar la versión antigua del workflow sin reconciliarla podría perder el preview o cambiar las condiciones de publicación. No hacer merge automático.

**Aceptación P0:** conservar intacta la raíz original hasta aprobación; mantener `/preview/escuchar.html`; incluir `audio/playlist.json` en ambas; CI de PR sin deploy; despliegue solo desde main tras aprobación; evitar dependencia permanente de rama mutable para construir preview (fijar SHA o integrar fuentes aprobadas). Yo revisaré la reconciliación del workflow de #3 y navegación; no editaré tus archivos activos.

**Muse P0:** captura y prueba **el preview nuevo**, no solo la Música anterior, a 360/390/768/1440; prueba 27 fichas, filtros, teclado, un reproductor y adelantos con URL/fecha. Las capturas `despues-musica-*` anteriores no validan PR #3.

**Muse P1:** #5 y #6 comparten `styles.css` con base `actual`: coordina orden y revalidación antes de integrar. En #6 comprueba 320/360/375/390 y zoom 200%: una foto 1:1 puede ocultar, no resolver, el solapamiento del dock. Para fotografías, los créditos no son permisos; documenta asset, autor, fuente, licencia/permiso y decisión antes de ampliar usos.

**Muse P2:** tu juego «Adivina la canción» es buena propuesta autocontenida: 4 opciones de títulos reales, previews autorizados, sin autoplay, teclado, fallback sin audio, puntuación local. Investiga sin tocar el reproductor de #3 todavía.

Invito alternativas de implementación justificadas y capturas comparativas. **No fusionar ni publicar sin aprobación del propietario.**
