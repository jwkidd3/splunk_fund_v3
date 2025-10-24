#!/usr/bin/env python3
"""
Splunk Fundamentals Course Validation Script

This script validates the course structure, content, and ensures:
1. All required files exist
2. Lab files are properly formatted
3. Data files are present
4. No timing references remain in labs or presentations
5. Presentation concepts are covered before corresponding labs
6. Links and references are valid
7. No incomplete content (TODO markers)
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

class CourseValidator:
    def __init__(self, course_root: str):
        self.course_root = Path(course_root)
        self.errors = []
        self.warnings = []
        self.lab_order = [
            "Lab1_Data_Loading.md",
            "Lab2_Basic_Searching.md",
            "Lab3_Using_Fields_in_Searches.md",
            "Lab4_Basic_Commands.md",
            "lab5_transforming_commands.md",
            "lab6_reports_dashboards.md",
            "lab7_pivot_datasets.md",
            "lab8_lookups.md",
            "lab9_alerts.md"
        ]
        self.required_data_files = [
            "access_30DAY.log",
            "linux_s_30DAY.log",
            "db_audit_30DAY.csv",
            "products.csv",
            "generate_course_data.py"
        ]

    def add_error(self, message: str):
        """Add an error to the validation results"""
        self.errors.append(f"❌ ERROR: {message}")

    def add_warning(self, message: str):
        """Add a warning to the validation results"""
        self.warnings.append(f"⚠️  WARNING: {message}")

    def validate_structure(self) -> bool:
        """Validate that all required directories and files exist"""
        print("\n📁 Validating Course Structure...")

        # Check main directories
        required_dirs = ["labs", "presentations", "scripts", "labs/data"]
        for dir_name in required_dirs:
            dir_path = self.course_root / dir_name
            if not dir_path.exists():
                self.add_error(f"Required directory missing: {dir_name}")
            else:
                print(f"  ✓ Found directory: {dir_name}")

        # Check lab files
        labs_dir = self.course_root / "labs"
        for lab_file in self.lab_order:
            lab_path = labs_dir / lab_file
            if not lab_path.exists():
                self.add_error(f"Required lab file missing: {lab_file}")
            else:
                print(f"  ✓ Found lab: {lab_file}")

        # Check data files
        data_dir = self.course_root / "labs" / "data"
        for data_file in self.required_data_files:
            data_path = data_dir / data_file
            if not data_path.exists():
                self.add_error(f"Required data file missing: {data_file}")
            else:
                print(f"  ✓ Found data file: {data_file}")

        # Check presentation files
        pres_dir = self.course_root / "presentations"
        for pres_file in ["content1.html", "content2.html"]:
            pres_path = pres_dir / pres_file
            if not pres_path.exists():
                self.add_error(f"Required presentation file missing: {pres_file}")
            else:
                print(f"  ✓ Found presentation: {pres_file}")

        return len(self.errors) == 0

    def validate_no_timing_references(self) -> bool:
        """Check that no timing references remain in labs or presentations"""
        print("\n⏱️  Validating No Timing References...")

        # Patterns to search for timing references
        timing_patterns = [
            r'Duration:\s*\d+\s*(?:min|hour|minute)',
            r'\d+-day\s+(?:intensive\s+)?course',
            r'\*Day\s+\d+\s*-\s*Lab',
            r'Lab\s+\d+\s+of\s+\d+',
        ]

        # Check labs
        labs_dir = self.course_root / "labs"
        for lab_file in self.lab_order:
            lab_path = labs_dir / lab_file
            if lab_path.exists():
                content = lab_path.read_text()
                for pattern in timing_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        self.add_error(f"Timing reference found in {lab_file}: {matches[0]}")

        # Check presentations
        pres_dir = self.course_root / "presentations"
        for pres_file in ["content1.html", "content2.html"]:
            pres_path = pres_dir / pres_file
            if pres_path.exists():
                content = pres_path.read_text()
                for pattern in timing_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        self.add_error(f"Timing reference found in {pres_file}: {matches[0]}")

        if len([e for e in self.errors if "Timing reference" in e]) == 0:
            print("  ✓ No timing references found")
            return True
        return False

    def validate_lab_formatting(self) -> bool:
        """Validate that lab files are properly formatted"""
        print("\n📝 Validating Lab Formatting...")

        labs_dir = self.course_root / "labs"
        for lab_file in self.lab_order:
            lab_path = labs_dir / lab_file
            if not lab_path.exists():
                continue

            content = lab_path.read_text()

            # Check for proper heading structure
            if not content.startswith("# Lab"):
                self.add_warning(f"{lab_file}: Should start with '# Lab' heading")

            # Check for required sections
            required_sections = ["Learning Objectives", "Prerequisites"]
            for section in required_sections:
                if section not in content:
                    self.add_warning(f"{lab_file}: Missing '{section}' section")

            # Check for TODO markers
            if "TODO" in content or "TBD" in content:
                self.add_warning(f"{lab_file}: Contains TODO/TBD markers")

            print(f"  ✓ Validated {lab_file}")

        return True

    def validate_presentation_coverage(self) -> bool:
        """Validate that presentation concepts are covered before labs"""
        print("\n🎓 Validating Presentation Coverage Before Labs...")

        # Define lab-to-concept mappings
        lab_concepts = {
            "Lab1_Data_Loading.md": ["data ingestion", "source type", "index"],
            "Lab2_Basic_Searching.md": ["search", "timeline", "Boolean", "search history", "jobs"],
            "Lab3_Using_Fields_in_Searches.md": ["fields", "sidebar"],
            "Lab4_Basic_Commands.md": ["commands", "table", "sort", "dedup"],
            "lab5_transforming_commands.md": ["stats", "chart", "transforming"],
            "lab6_reports_dashboards.md": ["reports", "dashboards", "visualizations"],
            "lab7_pivot_datasets.md": ["pivot", "datasets"],
            "lab8_lookups.md": ["lookups", "enrichment"],
            "lab9_alerts.md": ["alerts", "scheduled", "actions"]
        }

        # Read all presentation content
        pres_dir = self.course_root / "presentations"
        content1 = (pres_dir / "content1.html").read_text().lower() if (pres_dir / "content1.html").exists() else ""
        content2 = (pres_dir / "content2.html").read_text().lower() if (pres_dir / "content2.html").exists() else ""
        all_presentation_content = content1 + content2

        # Check each lab's concepts
        for lab_file, concepts in lab_concepts.items():
            missing_concepts = []
            for concept in concepts:
                if concept.lower() not in all_presentation_content:
                    missing_concepts.append(concept)

            if missing_concepts:
                self.add_warning(f"{lab_file}: Concepts not found in presentations: {', '.join(missing_concepts)}")
            else:
                print(f"  ✓ All concepts covered for {lab_file}")

        return True

    def validate_links(self) -> bool:
        """Validate internal links in markdown files"""
        print("\n🔗 Validating Internal Links...")

        labs_dir = self.course_root / "labs"
        for lab_file in self.lab_order:
            lab_path = labs_dir / lab_file
            if not lab_path.exists():
                continue

            content = lab_path.read_text()

            # Find markdown links [text](path)
            link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
            links = re.findall(link_pattern, content)

            for link_text, link_path in links:
                # Skip external links
                if link_path.startswith(('http://', 'https://', '#')):
                    continue

                # Check if internal file exists
                target_path = labs_dir / link_path
                if not target_path.exists():
                    self.add_warning(f"{lab_file}: Broken link to '{link_path}'")

        print("  ✓ Link validation complete")
        return True

    def generate_report(self) -> bool:
        """Generate and print validation report"""
        print("\n" + "="*70)
        print("📊 VALIDATION REPORT")
        print("="*70)

        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("\n✅ Course validation passed with no issues!")
            return True

        if len(self.errors) > 0:
            print(f"\n❌ Found {len(self.errors)} error(s):")
            for error in self.errors:
                print(f"  {error}")

        if len(self.warnings) > 0:
            print(f"\n⚠️  Found {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"  {warning}")

        print("\n" + "="*70)

        return len(self.errors) == 0

    def run_all_validations(self) -> bool:
        """Run all validation checks"""
        print("🚀 Starting Splunk Fundamentals Course Validation")
        print(f"📂 Course Root: {self.course_root.absolute()}\n")

        self.validate_structure()
        self.validate_no_timing_references()
        self.validate_lab_formatting()
        self.validate_presentation_coverage()
        self.validate_links()

        return self.generate_report()

def main():
    """Main entry point"""
    # Determine course root (current directory)
    course_root = os.getcwd()

    # Check if we're in the right directory
    if not os.path.exists(os.path.join(course_root, "labs")):
        print("❌ ERROR: Cannot find 'labs' directory. Please run this script from the course root directory.")
        sys.exit(1)

    # Create validator and run checks
    validator = CourseValidator(course_root)
    success = validator.run_all_validations()

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
