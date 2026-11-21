// ─── DIEZELL · datos verificados ──────────────────────────────────────────
// Fuente: ~/workspace/research_notes/diezell-banda-20261108-2310/report.md
// (investigación 8 nov 2026; verificación en vivo en Spotify, YouTube y TikTok)
// y ~/workspace/research_notes/diezell-rediseno-moderno-20261108-2326/report.md
// (auditoría de diseño moderno).
// No inventar fechas, tracklists ni enlaces: todo lo de aquí viene de ahí.

export const LINKS = {
  spotifyArtist: "https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g",
  spotifyInsania:
    "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88",
  spotifyCaotico:
    "https://open.spotify.com/album/738DN211pKelLzZTRzIC28",
  youtube: "https://www.youtube.com/@diezellmx",
  youtubeVideoCuento: "https://www.youtube.com/watch?v=MuvgZpXqsY8",
  tiktok: "https://www.tiktok.com/@diezellmx",
  instagram: "https://www.instagram.com/diezellmx",
  facebook: "https://www.facebook.com/diezelloficial",
  linktree: "https://linktr.ee/diezellmx",
  wikipedia: "https://es.wikipedia.org/wiki/Diezell",
} as const;

export const STATS = {
  fecha: "8 nov 2026",
  spotifyOyentes: "44,822",
  youtubeSubs: "12.2K",
  tiktokSeguidores: "13.7K",
  instagramSeguidores: "~6.9K",
  facebookSeguidores: "~10K",
} as const;

export interface Track {
  n: number;
  titulo: string;
  duracion: string;
}

export interface Album {
  id: "insania" | "caotico";
  titulo: string;
  fecha: string;
  canciones: number;
  duracionTotal: string;
  spotify: string;
  spotifyEmbed: string;
  concepto: string;
  cita: string;
  // Portada OFICIAL descargada de Spotify (ver README, apartado Portadas reales).
  portada: string;
  portadaAlt: string;
  // Cita COMPLETA de prensa, con atribución visible en la web.
  prensa: { cita: string; medio: string; fecha: string; url: string };
  tracks: Track[];
}

export const ALBUMS: Album[] = [
  {
    id: "insania",
    titulo: "INSANIA",
    fecha: "28 de noviembre de 2025",
    canciones: 10,
    duracionTotal: "36:46",
    spotify: LINKS.spotifyInsania,
    spotifyEmbed:
      "https://open.spotify.com/embed/album/3LGm9FVg9cswGMo5YneJ88?utm_source=generator&theme=0",
    concepto:
      "Diez canciones sobre vulnerabilidad, culpa, nostalgia y duelo.",
    cita: "“Hace frío aquí, no pude salir.” — Suspensión…",
    portada: "/images/insania.jpg",
    portadaAlt:
      "Portada oficial de INSANIA (2025): fondo gris, DIEZELL arriba y tres paneles verticales en blanco y negro; abajo, INSANIA invertido, que se lee VINVSNI",
    prensa: {
      cita: "Detrás de INSANIA hay también un proceso largo e íntimo: un año entero de reunirse noche tras noche para componer el disco, puliendo cada idea hasta darle forma a este concepto tan ambicioso.",
      medio: "Puro Rock Puro",
      fecha: "16 dic 2025",
      url: "https://purorockpuro.com/diezell-presenta-insania-su-segundo-album-de-estudio/",
    },
    tracks: [
      { n: 1, titulo: "Suspensión...", duracion: "3:58" },
      { n: 2, titulo: "Más Que Ayer, Menos Que Mañana", duracion: "3:29" },
      { n: 3, titulo: "Días Felices: Los Lunes", duracion: "3:04" },
      { n: 4, titulo: "Tus Flores Fueron Entregadas", duracion: "3:52" },
      { n: 5, titulo: "El Último Soldado En Pie", duracion: "4:21" },
      { n: 6, titulo: "El Monstruo De Gizmo", duracion: "3:41" },
      { n: 7, titulo: "La Paradoja De Tennessee", duracion: "3:42" },
      { n: 8, titulo: "Resiliencia", duracion: "3:50" },
      { n: 9, titulo: "Donde Nada Puede Malir Sal", duracion: "3:44" },
      { n: 10, titulo: "Una Triste Mañana de Noviembre", duracion: "3:01" },
    ],
  },
  {
    id: "caotico",
    titulo: "Caótico",
    fecha: "29 de septiembre de 2023",
    canciones: 11,
    duracionTotal: "37:56",
    spotify: LINKS.spotifyCaotico,
    spotifyEmbed:
      "https://open.spotify.com/embed/album/738DN211pKelLzZTRzIC28?utm_source=generator&theme=0",
    concepto:
      "Punk rock. Sus influencias, según Puro Rock Puro (5 oct 2023), “nos pueden transportar a los dosmiles”, a una generación que no vivió el auge del “emo”.",
    cita: "“Soy experto en arruinarlo todo.” — El Cuento De Aquel Imperfecto Ser",
    portada: "/images/caotico.jpg",
    portadaAlt:
      "Portada oficial de Caótico (2023): fondo negro con una figura fantasmal en grises y el título CAÓTICO en blanco",
    prensa: {
      cita: "El álbum trae canciones que nos pueden llenar de despecho, desilusión, o una forma de sacar todo aquel dolor interno que llevamos en el alma.",
      medio: "Puro Rock Puro",
      fecha: "5 oct 2023",
      url: "https://purorockpuro.com/diezell-nos-presentan-su-album-caotico/",
    },
    tracks: [
      { n: 1, titulo: "El Cuento De Aquel Imperfecto Ser", duracion: "3:21" },
      { n: 2, titulo: "Conmiseración", duracion: "3:40" },
      { n: 3, titulo: "Martes Con Aroma A Domingo", duracion: "3:14" },
      { n: 4, titulo: "Sin Destinatario", duracion: "3:09" },
      { n: 5, titulo: "Al Parecer Eso Parece", duracion: "3:28" },
      { n: 6, titulo: "Una, Dos O Tres Lágrimas Permitidas", duracion: "4:03" },
      { n: 7, titulo: "A Golpe de Mar, Pecho Sereno", duracion: "3:31" },
      { n: 8, titulo: "De Espaldas", duracion: "3:40" },
      { n: 9, titulo: "Mi Más Sentido Pésame (Murió El Sentido Común)", duracion: "3:06" },
      { n: 10, titulo: "Demencia", duracion: "3:06" },
      { n: 11, titulo: "El Último Recuerdo De La Noche", duracion: "3:31" },
    ],
  },
];

export const TOP_SONGS = [
  { titulo: "El Cuento De Aquel Imperfecto Ser", reproducciones: "1,670,521" },
  { titulo: "Sin Rencores", reproducciones: "1,044,041" },
  { titulo: "Martes Con Aroma A Domingo", reproducciones: "598,427" },
  { titulo: "De Espaldas", reproducciones: "586,078" },
  { titulo: "Suspensión...", reproducciones: "585,675" },
] as const;

export const SINGLES = [
  { titulo: "Insomnio", anio: "2021 en Spotify · 2018 según Letras.com — año original por confirmar" },
  { titulo: "Sin Rencores", anio: "2021 · sencillo debut" },
  { titulo: "El Mejor De Mis Errores", anio: "2021" },
  { titulo: "Tiempos De Un Tiempo", anio: "2021" },
  { titulo: "Muérdago Marchito", anio: "2021 · tema navideño" },
  { titulo: "Hipocresía", anio: "2022" },
  { titulo: "Suspensión...", anio: "2024 · adelanto de INSANIA" },
  { titulo: "El Monstruo De Gizmo", anio: "2025 · adelanto de INSANIA" },
] as const;

export interface Miembro {
  nombre: string;
  rol: string;
  nota?: string;
}

export const MIEMBROS: Miembro[] = [
  {
    nombre: "René Guzmán",
    rol: "Voz",
    nota: "También toca guitarra en vivo. @reneguzman19",
  },
  {
    nombre: "José Bernardo",
    rol: "Guitarra",
    nota: "“Bernie”.",
  },
  {
    nombre: "Emmash Batarse",
    rol: "Batería",
    nota: "También productor; canta segundas voces en vivo. @emmashbatarse",
  },
];

// Bajo: CONFLICTO NO RESUELTO entre fuentes. Nunca presentarlo como definitivo.
export const BAJO_CONFLICTO = {
  titulo: "Bajo — por confirmar",
  texto:
    "El bajo está por confirmar: Wikipedia lista a José Aguilar, mientras la cuenta oficial @diezellmx (2 sep 2026) presenta a Mau Batarse como bajista. En 2023–2024 las fuentes describen a la banda como trío; en 2025–2026 los pósters y videos muestran cuatro integrantes. No hay fuente que feche el cambio.",
  fuentes: [
    { etiqueta: "Wikipedia", url: LINKS.wikipedia },
    {
      etiqueta: "@diezellmx · 2 sep 2026",
      url: "https://www.instagram.com/p/DczGA1JmQqE/",
    },
  ],
} as const;

export interface FechaTour {
  fecha: string;
  diaSemana: string;
  ciudad: string;
  recinto: string;
  hora?: string;
  boletera?: string;
  estado: "sold-out" | "proximo" | "abierto" | "pasado";
  estadoTexto: string;
  boletos?: string;
  nota?: string;
}

export const TOUR: FechaTour[] = [
  {
    fecha: "21 AGO 2026",
    diaSemana: "Viernes",
    ciudad: "Aguascalientes",
    recinto: "Rocksí",
    hora: "21:00",
    boletera: "Passline",
    estado: "sold-out",
    estadoTexto: "Sold out",
    boletos: "https://www.passline.com/eventos/diezell-en-aguascalientes",
  },
  {
    fecha: "22 AGO 2026",
    diaSemana: "Sábado",
    ciudad: "Guadalajara",
    recinto: "C3 Rooftop",
    hora: "21:30",
    boletera: "TicketNow",
    estado: "sold-out",
    estadoTexto: "Sold out",
    nota: "Con Rebelmate",
  },
  {
    fecha: "16 OCT 2026",
    diaSemana: "Viernes",
    ciudad: "Toluca",
    recinto: "Foro Landó",
    boletera: "Passline",
    estado: "sold-out",
    estadoTexto: "Sold out",
  },
  {
    fecha: "17 OCT 2026",
    diaSemana: "Sábado",
    ciudad: "Querétaro",
    recinto: "Centro Cultural El Árbol",
    hora: "19:30",
    boletera: "Passline",
    estado: "sold-out",
    estadoTexto: "Sold out",
    boletos: "https://www.passline.com/eventos/diezell-en-queretaro",
  },
  {
    fecha: "23 OCT 2026",
    diaSemana: "Viernes",
    ciudad: "Puebla",
    recinto: "Madre Santa Pulquería",
    hora: "20:00",
    boletera: "Passline",
    estado: "sold-out",
    estadoTexto: "Sold out",
    boletos: "https://www.passline.com/eventos/diezell-en-puebla",
  },
  {
    fecha: "24 OCT 2026",
    diaSemana: "Viernes",
    ciudad: "Ciudad de México",
    recinto: "Fuck Off Room",
    hora: "20:00",
    boletera: "Superboletos",
    estado: "sold-out",
    estadoTexto: "Sold out",
  },
  {
    fecha: "06 NOV 2026",
    diaSemana: "Viernes",
    ciudad: "León",
    recinto: "El Callejón",
    hora: "19:00",
    boletera: "Passline",
    estado: "pasado",
    estadoTexto: "Ya pasó",
    nota: "Con Rebelmate",
  },
  {
    fecha: "07 NOV 2026",
    diaSemana: "Sábado",
    ciudad: "San Luis Potosí",
    recinto: "Estación Wadley",
    hora: "19:00",
    boletera: "Passline",
    estado: "pasado",
    estadoTexto: "Ya pasó",
    nota: "Con Rebelmate e Intento Fallido",
  },
  {
    fecha: "13 NOV 2026",
    diaSemana: "Viernes",
    ciudad: "Monterrey",
    recinto: "Foro Corona",
    hora: "21:00",
    boletera: "Ticketmaster",
    estado: "proximo",
    estadoTexto: "Cierre de gira",
    boletos: LINKS.linktree,
    nota: "Con Chris Mendez · Abre Overthink",
  },
  {
    fecha: "TBA",
    diaSemana: "Por anunciar",
    ciudad: "Mexicali",
    recinto: "—",
    estado: "abierto",
    estadoTexto: "TBA",
    boletos: LINKS.linktree,
  },
];

// Cuenta regresiva: Monterrey, Foro Corona, 13 nov 2026, 21:00 (America/Mexico_City, UTC-6)
export const COUNTDOWN_TARGET = "2026-11-13T21:00:00-06:00";

export const LETRAS = [
  {
    cancion: "El Cuento De Aquel Imperfecto Ser",
    fragmento: "Tuve cien / Cien maneras de explicarlo todo, y fallé / Soy experto en arruinarlo todo",
    url: "https://www.letras.com/diezell/el-cuento-de-aquel-imperfecto-ser/",
  },
  {
    cancion: "Sin Rencores",
    fragmento: "Ve y cuéntale a tus sábanas / Que alguien más ya estudia tu anatomía",
    url: "https://www.letras.com/diezell/sin-rencores/",
  },
  {
    cancion: "El Mejor De Mis Errores",
    fragmento: "Vengo a pedirte la razón / Te juro si regresas esta vez cambiaré",
    url: "https://www.cifraclub.com.br/diezell/el-mejor-de-mis-errores/letra/",
  },
  {
    cancion: "Suspensión...",
    fragmento: "Hace frío aquí, no pude salir / Cuesta respirar hacia el final",
    url: "https://www.letras.com/diezell/",
  },
  {
    cancion: "De Espaldas",
    fragmento: "Pues de espaldas, tú dijiste: Adiós / De espaldas, te juro, tanto no dolió",
    url: "https://www.letras.com/diezell/",
  },
  {
    cancion: "Conmiseración",
    fragmento: "Te cuento que al dormir ella me hacía soñar",
    url: "https://www.letras.com/diezell/",
  },
  {
    cancion: "Resiliencia",
    fragmento: "Trataré de ser preciso / Esto no es un paraíso",
    url: "https://www.letras.com/diezell/",
  },
  {
    cancion: "Muérdago Marchito",
    fragmento: "Y yo sigo esperando bajo el muérdago",
    url: "https://www.losacordes.com/acordes/diezell/muerdago-marchito",
  },
] as const;

export const HISTORIA = [
  {
    anio: "2015",
    texto: "Empiezan como banda de covers a finales de 2015, tocando en la calle Morelos, en el centro de Monterrey, como hobby.",
    fuentes: [
      { medio: "Monterrey Live", fecha: "30 oct 2023", url: "https://monterreylive.com/2023/10/diezell-debutara-en-vivo-en-el-foro-tims/" },
      { medio: "Punkeando", fecha: "15 ago 2021", url: "https://punkeando.com.mx/2021/08/15/10-nuevas-bandas-y-proyectos-mexicanos-que-debes-de-conocer/" },
    ],
  },
  {
    anio: "2018",
    texto: "Se consolidan como proyecto original con el nombre Diezell. “El nombre de Diezell fue parte de una broma entre ellos y así se les quedó.”",
    fuentes: [
      { medio: "Follow Control", fecha: "ene 2024", url: "https://followcontrol.com/2024/01/diezell-presento-su-primera-noche-caotica-en-foro-tims-de-monterrey/" },
    ],
  },
  {
    anio: "2021",
    texto: "“Sin Rencores”, su sencillo debut, fue un boom para empezar a ser escuchados y reconocidos. Llega su primer EP, de cinco canciones.",
    fuentes: [
      { medio: "Puro Rock Puro", fecha: "5 oct 2023", url: "https://purorockpuro.com/diezell-nos-presentan-su-album-caotico/" },
      { medio: "Punkeando", fecha: "15 ago 2021", url: "https://punkeando.com.mx/2021/08/15/10-nuevas-bandas-y-proyectos-mexicanos-que-debes-de-conocer/" },
    ],
  },
  {
    anio: "2023",
    texto: "29 de septiembre: Caótico, su primer álbum. El 20 de enero de 2024, “La Primer Noche Caótica” en Foro Tims abre su primera gira.",
    fuentes: [
      { medio: "Monterrey Live", fecha: "30 oct 2023", url: "https://monterreylive.com/2023/10/diezell-debutara-en-vivo-en-el-foro-tims/" },
    ],
  },
  {
    anio: "2024",
    texto: "Primera gira nacional. Punkeando los incluye entre las 10 bandas mexicanas a seguir en 2024. Se vuelven virales por las similitudes que el público encuentra con PXNDX.",
    fuentes: [
      { medio: "Punkeando", fecha: "1 ene 2024", url: "https://punkeando.com.mx/2024/01/01/ano-nuevo-sonidos-nuevos-10-bandas-mexicanas-a-seguir-en-2024/" },
      { medio: "Monterrey Live", fecha: "30 oct 2023", url: "https://monterreylive.com/2023/10/diezell-debutara-en-vivo-en-el-foro-tims/" },
    ],
  },
  {
    anio: "2025",
    texto: "28 de noviembre: INSANIA, su segundo álbum. Se presenta el 6 de diciembre en Foro Tims.",
    fuentes: [
      { medio: "Puro Rock Puro", fecha: "", url: "https://purorockpuro.com/diezell-presenta-insania-su-segundo-album-de-estudio/" },
    ],
  },
  {
    anio: "2026",
    texto: "Video oficial de “Tus Flores Fueron Entregadas” (dir. David Miranda). René canta “Martirio” con Kross Vázquez (ex PXNDX) en VIVX PXNDX Vol. 1. Insania Tour por 9 ciudades + Mexicali TBA.",
    fuentes: [
      { medio: "Puro Rock Puro", fecha: "15 abr 2026", url: "https://purorockpuro.com/diezell-expande-el-universo-de-insania-con-el-video-oficial-de-tus-flores-fueron-entregadas/" },
      { medio: "Heraldo de México", fecha: "3 abr 2026", url: "https://heraldodemexico.com.mx/espectaculos/2026/4/3/pxndx-esta-de-vuelta-asi-suenan-las-nuevas-canciones-con-invitados-especiales-video-790414.html" },
    ],
  },
] as const;

export const PRENSA = [
  {
    medio: "Puro Rock Puro",
    fecha: "5 oct 2023",
    titulo: "Caótico, uno de los mejores lanzamientos de esta segunda parte del 2023",
    url: "https://purorockpuro.com/diezell-nos-presentan-su-album-caotico/",
  },
  {
    medio: "Puro Rock Puro",
    fecha: "16 dic 2025",
    titulo: "INSANIA: una etapa más cruda, intensa y emocional",
    url: "https://purorockpuro.com/diezell-presenta-insania-su-segundo-album-de-estudio/",
  },
  {
    medio: "Puro Rock Puro",
    fecha: "15 abr 2026",
    titulo: "“Tus Flores Fueron Entregadas”, una de las canciones que mejor resume la carga emocional del proyecto",
    url: "https://purorockpuro.com/diezell-expande-el-universo-de-insania-con-el-video-oficial-de-tus-flores-fueron-entregadas/",
  },
  {
    medio: "Punkeando",
    fecha: "1 ene 2024",
    titulo: "Diezell entre las 10 bandas mexicanas a seguir en 2024",
    url: "https://punkeando.com.mx/2024/01/01/ano-nuevo-sonidos-nuevos-10-bandas-mexicanas-a-seguir-en-2024/",
  },
  {
    medio: "Monterrey Live",
    fecha: "30 oct 2023",
    titulo: "Diezell debutará en vivo en el Foro Tims",
    url: "https://monterreylive.com/2023/10/diezell-debutara-en-vivo-en-el-foro-tims/",
  },
  {
    medio: "Mr Indie",
    fecha: "Entrevista",
    titulo: "Diezell se prepara para su primera gira por México",
    url: "https://mrindie.com/entrevistas/diezell-se-preprara-para-su-primera-gira-por-mexico-entrevista/",
  },
] as const;

export const CURIOSIDADES = [
  "El nombre Diezell nació de una broma interna y “así se les quedó”.",
  "Antes de ser Diezell tocaban covers en la calle Morelos, en el centro de Monterrey (2015).",
  "Emmash Batarse también es productor: ha producido a Rebelmate, Say Ocean y AZVR.",
  "“Donde Nada Puede Malir Sal” es el track 9 de INSANIA, escrito así en Spotify; los fans lo han convertido en frase y meme.",
  "La portada de INSANIA tiene el título invertido: al derecho se lee VINVSNI, lo que ha generado lecturas erróneas (“VINYSNI”) en algunos listados.",
  "Su canción más escuchada es “El Cuento De Aquel Imperfecto Ser” (1.67 M en Spotify; 571K views en YouTube).",
  "Un fan se convirtió en bajista de la banda: iba a los ensayos desde la secundaria y ayudó a filmar “Al parecer eso parece”.",
  "En 2026 René cantó “Martirio” de PXNDX junto a Kross Vázquez en el tributo VIVX PXNDX Vol. 1.",
  "La comunidad fan se organiza en cuentas como @caoticosmty, @caotico_gdl e @insanialovermty; el 29 de septiembre de 2026 celebraron el 3.er aniversario de Caótico.",
  "Tocaron en el Tecate Food Truck Fest 2025 en Monterrey (2 ago 2025).",
] as const;

export const FUENTES = [
  { etiqueta: "Spotify · artista", url: LINKS.spotifyArtist },
  { etiqueta: "Spotify · Caótico", url: LINKS.spotifyCaotico },
  { etiqueta: "Spotify · INSANIA", url: LINKS.spotifyInsania },
  { etiqueta: "YouTube · @diezellmx", url: LINKS.youtube },
  { etiqueta: "Wikipedia · Diezell", url: LINKS.wikipedia },
  { etiqueta: "Puro Rock Puro · Caótico", url: "https://purorockpuro.com/diezell-nos-presentan-su-album-caotico/" },
  { etiqueta: "Puro Rock Puro · INSANIA", url: "https://purorockpuro.com/diezell-presenta-insania-su-segundo-album-de-estudio/" },
  { etiqueta: "Puro Rock Puro · video Tus Flores", url: "https://purorockpuro.com/diezell-expande-el-universo-de-insania-con-el-video-oficial-de-tus-flores-fueron-entregadas/" },
  { etiqueta: "Follow Control · Primera Noche Caótica", url: "https://followcontrol.com/2024/01/diezell-presento-su-primera-noche-caotica-en-foro-tims-de-monterrey/" },
  { etiqueta: "Punkeando · 10 bandas a seguir 2024", url: "https://punkeando.com.mx/2024/01/01/ano-nuevo-sonidos-nuevos-10-bandas-mexicanas-a-seguir-en-2024/" },
  { etiqueta: "Heraldo de México · VIVX PXNDX", url: "https://heraldodemexico.com.mx/espectaculos/2026/4/3/pxndx-esta-de-vuelta-asi-suenan-las-nuevas-canciones-con-invitados-especiales-video-790414.html" },
  { etiqueta: "C3 Stage · Instagram", url: "https://www.instagram.com/p/DaLWmfsgY7K/" },
  { etiqueta: "Mr Indie · entrevista", url: "https://mrindie.com/entrevistas/diezell-se-preprara-para-su-primera-gira-por-mexico-entrevista/" },
  { etiqueta: "Monterrey Live", url: "https://monterreylive.com/2023/10/diezell-debutara-en-vivo-en-el-foro-tims/" },
  { etiqueta: "Letras.com · Diezell", url: "https://www.letras.com/diezell/discografia/" },
] as const;
