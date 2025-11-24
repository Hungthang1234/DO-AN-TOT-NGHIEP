import pandas as pd

df = pd.read_csv('Data/cleaned_real_estate.csv')

print(f'\nTotal rows: {len(df):,}')
print(f'Year range: {df["year"].min()} - {df["year"].max()}')
print(f'Number of unique years: {df["year"].nunique()}')
print(f'\nYears available: {sorted(df["year"].unique())}')
print('\nRecords per year:')
print(df['year'].value_counts().sort_index())

# Check correlation with full dataset
print('\n' + '='*70)
print('CORRELATION WITH FULL DATASET')
print('='*70)
corr = df[['year', 'price', 'area_m2']].corr()
print(corr)
print(f'\n📊 Correlation year vs price: {corr.loc["year", "price"]:.4f}')
