import pandas as pd

# Read CSV file
df = pd.read_csv('nifty-500 (4).csv')

# Write to Excel file
df.to_excel('NIFTY500masterlist.xlsx', index=False)
