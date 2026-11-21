#!/usr/bin/env python3
"""Rebuild the four individual member pages with their own sourced content and images."""
from pathlib import Path
from html import escape, unescape
import re
source_root=Path('site')
out_root=Path('site/nuevo')
slugs=('rene','bernie','emmash','mau')
assert all((source_root/('miembro-'+slug+'.html')).is_file() for slug in slugs)
def cap(regex,s):
    m=re.search(regex,s,re.I)
    return m.group(1) if m else ''
def plain(s):
    return unescape(re.sub(r'<[^>]*>','',s)).strip()
for slug in slugs:
    source=(source_root/('miembro-'+slug+'.html')).read_text(encoding='utf-8')
    name=plain(cap(r'<h1[^>]*>([\s\S]*?)</h1>',source))
    role=plain(cap(r'<p class="miembro-rol lead">([\s\S]*?)</p>',source))
    facts=cap(r'<h2>Lo que sabemos de él</h2>\s*<ul class="lista">([\s\S]*?)</ul>',source)
    assert name and role and facts
    bullet_items=re.findall(r'<li>([\s\S]*?)</li>',facts)
    assert bullet_items
    lead=plain(cap(r'</figure>\s*<p class="lead">([\s\S]*?)</p>',source))
    figures=re.findall(r'<figure class="foto-wrap[^"]*"[^>]*>([\s\S]*?)</figure>',source)
    assert figures
    photos=[]
    for fig in figures:
        img=cap(r'(<img[^>]*src="[^"]+"[^>]*>)',fig)
        src=cap(r'src="([^"]+)"',img)
        alt=plain(cap(r'alt="([^"]*)"',img)) or (name+' en vivo')
        href=cap(r'<a href="(https?://[^"]+)"',fig)
        photos.append('<figure class="dz3-member-photo"><img src="'+escape(src,quote=True)+'" alt="'+escape(alt,quote=True)+'" width="720" height="900" loading="lazy"><figcaption>'+escape(alt)+(' · <a href="'+escape(href,quote=True)+'" target="_blank" rel="noopener">Fuente ↗</a>' if href else '')+'</figcaption></figure>')
    # External profile links already present in original content.
    social=re.findall(r'<a href="(https://www\.instagram\.com/[^"]+)"[^>]*>([\s\S]*?)</a>',source)
    social_unique=[]
    for href,label in social:
        if href not in [x[0] for x in social_unique] and 'p/' not in href:
            social_unique.append((href,plain(label)))
    social_html=(''.join('<a href="'+escape(href,quote=True)+'" target="_blank" rel="noopener">'+escape(label)+' ↗</a>' for href,label in social_unique)) or '<p>Consulta los canales oficiales de la banda.</p>'
    details=plain(cap(r'<p class="fuente-nota">([\s\S]*?)</p>',source))
    caveat=('<details class="dz3-member-caveat"><summary>Precisiones del archivo</summary><p>'+escape(details)+'</p></details>') if details else ''
    title=escape(name)
    page='''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0c1015"><meta name="robots" content="noindex,follow"><meta name="description" content="'''+escape(name+', integrante de Diezell. Biografía, fotografías y fuentes.',quote=True)+'''"><title>'''+title+''' | Diezell</title><link rel="icon" href="images/insania.jpg"><link rel="stylesheet" href="dz-rebuild.css"><link rel="stylesheet" href="dz-member.css"></head><body class="dz3 dz3-member-page"><a class="dz3-skip" href="#contenido">Saltar al contenido</a>
<header class="dz3-header"><nav class="dz3-nav dz3-wrap" aria-label="Navegación principal"><a class="dz3-logo" href="index.html" aria-label="Diezell, inicio">DIEZELL<span>.</span></a><button class="dz3-menu-toggle" type="button" aria-expanded="false" aria-controls="dz3-menu" aria-label="Abrir menú">Menú <span aria-hidden="true">☰</span></button><div class="dz3-menu" id="dz3-menu"><a href="index.html">Inicio</a><a href="escuchar.html">Música</a><a href="en-vivo.html">En vivo</a><a class="is-current" href="banda.html">La banda</a><a href="caoticos.html">Caóticos</a></div></nav></header>
<main id="contenido"><section class="dz3-member-hero"><div class="dz3-wrap dz3-member-hero-grid"><div><nav class="dz3-member-crumb" aria-label="Ruta"><a href="banda.html">La banda</a><span aria-hidden="true">/</span><span>Integrante</span></nav><p class="dz3-eyebrow">Diezell · Integrantes</p><h1>'''+title+'''</h1><p class="dz3-member-role">'''+escape(role)+'''</p><p class="dz3-member-desc">'''+escape(lead if lead else (role+' de Diezell.'))+'''</p><a class="dz3-member-back" href="banda.html#integrantes">Ver todos los integrantes ↗</a></div><img src="'''+escape(cap(r'src="([^"]+)"',figures[0]),quote=True)+'''" alt="" width="1000" height="1200"></div></section>
<section class="dz3-section dz3-wrap" id="perfil"><div class="dz3-section-heading"><p class="dz3-eyebrow">Perfil</p><h2>Su lugar en la banda.</h2></div><ul class="dz3-member-facts">'''+''.join('<li>'+item+'</li>' for item in bullet_items)+'''</ul>'''+caveat+'''</section>
<section class="dz3-section dz3-wrap" id="fotos"><div class="dz3-section-heading"><p class="dz3-eyebrow">En escena</p><h2>Momentos documentados.</h2></div><div class="dz3-member-gallery">'''+''.join(photos)+'''</div></section>
<section class="dz3-section dz3-wrap" id="redes"><div class="dz3-section-heading"><p class="dz3-eyebrow">Más información</p><h2>Enlaces del archivo.</h2></div><div class="dz3-member-social">'''+social_html+'''<a href="en-vivo.html">Conciertos documentados ↗</a></div></section></main><footer class="dz3-footer"><div class="dz3-wrap"><strong>DIEZELL.</strong><p>Archivo independiente creado por fans. No afiliado a la banda.</p><nav aria-label="Explorar"><a href="banda.html">La banda</a><a href="escuchar.html">Música</a><a href="en-vivo.html">Conciertos</a></nav></div></footer><script src="dz-rebuild.js" defer></script></body></html>'''
    assert page.count('<h1>')==1 and 'stripes' not in page
    (out_root/('miembro-'+slug+'.html')).write_text(page,encoding='utf-8')
    print('Rebuilt member',slug,':',name,'with',len(bullet_items),'facts and',len(photos),'photos')
