#!/usr/bin/env python3
"""Restore valuable site-wide music controls without reverting the new layouts."""
from pathlib import Path
import re

root=Path('site/nuevo')
pages=sorted(root.rglob('*.html'))
assert len(pages)==37
def svg(paths):
    return '<svg viewBox="0 0 24 24" aria-hidden="true">'+paths+'</svg>'
icons={
 'Inicio':svg('<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10.5V21h13V10.5"/><path d="M10 21v-7h4v7"/>'),
 'Música':svg('<path d="M3.5 14a8.5 8.5 0 0 1 17 0"/><rect x="3  y="13" width="4.5" height="7" rx="1.5"/><rect x="16.5" y="13" width="4.5" height="7" rx="1.5"/>'),
 'En vivo':svg('<rect x="2.5" y="6" width="13" height="12" rx="2"/><path d="M15.5 10.5 21 7v10l-5.5-3.5"/>'),
 'Caóticos':svg('<path d="m12 3 2.7 5.8 6.3.7-4.7 4.3 1.3 6.2-5.6-3.2L6.4 20l1.3-6.2L3 9.5l6.3-.7z"/>'),
 'Banda':svg('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 5.5a3.5 3.5 0 0 1 0 5.5"/><path d="M17.5 14.5a6.5 6.5 0 0 1 4 5.5"/>')
}
mini='''<div class="dz3-mini" id="dz-dock" role="region" aria-label="Reproductor inferior de Diezell">
 <audio id="dz-audio" preload="metadata"></audio>
 <div class="dz3-mini-progress" aria-hidden="true"><div id="dock-relleno" class="dz3-mini-progress-fill"></div></div>
 <div class="dz3-mini-inner">
  <button class="dz3-mini-open" id="dock-ir" type="button" aria-label="Abrir reproductor completo">
    <span class="dz3-mini-cover"><img id="dock-cover" src="images/insania.jpg" alt="" width="48" height="48"><span id="dock-cover-dzl" hidden>DZL</span></span>
    <span class="dz3-mini-info"><strong id="dock-titulo">Suspensión…</strong><span id="dock-album">Diezell · INSANIA · Adelanto 1:30</span></span>
  </button>
  <button class="dz3-mini-icon" id="dock-play" type="button" aria-label="Reproducir o pausar">▶</button>
  <button class="dz3-mini-icon" id="dock-next" type="button" aria-label="Siguiente adelanto">⏭</button>
 </div>
 <div id="dock-progreso" role="slider" aria-label="Progreso del adelanto" aria-valuemin="0" aria-valuemax="90" aria-valuenow="0" tabindex="0" hidden></div>
</div>'''
sheet='''<section class="dz3-sheet" id="dz3-player-sheet" role="dialog" aria-modal="true" aria-labelledby="dz3-sheet-heading" hidden>
 <button class="dz3-sheet-backdrop" id="dz3-sheet-backdrop" type="button" tabindex="-1" aria-label="Cerrar reproductor"></button>
 <div class="dz3-sheet-panel">
  <div class="dz3-sheet-head"><span class="dz3-sheet-eyebrow" id="dz3-sheet-heading">Reproductor de Diezell</span>
   <button class="dz3-sheet-close" type="button" id="dz3-sheet-close" aria-label="Cerrar reproductor">×</button></div>
  <div class="dz3-sheet-cover"><img src="images/insania.jpg" id="dz3-sheet-cover" alt="" width="240" height="240"><span id="dz3-sheet-cover-dzl" hidden>DZL</span></div>
  <div class="dz3-sheet-meta"><strong id="dz3-sheet-title">Suspensión…</strong><span id="dz3-sheet-album">Diezell · INSANIA</span></div>
  <div class="dz3-sheet-controls">
   <button id="dz3-sheet-prev" type="button" aria-label="Adelanto anterior">⏮</button>
   <button id="dz3-sheet-play" type="button" aria-label="Reproducir adelanto">▶</button>
   <button id="dz3-sheet-next" type="button" aria-label="Siguiente adelanto">⏭</button>
  </div>
  <div class="dz3-sheet-progress-row">
   <span id="dz3-sheet-elapsed">0:00</span>
   <div id="dz3-sheet-progress" class="dz3-sheet-progress" role="slider" tabindex="0" aria-label="Progreso del adelanto" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div id="dz3-sheet-progress-fill" class="dz3-sheet-progress-fill"></div></div>
   <span>1:30</span>
  </div>
  <div class="dz3-sheet-links"><a id="dz3-sheet-spotify" href="https://open.spotify.com/artist/2mEQCZzgLbG0mWCwaAEb3g" target="_blank" rel="noopener">Spotify ↗</a><a id="dz3-sheet-youtube" href="https://www.youtube.com/@diezellmx" target="_blank" rel="noopener">YouTube ↗</a></div>
  <div id="dz3-sheet-cta" class="dz3-sheet-cta" hidden><p>Terminó el adelanto. <strong>La canción completa está en las plataformas de la banda.</strong></p><button id="dz3-sheet-next-after" type="button">Siguiente adelanto →</button></div>
  <p id="dz3-sheet-status" class="dz3-sheet-note" role="status" aria-live="polite" hidden></p>
  <p class="dz3-sheet-note">Adelantos de máximo 90 segundos. Sin reproducción automática.</p>
  <button id="dock-prev" type="button" aria-label="Canción anterior" hidden></button>
 </div>
</section>'''
names=[('Inicio','index.html'),('Música','escuchar.html'),('En vivo','en-vivo.html'),('Caóticos','caoticos.html'),('Banda','banda.html')]
for page in pages:
    depth=len(page.relative_to(root).parts)-1
    prefix='../'*depth
    name=page.name
    active=('Música' if depth or name=='escuchar.html'
            else 'Banda' if name.startswith('miembro-') or name=='banda.html'
            else {'index.html':'Inicio','en-vivo.html':'En vivo','caoticos.html':'Caóticos'}.get(name,''))
    nav='<nav class="dz3-tabbar" aria-label="Navegación inferior móvil">'+''.join(
        '<a href="'+prefix+url+'"'+(' aria-current="page"' if title==active else '')+'>'+icons[title]+'<span>'+title+'</span></a>'
        for title,url in names)+'</nav>'
    content=page.read_text(encoding='utf-8')
    assert 'id="dz3-player-sheet"' not in content,(name,'Duplicate sheet')
    if '<div id="dz-dock" hidden><audio id="dz-audio" preload="metadata"></audio></div>' in content:
        content=content.replace('<div id="dz-dock" hidden><audio id="dz-audio" preload="metadata"></audio></div>',
            mini.replace('src="images/','src="'+prefix+'images/'))
    else:
        assert 'id="dz-dock"' not in content and 'id="dz-audio"' not in content,(name,'Unexpected audio source')
        content=content.replace('</body>',mini.replace('src="images/','src="'+prefix+'images/')+'</body>',1)
    assert content.count('id="dz-audio"')==1 and content.count('id="dz-dock"')==1,(name,'Duplicate audio/dock')
    inject=nav+sheet.replace('src="images/','src="'+prefix+'images/')
    content=content.replace('</body>',inject+'</body>',1)
    # Don't add a second copy of the original engine to the Music and song pages.
    if not re.search(r'<script[^>]*src=["\']'+re.escape(prefix)+r'app\.js',content):
        content=content.replace('</body>','<script src="'+prefix+'app.js" defer></script></body>',1)
    content=content.replace('</body>','<script src="'+prefix+'dz-dock.js" defer></script></body>',1)
    content=content.replace('</head>','<link rel="stylesheet" href="'+prefix+'dz-dock.css"></head>',1)
    assert 'dz-dock.css' in content and 'dz-dock.js' in content
    assert content.count('id="dz3-player-sheet"')==1
    assert content.count('id="dock-play"')==1
    assert content.count('id="dock-next"')==1
    assert content.count('id="dock-ir"')==1
    assert content.count('id="dock-prev"')==1
    page.write_text(content,encoding='utf-8')
# Patch only the isolated deployed player's engine; never mutate original main-site JS.
engine=root/'app.js'
source=engine.read_text(encoding='utf-8')
needle="    enlazar('dock-next', function () { cargar(DZ.indice + 1, true); });"
assert needle in source
source=source.replace(needle,needle+"\n    enlazar('dock-prev', function () { cargar(DZ.indice - 1, true); });")
source=source.replace('    function cargar(i, reproducir) {\n',
 '''    function cargar(i, reproducir) {
      if (!DZ.canciones || !DZ.canciones.length) return;
''')
source=source.replace('    function togglePlay() {\n',
 '''    function togglePlay() {
      if (!DZ.canciones || !DZ.canciones.length) return;
''')
source=source.replace('      DZ.indice = (i + DZ.canciones.length) % DZ.canciones.length;\n',
 '''      DZ.indice = (i + DZ.canciones.length) % DZ.canciones.length;
      try { sessionStorage.setItem('dz3-track-index', String(DZ.indice)); } catch (e) {}
''')
original="      var inicio = parseInt((document.body && document.body.getAttribute('data-dz-cancion')) || '1', 10);"
assert original in source
replacement='''      var remembered = '1';
      try {
        var rememberedIndex = parseInt(sessionStorage.getItem('dz3-track-index'), 10);
        if (isFinite(rememberedIndex) && rememberedIndex >= 0) remembered = String(rememberedIndex + 1);
      } catch (e) {}
      var inicio = parseInt((document.body && document.body.getAttribute('data-dz-cancion')) || remembered, 10);'''
source=source.replace(original,replacement)
assert source.count("enlazar('dock-prev'")==1
engine.write_text(source,encoding='utf-8')
print('Restored the bottom player, full sheet, 5-item mobile navigation and 90-second engine on',len(pages),'pages')
