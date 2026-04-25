#!/usr/bin/env python3
"""
CV ODS Manager
Read and update ODS CV files using Python.

Usage:
    python cv_ods_manager.py --file "cv types/dar_cv_engineer_short.ods" --inspect
    python cv_ods_manager.py --file "cv types/dar_cv_engineer_short.ods" --add-work
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from ezodf import opendoc, Sheet


class CVODSManager:
    """Manage ODS CV files."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"ODS file not found: {file_path}")
        
        self.doc = opendoc(str(self.file_path))
        self.sheets = {sheet.name: sheet for sheet in self.doc.sheets}
    
    def inspect(self):
        """Inspect ODS file structure."""
        print(f"\n{'='*60}")
        print(f"ODS File: {self.file_path.name}")
        print(f"{'='*60}\n")
        
        for i, (name, sheet) in enumerate(self.sheets.items(), 1):
            print(f"Sheet {i}: {name}")
            print(f"  Dimensions: {sheet.nrows()} rows × {sheet.ncols()} columns")
            
            # Show first few rows
            if sheet.nrows() > 0:
                print(f"  First row (headers):")
                headers = [sheet[0, j].value for j in range(min(sheet.ncols(), 10))]
                for j, header in enumerate(headers):
                    if header:
                        print(f"    Col {j}: {header}")
            print()
    
    def read_sheet_to_df(self, sheet_name: str, skip_rows: int = 1) -> pd.DataFrame:
        """Read a sheet into a pandas DataFrame."""
        if sheet_name not in self.sheets:
            available = ", ".join(self.sheets.keys())
            raise ValueError(f"Sheet '{sheet_name}' not found. Available: {available}")
        
        sheet = self.sheets[sheet_name]
        
        # Get headers
        headers = [sheet[skip_rows, j].value for j in range(sheet.ncols())]
        
        # Get data
        data = []
        for i in range(skip_rows + 1, sheet.nrows()):
            row = [sheet[i, j].value for j in range(sheet.ncols())]
            if any(cell is not None for cell in row):  # Skip empty rows
                data.append(row)
        
        df = pd.DataFrame(data, columns=headers)
        return df
    
    def show_entries(self):
        """Show all work entries."""
        try:
            # Try common sheet names
            for sheet_name in ['Sheet1', 'entries', 'Entries', 'Work']:
                if sheet_name in self.sheets:
                    df = self.read_sheet_to_df(sheet_name)
                    print(f"\n{'='*60}")
                    print(f"Entries from '{sheet_name}':")
                    print(f"{'='*60}\n")
                    print(df.to_string())
                    return df
            
            # If no match, show first sheet
            first_sheet = list(self.sheets.keys())[0]
            df = self.read_sheet_to_df(first_sheet)
            print(f"\n{'='*60}")
            print(f"Entries from '{first_sheet}':")
            print(f"{'='*60}\n")
            print(df.to_string())
            return df
            
        except Exception as e:
            print(f"Error reading entries: {e}")
            return None
    
    def add_work_entry(self, entry_data: Dict):
        """Add a new work entry to the ODS file."""
        # Get the first sheet (entries)
        sheet_name = list(self.sheets.keys())[0]
        sheet = self.sheets[sheet_name]
        
        # Find the next empty row
        next_row = sheet.nrows()
        
        # Append a new row
        sheet.append_rows(1)
        
        # Actual column structure from ODS:
        # Col 0: cv category (section)
        # Col 1: title of entry
        # Col 2: location
        # Col 3: primary institution
        # Col 4: Start date of entry (year)
        # Col 5: End year of entry
        # Col 6: description_1
        # Col 7: description_2 (if exists)
        # Col 8: description_3 (if exists)
        # Col 9: include?
        
        columns = {
            'section': 0,
            'title': 1,
            'location': 2,
            'institution': 3,
            'start': 4,
            'end': 5,
            'description_1': 6,
            'description_2': 7,
            'description_3': 8,
            'in_resume': 9
        }
        
        # Add the entry
        sheet[next_row, columns['section']].set_value(entry_data.get('section', 'industry_positions'))
        sheet[next_row, columns['title']].set_value(entry_data.get('title', ''))
        sheet[next_row, columns['location']].set_value(entry_data.get('location', ''))
        sheet[next_row, columns['institution']].set_value(entry_data.get('institution', ''))
        sheet[next_row, columns['start']].set_value(entry_data.get('start', ''))
        sheet[next_row, columns['end']].set_value(entry_data.get('end', ''))
        sheet[next_row, columns['description_1']].set_value(entry_data.get('description_1', ''))
        sheet[next_row, columns['description_2']].set_value(entry_data.get('description_2', ''))
        sheet[next_row, columns['description_3']].set_value(entry_data.get('description_3', ''))
        sheet[next_row, columns['in_resume']].set_value(entry_data.get('in_resume', 1))
        
        # Save the document
        self.doc.save()
        print(f"\n✓ Added work entry: {entry_data.get('title')} at {entry_data.get('institution')}")
        print(f"  Row {next_row + 1} in sheet '{sheet_name}'")
    
    def export_to_csv(self, output_dir: str = "exports"):
        """Export all sheets to CSV files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for sheet_name in self.sheets.keys():
            try:
                df = self.read_sheet_to_df(sheet_name)
                csv_file = output_path / f"{self.file_path.stem}_{sheet_name}.csv"
                df.to_csv(csv_file, index=False)
                print(f"✓ Exported {sheet_name} → {csv_file}")
            except Exception as e:
                print(f"✗ Failed to export {sheet_name}: {e}")


def interactive_add_work():
    """Interactive prompt to add work entry."""
    print("\n" + "="*60)
    print("Add New Work Entry")
    print("="*60 + "\n")
    
    entry = {}
    
    entry['section'] = 'industry_positions'
    entry['title'] = input("Job Title/Role: ").strip()
    entry['institution'] = input("Company/Institution: ").strip()
    entry['start'] = input("Start Date (e.g., 'May 2024'): ").strip()
    entry['end'] = input("End Date (or 'current'): ").strip()
    entry['description_1'] = input("Description 1: ").strip()
    entry['description_2'] = input("Description 2: ").strip()
    entry['description_3'] = input("Description 3: ").strip()
    entry['in_resume'] = 1
    
    print("\n" + "="*60)
    print("Review Entry:")
    print("="*60)
    for key, value in entry.items():
        if key != 'section':
            print(f"  {key}: {value}")
    
    confirm = input("\nAdd this entry? (y/n): ").strip().lower()
    
    return entry if confirm == 'y' else None


def main():
    parser = argparse.ArgumentParser(description="Manage CV ODS files")
    parser.add_argument("--file", required=True, help="Path to ODS file")
    parser.add_argument("--inspect", action="store_true", help="Inspect file structure")
    parser.add_argument("--show-entries", action="store_true", help="Show all entries")
    parser.add_argument("--add-work", action="store_true", help="Add work entry (interactive)")
    parser.add_argument("--export-csv", action="store_true", help="Export to CSV")
    
    # Direct entry addition
    parser.add_argument("--title", help="Job title")
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--start", help="Start date")
    parser.add_argument("--end", help="End date")
    parser.add_argument("--desc1", help="Description 1")
    parser.add_argument("--desc2", help="Description 2")
    parser.add_argument("--desc3", help="Description 3")
    
    args = parser.parse_args()
    
    try:
        manager = CVODSManager(args.file)
        
        if args.inspect:
            manager.inspect()
        
        if args.show_entries:
            manager.show_entries()
        
        if args.export_csv:
            manager.export_to_csv()
        
        if args.add_work:
            entry = interactive_add_work()
            if entry:
                manager.add_work_entry(entry)
            else:
                print("Entry cancelled.")
        
        # Direct entry addition
        if args.title and args.company:
            entry = {
                'section': 'industry_positions',
                'title': args.title,
                'institution': args.company,
                'start': args.start or '',
                'end': args.end or 'current',
                'description_1': args.desc1 or '',
                'description_2': args.desc2 or '',
                'description_3': args.desc3 or '',
                'in_resume': 1
            }
            manager.add_work_entry(entry)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
