# Verification Log — Final Version
## MSc Dissertation — Empirical Analysis
**Date:** 2026-06-13  
**Pipeline:** `Build_Master_Dataset_final.py` → `Analysis_Pipeline_final.py`  
**Engine:** sklearn (GridSearchCV) + statsmodels (OLS) + scipy (DM test)  
**Test period:** 2019-01-01 to 2024-12-31 (N = 1,440 observations)

---

## 1. Data Build Verification

| Check | Expected | Status |
|-------|----------|--------|
| Total panel rows | 4,020 | Verified at run time (printed to console) |
| ABBV rows (AbbVie spin-off Jan 2013) | 144 | Verified at run time |
| Other 19 tickers rows | 204 each | Verified at run time |
| Max \|Return − pct_change(Close)\| | < 1e-10 | 5.37e-16 ✅ |
| Max \|Market_Return − pct_change\| | < 1e-10 | 1.94e-16 ✅ |
| Sector dummy sum per row = 1 | 0 errors | 0 rows with sum ≠ 1 ✅ |
| Training obs (complete cases) | 2,580 | ✅ |
| Test obs (complete cases) | 1,440 | ✅ |

**Look-ahead prevention:** All lagged and rolling features call `shift(1)` on the return series before applying rolling windows. At prediction time t, only returns through t−1 enter Volatility and Momentum.

---

## 2. CAPM Results

| Metric | Value | Benchmark | Diff | Status |
|--------|-------|-----------|------|--------|
| RMSE | 0.06403 | 0.06403 | 0.000003 | ✅ |
| MAE | 0.04878 | 0.04878 | < 0.00001 | ✅ |
| R² | 0.33435 | 0.33435 | < 0.00001 | ✅ |
| N | 1,440 | 1,440 | 0 | ✅ |

**Notable finding:** Jensen's alpha = 0.0055 (p < 0.001) — statistically significant positive intercept over the 2008–2018 training window. Market beta = 1.056 (expected ≈ 1.0 for large-cap S&P 500 stocks).

---

## 3. Extended Model Results

| Metric | Value | Benchmark | Diff | Status |
|--------|-------|-----------|------|--------|
| RMSE | 0.06364 | 0.06364 | 0.000005 | ✅ |
| MAE | 0.04857 | 0.04857 | < 0.00001 | ✅ |
| R² | 0.34240 | 0.34240 | < 0.00001 | ✅ |
| N | 1,440 | 1,440 | 0 | ✅ |

**Significant predictors (training):** Market Return (p < 0.001 ***), Volatility (p < 0.001 ***).  
**Non-significant:** Lagged Return (p = 0.346), Momentum (p = 0.691).

---

## 4. Random Forest Results

**Hyperparameter selection:** Full GridSearchCV over 24 combinations × 5 TimeSeriesSplit folds using `neg_root_mean_squared_error`. Best params from canonical sklearn run:

```
{'max_depth': 5, 'max_features': None, 'min_samples_leaf': 5, 'n_estimators': 500}
```

| Metric | Value | Benchmark | Diff | Status |
|--------|-------|-----------|------|--------|
| RMSE | 0.06260 | 0.06260 | 0.000001 | ✅ |
| MAE | 0.04789 | 0.04789 | < 0.00001 | ✅ |
| R² | 0.36385 | 0.36385 | < 0.00001 | ✅ |
| N | 1,440 | 1,440 | 0 | ✅ |

**RF improvement over CAPM:** RMSE falls by 0.00143 (2.20%)  
**RF improvement over Extended Model:** RMSE falls by 0.00105 (1.64%)

---

## 5. Feature Importances (sklearn canonical)

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | Market_Return | 0.5687 |
| 2 | Momentum | 0.2261 |
| 3 | Volatility | 0.0748 |
| 4 | Lagged_Return | 0.0670 |
| 5 | Financials | 0.0327 |
| 6 | Risk_Free_Rate | 0.0189 |
| 7 | Technology | 0.0066 |
| 8 | Consumer | 0.0049 |
| 9 | Healthcare | 0.0004 |

---

## 6. Statistical Tests

DM-style paired t-tests on squared-error loss differentials:

| Comparison | t-stat | p-value | Significance |
|-----------|--------|---------|--------------|
| CAPM vs Extended Model | 2.4508 | 0.0144 | ** (5%) |
| CAPM vs Random Forest | 2.1623 | 0.0308 | ** (5%) |
| Extended Model vs Random Forest | 1.6617 | 0.0968 | * (10% only) |

---

## 7. Sector Analysis

| Sector | Best Model | Best RMSE |
|--------|-----------|----------|
| Consumer | Random Forest | 0.04532 |
| Financials | **CAPM** | 0.06232 |
| Healthcare | Random Forest | 0.06241 |
| Technology | Random Forest | 0.07262 |

**Sector nuance:** CAPM is the best model in Financials — where systemic market-wide credit-cycle risk dominates, and the single-factor linear specification is well-suited. RF excels in the three other sectors.

---

## 8. Output Files Checklist

| File | Location | Status |
|------|----------|--------|
| Build_Master_Dataset_final.py | final/ | ✅ |
| Analysis_Pipeline_final.py | final/ | ✅ |
| run_all.py | final/ | ✅ |
| requirements.txt | final/ | ✅ |
| README.md | final/ | ✅ |
| outputs/Results_Summary.xlsx | final/outputs/ | ✅ 7 sheets |
| outputs/Results_Report.docx | final/outputs/ | ✅ |
| outputs/Verification_Log.md | Generated at run time | — |
| Figures/Actual_vs_Predicted_CAPM.png | final/Figures/ | ✅ 300 dpi |
| Figures/Actual_vs_Predicted_Extended_Model.png | final/Figures/ | ✅ 300 dpi |
| Figures/Actual_vs_Predicted_Random_Forest.png | final/Figures/ | ✅ 300 dpi |
| Figures/RMSE_Comparison.png | final/Figures/ | ✅ 300 dpi |
| Figures/MAE_Comparison.png | final/Figures/ | ✅ 300 dpi |
| Figures/Sector_Performance_Comparison.png | final/Figures/ | ✅ 300 dpi |
| Figures/Feature_Importance.png | final/Figures/ | ✅ 300 dpi |
| notebooks/Dissertation_Analysis.ipynb | final/notebooks/ | ✅ |
| GitHub_Setup_Instructions.md | final/ | ✅ |

---

## 9. Summary

All benchmark metrics matched within tolerance (< 0.001 RMSE).  
No look-ahead bias detected.  
Sector dummy integrity: 0 rows with sum ≠ 1.  
Statistical significance correctly applied: ** at 5% (CAPM vs Ext, CAPM vs RF), * at 10% only (Ext vs RF).  
Feature importances are canonical sklearn MDI values from full GridSearchCV run.

**Overall result: PASS ✅**
