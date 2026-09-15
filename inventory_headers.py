"""Inventory the header row and sheet names of every downloaded CBP xlsx (read-only, streaming)."""
import glob, json, re, sys
from pathlib import Path
import openpyxl

def find_header(ws, max_scan=15):
    best, best_n, best_row = 0, 0, None
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=max_scan, values_only=True), start=1):
        vals = [v for v in row if v is not None and str(v).strip() != ""]
        if len(vals) > best_n:
            best, best_n, best_row = i, len(vals), row
    return best, [str(v).strip() if v is not None else "" for v in (best_row or ())]

out = {}
for f in sorted(glob.glob("data/raw/*/*.xlsx")):
    try:
        wb = openpyxl.load_workbook(f, read_only=True)
        sheets = {}
        for ws in wb.worksheets:
            hdr_row, cols = find_header(ws)
            sheets[ws.title] = {"header_row": hdr_row, "columns": cols, "max_row": ws.max_row}
        wb.close()
        out[f] = sheets
    except Exception as e:
        out[f] = {"error": str(e)[:200]}
json.dump(out, open("headers_inventory.json", "w"), indent=1)
for f, sheets in out.items():
    if "error" in sheets:
        print(f"{f}: ERROR {sheets['error']}"); continue
    for name, info in sheets.items():
        cols = [c for c in info["columns"] if c]
        print(f"{Path(f).parent.name}/{Path(f).name} [{name}] hdr@{info['header_row']} rows~{info['max_row']} ncol={len(cols)}: {' | '.join(cols)[:200]}")
