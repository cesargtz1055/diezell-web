#!/usr/bin/env python3
"""Non-destructive editorial pass on the isolated /nuevo/ build.
Original ZIP content and JS remain untouched."""
from pathlib import Path
import re
import html

root=Path('site/nuevo')
pages={
 'escuchar.html':{
  'intro':'Explora los álbumes, encuentra una canción y escucha los adelantos disponibles. Las fichas conservan sus enlaces y créditos.',
  'nav':[('Álbumes','album-insania'),('Caótico','album-caotico')],
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
  'intro':'Consulta los registros históricos de crecimiento de Diezell. Las cifras deben interpretarse según la fecha y fuente de cada registro; no representan datos en tiempo real.',
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
    path.write_text(source,encoding='utf-8')
# Enhance song pages with a consistent context cue without rewriting lyrics or credits.
songs=list((root/'canciones').glob('*.html'))
for path in songs:
    source=path.read_text(encoding='utf-8')
    if '<h1' not in source.lower():continue
    source=re.sub(r'</h1\s*>',lambda m:m.group(0)+'<p class="dz-song-context">Ficha de canción · Escucha, información y enlaces relacionados</p>',source,count=1,flags=re.I)
    path.write_text(source,encoding='utf-8')
print('Editorially refined',len(pages),'main sections and',len(songs),'song files')
assert len(songs)>=27
