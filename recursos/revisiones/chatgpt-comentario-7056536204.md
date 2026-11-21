## Muse — ya programé una aportación importante: PR #2 (Música)

No es una lista de críticas: **acabo de desarrollar un rediseño integral de la sección Música**, con HTML, CSS y JavaScript reales en una rama aislada. Revisa el [PR #2](https://github.com/cesargtz1055/diezell-web/pull/2) y su diff.

### Dirección de producto
El propietario observó tres problemas graves: no encuentra las fichas de canciones («páginas de productos»), ve demasiados reproductores y percibe duplicación de portadas/imágenes. Coincido: la arquitectura actual no separa explorar, leer y escuchar.

**Mi implementación:** hero editorial de alto contraste y tipografía rock; rutas claras hacia las fichas; catálogo visual de 27 canciones, búsqueda y filtros INSANIA/Caótico/sencillos; enlaces «Ver ficha» y «Adelanto» por tarjeta; un solo reproductor visible en Música; se eliminan los dos iframes Spotify redundantes pero permanecen enlaces oficiales a los álbumes. No se toca el motor global de audio ni main.

### Reparto inmediato
**Yo:** ya entregué `escuchar.html`, `music-experience.css`, `music-catalog.js` y PR de revisión. Mantendré la dirección UX y corregiré hallazgos verificables en mi rama.

**Tú, Muse — P0:** comprueba que cada una de las 27 tarjetas llega a la ficha correcta y que el adelanto reproduce el audio correspondiente. La rama fuente carece de imágenes y previews: prepara una fuente auditable con assets autorizados que permita probar en navegador. Revisa la discrepancia entre el ZIP de main y las fuentes, no hagas merge sin evidencia. Haz capturas a 360/390/768/1440 y documenta problemas reales.

**Tú, Muse — P1:** propón una plantilla de ficha individual realmente atractiva (arte único, créditos, contexto verificado, navegación anterior/siguiente y acciones claras), evitando reproducir un segundo reproductor grande y un dock simultáneamente. Investiga derechos de imágenes y metadatos.

**Criterios de aceptación:** 27 fichas navegables, 0 enlaces rotos, 1 reproductor visible en Música, 0 iframes Spotify duplicados, filtros funcionales, teclado accesible, responsive sin desbordamientos, recursos autorizados. Diferencia hechos probados de tareas pendientes.

Quiero tu revisión crítica del PR: si detectas un problema de diseño, código o datos, indícalo con archivo/línea y propuesta. También espero que propongas una mejora original adicional. **Trabajamos juntos, no en cadena de instrucciones sin criterio.**