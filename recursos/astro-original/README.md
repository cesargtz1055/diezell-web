# DIEZELL — Web de fans (Astro real)

Web de fans **no oficial** de DIEZELL, banda de Monterrey, Nuevo León.
Astro 5 + Tailwind CSS 4. Sin React. JavaScript vanilla en islas mínimas
(pestañas de discografía, cuenta regresiva, menú móvil, reveal al scroll).

## Diseño — INSANIA / VINVSNI 2026 + Material Design 3

Material Design 3 (Material You) es el **sistema**; Diezell es la
**identidad**. Nada de plantilla genérica de Google: la paleta, el hero
tipográfico 100vh, el VINVSNI y las portadas recreadas siguen siendo Diezell.

### Tokens de color M3 (`src/styles/global.css`, Tailwind v4 `@theme`)

Tema oscuro, un solo acento (rojo Diezell, sin colores nuevos):

| Rol M3 | Valor | Uso |
|---|---|---|
| `primary` | `#E8AFAF` (tono claro del rojo Diezell) | CTAs filled, indicador de tabs, enlaces clave |
| `on-primary` | `#3A0B0B` | Texto sobre primary |
| `primary-container` / `on-primary-container` | `#5E1515` / `#F6D9D9` | Chips de estado, selección |
| `inverse-primary` | `#8E1B1B` (rojo original) | Acento sobre superficie inversa (Tour) |
| `secondary` / `on-secondary` | `#C9C9C4` (hueso) / `#171715` | Acento secundario |
| `secondary-container` | `#2E2E2A` | Botones tonales, indicador de nav |
| `surface` / `on-surface` | `#0A0A0A` / `#F2F0EB` | Fondo y texto principal (contraste ~15:1, AA) |
| `surface-container-low → highest` | `#111110` → `#2F2F2C` | Tarjetas y app bar por elevación |
| `on-surface-variant` | `#C9C9C4` | Texto secundario (contraste ~11:1) |
| `outline` / `outline-variant` | `#757570` / `#2A2A2A` | Bordes y divisores de 1px |
| `error` | `#FFB4AB` | Solo estados de error |

Todos los componentes usan estos tokens (`bg-surface`, `text-on-surface`,
`border-outline-variant`…); no hay hex sueltos fuera de `global.css`.

### Escala tipográfica M3

Clases en `global.css`: Display Large/Medium/Small, Headline
Large/Medium/Small, Title Large/Medium/Small, Body Large/Medium/Small,
Label Large/Medium/Small — con tamaño, peso, interlineado y tracking M3.
**Fraunces solo para Display/Headline; Archivo para Title/Body/Label.**
Un Display por pantalla; el resto, Title/Body/Label.

### Forma, elevación y motion M3

- Shape scale: xs 4px, sm 8px, md 12px, lg 16px, xl 28px, full 999px.
  Tarjetas 12–16px, botones filled con forma full, chips 8px.
- Elevación 0–5 (sombra + tinte de superficie): Nav nivel 2, tarjetas de
  discos nivel 2, stats y sencillos nivel 1. Sin bordes gruesos.
- Motion: easing enfatizado `cubic-bezier(0.2,0,0,1)`, 200–500 ms, reveal
  fade + slide corto. Flip INSANIA/VINVSNI en 500 ms (máx. 3 usos).
  `prefers-reduced-motion` desactiva reveal, flip, marquee y skeleton.

### Componentes M3 reales

- **Botones:** Filled (CTA primario: Escuchar / Boletos), Tonal
  (secundario), Outlined (terciario), con state layers hover 8% / focus
  12% / pressed 12%, mínimo 48dp, forma full.
- **Chips:** Sold out (primary-container), Ya pasó (muted, atenuado),
  Próximo (botón filled), TBA (outlined).
- **Tabs primarias** en Discografía: indicador animado de 3px,
  `role="tablist/tab/tabpanel"`, `aria-selected`, navegación por teclado
  (flechas ←/→, Home, End) y `tabindex` gestionado.
- **Navegación:** Top App Bar M3 en escritorio (surface-container,
  elevación 2) + Navigation Bar M3 inferior en móvil (4 destinos con
  indicador activo en pill secondary-container).
- **Tarjetas:** Filled / Elevated / Outlined según jerarquía.
- **Divisores:** 1px `outline-variant`.

### UX / accesibilidad

- Skip link “Saltar al contenido”, landmarks (`header/nav/main/section/
  footer`), un solo `h1`, `aria-labels` en embeds, countdown con
  `aria-live="polite"`, menú móvil con `aria-expanded`, tabs y nav con
  estados ARIA.
- Objetivos táctiles mínimo 48dp en botones, tabs, links de tour y nav.
- Focus visible: outline 2px `primary`.
- Embeds con skeleton M3 y enlace de fallback si no cargan; countdown con
  estado “ya pasó”; fechas pasadas atenuadas y sin CTA.
- Layout M3: márgenes 16px móvil / 24px tablet / 32px escritorio,
  max-width 1280px, espaciado en múltiplos de 4/8dp, sin scroll horizontal.

### Versos, no jerga clínica

Se quitó toda la jerga de pacientes / autopsia / clínica / expediente
(“Un paciente. Una autopsia emocional”, “Dos discos. Una autopsia”,
“CASO Nº 01”, “casos clínicos”, “expediente abierto”, “estilo
radiografía”, “Autopsia mínima”). En su lugar, las descripciones usan
versos cortos y verificados de las canciones, en lenguaje llano
(desamor, duelo, resiliencia):

- Hero: sin cita. La cita destacada de Suspensión… vive solo en Discografía.
- Discografía: “Dos discos. Para cantar el desamor.” + una cita por álbum
  (“Soy experto en arruinarlo todo.” — El Cuento De Aquel Imperfecto Ser).
- Tracks: solo el número (“01”, “02”…), sin “CASO Nº”.
- Sección Letras: 8 fragmentos (Suspensión…, De Espaldas,
  Conmiseración, Resiliencia + los 4 originales), cada uno con su canción
  y enlace a la letra completa. La única “anatomía” que queda en la web
  es la de la propia letra de Sin Rencores (“Que alguien más ya estudia
  tu anatomía”). El flip INSANIA/VINVSNI se queda: es de la portada,
  no es jerga clínica.

### Fuentes y regla anti-invención (auditoría 10 nov 2026)

Regla: si una frase descriptiva no viene de entrevista, prensa o canción
verificada, no va en la web. Cada cita de prensa va COMPLETA, con contexto
y su fuente corta (medio, fecha, enlace “Leer fuente ↗”):

- INSANIA: “Detrás de INSANIA hay también un proceso largo e íntimo: un año
  entero de reunirse noche tras noche para componer el disco, puliendo cada
  idea hasta darle forma a este concepto tan ambicioso.” — Puro Rock Puro,
  16 dic 2025. Ese mismo artículo dice que el disco explora “la
  vulnerabilidad, la culpa, la nostalgia y el duelo” y marca “una etapa más
  cruda, intensa y emocional”. Su descripción de “casos clínicos /
  autopsia emocional / paciente” es de la prensa, no de la banda, y NO se
  restaura en esta web por decisión del usuario.
- Caótico: “El álbum trae canciones que nos pueden llenar de despecho,
  desilusión, o una forma de sacar todo aquel dolor interno que llevamos en
  el alma.” — Puro Rock Puro, 5 oct 2023. Ese artículo también dice que sus
  influencias “nos pueden transportar a los dosmiles” y que buscan conquistar
  a una nueva generación que no vivió el auge del “emo”.
- Influencias: “Diezell es una banda formada en 2018 en Monterrey,
  influenciada por el pop punk y punk rock… con guitarras que recuerdan a
  bandas de la década de los 90 al 2000 como Panda y División Minúscula.” —
  Follow Control, ene 2024. Verificado por índice de búsqueda el 10 nov
  2026; la página directa devolvió 404 ese día, por lo que la cita se
  conserva con su URL canónica y esta advertencia.
- Letras: solo versos cortos (máx. 2 líneas) con canción y enlace a la
  letra completa. Nunca letras completas (copyright).
- Historia: cada hito lleva su fuente visible (medio, fecha, enlace).
- ELIMINADO por sin fuente trazable (10 nov 2026): “Un año componiendo
  noche tras noche” como hecho suelto (ahora solo como cita completa de
  Puro Rock Puro 16 dic 2025); “Punk rock directo de los 2000” como
  afirmación propia (sustituido por la cita de Puro Rock Puro 5 oct 2023);
  “En Caótico el abandono se explora en tres formas… narrada desde la
  perspectiva de la mascota” (lectura de fans sin fuente de banda/prensa);
  “‘Donde Nada Puede Malir Sal’ está mal escrito a propósito” (intención
  no verificada; ahora solo el hecho observable: así está escrito en
  Spotify, track 9 de INSANIA, y los fans lo usan como frase).

### Portadas reales (10 nov 2026)

Las portadas ya NO son recreaciones en CSS/SVG. Son las portadas oficiales
descargadas de Spotify (vía oEmbed, `open.spotify.com/oembed`), guardadas en
`public/images/` y servidas como archivos locales (nada de hotlink):

| Álbum | Archivo | Tamaño | Origen |
|---|---|---|---|
| INSANIA (2025) | `public/images/insania.jpg` | 640×640, 138 KB | https://image-cdn-fa.spotifycdn.com/image/ab67616d0000b273e5ae0cede2bf07e60d4963bf |
| Caótico (2023) | `public/images/caotico.jpg` | 640×640, 123 KB | https://image-cdn-fa.spotifycdn.com/image/ab67616d0000b273a972099b66378a8a38a8dc97 |

Se probó también la versión 300px (`00001e02`); se usó la de 640px
(`0000b273`, mismo hash de imagen) por ser la mayor que devolvió 200.
**Verificación visual, sí:** INSANIA se vio directamente — fondo gris
claro texturizado, “D I E Z E L L” espaciado arriba, tres paneles
verticales en blanco y negro con esqueletos/anatomía, “VINVSNI”
(INSANIA invertido) abajo. Caótico también — fondo negro, figura
fantasmal en grises y “CAÓTICO” en blanco estilizado. Coinciden con la
descripción verificada en la investigación. En Discografía cada álbum
muestra su `<img>` real con `loading="lazy"`, `aspect-square` y pie
“Portada oficial · Spotify” (en INSANIA, además: “En la portada, INSANIA
aparece invertido”). El SVG genérico de 3 paneles se eliminó por completo
de Discografía. El flip INSANIA/VINVSNI del Hero se queda: es el gesto de
la portada real, no una recreación.

### Sin frases repetidas (10 nov 2026)

Regla: cada frase descriptiva, cita o atribución aparece UNA sola vez en
toda la web, en su sección propia. Inventario verificado con grep en
`dist/index.html`:

| Frase repetida | Aparecía | Quedó (1 vez) | Qué se quitó |
|---|---|---|---|
| “Diez canciones sobre vulnerabilidad, culpa, nostalgia y duelo” | 3× (Escucha, concepto INSANIA, Historia 2025) | Solo en el concepto de INSANIA, en Discografía | En Escucha: “Las diez canciones de INSANIA, el segundo álbum.” En Historia 2025: “INSANIA, su segundo álbum.” |
| “Hace frío aquí, no pude salir.” (con punto, como cita) | 2× (Hero, cita INSANIA en Discografía) | Solo en la cita destacada de INSANIA, en Discografía | Del Hero: ahora dice solo “El segundo álbum. Ya disponible.” En Letras queda únicamente dentro del fragmento de 2 versos (“Hace frío aquí, no pude salir / Cuesta respirar hacia el final”), sin punto, como parte del verso completo |
| “Soy experto en arruinarlo todo.” (con punto, como cita) | 1× como cita + dentro del fragmento de 3 versos en Letras | Solo en la cita destacada de Caótico, en Discografía | Nada que quitar: en Letras vive solo dentro del fragmento completo de 3 versos, sin punto |
| “Puro Rock Puro, 16 dic 2025” (atribución en prosa) | 3× (Escucha, Discografía, Historia 2025) | Solo junto a su cita, en Discografía | En Escucha se eliminó el bloque de prensa completo (la cita vive en Discografía, con enlace “ver cita en Discografía”). En Historia 2025 la fuente se conserva como enlace al mismo artículo, sin repetir la fecha en texto |
| “un año entero de reunirse noche tras noche” (cita de prensa) | 2× (Escucha, Discografía) | Solo en el bloque de prensa de INSANIA, en Discografía | Eliminada de Escucha (ver arriba) |
| Lista de sold-out del marquee | 2× | Se queda: es el loop del marquee (`aria-hidden`), por diseño | Nada; el texto visible normal no repite esa lista |
| Títulos de canciones | En tracklist, top 5 y Letras | Se quedan: son referencias cruzadas en listas, no prosa | Nada; la regla es para frases descriptivas, no para títulos en listas |

### Identidad conservada

- Hero 100vh: DIEZELL gigante + INSANIA que al hacer scroll (o al tocar)
  rota 180° y se lee **VINVSNI** — gesto único, máximo 3 usos en toda la web.
- Cero sellos, cintas, marcos, texturas de papel ni tablas. Una idea por
  pantalla, mucho espacio negativo, móvil primero, sin scroll horizontal.
- Sin reproductor propio: embeds oficiales de Spotify y YouTube.
- Las portadas son las oficiales de Spotify (ver apartado “Portadas
  reales” arriba). No se hotlinkea ninguna foto: no se encontró una foto
  de prensa cuya autoría y sujeto pudieran verificarse visualmente, y no
  se usan CDN de Instagram que expiran.

## Cómo correr

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # genera dist/
npm run preview  # sirve dist/ en local
```

## Despliegue

Sitio 100% estático (`dist/`). Sirve en Netlify, Vercel, Cloudflare Pages
o GitHub Pages: comando de build `npm run build`, directorio de salida `dist`.

## Estructura

```
astro.config.mjs          # Astro + plugin Tailwind (Vite)
src/
  pages/index.astro       # Home: 4 pantallas + archivo
  layouts/Layout.astro    # HTML base, fuentes, script global (reveal + flip)
  components/
    Nav.astro             # Nav fija mínima + menú móvil
    Hero.astro            # Hero 100vh, flip INSANIA/VINVSNI, stats
    Escucha.astro         # Embeds Spotify INSANIA + YouTube + top 5
    Tour.astro            # Lista editorial + countdown a Monterrey 13 nov
    Discografia.astro     # Pestañas INSANIA/Caótico, tracklists exactas
    Letras.astro          # Solo fragmentos cortos, con enlace a la completa
    Banda.astro           # Trío confirmado + bajo por confirmar
    Historia.astro        # Timeline 2015–2026
    Prensa.astro          # Prensa, datos curiosos, fuentes
    Footer.astro          # VINVSNI invertido como marca de agua
  data/diezell.ts         # TODOS los datos verificados en un solo lugar
  styles/global.css       # Tailwind v4 + tokens + reveal/flip/marquee
public/favicon.svg
```

## Datos verificados (8 nov 2026)

- **Caótico** — 29 sep 2023, 11 canciones, 37:56.
  <https://open.spotify.com/album/738DN211pKelLzZTRzIC28>
- **INSANIA** — 28 nov 2025, 10 canciones, 36:46.
  <https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88>
  Títulos correctos según Spotify: “La Paradoja De Tennessee” y
  “Una Triste Mañana de Noviembre” (no las erratas de Letras.com).
- Integrantes confirmados: René Guzmán (voz), José Bernardo “Bernie”
  (guitarra), Emmash Batarse (batería/productor).
- **Bajo por confirmar:** Wikipedia dice José Aguilar;
  la cuenta oficial @diezellmx (2 sep 2026) señala a Mau Batarse.
  Nunca se presenta como definitivo en esta web.
- Insania Tour 2026: 21 ago Aguascalientes (Rocksí), 22 ago Guadalajara
  (C3 Rooftop), 16 oct Toluca, 17 oct Querétaro, 23 oct Puebla, 24 oct CDMX,
  6 nov León, 7 nov San Luis Potosí, 13 nov Monterrey (Foro Corona, 21:00,
  Ticketmaster), Mexicali TBA. Corrección clave: Aguascalientes fue el 21,
  no el 22.
- Stats al 8 nov 2026: Spotify 44,822 oyentes mensuales, YouTube 12.2K,
  TikTok 13.7K, Instagram ~6.9K, Facebook ~10K.
- Letras: solo fragmentos cortos ya citados, con enlace a la letra completa.
  Nunca letras completas (copyright).

Fuentes completas en `src/data/diezell.ts` y en la sección Fuentes de la
web, y en los informes de investigación:

- `../research_notes/diezell-banda-20261108-2310/report.md`
- `../research_notes/diezell-rediseno-moderno-20261108-2326/report.md`

## Por confirmar (no inventado)

- Bajista actual (ver arriba).
- Nombre exacto del primer EP (“La Tormenta Antes De La Calma” vs.
  “La Tormenta Después de la Calma”) y su tracklist.
- Año original de “Insomnio” (2018 según Letras.com, 2021 en Spotify).
- Hora de Toluca (16 oct 2026) y fecha/recinto de Mexicali (TBA).
- Cifras exactas de Instagram/Facebook (metadatos, no perfil abierto).
