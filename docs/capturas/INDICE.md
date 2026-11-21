# Capturas visuales — Diezell antes/después (20 nov 2026, ~21:15 CST)

Capturadas con Playwright + Chromium headless local (`capturas.py`, `capturas_extra.py`).
Viewport superior de cada página + 4 capturas con scroll.

## DESPUÉS (en vivo, GitHub Pages — versión arreglada)

- `despues-inicio-360.png`, `despues-inicio-390.png`, `despues-inicio-768.png`, `despues-inicio-1440.png`
- `despues-musica-360.png`, `despues-musica-390.png`, `despues-musica-768.png`, `despues-musica-1440.png`
- `despues-musica-lista-390.png` (lista de canciones con scroll)
- `despues-inicio-historias-390.png` (fila de historias con scroll)
- `despues-inicio-datos-390.png` (tira de datos con scroll)

## ANTES (sustituto local — ver nota abajo)

- `antes-local-inicio-360.png`, `antes-local-inicio-390.png`, `antes-local-inicio-768.png`, `antes-local-inicio-1440.png`
- `antes-local-musica-360.png`, `antes-local-musica-390.png`, `antes-local-musica-768.png`, `antes-local-musica-1440.png`
- `antes-local-musica-lista-390.png` (lista de canciones con scroll)

## Nota importante sobre ANTES

La URL real del artefacto (`muse.ai/s/diezell-...`) es **inaccesible desde esta VM**: el
proxy de salida devuelve **403 Forbidden** en el CONNECT a `muse.ai:443` (verificado
con curl y con el navegador; también `http://` da 000). No existen `antes-inicio-*.png`
ni `antes-musica-*.png` del artefacto.

El sustituto `antes-local-*` es el **respaldo v2.2** (`workspace/diezell-backups/
v2.2-pre-reestructuracion-2026-11-20/`), servido en local: mismo HTML/CSS del diseño
previo al arreglo (abanico de tarjetas inclinadas, títulos de canciones en texto
plano). OJO: ese respaldo es pre-reestructura y YA trae los 5 accesos rápidos
(INSANIA, Caótico, Foro Corona, Foro Tims, Monterrey); el artefacto reestructurado
tenía en su lugar 4 círculos de integrantes. La fila de historias NO es, por tanto,
una diferencia antes/después en estas capturas. Las diferencias reales probadas son:
hero (abanico vs foto grande) y títulos de canciones (texto plano vs enlaces
subrayados con ›), más el cambio de etiqueta Escuchar → Música.

## Hallazgos (ver reporte del subagente para el detalle por ancho)

1. Hero DESPUÉS: foto grande sin recortes feos en 360/390/768/1440; rostro visible.
2. A 360 px el subtítulo "El segundo álbum ya suena: INSANIA" queda tapado por la
   barra fija del reproductor al cargar la página (a 390 px sí se ve completo).
3. Música DESPUÉS: 21 títulos subrayados con › (estilo computado: underline);
   ANTES: `<span>` de texto plano, sin affordance de enlace.
4. Fila de historias DESPUÉS a 390 px: tira con scroll horizontal; el 5º círculo
   (Monterrey) queda cortado al borde derecho; etiquetas legibles.
5. Tira de datos DESPUÉS: 44,147 / 16,534 / 1,678,233, legible, con botón
   "DIEZELL EN NÚMEROS →".
6. Barra del reproductor + tabbar apiladas sin encimarse (360/390); ocultas en
   768/1440 (navegación superior).
7. A 1440 px el ANTES también muestra la foto grande (el bug del hero era solo
   móvil/tablet, ≤768 px).
