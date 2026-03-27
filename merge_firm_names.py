"""
Merge firm names with EDGAR download data

Usage: python merge_firm_names.py
"""

import pandas as pd

# =============================================================
# CONFIGURATION - UPDATE THESE PATHS IF NEEDED
# =============================================================

FIRM_LIST_PATH = "Firm list-full sample-2.xls"
DOWNLOADS_PATH = "firm_year_downloads_2003_2015.csv"
OUTPUT_PATH = "firm_year_downloads_with_names.csv"

# =============================================================
# SCRIPT
# =============================================================

def main():
    print("Loading data...")
    
    # Load firm list
    firms = pd.read_excel(FIRM_LIST_PATH, sheet_name=0)
    
    # Load downloads
    downloads = pd.read_csv(DOWNLOADS_PATH)
    
    # Get unique CIK to company name mapping
    # Take first non-null value for each CIK
    firm_names = firms.groupby('cik').agg({
        'cmpy': 'first',
        'CompanyName': lambda x: x.dropna().iloc[0] if x.dropna().any() else None
    }).reset_index()
    
    firm_names['cik'] = firm_names['cik'].astype(int)
    
    # Merge
    merged = downloads.merge(firm_names, on='cik', how='left')
    
    # Reorder columns - put names first
    cols = ['cik', 'cmpy', 'CompanyName', 'year', 'total_downloads', 
            'htm_downloads', 'txt_downloads', 'xbrl_downloads', 
            'other_downloads', 'unique_filings_accessed']
    merged = merged[cols]
    
    # Sort
    merged = merged.sort_values(['cik', 'year'])
    
    # Save
    merged.to_csv(OUTPUT_PATH, index=False)
    
    # Summary
    print(f"\n{'='*60}")
    print("DONE!")
    print(f"{'='*60}")
    print(f"Total rows: {len(merged):,}")
    print(f"Unique firms: {merged['cik'].nunique()}")
    print(f"Firms with names: {merged['CompanyName'].notna().groupby(merged['cik']).first().sum()}")
    print(f"Output saved to: {OUTPUT_PATH}")
    
    # Preview
    print(f"\n{'='*60}")
    print("FIRST 20 ROWS")
    print(f"{'='*60}")
    print(merged.head(20).to_string(index=False))

if __name__ == "__main__":
    main()