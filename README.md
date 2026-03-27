# SEC EDGAR Download Activity Pipeline

A data pipeline for constructing a firm-year panel of SEC EDGAR filing download activity (2003–2015), used as a proxy for investor attention.

## Overview

EDGAR server logs record every time a user downloads a filing from the SEC website. By aggregating these logs to the firm-year level, we can measure how much investor attention each firm received in a given year.

This pipeline filters the raw EDGAR logs to a target sample of firms, aggregates download counts by firm and year, and produces a clean panel dataset.

## Data Sources

**EDGAR server logs** — Daily CSV log files published by the SEC, structured as:
```
year/QTR{1-4}/f_YYYYMMDD.csv
```
Each row represents one filing access event with columns: `date`, `cik`, `accession`, `nr_total`, `htm`, `txt`, `xbrl`, `other`, `form`, `filing_date`.

Download from: [SEC EDGAR Full-Index](https://www.sec.gov/dera/data/edgar-log-file-data-set)

**Firm list** — An Excel file (`Firm list-full sample-2.xls`) defining the research sample with columns `cik` and `CompanyName`. Not included in this repository; provide your own.

## Pipeline

Run the scripts in this order:

### Step 1: Filter raw logs — `agg_filter_logs.py`
Reads all daily EDGAR log CSVs for a given year, filters to only the CIKs in your firm list, and saves the result.

- **Input:** `{year}/QTR*/f_YYYYMMDD.csv` + `Firm list-full sample-2.xls`
- **Output:** `{year}_edgar_downloads_filtered_all.csv`
- **Config:** Update `EDGAR_LOGS_ROOT` and `OUTPUT_PATH` at the top of the script for each year

### Step 2: Aggregate to firm-year — `agg_by_firm_year.py`
Takes the filtered log file and aggregates from daily rows to one row per (CIK × year), summing downloads by file type and counting unique filings accessed.

- **Input:** `{year}_edgar_downloads_filtered_all.csv`
- **Output:** `{year}_firm_year_downloads.csv`
- **Config:** Update `FILTERED_DATA_PATH` and `OUTPUT_PATH` at the top of the script for each year

Repeat Steps 1–2 for each year (2003–2015).

### Step 3: Combine all years — `all_years_combine_data.py`
Concatenates all per-year aggregated files into one panel dataset.

- **Input:** `{year}_firm_year_downloads.csv` for all years
- **Output:** `firm_year_downloads_2003_2015.csv`

### Step 4: Merge company names — `merge_firm_names.py`
Joins company name and ticker from the firm list onto the combined panel.

- **Input:** `firm_year_downloads_2003_2015.csv` + `Firm list-full sample-2.xls`
- **Output:** `firm_year_downloads_with_names.csv`

### Step 5: Validate — `validation.py`
Sanity check: confirms no unexpected CIKs appear in the output and reports coverage (how many target firms were found in the logs).

- **Input:** `2015_edgar_downloads_filtered_all.csv` + `Firm list-full sample-2.xls`

## Output Schema

Final output: `firm_year_downloads_with_names.csv`

| Column | Description |
|---|---|
| `cik` | SEC CIK identifier |
| `cmpy` | Ticker / short company code |
| `CompanyName` | Full company name |
| `year` | Calendar year |
| `total_downloads` | Total filing downloads that year |
| `htm_downloads` | HTML file downloads |
| `txt_downloads` | Plain text file downloads |
| `xbrl_downloads` | XBRL file downloads |
| `other_downloads` | Other file type downloads |
| `unique_filings_accessed` | Number of distinct filings accessed |

## Setup & Usage

```bash
pip install -r requirements.txt
```

Then run each script in order as described in the Pipeline section above. For Steps 1–2, loop over each year (2003–2015), updating the path configs at the top of each script before running.

## Project Structure

```
.
├── agg_filter_logs.py          # Step 1: filter raw logs to target CIKs
├── agg_by_firm_year.py         # Step 2: aggregate to firm-year level
├── all_years_combine_data.py   # Step 3: combine all years
├── merge_firm_names.py         # Step 4: merge company names
├── validation.py               # Step 5: sanity check
├── requirements.txt
└── README.md
```

Raw EDGAR log data, firm list, and output CSVs are excluded from this repository.
