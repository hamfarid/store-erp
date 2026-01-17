#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Coverage Report Generator
===============================

Generates comprehensive test coverage reports for the Store ERP backend.

Usage:
    # Generate HTML coverage report:
    python backend/scripts/generate_coverage_report.py

    # Generate coverage report with specific test files:
    python backend/scripts/generate_coverage_report.py --tests tests/test_api_*.py

    # Generate coverage report with minimum threshold:
    python backend/scripts/generate_coverage_report.py --min-coverage 80

    # Generate JSON report for CI/CD:
    python backend/scripts/generate_coverage_report.py --format json
"""

import subprocess
import sys
import os
import argparse
import json
from pathlib import Path
from datetime import datetime


def run_command(cmd, cwd=None):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True
        )
        return result.stdout, result.stderr, 0
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode


def generate_coverage_report(
    test_pattern="tests/", min_coverage=None, output_format="html"
):
    """
    Generate test coverage report

    Args:
        test_pattern: Pattern for test files to run
        min_coverage: Minimum coverage percentage required
        output_format: Output format (html, json, xml, term)
    """
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    print("=" * 80)
    print("Test Coverage Report Generator")
    print("=" * 80)
    print(f"Backend directory: {backend_dir}")
    print(f"Test pattern: {test_pattern}")
    print(f"Output format: {output_format}")
    if min_coverage:
        print(f"Minimum coverage: {min_coverage}%")
    print("=" * 80)
    print()

    # Install coverage if not installed
    print("📦 Checking coverage installation...")
    stdout, stderr, code = run_command("pip show coverage")
    if code != 0:
        print("Installing coverage...")
        run_command("pip install coverage pytest-cov")
    print("✅ Coverage installed")
    print()

    # Run tests with coverage
    print("🧪 Running tests with coverage...")
    coverage_cmd = f"python -m pytest {test_pattern} --cov=src --cov-report=term --cov-report=html --cov-report=json --cov-report=xml -v"

    if min_coverage:
        coverage_cmd += f" --cov-fail-under={min_coverage}"

    print(f"Command: {coverage_cmd}")
    print()

    stdout, stderr, code = run_command(coverage_cmd)

    # Print output
    print(stdout)
    if stderr:
        print("STDERR:", stderr)

    # Parse coverage results
    print()
    print("=" * 80)
    print("Coverage Results")
    print("=" * 80)

    # Read JSON coverage report
    coverage_json_path = backend_dir / "coverage.json"
    if coverage_json_path.exists():
        with open(coverage_json_path, "r") as f:
            coverage_data = json.load(f)

        total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
        print(f"📊 Total Coverage: {total_coverage:.2f}%")
        print()

        # Print coverage by file
        print("Coverage by File:")
        print("-" * 80)
        files = coverage_data.get("files", {})
        sorted_files = sorted(
            files.items(), key=lambda x: x[1]["summary"]["percent_covered"]
        )

        for file_path, file_data in sorted_files:
            summary = file_data["summary"]
            percent = summary["percent_covered"]
            covered = summary["covered_lines"]
            total = summary["num_statements"]

            # Color code based on coverage
            if percent >= 80:
                status = "✅"
            elif percent >= 60:
                status = "⚠️"
            else:
                status = "❌"

            print(f"{status} {file_path:60s} {percent:6.2f}% ({covered}/{total})")

        print("-" * 80)
        print()

        # Print summary statistics
        print("Summary Statistics:")
        print("-" * 80)
        totals = coverage_data.get("totals", {})
        print(f"Total Statements:     {totals.get('num_statements', 0)}")
        print(f"Covered Statements:   {totals.get('covered_lines', 0)}")
        print(f"Missing Statements:   {totals.get('missing_lines', 0)}")
        print(f"Excluded Statements:  {totals.get('excluded_lines', 0)}")
        print(f"Coverage Percentage:  {totals.get('percent_covered', 0):.2f}%")
        print("-" * 80)
        print()

        # Check minimum coverage
        if min_coverage and total_coverage < min_coverage:
            print(f"❌ Coverage {total_coverage:.2f}% is below minimum {min_coverage}%")
            return 1
        elif min_coverage:
            print(f"✅ Coverage {total_coverage:.2f}% meets minimum {min_coverage}%")

    # Print report locations
    print()
    print("=" * 80)
    print("Generated Reports")
    print("=" * 80)

    html_report = backend_dir / "htmlcov" / "index.html"
    if html_report.exists():
        print(f"📄 HTML Report: {html_report}")
        print(f"   Open in browser: file://{html_report.absolute()}")

    json_report = backend_dir / "coverage.json"
    if json_report.exists():
        print(f"📄 JSON Report: {json_report}")

    xml_report = backend_dir / "coverage.xml"
    if xml_report.exists():
        print(f"📄 XML Report: {xml_report}")

    print("=" * 80)
    print()

    # Generate summary markdown
    generate_summary_markdown(coverage_data if coverage_json_path.exists() else None)

    return code


def generate_summary_markdown(coverage_data):
    """Generate a markdown summary of coverage"""
    backend_dir = Path(__file__).parent.parent
    summary_path = backend_dir / "coverage_summary.md"

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Test Coverage Summary\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if coverage_data:
            totals = coverage_data.get("totals", {})
            total_coverage = totals.get("percent_covered", 0)

            f.write("## Overall Coverage\n\n")
            f.write(f"- **Total Coverage:** {total_coverage:.2f}%\n")
            f.write(f"- **Total Statements:** {totals.get('num_statements', 0)}\n")
            f.write(f"- **Covered Statements:** {totals.get('covered_lines', 0)}\n")
            f.write(f"- **Missing Statements:** {totals.get('missing_lines', 0)}\n\n")

            # Coverage badge
            if total_coverage >= 80:
                badge_color = "brightgreen"
            elif total_coverage >= 60:
                badge_color = "yellow"
            else:
                badge_color = "red"

            f.write(
                f"![Coverage](https://img.shields.io/badge/coverage-{total_coverage:.0f}%25-{badge_color})\n\n"
            )

            # Coverage by module
            f.write("## Coverage by Module\n\n")
            f.write("| Module | Coverage | Statements | Covered | Missing |\n")
            f.write("|--------|----------|------------|---------|----------|\n")

            files = coverage_data.get("files", {})
            modules = {}

            # Group by module
            for file_path, file_data in files.items():
                module = file_path.split("/")[0] if "/" in file_path else "root"
                if module not in modules:
                    modules[module] = {"statements": 0, "covered": 0, "missing": 0}

                summary = file_data["summary"]
                modules[module]["statements"] += summary["num_statements"]
                modules[module]["covered"] += summary["covered_lines"]
                modules[module]["missing"] += summary["missing_lines"]

            # Write module summary
            for module, data in sorted(modules.items()):
                if data["statements"] > 0:
                    percent = (data["covered"] / data["statements"]) * 100
                    f.write(
                        f"| {module} | {percent:.2f}% | {data['statements']} | {data['covered']} | {data['missing']} |\n"
                    )

            f.write("\n")

            # Low coverage files
            f.write("## Files with Low Coverage (<60%)\n\n")
            low_coverage_files = [
                (path, data)
                for path, data in files.items()
                if data["summary"]["percent_covered"] < 60
            ]

            if low_coverage_files:
                f.write("| File | Coverage | Statements | Covered | Missing |\n")
                f.write("|------|----------|------------|---------|----------|\n")

                for file_path, file_data in sorted(
                    low_coverage_files, key=lambda x: x[1]["summary"]["percent_covered"]
                ):
                    summary = file_data["summary"]
                    percent = summary["percent_covered"]
                    f.write(
                        f"| {file_path} | {percent:.2f}% | {summary['num_statements']} | {summary['covered_lines']} | {summary['missing_lines']} |\n"
                    )
            else:
                f.write("✅ No files with coverage below 60%\n")

            f.write("\n")

    print(f"📄 Markdown Summary: {summary_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate test coverage report")
    parser.add_argument(
        "--tests", default="tests/", help="Test pattern (default: tests/)"
    )
    parser.add_argument("--min-coverage", type=int, help="Minimum coverage percentage")
    parser.add_argument(
        "--format",
        choices=["html", "json", "xml", "term"],
        default="html",
        help="Output format",
    )

    args = parser.parse_args()

    return generate_coverage_report(
        test_pattern=args.tests,
        min_coverage=args.min_coverage,
        output_format=args.format,
    )


if __name__ == "__main__":
    sys.exit(main())
