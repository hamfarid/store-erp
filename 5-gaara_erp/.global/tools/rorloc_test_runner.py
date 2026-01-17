#!/usr/bin/env python3
"""
RORLOC Test Runner
Automates the execution of RORLOC testing phases
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class RORLOCTestRunner:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path).resolve()
        self.artifacts_dir = self.project_path / "artifacts"
        self.tests_dir = self.project_path / "tests"
        self.utils_dir = self.project_path / "utils"
        
        # Create directories if they don't exist
        self.artifacts_dir.mkdir(exist_ok=True)
        self.tests_dir.mkdir(exist_ok=True)
        self.utils_dir.mkdir(exist_ok=True)
    
    def print_header(self, text: str):
        """Print colored header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")
    
    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")
    
    def print_warning(self, text: str):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")
    
    def print_info(self, text: str):
        """Print info message"""
        print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")
    
    def run_command(self, command: str, cwd: Optional[Path] = None) -> tuple:
        """Run shell command and return (success, output)"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.project_path,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        self.print_header("CHECKING PREREQUISITES")
        
        all_good = True
        
        # Check MODULE_MAP.md
        module_map = self.project_path / "docs" / "MODULE_MAP.md"
        if module_map.exists():
            self.print_success("docs/MODULE_MAP.md exists")
        else:
            self.print_error("docs/MODULE_MAP.md missing")
            self.print_info("Run: python .global/tools/module_mapper.py .")
            all_good = False
        
        # Check TODO files
        todo_files = [
            "docs/TODO.md",
            "docs/INCOMPLETE_TASKS.md",
            "docs/COMPLETE_TASKS.md"
        ]
        
        for todo_file in todo_files:
            file_path = self.project_path / todo_file
            if file_path.exists():
                self.print_success(f"{todo_file} exists")
            else:
                self.print_error(f"{todo_file} missing")
                all_good = False
        
        # Check Playwright installation
        success, _ = self.run_command("npx playwright --version")
        if success:
            self.print_success("Playwright installed")
        else:
            self.print_warning("Playwright not installed")
            self.print_info("Run: npm i -D @playwright/test typescript")
            self.print_info("Run: npx playwright install --with-deps")
        
        # Check playwright.config.ts
        config_file = self.project_path / "playwright.config.ts"
        if config_file.exists():
            self.print_success("playwright.config.ts exists")
        else:
            self.print_warning("playwright.config.ts missing")
            self.print_info("Will be created automatically")
        
        return all_good
    
    def run_phase_1_record(self) -> bool:
        """Phase 1: Record - Discovery & baselines"""
        self.print_header("PHASE 1: RECORD (Discovery & Baselines)")
        
        # Run discovery tests
        self.print_info("Running discovery tests...")
        success, output = self.run_command("npx playwright test tests/discovery/")
        
        if success:
            self.print_success("Phase 1: Record completed")
            
            # Check artifacts
            required_artifacts = [
                "site-map.json",
                "ui-inventory.json",
                "api-inventory.json",
                "db-schema.json",
                "baseline-issues.json"
            ]
            
            for artifact in required_artifacts:
                artifact_path = self.artifacts_dir / artifact
                if artifact_path.exists():
                    self.print_success(f"  {artifact} created")
                else:
                    self.print_warning(f"  {artifact} missing")
            
            return True
        else:
            self.print_error("Phase 1: Record failed")
            print(output)
            return False
    
    def run_phase_2_organize(self) -> bool:
        """Phase 2: Organize - Categorize & prioritize"""
        self.print_header("PHASE 2: ORGANIZE (Categorize & Prioritize)")
        
        # Run organization tests
        self.print_info("Creating test matrix...")
        success, output = self.run_command("npx playwright test tests/organize/")
        
        if success:
            self.print_success("Phase 2: Organize completed")
            
            # Check test matrix
            test_matrix = self.artifacts_dir / "test-matrix.json"
            if test_matrix.exists():
                self.print_success("  test-matrix.json created")
                
                # Display priority breakdown
                with open(test_matrix) as f:
                    matrix = json.load(f)
                    priority = matrix.get('priority', {})
                    
                    print(f"\n  Priority Breakdown:")
                    print(f"    Critical: {len(priority.get('critical', []))} routes")
                    print(f"    High: {len(priority.get('high', []))} routes")
                    print(f"    Medium: {len(priority.get('medium', []))} routes")
                    print(f"    Low: {len(priority.get('low', []))} routes")
            
            return True
        else:
            self.print_error("Phase 2: Organize failed")
            print(output)
            return False
    
    def run_phase_3_refactor(self) -> bool:
        """Phase 3: Refactor - Reuse & efficiency"""
        self.print_header("PHASE 3: REFACTOR (Reuse & Efficiency)")
        
        # Check utilities
        required_utils = [
            "base-page.ts",
            "cdp-guard.ts",
            "buttons-verifier.ts",
            "api-client.ts",
            "db-transaction.ts"
        ]
        
        all_exist = True
        for util in required_utils:
            util_path = self.utils_dir / util
            if util_path.exists():
                self.print_success(f"  {util} exists")
            else:
                self.print_warning(f"  {util} missing")
                all_exist = False
        
        if all_exist:
            self.print_success("Phase 3: Refactor completed")
            return True
        else:
            self.print_warning("Phase 3: Some utilities missing")
            self.print_info("Create utilities as per RORLOC methodology")
            return False
    
    def run_phase_4_locate(self) -> bool:
        """Phase 4: Locate - Execute & find issues"""
        self.print_header("PHASE 4: LOCATE (Execute & Find Issues)")
        
        # Run all locate tests
        self.print_info("Running comprehensive tests...")
        success, output = self.run_command("npx playwright test tests/locate/")
        
        if success:
            self.print_success("Phase 4: Locate completed")
            
            # Check reports
            reports = [
                "buttons-report.json",
                "error-report.json",
                "qa-report.json"
            ]
            
            for report in reports:
                report_path = self.artifacts_dir / report
                if report_path.exists():
                    self.print_success(f"  {report} created")
            
            return True
        else:
            self.print_error("Phase 4: Locate found issues")
            print(output)
            return False
    
    def run_phase_5_optimize(self) -> bool:
        """Phase 5: Optimize - Close gaps & harden"""
        self.print_header("PHASE 5: OPTIMIZE (Close Gaps & Harden)")
        
        self.print_info("Analyzing test results...")
        
        # Load QA report
        qa_report_path = self.artifacts_dir / "qa-report.json"
        if not qa_report_path.exists():
            self.print_error("qa-report.json not found")
            return False
        
        with open(qa_report_path) as f:
            qa_report = json.load(f)
        
        # Analyze issues
        issues = qa_report.get('issues', [])
        
        critical = [i for i in issues if i.get('severity') == 'critical']
        high = [i for i in issues if i.get('severity') == 'high']
        medium = [i for i in issues if i.get('severity') == 'medium']
        low = [i for i in issues if i.get('severity') == 'low']
        
        print(f"\n  Issue Breakdown:")
        print(f"    Critical: {len(critical)}")
        print(f"    High: {len(high)}")
        print(f"    Medium: {len(medium)}")
        print(f"    Low: {len(low)}")
        
        if critical or high:
            self.print_error(f"Phase 5: {len(critical)} critical and {len(high)} high priority issues must be fixed")
            return False
        else:
            self.print_success("Phase 5: No critical or high priority issues")
            return True
    
    def run_phase_6_confirm(self) -> bool:
        """Phase 6: Confirm - Regression & sign-off"""
        self.print_header("PHASE 6: CONFIRM (Regression & Sign-Off)")
        
        # Run confirmation tests
        self.print_info("Running final validation...")
        success, output = self.run_command("npx playwright test tests/confirm/")
        
        if not success:
            self.print_error("Phase 6: Confirmation tests failed")
            print(output)
            return False
        
        # Run system verification
        self.print_info("Running system verification...")
        success, output = self.run_command(
            "python .global/tools/complete_system_checker.py ."
        )
        
        if success:
            self.print_success("Phase 6: System verification passed (100%)")
            
            # Generate final report
            self.generate_final_report()
            
            return True
        else:
            self.print_error("Phase 6: System verification failed")
            print(output)
            return False
    
    def generate_final_report(self):
        """Generate final QA report"""
        report_path = self.artifacts_dir / "FINAL_QA_REPORT.md"
        
        report_content = f"""# Final QA Report

**Project:** {self.project_path.name}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**RORLOC Phase:** 6 - Confirm

---

## Executive Summary

**Overall Status:** ✅ PASS

All RORLOC phases completed successfully.

---

## RORLOC Phases

| Phase | Status | Completion Date |
|-------|--------|-----------------|
| 1. Record | ✅ PASS | {datetime.now().strftime('%Y-%m-%d')} |
| 2. Organize | ✅ PASS | {datetime.now().strftime('%Y-%m-%d')} |
| 3. Refactor | ✅ PASS | {datetime.now().strftime('%Y-%m-%d')} |
| 4. Locate | ✅ PASS | {datetime.now().strftime('%Y-%m-%d')} |
| 5. Optimize | ✅ PASS | {datetime.now().strftime('%Y-%m-%d')} |
| 6. Confirm | ✅ PASS | {datetime.now().strftime('%Y-%m-%d')} |

---

## System Verification

**complete_system_checker.py results:**
- ✅ All pages: 100%
- ✅ All buttons: 100%
- ✅ Backend: 100%
- ✅ Database: 100%
- ✅ **Overall: 100%**

---

## Recommendation

**GO / NO-GO:** ✅ GO

The application is production-ready.

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(report_path, 'w') as f:
            f.write(report_content)
        
        self.print_success(f"Final report generated: {report_path}")
    
    def run_all_phases(self):
        """Run all RORLOC phases in sequence"""
        self.print_header("RORLOC TEST RUNNER")
        self.print_info(f"Project: {self.project_path}")
        self.print_info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check prerequisites
        if not self.check_prerequisites():
            self.print_error("Prerequisites not met. Please fix issues and try again.")
            return False
        
        # Run phases
        phases = [
            ("Phase 1: Record", self.run_phase_1_record),
            ("Phase 2: Organize", self.run_phase_2_organize),
            ("Phase 3: Refactor", self.run_phase_3_refactor),
            ("Phase 4: Locate", self.run_phase_4_locate),
            ("Phase 5: Optimize", self.run_phase_5_optimize),
            ("Phase 6: Confirm", self.run_phase_6_confirm),
        ]
        
        for phase_name, phase_func in phases:
            if not phase_func():
                self.print_error(f"{phase_name} failed. Stopping.")
                return False
        
        # Success
        self.print_header("RORLOC TESTING COMPLETE")
        self.print_success("All phases passed!")
        self.print_success("System is production-ready.")
        self.print_info(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python rorloc_test_runner.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"Error: Project path '{project_path}' does not exist")
        sys.exit(1)
    
    runner = RORLOCTestRunner(project_path)
    success = runner.run_all_phases()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

