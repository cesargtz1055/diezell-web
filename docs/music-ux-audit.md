# DIEZELL / Propuesta de experiencia musical — auditoría y criterios QA

Autor: ChatGPT · rama `chatgpt/experiencia-musical-ux` · para revisión de Muse y del propietario.

## Diagnóstico verificable antes del cambio

La vista Música mezclaba (1) reproductor de adelantos propio, (2) barra de reproducción fija con la misma portada en móviles, (3) lista de reproducción adicional, (4) dos embeds externos de Spotify y (5) listas de álbumes y sencillos que eran la única vía visible hacia las 27 fichas. El usuario no distinguía entre descubrir una canción, entrar a su ficha y reproducirla. La portada se duplicaba entre el reproductor principal y el dock móvil. La navegación a las fichas estaba demasiado abajo.

No es un problema de añadir sombra o redondear botones (Material Design). Es un problema de **arquitectura de información, jerarquía, significado de las acciones y exceso de superficies compitiendo por atención**.

## Implementación propuesta (ya programada en esta rama)

1. **Portada editorial** de Música con dirección artística de Diezell, foto existente del concierto, tipografía de alto contraste y dos CTAs inequívocos: explorar canciones y escuchar adelantos.
2. **Rutas visibles** a catálogo, reproductor y álbumes para anticipar el contenido disponible.
3. **Catálogo de fichas** antes del player: 27 enlaces deduplicados, búsqueda tolerante a acentos, filtros por álbum y sencillos, conteo actualizado, tratamiento de ausencia de resultados y botones con acción distinta: “abrir ficha” vs “adelanto de 1:30”. Cada ficha toma su URL y título de los enlaces ya presentes en el HTML; no inventamos discografía.
4. **Una sola superficie de audio visible**: se oculta el dock móvil redundante, se eliminan los dos embeds de Spotify y la lista secundaria de canciones. El único `<audio>` del reproductor existente sigue operativo. El catálogo llama la API `window.DZ_REPRODUCIR(titulo)` para reproducir la canción seleccionada en ese mismo reproductor.
5. **Enlaces oficiales independientes**: Spotify y YouTube siguen disponibles, pero sin incrustar otros reproductores que compitan.
6. **Fichas editoriales**: el CSS mejora el encabezado de las 27 páginas de canciones y sus controles, sin alterar datos o citas.
7. **Usabilidad y accesibilidad**: controles de búsqueda con etiqueta; filtros con `aria-pressed`; resultados anunciados mediante `role=status`; áreas táctiles de al menos 44 px en filtros; enfoque visible; movimiento reducido; progresos del audio anunciados en segundos según su `aria-valuemax=90`; botón play/pausa con etiqueta contextual; estado de error si falla el audio.
8. **CI verificable**: el workflow construye con ZIPs originales y superpone el código fuente revisable. En PR solo entrega artefacto descargable, SIN publicar; solo `main` despliega. Comprobaciones de sintaxis JS, existencia de 27 URLs de fichas y eliminación de embeds duplicados.

## Material / heurísticas de experiencia

- **Jerarquía:** una intención principal por región y CTA claro.
- **Reconocimiento:** las fichas se ven y se filtran sin necesitar conocer los nombres de antemano.
- **Control y libertad:** escuchar en el sitio no lleva a otra app; abrir ficha y escuchar en Spotify son opciones diferenciadas.
- **Consistencia:** controles y estados de reproducción unificados.
- **Prevención de error:** no mostrar controles de adelanto antes de cargar el catálogo; mensaje legible si un audio falla.
- **Accesibilidad:** foco visible, filtros semánticos, navegación por teclado, semántica de lectura y soporte `prefers-reduced-motion`.
- **Identidad:** uso de rojo profundo, gris hueso, Anton/Archivo y una fotografía ya presente; no se introduce una librería visual genérica ni dependencias de terceros.

## Pendiente de validación manual (no declarar aprobado sin evidencia)

- [ ] Capturas 360, 390, 768, 1024 y 1440 px; verificar que el texto del hero no se superpone a la fotografía ni genera scroll horizontal.
- [ ] Navegar con teclado a filtros, catálogo, fichas, player y enlaces oficiales.
- [ ] Verificar que aparecen 27 fichas sin repeticiones, que los filtros muestran 10 INSANIA, 11 Caótico y 8 menciones de sencillos (6 exclusivos + 2 promocionales ya presentes en álbumes).
- [ ] Pulsar “Adelanto 1:30” desde fichas de cada categoría y comprobar que cambia el tema en el único player.
- [ ] Comprobar audio al minuto y medio, seek, autoplay restringido por navegador y error de archivo faltante.
- [ ] Verificar enlaces internos y portada en GitHub Pages preview descargable del PR antes de integrar.
- [ ] Revisar licencia/reutilización de fotografías y previews; los cambios reusan recursos del sitio, no acreditan por sí mismos permiso.
- [ ] Verificar interacción en Android Chrome, Safari iOS, escritorio y con reduce motion.
- [ ] Comparar con `version-anterior` para asegurar que no se perdieron los elementos aprobados del inicio.

## Decisiones para Muse

1. No desplegar sin capturas y QA. Revisar los cambios en este PR; proponer mejoras visuales **sobre la nueva dirección editorial**, no duplicar reproductores.
2. Confirmar que la versión desplegada y el ZIP base sean consistentes con la rama de fuentes, especialmente `audio/playlist.json`.
3. Revisar la atribución y permiso de los recursos visuales y audios.
4. Proponer una mejora que complemente (no replique) la experiencia: por ejemplo, artículos editoriales bien documentados en cada ficha, accesibles desde el catálogo.

**Estado:** código propuesto en una rama. No fusionado, no publicado y sin pruebas de navegador reales todavía.
