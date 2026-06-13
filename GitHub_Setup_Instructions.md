# GitHub + Google Colab Setup Instructions
## Professional Showcase for MSc Dissertation

Follow these steps in order. Each step takes 2–5 minutes.

---

## Step 1: Create a GitHub Account (skip if you have one)

1. Go to [https://github.com](https://github.com)
2. Click **Sign up**
3. Enter your email, choose a password, and pick a username
   - Suggested username: `kiribalan-finance` or similar professional name
4. Verify your email address
5. On the welcome screen, click **Skip personalisation** (or fill it in)

---

## Step 2: Create a New Repository

1. After logging in, click the **+** icon (top-right) → **New repository**
2. Fill in the form:
   - **Repository name:** `sp500-return-prediction` (or similar)
   - **Description:** `MSc dissertation empirical analysis: CAPM vs Extended OLS vs Random Forest for S&P 500 monthly return prediction (2008–2024)`
   - **Visibility:** ✅ **Public** (so your professor can view it without an account)
   - ☐ Do NOT tick "Add a README file" (we already have one)
3. Click **Create repository**
4. You will see a page with setup instructions — **keep this page open**

---

## Step 3: Install Git on Your Computer

### Mac (you likely already have it)
Open Terminal and type:
```bash
git --version
```
If you see a version number, Git is installed. Otherwise:
```bash
xcode-select --install
```

### Windows
Download and install from [https://git-scm.com/download/win](https://git-scm.com/download/win)  
Accept all defaults during installation.

---

## Step 4: Configure Git (first-time only)

> **Before running these commands, confirm Git is installed** (Step 3). On Mac, open **Terminal** (search Spotlight for "Terminal"). On Windows, open **Git Bash** (installed in Step 3) — do NOT use Command Prompt or PowerShell, as they may not recognise `git`.

Type each line separately and press **Enter** after each one. Replace the placeholder text with your actual name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Use the same email you registered on GitHub.

To verify it worked, run:
```bash
git config --global user.name
git config --global user.email
```
You should see your name and email printed back.

---

## Step 5: Prepare Your Project Folder

Your `final/` folder should contain:
```
final/
├── Build_Master_Dataset_final.py
├── Analysis_Pipeline_final.py
├── run_all.py
├── requirements.txt
├── README.md
├── Verification_Log_final.md
├── GitHub_Setup_Instructions.md
├── Figures/          (7 PNG files)
├── notebooks/
│   └── Dissertation_Analysis.ipynb
└── outputs/          (CSVs, xlsx, docx)
```

**Important:** Do NOT include your raw data files (`SP500_20_Companies_Monthly.csv`, etc.) in the repository if they are proprietary. If you can share them, place them in an `inputs/` subfolder.

---

## Step 6: Create a `.gitignore` File

On Mac, Finder blocks creating files that start with a dot. Use Terminal instead — copy and paste the entire block below in one go (including the last line `EOF`), then press **Enter**:

```bash
cd /Users/kiribalankannan/Documents/Codex/2026-06-11/files-mentioned-by-the-user-company/final
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
.mpl_cache/
*.so
*.c

# Data files (remove these lines if you want to share your data)
inputs/
outputs/Master_Dataset.csv
outputs/Model_Predictions.csv

# OS files
.DS_Store
Thumbs.db
EOF
```

To confirm it was created, run `ls -a` — you should see `.gitignore` in the list.

---

## Step 7: Push Your Files to GitHub

Open Terminal, navigate to the folder **containing** your `final/` folder, then run:

```bash
# Navigate to the final/ folder
cd /Users/kiribalankannan/Documents/Codex/2026-06-11/files-mentioned-by-the-user-company/final

# Initialise git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: MSc dissertation empirical analysis — CAPM vs Extended OLS vs Random Forest"

# Link to your GitHub repository
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

When prompted, enter your GitHub username and password.  
**Note:** If you have two-factor authentication enabled, use a Personal Access Token as your password (see Step 8 below).

---

## Step 8: Create a Personal Access Token (if needed)

GitHub no longer accepts plain passwords for command-line pushes. To create a token:

1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Name: `dissertation-push`
4. Expiration: 90 days
5. Scopes: tick ✅ **repo**
6. Click **Generate token**
7. **Copy the token immediately** — GitHub only shows it once
8. Use this token instead of your password when running `git push`

---

## Step 9: Update the Colab Badge URL in README.md

Open `README.md` and replace both instances of `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME`:

**Current (placeholder):**
```
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/blob/main/final/notebooks/Dissertation_Analysis.ipynb)
```

**Replace with your actual values, e.g.:**
```
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kiribalan-finance/sp500-return-prediction/blob/main/final/notebooks/Dissertation_Analysis.ipynb)
```

Also update the notebook cell 1 to replace the repo URL:
```python
REPO = 'https://github.com/kiribalan-finance/sp500-return-prediction.git'
```

Then push the update:
```bash
git add README.md notebooks/Dissertation_Analysis.ipynb
git commit -m "Update Colab badge URL and notebook repo reference"
git push
```

---

## Step 10: Verify Everything Works

1. Go to `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`
2. You should see all your files, with the README displayed at the bottom
3. The Colab badge should appear as a clickable orange button
4. Click the badge — it should open your notebook in Google Colab

---

## Step 11: Test the Colab Run (Optional but Impressive)

1. In Colab, run cell 1 (setup) — it clones your repo and installs requirements
2. Run cells 2–11 to show results loading from CSVs
3. Section 8 shows the pre-run canonical results; skip the GridSearchCV cell for speed
4. All charts and tables should display inline

---

## Step 12: Share with Your Professor

Send your professor:

```
Dear Professor [Name],

Please find my MSc dissertation empirical analysis at the link below:

GitHub Repository:
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME

Interactive Notebook (runs in browser, no installation needed):
https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO_NAME/blob/main/final/notebooks/Dissertation_Analysis.ipynb

The repository contains:
- Full reproducible Python pipeline (CAPM, Extended OLS, Random Forest)
- Professional Excel workbook (7 sheets) and Word report
- 7 publication-quality figures (300 dpi)
- Verification log confirming all benchmark metrics

All code is original, documented, and runs end-to-end from raw data.

Best regards,
kiribalan
```

---

## Common Troubleshooting

| Problem | Solution |
|---------|----------|
| `git: command not found` | Install Git (Step 3) |
| `Authentication failed` | Use Personal Access Token, not password (Step 8) |
| `error: remote origin already exists` | Run `git remote remove origin` then re-add |
| Colab badge gives 404 | Check the URL — must match exact repo path and branch (`main`) |
| Colab can't find data files | Either include `inputs/` in the repo or upload manually in Colab |
| Push rejected (non-fast-forward) | Run `git pull --rebase origin main` first |

---

## Quick Reference: Common Git Commands

```bash
# Check status of your files
git status

# Add all changes
git add .

# Commit with a message
git commit -m "Your message here"

# Push to GitHub
git push

# Pull latest from GitHub
git pull

# See commit history
git log --oneline
```

---

*Last updated: 2026-06-13*
