<a id="cbp-border-enforcement-data-deportation-data-project-foia-releases-as-a-duckdb-database"></a>

# CBP Border Enforcement Database

U.S. Customs and Border Protection (CBP) enforcement records released through the Deportation Data Project (DDP) under the Freedom of Information Act (FOIA). They include Border Patrol apprehensions and encounters, Office of Field Operations (OFO) inadmissibility events at ports of entry, Title 42 expulsions and CBP One appointments. An inadmissibility event records a person arriving at a port of entry who was deemed inadmissible. Use the table guide to select a record type and its actual coverage before querying. The eight tables contain about 51.3 million stored rows across overlapping and superseded series, not that many distinct people or events. Some periods have substantial gaps, and no stable cross-release person linkage is supplied. Do not add overlapping series or treat missing months as zero activity.

<a id="quick-start"></a>

## Start querying

Preview up to five apprehension records dated 2023 onward, showing the event timestamp (`event_datetime`) and recorded citizenship. These released records have coverage gaps and are not a complete count for the period.

Choose R or Python. Install the datapond package once: use `install.packages("datapond")` in R, or run `python -m pip install datapond` in a terminal.

### R

```r
library(datapond)
con <- dp_connect("cbp")
tryCatch({
  DBI::dbExecute(con, "SET threads=1")
  DBI::dbExecute(con, "SET memory_limit='128MiB'")
  DBI::dbExecute(con, "SET max_temp_directory_size='0B'")
  print(DBI::dbGetQuery(con, "SELECT event_datetime,citizenship FROM apprehensions WHERE event_datetime>=TIMESTAMP '2023-01-01' LIMIT 5"))
}, finally = dp_disconnect(con))
```

### Python

```python
import datapond
con = datapond.connect('cbp')
try:
    con.execute("SET threads=1")
    con.execute("SET memory_limit='128MiB'")
    con.execute("SET max_temp_directory_size='0B'")
    print(con.execute("""SELECT event_datetime,citizenship FROM apprehensions WHERE event_datetime>=TIMESTAMP '2023-01-01' LIMIT 5""").fetchall())
finally:
    con.close()
```

Queries run on your computer and read the byte ranges they need. A small result can still require a large scan. These examples limit DuckDB to one thread and a 128 MiB buffer pool with disk spill disabled; that is not a limit on the entire R or Python process. Larger analyses may need more memory or a local download with enough disk space.

<a id="additional-dataset-notes"></a>

<a id="coverage-fields-and-sources"></a>

## Tables and coverage

FY means fiscal year; CY means calendar year.

| Table | One row per | Coverage | Source files |
|-------|-------------|----------|--------------|
| `apprehensions` | person apprehended by Border Patrol | Oct 2007 - Dec 2025 (gaps: Apr-Sep 2014, Oct 2022 - Mar 2024, Jul-Nov 2024, Aug 2025) | 30 |
| `apprehensions_origin` | apprehension, with place of birth | fiscal year 2000 - FY2022 | 23 |
| `encounters` | Border Patrol encounter (prior-encounter history, seizures) | fiscal year 2010 - FY2018, Oct 2022 - Sep 2024 | 17 |
| `inadmissibles` | person deemed inadmissible at a port of entry (OFO) | calendar year 2014 - Jan 2026 | 19 of 42 (selected non-overlapping files) |
| `title42_expulsions` | Title 42 expulsion | Mar 2020 - May 2022 | 3 |
| `cbp_one` | CBP One appointment (individual-level extract) | Jan 12 - Oct 31 2023 | 1 |
| `cbp_one_monthly` | port x month aggregate | May 2021 - Feb 2024, five overlapping extracts | 5 |
| `inadmissibles_superseded` | older overlapping inadmissibility release records, retained for reference | rows from the 23 overlapping release files | 23 |

`inadmissibles` uses selected files covering non-overlapping periods. The 23 older overlapping releases remain in `inadmissibles_superseded` for comparison; do not add them to the main table as additional events.

See the [data dictionary](https://github.com/ian-nason/cbp-database/blob/main/DICTIONARY.md) for column definitions. Row counts, columns and null rates are also in `DICTIONARY.md`.

## Source-tracking reference table

Use `_files` to inspect which release a row or coverage window came from.

| Table | One row per | Contents | Files |
|---|---|---|---|
| `_files` | source file | window, DDP row count, URL, whether included in the selected non-overlapping files and why not | 121 |

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

<a id="advanced-access-quick-start"></a>

Redaction markers such as `(b)(6)` are stored as `NULL`. A field absent from a release is also `NULL`; check column availability before comparing periods. Event dates are stored as timestamps.

## More example queries

Count released apprehension records by year and recorded citizenship from 2023 onward. The result reflects the gaps listed above and is not a complete annual total.

```python
import datapond
con = datapond.connect("cbp")
con.sql("""
    SELECT EXTRACT(YEAR FROM event_datetime) AS year, citizenship, COUNT(*) AS n
    FROM apprehensions WHERE event_datetime >= '2023-01-01'
    GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 20
""").show()
```

## Sources and maintenance

### Sources and related datasets

Source: [Deportation Data Project (CBP FOIA releases)](https://deportationdata.org/data/cbp.html). License: CC-0.

The individual-level records were obtained through FOIA litigation and harmonized into one schema per record type. Companion to
[ice-database](https://github.com/ian-nason/ice-database) (same source project, interior
enforcement) and [eoir-database](https://github.com/ian-nason/eoir-database) (immigration courts).

### How the release files were combined

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
4. selects files covering non-overlapping periods for each table. Most record types
   have annual or quarterly files that fit together. Inadmissibles do not: CBP released annual
   calendar-year files for 2014-2024 plus a dozen partial extracts whose windows overlap
   them. The base `inadmissibles` table uses the annual and quarterly files covering non-overlapping periods in
   2014-2024, then `2025-01..05`, `2025-06..09-06` and `2025-09..2026-01` (trimmed to start
   2025-09-07): 19 files. The other 23 inadmissibles files are loaded unchanged into
   `inadmissibles_superseded`, and `_files` records the reason (`in_base_table`,
   `superseded_reason`). `_files` is the authoritative list; the counts here are copied from it.

Dates: DuckDB timestamps (Excel serials and `MM/DD/YYYY` text both parsed). Redaction
markers such as `(b)(6)` are stored as NULL.

### Build

```bash
uv sync
uv run python refresh_releases.py   # re-read the DDP page: adds new files to releases.json / download_list.tsv, reports removed ones (--check to only report)
./scripts_download.sh               # 121 files, 4.6 GB, from box.com links in download_list.tsv; exits 1 if any download failed
uv run python build_database.py  # ~45 minutes, DuckDB capped at 4 GB, pandas one sheet at a time
uv run python publish_to_hf.py --token hf_xxx --verify
```

### License

Code: MIT. Data: CC0 as published by the Deportation Data Project (public records).
