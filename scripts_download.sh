#!/usr/bin/env bash
# Download every CBP release listed in download_list.tsv into data/raw/<table>/
set -uo pipefail
cd "$(dirname "$0")"
ok=0; fail=0
while IFS=$'\t' read -r name url; do
  dest="data/raw/$name"; mkdir -p "$(dirname "$dest")"
  if [[ -s "$dest" ]]; then ok=$((ok+1)); continue; fi
  if curl -L --retry 5 --retry-delay 10 -sS -A "Mozilla/5.0 (datapond-maintenance)" -o "$dest.part" "$url" && [[ -s "$dest.part" ]]; then
    mv "$dest.part" "$dest"; ok=$((ok+1)); echo "ok   $name $(stat -c %s "$dest")"
  else
    rm -f "$dest.part"; fail=$((fail+1)); echo "FAIL $name $url"
  fi
done < download_list.tsv
echo "DOWNLOADS DONE ok=$ok fail=$fail"
