# Diezell · Auditoría editorial, UX y funcional · Dirección aprobada
Fecha: 2026-11-20. Estado: hallazgos por lectura de fuentes en rama `actual`, no prueba visual exhaustiva ni aprobación de datos.

## Principio
Modernizar **sin borrar las 37 páginas, 27 fichas de canción, audio, archivo, fuentes ni historial**. El prototipo `/nuevo/` es la referencia visual. **80 % de esfuerzo de diseño/QA para móvil 360 y 390 px**, 20 % para desktop. Material Design se adopta como sistema de decisiones (jerarquía, superficies, estados, accesibilidad), no como plantilla visual.

## Hallazgos comprobados
1. **Portada** (`index.html`): H1 `DIEZELL`; H2 sucesivos `INSANIA — 2025`, `La banda sobre el escenario`, `Caóticos unidos, jamás serán vencidos`, `La banda sigue creciendo`. La secuencia salta de álbum a fotos, lema comunitario y analítica sin una narrativa de descubrimiento consistente. La portada nueva debe ordenar **identidad → escuchar música → explorar álbumes → conciertos → banda/archivo**. La analítica de crecimiento no debe competir con música como CTA principal.
2. **Música** (`escuchar.html` en `actual`): H1 Música y primer H2 `Reproductor`, después INSANIA, Caótico y Sencillos. Esto prioriza el instrumento de reproducción sobre el contenido. Nuevo orden recomendado: **hero editorial Música → búsqueda/catálogo y filtros → álbumes/sencillos → reproductor contextual**, preservando controles accesibles. El PR #3 ya aborda parte del problema; reutilizar su lógica corregida, no fusionar su estética ni su workflow antiguo.
3. **En vivo** (`en-vivo.html`): `Diez fotos en vivo`, `El video`, `Insania Tour 2026 · Archivo`. Encabezados centrados en formatos, no en necesidades del visitante. Reorganizar: **archivo de conciertos → registros destacados con fecha/fuente → galería → video**; diferenciar conciertos pasados de futuros, sin insinuar agenda vigente cuando no hay fuente actual.
4. **Banda** (`banda.html`): H1 Banda y H2 para cuatro integrantes, después `La banda sobre el escenario`, `Historia`, `Prensa`, `Datos curiosos`. Reordenar: **quiénes son → integrantes → historia cronológica → prensa/fuentes**. Evitar repetir galerías de la portada y `En vivo` sin una razón editorial.
5. **Caóticos** (`caoticos.html`): H1 es el lema `Caóticos Unidos Jamás Serán Vencidos`; H2 ritual de luces, cuentas de fans y aniversario. Añadir un encabezado semántico identificable `Caóticos` con el lema como subtítulo; explicar en el primer viewport qué significa y por qué existe esta sección. No utilizar `Unirme` ni prometer registro/club administrado si no existe.
6. **Crecimiento** (`crecimiento.html`): H1 `Diezell en números`; H2 oyentes, seguidores, movimientos diarios, menciones y comentarios. La página necesita **fecha de actualización, procedencia y estado de los datos** junto a cada métrica; si están desactualizados, etiquetar `Última actualización verificada`, no simular tiempo real. Sin rankings de personas basados en datos no auditables.
7. **Fichas** (muestra `canciones/suspension.html`): H1 canción; H2 `Escuchar`, `Sus números`, `INSANIA`. Ordenar **título + álbum + acceso a reproducción → contexto verificado y créditos → fuentes → métricas fechadas**, sin reproducir letras completas. Conservar enlaces a canciones anterior/siguiente y controles de audio.
8. **Estética y estructura**: el sistema previo mezcla texturas, contraste de hueso/rojo y Anton con la nueva portada oscura/lima. La capa `site-modern.css` es un puente de migración, **no una garantía de acabado**: hay que inspeccionar selectores, estados y layouts por plantilla; no declarar finalizadas 37 páginas solo porque reciben CSS.

## Arquitectura editorial / navegación
Navegación primaria móvil: **Inicio · Música · En vivo · Banda · Caóticos**. El archivo histórico y estadísticas se descubren por rutas secundarias contextuales. Etiquetas consistentes: usar `En vivo` o `Conciertos` en todos los encabezados y enlaces, no alternarlos sin criterio. El menú móvil abre/cierra, cierra con Escape y navegación, y mantiene foco visible. Todos los controles táctiles mínimo 48 × 48 CSS px cuando sea viable.

Plantillas reutilizables:
- Portada: hero, accesos prioritarios, música destacada, en vivo, historia, footer.
- Música: portada editorial, búsqueda, filtros, resultados, álbum, reproductor único.
- En vivo: línea temporal, eventos verificados, galería contextual, videos autorizados.
- Banda/Caóticos: presentación, narrativa, personas o comunidad, fuentes.
- Canción: título, álbum, escucha, créditos, contexto, enlaces y fuente.
- Datos: resumen fechado, gráficas accesibles, procedencia y estados sin datos.

## Reglas de contenido
- Un H1 significativo por página; H2 por sección y H3 por tarjeta cuando tenga contenido subordinado.
- CTA con verbo y destino real: `Explorar canciones`, `Ver conciertos registrados`, `Conocer a la banda`; evitar `Ver más`, `Descubre la magia`, `Únete` si no hay función.
- Nunca afirmar `oficial`, `en vivo ahora`, `próximo concierto` ni datos biográficos/fechas sin fuente verificable.
- Créditos de fotos y permisos documentados; atribución no sustituye licencia.
- Metadata única por página, títulos descriptivos, canonical correcta cuando proceda, OG y alt que describan la función de cada imagen.
- Reproductor: un único audio activo; errores legibles; botones deshabilitados cuando falta pista; sin reproducción automática.
- En móvil: evitar barras fijas que tapen CTAs, scroll horizontal y doble columna ilegible; filtros desplazables con indicación de scroll; espacio inferior para dock si existe.

## Criterios de aceptación antes de reemplazar producción
1. Pruebas de 360/390/768/1440 para portada, música, concierto, banda, Caóticos, estadísticas y al menos dos fichas; capturas comparativas.
2. Revisión manual de teclado, foco, Escape, contraste WCAG AA, zoom 200 %, reduced-motion, alt y H1/H2.
3. Links internos sin 404, 27 fichas accesibles, filtros/búsqueda estables, playlist 404/vacía/tardía con fallback.
4. Verificar que /, /preview/ y /nuevo/ siguen separados; ZIPs y commits intactos.
5. Aprobar recursos y revisar fechas/cifras antes de presentar el resultado como sitio definitivo.

## Reparto
**ChatGPT:** arquitectura editorial, guía de copy, revisión visual y cambios coordinados en el sistema global de /nuevo/.
**Muse:** auditar páginas/plantillas y estados reales en navegador, proponer mejoras por sección y corregir errores funcionales existentes en sus PR sin colisiones con la capa de diseño. Priorizar pruebas móviles y entregar capturas + URLs + lista de fallos.
