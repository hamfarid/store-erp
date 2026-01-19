"""
FILE: backend/scripts/run_tests.py | PURPOSE: Test runner script | OWNER: QA Team | LAST-AUDITED: 2025-11-18

Test Runner Script

Runs all tests and generates coverage reports.

Usage:
    python backend/scripts/run_tests.py [options]
    
Options:
    --unit          Run only unit tests
    --integration   Run only integration tests
    --e2e           Run only E2E tests
    --security      Run only security tests
    --coverage      Generate coverage report
    --html          Generate HTML coverage report
    --verbose       Verbose output

Version: 1.0.0
"""

import sys
import subprocess
from pathlib import Path
import argparse


def main():
    """Run tests with specified options"""
    
    parser = argparse.ArgumentParser(description='Run Gaara AI tests')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--e2e', action='store_true', help='Run E2E tests only')
    parser.add_argument('--security', action='store_true', help='Run security tests only')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--failfast', '-x', action='store_true', help='Stop on first failure')
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = ['pytest']
    
    # Add markers
    markers = []
    if args.unit:
        markers.append('unit')
    if args.integration:
        markers.append('integration')
    if args.e2e:
        markers.append('e2e')
    if args.security:
        markers.append('security')
    
    if markers:
        cmd.extend(['-m', ' or '.join(markers)])
    
    # Add coverage
    if args.coverage or args.html:
        cmd.extend(['--cov=src', '--cov-report=term-missing'])
        if args.html:
            cmd.append('--cov-report=html')
    
    # Add verbosity
    if args.verbose:
        cmd.append('-vv')
    else:
        cmd.append('-v')
    
    # Add fail fast
    if args.failfast:
        cmd.append('-x')
    
    # Add test directory
    cmd.append('tests')
    
    print("=" * 80)
    print("🧪 GAARA AI - TEST RUNNER")
    print("=" * 80)
    print(f"Command: {' '.join(cmd)}")
    print("=" * 80)
    print()
    
    # Run tests
    result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
    
    print()
    print("=" * 80)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 80)
    
    sys.exit(result.returncode)


if __name__ == '__main__':
    main()

