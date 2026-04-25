---
description: Update CV with new work experience and regenerate PDF
---

# CV Update Workflow

## Overview
This workflow updates your CV data and regenerates the PDF using Quarto and R targets pipeline.

## Prerequisites
- Python 3.x with venv
- R with renv
- Quarto installed

## Steps

### 1. Update CV Data (ODS Files)

**Option A: Manual Edit**
- Open ODS file in LibreOffice: `cv types/dar_cv_engineer_short.ods`
- Add/edit entries in Sheet 1 (entries)
- Update skills in Sheet 2 if needed
- Save file

**Option B: Python Script (Recommended)**

```bash
cd scripts

# First time setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add new work entry interactively
python cv_ods_manager.py --file "../cv types/dar_cv_engineer_short.ods" --add-work

# Or add directly via command line
python cv_ods_manager.py --file "../cv types/dar_cv_engineer_short.ods" \
  --title "Senior Data Engineer" \
  --company "TeamStation" \
  --start "2024" \
  --end "current" \
  --desc1 "Built data lake using AWS Glue, Step Functions, Lambda, DMS" \
  --desc2 "Integrated BI tool with AI-powered querying" \
  --desc3 "Established documentation process with Quarto and GitHub Actions"

# Inspect ODS structure
python cv_ods_manager.py --file "../cv types/dar_cv_engineer_short.ods" --inspect

# View current entries
python cv_ods_manager.py --file "../cv types/dar_cv_engineer_short.ods" --show-entries
```

### 2. Regenerate CV PDF

// turbo
```bash
# Restore R environment (first time or after updates)
Rscript -e "renv::restore()"
```

// turbo
```bash
# Run targets pipeline to regenerate CV
Rscript -e "targets::tar_make()"
```

This will:
- Read ODS file data
- Process work entries, education, skills
- Render `AutoCV.qmd` with Quarto
- Generate `danielamievarodriguez_cv.pdf`

### 3. Verify Output

```bash
# Check the generated PDF
xdg-open danielamievarodriguez_cv.pdf
```

### 4. Commit and Push (Optional)

```bash
git add "cv types/dar_cv_engineer_short.ods" danielamievarodriguez_cv.pdf
git commit -m "Update CV: Add [Company Name] experience"
git push origin main
```

GitHub Actions will automatically deploy to gh-pages.

## Bonus: GitHub Repository Database

Build a searchable database of your GitHub projects to quickly reference in CV updates:

```bash
cd scripts

# Fetch all your GitHub repos
python fetch_github_repos.py

# Query by technology
python query_repos.py --topics "aws,data-engineering,python"
python query_repos.py --language Python --min-stars 5

# Generate skills list for CV
python query_repos.py --cv-skills --categories "Cloud & AWS,Data Engineering,AI & ML"

# Search for specific projects
python query_repos.py --search "pipeline"
```

## File Structure

```
cv types/
  ├── dar_cv_engineer_short.ods      # Main CV data (currently used)
  ├── dar_cv_engineer.ods            # Full version
  └── dar_cv_ai_engineer_short.ods   # AI-focused version

scripts/
  ├── cv_ods_manager.py              # ODS file manager
  ├── fetch_github_repos.py          # GitHub repo scraper
  ├── query_repos.py                 # Query repo database
  └── requirements.txt               # Python dependencies

AutoCV.qmd                           # Quarto template
_targets.R                           # R pipeline definition
R/
  ├── ods_parse_information.R        # ODS parsing functions
  └── render_quarto_cv.R             # Quarto rendering functions

danielamievarodriguez_cv.pdf         # Generated CV output
```

## ODS File Structure

Each ODS file has 4 sheets:

1. **entries** - Work experience and education
   - Columns: section, title, location, institution, start, end, description_1-3, in_resume
   
2. **language_skills** - Language proficiency

3. **text_blocks** - General title and summary text

4. **contact_info** - Contact information

## Troubleshooting

**R packages missing:**
```bash
Rscript -e "renv::restore()"
```

**Python dependencies missing:**
```bash
cd scripts
pip install -r requirements.txt
```

**ODS file locked:**
Close LibreOffice and remove `.~lock.*` files

**Quarto not found:**
Install from https://quarto.org/docs/get-started/
