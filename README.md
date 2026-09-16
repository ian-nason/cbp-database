# CBP border enforcement data (Deportation Data Project FOIA releases) as a DuckDB database

Individual-level U.S. Customs and Border Protection records obtained by the
[Deportation Data Project](https://deportationdata.org/data/cbp.html) through FOIA
litigation, harmonised into one schema per record type. Companion to
[ice-database](https://github.com/ian-nason/ice-database) (same source project, interior
enforcement) and [eoir-database](https://github.com/ian-nason/eoir-database) (immigration courts).

| Table | One row per | Coverage | Source files |
|-------|-------------|----------|--------------|
| `apprehensions` | person apprehended by Border Patrol | Oct 2007 - Dec 2025 (gaps: Apr-Sep 2014, Oct 2022 - Mar 2024, Jul-Nov 2024, Aug 2025) | 30 |
| `apprehensions_origin` | apprehension, with place of birth | FY2000 - FY2022 | 23 |
| `encounters` | Border Patrol encounter (prior-encounter history, seizures) | FY2010 - FY2018, Oct 2022 - Sep 2024 | 17 |
| `inadmissibles` | person deemed inadmissible at a port of entry (OFO) | CY2014 - Jan 2026 | 19 of 42 (see tiling) |
| `title42_expulsions` | Title 42 expulsion | Mar 2020 - May 2022 | 3 |
| `cbp_one` | CBP One appointment (individual-level extract) | Jan 12 - Oct 31 2023 | 1 |
| `cbp_one_monthly` | port x month aggregate | May 2021 - Feb 2024, five overlapping extracts | 5 |
| `inadmissibles_superseded` | same schema as `inadmissibles` | rows from the 23 overlapping release files | 23 |
| `_files` | source file | window, DDP row count, URL, whether in the base tiling and why not | 121 |

Row counts, columns and null rates: `DICTIONARY.md`.

## Quick start

```python
import datapond
con = datapond.connect("cbp")
con.sql("""
    SELECT EXTRACT(YEAR FROM event_datetime) AS year, citizenship, COUNT(*) AS n
    FROM apprehensions WHERE event_datetime >= '2023-01-01'
    GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 20
""").show()
```

## How the release files were combined

CBP answers each FOIA request with a fresh extract, so the 121 files differ in
column names (the same field appears as `CITIZENSHIP`, `CITIZENSHIP_CD` or `Citizenship
Country Name`), in header-row position, in sheet layout (some annual files have one sheet
per quarter) and in coverage window. The build:

1. reads every sheet of every file, normalises headers to `snake_case` and merges known
   synonyms (`ALIASES` in `build_database.py`; e.g. `appr_dt_time`, `event_created_datetime`
   and `encounter_dt_time` all become `event_datetime`);
2. unions files by column name, so a column only some releases carry is NULL elsewhere
   (`DICTIONARY.md` shows the null rate);
3. keeps provenance on every row: `source_file`, `source_sheet`, `window_start`, `window_end`;
4. **tiles** each table from a non-overlapping set of files. Most record types tile
   naturally (annual/quarterly files). Inadmissibles do not: CBP released annual
   calendar-year files for 2014-2024 plus a dozen partial extracts whose windows overlap
   them. The base `inadmissibles` table uses the annual and quarterly files that tile
   2014-2024, then `2025-01..05`, `2025-06..09-06` and `2025-09..2026-01` (trimmed to start
   2025-09-07): 19 files. The other 23 inadmissibles files are loaded unchanged into
   `inadmissibles_superseded`, and `_files` records the reason (`in_base_table`,
   `superseded_reason`). `_files` is the authoritative list; the counts here are copied from it.

Dates: DuckDB timestamps (Excel serials and `MM/DD/YYYY` text both parsed). Redaction
markers such as `(b)(6)` are stored as NULL.

## Researcher caveats

- **No stable person identifier.** Only 2021+ apprehension files carry `subject_key`, and
  it is re-anonymised per release; rows cannot be linked across files or to ICE data.
- **Counts differ between extracts of the same window** (e.g. the two Oct 2024 - Mar 2025
  inadmissibles extracts have 478K and 430K rows). Treat release-level counts as
  approximate and check `source_file` when a series looks discontinuous.
- **Apprehensions gaps are real gaps in what CBP has released**, not zero activity.
- Coverage windows are the DDP's, taken from the file names/pages; `event_datetime`
  min/max per file can extend slightly outside them.
- `apprehensions_origin` is a separate FOIA series (place of birth fields) that overlaps
  `apprehensions` in time; do not add the two.
- `cbp_one_monthly` files overlap each other; pick one `source_file` per analysis.

## Build

```bash
uv sync
uv run python refresh_releases.py   # re-read the DDP page: adds new files to releases.json / download_list.tsv, reports removed ones (--check to only report)
./scripts_download.sh               # 121 files, 4.6 GB, from box.com links in download_list.tsv; exits 1 if any download failed
uv run python build_database.py  # ~45 minutes, DuckDB capped at 4 GB, pandas one sheet at a time
uv run python publish_to_hf.py --token hf_xxx --verify
```

## License

Code: MIT. Data: CC0 as published by the Deportation Data Project (public records).
