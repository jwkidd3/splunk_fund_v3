#!/usr/bin/env python3
"""
SPL-Data Alignment Validation Script

This script validates that all SPL queries in labs reference only fields
and data that actually exist in the provided data files.
"""

import os
import re
import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple

class SPLDataValidator:
    def __init__(self, course_root: str):
        self.course_root = Path(course_root)
        self.errors = []
        self.warnings = []

        # Define expected fields for each sourcetype based on actual data
        self.sourcetype_fields = {
            "access_combined": {
                # Fields Splunk auto-extracts from Common Log Format
                "clientip", "method", "uri", "uri_path", "uri_query", "file",
                "status", "bytes", "referer", "useragent", "req_time",
                # URL parameters that appear in the data
                "action", "categoryId", "productId", "JSESSIONID",
                # Splunk default fields
                "_time", "host", "source", "sourcetype", "_raw", "_indextime"
            },
            "access_combined_wcookie": {
                # Same fields as access_combined (wcookie variant extracts same fields)
                "clientip", "method", "uri", "uri_path", "uri_query", "file",
                "status", "bytes", "referer", "useragent", "req_time",
                # URL parameters that appear in the data
                "action", "categoryId", "productId", "JSESSIONID",
                # Splunk default fields
                "_time", "host", "source", "sourcetype", "_raw", "_indextime"
            },
            "linux_secure": {
                # Fields from Linux secure logs (sshd)
                "user", "src_ip", "port", "process", "action", "info",
                # Splunk default fields
                "_time", "host", "source", "sourcetype", "_raw"
            },
            "db_audit": {
                # CSV headers from db_audit_30DAY.csv
                "Time", "Type", "Command", "Duration",
                # Splunk default fields
                "_time", "host", "source", "sourcetype", "_raw"
            }
        }

        # Lookup table fields
        self.lookup_fields = {
            "products.csv": {
                "productId", "product_name", "categoryId", "price", "Code"
            }
        }

        # Valid index names
        self.valid_indexes = {"main", "web", "security", "database", "_audit", "_internal"}

        # Map common field names to their actual names
        self.field_aliases = {
            "clientip": ["clientip", "client_ip"],
            "useragent": ["useragent", "user_agent"],
        }

    def add_error(self, message: str):
        """Add an error to validation results"""
        self.errors.append(f"❌ ERROR: {message}")

    def add_warning(self, message: str):
        """Add a warning to validation results"""
        self.warnings.append(f"⚠️  WARNING: {message}")

    def extract_spl_from_labs(self) -> Dict[str, List[Tuple[int, str]]]:
        """Extract all SPL queries from lab files"""
        print("\n🔍 Extracting SPL queries from labs...")

        spl_queries = {}
        labs_dir = self.course_root / "labs"

        for lab_file in labs_dir.glob("*.md"):
            queries = []
            content = lab_file.read_text()

            # Find code blocks (between ``` or single backticks)
            # Pattern 1: Triple backtick code blocks
            code_blocks = re.findall(r'```(?:spl|splunk)?\n(.*?)```', content, re.DOTALL)

            # Pattern 2: Inline code that looks like SPL (starts with index= or |)
            inline_spl = re.findall(r'`([^`]*(?:index=|^\|)[^`]*)`', content, re.MULTILINE)

            all_code = code_blocks + inline_spl

            for code in all_code:
                # Clean up the code
                code = code.strip()
                if not code:
                    continue

                # Remove comment lines before validation
                code_lines = code.split('\n')
                code_lines = [line for line in code_lines if not line.strip().startswith('#')]
                code = '\n'.join(code_lines).strip()

                # Skip if it's just a comment or example text or empty after removing comments
                if not code or 'Example:' in code or 'Note:' in code:
                    continue

                # Check if it's actually SPL (contains Splunk keywords)
                spl_indicators = ['index=', 'sourcetype=', '| stats', '| table', '| sort',
                                 '| top', '| rare', '| eval', '| search', '| fields',
                                 '| rename', '| dedup', '| lookup', '| inputlookup']

                if any(indicator in code for indicator in spl_indicators):
                    # Get line number (approximate)
                    lines_before = content[:content.find(code)].count('\n')
                    queries.append((lines_before, code))

            if queries:
                spl_queries[lab_file.name] = queries
                print(f"  ✓ Found {len(queries)} SPL queries in {lab_file.name}")

        return spl_queries

    def extract_fields_from_spl(self, spl: str) -> Set[str]:
        """Extract field names referenced in SPL query"""
        fields = set()

        # Pattern for field=value
        field_value_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*[=<>!]'
        matches = re.findall(field_value_pattern, spl)
        fields.update(matches)

        # Pattern for fields in commands: | stats ... by field
        by_pattern = r'by\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)'
        by_matches = re.findall(by_pattern, spl)
        for match in by_matches:
            fields.update(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', match))

        # Pattern for function arguments: func(field)
        func_pattern = r'\b(?:count|sum|avg|min|max|dc|list|values|distinct_count)\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)'
        func_matches = re.findall(func_pattern, spl)
        fields.update(func_matches)

        # Pattern for | table field1 field2
        table_pattern = r'\|\s*table\s+([a-zA-Z_][a-zA-Z0-9_,\s]*)'
        table_matches = re.findall(table_pattern, spl)
        for match in table_matches:
            fields.update(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', match))

        # Pattern for | fields field1 field2
        fields_pattern = r'\|\s*fields\s+[-+]?\s*([a-zA-Z_][a-zA-Z0-9_,\s]*)'
        fields_matches = re.findall(fields_pattern, spl)
        for match in fields_matches:
            fields.update(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', match))

        # Pattern for | sort field
        sort_pattern = r'\|\s*sort\s+[-+]?\s*([a-zA-Z_][a-zA-Z0-9_,\s]*)'
        sort_matches = re.findall(sort_pattern, spl)
        for match in sort_matches:
            fields.update(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', match))

        # Pattern for | rename oldfield as newfield
        rename_pattern = r'\|\s*rename\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+as'
        rename_matches = re.findall(rename_pattern, spl)
        fields.update(rename_matches)

        # Remove common SPL keywords that aren't fields
        keywords = {'index', 'sourcetype', 'earliest', 'latest', 'as', 'by', 'eval',
                   'where', 'search', 'stats', 'table', 'sort', 'top', 'rare',
                   'count', 'sum', 'avg', 'min', 'max', 'dc', 'list', 'values',
                   'fields', 'rename', 'dedup', 'head', 'tail', 'limit', 'span',
                   'bin', 'chart', 'timechart', 'distinct_count', 'estdc',
                   'showperc', 'countfield', 'percentfield', 'useother', 'otherstr'}
        fields = fields - keywords

        return fields

    def get_sourcetype_from_spl(self, spl: str) -> str:
        """Extract sourcetype from SPL query"""
        match = re.search(r'sourcetype\s*=\s*([a-zA-Z0-9_]+)', spl)
        if match:
            return match.group(1)

        # Try to infer from index
        if 'index=web' in spl or 'access' in spl.lower():
            return 'access_combined'
        elif 'linux' in spl.lower() or 'secure' in spl.lower() or 'ssh' in spl.lower():
            return 'linux_secure'
        elif 'db_audit' in spl or 'database' in spl.lower():
            return 'db_audit'

        return 'unknown'

    def validate_spl_query(self, lab_file: str, line_num: int, spl: str) -> bool:
        """Validate a single SPL query"""
        is_valid = True

        # Extract sourcetype
        sourcetype = self.get_sourcetype_from_spl(spl)

        # Skip validation for lookup-only queries
        if 'inputlookup' in spl and 'index=' not in spl:
            return True

        # Skip validation if no specific sourcetype and using generic queries
        if sourcetype == 'unknown' and ('index=main' in spl or 'index=_audit' in spl):
            # Allow common Splunk default fields even when sourcetype unknown
            return True

        # Extract fields referenced in the query
        referenced_fields = self.extract_fields_from_spl(spl)

        # Get valid fields for this sourcetype
        valid_fields = self.sourcetype_fields.get(sourcetype, set())

        # Always allow Splunk default fields regardless of sourcetype
        default_fields = {"_time", "host", "source", "sourcetype", "_raw", "index", "_indextime",
                         # Time-based fields auto-extracted from _time
                         "date_hour", "date_mday", "date_minute", "date_month", "date_second",
                         "date_wday", "date_year", "date_zone"}
        valid_fields = valid_fields | default_fields

        # If using | rest command, add REST API fields
        if '| rest' in spl:
            rest_fields = {"title", "search", "cron_schedule", "is_scheduled",
                          "alert_comparator", "alert_threshold", "actions", "sid",
                          "disabled", "updated", "published", "trigger_time",
                          "severity", "next_scheduled_time", "next_run", "triggered_alert_count"}
            valid_fields = valid_fields | rest_fields

        # Extract fields that are created within the query (aliases)
        created_fields = set()
        # Fields created with "as" keyword
        as_pattern = r'as\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        created_fields.update(re.findall(as_pattern, spl))

        # If query uses lookup, add lookup table fields to valid fields
        # Also add for access_combined_wcookie since automatic lookups are configured in Lab8
        if '| lookup' in spl or 'lookup' in spl or sourcetype == 'access_combined_wcookie':
            # Add fields from products.csv lookup (both original and aliased names)
            lookup_fields = {"productId", "product_name", "ProductName", "categoryId",
                           "price", "Price", "Code", "product"}
            valid_fields = valid_fields | lookup_fields

        # Skip validation for syntax examples (contain placeholders)
        if '<' in spl and '>' in spl:
            return True

        # Check each referenced field
        for field in referenced_fields:
            # Skip quoted strings and special fields
            if field.startswith('"') or field.startswith("'"):
                continue

            # Skip fields that are created within this query
            if field in created_fields:
                continue

            # Skip fields that are created by eval or rename
            if '| eval' in spl and field in spl.split('| eval')[1].split('=')[0]:
                continue

            # Check if field exists
            if field not in valid_fields:
                # Check if it's an aliased field
                is_alias = False
                for canonical, aliases in self.field_aliases.items():
                    if field in aliases and canonical in valid_fields:
                        is_alias = True
                        break

                if not is_alias:
                    self.add_error(
                        f"{lab_file}:{line_num} - Field '{field}' not found in sourcetype '{sourcetype}'\n"
                        f"     Available fields: {sorted(valid_fields)}\n"
                        f"     SPL: {spl[:100]}..."
                    )
                    is_valid = False

        return is_valid

    def validate_data_files(self) -> bool:
        """Validate that data files exist and can be parsed"""
        print("\n📊 Validating Data Files...")

        data_dir = self.course_root / "labs" / "data"

        # Check access logs
        access_log = data_dir / "access_30DAY.log"
        if access_log.exists():
            print(f"  ✓ Found {access_log.name}")
            # Sample a few lines to verify format
            with open(access_log) as f:
                for i, line in enumerate(f):
                    if i >= 3:
                        break
                    # Check if line matches expected format
                    if not re.match(r'^\d+\.\d+\.\d+\.\d+\s+-\s+-\s+\[', line):
                        self.add_warning(f"Line {i+1} in {access_log.name} doesn't match expected format")
        else:
            self.add_error(f"Missing data file: access_30DAY.log")

        # Check Linux secure logs
        linux_log = data_dir / "linux_s_30DAY.log"
        if linux_log.exists():
            print(f"  ✓ Found {linux_log.name}")
        else:
            self.add_error(f"Missing data file: linux_s_30DAY.log")

        # Check CSV files
        for csv_file in ["db_audit_30DAY.csv", "products.csv"]:
            csv_path = data_dir / csv_file
            if csv_path.exists():
                print(f"  ✓ Found {csv_file}")
                # Verify CSV headers
                with open(csv_path) as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    if csv_file == "db_audit_30DAY.csv":
                        expected = ["Time", "Type", "Command", "Duration"]
                        if headers != expected:
                            self.add_error(f"{csv_file} has wrong headers: {headers}, expected: {expected}")
                    elif csv_file == "products.csv":
                        expected = ["productId", "product_name", "categoryId", "price", "Code"]
                        if headers != expected:
                            self.add_error(f"{csv_file} has wrong headers: {headers}, expected: {expected}")
            else:
                self.add_error(f"Missing data file: {csv_file}")

        return len(self.errors) == 0

    def run_validation(self) -> bool:
        """Run all validation checks"""
        print("🚀 Starting SPL-Data Alignment Validation")
        print(f"📂 Course Root: {self.course_root.absolute()}\n")

        # Validate data files exist
        self.validate_data_files()

        # Extract all SPL queries
        spl_queries = self.extract_spl_from_labs()

        # Validate each query
        print("\n🔬 Validating SPL Field References...")
        total_queries = sum(len(queries) for queries in spl_queries.values())
        validated = 0

        for lab_file, queries in spl_queries.items():
            for line_num, spl in queries:
                self.validate_spl_query(lab_file, line_num, spl)
                validated += 1

        print(f"  ✓ Validated {validated} SPL queries across {len(spl_queries)} lab files")

        # Generate report
        return self.generate_report()

    def generate_report(self) -> bool:
        """Generate and print validation report"""
        print("\n" + "="*70)
        print("📊 SPL-DATA ALIGNMENT REPORT")
        print("="*70)

        if len(self.errors) == 0 and len(self.warnings) == 0:
            print("\n✅ 100% SPL-Data alignment confirmed! All queries reference valid fields.")
            return True

        if len(self.errors) > 0:
            print(f"\n❌ Found {len(self.errors)} field alignment error(s):\n")
            for error in self.errors:
                print(f"{error}\n")

        if len(self.warnings) > 0:
            print(f"\n⚠️  Found {len(self.warnings)} warning(s):\n")
            for warning in self.warnings:
                print(f"{warning}\n")

        print("="*70)

        return len(self.errors) == 0

def main():
    """Main entry point"""
    course_root = os.getcwd()

    if not os.path.exists(os.path.join(course_root, "labs")):
        print("❌ ERROR: Cannot find 'labs' directory. Run from course root.")
        return 1

    validator = SPLDataValidator(course_root)
    success = validator.run_validation()

    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
