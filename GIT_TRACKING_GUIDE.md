# Git Tracking Guide - What to Commit

## ✅ Files TO Track (Commit to Git)

### Source Files
- `*.qmd` - Quarto source documents
- `*.R` - R scripts and functions
- `*.py` - Python scripts
- `_quarto.yml` - Quarto project configuration
- `_targets.R` - Targets pipeline definition
- `*.css` - Stylesheets
- `*.md` - Documentation (README, guides)

### Data & Configuration
- `cv types/*.ods` - CV data files (source of truth)
- `renv.lock` - R package versions
- `.Rprofile` - R project settings
- `requirements.txt` - Python dependencies
- `.github/` - GitHub Actions workflows

### Assets
- `favicon.ico` - Website favicon
- Images in `assets/` or similar
- `_extensions/` - Quarto extensions

### Output (for GitHub Pages)
- `docs/` - **Keep tracked** (published to gh-pages)
- `danielamievarodriguez_cv.pdf` - Final CV PDF

---

## ❌ Files NOT to Track (Ignored)

### Quarto Build Artifacts
```
/.quarto/              # Quarto cache
*_cache/               # Render cache
*_files/               # Generated support files
index_files/           # HTML dependencies
site_libs/             # Site libraries
AutoCV_files/          # LaTeX support files
**/*.quarto_ipynb      # Jupyter notebook conversions
.luarc.json            # Lua configuration
```

### R/RStudio
```
.Rproj.user/           # RStudio user data
.Rhistory              # R command history
.RData                 # R workspace
.Ruserdata             # User data
.Renviron              # Environment variables
```

### Targets Pipeline
```
_targets/              # Targets cache (except _targets.R)
```

### LaTeX Intermediate Files
```
*.aux, *.log, *.out, *.toc
*.tex                  # Generated TeX (keep .qmd source)
*.fls, *.fdb_latexmk
*.synctex.gz
*.bbl, *.blg
```

### Python
```
__pycache__/           # Python bytecode
*.pyc, *.pyo, *.pyd
.venv/, venv/          # Virtual environments
*.egg-info/            # Package metadata
```

### Database Files
```
*.db                   # SQLite databases
*.sqlite, *.sqlite3
github_repos.db        # Generated from API
```

### IDE & System
```
.vscode/               # VS Code settings
.idea/                 # JetBrains IDEs
.DS_Store              # macOS
*.swp, *.swo           # Vim
.positai               # AI tools
```

### Secrets
```
.secrets/              # Secret files
*.key, *.pem           # Private keys
.env                   # Environment variables
```

---

## Current Setup

### Output Directory
```yaml
# _quarto.yml
project:
  output-dir: docs     # Published to GitHub Pages
```

**Why `docs/` is tracked:**
- GitHub Pages serves from `docs/` folder
- Contains final rendered HTML
- Needs to be in repo for deployment

### Intermediate Files (Ignored)
- `index_files/` - HTML dependencies for index.qmd
- `site_libs/` - Shared site libraries
- `AutoCV_files/` - LaTeX support files

---

## Best Practices

### 1. Clean Build Artifacts
```bash
# Remove all generated files
rm -rf *_files/ *_cache/ .quarto/

# Rebuild from scratch
quarto render
```

### 2. Check What's Tracked
```bash
# See what Git is tracking
git ls-files

# See what's ignored
git status --ignored
```

### 3. Remove Already-Tracked Files
```bash
# If files were tracked before adding to .gitignore
git rm --cached index_files/ -r
git rm --cached site_libs/ -r
git rm --cached AutoCV_files/ -r
git rm --cached _targets/ -r
git rm --cached *.log
git rm --cached *.tex

git commit -m "Remove build artifacts from tracking"
```

### 4. Verify Ignore Patterns
```bash
# Test if file would be ignored
git check-ignore -v index_files/libs/bootstrap/bootstrap.min.css

# List all ignored files
git status --ignored
```

---

## GitHub Pages Deployment

### What Gets Published
```
docs/
├── index.html                          # ✅ Main page
├── portfolio_animations_complete.html  # ✅ Animations
├── bubble_animation_demo.html          # ✅ Demos
├── danielamievarodriguez_cv.pdf        # ✅ CV PDF
├── styles.css                          # ✅ Styles
├── portfolio-styles.css                # ✅ Styles
└── site_libs/                          # ✅ Required libraries
```

### What Stays Local
```
index_files/          # ❌ Intermediate build files
AutoCV_files/         # ❌ LaTeX support
_targets/             # ❌ Pipeline cache
.quarto/              # ❌ Quarto cache
*.log, *.tex          # ❌ LaTeX intermediates
```

---

## Workflow

### Daily Development
```bash
# 1. Edit source files
vim index.qmd

# 2. Render (generates docs/)
quarto render

# 3. Commit only source + output
git add index.qmd docs/
git commit -m "Update homepage"

# 4. Push (triggers GitHub Pages)
git push
```

### Clean Rebuild
```bash
# Remove all build artifacts
rm -rf *_files/ *_cache/ .quarto/ _targets/

# Rebuild everything
targets::tar_make()    # R pipeline
quarto render          # Website

# Commit
git add docs/
git commit -m "Rebuild site"
```

---

## Summary

**Track**: Source files, configuration, docs/ output  
**Ignore**: Build artifacts, caches, intermediate files, secrets  

The updated `.gitignore` follows Quarto best practices and keeps your repo clean! 🎯
