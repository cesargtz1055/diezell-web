/* Restored Diezell music companion.
   One <audio> per page. All controls delegate to the original 90-second player
   engine; opening a sheet does not create another stream or autoplay. */
(function(){
  'use strict';
  const root=document.getElementById('dz-dock');
  const audio=document.getElementById('dz-audio');
  const sheet=document.getElementById('dz3-player-sheet');
  const openButton=document.getElementById('dock-ir');
  if(!root||!audio||!sheet||!openButton)return;
  const byId=id=>document.getElementById(id);
  const play=byId('dock-play');
  const next=byId('dock-next');
  const previous=byId('dock-prev');
  const progress=byId('dz3-sheet-progress');
  const status=byId('dz3-sheet-status');
  const closeButton=byId('dz3-sheet-close');
  const backdrop=byId('dz3-sheet-backdrop');
  const sheetPlay=byId('dz3-sheet-play');
  const sheetNext=byId('dz3-sheet-next');
  const sheetPrevious=byId('dz3-sheet-prev');
  let previouslyFocused=null;
  let expanded=false;
  const MAX_SECONDS=90;

  function track(){
    const title=byId('dock-titulo')?.textContent?.trim();
    const album=byId('dock-album')?.textContent?.trim()||'';
    return (window.DZ_FALLBACK||[]).find(item=>item.titulo===title && (!item.album || album.includes(item.album)))||null;
  }
  function formatSeconds(time){
    const seconds=Math.max(0,Math.floor(Number.isFinite(time)?time:0));
    return Math.floor(seconds/60)+':'+String(seconds%60).padStart(2,'0');
  }
  function sync(){
    const label=byId('dock-titulo')?.textContent?.trim()||'Diezell';
    const subtitle=byId('dock-album')?.textContent?.trim()||'Adelantos de 90 segundos';
    byId('dz3-sheet-title').textContent=label;
    byId('dz3-sheet-album').textContent=subtitle;
    sheetPlay.textContent=audio.paused?'▶':'⏸';
    sheetPlay.setAttribute('aria-label',audio.paused?'Reproducir adelanto':'Pausar adelanto');
    const originalCover=byId('dock-cover');
    const sheetCover=byId('dz3-sheet-cover');
    const sheetFallback=byId('dz3-sheet-cover-dzl');
    if(originalCover&&!originalCover.hidden){
      if(sheetCover.getAttribute('src')!==originalCover.getAttribute('src'))sheetCover.setAttribute('src',originalCover.getAttribute('src'));
      sheetCover.hidden=false;sheetFallback.hidden=true;
    } else {
      sheetCover.hidden=true;sheetFallback.hidden=false;
    }
    const t=Math.min(MAX_SECONDS,audio.currentTime||0);
    const percent=Math.round(t/MAX_SECONDS*100);
    byId('dz3-sheet-elapsed').textContent=formatSeconds(t);
    byId('dz3-sheet-progress-fill').style.width=percent+'%';
    progress.setAttribute('aria-valuenow',String(percent));
    progress.setAttribute('aria-valuetext',formatSeconds(t)+' de 1:30');
    const item=track();
    if(item){
      if(item.spotify) byId('dz3-sheet-spotify').href=item.spotify;
      else byId('dz3-sheet-spotify').removeAttribute('href');
      if(item.youtube) byId('dz3-sheet-youtube').href=item.youtube;
      else byId('dz3-sheet-youtube').removeAttribute('href');
      byId('dz3-sheet-spotify').hidden=!item.spotify;
      byId('dz3-sheet-youtube').hidden=!item.youtube;
    } else {
      // Never show links for a different song while metadata is loading.
      ['dz3-sheet-spotify','dz3-sheet-youtube'].forEach(id=>{
        const link=byId(id);
        link.removeAttribute('href');
        link.hidden=true;
      });
    }
    const ended=audio.ended||(!audio.paused?false:t>=MAX_SECONDS-.05);
    byId('dz3-sheet-cta').hidden=!ended;
  }
  function setStatus(message){
    if(!status)return;
    status.textContent=message||'';
    status.hidden=!message;
  }
  function open(){
    if(expanded)return;
    previouslyFocused=document.activeElement;
    expanded=true;sheet.hidden=false;
    document.body.classList.add('dz3-sheet-open');
    sync();
    closeButton.focus();
  }
  function close(){
    if(!expanded)return;
    sheet.hidden=true;expanded=false;
    document.body.classList.remove('dz3-sheet-open');
    if(previouslyFocused&&previouslyFocused.focus)previouslyFocused.focus();
  }
  // Existing app.js uses dock-ir for page navigation. We retain the player engine,
  // but intercept this button so it opens the full view on any page.
  openButton.addEventListener('click',event=>{
    event.preventDefault();
    event.stopImmediatePropagation();
    open();
  },true);
  closeButton.addEventListener('click',close);
  backdrop.addEventListener('click',close);
  document.addEventListener('keydown',event=>{
    if(!expanded)return;
    if(event.key==='Escape'){event.preventDefault();close();return;}
    if(event.key!=='Tab')return;
    const controls=[...sheet.querySelectorAll('button:not([disabled]),a[href]:not([hidden]),[tabindex="0"]')].filter(el=>!el.hidden&&el.offsetParent!==null);
    if(!controls.length)return;
    const first=controls[0],last=controls[controls.length-1];
    if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
    else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
  });
  sheetPlay.addEventListener('click',()=>play?.click());
  sheetNext.addEventListener('click',()=>next?.click());
  sheetPrevious.addEventListener('click',()=>{
    // Music page has a visible previous control; other pages use the dock's
    // hidden previous control. Both delegate to the SAME app.js audio engine.
    const control=byId('dz-anterior')||previous;
    if(control)control.click();
    else setStatus('No se pudo cambiar al adelanto anterior.');
  });
  byId('dz3-sheet-next-after').addEventListener('click',()=>next?.click());
  function seek(frac){
    if(!audio.src)return;
    audio.currentTime=Math.min(MAX_SECONDS,Math.max(0,frac*MAX_SECONDS));
    // Seeking backwards must dismiss the finished-preview CTA immediately.
    // The app engine owns the primary CTA; this sheet has its own state.
    byId('dz3-sheet-cta').hidden=audio.currentTime<MAX_SECONDS-.05;
    sync();
  }
  progress.addEventListener('click',event=>{
    const box=progress.getBoundingClientRect();
    if(box.width>0)seek((event.clientX-box.left)/box.width);
  });
  progress.addEventListener('keydown',event=>{
    if(event.key==='ArrowRight'||event.key==='ArrowLeft'){
      event.preventDefault();
      seek((audio.currentTime+(event.key==='ArrowRight'?5:-5))/MAX_SECONDS);
    }
    if(event.key==='Home'){event.preventDefault();seek(0);}
    if(event.key==='End'){event.preventDefault();seek(1);}
  });
  ['play','pause','timeupdate','loadedmetadata','ended','emptied'].forEach(name=>audio.addEventListener(name,sync));
  audio.addEventListener('error',()=>{
    setStatus('Este adelanto no está disponible. Puedes escucharlo en Spotify o YouTube.');
    sync();
  });
  audio.addEventListener('playing',()=>setStatus(''));
  audio.addEventListener('abort',()=>setStatus(''));
  audio.addEventListener('loadstart',()=>setStatus(''));
  audio.addEventListener('stalled',()=>setStatus('El adelanto está tardando en cargar.'));
  const title=byId('dock-titulo');
  if(title){
    new MutationObserver(sync).observe(title,{childList:true,characterData:true,subtree:true});
  }
  // One listening engine only: external platforms are links, never embedded players.
  // This prevents a Spotify iframe from playing alongside the local 90 s preview.
  document.querySelectorAll('.dz3-album-embed').forEach(details=>{
    details.hidden=true;
  });
  if(!audio.src)setStatus('');
  sync();
})();
