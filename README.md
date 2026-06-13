# Does the Inclusion of Additional Financial Information Improve Stock Return Prediction Accuracy?
### Evidence from CAPM, Extended Financial Models, and Random Forest Models on S&P 500 Stocks (2008–2024)
**MSc International Finance Dissertation**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/blob/main/final/notebooks/Dissertation_Analysis.ipynb)

> **Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME` in the badge URL above once you have created your GitHub repository.**

---

## Overview

This repository contains the complete empirical analysis for an MSc International Finance dissertation examining whether richer financial information improves monthly stock return prediction accuracy for a panel of 20 S&P 500 companies over 2008–2024.

Three models are compared:
- **CAPM** — single-factor market beta benchmark
- **Extended OLS** — adds lagged returns, rolling volatility, and 12-month momentum
- **Random Forest** — non-linear machine learning model with TimeSeriesSplit cross-validation

All results are fully reproducible from the raw input data.

---

## Key Results

| Model | RMSE | MAE | R² | vs CAPM |
|-------|------|-----|-----|---------|
| CAPM | 0.06403 | 0.04878 | 0.334 | — |
| Extended OLS | 0.06364 | 0.04857 | 0.342 | −0.61% |
| **Random Forest** | **0.06260** | **0.04789** | **0.364** | **−2.20%** |

- RF vs CAPM: statistically significant at 5% (p = 0.031, DM test)
- Extended vs CAPM: statistically significant at 5% (p = 0.014, DM test)
- RF vs Extended: significant at 10% only (p = 0.097)

**Top RF features:** Market Return (56.9%), Momentum (22.6%), Volatility (7.5%)

---

## Repository Structure

```
final/
├── Build_Master_Dataset_final.py    # Step 1: build the master panel dataset
├── Analysis_Pipeline_final.py       # Step 2: run all three models + outputs
├── run_all.py                       # Single-command orchestrator
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── Verification_Log_final.md        # Benchmark checks and data integrity
├── GitHub_Setup_Instructions.md     # Step-by-step GitHub + Colab guide
│
├── inputs/                          # ← Place your raw data files here
│   ├── SP500_20_Companies_Monthly.csv
│   ├── SP500_Market_Returns.csv
│   └── TB3MS.csv
│
├── outputs/                         # Generated automatically
│   ├── Master_Dataset.csv
│   ├── Model_Predictions.csv
│   ├── Model_Comparison.csv
│   ├── OLS_Coefficients.csv
│   ├── RF_Best_Params.csv
│   ├── Random_Forest_Feature_Importance.csv
│   ├── Sector_Analysis.csv
│   ├── Statistical_Tests.csv
│   ├── Results_Summary.xlsx         # 7-sheet professional Excel workbook
│   ├── Results_Report.docx          # Full dissertation-style Word report
│   ├── Verification_Log.md          # Run-time benchmark checks
│   └── Figures/
│       ├── Actual_vs_Predicted_CAPM.png
│       ├── Actual_vs_Predicted_Extended_Model.png
│       ├── Actual_vs_Predicted_Random_Forest.png
│       ├── RMSE_Comparison.png
│       ├── MAE_Comparison.png
│       ├── Sector_Performance_Comparison.png
│       └── Feature_Importance.png
│
└── notebooks/
    └── Dissertation_Analysis.ipynb  # Jupyter notebook (Colab-ready)
```

---

## How to Run

### Option A — Local (recommended for full reproduction)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME/final

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place input data files in the inputs/ folder
#    SP500_20_Companies_Monthly.csv
#    SP500_Market_Returns.csv
#    TB3MS.csv

# 4. Run the full pipeline
python run_all.py

# 5. (Optional) Open the Jupyter notebook
jupyter notebook notebooks/Dissertation_Analysis.ipynb
```

### Option B — Google Colab (zero setup, browser-based)

Click the **Open in Colab** badge at the top of this README.
Follow the instructions in the first notebook cell to clone the repo and install requirements.

> **Note:** The Random Forest GridSearchCV step takes ~10–20 minutes. The notebook contains pre-run canonical results if you want to review outputs without waiting.

---

## Technical Design Choices

| Choice | Rationale |
|--------|-----------|
| sklearn `GridSearchCV` + `TimeSeriesSplit` | Canonical, reproducible hyperparameter selection without look-ahead |
| `statsmodels` OLS | Exact p-values, confidence intervals, and diagnostic statistics |
| `scipy.stats.t.cdf` for DM test | Exact t-distribution p-values (not asymptotic normal approximation) |
| `shift(1)` before rolling windows | Eliminates all look-ahead bias in Volatility and Momentum features |
| 2008–2018 train / 2019–2024 test | Strict chronological split; no random shuffling |
| `random_state=42` throughout | Full reproducibility |
| Relative paths via `Path(__file__).parent` | Scripts run correctly from any folder without modification |

---

## Data Sources

| File | Source |
|------|--------|
| `SP500_20_Companies_Monthly.csv` | Monthly adjusted closing prices for 20 S&P 500 stocks |
| `SP500_Market_Returns.csv` | S&P 500 index monthly returns |
| `TB3MS.csv` | 3-Month US Treasury Bill rate (FRED, Federal Reserve Bank of St. Louis) |

**Note:** ABBV (AbbVie) data begins January 2013 (spin-off from Abbott Laboratories), giving 144 monthly observations versus 204 for the other 19 tickers. Total panel: 4,020 rows.

---

## Requirements

- Python 3.10+
- See `requirements.txt` for full package list

Key packages: `numpy`, `pandas`, `scikit-learn`, `statsmodels`, `scipy`, `matplotlib`, `seaborn`, `openpyxl`, `python-docx`

---

## Author

MSc International Finance Dissertation  
*kiribalan*  
2026
