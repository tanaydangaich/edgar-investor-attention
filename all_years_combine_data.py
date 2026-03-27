import pandas as pd
from pathlib import Path

# Find all year files
files = sorted(Path('.').glob('*_firm_year_downloads.csv'))

print(f"Found {len(files)} files:")
for f in files:
    print(f"  {f.name}")

# Combine
combined = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Sort by firm and year
combined = combined.sort_values(['cik', 'year'])

# Save
combined.to_csv('firm_year_downloads_2003_2015.csv', index=False)

print(f"\nDone! Combined {len(combined):,} rows")
print(f"Unique firms: {combined['cik'].nunique()}")
print(f"Year range: {combined['year'].min()} - {combined['year'].max()}")