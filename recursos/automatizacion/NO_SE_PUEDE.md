# NO SE PUEDE — Diezell, 20 nov 2026

Corto y directo: lo que se intentó de verdad y no tiene vía sin
cuentas, sin logins y sin que Cesar cree nada. Con evidencia de
cada intento (20 nov 2026, desde esta máquina).

## Fuentes cerradas

- **Instagram (perfil, posts, historias)**: 5 vías probadas, todas
  fallan. `web_profile_info` → 429; `?__a=1` → error 1357055;
  `ddinstagram.com` → sin conexión; Picuki → 403 Cloudflare;
  `/embed/` → 200 pero cáscara JS sin seguidores ni posts.
  Historias exigen login. Sin cuenta no hay vía.
- **TikTok por video**: el perfil trae conteos (seguidores,
  videos, likes totales) pero `itemList` viene vacío;
  `/api/post/item_list/` → 0 bytes sin sesión. Sin login no hay
  stats por video.
- **Reddit**: `.json` → 403 en www, api y old; old redirige a
  login. Pushshift: `search.pullpush.io` sin conexión,
  `api.pullpush.io` 404, `undelete` 403 Cloudflare. Reddit ya
  exige OAuth para `.json` anónimo.
- **setlist.fm**: API sin clave → 403. La web da 202 vacía
  (anti-bot). La API exige clave gratuita, y la clave exige
  cuenta en setlist.fm. Nadie crea esa cuenta.
- **Seguidores/likes de Facebook**: el plugin público de página
  trae los últimos 5 posts con fecha y texto, pero 0
  coincidencias de `follower_count`, `fan_count` y `like_count`,
  y no pagina. Los posts sí se capturan (`facebook_plugin.py`);
  los seguidores/likes no.
- **Bandsintown**: 403.
- **Google Trends**: explore 429 sin cookies; RSS genérico.
  Cerrado, fuera de `run_daily.sh`.

## Datos que no se pueden tener frescos

- **Oyentes mensuales de Spotify al día**: no están en ninguna
  API pública gratuita. La única ruta es Music Metrics Vault, y
  su página no se actualiza desde el 16 nov 2026 (44,147
  oyentes / 16,525 seguidores). La gráfica termina el 16 nov
  hasta que esa página se actualice. El refresh Livewire se
  colgó 90 s y no se reintenta sin aprobación.
- **Streams totales 9.7M (Viberate)**: ese número no existe en
  el ledger (ningún registro con ese valor). Viberate da 403 a
  los colectores y su página tiene texto generado sin verificar.
  Fuente de baja confianza; no se usa.
- **Comentarios de YouTube frescos**: el colector fallaba por
  límite de YouTube (3 cortes seguidos), pero se recuperó solo
  en el corte de verificación del 20 nov por la noche: 67
  comentarios nuevos, 0 errores; total 439. El límite es
  intermitente y se levanta solo; no se fuerza en ráfaga.
  Lo que sigue sin vía es la paginación más allá de los
  primeros 20 comentarios por video (pendiente de decidir si
  vale el tiempo de corrida).
- **Bajista, resuelto del todo**: la evidencia inclina a Mau
  Batarse (post oficial @diezellmx, 2 sep 2026), y José Aguilar
  solo aparece en la Wikipedia borrada. Pero nadie confirma el
  nombre completo de Mau, ni si Aguilar fue bajista anterior,
  ni cuándo ocurrió el cambio. Solo se resuelve preguntando a
  la banda. La web lo dice así: "por confirmar".

## Producción sin cuentas

- **Dominio propio** (`diezell.mx` o similar): imposible sin
  que alguien registre y pague un dominio. No hay dominio.
- **CI externo (GitHub Actions, Netlify, Vercel)**: imposible
  sin cuenta GitHub ni cuenta de hosting. No hay repo ni
  despliegue externo.
- **Re-share automático del artefacto**: el artefacto `diezell`
  es una instantánea que solo se actualiza volviéndolo a
  compartir, y eso exige aprobación. No hay deploy automático
  diario: cada sincronización se prepara y se comparte con un
  sí. El vigilante de Muse solo mantiene vivo el timer; no
  publica nada solo.
- **Garantía del 100% del corte diario**: imposible con
  systemd solo, porque la VM borra las unidades en cada
  reemplazo (5 veces). El vigilante (cron cada 30 min) lo
  reinstala si falta, pero si la VM está caída todo un día, el
  corte de ese día se pierde y solo se recupera a mano con su
  fecha original.
- **Cobertura del 100%**: imposible. Con los arreglos del
  20 nov se llega a ~92–95 %. Lo de arriba es el resto.
