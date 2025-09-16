import pandas as pd
from datetime import datetime

print("=" * 60)
print("LEVEL 4 STOCK SCREENER - FUNDAMENTAL FILTERS")
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
    "current_price": ["current_price", "price", "cmp", "market_price"],
    "pe": ["pe", "p/e", "price_to_earning", "price_to_earnings"],
    "peg": ["peg", "peg_ratio"],
    "roe": ["roe", "return_on_equity", "return_on_equity_%"],
    "roce": ["roce", "return_on_capital_employed", "roce_%"],
    "eps": ["eps", "earnings_per_share"],
    "current_ratio": ["current_ratio", "cr"],
    "quick_ratio": ["quick_ratio", "qr"],
    "interest_coverage": ["interest_coverage", "interest_coverage_ratio", "icr"],
    "debt_to_equity": ["debt_to_equity", "d/e", "de_ratio", "debt_equity_ratio"],
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
col_peg = resolve_column(COLUMN_ALIASES["peg"])
col_roe = resolve_column(COLUMN_ALIASES["roe"])
col_roce = resolve_column(COLUMN_ALIASES["roce"])
col_eps = resolve_column(COLUMN_ALIASES["eps"])
col_current_ratio = resolve_column(COLUMN_ALIASES["current_ratio"])
col_quick_ratio = resolve_column(COLUMN_ALIASES["quick_ratio"])
col_interest_coverage = resolve_column(COLUMN_ALIASES["interest_coverage"])
col_debt_to_equity = resolve_column(COLUMN_ALIASES["debt_to_equity"])

# Debug: print resolved columns
print("\nResolved Columns:")
print("Company:", col_company)
print("Industry:", col_industry)
print("Current Price:", col_price)
print("P/E:", col_pe)
print("PEG:", col_peg)
print("ROE:", col_roe)
print("ROCE:", col_roce)
print("EPS:", col_eps)
print("Current Ratio:", col_current_ratio)
print("Quick Ratio:", col_quick_ratio)
print("Interest Coverage:", col_interest_coverage)
print("Debt to Equity:", col_debt_to_equity)

# -------------------------------------------------------------------------
# Step 3: Apply Screening Conditions
# -------------------------------------------------------------------------
print("\nStep 2: Filtering with Level 4 conditions...")

criteria = []
if col_peg: criteria.append(df[col_peg] < 1.2)
if col_pe: criteria.append(df[col_pe] < 35)
if col_roe: criteria.append(df[col_roe] > 20)
if col_roce: criteria.append(df[col_roce] > 20)
if col_eps: criteria.append(df[col_eps] > 18)
if col_current_ratio: criteria.append(df[col_current_ratio] > 1)
if col_quick_ratio: criteria.append(df[col_quick_ratio] > 0.7)
if col_interest_coverage: criteria.append(df[col_interest_coverage] > 4)
if col_debt_to_equity: criteria.append(df[col_debt_to_equity] < 2.2)

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

    display_cols = [
        col_company, col_industry, col_price,
        col_pe, col_peg, col_roe, col_roce, col_eps,
        col_current_ratio, col_quick_ratio,
        col_interest_coverage, col_debt_to_equity,
        "date"
    ]

    # Replace None with a placeholder column if missing
    for c in display_cols:
        if c is None and c != "date":
            filtered_df[c] = None

    display_cols = [c for c in display_cols if c]

    print("\nFiltered Companies:")
    print("-" * 100)
    print(filtered_df[display_cols].to_string(index=False))

    filtered_df[display_cols].to_excel("level4stocks.xlsx", index=False)
    print(f"\n✅ Saved {len(filtered_df)} companies to 'level4stocks.xlsx'")
else:
    print("❌ No companies met all strict criteria.")

print("\n" + "=" * 60)
print("LEVEL 4 SCREENING COMPLETED!")
print("=" * 60)
