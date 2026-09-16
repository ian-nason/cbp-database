#!/usr/bin/env python3
"""Refresh releases.json from the Deportation Data Project's CBP page.

    uv run python refresh_releases.py            # rewrite releases.json + download_list.tsv, report changes
    uv run python refresh_releases.py --check    # report only, exit 1 if the page lists files we lack

The page (https://deportationdata.org/data/cbp.html) renders its file tables from JSON
embedded in the HTML (reactable htmlwidgets). Each table row has Type, Start, End,
Records, Source, Original (box.com links) and the DDP's column inventory. Entries
already in releases.json keep their `local` file name (the build keys on it); new
files get `<type>/<start>_<end>_<nnn>.<ext>` and `ext` from the download URL.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

PAGE = "https://deportationdata.org/data/cbp.html"
TYPE_DIRS = {"Apprehensions": "apprehensions", "Apprehensions (with origin)": "apprehensions_origin",
             "Encounters": "encounters", "Inadmissibles": "inadmissibles", "Title 42 Expulsions": "title42",
             "CBP One": "cbp_one", "CBP One (monthly)": "cbp_one_monthly"}


def fetch_rows() -> list[dict]:
    page = urllib.request.urlopen(urllib.request.Request(PAGE, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8")
    rows = []
    for t, (_wid, body) in enumerate(re.findall(r'<script type="application/json" data-for="([^"]+)">(.*?)</script>', page, flags=re.S)):
        widget = json.loads(html.unescape(body))
        data = widget.get("x", {}).get("tag", {}).get("attribs", {}).get("data")
        if not isinstance(data, dict) or "Original" not in data:
            continue
        n = len(data["Type"])
        for i in range(n):
            urls = data["Original"][i] or []
            rows.append({
                "table": t, "idx": i, "Type": data["Type"][i], "Start": data["Start"][i], "End": data["End"][i],
                "Records": data["Records"][i], "Source": data["Source"][i],
                "column_names": (data.get("column_names") or [None] * n)[i],
                "url": urls[0] if urls else None, "all_urls": urls,
            })
    return rows


def slug(t: str) -> str:
    return TYPE_DIRS.get(t, re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    here = Path(__file__).parent
    current = json.loads((here / "releases.json").read_text()) if (here / "releases.json").exists() else []
    by_url = {e["url"]: e for e in current}
    rows = fetch_rows()
    if not rows:
        sys.exit("no file tables found on the page (layout changed?)")
    merged, new, seen = [], [], set()
    counters: dict[str, int] = {}
    for r in rows:
        if not r["url"]:
            continue
        seen.add(r["url"])
        if r["url"] in by_url:
            e = dict(by_url[r["url"]]); e.update({k: r[k] for k in ("table", "idx", "Records", "Source", "column_names")})
        else:
            d = slug(r["Type"]); counters[d] = counters.get(d, 0) + 1
            ext = "csv" if ".csv" in (r["url"] or "").lower() else "xlsx"
            e = {**{k: r[k] for k in ("table", "idx", "Type", "Start", "End", "Records", "Source", "column_names", "url")},
                 "size": None, "ext": ext, "local": f"{d}/{r['Start']}_{r['End']}_{len([x for x in current if x['local'].startswith(d + '/')]) + counters[d] - 1:03d}.{ext}"}
            new.append(e)
        merged.append(e)
    removed = [e for e in current if e["url"] not in seen]
    print(f"page lists {len(merged)} files; {len(new)} new, {len(removed)} no longer listed, {len(current)} in releases.json")
    for e in new:
        print(f"  NEW  {e['Type']:28s} {e['Start']} .. {e['End']}  -> {e['local']}")
    for e in removed:
        print(f"  GONE {e['Type']:28s} {e['Start']} .. {e['End']}  ({e['local']})")
    if a.check:
        return 1 if new else 0
    (here / "releases.json").write_text(json.dumps(merged, indent=1))
    (here / "download_list.tsv").write_text("".join(f"{e['local']}\t{e['url']}\n" for e in merged))
    print("wrote releases.json and download_list.tsv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
