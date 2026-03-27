"""
EDGAR Server Log Filter Script (v2)
Handles nested folder structure: year/QTR/files.csv

Usage:
1. Update the paths below
2. Run: python filter_edgar_logs_v2.py
"""

import pandas as pd
from pathlib import Path
import time

# =============================================================
# CONFIGURATION - UPDATE THESE PATHS
# =============================================================

# Path to your firm list Excel file
FIRM_LIST_PATH = "Firm list-full sample-2.xls"

# Path to root folder containing year folders (e.g., 2003/, 2004/, etc.)
EDGAR_LOGS_ROOT = "2015/"  # UPDATE THIS

# Output file path
OUTPUT_PATH = "2015_edgar_downloads_filtered_all.csv"

# =============================================================
# SCRIPT - No need to modify below
# =============================================================

def load_target_ciks(firm_list_path):
    """Load unique CIKs from the firm list Excel file."""
    df = pd.read_excel(firm_list_path, sheet_name=0)
    ciks = set(df['cik'].dropna().astype(int).unique())
    print(f"Loaded {len(ciks)} unique CIKs from firm list")
    return ciks

def process_edgar_logs(logs_root, target_ciks, output_path):
    """Process all EDGAR log files recursively through year/QTR folders."""
    
    logs_path = Path(logs_root)
    
    # Find all CSV files recursively (handles year/QTR/files.csv structure)
    csv_files = list(logs_path.glob("**/*.csv")) + list(logs_path.glob("**/*.csv.gz"))
    
    print(f"Found {len(csv_files)} log files to process")
    
    results = []
    total_rows_processed = 0
    total_rows_matched = 0
    
    start_time = time.time()
    
    for i, file in enumerate(sorted(csv_files)):
        try:
            # Read file (handles both .csv and .csv.gz)
            if file.suffix == '.gz' or '.gz' in file.suffixes:
                df = pd.read_csv(file, compression='gzip')
            else:
                df = pd.read_csv(file)
            
            total_rows_processed += len(df)
            
            # Filter to target CIKs
            filtered = df[df['cik'].isin(target_ciks)]
            
            if len(filtered) > 0:
                results.append(filtered)
                total_rows_matched += len(filtered)
            
            # Progress update every 50 files
            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                pct = (i + 1) / len(csv_files) * 100
                print(f"[{pct:5.1f}%] Processed {i+1}/{len(csv_files)} files | "
                      f"Matched {total_rows_matched:,} rows | "
                      f"Time: {elapsed:.1f}s | "
                      f"Current: {file.parent.parent.name}/{file.parent.name}")
                
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    
    # Combine all results
    if results:
        print("\nCombining results...")
        final_df = pd.concat(results, ignore_index=True)
        
        # Sort by date and CIK
        final_df = final_df.sort_values(['date', 'cik'])
        
        final_df.to_csv(output_path, index=False)
        
        elapsed = time.time() - start_time
        print(f"\n{'='*60}")
        print(f"DONE!")
        print(f"Total rows processed: {total_rows_processed:,}")
        print(f"Total rows matched: {total_rows_matched:,}")
        print(f"Unique CIKs found: {final_df['cik'].nunique()}")
        print(f"Date range: {final_df['date'].min()} - {final_df['date'].max()}")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {Path(output_path).stat().st_size / 1024 / 1024:.2f} MB")
        print(f"Total time: {elapsed/60:.1f} minutes")
        print(f"{'='*60}")
    else:
        print("No matching rows found!")

def main():
    print("="*60)
    print("EDGAR Server Log Filter")
    print("="*60)
    
    print("\nLoading target CIKs...")
    target_ciks = load_target_ciks(FIRM_LIST_PATH)
    
    print("\nProcessing EDGAR log files...")
    process_edgar_logs(EDGAR_LOGS_ROOT, target_ciks, OUTPUT_PATH)

if __name__ == "__main__":
    main()