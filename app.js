/*
  DIEZELL · app.js — interacción (JavaScript vanilla, sin build)
  1. Menú móvil. 2. Reveal al scroll (solo desplaza 14px, nunca oculta).
  3. Créditos de foto: botón circular "i" que abre un popover con
     fotógrafo, fuente, fecha y enlace. Esc cierra y devuelve el foco.
*/
(function () {
  'use strict';

  /* Páginas en canciones/ viven un nivel más abajo: sus rutas relativas
     llevan ../ (audio, imágenes, enlaces). El resto de páginas usan ''. */
  var DZ_BASE = window.location.pathname.indexOf('/canciones/') !== -1 ? '../' : '';
  function conBase(ruta) {
    if (!ruta || ruta.indexOf('http') === 0 || ruta.indexOf('../') === 0) return ruta;
    return DZ_BASE + ruta;
  }

  /* 1. Menú móvil */
  var menuBtn = document.getElementById('menu-btn');
  var nav = document.getElementById('nav-principal');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var abierto = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', abierto ? 'true' : 'false');
      menuBtn.setAttribute('aria-label', abierto ? 'Cerrar menú' : 'Abrir menú');
    });
    nav.querySelectorAll('a').forEach(function (enlace) {
      enlace.addEventListener('click', function () {
        nav.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
        menuBtn.setAttribute('aria-label', 'Abrir menú');
      });
    });
  }

  /* 2. Reveal al scroll — solo desplazamiento suave, contenido siempre visible */
  var reducirMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reducirMovimiento && 'IntersectionObserver' in window) {
    var observador = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('visible');
          observador.unobserve(entrada.target);
        }
      });
    }, { threshold: 0.05 });
    document.querySelectorAll('.section, .album-screen, .slogan-band, .quote-band').forEach(function (el) {
      el.classList.add('reveal');
      observador.observe(el);
    });
  }

  /* 3. Créditos de foto */
  var botones = Array.prototype.slice.call(document.querySelectorAll('.foto-info'));
  var abiertoBtn = null;

  function cerrarPopover(btn) {
    if (!btn) return;
    var pop = document.getElementById(btn.getAttribute('aria-controls'));
    if (pop) pop.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    if (abiertoBtn === btn) abiertoBtn = null;
  }

  botones.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var pop = document.getElementById(btn.getAttribute('aria-controls'));
      if (!pop) return;
      var yaAbierto = btn.getAttribute('aria-expanded') === 'true';
      if (abiertoBtn && abiertoBtn !== btn) cerrarPopover(abiertoBtn);
      if (yaAbierto) {
        cerrarPopover(btn);
      } else {
        pop.hidden = false;
        btn.setAttribute('aria-expanded', 'true');
        abiertoBtn = btn;
        var cerrar = pop.querySelector('.foto-popover-cerrar');
        if (cerrar) cerrar.focus();
      }
    });
  });

  document.querySelectorAll('.foto-popover-cerrar').forEach(function (cerrar) {
    cerrar.addEventListener('click', function (e) {
      e.stopPropagation();
      var pop = cerrar.closest('.foto-popover');
      var btn = pop ? document.querySelector('[aria-controls="' + pop.id + '"]') : null;
      cerrarPopover(btn);
      if (btn) btn.focus();
    });
  });

  document.addEventListener('click', function (e) {
    if (abiertoBtn && !e.target.closest('.foto-wrap')) cerrarPopover(abiertoBtn);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && abiertoBtn) {
      var btn = abiertoBtn;
      cerrarPopover(btn);
      btn.focus();
    }
  });

  window.DZ_FALLBACK = [{"n": 1, "titulo": "Suspensión...", "album": "INSANIA", "preview": "audio/previews/01-insania-suspension.mp3", "archivo": "audio/previews/01-insania-suspension.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=xAJttFYLxO8", "videoId": "xAJttFYLxO8"}, {"n": 2, "titulo": "Más Que Ayer, Menos Que Mañana", "album": "INSANIA", "preview": "audio/previews/02-insania-mas-que-ayer-menos-que-manana.mp3", "archivo": "audio/previews/02-insania-mas-que-ayer-menos-que-manana.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=a2bWhsOhNeM", "videoId": "a2bWhsOhNeM"}, {"n": 3, "titulo": "Días Felices: Los Lunes", "album": "INSANIA", "preview": "audio/previews/03-insania-dias-felices-los-lunes.mp3", "archivo": "audio/previews/03-insania-dias-felices-los-lunes.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=RWEEVDLSCik", "videoId": "RWEEVDLSCik"}, {"n": 4, "titulo": "Tus Flores Fueron Entregadas", "album": "INSANIA", "preview": "audio/previews/04-insania-tus-flores-fueron-entregadas.mp3", "archivo": "audio/previews/04-insania-tus-flores-fueron-entregadas.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=RDrvjTxAHkY", "videoId": "RDrvjTxAHkY"}, {"n": 5, "titulo": "El Último Soldado En Pie", "album": "INSANIA", "preview": "audio/previews/05-insania-el-ultimo-soldado-en-pie.mp3", "archivo": "audio/previews/05-insania-el-ultimo-soldado-en-pie.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=yzDN1Xg8w1c", "videoId": "yzDN1Xg8w1c"}, {"n": 6, "titulo": "El Monstruo De Gizmo", "album": "INSANIA", "preview": "audio/previews/06-insania-el-monstruo-de-gizmo.mp3", "archivo": "audio/previews/06-insania-el-monstruo-de-gizmo.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=yUvkRgX-RC8", "videoId": "yUvkRgX-RC8"}, {"n": 7, "titulo": "La Paradoja De Tennessee", "album": "INSANIA", "preview": "audio/previews/07-insania-la-paradoja-de-tennessee.mp3", "archivo": "audio/previews/07-insania-la-paradoja-de-tennessee.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=Z5AR4Y4mZjE", "videoId": "Z5AR4Y4mZjE"}, {"n": 8, "titulo": "Resiliencia", "album": "INSANIA", "preview": "audio/previews/08-insania-resiliencia.mp3", "archivo": "audio/previews/08-insania-resiliencia.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=mrv-jjIP6Wo", "videoId": "mrv-jjIP6Wo"}, {"n": 9, "titulo": "Donde Nada Puede Malir Sal", "album": "INSANIA", "preview": "audio/previews/09-insania-donde-nada-puede-malir-sal.mp3", "archivo": "audio/previews/09-insania-donde-nada-puede-malir-sal.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=mhG5BStAGEU", "videoId": "mhG5BStAGEU"}, {"n": 10, "titulo": "Una Triste Mañana de Noviembre", "album": "INSANIA", "preview": "audio/previews/10-insania-una-triste-manana-de-noviembre.mp3", "archivo": "audio/previews/10-insania-una-triste-manana-de-noviembre.mp3", "cover": "images/insania.jpg", "spotify": "https://open.spotify.com/album/3LGm9FVg9cswGMo5YneJ88", "youtube": "https://www.youtube.com/watch?v=wJvPm8h1X6s", "videoId": "wJvPm8h1X6s"}, {"n": 11, "titulo": "El Cuento De Aquel Imperfecto Ser", "album": "Caótico", "preview": "audio/previews/11-caotico-el-cuento-de-aquel-imperfecto-ser.mp3", "archivo": "audio/previews/11-caotico-el-cuento-de-aquel-imperfecto-ser.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=MuvgZpXqsY8", "videoId": "MuvgZpXqsY8"}, {"n": 12, "titulo": "Conmiseración", "album": "Caótico", "preview": "audio/previews/12-caotico-conmiseracion.mp3", "archivo": "audio/previews/12-caotico-conmiseracion.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=xV-S1Un7S7E", "videoId": "xV-S1Un7S7E"}, {"n": 13, "titulo": "Martes Con Aroma A Domingo", "album": "Caótico", "preview": "audio/previews/13-caotico-martes-con-aroma-a-domingo.mp3", "archivo": "audio/previews/13-caotico-martes-con-aroma-a-domingo.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=HETRiythGW0", "videoId": "HETRiythGW0"}, {"n": 14, "titulo": "Sin Destinatario", "album": "Caótico", "preview": "audio/previews/14-caotico-sin-destinatario.mp3", "archivo": "audio/previews/14-caotico-sin-destinatario.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=WBnMi0n6-CM", "videoId": "WBnMi0n6-CM"}, {"n": 15, "titulo": "Al Parecer Eso Parece", "album": "Caótico", "preview": "audio/previews/15-caotico-al-parecer-eso-parece.mp3", "archivo": "audio/previews/15-caotico-al-parecer-eso-parece.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=4Zt18UbJXbI", "videoId": "4Zt18UbJXbI"}, {"n": 16, "titulo": "Una, Dos O Tres Lágrimas Permitidas", "album": "Caótico", "preview": "audio/previews/16-caotico-una-dos-o-tres-lagrimas-permitidas.mp3", "archivo": "audio/previews/16-caotico-una-dos-o-tres-lagrimas-permitidas.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=ryMF1coGHvQ", "videoId": "ryMF1coGHvQ"}, {"n": 17, "titulo": "A Golpe de Mar, Pecho Sereno", "album": "Caótico", "preview": "audio/previews/17-caotico-a-golpe-de-mar-pecho-sereno.mp3", "archivo": "audio/previews/17-caotico-a-golpe-de-mar-pecho-sereno.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=UZSr0VfMBAw", "videoId": "UZSr0VfMBAw"}, {"n": 18, "titulo": "De Espaldas", "album": "Caótico", "preview": "audio/previews/18-caotico-de-espaldas.mp3", "archivo": "audio/previews/18-caotico-de-espaldas.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=G0LeyJihYEY", "videoId": "G0LeyJihYEY"}, {"n": 19, "titulo": "Mi Más Sentido Pésame (Murió El Sentido Común)", "album": "Caótico", "preview": "audio/previews/19-caotico-mi-mas-sentido-pesame.mp3", "archivo": "audio/previews/19-caotico-mi-mas-sentido-pesame.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=1Pn9TNesM-Y", "videoId": "1Pn9TNesM-Y"}, {"n": 20, "titulo": "Demencia", "album": "Caótico", "preview": "audio/previews/20-caotico-demencia.mp3", "archivo": "audio/previews/20-caotico-demencia.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=ViTEzKb4FFA", "videoId": "ViTEzKb4FFA"}, {"n": 21, "titulo": "El Último Recuerdo De La Noche", "album": "Caótico", "preview": "audio/previews/21-caotico-el-ultimo-recuerdo-de-la-noche.mp3", "archivo": "audio/previews/21-caotico-el-ultimo-recuerdo-de-la-noche.mp3", "cover": "images/caotico.jpg", "spotify": "https://open.spotify.com/album/738DN211pKelLzZTRzIC28", "youtube": "https://www.youtube.com/watch?v=txXzCHGZYog", "videoId": "txXzCHGZYog"}, {"n": 22, "titulo": "Insomnio", "album": "Sencillo · 2021", "preview": "audio/previews/22-sencillo-insomnio.mp3", "archivo": "audio/previews/22-sencillo-insomnio.mp3", "cover": null, "spotify": "https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g", "youtube": "https://www.youtube.com/watch?v=rffBFmML9Pw", "videoId": "rffBFmML9Pw"}, {"n": 23, "titulo": "Sin Rencores", "album": "Sencillo · 2021", "preview": "audio/previews/23-sencillo-sin-rencores.mp3", "archivo": "audio/previews/23-sencillo-sin-rencores.mp3", "cover": null, "spotify": "https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g", "youtube": "https://www.youtube.com/watch?v=tIEk-WAnrLE", "videoId": "tIEk-WAnrLE"}, {"n": 24, "titulo": "El Mejor De Mis Errores", "album": "Sencillo · 2021", "preview": "audio/previews/24-sencillo-el-mejor-de-mis-errores.mp3", "archivo": "audio/previews/24-sencillo-el-mejor-de-mis-errores.mp3", "cover": null, "spotify": "https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g", "youtube": "https://www.youtube.com/watch?v=g4aoHlpNBmM", "videoId": "g4aoHlpNBmM"}, {"n": 25, "titulo": "Tiempos De Un Tiempo", "album": "Sencillo · 2021", "preview": "audio/previews/25-sencillo-tiempos-de-un-tiempo.mp3", "archivo": "audio/previews/25-sencillo-tiempos-de-un-tiempo.mp3", "cover": null, "spotify": "https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g", "youtube": "https://www.youtube.com/watch?v=5vRhWd78pTY", "videoId": "5vRhWd78pTY"}, {"n": 26, "titulo": "Muérdago Marchito", "album": "Sencillo · 2021", "preview": "audio/previews/26-sencillo-muerdago-marchito.mp3", "archivo": "audio/previews/26-sencillo-muerdago-marchito.mp3", "cover": null, "spotify": "https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g", "youtube": "https://www.youtube.com/watch?v=-yFKtUmw_9g", "videoId": "-yFKtUmw_9g"}, {"n": 27, "titulo": "Hipocresía", "album": "Sencillo · 2022", "preview": "audio/previews/27-sencillo-hipocresia.mp3", "archivo": "audio/previews/27-sencillo-hipocresia.mp3", "cover": null, "spotify": "https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g", "youtube": "https://www.youtube.com/watch?v=YfDMFYyOgG8", "videoId": "YfDMFYyOgG8"}];
  /* 4. Reproductor interno (v2.2) — adelantos de 90 segundos con permiso de la banda.
     El límite vive en UNA sola constante. Si la banda amplía el permiso, se cambia
     este número y se regeneran los previews desde los archivos completos; el código no cambia.
     La web solo sirve los previews (audio/previews/); los archivos completos
     no se enlazan en ningún sitio. */
  var PREVIEW_LIMIT_SECONDS = 90;

  var dzAudio = document.getElementById('dz-audio');
  var dzListaEl = document.getElementById('dz-lista');
  var dzDock = document.getElementById('dz-dock');
  if (dzAudio && (dzListaEl || dzDock)) {
    var DZ = { canciones: null, indice: 0, sonando: false, cta: false };
    var $ = function (id) { return document.getElementById(id); };

    function fmt(s) {
      if (!isFinite(s) || s < 0) s = 0;
      var m = Math.floor(s / 60);
      var r = Math.floor(s % 60);
      return m + ':' + (r < 10 ? '0' : '') + r;
    }
    function actual() { return DZ.canciones[DZ.indice]; }
    function clamp90(t) { return Math.max(0, Math.min(PREVIEW_LIMIT_SECONDS, t)); }

    function setCover(img, dzl, c) {
      if (!img) return;
      if (c.cover) {
        img.src = c.cover; img.hidden = false;
        if (dzl) dzl.hidden = true;
      } else {
        img.hidden = true;
        if (dzl) dzl.hidden = false;
      }
    }

    function pintarBotones() {
      var icono = DZ.sonando ? '⏸' : '▶';
      var p1 = $('dz-play'); if (p1) p1.textContent = icono;
      var p2 = $('dock-play'); if (p2) p2.textContent = icono;
    }

    function pintar() {
      var c = actual();
      if (!c) return;
      var t = $('dz-titulo'); if (t) t.textContent = c.titulo;
      var a = $('dz-album'); if (a) a.textContent = 'Diezell · ' + c.album;
      var sp = $('dz-spotify'); if (sp) sp.href = c.spotify;
      var yt = $('dz-youtube'); if (yt) yt.href = c.youtube;
      setCover($('dz-cover'), $('dz-cover-dzl'), c);
      var dt = $('dock-titulo'); if (dt) dt.textContent = c.titulo;
      var da = $('dock-album'); if (da) da.textContent = 'Diezell · ' + c.album + ' · Adelanto 1:30';
      setCover($('dock-cover'), $('dock-cover-dzl'), c);
      var ct = $('dz-cta-titulo'); if (ct) ct.textContent = c.titulo;
      var cs = $('dz-cta-spotify'); if (cs) cs.href = c.spotify;
      var cy = $('dz-cta-youtube'); if (cy) cy.href = c.youtube;
      pintarBotones();
      if (dzListaEl) {
        var filas = dzListaEl.querySelectorAll('.dz-fila');
        filas.forEach(function (fila, i) {
          fila.classList.toggle('active', i === DZ.indice);
          fila.classList.toggle('sonando', i === DZ.indice && DZ.sonando);
          fila.setAttribute('aria-current', i === DZ.indice ? 'true' : 'false');
        });
      }
    }

    function construirLista() {
      if (!dzListaEl) return;
      dzListaEl.innerHTML = '';
      var grupos = [
        { titulo: 'INSANIA · 2025', filtro: function (c) { return c.album === 'INSANIA'; } },
        { titulo: 'Caótico · 2023', filtro: function (c) { return c.album === 'Caótico'; } },
        { titulo: 'Sencillos · 2021–2022', filtro: function (c) { return c.album.indexOf('Sencillo') === 0; } }
      ];
      grupos.forEach(function (g) {
        var items = DZ.canciones.filter(g.filtro);
        if (!items.length) return;
        var h = document.createElement('h3');
        h.className = 'dz-grupo';
        h.textContent = g.titulo;
        dzListaEl.appendChild(h);
        var ol = document.createElement('ol');
        ol.className = 'dz-filas';
        items.forEach(function (c) {
          var li = document.createElement('li');
          var b = document.createElement('button');
          b.type = 'button';
          b.className = 'dz-fila';
          b.setAttribute('data-i', String(c.n - 1));
          var idx = document.createElement('span');
          idx.className = 'dz-idx';
          var num = document.createElement('span');
          num.className = 'dz-idx-num';
          num.textContent = String(c.n);
          var play = document.createElement('span');
          play.className = 'dz-idx-play';
          play.setAttribute('aria-hidden', 'true');
          play.textContent = '▶';
          var eq = document.createElement('span');
          eq.className = 'dz-idx-eq';
          eq.setAttribute('aria-hidden', 'true');
          eq.innerHTML = '<i></i><i></i><i></i>';
          idx.appendChild(num); idx.appendChild(play); idx.appendChild(eq);
          var cover = document.createElement('span');
          cover.className = 'dz-fila-cover';
          if (c.cover) {
            var img = document.createElement('img');
            img.src = c.cover; img.alt = ''; img.width = 40; img.height = 40; img.loading = 'lazy';
            cover.appendChild(img);
          } else {
            var dzl = document.createElement('span');
            dzl.className = 'dz-fila-dzl';
            dzl.textContent = 'DZL';
            cover.appendChild(dzl);
          }
          var texto = document.createElement('span');
          texto.className = 'dz-fila-texto';
          var st = document.createElement('strong');
          st.textContent = c.titulo;
          var sa = document.createElement('span');
          sa.textContent = 'Diezell';
          texto.appendChild(st); texto.appendChild(sa);
          var alb = document.createElement('span');
          alb.className = 'dz-fila-album';
          alb.textContent = c.album;
          var dur = document.createElement('span');
          dur.className = 'dz-fila-dur';
          dur.textContent = '1:30';
          b.appendChild(idx); b.appendChild(cover); b.appendChild(texto); b.appendChild(alb); b.appendChild(dur);
          b.addEventListener('click', function () {
            var i = c.n - 1;
            if (i === DZ.indice && DZ.sonando) { togglePlay(); return; }
            cargar(i, true);
          });
          li.appendChild(b);
          ol.appendChild(li);
        });
        dzListaEl.appendChild(ol);
      });
    }

    function ocultarCTA() {
      DZ.cta = false;
      var cta = $('dz-cta');
      if (cta) cta.hidden = true;
    }
    function mostrarCTA() {
      if (DZ.cta) return;
      DZ.cta = true;
      pintar();
      var cta = $('dz-cta');
      if (cta) cta.hidden = false;
    }

    function cargar(i, reproducir) {
      DZ.indice = (i + DZ.canciones.length) % DZ.canciones.length;
      var c = actual();
      ocultarCTA();
      dzAudio.src = c.preview || c.archivo;
      dzAudio.load();
      pintar();
      if (reproducir) {
        var p = dzAudio.play();
        if (p && p.catch) p.catch(function () { /* el navegador pide gesto: el click ya lo es */ });
      }
    }

    function togglePlay() {
      if (!dzAudio.src) { cargar(DZ.indice, true); return; }
      if (dzAudio.paused) {
        if (dzAudio.currentTime >= PREVIEW_LIMIT_SECONDS - 0.2) dzAudio.currentTime = 0;
        ocultarCTA();
        dzAudio.play();
      } else {
        dzAudio.pause();
      }
    }

    function seekFrac(frac) {
      if (!dzAudio.src) return;
      dzAudio.currentTime = clamp90(frac * PREVIEW_LIMIT_SECONDS);
      ocultarCTA();
      actualizarProgreso();
    }

    function actualizarProgreso() {
      var t = Math.min(dzAudio.currentTime || 0, PREVIEW_LIMIT_SECONDS);
      var frac = PREVIEW_LIMIT_SECONDS ? t / PREVIEW_LIMIT_SECONDS : 0;
      var act = $('dz-actual'); if (act) act.textContent = fmt(t);
      var rel = $('dz-progreso-relleno'); if (rel) rel.style.width = (frac * 100) + '%';
      var bar = $('dz-progreso'); if (bar) bar.setAttribute('aria-valuenow', Math.round(frac * 100));
      var drel = $('dock-relleno'); if (drel) drel.style.width = (frac * 100) + '%';
      var dbar = $('dock-progreso'); if (dbar) dbar.setAttribute('aria-valuenow', Math.round(frac * 100));
    }

    dzAudio.addEventListener('timeupdate', function () {
      if (dzAudio.currentTime >= PREVIEW_LIMIT_SECONDS - 0.05) {
        dzAudio.pause();
        dzAudio.currentTime = PREVIEW_LIMIT_SECONDS;
        actualizarProgreso();
        mostrarCTA();
        return;
      }
      actualizarProgreso();
    });
    dzAudio.addEventListener('ended', function () { mostrarCTA(); });
    dzAudio.addEventListener('play', function () { DZ.sonando = true; pintar(); });
    dzAudio.addEventListener('pause', function () { DZ.sonando = false; pintar(); });

    function enlazar(id, fn) { var el = $(id); if (el) el.addEventListener('click', fn); }
    enlazar('dz-play', togglePlay);
    enlazar('dock-play', togglePlay);
    enlazar('dz-anterior', function () { cargar(DZ.indice - 1, true); });
    enlazar('dz-siguiente', function () { cargar(DZ.indice + 1, true); });
    enlazar('dock-next', function () { cargar(DZ.indice + 1, true); });
    enlazar('dz-cta-siguiente', function () { cargar(DZ.indice + 1, true); });
    enlazar('dock-ir', function () {
      if (window.location.pathname.indexOf('escuchar.html') !== -1) {
        var rep = document.getElementById('reproductor');
        if (rep) rep.scrollIntoView({ behavior: 'smooth' });
      } else {
        window.location.href = DZ_BASE + 'escuchar.html#reproductor';
      }
    });

    function barraSeek(id, esDock) {
      var bar = $(id);
      if (!bar) return;
      bar.addEventListener('click', function (e) {
        var rect = bar.getBoundingClientRect();
        seekFrac((e.clientX - rect.left) / rect.width);
      });
      bar.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowRight') { dzAudio.currentTime = clamp90(dzAudio.currentTime + 5); ocultarCTA(); actualizarProgreso(); e.preventDefault(); }
        if (e.key === 'ArrowLeft') { dzAudio.currentTime = clamp90(dzAudio.currentTime - 5); ocultarCTA(); actualizarProgreso(); e.preventDefault(); }
      });
    }
    barraSeek('dz-progreso');
    barraSeek('dock-progreso');

    var vol = $('dz-vol');
    if (vol) {
      dzAudio.volume = vol.value / 100;
      vol.addEventListener('input', function () { dzAudio.volume = vol.value / 100; });
    } else {
      dzAudio.volume = 0.9;
    }

    function iniciar(canciones) {
      DZ.canciones = canciones.map(function (c) {
        var d = {};
        for (var k in c) d[k] = c[k];
        d.preview = conBase(c.preview);
        d.archivo = conBase(c.archivo);
        d.cover = c.cover ? conBase(c.cover) : c.cover;
        return d;
      });
      construirLista();
      var inicio = parseInt((document.body && document.body.getAttribute('data-dz-cancion')) || '1', 10);
      if (!isFinite(inicio) || inicio < 1 || inicio > DZ.canciones.length) inicio = 1;
      cargar(inicio - 1, false);
    }
    fetch(DZ_BASE + 'audio/playlist.json')
      .then(function (r) { if (!r.ok) throw new Error('sin playlist'); return r.json(); })
      .then(function (d) { iniciar(d.canciones); })
      .catch(function () {
        if (window.DZ_FALLBACK) iniciar(window.DZ_FALLBACK);
        else if (dzListaEl) dzListaEl.innerHTML = '<p class="dz-lista-cargando">No se pudo cargar la lista de canciones.</p>';
      });
  }
})();

/* 4. Historias flotantes de integrantes (modal a pantalla completa).
   Se abre con el botón data-historia o con el enlace index.html#historia-<slug>.
   Cierra con X, con clic fuera del contenido y con Esc. Devuelve el foco. */
(function () {
  'use strict';
  var modales = {};
  var ultimoFoco = null;
  var abierto = null;

  function $ (id) { return document.getElementById(id); }
  function slugDeHash() {
    var h = window.location.hash || '';
    var m = h.match(/^#historia-(rene|bernie|emmash|mau)$/);
    return m ? m[1] : null;
  }
  function abrir(slug) {
    var modal = modales[slug];
    if (!modal || abierto === modal) return;
    if (abierto) cerrar(false);
    ultimoFoco = document.activeElement;
    abierto = modal;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    var cerrarBtn = modal.querySelector('.historia-cerrar');
    if (cerrarBtn) cerrarBtn.focus();
  }
  function cerrar(restaurarHash) {
    if (!abierto) return;
    abierto.hidden = true;
    abierto = null;
    document.body.style.overflow = '';
    if (restaurarHash !== false && slugDeHash()) {
      history.replaceState(null, '', window.location.pathname + window.location.search);
    }
    if (ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
    ultimoFoco = null;
  }
  ['rene', 'bernie', 'emmash', 'mau'].forEach(function (slug) {
    var modal = $('historia-' + slug);
    if (modal) modales[slug] = modal;
  });
  if (!Object.keys(modales).length) return;
  document.querySelectorAll('[data-historia]').forEach(function (btn) {
    btn.addEventListener('click', function () { abrir(btn.getAttribute('data-historia')); });
  });
  Object.keys(modales).forEach(function (slug) {
    var modal = modales[slug];
    modal.addEventListener('click', function (e) {
      if (e.target === modal || e.target.classList.contains('historia-modal-foto')) cerrar();
    });
    var btn = modal.querySelector('.historia-cerrar');
    if (btn) btn.addEventListener('click', function () { cerrar(); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && abierto) { cerrar(); e.preventDefault(); }
  });
  window.addEventListener('hashchange', function () {
    var slug = slugDeHash();
    if (slug) abrir(slug);
    else cerrar(false);
  });
  var inicial = slugDeHash();
  if (inicial) abrir(inicial);
})();
