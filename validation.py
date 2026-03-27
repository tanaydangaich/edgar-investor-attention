import pandas as pd

# Load your target CIKs
firms = pd.read_excel("Firm list-full sample-2.xls", sheet_name=0)
target_ciks = set(firms['cik'].dropna().astype(int))

# Load filtered results
filtered = pd.read_csv("2015_edgar_downloads_filtered_all.csv")
result_ciks = set(filtered['cik'].unique())

# Check for any CIKs that shouldn't be there
unexpected = result_ciks - target_ciks

if unexpected:
    print(f"❌ Found {len(unexpected)} unexpected CIKs:")
    print(unexpected)
else:
    print("✓ All CIKs in output are from target list")

# Check coverage
found = result_ciks & target_ciks
missing = target_ciks - result_ciks
print(f"\nCoverage: {len(found)}/{len(target_ciks)} firms found ({len(found)/len(target_ciks)*100:.1f}%)")
print(f"Missing: {len(missing)} firms (may not have filings in this period)")