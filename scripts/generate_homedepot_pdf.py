#!/usr/bin/env python3
"""Generate Home Depot tailored CV PDF from CSV (AgileEngine format)."""

import csv
import sys
from pathlib import Path
from fpdf import FPDF


def clean_text(text):
    """Replace Unicode characters with ASCII equivalents."""
    if not text:
        return text
    # Replace em-dash, en-dash, and other unicode chars
    replacements = {
        '—': '-',  # em dash
        '–': '-',  # en dash
        ''': "'",  # smart quote
        ''': "'",  # smart quote
        '"': '"',  # smart quote
        '"': '"',  # smart quote
        '•': '-',  # bullet
        '~': '~',  # tilde
    }
    for unicode_char, ascii_char in replacements.items():
        text = text.replace(unicode_char, ascii_char)
    return text


def parse_csv(filepath):
    """Parse the tailored CV CSV file."""
    sections = {
        'text_blocks': [],
        'industry_positions': [],
        'skills': []
    }

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            section = row.get('section', '').strip()
            if section in sections:
                sections[section].append(row)

    return sections


class CVPDF(FPDF):
    """PDF formatter for AgileEngine-style CV."""

    def __init__(self):
        super().__init__(unit='pt', format='A4')
        self.set_auto_page_break(auto=True, margin=60)
        self.set_margins(left=60, top=60, right=60)

    def header(self):
        pass  # No default header

    def add_name_and_title(self, name, title):
        """Add name and title at top."""
        name = clean_text(name)
        title = clean_text(title)
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(0, 0, 0)
        self.cell(0, 30, name, ln=True, align='L')

        self.set_font("Helvetica", "", 14)
        self.set_text_color(80, 80, 80)
        self.cell(0, 20, title, ln=True, align='L')
        self.ln(10)

    def add_section_header(self, text):
        """Add a section header in bold uppercase."""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(0, 0, 0)
        self.cell(0, 20, text.upper(), ln=True, align='L')
        # Add subtle underline
        self.set_draw_color(0, 0, 0)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(8)

    def add_paragraph(self, text, indent=0):
        """Add justified paragraph text."""
        text = clean_text(text)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)

        # Handle line wrapping with safe margins
        usable_width = self.w - self.l_margin - self.r_margin - indent - 20
        self.set_x(self.l_margin + indent)
        self.multi_cell(usable_width, 14, text)
        self.ln(5)

    def add_skills(self, skills_rows):
        """Add skills section (flat text format)."""
        self.add_section_header("SKILLS")

        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)

        for row in skills_rows:
            skill_text = row.get('title', '').strip()
            skill_text = clean_text(skill_text)
            if skill_text:
                usable_width = self.w - self.l_margin - self.r_margin - 20
                self.multi_cell(usable_width, 14, skill_text)
                self.ln(4)

    def add_employment_history(self, positions):
        """Add employment history in AgileEngine format."""
        self.add_section_header("RELEVANT EMPLOYMENT HISTORY")

        for pos in positions:
            company = clean_text(pos.get('institution', '').strip())
            title = clean_text(pos.get('title', '').strip())
            location = clean_text(pos.get('location', '').strip())
            dates = f"{pos.get('start', '').strip()} - {pos.get('end', '').strip()}"

            # Company line: BAZ, Business Developer Engineer  2023 - Present
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(0, 0, 0)
            self.cell(0, 18, f"{company}, {title}    {dates}", ln=True, align='L')
            self.ln(2)

            # Get descriptions
            desc1 = clean_text(pos.get('description_1', '').strip())
            desc2 = clean_text(pos.get('description_2', '').strip())
            desc3 = clean_text(pos.get('description_3', '').strip())

            # Each bullet becomes a "project" paragraph in AgileEngine format
            self.set_font("Helvetica", "", 10)
            self.set_text_color(40, 40, 40)

            usable_width = self.w - self.l_margin - self.r_margin - 20

            # Project 1
            if desc1:
                self.multi_cell(usable_width, 14, desc1)
                self.ln(3)

            # Project 2
            if desc2:
                self.multi_cell(usable_width, 14, desc2)
                self.ln(3)

            # Project 3
            if desc3:
                self.multi_cell(usable_width, 14, desc3)
                self.ln(3)

            # Activities and responsibilities header
            self.set_font("Helvetica", "B", 10)
            self.cell(0, 16, "Key Achievements:", ln=True, align='L')
            self.ln(2)

            # Bullet points
            self.set_font("Helvetica", "", 10)
            for desc in [desc1, desc2, desc3]:
                if desc:
                    bullet_text = f"    - {desc[:80]}..." if len(desc) > 80 else f"    - {desc}"
                    self.multi_cell(usable_width, 14, bullet_text)
            self.ln(5)

            # Technologies line
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(80, 80, 80)

            # Build technologies from the content
            tech_keywords = []
            all_text = f"{desc1} {desc2} {desc3}"
            tech_map = [
                'Python', 'SQL', 'BigQuery', 'AWS', 'Glue', 'Lambda', 'Step Functions',
                'DMS', 'Kafka', 'Spark', 'DuckDB', 'GitHub Actions', 'Terraform',
                'Snowflake', 'Docker', 'Airflow', 'dbt', 'Quarto', 'Looker',
                'Power BI', 'Azure', 'GCP', 'Cloudera', 'CI/CD', 'ETL'
            ]
            for tech in tech_map:
                if tech.lower() in all_text.lower():
                    tech_keywords.append(tech)

            if tech_keywords:
                tech_line = f"Technologies: {', '.join(sorted(set(tech_keywords)))}"
                self.multi_cell(0, 14, tech_line)

            self.ln(15)


def generate_pdf(csv_path, output_path):
    """Generate PDF from CSV."""
    sections = parse_csv(csv_path)

    pdf = CVPDF()
    pdf.add_page()

    # Get name from file context
    name = "Daniel Amieva Rodriguez"

    # Get title from text blocks
    title = "Senior Data Engineer"
    summary = ""
    for tb in sections['text_blocks']:
        text = tb.get('title', '').strip()
        if text and 'years' in text.lower():
            summary = text
        elif text and not summary:
            # Check if it's the title row
            if any(word in text.lower() for word in ['engineer', 'developer', 'manager']):
                title = text

    # Add name and title
    pdf.add_name_and_title(name, title)

    # Add summary
    if summary:
        pdf.add_section_header("SUMMARY")
        pdf.add_paragraph(summary)

    # Add skills
    if sections['skills']:
        pdf.add_skills(sections['skills'])

    # Add employment history
    if sections['industry_positions']:
        pdf.add_employment_history(sections['industry_positions'])

    # Save PDF
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    csv_path = base_dir / "cv types" / "dar_cv_homedepot_tailored.csv"
    output_path = base_dir / "cv types" / "dar_cv_homedepot_tailored.pdf"

    generate_pdf(csv_path, output_path)
