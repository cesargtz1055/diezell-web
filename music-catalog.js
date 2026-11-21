/* Archivo sonoro: catálogo navegable construido desde el playlist existente.
   No duplica ni modifica el motor de reproducción de app.js. */
(function(){
  'use strict';
  var root=document.getElementById('music-catalog-grid');
  if(!root)return;
  var search=document.getElementById('music-search');
  var count=document.getElementById('music-catalog-count');
  var empty=document.getElementById('music-empty');
  var filters=Array.prototype.slice.call(document.querySelectorAll('[data-music-filter]'));
  var filter='all',songs=[];
  var norm=function(s){return String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');};
  var links={};
  document.querySelectorAll('a[href^="canciones/"]').forEach(function(a){
    var key=norm(a.textContent);if(key&&!links[key])links[key]=a.getAttribute('href');
  });
  function group(c){return c.album==='INSANIA'?'insania':c.album==='Caótico'?'caotico':'sencillos';}
  function make(tag,cls,txt){var el=document.createElement(tag);if(cls)el.className=cls;if(txt!==undefined)el.textContent=txt;return el;}
  function render(){
    root.replaceChildren();
    var term=norm(search.value);
    var shown=songs.filter(function(c){return (filter==='all'||group(c)===filter)&&(!term||norm(c.titulo+' '+c.album).includes(term));});
    count.textContent=shown.length+' de '+songs.length+' canciones';
    empty.hidden=shown.length!==0;
    var fragment=document.createDocumentFragment();
    shown.forEach(function(c){
      var card=make('article','music-song-card');
      var art=make('div','music-song-art');
      if(c.cover&&/^images\/[a-zA-Z0-9_.\/-]+$/.test(c.cover)){
        var img=make('img');img.src=c.cover;img.alt='';img.loading='lazy';img.width=440;img.height=275;
        img.addEventListener('error',function(){img.remove();});
        art.appendChild(img);
      }
      art.appendChild(make('span','',c.album));
      var body=make('div','music-song-body');
      body.appendChild(make('small','',String(c.n).padStart(2,'0')+' / DIEZELL'));
      body.appendChild(make('h3','',c.titulo));
      var actions=make('div','music-song-actions');
      var href=links[norm(c.titulo)];
      if(href){var link=make('a','', 'Ver ficha ↗');link.href=href;link.setAttribute('aria-label','Ver ficha de '+c.titulo);actions.appendChild(link);}
      var play=make('button','', '▶ Adelanto');
      play.type='button';play.setAttribute('aria-label','Escuchar adelanto de '+c.titulo);
      play.addEventListener('click',function(){
        var hidden=document.querySelector('#dz-lista .dz-fila[data-i="'+(Number(c.n)-1)+'"]');
        if(hidden){hidden.click();document.getElementById('reproductor').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}
        else{window.location.href='escuchar.html#reproductor';}
      });
      actions.appendChild(play);body.appendChild(actions);card.appendChild(art);card.appendChild(body);fragment.appendChild(card);
    });
    root.appendChild(fragment);
  }
  search.addEventListener('input',render);
  filters.forEach(function(b){b.addEventListener('click',function(){filter=b.dataset.musicFilter;filters.forEach(function(x){var on=x===b;x.classList.toggle('is-selected',on);x.setAttribute('aria-pressed',String(on));});render();});});
  fetch('audio/playlist.json').then(function(r){if(!r.ok)throw Error('Playlist no disponible');return r.json();}).then(function(data){
    if(!Array.isArray(data.canciones)||!data.canciones.length)throw Error('Lista vacía');
    songs=data.canciones.filter(function(c){return c&&c.titulo&&Number.isInteger(Number(c.n));});render();
  }).catch(function(){
    count.textContent='Catálogo temporalmente no disponible';
    empty.hidden=false;empty.textContent='No se pudo cargar el catálogo interactivo. Puedes consultar las canciones en los álbumes y sencillos más abajo.';
  });
})();
