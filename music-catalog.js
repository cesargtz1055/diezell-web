/*
 * DIEZELL — Explorador editorial de canciones.
 * Fuente de verdad: enlaces de las listas HTML existentes.
 * Sin API adicional, sin dependencias y sin datos inventados.
 */
(function () {
  'use strict';
  var root = document.getElementById('music-catalog-grid');
  if (!root) return;
  var search = document.getElementById('music-search');
  var status = document.getElementById('music-catalog-count');
  var empty = document.getElementById('music-empty');
  var controls = Array.prototype.slice.call(document.querySelectorAll('[data-music-filter]'));
  var currentFilter = 'all';

  function normalizar(texto) {
    return String(texto || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }

  function seleccionar(el, selector) {
    return el ? el.querySelector(selector) : null;
  }

  var tracks = [];
  var byUrl = Object.create(null);
  function registrar(url, titulo, tipo, ano, numero, duracion, secundario) {
    if (!url || !titulo) return;
    var key = url.split('#')[0];
    if (byUrl[key]) {
      if (secundario) byUrl[key].esSencillo = true;
      return;
    }
    var entrada = {
      url: key, titulo: titulo, tipo: tipo, ano: ano,
      numero: numero, duracion: duracion, esSencillo: tipo === 'sencillos'
    };
    byUrl[key] = entrada;
    tracks.push(entrada);
  }

  [
    { id: 'album-insania', tipo: 'insania', ano: '2025' },
    { id: 'album-caotico', tipo: 'caotico', ano: '2023' }
  ].forEach(function (album) {
    var titulo = document.getElementById(album.id);
    var section = titulo && titulo.closest('.album-screen');
    if (!section) return;
    section.querySelectorAll('.tracklist li').forEach(function (li, index) {
      var a = li.querySelector('a.track-titulo') || li.querySelector('.track-titulo a');
      if (!a) return;
      var dur = seleccionar(li, '.track-dur');
      registrar(a.getAttribute('href'), a.textContent.trim(), album.tipo, album.ano,
        String(index + 1).padStart(2, '0'), dur ? dur.textContent.trim() : '', false);
    });
  });

  document.querySelectorAll('.sencillos-row a.sencillo-card').forEach(function (a) {
    var nombre = seleccionar(a, 'strong');
    var meta = seleccionar(a, 'span');
    var ano = meta && meta.textContent.match(/20\d{2}/);
    registrar(a.getAttribute('href'), nombre ? nombre.textContent.trim() : a.textContent.trim(),
      'sencillos', ano ? ano[0] : '', '—', '', true);
  });

  function nuevo(tag, clase, contenido) {
    var el = document.createElement(tag);
    if (clase) el.className = clase;
    if (contenido !== undefined) el.textContent = contenido;
    return el;
  }
  function categoria(item) {
    return item.tipo === 'insania' ? 'INSANIA' : item.tipo === 'caotico' ? 'CAÓTICO' : 'SENCILLO';
  }

  function pintar() {
    var texto = normalizar(search && search.value);
    var visibles = tracks.filter(function (item) {
      var cumpleTipo = currentFilter === 'all' || item.tipo === currentFilter ||
        (currentFilter === 'sencillos' && item.esSencillo);
      var cumpleBusqueda = !texto || normalizar(item.titulo + ' ' + categoria(item) + ' ' + item.ano).indexOf(texto) >= 0;
      return cumpleTipo && cumpleBusqueda;
    });

    var fragment = document.createDocumentFragment();
    visibles.forEach(function (item, index) {
      var card = nuevo('article', 'music-track');
      var enlace = nuevo('a', 'music-track-main');
      enlace.href = item.url;
      enlace.setAttribute('aria-label', 'Abrir ficha de ' + item.titulo);

      var num = nuevo('span', 'music-track-index', item.numero === '—' ? String(index + 1).padStart(2, '0') : item.numero);
      num.setAttribute('aria-hidden', 'true');
      var info = nuevo('span', 'music-track-info');
      info.appendChild(nuevo('strong', 'music-track-title', item.titulo));
      info.appendChild(nuevo('span', 'music-track-album', categoria(item) + (item.ano ? ' / ' + item.ano : '')));
      var arrow = nuevo('span', 'music-track-arrow', '↗');
      arrow.setAttribute('aria-hidden', 'true');
      enlace.appendChild(num); enlace.appendChild(info); enlace.appendChild(arrow);

      var actions = nuevo('div', 'music-track-actions');
      actions.appendChild(nuevo('span', 'music-track-detail', item.duracion ? item.duracion + ' · Ver ficha →' : 'Ver ficha →'));
      var button = nuevo('button', 'music-track-preview');
      button.type = 'button';
      button.dataset.dzPreviewTitle = item.titulo;
      button.setAttribute('aria-label', 'Escuchar adelanto de ' + item.titulo);
      button.disabled = typeof window.DZ_REPRODUCIR !== 'function';
      var glyph = nuevo('span', '', '▶');
      glyph.setAttribute('aria-hidden', 'true');
      button.appendChild(glyph);
      button.appendChild(nuevo('span', '', 'Adelanto 1:30'));
      actions.appendChild(button);

      card.appendChild(enlace); card.appendChild(actions);
      fragment.appendChild(card);
    });

    root.replaceChildren(fragment);
    if (empty) empty.hidden = visibles.length !== 0;
    if (status) status.textContent = visibles.length + (visibles.length === 1 ? ' canción' : ' canciones') + ' · ' + (currentFilter === 'all' ? 'Todo el archivo' : currentFilter === 'sencillos' ? 'Sencillos' : categoria({ tipo: currentFilter }));
  }

  if (search) search.addEventListener('input', pintar);
  controls.forEach(function (button) {
    button.addEventListener('click', function () {
      currentFilter = button.dataset.musicFilter;
      controls.forEach(function (c) {
        var active = c === button;
        c.classList.toggle('is-selected', active);
        c.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      pintar();
    });
  });

  root.addEventListener('click', function (event) {
    var button = event.target.closest('[data-dz-preview-title]');
    if (!button || button.disabled) return;
    var ok = typeof window.DZ_REPRODUCIR === 'function' && window.DZ_REPRODUCIR(button.dataset.dzPreviewTitle);
    if (!ok && status) status.textContent = 'Este adelanto no está disponible. Abre la ficha para acceder a las fuentes oficiales.';
  });
  document.addEventListener('diezell:playlist-ready', function () {
    root.querySelectorAll('[data-dz-preview-title]').forEach(function (button) { button.disabled = false; });
  });

  pintar();
})();
