# CV Generation Workflow - Updated & Modernized

## Overview

Yes, you **still need to run the R targets workflow** to generate the PDF CV. The workflow reads data from ODS files and renders a PDF using Quarto.

## Code Updates Made

### ✅ Modernized R Code

**Updated to modern R patterns:**
- ✅ Native pipe `|>` (already in use)
- ✅ Removed unnecessary `return()` statements
- ✅ Simplified function bodies
- ✅ Used `case_when()` with `.default` instead of multiple filters
- ✅ Combined `mutate()` calls
- ✅ Removed redundant intermediate variables
- ✅ Cleaner `rowwise()` → `ungroup()` pattern

**Fixed Issues:**
- ✅ Updated `AutoCV.qmd` - Changed "Rackspace" to "TeamStation AI"
- ✅ Cleaned up commented code
- ✅ Improved code readability

## How the ODS Parsing Works

### 1. **ODS File Structure** (`cv types/dar_cv_engineer_short.ods`)

The ODS file has **4 sheets**:

| Sheet # | Name | Content | Columns |
|---------|------|---------|---------|
| 1 | Entries | Work & Education | `section`, `title`, `institution`, `start`, `end`, `description_1`, `description_2`, `description_3`, `in_resume` |
| 2 | Skills | Technical skills | `skill` |
| 3 | Text | Title & Summary | `location`, `text` |
| 4 | Contact | Contact info | Contact details |

### 2. **Data Flow Pipeline**

```
ODS File
  ↓
build_cv_components() - Reads all 4 sheets
  ↓
fetch_cv_entries() - Filters entries where in_resume == 1
  ↓
process_entries_to_match_cv_events() - Formats entries
  ↓
fetch_work_entries() / fetch_education_entries() - Splits by type
  ↓
format_cv_entries() - Converts to LaTeX \cvevent commands
  ↓
render_quarto_cv() - Renders PDF with Quarto
```

### 3. **Key Functions**

#### `build_cv_components(cv_type_file_path)`
```r
# Reads all 4 sheets from ODS file
list(
  entries = read_cv_ods(cv_type_file_path, 1, skip = 1),
  skills = read_cv_ods(cv_type_file_path, 2, skip = 1),
  text = read_cv_ods(cv_type_file_path, 3, skip = 1),
  contact = read_cv_ods(cv_type_file_path, 4, skip = 1)
)
```

#### `fetch_cv_entries(cv_data)`
```r
# Filters only entries marked for inclusion (in_resume == 1)
# Adds entry_type column (work/education)
cv_data |> 
  pluck("entries") |>
  filter(in_resume == 1) |>
  mutate(entry_type = case_when(...))
```

#### `process_entries_to_match_cv_events(unified_entries_df)`
```r
# Combines description columns into a list
# Creates "when" field (start - end)
# Renames columns to match CV template
unified_entries_df |> 
  mutate(
    when = paste0(start, " - ", end),
    across(description_1:description_3, ~coalesce(., "EMPTY"))
  ) |> 
  rowwise() |> 
  mutate(tasks = list(c(description_1, description_2, description_3)))
```

#### `format_cv_entries(cv_entries)`
```r
# Converts to LaTeX \cvevent{when}{what}{where}{tasks}
# Removes "EMPTY" placeholders
# Wraps each task in {}
cv_entries |> 
  pull(tasks) |> 
  map(~ .x[!grepl("EMPTY", .x)]) |> 
  map_chr(~ paste0("{", .x, "}", collapse = ","))
```

## Running the Workflow

### Option 1: Full Pipeline (Recommended)
```r
# In R console
targets::tar_make()
```

This will:
1. Read ODS file
2. Process all entries
3. Format for LaTeX
4. Render PDF to `danielamievarodriguez_cv.pdf`

### Option 2: Individual Steps (Debugging)
```r
# Load targets
library(targets)

# Run specific target
tar_make(cv_components)
tar_make(work_entries)
tar_make(render_quarto_pdf_cv)

# View intermediate results
tar_read(cv_components)
tar_read(work_entries)
```

### Option 3: Python Script (Update ODS)
```bash
cd scripts
python cv_ods_manager.py --file "../cv types/dar_cv_engineer_short.ods" --add-work
```

Then run R pipeline:
```r
targets::tar_make()
```

## File Locations

```
Curriculum-Vitae/
├── cv types/
│   └── dar_cv_engineer_short.ods    # Source data (4 sheets)
├── R/
│   ├── ods_parse_information.R      # ODS reading & processing
│   └── render_quarto_cv.R           # PDF rendering
├── _targets.R                        # Pipeline definition
├── AutoCV.qmd                        # Quarto template
└── danielamievarodriguez_cv.pdf     # Output PDF
```

## ODS Sheet Details

### Sheet 1: Entries
```
section | title | institution | start | end | description_1 | description_2 | description_3 | in_resume
industry_positions | Senior Data Engineer | TeamStation AI | May 2025 | current | Built data lake... | CI/CD pipelines... | Infrastructure... | 1
```

### Sheet 2: Skills
```
skill
Python
AWS
Docker
CI/CD
...
```

### Sheet 3: Text
```
location | text
general title | Senior Data Engineer & DevOps Specialist
summary | Experienced data engineer with expertise in...
```

### Sheet 4: Contact
```
Contact information fields
```

## Critical Parameters

### In `_targets.R`:
```r
cv_type <- "cv types/dar_cv_engineer_short.ods"  # Source file
contact_info <- "linkedin.jobs.frequent526@passmail.net"
```

### In `AutoCV.qmd`:
```yaml
cvmeta:
  - title: Current Role
    left: "Senior Data Engineer @ TeamStation AI"  # ✅ Updated
```

## Troubleshooting

### Issue: "in_resume column not found"
**Solution**: Ensure Sheet 1 has `in_resume` column with values 0 or 1

### Issue: "Empty descriptions"
**Solution**: The code handles this - uses "EMPTY" placeholder and filters it out

### Issue: "PDF not rendering"
**Solution**: 
```r
# Check intermediate targets
tar_read(formatted_work_entries)
tar_read(formatted_education_entries)

# Re-run specific target
tar_make(render_quarto_pdf_cv, callr_function = NULL)  # Shows errors
```

### Issue: "Skills not showing"
**Solution**: Check Sheet 2 has column named `skill` (lowercase)

## Dependencies

### R Packages (from `_targets.R`):
- `targets` - Pipeline orchestration
- `dplyr` - Data manipulation
- `tidyr` - Data tidying
- `readODS` - ODS file reading
- `glue` - String interpolation
- `quarto` - PDF rendering
- `purrr` - Functional programming
- `janitor` - Column name cleaning

### System:
- Quarto CLI
- LaTeX (for PDF rendering)
- R 4.0+

## Workflow Summary

**To update CV:**
1. Edit `cv types/dar_cv_engineer_short.ods` (or use Python script)
2. Run `targets::tar_make()` in R
3. PDF generated at `danielamievarodriguez_cv.pdf`
4. Push to GitHub → GitHub Actions deploys to gh-pages

**The R pipeline is essential** - it's the only way to convert ODS → PDF with proper formatting.
