#!/usr/bin/env python3
"""Rebuild Band editorial page with the original roster, chronology and references."""
from pathlib import Path
from html import escape,unescape
import re
root=Path('site/nuevo')
source=Path('site/banda.html').read_text(encoding='utf-8')
page=(root/'banda.html').read_text(encoding='utf-8')
def inner(pattern,s):
    m=re.search(pattern,s,re.I)
    return m.group(1) if m else None
def plain(s):
    return unescape(re.sub(r'<[^>]+>','',s or '')).strip()
roster=inner(r'<ol class="roster">([\s\S]*?)</ol>',source)
assert roster
members=[]
for li in re.findall(r'<li>([\s\S]*?)</li>',roster):
    name=plain(inner(r'<h2[^>]*>([\s\S]*?)</h2>',li))
    role=plain(inner(r'<p class="miembro-rol">([\s\S]*?)</p>',li))
    initials=plain(inner(r'<span class="badge-iniciales">([^<]+)</span>',li))
    description=inner(r'<p>([\s\S]*?)</p>',li) or ''
    if name:
        members.append('<article class="dz3-member"><span class="dz3-member-initials" aria-hidden="true">'+escape(initials)+'</span><div><h3>'+escape(name)+'</h3><p class="dz3-member-role">'+escape(role)+'</p><p>'+description+'</p></div></article>')
assert len(members)==4, f'Expected 4 sourced members: {len(members)}'
timeline=inner(r'<ol class="timeline">([\s\S]*?)</ol>',source)
assert timeline
events=[]
for li in re.findall(r'<li>([\s\S]*?)</li>',timeline):
    year=plain(inner(r'<span class="anio">([^<]+)</span>',li))
    body=inner(r'<p>([\s\S]*?)</p>',li)
    if year and body: events.append('<li><time>'+escape(year)+'</time><p>'+body+'</p></li>')
assert len(events)>=7, f'Expected complete timeline: {len(events)}'
press=inner(r'<h3[^>]*>Prensa</h3>\s*<ul class="lista">([\s\S]*?)</ul>',source)
facts=inner(r'<h3[^>]*>Datos curiosos</h3>\s*<ul class="lista">([\s\S]*?)</ul>',source)
assert press and facts
press_items=re.findall(r'<li>([\s\S]*?)</li>',press)
facts_items=re.findall(r'<li>([\s\S]*?)</li>',facts)
assert len(press_items)>=6 and len(facts_items)>=5
page=page.replace('<!-- DZ3_MEMBERS -->','\n'.join(members))
page=page.replace('<!-- DZ3_TIMELINE -->','\n'.join(events))
page=page.replace('<!-- DZ3_PRESS -->','\n'.join('<li>'+item+'</li>' for item in press_items))
page=page.replace('<!-- DZ3_FACTS -->','\n'.join('<li>'+item+'</li>' for item in facts_items))
assert '<!-- DZ3_' not in page
(root/'banda.html').write_text(page,encoding='utf-8')
print('Rebuilt Band:',len(members),'members,',len(events),'timeline years,',len(press_items),'press sources')
