#!/usr/bin/env bash
# Rebuild the local copy of the talk from the slide files in deck/project/.
# Output: slides_local.html (slides + speaker notes) and slides_local.pdf (slides only).
# Why: the online deck shows images by upload id (/_blob/...); the local copy points
# them to the paper figures, so it opens offline from this folder.
# Run from anywhere: bash tips/presentation/build_local.sh
set -euo pipefail
cd "$(dirname "$0")"

F=../../papers/paper_mvp1/figures
OUT=slides_local.html
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# upload id -> paper figure file (the 18 figures uploaded to the online deck)
MAP=(
  "f1962a5429c289b56bb1321737717fdb drop_reasons.png"
  "4b6dbeeb8d4c89aa099011c8850e8ea3 fig4_calibration_gap.png"
  "4f6567840fdebf6a7827a918aaab8508 fig4_calibration_rate_col.png"
  "50336fd0a3d903e76d640646cbd7d0bd fig6_ccdf.png"
  "6f49999e06e661dde60926ef827f5a57 fig7_lorenz.png"
  "634b5d8e5163bf6db983db6fe47816dc hist_trade_size.png"
  "b5fea725872060da08621359a1d21a06 qq_trade_size_raw_log.png"
  "7a92142d4bce249652cc54fa16d8cf77 fig_r3_m3_cluster_bootstrap.png"
  "dae8c2a548e569b365a5ea43784e20c3 fig_r3_m5_implied_gap.png"
  "7c6571fe4b62f10eb82e08507a9734a3 hist_price_p1d.png"
  "d7a873a86ee35c05bf11eb50eecacbbd qq_wallet_volume_raw_log.png"
  "26093cdd07c53762949429523d370b47 wallet_dist_panels.png"
  "b7015dd0cb953bc967f993ed30505fee fig5_ecdf_yes_no.png"
  "559b3b8714f9955236f383016d428d97 fig_r3_m4_kept_vs_dropped.png"
  "5845a06a1765090afe767ae22a8b5629 fig_r3_m1_price_definition.png"
  "727f35750af0e3b714c0a723cd233bcb fig_r3_m2_yes_reliability.png"
  "100321546d88828ede2423c5b94ea7fa fig6_ccdf_top_sampled.png"
  "a5e7147e0661a0704e4c04239eca8b43 fig_pnl_distribution.png"
)
SED_ARGS=(-e "s#/_blob/9f89f600ea3d7048b20fd3d1bd9aa18a#../../docs/kalshi_screenshot.png#g"  # Kalshi screenshot lives in docs/
  -e "s#/_blob/9f55de1460e0ba17dd3bca5839764873#../../images/aliean_grute.jpeg#g"  # alien teaser images live in images/
  -e "s#/_blob/6eb2ff6e265940a4e829224883f94b19#../../images/rocket_aliean.jpg#g"
  -e "s#/_blob/0f59a8a435d19692aa3bb3fef41761fd#../../images/yoda_alien.jpeg#g")
for pair in "${MAP[@]}"; do
  set -- $pair
  SED_ARGS+=(-e "s#/_blob/$1#$F/$2#g")
done

{
cat <<'EOF'
<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>6344 Polymarket Talk</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&display=swap">
<style>
EOF
cat deck/project/deck.css
cat <<'EOF'
/* local viewer only: fixed 1920x1080 slides, scaled to the window; notes under each slide */
html,body{margin:0;background:#E5E5E5}
body{counter-reset:page}
section{width:1920px;height:1080px;margin:0 auto}
.slide{zoom:var(--z,0.5);margin:24px auto;width:1920px;box-shadow:0 0 0 1px #737373}
aside{display:none}
.fragment{opacity:1!important}  /* local copy shows every click step at once */
.notes{zoom:var(--z,0.5);width:1920px;margin:0 auto;box-sizing:border-box;padding:24px 128px;background:#FFFFFF;border-top:1px solid #737373;font:24px/1.4 "IBM Plex Mono",monospace;color:#262626}
@media print{
  @page{size:1920px 1080px;margin:0}
  html,body{background:#FFFFFF}
  .slide{zoom:1;margin:0;box-shadow:none;break-after:page}
  .notes{display:none}
}
</style>
<script>function fit(){document.documentElement.style.setProperty('--z',Math.min(1,(window.innerWidth-48)/1920))}addEventListener('resize',fit);addEventListener('DOMContentLoaded',fit)</script>
</head><body>
EOF
# slide order comes from deck.json "order"; newlines and spaces are stripped first, so compact and pretty JSON both work
for id in $(tr -d ' \n' < deck/project/deck.json | grep -o '"order":\[[^]]*\]' | grep -o '"[A-Za-z0-9_-]*"' | tr -d '"' | grep -v '^order$'); do
  echo '<div class="slide">'
  sed "${SED_ARGS[@]}" "deck/project/slides/$id.html"
  echo '</div>'
  notes=$(sed -n 's/.*<aside>\(.*\)<\/aside>.*/\1/p' "deck/project/slides/$id.html")
  if [ -n "$notes" ]; then echo "<div class=\"notes\"><b>Notes:</b> $notes</div>"; fi
done
echo '</body></html>'
} > "$OUT"

echo "wrote $OUT ($(grep -c '<section' "$OUT") slides)"
if [ -x "$CHROME" ]; then
  P=$(mktemp -d)
  timeout 90 "$CHROME" --headless=new --use-mock-keychain --password-store=basic --no-first-run \
    --no-default-browser-check --disable-extensions --disable-sync --user-data-dir="$P" \
    --no-pdf-header-footer --virtual-time-budget=5000 \
    --print-to-pdf="$PWD/slides_local.pdf" "file://$PWD/$OUT" 2>/dev/null
  echo "wrote slides_local.pdf"
else
  echo "Chrome not found: open $OUT in a browser and print to PDF"
fi
