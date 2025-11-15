import pandas as pd

# Read the CSV file
csv_file = 'nifty-500.csv'
df = pd.read_csv(csv_file)

# Write to Excel file
excel_file = 'NIFTY500masterlist.xlsx'
df.to_excel(excel_file, index=False)

print(f"Conversion complete. File saved as {excel_file}")
