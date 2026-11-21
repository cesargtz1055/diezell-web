#!/usr/bin/env python3
"""Build each of the 27 song pages anew, retaining its own sourced data and links."""
from pathlib import Path
from html import escape,unescape
import re

src=Path('site/canciones')
dst=Path('site/nuevo/canciones')
files=sorted(src.glob('*.html'))
assert len(files)==27,f'Expected 27 song sources, got {len(files)}'

def cap(pattern,s,default=''):
    m=re.search(pattern,s,re.I)
    return m.group(1) if m else default

def plain(s):
    return unescape(re.sub(r'<[^>]+>','',s)).strip()

def safe_url(s):
    return escape(s,quote=True)

head='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0c1015"><meta name="robots" content="noindex,follow"><meta name="description" content="{description}"><title>{title} | Diezell</title><link rel="icon" href="../images/insania.jpg"><link rel="stylesheet" href="../dz-rebuild.css"><link rel="stylesheet" href="../dz-song.css"></head><body class="dz3 dz3-song" data-dz-cancion="{number}"><a class="dz3-skip" href="#contenido">Saltar al contenido</a>
<header class="dz3-header"><nav class="dz3-nav dz3-wrap" aria-label="Navegación principal"><a class="dz3-logo" href="../index.html" aria-label="Diezell, inicio">DIEZELL<span>.</span></a><button class="dz3-menu-toggle" type="button" aria-expanded="false" aria-controls="dz3-menu" aria-label="Abrir menú">Menú <span aria-hidden="true">☰</span></button><div class="dz3-menu" id="dz3-menu"><a href="../index.html">Inicio</a><a class="is-current" aria-current="page" href="../escuchar.html">Música</a><a href="../en-vivo.html">En vivo</a><a href="../banda.html">La banda</a><a href="../caoticos.html">Caóticos</a></div></nav></header>'''
foot='''</main><footer class="dz3-footer"><div class="dz3-wrap"><strong>DIEZELL.</strong><p>Archivo independiente creado por fans. No afiliado a la banda.</p><nav aria-label="Explorar"><a href="../escuchar.html">Discografía</a><a href="../en-vivo.html">Conciertos</a><a href="../banda.html">La banda</a></nav></div></footer><div id="dz-dock" hidden><audio id="dz-audio" preload="metadata"></audio></div><script src="../app.js" defer></script><script src="../dz-rebuild.js" defer></script></body></html>'''
count=0
for file in files:
    source=file.read_text(encoding='utf-8')
    title=plain(cap(r'<h1[^>]*>([\s\S]*?)</h1>',source))
    number=cap(r'<body[^>]*data-dz-cancion="([0-9]+)"',source)
    album=plain(cap(r'<p class="kicker">([\s\S]*?)</p>',source))
    duration=plain(cap(r'<p class="album-meta">([\s\S]*?)</p>',source))
    spotify=cap(r'<a[^>]*id="dz-spotify"[^>]*href="([^"]+)"',source)
    youtube=cap(r'<a[^>]*id="dz-youtube"[^>]*href="([^"]+)"',source)
    image=cap(r'<img[^>]*id="dz-cover"[^>]*src="([^"]+)"',source,'../images/insania.jpg')
    cover_tag=cap(r'(<img[^>]*id="dz-cover"[^>]*>)',source)
    cover_hidden=bool(re.search(r'\shidden(?:\s|>)',cover_tag))
    album_href=cap(r'<a href="(\.\./escuchar\.html#[^"]+)"',source,'../escuchar.html')
    assert title and number and spotify and youtube, str(file)
    assert number.isdigit() and 1<=int(number)<=27
    media='''<section class="dz3-song-player" id="reproductor" aria-labelledby="song-listen"><div class="dz3-wrap">
      <div class="dz3-section-heading"><p class="dz3-eyebrow">Escucha la canción</p><h2 id="song-listen">Un adelanto antes de seguir.</h2><p>Hasta 90 segundos en esta web. Para escucharla completa, abre la plataforma de la banda.</p></div>
      <div class="dz3-player" id="dz-player"><div class="dz3-now">
        <div class="dz-cover" id="dz-cover-wrap"><img id="dz-cover" src="{cover}" alt="Portada" width="110" height="110" {hidden}><span class="dz-cover-dzl" id="dz-cover-dzl" {placeholder}>DZL</span></div>
        <div class="dz3-now-text"><span class="dz3-playing-label">Adelanto seleccionado</span><strong id="dz-titulo">{title}</strong><span id="dz-album">Diezell · {album}</span></div><span class="dz-badge">90 s</span>
      </div><div class="dz3-player-bottom"><div class="dz-controls"><button class="dz-btn" id="dz-anterior" type="button" aria-label="Adelanto anterior">⏮</button><button class="dz-btn dz-btn--play" id="dz-play" type="button" aria-label="Reproducir o pausar">▶</button><button class="dz-btn" id="dz-siguiente" type="button" aria-label="Siguiente adelanto">⏭</button></div><div class="dz-progreso-row"><span class="dz-tiempo" id="dz-actual">0:00</span><div class="dz-progreso" id="dz-progreso" role="slider" aria-label="Progreso del adelanto" aria-valuemin="0" aria-valuemax="90" aria-valuenow="0" tabindex="0"><div class="dz-progreso-relleno" id="dz-progreso-relleno"></div></div><span class="dz-tiempo">1:30</span></div>
      <div class="dz3-player-links"><a class="dz-link" id="dz-spotify" href="{spotify}" target="_blank" rel="noopener">Spotify ↗</a><a class="dz-link" id="dz-youtube" href="{youtube}" target="_blank" rel="noopener">YouTube ↗</a></div><div class="dz-volumen"><label for="dz-vol">Volumen</label><input id="dz-vol" type="range" min="0" max="100" value="90"></div></div>
      <div class="dz-cta" id="dz-cta" hidden><p>Terminó el adelanto de <strong id="dz-cta-titulo">{title}</strong>.</p><div class="dz-cta-botones"><a class="dz-btn-cta" id="dz-cta-spotify" href="{spotify}" target="_blank" rel="noopener">Escuchar en Spotify ↗</a><a class="dz-btn-cta" id="dz-cta-youtube" href="{youtube}" target="_blank" rel="noopener">Ver en YouTube ↗</a><button class="dz-btn-cta" id="dz-cta-siguiente" type="button">Siguiente adelanto →</button></div></div><p id="dz3-player-feedback" class="dz3-player-feedback" role="status" aria-live="polite" hidden></p></div></div></section>'''.format(cover=safe_url(image),hidden='hidden' if cover_hidden else '',placeholder='' if cover_hidden else 'hidden',title=escape(title),album=escape(album),spotify=safe_url(spotify),youtube=safe_url(youtube))
    # Preserve only recorded song metrics; never manufacture a current counter.
    metrics=[]
    for part in re.findall(r'<p class="dato">([\s\S]*?)</p>',source):
        value=plain(cap(r'<span class="dato-num">([\s\S]*?)</span>',part))
        label=plain(cap(r'<span class="dato-label">([\s\S]*?)</span>',part))
        stamp=plain(cap(r'<span class="dato-note">([\s\S]*?)</span>',part))
        if value and label:
            metrics.append('<li><strong>'+escape(value)+'</strong><span>'+escape(label)+'</span><small>'+escape(stamp)+'</small></li>')
    stats=('''<section class="dz3-section dz3-wrap" id="registros" aria-labelledby="registros-title"><div class="dz3-section-heading"><p class="dz3-eyebrow">Historial, no tiempo real</p><h2 id="registros-title">Registros de esta canción.</h2><p>Cifras publicadas en fechas distintas. No representan reproducciones actuales.</p></div><ul class="dz3-song-metrics">'''+''.join(metrics)+'''</ul><p class="dz3-song-footnote"><a href="../crecimiento.html">Ver cómo se documentan las cifras ↗</a></p></section>''') if metrics else ''
    words=cap(r'<p class="lyric-big">([\s\S]*?)</p>',source)
    lyrics=cap(r'<a href="(https?://[^"]+)"[^>]*>Letra completa',words)
    lyrics_link=('<a href="'+safe_url(lyrics)+'" target="_blank" rel="noopener">Consultar letra completa ↗</a>') if lyrics else ''
    footer_section=cap(r'<section class="section" aria-label="Canción anterior y siguiente">([\s\S]*?)</section>',source)
    related=[]
    for href,label in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)</a>',footer_section):
        related.append('<a href="'+safe_url(href)+'">'+escape(plain(label))+'</a>')
    if not related: related=['<a href="../escuchar.html">Volver a Música ↗</a>']
    desc=f'{title}, de Diezell. Escucha un adelanto y consulta su álbum, referencias y registros históricos.'
    page=head.format(description=escape(desc,quote=True),title=escape(title),number=number)
    page+='''<main id="contenido"><section class="dz3-song-hero"><div class="dz3-wrap dz3-song-hero-grid"><div><nav class="dz3-song-crumb" aria-label="Ruta"><a href="../escuchar.html">Música</a><span aria-hidden="true">/</span><a href="'''+safe_url(album_href)+'''">'''+escape(album.split(' · ')[0])+'''</a></nav><p class="dz3-eyebrow">Ficha de canción · Diezell</p><h1>'''+escape(title)+'''</h1><p class="dz3-song-meta">'''+escape(album)+(' · '+escape(duration) if duration else '')+'''</p><a class="dz3-song-listen-link" href="#reproductor">Escuchar adelanto ↓</a></div><div class="dz3-song-art">'''+('<span class="dz3-song-placeholder">DIEZELL</span>' if cover_hidden else '<img src="'+safe_url(image)+'" alt="Portada de '+escape(album.split(' · ')[0],quote=True)+'" width="640" height="640">')+'''</div></div></section>'''
    page+=media
    page+='''<section class="dz3-section dz3-wrap" id="mas-de-esta-cancion" aria-labelledby="mas-title"><div class="dz3-section-heading"><p class="dz3-eyebrow">Sigue explorando</p><h2 id="mas-title">Dentro de la discografía.</h2><p>Esta canción tiene un lugar en el catálogo de Diezell. Puedes volver al álbum o descubrir otra canción.</p></div><nav class="dz3-song-related" aria-label="Canciones relacionadas">'''+''.join(related)+'''</nav>'''+('<p class="dz3-song-lyrics">'+lyrics_link+'</p>' if lyrics_link else '')+'''</section>'''
    page+=stats+foot
    assert page.count('id="dz-player"')==1 and page.count('id="dz-audio"')==1
    assert page.count('<h1>')==1
    (dst/file.name).write_text(page,encoding='utf-8')
    count+=1
assert count==27
print('Rebuilt',count,'song detail pages using individual title, album, cover, links, related songs, dated metrics')
