#!/usr/bin/env python3
import os
import glob

def generate_report():
    report_content = "# Comprehensive Test Report\n\n"
    
    # Audit Section
    if os.path.exists("reports/audit_result.json"):
        with open("reports/audit_result.json") as f:
            report_content += "## System Audit\n```json\n" + f.read() + "\n```\n\n"
            
    # Logs Section
    report_content += "## Execution Logs\n"
    for log_file in glob.glob("reports/*.log"):
        filename = os.path.basename(log_file)
        with open(log_file) as f:
            content = f.read()
            # Summarize: take first 5 lines and last 5 lines
            lines = content.splitlines()
            summary = "\n".join(lines[:10])
            if len(lines) > 20:
                summary += "\n... (truncated) ...\n" + "\n".join(lines[-10:])
            else:
                summary = "\n".join(lines)
                
            report_content += f"### {filename}\n```\n{summary}\n```\n\n"
            
    with open("reports/test_summary.md", "w") as f:
        f.write(report_content)
    print("Report generated at reports/test_summary.md")

if __name__ == "__main__":
    generate_report()
