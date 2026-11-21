#!/usr/bin/env python3
"""Non-destructive editorial pass on the isolated /nuevo/ build.
Original ZIP content and JS remain untouched."""
from pathlib import Path
import re
import html

root=Path('site/nuevo')
pages={
 'escuchar.html':{
  'intro':'Explora álbumes y sencillos, escucha adelantos y conoce la historia de cada canción.',
  'nav':[('Álbumes','album-insania'),('Caótico','album-caotico'),('Escuchar adelantos','reproductor')],
  'labels':{'Reproductor':'Escucha y explora','Sencillos':'Canciones y sencillos'}},
 'en-vivo.html':{
  'intro':'Conoce los conciertos y registros audiovisuales disponibles en el archivo. Las fotografías y videos documentan presentaciones pasadas.',
  'nav':[('Archivo de gira','archivo'),('Fotografías','fotos')],
  'labels':{'Diez fotos en vivo':'Fotografías de conciertos','El video':'Video en vivo','Insania Tour 2026 · Archivo':'Archivo de INSANIA Tour 2026'}},
 'banda.html':{
  'intro':'Conoce a los integrantes, la historia y los registros disponibles de Diezell.',
  'nav':[('Historia','historia'),('Integrantes','integrantes')],
  'labels':{'Datos curiosos':'Detalles de la banda'}},
 'caoticos.html':{
  'intro':'Caóticos es el nombre con el que se identifica la comunidad de seguidores de Diezell. Aquí reunimos sus historias y expresiones.',
  'nav':[],
  'labels':{'El ritual de las luces azules':'El ritual de las luces azules','Cuentas de fans':'Cuentas de la comunidad'}},
 'crecimiento.html':{
  'intro':'Consulta los registros históricos de crecimiento de Diezell. Cada gráfica permite comparar registros históricos; revisa la fecha y la fuente antes de sacar conclusiones.',
  'nav':[],
  'labels':{'Los que más comentan':'Actividad registrada en comentarios'}},
}
def add_intro(source,config):
    m=re.search(r'</h1\s*>',source,re.I)
    if not m: return source
    links=''
    # Avoid fake anchors: links are only added when IDs are present in the actual page.
    for label,anchor in config['nav']:
        if re.search(r'id=["\']'+re.escape(anchor)+r'["\']',source,re.I):
            links+=f'<a href="#{anchor}">{html.escape(label)}</a>'
    block='<div class="dz-editorial-intro"><p>'+html.escape(config['intro'])+'</p>'
    if links:block+='<nav class="dz-section-nav" aria-label="En esta página">'+links+'</nav>'
    block+='</div>'
    return source[:m.end()]+block+source[m.end():]
def replace_headings(source,labels):
    for old,new in labels.items():
        if old==new:continue
        pattern=r'(<h[23]\b[^>]*>\s*)'+re.escape(old)+r'(\s*</h[23]>)'
        source=re.sub(pattern,lambda m:m.group(1)+new+m.group(2),source,flags=re.I)
    return source
for name,config in pages.items():
    path=root/name
    if not path.exists():raise SystemExit(f'Missing expected page {path}')
    source=path.read_text(encoding='utf-8')
    if name=='escuchar.html':
        # One visible player on Music: keep the audio element and JS bound to
        # the hidden dock; controls remain available in the full player.
        source=source.replace('<body>', '<body class="dz-music-page">', 1)
        source=source.replace('Primero INSANIA, luego Caótico, luego los sencillos.', 'Canciones, álbumes y adelantos en un solo lugar.')
    source=replace_headings(source,config['labels'])
    source=add_intro(source,config)
    if name=='caoticos.html':
        # Keep the historic slogan visible while making the H1 intelligible.
        source=re.sub(r'(<h1\b[^>]*>)[\s\S]*?(</h1>)',r'\g<1>Caóticos\g<2><p class="dz-page-slogan">Unidos, jamás serán vencidos.</p>',source,count=1,flags=re.I)
    if name=='caoticos.html':
        source=source.replace('Unirme en Instagram','Ver la comunidad en Instagram')
        source=source.replace('29 SEP 2026 · 3.er aniversario · Luces azules 100% · Días Felices: Los Lunes · @caoticosmty','Tradiciones, encuentros y recuerdos de los fans.')
    if name=='en-vivo.html':
        source=source.replace('No hay fechas anunciadas por ahora — cuando la banda publique una, aparecerá aquí.','Este apartado reúne presentaciones documentadas. Para próximas fechas, consulta los canales de la banda.')
        source=source.replace('Último show','Concierto documentado')
        source=source.replace('Lo último que tocaron, en fotos y video.','Conciertos, fotografías y videos que forman parte del archivo.')
    if name=='crecimiento.html':
        source=source.replace('Cada cifra que ves aquí se guardó con su fecha y su fuente. Nada se borra: cuando un número cambia, el viejo queda y el nuevo se suma. Así se ve crecer a una banda.','Compara la evolución de Diezell con registros fechados y fuentes identificadas.')
        source=source.replace('Los que más comentan','Actividad en comentarios')
        source=source.replace('Lo que dicen los números','Claves de la evolución')
    if name=='banda.html':
        source=source.replace('<h1>Banda</h1>','<h1>La banda</h1>')
    path.write_text(source,encoding='utf-8')
# The homepage is an editorial gateway, not a live analytics dashboard.
home=root/'index.html'
if home.exists():
    source=home.read_text(encoding='utf-8')
    source=source.replace('Unirme a los Caóticos','Conocer a los Caóticos')
    source=source.replace('VINVSNI','DIEZELL')
    source=source.replace('Portadas oficiales de Spotify · Datos de Spotify del 15 nov 2026.','Archivo independiente de fans · Consulta las fuentes en cada sección.')
    source=source.replace('La banda sigue creciendo','Diezell en cifras')
    source=source.replace('Datos · 15 nov 2026','Archivo de estadísticas · Último registro identificado: noviembre de 2026')
    source=source.replace('Diezell en números →','Consultar gráficas y fuentes →')
    # Preserve factual figures and links but reduce the visual dominance of stale metrics.
    source=source.replace('section datos-strip dark','section datos-strip dark dz-data-secondary')
    home.write_text(source,encoding='utf-8')
# On Music, listening is a contextual tool, not the first thing in the reading order.
music=root/'escuchar.html'
if music.exists():
    source=music.read_text(encoding='utf-8')
    match=re.search(r'<section\b[^>]*\bid="reproductor"[^>]*>[\s\S]*?</section>',source,re.I)
    if match:
        player=match.group(0)
        source=source[:match.start()]+source[match.end():]
        close=source.lower().find('</main>')
        if close!=-1:
            source=source[:close]+player+chr(10)+source[close:]
    source=source.replace('Escucha y explora','Reproductor de adelantos')
    music.write_text(source,encoding='utf-8')
# Do not show internal production messages on the new editorial homepage.
# The root index is purpose-built, so remove the prototype-only warning.
# Enhance song pages with a consistent context cue without rewriting lyrics or credits.
songs=list((root/'canciones').glob('*.html'))
for path in songs:
    source=path.read_text(encoding='utf-8')
    if '<h1' not in source.lower():continue
    source=re.sub(r'</h1\s*>',lambda m:m.group(0)+'<p class="dz-song-context">Ficha de canción · Escucha, información y enlaces relacionados</p>',source,count=1,flags=re.I)
    path.write_text(source,encoding='utf-8')
print('Editorially refined',len(pages),'main sections and',len(songs),'song files')
assert len(songs)>=27
