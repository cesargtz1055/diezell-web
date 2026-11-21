# Diezell — auditoría de regresiones y recuperación funcional

Fuentes inspeccionadas: ramas `version-anterior` (v2, seis páginas), `actual` (37 páginas), `chatgpt/experiencia-musical-ux` (prototipo musical), y reconstrucción independiente `/nuevo/` de `chatgpt/direccion-visual-material-editorial`. Se inspeccionaron directamente `app.js`, `escuchar.html`, `en-vivo.html`, `index.html`, `banda.html`, `crecimiento.html`, ejemplos de fichas y scripts de compilación.

## Principio innegociable
Cambiar el diseño no autoriza eliminar funcionalidades, registros, fuentes ni navegación. Cualquier sustitución debe mantener una capacidad equivalente o mejor, no solo su apariencia.

## Recuperaciones implementadas en /nuevo/
| Capacidad valiosa | Origen | Regresión del primer rediseño | Restauración |
|---|---|---|---|
| Minirreproductor inferior en las páginas | v2 y actual | Se dejó un div `#dz-dock` oculto, eliminando los controles | Barra visible con portada, título, reproducción y siguiente, en las 37 páginas |
| Ampliar el reproductor desde su portada | Original `dock-ir` saltaba al reproductor principal | El control inferior desapareció | Vista completa tipo hoja modal, con cerrar, foco, anterior/siguiente, progreso y plataformas |
| Audio único, 90 s y CTA al finalizar | `app.js` de actual | Motor residual sin interfaz de acceso universal | Se reutiliza un solo elemento `audio`, se mantiene `PREVIEW_LIMIT_SECONDS=90` y CTA dentro de la vista ampliada |
| Navegación fija inferior de cinco accesos | v2 y actual | Se eliminó en /nuevo/ | Inicio, Música, En vivo, Caóticos y Banda en móvil |
| Portadas únicas y respaldo DZL | v2 y actual | Imágenes/badges superpuestos | Respeto explícito de `[hidden]` y portadas no duplicadas |
| Reproductores integrados INSANIA y Caótico | actual | Reemplazados por texto | Se abren opcionalmente mediante `details`, y el iframe Spotify solo carga al expandir |
| Listas completas por álbum en fichas | actual (27 fichas) | Se redujeron a enlaces relacionados | Tracklists completos reintroducidos en desplegables, conservando navegación directa |
| Créditos originales de fotos, fechas y fuentes | v2 y actual | Pies simplificados, sin fotógrafo ni contexto | Desplegables con créditos y enlace de origen |
| Diez fotos del archivo En vivo | actual | Solo ocho en /nuevo/ por un selector que ignoraba los `figure` con ID | Se recuperan las diez y se preservan `#foto-tims`, `#foto-monterrey`, `#ultimo-show` |
| Fotos y enlaces rápidos en Home | v2 | Se perdió acceso directo a recuerdos específicos | Una pequeña selección de momentos con enlace a su foto y crédito |
| Ranking de ciudades y canciones con fecha | v2 `banda.html` | Se descartó al rediseñar estadísticas | Se mueve a En cifras, con notas claras sobre los cortes del 8 y 15 nov 2026 |
| 27 canciones, 4 integrantes, giras, prensa y datos | actual | Riesgo de pérdida al sustituir HTML | Scripts de compilación migran las fuentes originales y validan conteos |

## Comportamientos y límites
- La canción seleccionada se recuerda al cambiar de página mediante almacenamiento de sesión; la reproducción **no continúa sin interrupción** a través de una navegación HTML tradicional. No prometer reproducción continua sin crear una arquitectura que mantenga un único documento.
- El modal ampliado es una segunda **interfaz** sobre el mismo audio, **no otro reproductor**.
- No cargar Spotify ni reproducir adelantos automáticamente.
- Si fallan los archivos de música, mostrar un estado comprensible y enlaces válidos, sin texto técnico o rutas internas.
- La atribución de una fotografía **no prueba autorización de uso**. Revisar permisos de los recursos antes de aprobar uso final.
- El archivo completo y la versión original continúan aislados en `/`. Los cambios están solo en `/nuevo/`.

## Validación automatizada integrada
En GitHub Actions: existencia de 37 páginas; 27 fichas con una sola fuente de audio; 4 perfiles; 10 fotos y créditos; los dos iframes restaurables; dos álbumes; enlaces profundos; documento con un H1; ausencia de decoraciones heredadas; recursos locales, vínculos internos y navegación. La compilación fallará si se pierde una de estas capacidades.

## Validación pendiente en navegador real
- Móvil 360 y 390 px: barra sin superposiciones, navegación inferior, scroll, vista ampliada sin contenidos cortados y cierre con Escape/tacto.
- Adelanto de cada álbum; reproducir/pausar; anterior/siguiente; seek con teclado; CTA exactamente a los 90 s; error de MP3 faltante.
- Cambio de página: recordar canción y no comenzar audio sin interacción.
- Apertura voluntaria de cada embed de Spotify; reproducciones simultáneas; cierre y enlaces externos.
- Fotos, créditos y anclas; contraste AA, zoom 200 %, reduced-motion y lector de pantalla.
- El build exitoso **no equivale** a pruebas reales en Chrome Android / Safari iOS.

## No recuperar sin justificación
- Decoraciones de tres rayas, textos de sistema, rankings sin procedencia, afirmaciones históricas inventadas o un segundo audio independiente.
- Fragmetos de letras si no hay permiso de reproducción. Es suficiente enlazar a la fuente.
- Formularios o secciones dependientes de aportaciones de fans cuando no existe una operación editorial que pueda mantenerlos.
