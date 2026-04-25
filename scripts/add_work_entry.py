#!/usr/bin/env python3
"""
Add work entry to CV - Generic flexible script

Usage:
    # Interactive mode
    python add_work_entry.py
    
    # Command-line mode
    python add_work_entry.py \
        --title "Senior Data Engineer" \
        --company "TeamStation" \
        --location "Remote" \
        --start "2024" \
        --end "current" \
        --desc1 "Built data lake from ground up..." \
        --desc2 "Integrated BI tool..." \
        --desc3 "Established documentation process..."
    
    # Specify CV file
    python add_work_entry.py --cv-file "../cv types/dar_cv_ai_engineer_short.ods"
"""

import argparse
import sys
from pathlib import Path
from cv_ods_manager import CVODSManager


def add_work_record_entry(
    cv_file: str,
    title: str,
    company: str,
    location: str = "",
    start: str = "",
    end: str = "current",
    desc1: str = "",
    desc2: str = "",
    desc3: str = "",
    section: str = "industry_positions",
    in_resume: int = 1
):
    """
    Add a work entry record to CV ODS file.
    
    Args:
        cv_file: Path to ODS CV file
        title: Job title/role
        company: Company/institution name
        location: Work location (default: "")
        start: Start date (default: "")
        end: End date or "current" (default: "current")
        desc1: First description/achievement (default: "")
        desc2: Second description/achievement (default: "")
        desc3: Third description/achievement (default: "")
        section: CV section (default: "industry_positions")
        in_resume: Include in resume 1=yes, 0=no (default: 1)
    """
    entry_data = {
        'section': section,
        'title': title,
        'location': location,
        'institution': company,
        'start': start,
        'end': end,
        'description_1': desc1,
        'description_2': desc2,
        'description_3': desc3,
        'in_resume': in_resume
    }
    
    print(f"\nAdding work entry to {cv_file}...")
    print(f"  Title: {title}")
    print(f"  Company: {company}")
    print(f"  Period: {start} - {end}")
    
    manager = CVODSManager(cv_file)
    manager.add_work_entry(entry_data)
    
    print("\n✓ Entry added successfully!")
    print("\nNext steps:")
    print("  1. Open the ODS file to verify the entry")
    print("  2. Run: Rscript -e 'targets::tar_make()' to regenerate CV")
    print("  3. Check danielamievarodriguez_cv.pdf")
    
    return True


def interactive_mode(cv_file: str):
    """Interactive mode to collect work entry data."""
    print("\n" + "="*60)
    print("Add Work Entry - Interactive Mode")
    print("="*60 + "\n")
    
    title = input("Job Title/Role: ").strip()
    if not title:
        print("Error: Title is required")
        return False
    
    company = input("Company/Institution: ").strip()
    if not company:
        print("Error: Company is required")
        return False
    
    location = input("Location (optional): ").strip()
    start = input("Start Date (e.g., '2024' or 'May 2024'): ").strip()
    end = input("End Date (or 'current'): ").strip() or "current"
    
    print("\nDescriptions/Achievements (press Enter to skip):")
    desc1 = input("  1. ").strip()
    desc2 = input("  2. ").strip()
    desc3 = input("  3. ").strip()
    
    # Confirm
    print("\n" + "="*60)
    print("Review Entry:")
    print("="*60)
    print(f"Title: {title}")
    print(f"Company: {company}")
    print(f"Location: {location}")
    print(f"Period: {start} - {end}")
    if desc1:
        print(f"Desc 1: {desc1[:80]}...")
    if desc2:
        print(f"Desc 2: {desc2[:80]}...")
    if desc3:
        print(f"Desc 3: {desc3[:80]}...")
    
    confirm = input("\nAdd this entry? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Cancelled.")
        return False
    
    return add_work_record_entry(
        cv_file=cv_file,
        title=title,
        company=company,
        location=location,
        start=start,
        end=end,
        desc1=desc1,
        desc2=desc2,
        desc3=desc3
    )


def main():
    parser = argparse.ArgumentParser(
        description="Add work entry to CV ODS file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python add_work_entry.py
  
  # Command-line mode
  python add_work_entry.py --title "Senior Data Engineer" --company "TeamStation"
  
  # Full example
  python add_work_entry.py \\
    --title "Senior Data Engineer" \\
    --company "TeamStation" \\
    --location "Remote" \\
    --start "2024" \\
    --end "current" \\
    --desc1 "Built data lake using AWS Glue, Step Functions, Lambda" \\
    --desc2 "Integrated BI tool with AI capabilities" \\
    --desc3 "Established CI/CD with GitHub Actions"
        """
    )
    
    parser.add_argument(
        "--cv-file",
        default="../cv types/dar_cv_engineer_short.ods",
        help="Path to CV ODS file (default: dar_cv_engineer_short.ods)"
    )
    parser.add_argument("--title", help="Job title/role")
    parser.add_argument("--company", help="Company/institution name")
    parser.add_argument("--location", default="", help="Work location")
    parser.add_argument("--start", default="", help="Start date")
    parser.add_argument("--end", default="current", help="End date or 'current'")
    parser.add_argument("--desc1", default="", help="First description/achievement")
    parser.add_argument("--desc2", default="", help="Second description/achievement")
    parser.add_argument("--desc3", default="", help="Third description/achievement")
    parser.add_argument(
        "--section",
        default="industry_positions",
        help="CV section (default: industry_positions)"
    )
    parser.add_argument(
        "--in-resume",
        type=int,
        default=1,
        choices=[0, 1],
        help="Include in resume: 1=yes, 0=no (default: 1)"
    )
    
    args = parser.parse_args()
    
    # Check if CV file exists
    cv_path = Path(args.cv_file)
    if not cv_path.exists():
        print(f"Error: CV file not found: {args.cv_file}")
        sys.exit(1)
    
    # Interactive mode if no title/company provided
    if not args.title or not args.company:
        success = interactive_mode(args.cv_file)
    else:
        # Command-line mode
        success = add_work_record_entry(
            cv_file=args.cv_file,
            title=args.title,
            company=args.company,
            location=args.location,
            start=args.start,
            end=args.end,
            desc1=args.desc1,
            desc2=args.desc2,
            desc3=args.desc3,
            section=args.section,
            in_resume=args.in_resume
        )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
