## Muse — primera aportación de programación y diseño lista para revisar

Implementé una propuesta concreta y extensa (no solo comentarios): **PR borrador #3** → https://github.com/cesargtz1055/diezell-web/pull/3

El propietario señaló explícitamente tres problemas: **demasiados reproductores sin diferencia clara, portada duplicada en el reproductor y ausencia de una navegación visible hacia las fichas**. La solución que preparé elimina la competencia entre componentes y reorganiza Música como una experiencia editorial. Hay código nuevo en `escuchar.html`, `styles.css`, `app.js`, `music-catalog.js`, workflow de CI y auditoría con criterios QA.

### Lo que ya programé personalmente
- Hero editorial de alto impacto, no interfaz genérica tipo plantilla.
- Catálogo único de 27 fichas con búsqueda tolerante a acentos, filtros y enlaces a las páginas existentes.
- Botón «Adelanto 1:30» por canción, conectado al único reproductor mediante `DZ_REPRODUCIR`.
- Eliminados dos embeds de Spotify y la lista de pistas redundante; dock móvil oculto para evitar la imagen repetida.
- Mejoras visuales globales para fichas de canción, teclado, foco, movimiento reducido, estados vacíos y error de audio.
- CI que compila desde los ZIP originales más el código versionado, **sin publicar en PR**; en el PR se genera `diezell-ux-preview`, y se ejecutan comprobaciones de sintaxis y enlaces.

### Coordinación: qué necesito de ti ahora
1. **No crees un segundo reproductor ni reintroduzcas los iframes.** Revisa el PR #3 y sus criterios; propón ajustes visuales específicos si encuentras algo mejor.
2. Prueba el preview del PR en 360/390/768/1440 px y verifica, con evidencias, las 27 fichas, preview, filtros, accesibilidad y ausencia de imagen duplicada. El workflow ya completó con éxito los pasos de desempaquetado, overlay y validación técnica; falta la revisión visual.
3. Dime si alguna página existente usa el dock para algo esencial no contemplado, para corregirlo antes de integrar.
4. Identifica con evidencia si el usuario se refería a **fichas de canciones/álbumes** o a **productos de merchandising**: no inventemos una tienda ni productos. Si existen artículos oficiales verificables, proponlos como un módulo aparte.
5. Continúa investigando la autonomía del contenido, pero sin añadir secciones superficiales ni datos ficticios. Prioriza diseño excelente y UX real.

**No fusionar ni publicar este PR sin aprobación explícita del propietario.** Yo asumo la responsabilidad de revisar y corregir mi propio código; tú puedes cuestionar las decisiones, validar la propuesta y sugerir mejoras concretas en el PR. Documentemos aquí qué queda confirmado y qué sigue sin probar.