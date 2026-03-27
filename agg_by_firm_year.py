"""
EDGAR Download Aggregation Script
Aggregates filtered EDGAR downloads to firm-year level.

Run this AFTER filter_edgar_logs_v2.py completes.

Usage: python aggregate_firm_year.py
"""

import pandas as pd
from pathlib import Path

# =============================================================
# CONFIGURATION - UPDATE THESE PATHS
# =============================================================

# Input: filtered EDGAR downloads (output from filter_edgar_logs_v2.py)
FILTERED_DATA_PATH = "2015_edgar_downloads_filtered_all.csv"

# Output: firm-year aggregated data
OUTPUT_PATH = "2015_firm_year_downloads.csv"

# =============================================================
# SCRIPT
# =============================================================

def main():
    print("="*60)
    print("EDGAR Download Aggregation")
    print("="*60)
    
    print("\nLoading filtered EDGAR data...")
    df = pd.read_csv(FILTERED_DATA_PATH)
    
    print(f"Loaded {len(df):,} rows")
    print(f"Columns: {df.columns.tolist()}")
    
    # Extract year from date column (format: YYYYMMDD)
    df['year'] = df['date'].astype(str).str[:4].astype(int)
    
    # Aggregate to firm-year level
    print("\nAggregating to firm-year level...")
    
    firm_year = df.groupby(['cik', 'year']).agg({
        'nr_total': 'sum',      # Total downloads
        'htm': 'sum',           # HTML downloads
        'txt': 'sum',           # Text downloads
        'xbrl': 'sum',          # XBRL downloads
        'other': 'sum',         # Other downloads
        'accession': 'nunique'  # Number of unique filings accessed
    }).reset_index()
    
    # Rename columns for clarity
    firm_year.columns = ['cik', 'year', 'total_downloads', 'htm_downloads', 
                         'txt_downloads', 'xbrl_downloads', 'other_downloads',
                         'unique_filings_accessed']
    
    # Sort by CIK and year
    firm_year = firm_year.sort_values(['cik', 'year'])
    
    # Save output
    firm_year.to_csv(OUTPUT_PATH, index=False)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Unique firms: {firm_year['cik'].nunique()}")
    print(f"Year range: {firm_year['year'].min()} - {firm_year['year'].max()}")
    print(f"Total firm-years: {len(firm_year)}")
    print(f"Total downloads: {firm_year['total_downloads'].sum():,}")
    print(f"\nOutput saved to: {OUTPUT_PATH}")
    print(f"File size: {Path(OUTPUT_PATH).stat().st_size / 1024:.1f} KB")
    
    # Downloads per year
    print(f"\n{'='*60}")
    print("DOWNLOADS BY YEAR")
    print(f"{'='*60}")
    yearly = firm_year.groupby('year').agg({
        'total_downloads': 'sum',
        'cik': 'nunique'
    }).rename(columns={'cik': 'num_firms'})
    print(yearly.to_string())
    
    # Summary stats
    print(f"\n{'='*60}")
    print("DOWNLOAD DISTRIBUTION (per firm-year)")
    print(f"{'='*60}")
    print(firm_year['total_downloads'].describe().to_string())
    
    # Preview
    print(f"\n{'='*60}")
    print("FIRST 20 ROWS")
    print(f"{'='*60}")
    print(firm_year.head(20).to_string(index=False))

if __name__ == "__main__":
    main()