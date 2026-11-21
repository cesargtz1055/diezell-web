/* Diezell · rebuilt Music interaction. The source audio engine is app.js;
   this module only handles discovery UI, routing, and audible error feedback. */
(function(){
  'use strict';
  const menuButton=document.querySelector('.dz3-menu-toggle');
  const menu=document.querySelector('#dz3-menu');
  if(menuButton&&menu){
    const close=()=>{menu.classList.remove('is-open');menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label','Abrir menú')};
    menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')==='true';if(open){close()}else{menu.classList.add('is-open');menuButton.setAttribute('aria-expanded','true');menuButton.setAttribute('aria-label','Cerrar menú')}});
    menu.addEventListener('click',e=>{if(e.target.closest('a'))close()});
    document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
    document.addEventListener('click',e=>{if(!menu.contains(e.target)&&!menuButton.contains(e.target))close()});
  }
  const list=document.querySelector('#dz-lista');
  const search=document.querySelector('#dz3-search');
  const filters=[...document.querySelectorAll('[data-filter]')];
  const empty=document.querySelector('#dz3-zero');
  const detail=document.querySelector('#dz3-ficha-links');
  let chosen='all';
  const clean=s=>(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();
  const groupFor=h=>{
    const t=clean(h.textContent);
    return t.includes('insania')?'insania':t.includes('caotico')?'caotico':'sencillos';
  };
  const links=Array.isArray(window.DZ3_LINKS)?window.DZ3_LINKS:[];
  function filterList(){
    if(!list)return;
    const term=clean(search?search.value:'');
    let shown=0;
    list.querySelectorAll('.dz-grupo').forEach(h=>{
      const ol=h.nextElementSibling;
      if(!ol||!ol.classList.contains('dz-filas'))return;
      let inGroup=0;
      const group=groupFor(h);
      ol.querySelectorAll('li').forEach(li=>{
        const label=li.querySelector('.dz-fila-texto strong')?.textContent||'';
        const match=(chosen==='all'||chosen===group)&&clean(label).includes(term);
        li.hidden=!match;
        if(match){inGroup++;shown++}
      });
      h.hidden=!inGroup;ol.hidden=!inGroup;
      h.id='lista-'+group;
    });
    if(empty)empty.hidden=shown!==0;
    if(detail)detail.textContent=shown===1?'1 canción encontrada. Abre su ficha junto a la pista.':shown+' canciones encontradas. Abre una ficha junto a cada pista.';
    if(search)search.setAttribute('aria-describedby','dz3-ficha-links');
  }
  function decorate(){
    if(!list)return;
    const rows=[...list.querySelectorAll('.dz-filas > li')];
    if(!rows.length)return;
    for(const li of rows){
      const button=li.querySelector('.dz-fila');
      if(!button||li.querySelector('.dz3-track-detail'))continue;
      const i=Number(button.getAttribute('data-i'));
      const href=links[i];
      if(!href)continue;
      const link=document.createElement('a');
      link.className='dz3-track-detail';link.href=href;link.textContent='Ficha ↗';
      const title=button.querySelector('.dz-fila-texto strong')?.textContent||'esta canción';
      link.setAttribute('aria-label','Ver ficha de '+title);
      li.appendChild(link);
    }
    filterList();
  }
  filters.forEach(btn=>btn.addEventListener('click',()=>{
    chosen=btn.dataset.filter;
    filters.forEach(x=>x.setAttribute('aria-pressed',String(x===btn)));
    filterList();
  }));
  if(search){
    search.addEventListener('input',filterList);
    search.addEventListener('keydown',event=>{
      if(event.key==='Escape'&&search.value){search.value='';filterList();event.stopPropagation()}
    });
  }
  if(list){
    const observer=new MutationObserver(()=>decorate());
    observer.observe(list,{childList:true,subtree:false});
    decorate();
  }
  const audio=document.querySelector('#dz-audio');
  const feedback=document.querySelector('#dz3-player-feedback');
  if(audio&&feedback){
    audio.addEventListener('error',()=>{feedback.textContent='El adelanto no está disponible. Puedes abrir la canción en Spotify o YouTube.';feedback.hidden=false});
    audio.addEventListener('playing',()=>{feedback.hidden=true;feedback.textContent=''});
    audio.addEventListener('stalled',()=>{feedback.textContent='La conexión está tardando en cargar el adelanto.';feedback.hidden=false});
  }
})();