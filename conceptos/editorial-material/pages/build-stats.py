#!/usr/bin/env python3
"""Preserve the existing audited data renderer while rebuilding its entire UI."""
from pathlib import Path
import re
root=Path('site/nuevo')
source=Path('site/crecimiento.html').read_text(encoding='utf-8')
match=re.search(r'<script>\s*([\s\S]*?)\s*</script>',source,re.I)
assert match,'Data renderer missing from original'
engine=match.group(1).strip()
assert 'datos/ledger/ledger.json' in engine
assert 'grafica-oyentes' in engine and 'grafica-seguidores' in engine
# Make failures comprehensible rather than exposing internal file paths or HTTP details.
engine=engine.replace('El archivo datos/ledger/ledger.json no se pudo leer desde esta página (" + err.message + "). " +\n        "La página necesita servirse por HTTP, como el resto del sitio.','Los registros no están disponibles en este momento. Vuelve a consultar esta sección más tarde.')
(root/'dz-stats-engine.js').write_text(engine+'\n',encoding='utf-8')
page=(root/'crecimiento.html').read_text(encoding='utf-8')
assert 'id="grafica-oyentes"' in page and 'id="tabla-archivo"' in page
assert 'id="lista-menciones"' in page and 'id="lista-comentaristas"' in page
print('Rebuilt Stats with original historical graph renderer and linked ledger')
