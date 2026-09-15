# cbp Data Dictionary

Source: [Deportation Data Project - CBP](https://deportationdata.org/data/cbp.html) FOIA releases.
Columns are the union of every release's headers (synonyms merged); a NULL rate near 100% means only some releases carry the field.
`_files` lists every source file, its window, and whether it is part of the base tiling.

## apprehensions

Border Patrol apprehensions between ports of entry, one row per person apprehended (FOIA releases covering Oct 2007 - Dec 2025; monthly gaps where CBP has not yet released data)

Rows: 7,907,911

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| citizenship | VARCHAR | 0.0% | AFGHA |  |
| gender | VARCHAR | 0.0% | F |  |
| age | INTEGER | 0.1% | 0 |  |
| uac_indicator | VARCHAR | 92.5% | N |  |
| credible_fear_indicator | VARCHAR | 94.4% | N |  |
| marital_status | VARCHAR | 26.3% | D |  |
| entry_date | TIMESTAMP | 0.8% | 1800-04-13 00:00:00 |  |
| status_at_entry | VARCHAR | 5.8% | 324 |  |
| lpr | VARCHAR | 100.0% | LPR |  |
| event_datetime | TIMESTAMP | 4.4% | 2007-10-01 00:00:00 |  |
| sector | VARCHAR | 0.2% | BBT | Border Patrol sector (apprehensions/encounters) |
| disposition | VARCHAR | 0.0% | ADMDPT |  |
| statute_charge | VARCHAR | 23.5% | 10 USC 164C |  |
| arrest_method | VARCHAR | 0.0% | 287(g) Program |  |
| source_file | VARCHAR | 0.0% | 2007-10-01_2008-09-30_185.xlsx | FOIA release file the row came from; joins to _files.source_file |
| source_sheet | VARCHAR | 0.0% | APPs |  |
| window_start | VARCHAR | 0.0% | 2007-10-01 |  |
| window_end | VARCHAR | 0.0% | 2008-09-30 |  |
| referred_for_prosecution | VARCHAR | 84.5% | N |  |
| charge_code | VARCHAR | 89.6% | 18 USC 1001 |  |
| case_filing_date | TIMESTAMP | 89.7% | 1918-10-29 00:00:00 |  |
| fmua_indicator | VARCHAR | 79.9% | FMUA AAC |  |
| cds_program | VARCHAR | 88.0% | ACA_ECUA |  |
| ces_indicator | VARCHAR | 98.7% | Y |  |
| ncic_charge_code | VARCHAR | 98.7% | (b)(7)( E) |  |
| ncic_desc | VARCHAR | 98.7% | (b)(7)( E) |  |
| final_bookout_datetime | TIMESTAMP | 36.4% | 1900-01-01 00:00:00 |  |
| removal_type | VARCHAR | 51.2% | BKT |  |
| num_children_and_nationality | VARCHAR | 99.4% | 0 |  |
| civ_id | VARCHAR | 94.5% | (b)(6)(b)(7)( C) |  |
| of_subjects_per_event | VARCHAR | 94.5% | 1 |  |
| event_number | VARCHAR | 93.8% | (b)(6)(b)(7)( C)(b)(7)( E) | CBP event identifier where released |
| city_of_birth | VARCHAR | 97.7% | (HONDURAS) |  |
| birth_state | VARCHAR | 94.4% | AGUASCALIENTES |  |
| highest_statute_charge | VARCHAR | 95.8% | 18 USC 1001 |  |
| language | VARCHAR | 99.3% | #MULTIVALUE |  |
| num_previous_encounters | INTEGER | 94.8% | 0 |  |
| most_recent_prior_encounter_datetime | TIMESTAMP | 98.9% | 1998-05-01 20:00:00 |  |
| arrest_date | VARCHAR | 95.6% | 2024-04-01 00:00:00 |  |
| credible_fear_ind | VARCHAR | 98.3% | N |  |
| family_unit_group | VARCHAR | 98.8% | (b)(6)(b)(7)( C) |  |
| first_country_of_residence | VARCHAR | 96.5% | . |  |
| gang_indicator | VARCHAR | 100.0% | (b)(7)( E) |  |
| cds_program_code | VARCHAR | 97.8% | - |  |
| ces_criminal_indicator | VARCHAR | 95.7% | N |  |
| demographic | VARCHAR | 94.5% | FMUA |  |
| entry_status | VARCHAR | 94.2% | 324 |  |
| ethnicity | VARCHAR | 100.0% | H |  |
| juvenile | VARCHAR | 95.3% | N |  |
| transfer_to_ero | VARCHAR | 97.6% | BKT |  |
| civ_id_unique_identifier | VARCHAR | 100.0% |  |  |
| arrest_time | VARCHAR | 99.6% | 00:00:00 |  |
| charge_code_statue_charge | VARCHAR | 99.8% | 8 USC 1325 |  |
| ncic_charge_code_owned_by_doj_not_cbp | VARCHAR | 100.0% |  |  |
| ncic_desc_owned_by_doj_not_cbp | VARCHAR | 100.0% |  |  |
| landmark_name_for_latest_apprehension_withheld_in_full | VARCHAR | 100.0% |  |  |
| unique_case_id | VARCHAR | 100.0% |  |  |
| unique_person_identifier | VARCHAR | 100.0% |  |  |
| subject_key | VARCHAR | 99.3% | (b)(6)(b)(7)( C) | CBP anonymized person key where released (2021+ files only); not stable across releases |
| fmu_number | VARCHAR | 100.0% | (b)(6)(b)(7)( C) |  |
| sector_district | VARCHAR | 99.8% | BBT |  |
| general_processing_code | VARCHAR | 99.7% | ACA_HOND |  |
| transferred_to_group | VARCHAR | 99.3% | BKT |  |
| criminal_conviction | VARCHAR | 99.7% | N |  |
| ncic_charge_code_defer_to_doj | VARCHAR | 100.0% |  |  |
| ncic_desc_defer_to_doj | VARCHAR | 100.0% |  |  |
| state_of_birth | VARCHAR | 99.3% | AGUASCALIENTES |  |
| num_people_per_event | INTEGER | 99.3% | 1 |  |
| birth_date | TIMESTAMP | 100.0% |  |  |
| transferred_to_group_1 | VARCHAR | 99.4% | (b)(7)( E) |  |
| gang_name | VARCHAR | 100.0% | (b)(7)( E) |  |
| landmark_name_for_latest_apprehension | VARCHAR | 100.0% |  |  |
| country_of_res_cd | VARCHAR | 99.9% | AFGHA |  |
| country_of_birth | VARCHAR | 99.3% | AFGHA |  |
| statue_charge | VARCHAR | 100.0% | 8 USC 1325 |  |
| border | VARCHAR | 99.5% | CB |  |
| apprehension_time | VARCHAR | 99.5% | 00:00:00 |  |
| charge_code_statue_code | VARCHAR | 99.7% | 18 USC 1001 |  |
| suspected_gang_member | VARCHAR | 100.0% | (b)(7)( E) |  |
| most_recent_prior_entry_date_time | VARCHAR | 99.8% | 1980-01-01 12:00:00 |  |
| landmark | VARCHAR | 99.5% | (b)(7)( E) |  |

## apprehensions_origin

Border Patrol apprehensions with place of birth (country/state/city), one row per apprehension, FY2000 - FY2022

Rows: 16,719,589

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| fy | INTEGER | 100.0% |  |  |
| country_of_birth | VARCHAR | 0.0% | AFGHANISTAN |  |
| state_of_birth | VARCHAR | 13.2% | AGUASCALIENTES |  |
| city_of_birth | VARCHAR | 34.9% |                     HUE |  |
| age | INTEGER | 0.1% | -620 |  |
| gender | VARCHAR | 0.0% | Female |  |
| ethnicity | VARCHAR | 98.8% | Hispanic or Latino |  |
| language | VARCHAR | 13.5% | 
 |  |
| source_file | VARCHAR | 0.0% | 1999-10-01_2000-09-30_194.xlsx | FOIA release file the row came from; joins to _files.source_file |
| source_sheet | VARCHAR | 0.0% | APR-SEP |  |
| window_start | VARCHAR | 0.0% | 1999-10-01 |  |
| window_end | VARCHAR | 0.0% | 2000-09-30 |  |
| demographic | VARCHAR | 66.2% | FMUA |  |
| head_of_family_ind | VARCHAR | 96.5% | Y |  |
| number_of_fmu_members | INTEGER | 95.6% | 1 |  |
| title_8_subjects_in_fmu | INTEGER | 95.6% | 1 |  |

## encounters

Border Patrol encounters (apprehensions with prior-encounter history and seizure fields), FY2010 - FY2018 and Oct 2022 - Sep 2024

Rows: 7,164,459

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| event_datetime | TIMESTAMP | 0.0% | 2009-10-01 00:01:00 |  |
| border | VARCHAR | 0.0% | BORDER |  |
| sector | VARCHAR | 1.7% | APPREHENSION
SECTOR | Border Patrol sector (apprehensions/encounters) |
| state | VARCHAR | 70.2% | (b)(7)( E) |  |
| latitude | VARCHAR | 68.5% | (b)(7)( E) |  |
| disposition | VARCHAR | 0.0% | ADMDPT |  |
| mpp_indicator | VARCHAR | 0.0% | MPP_INDICATOR (Y/N) |  |
| spp_program | VARCHAR | 98.1% | ACA_GUAT |  |
| citizenship | VARCHAR | 0.0% | AFGHANISTAN |  |
| num_previous_encounters | INTEGER | 11.7% | 0 |  |
| most_recent_prior_encounter_datetime | TIMESTAMP | 11.7% | 2009-10-01 00:00:00 |  |
| earliest_encounter_date | TIMESTAMP | 11.7% | 1998-10-01 00:00:00 |  |
| ces_indicator | VARCHAR | 0.0% | CES(Y/N) |  |
| uac_indicator | VARCHAR | 93.5% | N |  |
| gang_indicator | VARCHAR | 100.0% | (b)(7)( E) |  |
| drugs_seized_during_apprehension | VARCHAR | 0.0% | DRUGS SEIZED 
DURING APPREHENSION (Y/N) |  |
| type_of_drugs_seized_during_apprehension | VARCHAR | 99.8% | CAP, MAR |  |
| marital_status | VARCHAR | 27.0% | Divorced |  |
| age | INTEGER | 0.0% | 0 |  |
| juvenile | VARCHAR | 0.0% | ADULT OR JUVENILE |  |
| country_of_residence | VARCHAR | 30.3% | AFGHANISTAN |  |
| smuggled_cost | VARCHAR | 92.2% | 0 |  |
| referred_for_prosecution | VARCHAR | 0.0% | Not referred |  |
| statute_charge | VARCHAR | 14.5% | 10 USC 164C |  |
| gender | VARCHAR | 0.0% | Female |  |
| time_in_us | VARCHAR | 8.3% | 1 month to 1 year |  |
| num_children_and_nationality | VARCHAR | 75.0% | ! EL SALVADOR |  |
| arrest_at_checkpoint | VARCHAR | 0.0% | ARREST_AT_CHECKPOINT (Y/N) |  |
| city_of_residence | VARCHAR | 44.2% |  Ciudad de Quito, |  |
| currency_seiz_during_app | VARCHAR | 100.0% | (b)(7)( E) |  |
| source_file | VARCHAR | 0.0% | 2009-10-01_2010-09-30_181.xlsx | FOIA release file the row came from; joins to _files.source_file |
| source_sheet | VARCHAR | 0.0% | FY23 Q1 |  |
| window_start | VARCHAR | 0.0% | 2009-10-01 |  |
| window_end | VARCHAR | 0.0% | 2010-09-30 |  |
| demographic | VARCHAR | 6.5% | DEMOGRAPHIC |  |
| final_bookout_datetime | TIMESTAMP | 26.0% | 2013-10-01 08:24:42 |  |
| transferred_to_group | VARCHAR | 26.0% | BKT |  |
| sector_of_booked_out | VARCHAR | 64.8% | (b)(7)( E) |  |

## inadmissibles

Office of Field Operations events where a person arriving at a port of entry was deemed inadmissible, one row per event, CY2014 - Jan 2026

Rows: 11,591,432

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| calendar_year | INTEGER | 2.6% | 2014 |  |
| event_datetime | TIMESTAMP | 0.0% | 2014-01-01 00:01:43 |  |
| final_bookout_datetime | TIMESTAMP | 12.1% | 1914-09-20 09:13:00 |  |
| disposition | VARCHAR | 0.0% | ABSCONDER |  |
| mode_of_transport | VARCHAR | 0.0% | AIR |  |
| north_south_indicator | VARCHAR | 34.1% | N |  |
| citizenship | VARCHAR | 0.0% | AFGHANISTAN |  |
| fmua_uac_am_single | VARCHAR | 0.0% | AM |  |
| age | INTEGER | 0.0% | -1 |  |
| country_of_birth | VARCHAR | 0.0% | AFGHANISTAN |  |
| presented_to_ausa | VARCHAR | 98.5% | (b)(7)( E) |  |
| charge | VARCHAR | 13.2% | 10 USC 164C-COMMAND AUTH. COMBATANT COMMANDERS |  |
| duplicate_subject_indicator | VARCHAR | 44.5% | #MULTIVALUE |  |
| entry_status | VARCHAR | 0.0% | ASYLEE |  |
| gender | VARCHAR | 0.0% | F - FEMALE |  |
| country_name | VARCHAR | 19.6% | AFGHANISTAN |  |
| transferred_to_group | VARCHAR | 69.3% | FEDERAL/STATE/LOCAL FACILITY |  |
| gang_affiliation_name | VARCHAR | 100.0% | (b)(7)( E) |  |
| gang_affiliation_comments | VARCHAR | 100.0% | (b)(7)( E) |  |
| field_office_name | VARCHAR | 0.0% | ATLANTA | OFO field office (inadmissibles) |
| state | VARCHAR | 12.2% | (b)(7)( E) |  |
| marital_status | VARCHAR | 31.8% | DIVORCED |  |
| destination_address_in_u_s | VARCHAR | 96.7% | (b)(6)(b)(7)( C) |  |
| source_file | VARCHAR | 0.0% | 2014-01-01_2014-12-31_167.xlsx | FOIA release file the row came from; joins to _files.source_file |
| source_sheet | VARCHAR | 0.0% | 2014 |  |
| window_start | VARCHAR | 0.0% | 2014-01-01 |  |
| window_end | VARCHAR | 0.0% | 2014-12-31 |  |
| calendar_month | VARCHAR | 17.7% | 2017-01-01 00:00:00 |  |
| credible_fear_indicator | VARCHAR | 95.7% | NO |  |
| event_reason | VARCHAR | 95.7% | ADMINISTRATIVE ALIEN SMUGGLING |  |
| person_count | INTEGER | 97.4% | 1 |  |
| approving_supervisor | VARCHAR | 100.0% |  |  |
| alien_file_number | VARCHAR | 100.0% |  |  |
| subject_key | VARCHAR | 100.0% |  | CBP anonymized person key where released (2021+ files only); not stable across releases |
| sigma_event_id | VARCHAR | 100.0% |  |  |

## title42_expulsions

Title 42 expulsions by Border Patrol, one row per expulsion, FY2020 - FY2022

Rows: 1,976,471

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| fy | INTEGER | 100.0% |  |  |
| subject_key | VARCHAR | 100.0% |  | CBP anonymized person key where released (2021+ files only); not stable across releases |
| month | VARCHAR | 0.0% | Apr |  |
| event_datetime | TIMESTAMP | 0.0% | 2020-03-20 03:05:45 |  |
| final_bookout_datetime | TIMESTAMP | 72.0% | 2020-03-23 01:26:00 |  |
| disposition | VARCHAR | 0.0% | DTNR |  |
| border | VARCHAR | 0.0% | CBO |  |
| sector | VARCHAR | 100.0% |  | Border Patrol sector (apprehensions/encounters) |
| citizenship | VARCHAR | 0.0% | AFGHANISTAN |  |
| num_previous_encounters | INTEGER | 0.0% | 0 |  |
| most_recent_prior_encounter_datetime | TIMESTAMP | 41.9% | 1998-10-01 00:00:00 |  |
| demographic | VARCHAR | 0.0% | Family Unit / Group |  |
| age | INTEGER | 0.0% | 0 |  |
| country_of_birth | VARCHAR | 0.0% | AFGHANISTAN |  |
| status_at_entry | VARCHAR | 0.0% | Asylum |  |
| gender | VARCHAR | 0.0% | Female |  |
| num_children | INTEGER | 100.0% |  |  |
| ces_indicator | VARCHAR | 98.8% | Y |  |
| gang_indicator | VARCHAR | 100.0% | Y |  |
| title_group | VARCHAR | 0.0% | T42 Delayed |  |
| source_file | VARCHAR | 0.0% | 2019-10-01_2020-09-30_143.xlsx | FOIA release file the row came from; joins to _files.source_file |
| source_sheet | VARCHAR | 0.0% | Sheet1 |  |
| window_start | VARCHAR | 0.0% | 2019-10-01 |  |
| window_end | VARCHAR | 0.0% | 2020-09-30 |  |

## cbp_one

CBP One app appointments at ports of entry, individual-level extract, Jan 12 - Oct 31 2023

Rows: 323,686

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| event_datetime | TIMESTAMP | 0.0% | 2023-01-12 00:00:00 |  |
| port_name | VARCHAR | 100.0% |  |  |
| site_code | VARCHAR | 100.0% |  |  |
| citizenship | VARCHAR | 0.1% | AFG |  |
| birth_date | TIMESTAMP | 100.0% |  |  |
| age | INTEGER | 0.0% | 0 |  |
| gender | VARCHAR | 0.0% | F |  |
| country_of_birth | VARCHAR | 0.1% | ABW |  |
| country_of_citizenship | VARCHAR | 0.1% | AFG |  |
| class_of_admission | VARCHAR | 0.0% | AS |  |
| appointment_created_datetime | TIMESTAMP | 100.0% |  |  |
| requested_entry_date | TIMESTAMP | 20.0% | 2021-05-17 00:00:00 |  |
| requested_port_code | VARCHAR | 100.0% |  |  |
| grp | VARCHAR | 18.0% | YES |  |
| language | VARCHAR | 0.0% | ACR |  |
| source_file | VARCHAR | 0.0% | 2023-01-12_2023-10-31_118.xlsx | FOIA release file the row came from; joins to _files.source_file |
| source_sheet | VARCHAR | 0.0% | CBP One Processed |  |
| window_start | VARCHAR | 0.0% | 2023-01-12 |  |
| window_end | VARCHAR | 0.0% | 2023-10-31 |  |

## cbp_one_monthly

CBP One monthly appointment counts by port of entry and citizenship (five overlapping FOIA extracts; see source_file)

Rows: 27,731

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| fiscal_month | VARCHAR | 46.3% | FY 21-08 (MAY) |  |
| port_name | VARCHAR | 99.9% | (b)(7)(e) |  |
| citizenship | VARCHAR | 0.0% | AFGHANISTAN |  |
| fmua_uac_am_single | VARCHAR | 46.3% | AM |  |
| nta_or_paroled_released_with_cbp1 | VARCHAR | 83.2% | 1 |  |
| not_released_with_cbp1 | VARCHAR | 92.9% | 1 |  |
| ratio | VARCHAR | 100.0% | 0.9624 |  |
| source_file | VARCHAR | 0.0% | 2021-05-01_2023-12-31_111.xlsx | FOIA release file the row came from; joins to _files.source_file |
| source_sheet | VARCHAR | 0.0% | Sheet1 |  |
| window_start | VARCHAR | 0.0% | 2021-05-01 |  |
| window_end | VARCHAR | 0.0% | 2022-11-30 |  |
| mode_of_transport | VARCHAR | 99.9% | LAND |  |
| last_foreign_airport_name | VARCHAR | 99.9% | NONE/UNKNOWN |  |
| disposition | VARCHAR | 98.9% | PAROLED-(RCO)-COLOMBIAN FAMILY REUNIFICATION PAROLE |  |
| person_count | INTEGER | 99.9% | 1 |  |
| chnv_parole | VARCHAR | 67.0% | 1 |  |
| date | TIMESTAMP | 53.7% | 2023-05-11 00:00:00 |  |
| t8_count | VARCHAR | 53.7% | 1 |  |
| frp_count | VARCHAR | 98.9% | 1 |  |

## inadmissibles_superseded

Rows from inadmissibles release files whose windows overlap the base tiling (see _files.superseded_reason); same schema as inadmissibles

Rows: 5,634,463

| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
| citizenship | VARCHAR | 0.0% | AFGHANISTAN |  |
| gender | VARCHAR | 23.7% | F - FEMALE |  |
| age | INTEGER | 0.0% | 0 |  |
| uac_indicator | VARCHAR | 99.7% | YES |  |
| fmua_indicator | VARCHAR | 60.4% | NO |  |
| credible_fear_indicator | VARCHAR | 16.1% | NO |  |
| marital_status | VARCHAR | 61.8% | DIVORCED |  |
| event_datetime | TIMESTAMP | 0.0% | 2020-04-01 01:40:48 |  |
| field_office_name | VARCHAR | 0.0% | ATLANTA | OFO field office (inadmissibles) |
| entry_status | VARCHAR | 0.0% | ASYLEE |  |
| event_reason | VARCHAR | 16.1% | ADMINISTRATIVE ALIEN SMUGGLING |  |
| disposition | VARCHAR | 0.0% | ABSCONDER |  |
| transferred_to_group | VARCHAR | 76.1% | FEDERAL/STATE/LOCAL FACILITY |  |
| final_bookout_datetime | TIMESTAMP | 12.2% | 2020-02-15 20:58:00 |  |
| person_count | INTEGER | 0.6% | 1 |  |
| source_file | VARCHAR | 0.0% | 2020-04-01_2022-03-31_134.xlsx | FOIA release file the row came from; joins to _files.source_file |
| source_sheet | VARCHAR | 0.0% | Detail |  |
| window_start | VARCHAR | 0.0% | 2020-04-01 |  |
| window_end | VARCHAR | 0.0% | 2022-03-31 |  |
| fmua_uac_am_single | VARCHAR | 68.4% | AM |  |
| mode_of_transport | VARCHAR | 71.3% | AIR |  |
| state | VARCHAR | 83.9% | AK |  |
| city_name | VARCHAR | 87.2% | (NAVARRA) |  |
| country | VARCHAR | 85.7% | AFGHANISTAN |  |
| calendar_year | INTEGER | 100.0% |  |  |
| calendar_month | VARCHAR | 83.9% | 2024-10-01 00:00:00 |  |
| north_south_indicator | VARCHAR | 86.2% | N |  |
| country_of_birth | VARCHAR | 83.3% | AFGHANISTAN |  |
| charge | VARCHAR | 83.7% | 18 USC 1001-GENERAL FRAUD/MAKING FALSE STATEMENT |  |
| presented_to_ausa | VARCHAR | 99.8% | NO |  |
| destination_address_in_u_s | VARCHAR | 99.7% | (b)(6)(b)(7)( C) |  |
| gang_affiliation_comments | VARCHAR | 100.0% | (b)(7)( E) |  |
| alien_file_number | VARCHAR | 100.0% |  |  |
| subject_key | VARCHAR | 100.0% |  | CBP anonymized person key where released (2021+ files only); not stable across releases |
| sigma_event_id | VARCHAR | 100.0% |  |  |
| calendar_month_name | VARCHAR | 99.4% | SEPTEMBER |  |
| duplicate_subject_indicator | VARCHAR | 99.6% | Duplicate Subject to Previous Row |  |
| gang_affiliation_name | VARCHAR | 100.0% |  |  |
| first_street_name | VARCHAR | 100.0% |  |  |
| state_name | VARCHAR | 99.8% | ALABAMA |  |
| postal_zip_code | VARCHAR | 100.0% |  |  |

## _files


| Column | Type | Nulls | Example | Join |
|--------|------|-------|---------|------|
