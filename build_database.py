#!/usr/bin/env python3
"""Build cbp.duckdb from the Deportation Data Project's CBP FOIA releases.

Source: https://deportationdata.org/data/cbp.html (121 xlsx files, listed in
releases.json with their DDP-reported windows). Six record types become six
tables:

    apprehensions          Border Patrol apprehensions, FY2008 - Dec 2025 (annual/quarterly/monthly files)
    apprehensions_origin   Border Patrol apprehensions with place of birth, FY2000 - FY2022
    encounters             Border Patrol encounters, FY2010 - FY2018 and FY2023 - FY2024
    inadmissibles          Office of Field Operations "deemed inadmissible" events, CY2014 - Jan 2026
    title42_expulsions     Title 42 expulsions, FY2020 - FY2022
    cbp_one                CBP One appointments (individual-level extract, Jan - Oct 2023)
    cbp_one_monthly        CBP One monthly aggregates by port (five overlapping extracts)

Every file is staged as-is (headers normalised to snake_case, synonyms merged
via ALIASES) and combined with UNION ALL BY NAME, so columns that only some
releases carry are simply NULL elsewhere. Overlapping release windows (the
inadmissibles set has many) are resolved by TILING: each table's base rows come
from a non-overlapping set of files; rows from the other files are kept in
<table>_superseded with the same schema so nothing is thrown away.

Usage:
    uv run python build_database.py [--tables apprehensions inadmissibles] [--output cbp.duckdb]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import duckdb
import pandas as pd

from datapond_build import Checker, build_columns_table, ensure_metadata, export_dictionary
from datapond_build.session import connect

DEFAULT_OUTPUT = "cbp.duckdb"
RAW = Path("data/raw")

TYPE_TO_TABLE = {
    "Apprehensions": "apprehensions",
    "Apprehensions with place of origin": "apprehensions_origin",
    "Encounters": "encounters",
    "Deemed inadmissible": "inadmissibles",
    "Title 42 expulsions": "title42_expulsions",
    "CBP One": "cbp_one",
}

TABLE_DESCRIPTIONS = {
    "apprehensions": "Border Patrol apprehensions between ports of entry, one row per person apprehended (FOIA releases covering Oct 2007 - Dec 2025; monthly gaps where CBP has not yet released data)",
    "apprehensions_origin": "Border Patrol apprehensions with place of birth (country/state/city), one row per apprehension, FY2000 - FY2022",
    "encounters": "Border Patrol encounters (apprehensions with prior-encounter history and seizure fields), FY2010 - FY2018 and Oct 2022 - Sep 2024",
    "inadmissibles": "Office of Field Operations events where a person arriving at a port of entry was deemed inadmissible, one row per event, CY2014 - Jan 2026",
    "title42_expulsions": "Title 42 expulsions by Border Patrol, one row per expulsion, FY2020 - FY2022",
    "cbp_one": "CBP One app appointments at ports of entry, individual-level extract, Jan 12 - Oct 31 2023",
    "cbp_one_monthly": "CBP One monthly appointment counts by port of entry and citizenship (five overlapping FOIA extracts; see source_file)",
}

# Normalised source header -> canonical column. Anything not listed keeps its
# normalised name, so no column is lost; this only merges obvious synonyms.
ALIASES = {
    # people
    "citizenship_cd": "citizenship", "citizenship_country_name": "citizenship",     "nationality": "citizenship",
    "cbpone_crte_dttm": "appointment_created_datetime",
    "sex": "gender",
    "app_age": "age", "age_at_event_creation_time": "age",
    "marital_status_cd": "marital_status", "marital_status_name": "marital_status",
    "country_of_birth_cd": "country_of_birth", "birth_country_name": "country_of_birth",
    "birth_city": "city_of_birth",
    "uc_indicator": "uac_indicator", "unaccompanied_child": "uac_indicator", "unaccompanied_minor_indicator": "uac_indicator",
    "fmua_uac_indicator": "fmua_uac_am_single", "fmua_uac_am_single": "fmua_uac_am_single",
    "credible_fear": "credible_fear_indicator", "cred_fear_indicator": "credible_fear_indicator",
    "ces": "ces_indicator", "ces_ind": "ces_indicator",
    "gang_ind": "gang_indicator", "gang_code": "gang_indicator", "gang_affiliation": "gang_indicator",
    "suspected_gang_affiliation_name": "gang_affiliation_name", "gang_affiliation_type_name": "gang_affiliation_name",
    "juvenile_18": "juvenile", "adult_or_juvenile": "juvenile",
    "status_at_entry_cd": "status_at_entry", "entry_status": "status_at_entry",
    "dhs_status_code_lpr": "lpr",
    # events / dates
    "appr_dt_time": "event_datetime", "app_dt_time": "event_datetime", "apprehension_dt": "event_datetime",
    "encounter_dt_time": "event_datetime", "encounter_date_time": "event_datetime", "arrest_datetime": "event_datetime",
    "event_created_datetime": "event_datetime", "event_created_date_time": "event_datetime", "arrest_date_time": "event_datetime",
    "date_processed": "event_datetime", "arrest_date": "event_datetime",
    "civ_id": "subject_key", "civ_id_unique_identifier": "subject_key", "family_unit_group": "fmu_number",
    "highest_statute_charge": "statute_charge", "of_subjects_per_event": "num_people_per_event",
    "entry_dt": "entry_date",
    "final_bookout_date_time": "final_bookout_datetime", "final_bookout_date": "final_bookout_datetime",
    "custody_date_time_out": "final_bookout_datetime",
    "case_file_date": "case_filing_date",
    "most_recent_prior_ent_datetime": "most_recent_prior_encounter_datetime",
    "most_recent_prior_encounter_date_time": "most_recent_prior_encounter_datetime",
    "most_recent_apprehension_date": "most_recent_prior_encounter_datetime",
    "most_recent_encounter_date": "most_recent_prior_encounter_datetime",
    "number_of_previous_apprehensions": "num_previous_encounters", "of_previous_apprehensions": "num_previous_encounters",
    "number_of_previous_apprehension": "num_previous_encounters", "number_of_previous_encounter": "num_previous_encounters",
    "number_of_prev_encounters": "num_previous_encounters",
    "earliest_apprehension_date": "earliest_encounter_date",
    # place
    "apprehension_sector": "sector", "field_office": "field_office_name",
    "apprehension_state": "state", "usa_state_code": "state",
    "apprehension_latitude": "latitude",
    # process
    "disposition_name": "disposition",
    "referred_prosecution": "referred_for_prosecution", "prosecution_indicator": "referred_for_prosecution",
    "refferred_for_prosecution_under_8_usc_1325_or_8_usc_1326": "referred_for_prosecution",
    "transfer_to": "transferred_to_group", "transfer_to_group": "transferred_to_group",
    "i216_custody_transfer_to": "transferred_to_group",
    "mode_of_transportation": "mode_of_transport", "mot": "mode_of_transport",
    "of_children_and_nationality": "num_children_and_nationality", "number_children_and_nationality": "num_children_and_nationality",
    "number_of_children": "num_children",
    "of_people_per_event": "num_people_per_event",
    "family_unit_type": "fmua_indicator",
    "unique_case_identifier": "unique_case_id",
    "duplicate_indicator": "duplicate_subject_indicator", "duplicates": "duplicate_subject_indicator",
    "sigma_subject_person_id": "subject_key",
    "event_subject_count": "person_count",
    "inadmissibles_subject_count": "person_count", "inadmissibles_count": "person_count",
    "port_name": "port_name", "prmry_lang_txt": "language",
    "cbpone_rqstd_entry_dt": "requested_entry_date", "rqstd_poe_cd": "requested_port_code",
}

DATETIME_COLS = {"event_datetime", "appointment_created_datetime", "entry_date", "final_bookout_datetime", "case_filing_date",
                 "most_recent_prior_encounter_datetime", "earliest_encounter_date", "requested_entry_date",
                 "earliest_apprehension_date", "birth_date", "date"}
INT_COLS = {"age", "num_previous_encounters", "num_children", "num_people_per_event", "person_count",
            "number_of_fmu_members", "title_8_subjects_in_fmu", "fy", "calendar_year"}

# Files that are NOT part of the base tiling (their rows go to <table>_superseded).
# Keyed by local file name; reasons documented for the README.
SUPERSEDED = {
    # inadmissibles: annual CY files 2014-2024 + 2025-01..05 (015) + 2025-06..09-06 (019) + 2025-09..2026-01 (024) are canonical
    "2020-04-01_2022-03-31_134.xlsx": "overlaps CY2020-2022 annual files",
    "2022-04-01_2022-04-30_133.xlsx": "inside CY2022 annual file",
    "2022-07-01_2023-02-28_124.xlsx": "overlaps CY2022/CY2023 annual files",
    "2022-07-01_2023-02-28_125.xlsx": "duplicate extract of the same window",
    "2023-05-01_2023-06-20_122.xlsx": "inside CY2023 annual file",
    "2023-07-01_2023-07-31_120.xlsx": "inside CY2023 annual file",
    "2023-07-01_2023-12-31_116.xlsx": "inside CY2023 annual file",
    "2023-11-01_2024-08-01_105.xlsx": "overlaps CY2023/CY2024 annual files",
    "2024-01-01_2024-06-30_106.xlsx": "inside CY2024 annual file",
    "2024-10-01_2024-11-30_103.xlsx": "inside CY2024 annual file",
    "2024-10-01_2025-03-19_010.xlsx": "overlaps CY2024 annual file and 2025-01..05 file",
    "2024-10-01_2025-03-19_011.xlsx": "second extract of the same window",
    "2025-03-01_2025-03-31_012.xlsx": "inside 2025-01..05 file",
    "2025-04-01_2025-04-30_013.xlsx": "inside 2025-01..05 file",
    "2025-05-01_2025-05-31_014.xlsx": "inside 2025-01..05 file",
    "2025-06-01_2025-06-30_016.xlsx": "inside 2025-06..09-06 file",
    "2025-07-01_2025-07-31_017.xlsx": "inside 2025-06..09-06 file",
    "2025-08-01_2025-08-31_018.xlsx": "inside 2025-06..09-06 file",
    "2025-09-01_2025-09-30_020.xlsx": "inside 2025-09..2026-01 file",
    "2025-10-01_2025-10-31_021.xlsx": "inside 2025-09..2026-01 file",
    "2025-11-01_2025-11-30_022.xlsx": "inside 2025-09..2026-01 file",
    "2025-12-01_2025-12-31_023.xlsx": "inside 2025-09..2026-01 file",
    "2026-01-01_2026-01-31_025.xlsx": "inside 2025-09..2026-01 file",
}
# Date trims applied to canonical files whose window overlaps a neighbour.
TRIM_BEFORE = {"2025-09-01_2026-01-31_024.xlsx": "2025-09-07"}  # 019 covers through 2025-09-06

CBP_ONE_INDIVIDUAL = "2023-01-12_2023-10-31_118.xlsx"


def norm(h: str) -> str:
    h = str(h).replace("\n", " ").strip().lower()
    h = re.sub(r"\(.*?\)", " ", h)
    h = re.sub(r"[^a-z0-9]+", "_", h).strip("_")
    return ALIASES.get(h, h)


def find_header_row(path: Path, sheet: str, max_scan: int = 15) -> int:
    probe = pd.read_excel(path, sheet_name=sheet, header=None, nrows=max_scan, engine="openpyxl")
    counts = probe.notna().sum(axis=1)
    return int(counts.idxmax()) if len(counts) else 0


def read_sheet(path: Path, sheet: str) -> pd.DataFrame | None:
    hdr = find_header_row(path, sheet)
    df = pd.read_excel(path, sheet_name=sheet, header=hdr, engine="openpyxl", dtype=str)
    df = df.loc[:, [c for c in df.columns if not str(c).startswith("Unnamed")]]
    if df.shape[1] < 3 or len(df) == 0:
        return None
    # normalise + de-duplicate column names
    cols, seen = [], {}
    for c in df.columns:
        n = norm(c) or "col"
        if n in seen:
            seen[n] += 1; n = f"{n}_{seen[n]}"
        else:
            seen[n] = 0
        cols.append(n)
    df.columns = cols
    df = df.dropna(how="all")
    return df


def stage_file(con, table: str, rel: dict, idx: int) -> list[str]:
    """Load every data sheet of one xlsx into staging tables; returns their names."""
    path = RAW / rel["local"]
    stages = []
    xl = pd.ExcelFile(path, engine="openpyxl")
    for si, sheet in enumerate(xl.sheet_names):
        try:
            df = read_sheet(path, sheet)
        except Exception as e:  # noqa: BLE001
            print(f"    WARNING {path.name}[{sheet}]: {e}"); continue
        if df is None:
            continue
        df["source_file"] = path.name
        df["source_sheet"] = sheet
        df["window_start"] = rel["Start"]
        df["window_end"] = rel["End"]
        stage = f"_stage_{table}_{idx}_{si}"
        con.execute(f'DROP TABLE IF EXISTS "{stage}"')
        con.register("_df", df)
        con.execute(f'CREATE TABLE "{stage}" AS SELECT * FROM _df')
        con.unregister("_df")
        print(f"    {path.name}[{sheet}]: {len(df):,} rows x {df.shape[1]} cols")
        stages.append(stage)
        del df
    return stages


def cast_columns(con, table: str) -> None:
    cols = {r[0]: r[1] for r in con.execute(
        "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = ?", [table]).fetchall()}
    for c in cols:
        q = f'"{c}"'
        if c in DATETIME_COLS:
            con.execute(f"""ALTER TABLE {table} ALTER COLUMN {q} SET DATA TYPE TIMESTAMP USING
                COALESCE(TRY_CAST({q} AS TIMESTAMP), TRY_STRPTIME({q}, '%m/%d/%Y %H:%M'), TRY_STRPTIME({q}, '%m/%d/%Y'),
                         CASE WHEN TRY_CAST({q} AS DOUBLE) BETWEEN 20000 AND 60000
                              THEN TIMESTAMP '1899-12-30' + INTERVAL (CAST(TRY_CAST({q} AS DOUBLE) * 86400 AS BIGINT)) SECOND END)""")
        elif c in INT_COLS:
            con.execute(f"""ALTER TABLE {table} ALTER COLUMN {q} SET DATA TYPE INTEGER USING
                TRY_CAST(TRY_CAST({q} AS DOUBLE) AS INTEGER)""")
        else:
            con.execute(f"UPDATE {table} SET {q} = NULL WHERE TRIM({q}) IN ('', 'NULL', 'nan', 'None', '(b)(6)', '(b)(7)(E)', '(b)(6)(b)(7)(C)')")


def build_table(con, table: str, rels: list[dict]) -> tuple[int, int]:
    print(f"\n== {table}: {len(rels)} files")
    stages, sup_stages = [], []
    for i, rel in enumerate(rels):
        names = stage_file(con, table, rel, i)
        (sup_stages if Path(rel["local"]).name in SUPERSEDED else stages).extend(names)
    n_base = n_sup = 0
    for target, group in ((table, stages), (f"{table}_superseded", sup_stages)):
        con.execute(f"DROP TABLE IF EXISTS {target}")
        if not group:
            continue
        union = " UNION ALL BY NAME ".join(f'SELECT * FROM "{s}"' for s in group)
        con.execute(f"CREATE TABLE {target} AS {union}")
        for s in group:
            con.execute(f'DROP TABLE "{s}"')
        cast_columns(con, target)
    if stages:
        for fname, before in TRIM_BEFORE.items():
            if "event_datetime" in [r[0] for r in con.execute(f"DESCRIBE {table}").fetchall()]:
                n = con.execute(f"DELETE FROM {table} WHERE source_file = ? AND event_datetime < ?", [fname, before]).fetchone()
                print(f"    trimmed rows before {before} from {fname}")
        n_base = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    if sup_stages:
        n_sup = con.execute(f"SELECT COUNT(*) FROM {table}_superseded").fetchone()[0]
    print(f"  -> {table}: {n_base:,} rows" + (f"; {table}_superseded: {n_sup:,} rows" if sup_stages else ""))
    return n_base, n_sup


def build_files_table(con, rels: list[dict]) -> None:
    con.execute("DROP TABLE IF EXISTS _files")
    con.execute("""CREATE TABLE _files (source_file VARCHAR, record_type VARCHAR, "table" VARCHAR, window_start DATE,
                   window_end DATE, ddp_records VARCHAR, size VARCHAR, url VARCHAR, in_base_table BOOLEAN, superseded_reason VARCHAR)""")
    for r in rels:
        name = Path(r["local"]).name
        tbl = TYPE_TO_TABLE[r["Type"]]
        if tbl == "cbp_one" and name != CBP_ONE_INDIVIDUAL:
            tbl = "cbp_one_monthly"
        con.execute("INSERT INTO _files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [name, r["Type"], tbl, r["Start"], r["End"], r.get("Records"), r.get("size"), r.get("url"),
                     name not in SUPERSEDED, SUPERSEDED.get(name)])


def run_validation(con) -> int:
    ck = Checker("Validation")
    for t in TABLE_DESCRIPTIONS:
        ck.query(con, f"{t} non-empty", f"SELECT COUNT(*) FROM {t}", lambda n: n > 0, lambda n: f"{n:,} rows")
    ck.query(con, "apprehensions event_datetime parsed (> 98%)",
             "SELECT COUNT(event_datetime) * 1.0 / COUNT(*) FROM apprehensions", lambda v: v > 0.98, lambda v: f"{v:.2%}")
    ck.query(con, "inadmissibles event_datetime parsed (> 98%)",
             "SELECT COUNT(event_datetime) * 1.0 / COUNT(*) FROM inadmissibles", lambda v: v > 0.98, lambda v: f"{v:.2%}")
    ck.query(con, "inadmissibles latest event in 2026",
             "SELECT MAX(event_datetime) FROM inadmissibles", lambda d: str(d) >= "2026-01-01", str)
    ck.query(con, "apprehensions latest event in Dec 2025",
             "SELECT MAX(event_datetime) FROM apprehensions", lambda d: str(d) >= "2025-12-01", str)
    # tiling: no two base files overlap in window (per table)
    # Files with an identical window are parts of one release (e.g. "2023 Records Part 1/2/3"),
    # not overlaps; the 019/024 pair is resolved by TRIM_BEFORE.
    ck.query(con, "base tiling has no overlapping windows", """
        SELECT COUNT(*) FROM _files a JOIN _files b
          ON a."table" = b."table" AND a.source_file < b.source_file AND a.in_base_table AND b.in_base_table
         AND a."table" NOT IN ('cbp_one_monthly') AND a.window_start <= b.window_end AND b.window_start <= a.window_end
         AND NOT (a.window_start = b.window_start AND a.window_end = b.window_end)
         AND NOT (a.source_file IN ('2025-06-01_2025-09-06_019.xlsx','2025-09-01_2026-01-31_024.xlsx')
                  AND b.source_file IN ('2025-06-01_2025-09-06_019.xlsx','2025-09-01_2026-01-31_024.xlsx'))""",
             lambda n: n == 0, lambda n: f"{n} overlapping pairs")
    ck.query(con, "every listed file loaded", "SELECT COUNT(*) FROM _files f WHERE NOT EXISTS (SELECT 1 FROM (SELECT DISTINCT source_file FROM apprehensions UNION ALL SELECT DISTINCT source_file FROM apprehensions_origin UNION ALL SELECT DISTINCT source_file FROM encounters UNION ALL SELECT DISTINCT source_file FROM inadmissibles UNION ALL SELECT DISTINCT source_file FROM inadmissibles_superseded UNION ALL SELECT DISTINCT source_file FROM title42_expulsions UNION ALL SELECT DISTINCT source_file FROM cbp_one UNION ALL SELECT DISTINCT source_file FROM cbp_one_monthly) s WHERE s.source_file = f.source_file)",
             lambda n: n == 0, lambda n: f"{n} files missing")
    return ck.report()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=Path(DEFAULT_OUTPUT))
    ap.add_argument("--tables", nargs="+", default=None)
    a = ap.parse_args()
    t0 = time.time()
    rels = json.load(open("releases.json"))
    groups: dict[str, list[dict]] = {t: [] for t in TABLE_DESCRIPTIONS}
    for r in rels:
        tbl = TYPE_TO_TABLE[r["Type"]]
        if tbl == "cbp_one" and Path(r["local"]).name != CBP_ONE_INDIVIDUAL:
            tbl = "cbp_one_monthly"
        groups[tbl].append(r)
    if a.tables:
        groups = {t: g for t, g in groups.items() if t in a.tables}
    # --tables rebuilds only those tables inside an existing file (the others are kept).
    con = connect(a.output, fresh=a.tables is None, memory_limit="4GB", threads=2)
    counts = {}
    for t, g in groups.items():
        counts[t] = build_table(con, t, sorted(g, key=lambda r: (r["Start"], r["End"])))
    build_files_table(con, rels)
    print("\nMetadata + dictionary")
    present = {r[0] for r in con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main' AND table_type='BASE TABLE'").fetchall()}
    tables = [t for t in TABLE_DESCRIPTIONS if t in present] + [f"{t}_superseded" for t in TABLE_DESCRIPTIONS if f"{t}_superseded" in present]
    desc = dict(TABLE_DESCRIPTIONS)
    for t in TABLE_DESCRIPTIONS:
        if f"{t}_superseded" in present:
            desc[f"{t}_superseded"] = f"Rows from {t} release files whose windows overlap the base tiling (see _files.superseded_reason); same schema as {t}"
    ensure_metadata(con, descriptions=desc, tables=tables, source_url="https://deportationdata.org/data/cbp.html",
                    license="CC0 (Deportation Data Project) / public records", replace=True)
    build_columns_table(con, join_hints={
        "source_file": "FOIA release file the row came from; joins to _files.source_file",
        "subject_key": "CBP anonymized person key where released (2021+ files only); not stable across releases",
        "event_number": "CBP event identifier where released",
        "sector": "Border Patrol sector (apprehensions/encounters)",
        "field_office_name": "OFO field office (inadmissibles)",
    }, tables=tables)
    export_dictionary(con, Path("DICTIONARY.md"), title="cbp Data Dictionary",
                      intro=["Source: [Deportation Data Project - CBP](https://deportationdata.org/data/cbp.html) FOIA releases.",
                             "Columns are the union of every release's headers (synonyms merged); a NULL rate near 100% means only some releases carry the field.",
                             "`_files` lists every source file, its window, and whether it is part of the base tiling."],
                      style="registry", tables=tables + ["_files"])
    con.execute("CHECKPOINT")
    failures = run_validation(con)
    con.close()
    total = con_total = sum(r[0] for r in [(0,)]) if False else sum(b for b, _ in counts.values())
    print(f"\nBUILD DONE in {(time.time() - t0) / 60:.1f} min; {total:,} base rows; {a.output.stat().st_size / 1024**3:.2f} GB")
    if failures:
        print(f"BUILD FAILED: {failures} check(s) failed -- do not publish this file")
        sys.exit(1)


if __name__ == "__main__":
    main()
