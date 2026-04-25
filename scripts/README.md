# GitHub Repository Database Scripts

Python scripts to fetch, store, and query your GitHub repositories for CV updates.

## Setup

```bash
cd scripts
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Add Work Entry to CV

Add new work experience to your CV ODS file:

```bash
# Interactive mode (prompts for all fields)
python add_work_entry.py

# Command-line mode
python add_work_entry.py \
  --title "Senior Data Engineer" \
  --company "TeamStation" \
  --location "Remote" \
  --start "2024" \
  --end "current" \
  --desc1 "Built data lake using AWS Glue, Step Functions, Lambda, DMS" \
  --desc2 "Integrated BI tool with AI-powered querying and visualization" \
  --desc3 "Established documentation process with Quarto and GitHub Actions"

# Specify different CV file
python add_work_entry.py --cv-file "../cv types/dar_cv_ai_engineer_short.ods"

# Add but exclude from resume (draft mode)
python add_work_entry.py --title "..." --company "..." --in-resume 0
```

### 2. Fetch Repositories

Fetch all your GitHub repositories and create a local SQLite database:

```bash
python fetch_github_repos.py
```

This will:
- Fetch all repositories from `dar4datascience` GitHub account
- Create `github_repos.db` SQLite database
- Extract skills from languages and topics
- Generate `github_repos.json` export
- Print a summary

**Options:**
```bash
python fetch_github_repos.py --username YOUR_USERNAME
python fetch_github_repos.py --output custom_db.db
python fetch_github_repos.py --no-json  # Skip JSON export
```

### 3. Query Repositories

Query the database to find relevant projects for your CV:

```bash
# Find Python projects with 5+ stars
python query_repos.py --language Python --min-stars 5

# Find repos with specific topics
python query_repos.py --topics "aws,data-engineering,python"

# Search by keyword
python query_repos.py --search "pipeline"

# Show top 20 skills
python query_repos.py --top-skills 20

# Show skills in a category
python query_repos.py --category "Cloud & AWS"

# Generate CV skills list
python query_repos.py --cv-skills
python query_repos.py --cv-skills --categories "Programming Languages,Cloud & AWS,Data Engineering"
```

## Database Schema

### `repositories` table
- name, full_name, description, url
- language, topics (JSON array)
- stars, forks
- created_at, updated_at
- is_fork, is_archived

### `skills` table
- skill_name, category
- repo_count (how many repos use this skill)
- last_updated

## Skill Categories

- Programming Languages
- Data Engineering
- Cloud & AWS
- AI & ML
- Backend & Web
- Databases
- Big Data
- DevOps
- Data Visualization
- Other

## Integration with CV Workflow

1. Run `fetch_github_repos.py` to update your project database
2. Use `query_repos.py` to find relevant projects for specific job profiles
3. Update your ODS CV files with selected projects and skills
4. Run `targets::tar_make()` in R to regenerate your CV
