# CV Spacing Implementation Documentation

## Problem Identified

The `classic-cv-pdf` Quarto extension template **ignores standard Quarto YAML options** for spacing and geometry. Settings like `linestretch`, `geometry`, and `include-in-header` in the YAML frontmatter are not applied because the template has hardcoded values.

### Original Template Issues
- **Hardcoded geometry**: `\geometry{top=1.25cm, bottom=-.1cm, left=1.5cm, right=1.5cm}`
  - Note: **negative bottom margin** of -0.1cm!
- **No line spacing control**: No `\linespread` or `\baselineskip` modifications
- **No paragraph spacing**: Default LaTeX spacing (very tight)
- **No widow/orphan control**: Sections could break awkwardly across pages

## Solution Implemented

### Direct Template Modification
Modified `_extensions/schochastics/classic-cv/template.tex` directly (backup saved as `template.tex.backup`):

**Line 62 - Geometry:**
```latex
% OLD: \geometry{top=1.25cm, bottom=-.1cm, left=1.5cm, right=1.5cm}
% NEW:
\geometry{top=20mm, bottom=30mm, left=20mm, right=20mm}
```

**Lines 198-202 - Spacing & Penalties (added after line 197):**
```latex
\linespread{1.2}\selectfont
\setlength{\parskip}{6pt plus 2pt minus 1pt}
\widowpenalty=10000
\clubpenalty=10000
\raggedbottom
```

### Spacing Values Chosen

Based on industry research for resume/CV readability:

| Setting | Value | Rationale |
|---------|-------|-----------|
| **Line spacing** | 1.2 (120%) | Industry standard for CVs is 1.0-1.15 for body text; 1.2 provides breathing room while staying compact |
| **Paragraph spacing** | 6pt | Adds visual separation between paragraphs without excessive whitespace |
| **Top margin** | 20mm | Standard professional document margin |
| **Bottom margin** | 30mm | Larger than top to prevent text crowding at page bottom |
| **Left/Right margins** | 20mm | Standard professional document margins |
| **Widow penalty** | 10000 | Prevents single lines at top of page (orphans) |
| **Club penalty** | 10000 | Prevents single lines at bottom of page (widows) |
| **Raggedbottom** | Enabled | Allows pages to end naturally instead of forcing content to fill |

### Research Sources

**Resume Spacing Best Practices (TealHQ):**
- Body text: 1.0 to 1.15 line spacing for scanability
- Optimal readability: 120% to 150% (1.2 to 1.5) of font size
- Paragraph spacing: 6-10pt between paragraphs
- Margins: 1 inch (25.4mm) standard, minimum 0.7 inches (18mm)

**LaTeX Spacing (Overleaf):**
- `\linespread{1.2}` = 120% line spacing
- `\parskip` package with `skip=6pt plus 2pt minus 1pt` for flexible paragraph spacing
- `\widowpenalty` and `\clubpenalty` set to 10000 to prevent orphans/widows

## Quality Verification

Created automated verification script: `scripts/verify_cv_pdf.sh`

**Checks performed:**
1. ✓ PDF exists and is valid
2. ✓ Page count (warns if > 3 pages)
3. ✓ LaTeX source has correct spacing settings
4. ✓ Content sections are present (TeamStation, Rackspace, Certifications)
5. ✓ File size is reasonable (50-500KB)

**Usage:**
```bash
./scripts/verify_cv_pdf.sh
# Or specify custom paths:
./scripts/verify_cv_pdf.sh "path/to/cv.pdf" "path/to/source.tex"
```

## Results

**Before:**
- 2 pages (too cramped)
- Negative bottom margin causing text to crowd page edge
- No paragraph spacing
- Default tight line spacing
- Sections could break awkwardly

**After:**
- 3 pages (readable, professional)
- Proper 30mm bottom margin
- 6pt paragraph spacing for visual breathing room
- 1.2 (120%) line spacing for readability
- Widow/orphan penalties prevent awkward breaks

**Verification Output:**
```
=== CV PDF Quality Verification ===

✓ Checking PDF exists...
✓ Checking PDF metadata...
  - Pages: 3
✓ Checking LaTeX source for spacing settings...
  ✓ Bottom margin: 30mm (correct)
  ✓ Line spacing: 1.2 (120% - optimized for CV)
  ✓ Paragraph spacing: 6pt (optimized for CV)
  ✓ Widow/orphan penalties: enabled
✓ Checking PDF content...
  ✓ TeamStation section found
  ✓ Rackspace section found
  ✓ Certifications section found
✓ Checking PDF file size...
  - Size: 126KB

=== Verification Complete ===
```

## Files Modified

1. **`_extensions/schochastics/classic-cv/template.tex`**
   - Line 62: Updated geometry
   - Lines 198-202: Added spacing and penalty settings
   - Backup: `template.tex.backup`

2. **`homedepot_cv.qmd`**
   - Added `keep-tex: true` to preserve LaTeX source for verification

3. **`scripts/verify_cv_pdf.sh`** (NEW)
   - Automated quality verification script

## Future Adjustments

If spacing needs fine-tuning:

**To increase spacing (if CV feels too cramped):**
```latex
\linespread{1.25}\selectfont          % 125% line spacing
\setlength{\parskip}{8pt plus 2pt minus 1pt}  % 8pt paragraph spacing
```

**To decrease spacing (if CV is too long):**
```latex
\linespread{1.15}\selectfont          % 115% line spacing
\setlength{\parskip}{4pt plus 1pt minus 1pt}  % 4pt paragraph spacing
```

**To adjust margins:**
```latex
\geometry{top=15mm, bottom=25mm, left=18mm, right=18mm}
```

## Workflow Integration

**Standard CV update workflow:**
1. Edit `homedepot_cv.qmd` content
2. Run `quarto render homedepot_cv.qmd`
3. Run `./scripts/verify_cv_pdf.sh` to verify changes
4. Copy to final location: `cp docs/danielamievarodriguez_cv.pdf "cv types/dar_cv_homedepot_tailored_quarto.pdf"`

**Automated (one command):**
```bash
quarto render homedepot_cv.qmd && \
cp docs/danielamievarodriguez_cv.pdf "cv types/dar_cv_homedepot_tailored_quarto.pdf" && \
./scripts/verify_cv_pdf.sh
```
