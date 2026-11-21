#!/bin/bash
# Diezell — corte diario del archivo. Puro código, sin IA, sin claves.
# Ejecuta todos los colectores en orden; cada uno registra OK/FAIL.
# Un colector fallido NO detiene a los demás (el hueco queda en el log).
# Uso: ./run_daily.sh   (lo llama el timer de systemd, 1 vez al día)
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
BASE="$(dirname "$DIR")"
LEDGER="$BASE/datos/ledger"
LOG="$LEDGER/runs/$(date +%Y-%m-%d-%H%M%S).log"
mkdir -p "$LEDGER/runs"
{
echo "=== CORTE DIARIO DIEZELL — $(date -u +"%Y-%m-%dT%H:%M:%SZ") UTC / $(TZ=America/Mexico_City date +"%Y-%m-%d %H:%M") America/Mexico_City ==="
cd "$DIR" || exit 1
for script in deezer.py youtube_rss.py youtube_public.py youtube_video.py \
              youtube_comments.py \
              tiktok_public.py tiktok_tag.py instagram_public.py soundcloud.py \
              reddit.py google_news_rss.py bing_news_rss.py press_rss.py \
              musicbrainz.py itunes.py spotify_public.py lastfm_public.py \
              setlistfm_public.py bandsintown_public.py songkick_public.py \
              facebook_public.py facebook_plugin.py wikipedia.py wayback.py charts.py \
              stories.py commenters.py; do
  echo "--- $script ---"
  python3 "$DIR/$script"
  sleep 1
done
echo "=== FIN DEL CORTE — registros en el ledger: $(python3 -c "import json; print(len(json.load(open('$LEDGER/ledger.json'))['records']))") ==="
} | tee "$LOG"
