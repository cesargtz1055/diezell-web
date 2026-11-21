#!/usr/bin/env python3
"""Build En vivo from a completely new template, using only sourced archive data."""
from pathlib import Path
from html import escape, unescape
import re

root=Path('site/nuevo')
source=Path('site/en-vivo.html').read_text(encoding='utf-8')
template=(root/'en-vivo.html').read_text(encoding='utf-8')
tour=re.search(r'<ul class="tour-list">([\s\S]*?)</ul>',source)
assert tour, 'Original tour archive not found'
items=re.findall(r'<li>([\s\S]*?)</li>',tour.group(1))
assert len(items)==10, f'Expected ten archived announcements, found {len(items)}'
def text(value):
    return unescape(re.sub(r'<[^>]+>','',value)).strip()
def span(item,class_name):
    m=re.search(r'<span class="'+re.escape(class_name)+r'">([\s\S]*?)</span>',item)
    return m.group(1) if m else ''
cards=[]
for item in items:
    date=text(span(item,'tour-fecha'))
    place=span(item,'tour-lugar')
    city_match=re.search(r'<strong>(.*?)</strong>',place)
    city=text(city_match.group(1)) if city_match else 'Ciudad por confirmar'
    detail=text(re.sub(r'<strong>[\s\S]*?</strong>\s*','',place,count=1)).lstrip('— ').strip()
    pending=('TBA' in date or 'anunciar' in date.lower())
    cls=' dz3-tour-date--pending' if pending else ''
    badge='Sin fecha confirmada' if pending else 'Concierto registrado'
    cards.append('<article class="dz3-tour-date'+cls+'"'+(' id="ultimo-show"' if city=='Monterrey' and '13 NOV' in date else '')+'>'
                 +'<time>'+escape(date)+'</time><div><h3>'+escape(city)+'</h3>'
                 +'<p>'+escape(detail)+'</p><span class="dz3-tour-label">'+badge+'</span></div></article>')
figures=re.findall(r'<figure class="foto-wrap"([^>]*)>([\s\S]*?)</figure>',source)
assert len(figures)==10, f'Expected all ten original photos, found {len(figures)}'
gallery=[]
for attrs,figure in figures:
    id_match=re.search(r'\bid="([^"]+)"',attrs)
    preserved_id=id_match.group(1) if id_match else ''
    id_attr=' id="'+escape(preserved_id,quote=True)+'"' if preserved_id else ''
    img=re.search(r'<img\s+[^>]*src="([^"]+)"[^>]*>',figure)
    if not img: continue
    src=img.group(1)
    tag=img.group(0)
    alt=re.search(r'alt="([^"]*)"',tag)
    description=unescape(alt.group(1)) if alt else 'Diezell en vivo'
    anchor=re.search(r'<a\s+href="(https?://[^"]+)"',figure)
    href=anchor.group(1) if anchor else None
    link=('<a href="'+escape(href,quote=True)+'" target="_blank" rel="noopener">Ver fuente ↗</a>') if href else ''
    credit_match=re.search(r'<div class="foto-popover"[^>]*>[\s\S]*?<p>([\s\S]*?)</p>',figure)
    credit=credit_match.group(1) if credit_match else ''
    details=('<details class="dz3-photo-credit"><summary>Fotografía y créditos</summary><div>'+credit+'</div></details>') if credit else ''
    gallery.append('<figure class="dz3-photo"'+id_attr+'><img src="'+escape(src,quote=True)+'" alt="'+escape(description,quote=True)+'" loading="lazy" width="680" height="850">'
                   +'<figcaption><span>'+escape(description)+'</span>'+details+('' if details else link)+'</figcaption></figure>')
template=template.replace('<!-- DZ3_TOUR -->','\n'.join(cards))
template=template.replace('<!-- DZ3_GALLERY -->','\n'.join(gallery))
assert 'DZ3_TOUR' not in template and 'DZ3_GALLERY' not in template
assert template.count('class="dz3-tour-date')==10
assert template.count('class="dz3-photo"')==len(gallery)
(root/'en-vivo.html').write_text(template,encoding='utf-8')
print('Rebuilt En vivo:',len(cards),'archive announcements,',len(gallery),'documented photographs')
