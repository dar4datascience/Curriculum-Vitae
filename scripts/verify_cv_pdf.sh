#!/bin/bash
# CV PDF Quality Verification Script
# Checks that spacing and formatting changes are properly applied

set -e

CV_PDF="${1:-cv types/dar_cv_detailed.pdf}"
TEX_FILE="${2:-detailed_cv.tex}"

echo "=== CV PDF Quality Verification ==="
echo ""

# Check 1: PDF exists and is valid
echo "✓ Checking PDF exists..."
if [ ! -f "$CV_PDF" ]; then
    echo "❌ ERROR: PDF file not found: $CV_PDF"
    exit 1
fi

# Check 2: PDF info and page count
echo "✓ Checking PDF metadata..."
PDF_INFO=$(pdfinfo "$CV_PDF" 2>/dev/null || echo "pdfinfo not available")
if [ "$PDF_INFO" != "pdfinfo not available" ]; then
    PAGES=$(echo "$PDF_INFO" | grep "Pages:" | awk '{print $2}')
    echo "  - Pages: $PAGES"
    if [ "$PAGES" -gt 3 ]; then
        echo "  ⚠️  WARNING: CV is $PAGES pages (should be 2-3 pages max)"
    fi
else
    echo "  ℹ️  pdfinfo not available, skipping metadata check"
fi

# Check 3: Verify LaTeX source has correct spacing settings
echo "✓ Checking LaTeX source for spacing settings..."
if [ -f "$TEX_FILE" ]; then
    # Check geometry
    GEOMETRY=$(grep "\\\\geometry{" "$TEX_FILE" | head -1)
    if echo "$GEOMETRY" | grep -q "bottom=30mm"; then
        echo "  ✓ Bottom margin: 30mm (correct)"
    else
        echo "  ❌ Bottom margin not set to 30mm"
        echo "     Found: $GEOMETRY"
    fi
    
    # Check linespread
    if grep -q "\\\\linespread{1.2}" "$TEX_FILE"; then
        echo "  ✓ Line spacing: 1.2 (120% - optimized for CV)"
    elif grep -q "\\\\linespread{1.3}" "$TEX_FILE"; then
        echo "  ✓ Line spacing: 1.3 (130%)"
    else
        echo "  ❌ Line spacing not configured"
    fi
    
    # Check parskip
    if grep -q "\\\\setlength{\\\\parskip}{6pt" "$TEX_FILE"; then
        echo "  ✓ Paragraph spacing: 6pt (optimized for CV)"
    elif grep -q "\\\\setlength{\\\\parskip}{8pt" "$TEX_FILE"; then
        echo "  ✓ Paragraph spacing: 8pt"
    else
        echo "  ❌ Paragraph spacing not configured"
    fi
    
    # Check widow/orphan penalties
    if grep -q "\\\\widowpenalty=10000" "$TEX_FILE"; then
        echo "  ✓ Widow/orphan penalties: enabled"
    else
        echo "  ⚠️  Widow/orphan penalties not set"
    fi
else
    echo "  ⚠️  LaTeX source file not found: $TEX_FILE"
    echo "     Run with keep-tex: true to generate .tex file"
fi

# Check 4: Verify content is present
echo "✓ Checking PDF content..."
if command -v pdftotext &> /dev/null; then
    PDF_TEXT=$(pdftotext "$CV_PDF" - 2>/dev/null || echo "")
    
    # Check for key sections
    if echo "$PDF_TEXT" | grep -q "TeamStation"; then
        echo "  ✓ TeamStation section found"
    else
        echo "  ❌ TeamStation section missing"
    fi
    
    if echo "$PDF_TEXT" | grep -q "Rackspace"; then
        echo "  ✓ Rackspace section found"
    else
        echo "  ❌ Rackspace section missing"
    fi
    
    if echo "$PDF_TEXT" | grep -q "Certifications"; then
        echo "  ✓ Certifications section found"
    else
        echo "  ❌ Certifications section missing"
    fi
else
    echo "  ℹ️  pdftotext not available, skipping content check"
fi

# Check 5: File size (should be reasonable)
echo "✓ Checking PDF file size..."
FILE_SIZE=$(stat -f%z "$CV_PDF" 2>/dev/null || stat -c%s "$CV_PDF" 2>/dev/null || echo "0")
FILE_SIZE_KB=$((FILE_SIZE / 1024))
echo "  - Size: ${FILE_SIZE_KB}KB"
if [ "$FILE_SIZE_KB" -lt 50 ]; then
    echo "  ⚠️  WARNING: PDF seems unusually small (< 50KB)"
elif [ "$FILE_SIZE_KB" -gt 500 ]; then
    echo "  ⚠️  WARNING: PDF seems unusually large (> 500KB)"
fi

echo ""
echo "=== Verification Complete ==="
echo ""
echo "To view the PDF, run:"
echo "  xdg-open '$CV_PDF'  # Linux"
echo "  open '$CV_PDF'      # macOS"
