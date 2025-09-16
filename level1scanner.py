import pandas as pd
from datetime import datetime

print("=" * 60)
print("LEVEL 1 STOCK SCREENER - FUNDAMENTAL FILTERS")
print("=" * 60)

# -------------------------------------------------------------------------
# Step 1: Read Excel File
# -------------------------------------------------------------------------
print("\nStep 1: Reading Excel file...")
df = pd.read_excel('NIFTY500masterlist.xlsx')
print(f"✅ Successfully loaded {len(df)} companies")

# --- Normalize column names (lowercase, underscores) ---
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace('%', '', regex=False)
    .str.replace('[()]', '', regex=True)
    .str.replace(' ', '_')
)

print("\nAvailable columns:", list(df.columns))

# -------------------------------------------------------------------------
# Step 2: Resolve columns we need
# -------------------------------------------------------------------------
COLUMN_ALIASES = {
    "company": ["company", "name", "company_name"],
    "industry": ["industry", "sector"],
    "current_price": ["current_price", "price", "cmp"],
    "pe": ["pe", "p/e", "price_to_earning"],
    "pb": ["pb", "p/b", "price_to_book"],
    "peg": ["peg", "peg_ratio"],
    "ev_ebitda": ["ev/ebitda", "ev_ebitda", "enterprise_value_to_ebitda"],
}

def resolve_column(alias_list):
    for col in alias_list:
        if col in df.columns:
            return col
    return None

col_company = resolve_column(COLUMN_ALIASES["company"])
col_industry = resolve_column(COLUMN_ALIASES["industry"])
col_price = resolve_column(COLUMN_ALIASES["current_price"])
col_pe = resolve_column(COLUMN_ALIASES["pe"])
col_pb = resolve_column(COLUMN_ALIASES["pb"])
col_peg = resolve_column(COLUMN_ALIASES["peg"])
col_ev_ebitda = resolve_column(COLUMN_ALIASES["ev_ebitda"])

# -------------------------------------------------------------------------
# Step 3: Apply Screening Conditions
# -------------------------------------------------------------------------
print("\nStep 2: Filtering with new conditions...")

criteria = []
if col_peg: criteria.append(df[col_peg] < 1.2)
if col_pe: criteria.append(df[col_pe] < 35)
if col_pb: criteria.append(df[col_pb] < 1.5)
if col_ev_ebitda: criteria.append(df[col_ev_ebitda] < 8)

if criteria:
    filtered_df = df.loc[pd.concat(criteria, axis=1).all(axis=1)]
else:
    filtered_df = pd.DataFrame()

print(f"\nCompanies meeting ALL conditions: {len(filtered_df)}")

# -------------------------------------------------------------------------
# Step 4: Save Results
# -------------------------------------------------------------------------
if not filtered_df.empty:
    today = datetime.today().strftime('%Y-%m-%d')
    filtered_df["date"] = today

    display_cols = [c for c in [col_company, col_industry, col_price, col_pe, col_pb, col_peg, col_ev_ebitda, "date"] if c]

    print("\nFiltered Companies:")
    print("-" * 100)
    print(filtered_df[display_cols].to_string(index=False))

    filtered_df[display_cols].to_excel("level1stocks.xlsx", index=False)
    print(f"\n✅ Saved {len(filtered_df)} companies to 'level1stocks.xlsx'")
else:
    print("❌ No companies met all strict criteria.")

print("\n" + "=" * 60)
print("LEVEL 1 SCREENING COMPLETED!")
print("=" * 60)
