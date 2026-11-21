# Dirección visual nueva para Diezell — investigación, prototipo y reporte

**Fecha:** 21 nov 2026. **Alcance:** solo portada, prototipo visual. No se tocó el PR #3,
no se subió nada al repo, no se publicó nada. Servir local con
`python3 -m http.server 8940` dentro de esta carpeta y abrir
`http://127.0.0.1:8940/index.html`.

## 1. Las 3 direcciones investigadas

### A — «Papel / Archivo INSANIA» (ELEGIDA para el prototipo)

**Idea:** la portada del propio álbum como sistema de diseño. INSANIA es papel
gris claro texturizado, «D I E Z E L L» en serif espaciada, tres paneles
verticales con grabados anatómicos en blanco y negro y el título invertido
(VINVSNI). El acoustic session de la banda usa el mismo registro: tipografía
negra sobre fondo hueso con foto en blanco y negro.

**Referencias reales:**
- **Pitchfork** — wordmark y sistema tipográfico de Grilli Type («Walfork»):
  serif que referencia tipografías de periódico y publicaciones musicales de
  los 70, con detalles extravagantes para no perder el carácter rock.
  grillitype.com/case-study/pitchfork
- **Pitchfork, rediseño de Joy Zagar** — reconstruir la experiencia de
  descubrimiento con curaduría editorial al centro, sistema de rejilla
  flexible y lenguaje visual refinado. joyzagar.com/case-studies/pitchfork-website-redesign
- **Crack Magazine** — sitio editorial minimalista: fondo blanco, color solo
  dentro de las imágenes, navegación como encabezado largo y formal.
- **The Fader / Dazed (edición impresa)** — portadas de revista: titular
  serif grande, filetes, índice numerado, fotografía documental protagonista.

**Sistema:** papel cálido `#f3f0e8`, tinta `#1a1712`, un solo acento: azul
petróleo `#0e5a72` muestreado de la luz azul real de las fotos en vivo.
Serif editorial contemporánea (Fraunces, autocontenida) + grotesca de sistema
para etiquetas. Filetes, índice numerado, cita editorial, tabla de gira densa.
Ritmo: bloques amplios (hero, cita) alternados con bloques densos (índice,
tracklist, tabla).

**Por qué encaja con Diezell:** es el lenguaje que la banda ya eligió para su
disco; invierte el problema de raíz (las dos versiones actuales luchan contra
la portada al ser oscuras). Lee «revista de música», no «plantilla de rock».

### B — «Luz azul / Documento en vivo»

**Idea:** las fotos de Balleza como protagonistas: haces cian/azules intensos,
oscuridad, el teléfono de un fan grabando. Fondo oscuro, pero el acento es el
azul real del escenario, no un rojo genérico.

**Referencias reales:**
- **NTS Radio** — oscuro, fotografía protagonista, música primero.
- **Resident Advisor (ra.co)** — editorial oscuro, listados de eventos,
  rejilla fuerte; rediseño 2021 con cambio de dominio.
- **23:59, estudio creativo de RA, por HelloMe** — azul fluorescente elegido
  como «color de las horas del crepúsculo» y referencia a relojes digitales.
  designweek.co.uk (nov 2023).

**Por qué no se eligió:** sigue siendo oscura y, a primera vista, podría
confundirse con las versiones actuales (ambas oscuras). La diferencia
dependería solo del acento y la tipografía. Es el plan B si Cesar quiere
mantener fondo oscuro.

### C — «Fanzine / Collage del tour»

**Idea:** el póster del Insania Tour 2026 como sistema: collage monocromo en
blanco y negro, serif grande «DIEZELL», cintas de papel rasgado con ciudad y
fecha, ilustraciones anatómicas, motivos clínicos. Y la comunidad Caóticos
como materia: cuentas fan, «Malir Sal» como meme, el «santo René Guzmán».

**Referencias reales:**
- **Tradición fanzine punk** — Teal Triggs, «Scissors and Glue: Punk Fanzines
  and the Creation of a DIY Aesthetic», *Journal of Design History* 19(1),
  2006; manifiesto DIY Punk (cut-and-paste, ransom-note type, grano Xerox,
  bordes rasgados).
- **Los zines impresos de Pitchfork, por Chris Panicker** — «templated but
  never monotonous», identidades temporales por artista, experimentación
  (glitch, analógico) como método. the-brandidentity.com, 2026.
- **OMORO, guía de estilo collage** — Dada → punk zine → póster
  contemporáneo; tipografía mixta, capas visibles, bordes rasgados.

**Por qué no se eligió para el prototipo completo:** el collage exige mucha
disciplina para no volverse desorden o punk genérico; funciona mejor como
capa de comunidad que como sistema de un archivo de 27 fichas. Ver §4
(alternativa propia).

## 2. El prototipo (dirección A)

**Archivos:** `index.html` (autocontenido: CSS y JS en línea, sin librerías),
`fonts/` (4 woff2 de Fraunces, 77 KB), `images/` (8 fotos optimizadas),
`capturas/`, `test-capturas.py`.

**Primer viewport (móvil y escritorio):** foto documental (René, luces azules)
+ titular DIEZELL en serif + standfirst con los tres hechos (banda de
Monterrey desde 2018; INSANIA, 28 nov 2025; Insania Tour 2026, 9 ciudades,
cierre 13 nov en Foro Corona) + CTA a Spotify + línea de actividad
verificable («Último concierto registrado: 13 nov 2026 · Foro Corona —
6 de 9 fechas sold out. Sin fechas anunciadas.»). Sin estadísticas
arbitrarias: las únicas dos cifras de la página llevan fecha y fuente
(44,147 oyentes, 1,678,233 reproducciones, corte 15 nov 2026).

**Secciones:** Índice numerado (01 Música, 02 En vivo, 03 La banda,
04 Caóticos, 05 Números) · El disco (portada INSANIA, cita de Puro Rock Puro
16 dic 2025, nota VINVSNI, tracklist de 10 con duraciones, Caótico) ·
El archivo de la gira (tabla de 9 fechas con sold outs, 2 fotos) ·
La banda (trío confirmado, origen del nombre, Follow Control ene 2024) ·
Caóticos (lema «Unidos, jamás serán vencidos», cuentas fan) ·
Diezell en números (2 cifras fechadas) · Footer oscuro con enlaces oficiales
y créditos de fotos.

**Motion:** reveal sutil (fade + 12 px) solo con JS activo y solo si no hay
`prefers-reduced-motion`; sin JS el contenido es siempre visible (mejora
progresiva — esto se corrigió durante las pruebas, ver §5).

## 3. Fotos usadas — fuente, permiso y limitaciones

Todas con crédito visible en su pie de foto. Crédito ≠ permiso: el permiso de
reutilización de las fotos de Balleza y Follow Control no está verificado;
este prototipo las usa solo como demostración de diseño, con su fuente
registrada, igual que el sitio actual.

| Archivo | Contenido | Fuente |
|---|---|---|
| `en-vivo-insania.jpg` | René, luces azules (hero) | Balleza Photography — «Diezell \| INSANIA», Behance, 9 feb 2026 |
| `insania.jpg` | Portada oficial INSANIA | Spotify (portada oficial) |
| `caotico.jpg` | Portada oficial Caótico | Spotify (portada oficial) |
| `en-vivo-monterrey.jpg` | Diezell en Monterrey | Balleza Photography — «Diezell \| Monterrey», Behance, 10 dic 2025 |
| `en-vivo-tims-talvez.jpg` | Foro Tims, «TAL VEZ» | Follow Control, enero 2024 |
| `en-vivo-cantando.jpg` | René + Emmash en batería | Balleza Photography — «Diezell \| INSANIA», Behance, 9 feb 2026 |
| `en-vivo-guitarra-rosa.jpg` | Bernie, guitarra rosa | Balleza Photography — «Diezell \| INSANIA», Behance, 9 feb 2026 |
| `en-vivo-pose.jpg` | René, puño en alto | Balleza Photography — «Diezell \| INSANIA», Behance, 9 feb 2026 |

**No usadas (4):** `en-vivo-bajo-bn.jpg` y `en-vivo-bajo-bn2.jpg` (Mau; se
evitan para no prejuzgar el bajo, «por confirmar»); `en-vivo-foro-tims.jpg`
(duplicaría el tema Foro Tims); `en-vivo-guitarra-tie.jpg` (Bernie bajo luz
roja; reservada para fichas). Las 8 usadas son copias optimizadas (máx.
1200 px, q82; 1,822 → 1,142 KB); los originales están intactos en
`~/workspace/diezell-html/images/`.

## 4. Alternativa propia (mejora del brief)

**A como sistema base + C como «capa Caóticos».** La portada, las fichas de
canción y el archivo usan Papel/Archivo (serio, legible, ordenado); la
sección de comunidad y los materiales de gira usan el lenguaje fanzine
(cinta rasgada con ciudad + fecha, sello «SOLD OUT», tipografía mixta). Un
solo sistema con dos registros: archivo y comunidad. Esto resuelve que la
dirección C sola sería demasiado ruidosa para 27 fichas, y le da a Caóticos
una identidad propia en vez de ser una página más.

Segunda mejora, sin costo: el detalle **VINVSNI** (el título invertido de
INSANIA) como gesto distintivo del sitio — en la portada, en la ficha del
disco y como marca de sección — en vez de un logo inventado.

## 5. Verificación (Playwright + Chromium, `test-capturas.py`)

| Comprobación | Resultado |
|---|---|
| Overflow horizontal 360 / 390 / 768 / 1440 | **0 px en los 4 anchos** |
| Primer viewport 360: H1 411–461 px, CTA 738–786 px (viewport 800) | **CTA visible sin scroll** |
| Primer viewport 390: CTA 713–761 px | **visible** |
| Menú móvil 360 | abre (`aria-expanded=true`), cierra con Escape, Tab llega al skip-link |
| Reduced-motion | `.reveal` con opacidad 1 (sin animación) |
| Peticiones externas | **0** (fuentes e imágenes locales) |
| Peso | HTML+CSS+JS ~33 KB · fuentes 77 KB · imágenes 1,142 KB |

**Defectos encontrados y corregidos durante las pruebas:**
1. El H1 gigante desbordaba la rejilla a 360/390/768 (57/27/46 px). Causa:
   tamaño en `vw` sin límite por columna. Corrección: `clamp()` por
   breakpoint (52 px móvil, máx. 104 px escritorio).
2. El índice envolvía la flecha a una segunda línea. Causa: 4 hijos en una
   rejilla de 3 columnas. Corrección: 4 columnas.
3. La tabla de la gira desbordaba a 360 (min-content ~417 px). Corrección:
   `table-layout:fixed` + columnas proporcionales + guionado (`hyphens:auto`).
   Queda como defecto conocido: a 360 «Aguascalientes» se guiona
   («Aguasca-lientes»). Alternativa si molesta: convertir la tabla en lista
   apilada en móvil.
4. Los `.reveal` dejaban la página en blanco bajo el fold sin scroll (y sin
   JS). Corrección: el estado oculto solo existe cuando JS está activo
   (`html.js .reveal`); sin JS todo es visible.

**Capturas** (`capturas/`): `pagina-{360,390,768,1440}.png` (página completa),
`hero-{360,390}.png`, `menu-abierto-360.png`, `footer-1440.png`,
`tabla-gira-360.png`.

## 6. Auto-evaluación contra los 5 criterios

1. **Diferencia inequívoca de ambas versiones actuales — SÍ.** Fondo papel
   claro frente a negro en v2.0, /preview/ y /nuevo/; serif Fraunces frente a
   Anton e Inter; acento azul petróleo frente a rojo, lima y terracota; sin
   barra inferior fija ni historias circulares; índice editorial en vez de
   accesos rápidos. La portada no comparte ningún token visual con las
   versiones actuales.
2. **Móvil/desktop — SÍ.** Verificado arriba: 0 px de overflow en 4 anchos,
   primer viewport completo a 360/390, menú por teclado, desktop 1440 con
   composición propia de revista (hero en 2 columnas, disco en 2 columnas,
   índice), no un móvil ampliado.
3. **Nada inventado — SÍ.** Todos los datos vienen del informe verificado
   (`research_notes/diezell-banda-20261108-2310/report.md`), de
   `datos.json` (corte 15 nov 2026) y del sitio: fechas de álbumes,
   duraciones, tracklist, fechas y sold outs de la gira, 8 fragmentos de
   letras, cita de Puro Rock Puro (16 dic 2025), origen del nombre (Follow
   Control, ene 2024), cifras con fecha y fuente. El bajo no se nombra; no
   hay fechas futuras; no hay letras completas.
4. **Performance — SÍ.** 0 peticiones externas, sin librerías, JS < 2 KB,
   imágenes optimizadas con `loading="lazy"` salvo el hero (`fetchpriority`).
   Total ≈ 1,25 MB. En producción: WebP/AVIF + `srcset`.
5. **Preservar enlaces / catálogo / archivos / reproductor — SÍ, por
   diseño.** La navegación apunta a las 5 páginas existentes con sus slugs
   actuales (escuchar, en-vivo, banda, caoticos, crecimiento); el índice
   enlaza a las secciones; los CTAs usan las URLs reales de Spotify
   (álbumes y artista). El catálogo de 27 fichas y el reproductor no se
   tocan en este prototipo (es solo portada) y los tokens tipográficos y de
   color están pensados para aplicarse a las 37 páginas sin reescribir su
   contenido. Pendiente para fases posteriores: aplicar el sistema a las
   fichas, al catálogo y al reproductor; verificar el permiso fotográfico
   antes de ampliar usos.
