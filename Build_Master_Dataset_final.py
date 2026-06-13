"""
Build a clean master dataset for an MSc International Finance dissertation.

Dissertation:
    "Does the Inclusion of Additional Financial Information Improve Stock Return
    Prediction Accuracy? Evidence from CAPM, Extended Financial Models, and Random
    Forest Models on S&P 500 Stocks (2008-2024)"

Usage:
    Place the three input files in the same folder as this script (or a sub-folder
    called 'inputs/'), then run:

        python Build_Master_Dataset_final.py

    All outputs are written relative to this script's location — no hard-coded
    paths, so the folder can be moved or shared without modification.

Inputs  (searched in: <script dir>/inputs/, then <script dir>/)
    SP500_20_Companies_Monthly.csv
    SP500_Market_Returns.csv
    TB3MS.csv                          (FRED 3-Month Treasury Bill rate)

Outputs  (written to <script dir>/outputs/)
    Master_Dataset.csv
    Data_Quality_Report.txt
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Path resolution — all paths relative to this script
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent.resolve()

def _locate(filename: str) -> Path:
    """Search inputs/ sub-folder, then script directory."""
    for candidate in [SCRIPT_DIR / "inputs" / filename, SCRIPT_DIR / filename]:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Cannot find '{filename}'.  "
        f"Place it in '{SCRIPT_DIR / 'inputs'}' or '{SCRIPT_DIR}'."
    )

OUTPUT_DIR = SCRIPT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STOCK_FILE  = _locate("SP500_20_Companies_Monthly.csv")
MARKET_FILE = _locate("SP500_Market_Returns.csv")
TBILL_FILE  = _locate("TB3MS.csv")

MASTER_OUTPUT = OUTPUT_DIR / "Master_Dataset.csv"
REPORT_OUTPUT = OUTPUT_DIR / "Data_Quality_Report.txt"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def monthly_date_key(series: pd.Series) -> pd.Series:
    """Convert a date series to month-start datetime (period-safe)."""
    return pd.to_datetime(series, errors="coerce").dt.to_period("M").dt.to_timestamp()


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    missing_count = df.isna().sum()
    missing_pct   = (missing_count / len(df) * 100).round(2)
    return pd.DataFrame({"Missing_Count": missing_count, "Missing_Percent": missing_pct})


def section(title: str) -> str:
    return f"\n{title}\n{'=' * len(title)}\n"


# ---------------------------------------------------------------------------
# Step 1: Load raw files
# ---------------------------------------------------------------------------

stocks = pd.read_csv(STOCK_FILE)
market = pd.read_csv(MARKET_FILE)
tbill  = pd.read_csv(TBILL_FILE)

raw_shapes = {
    "Stocks":        stocks.shape,
    "Market":        market.shape,
    "Treasury Bill": tbill.shape,
}

# FRED TB3MS may export the date column under different names
tbill_date_col = next(
    (c for c in ["DATE", "Date", "observation_date"] if c in tbill.columns), None
)
if tbill_date_col is None:
    raise ValueError("TB3MS file must contain DATE, Date, or observation_date.")

stocks["Date"] = monthly_date_key(stocks["Date"])
market["Date"] = monthly_date_key(market["Date"])
tbill["Date"]  = monthly_date_key(tbill[tbill_date_col])


# ---------------------------------------------------------------------------
# Step 2: Deduplication and sorting
# ---------------------------------------------------------------------------

missing_before   = {k: missing_report(df) for k, df in
                    [("Stocks", stocks), ("Market", market), ("Treasury Bill", tbill)]}
duplicate_counts = {k: int(df.duplicated().sum()) for k, df in
                    [("Stocks", stocks), ("Market", market), ("Treasury Bill", tbill)]}

stocks = stocks.drop_duplicates().sort_values(["Ticker", "Date"]).reset_index(drop=True)
market = market.drop_duplicates().sort_values("Date").reset_index(drop=True)
tbill  = tbill.drop_duplicates().sort_values("Date").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Step 3: Merge market returns and risk-free rate
# ---------------------------------------------------------------------------

master = stocks.merge(market[["Date", "Market_Return"]], on="Date", how="left", validate="many_to_one")
master = master.merge(tbill[["Date", "TB3MS"]],          on="Date", how="left", validate="many_to_one")


# ---------------------------------------------------------------------------
# Step 4 – 8: Derived features
#   Risk_Free_Rate : monthly decimal from annualised TB3MS
#   Excess_Return  : stock return minus risk-free rate
#   Excess_Market_Return : market return minus risk-free rate
#   Lagged_Return  : one-month lag of stock return (shift(1) within ticker)
#   Volatility     : trailing 12-month std of stock return (shift(1) applied first)
#   Momentum       : trailing 12-month compounded return  (shift(1) applied first)
#
# NOTE — look-ahead prevention:
#   Both rolling features call shift(1) BEFORE the rolling window, so the
#   feature observed at month t uses only returns up to t-1.  This mirrors
#   standard practice in the empirical-finance literature and avoids any form
#   of in-sample information leakage.
# ---------------------------------------------------------------------------

master["Risk_Free_Rate"]       = (master["TB3MS"] / 100) / 12
master["Excess_Return"]        = master["Return"] - master["Risk_Free_Rate"]
master["Excess_Market_Return"] = master["Market_Return"] - master["Risk_Free_Rate"]

master["Lagged_Return"] = master.groupby("Ticker")["Return"].shift(1)

master["Volatility"] = (
    master.groupby("Ticker")["Return"]
    .transform(lambda s: s.shift(1).rolling(window=12, min_periods=12).std())
)

master["Momentum"] = (
    master.groupby("Ticker")["Return"]
    .transform(
        lambda s: s.shift(1)
        .rolling(window=12, min_periods=12)
        .apply(lambda x: np.prod(1 + x) - 1, raw=True)
    )
)


# ---------------------------------------------------------------------------
# Step 9: Sector dummy variables
# ---------------------------------------------------------------------------

sector_dummies = pd.get_dummies(master["Sector"], dtype=int)
for sector in ["Technology", "Financials", "Healthcare", "Consumer"]:
    if sector not in sector_dummies.columns:
        sector_dummies[sector] = 0

master = pd.concat(
    [master, sector_dummies[["Technology", "Financials", "Healthcare", "Consumer"]]],
    axis=1,
)


# ---------------------------------------------------------------------------
# Step 10: Final column selection and sort
# ---------------------------------------------------------------------------

FINAL_COLS = [
    "Date", "Ticker", "Sector", "Return",
    "Market_Return", "Risk_Free_Rate",
    "Excess_Return", "Excess_Market_Return",
    "Lagged_Return", "Volatility", "Momentum",
    "Technology", "Financials", "Healthcare", "Consumer",
]

master = master.sort_values(["Date", "Ticker"]).reset_index(drop=True)[FINAL_COLS]

VALIDATION_VARS = ["Return", "Market_Return", "Risk_Free_Rate",
                   "Lagged_Return", "Volatility", "Momentum"]
summary_stats  = master[VALIDATION_VARS].describe().T
final_missing  = missing_report(master)

# Integrity checks
n_stocks        = master["Ticker"].nunique()
obs_per_ticker  = master.groupby("Ticker").size()
abbv_rows       = int(obs_per_ticker.get("ABBV", 0))
other_rows      = [int(v) for t, v in obs_per_ticker.items() if t != "ABBV"]
sector_sum_ok   = int((master[["Technology", "Financials", "Healthcare", "Consumer"]].sum(axis=1) != 1).sum())

print(f"Total rows       : {len(master)}")
print(f"Stocks           : {n_stocks}")
print(f"ABBV rows        : {abbv_rows}  (expected 144 — spin-off Jan 2013)")
print(f"Other ticker rows: {set(other_rows)} (expected {{204}})")
print(f"Sector dummy sum ≠ 1 rows: {sector_sum_ok} (expected 0)")


# ---------------------------------------------------------------------------
# Step 11: Save outputs
# ---------------------------------------------------------------------------

master.to_csv(MASTER_OUTPUT, index=False)

lines = ["DATA QUALITY REPORT\n",
         "Master dataset for: Does the Inclusion of Additional Financial Information Improve "
         "Stock Return Prediction Accuracy? Evidence from CAPM, Extended Financial Models, "
         "and Random Forest Models on S&P 500 Stocks (2008-2024)\n"]

lines += [section("Input Files"),
          f"Stock file      : {STOCK_FILE}\n",
          f"Market file     : {MARKET_FILE}\n",
          f"Treasury Bill   : {TBILL_FILE}\n",
          f"Raw stock shape : {raw_shapes['Stocks']}\n",
          f"Raw market shape: {raw_shapes['Market']}\n",
          f"Raw TB3MS shape : {raw_shapes['Treasury Bill']}\n"]

lines += [section("Data Cleaning Actions"),
          "1. Date columns normalised to month-start datetimes.\n",
          "2. Exact duplicate rows removed (counts reported below).\n",
          "3. All files sorted by [Ticker, Date] or [Date].\n",
          "4. Merged via left-join on monthly Date key.\n",
          "5. Risk_Free_Rate = (TB3MS / 100) / 12 (monthly decimal).\n",
          "6. Excess_Return and Excess_Market_Return computed.\n",
          "7. Lagged_Return = shift(1) within ticker.\n",
          "8. Volatility  = 12-month trailing std  (shift(1) applied first — no look-ahead).\n",
          "9. Momentum    = 12-month compounded ret (shift(1) applied first — no look-ahead).\n",
          "10. Sector dummy variables created via one-hot encoding.\n",
          "11. ABBV expected to have 144 rows (AbbVie spun off from Abbott Jan 2013).\n"]

lines += [section("Duplicate Rows Before Removal")]
for name, count in duplicate_counts.items():
    lines.append(f"{name}: {count}\n")

lines += [section("Missing Values Before Handling")]
for name, report_df in missing_before.items():
    lines.append(f"\n{name}\n")
    lines.append(report_df.to_string())
    lines.append("\n")

lines += [section("Merged Dataset Validation"),
          f"Number of stocks    : {n_stocks}\n",
          f"Total observations  : {len(master)}\n",
          f"Date range          : {master['Date'].min().date()} to {master['Date'].max().date()}\n",
          f"Unique sectors      : {', '.join(sorted(master['Sector'].dropna().unique()))}\n",
          f"ABBV rows           : {abbv_rows} (expected 144)\n",
          f"Sector dummy errors : {sector_sum_ok} rows with sum ≠ 1 (expected 0)\n"]

lines += [section("Missing Values in Final Master Dataset"),
          final_missing.to_string(), "\n"]

lines += [section("Summary Statistics"),
          summary_stats.to_string(), "\n"]

lines += [section("Output Files"),
          f"Master dataset      : {MASTER_OUTPUT}\n",
          f"Data quality report : {REPORT_OUTPUT}\n"]

REPORT_OUTPUT.write_text("".join(lines), encoding="utf-8")
print(f"\nMaster dataset saved  : {MASTER_OUTPUT}")
print(f"Quality report saved  : {REPORT_OUTPUT}")
print("\nMASTER DATASET SUCCESSFULLY CREATED")
