#!/usr/bin/env python3
"""
System Logger - Automatic logging utility for AI agents
"""

import os
from datetime import datetime
from pathlib import Path

class SystemLogger:
    def __init__(self, log_file="system_log.md"):
        self.log_file = Path(log_file)
        if not self.log_file.exists():
            self.log_file.write_text("# System Log\n\n")
    
    def log_intent(self, command: str, task: str, details: str = ""):
        """Log the intent before executing a command"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        log_entry = f"`{timestamp}` - **[INTENT]** - `Executing command: {command}` - **[DETAILS]** - `Task: {task}`"
        if details:
            log_entry += f" - {details}"
        log_entry += "\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        print(f"[LOGGED INTENT] {command}")
    
    def log_result(self, exit_code: int, output: str = "", details: str = ""):
        """Log the result after executing a command"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        status = "SUCCESS" if exit_code == 0 else "FAILURE"
        truncated_output = output[:200] + "..." if len(output) > 200 else output
        
        log_entry = f"`{timestamp}` - **[RESULT]** - `Exit Code: {exit_code}` - **[STATUS]** - `{status}`"
        if truncated_output:
            log_entry += f" - **[OUTPUT]** - `{truncated_output}`"
        if details:
            log_entry += f" - **[DETAILS]** - `{details}`"
        log_entry += "\n\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        print(f"[LOGGED RESULT] Exit Code: {exit_code}")
    
    def log_phase_start(self, phase_name: str, phase_number: int):
        """Log the start of a new phase"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        log_entry = f"\n---\n\n## Phase {phase_number}: {phase_name}\n\n`{timestamp}` - **[PHASE_START]** - `Starting Phase {phase_number}: {phase_name}`\n\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        print(f"[PHASE START] Phase {phase_number}: {phase_name}")
    
    def log_phase_complete(self, phase_name: str, phase_number: int):
        """Log the completion of a phase"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        log_entry = f"`{timestamp}` - **[PHASE_COMPLETE]** - `Completed Phase {phase_number}: {phase_name}`\n\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        print(f"[PHASE COMPLETE] Phase {phase_number}: {phase_name}")
    
    def log_error(self, error_message: str, severity: str = "HIGH"):
        """Log an error"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        log_entry = f"`{timestamp}` - **[ERROR]** - **[SEVERITY: {severity}]** - `{error_message}`\n\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        print(f"[ERROR] {error_message}")
    
    def log_decision(self, decision: str, rationale: str):
        """Log a decision and its rationale"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        log_entry = f"`{timestamp}` - **[DECISION]** - `{decision}` - **[RATIONALE]** - `{rationale}`\n\n"
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        print(f"[DECISION] {decision}")

# Example usage
if __name__ == "__main__":
    logger = SystemLogger()
    
    # Example: Log a phase start
    logger.log_phase_start("Initialization & Analysis", 1)
    
    # Example: Log an intent
    logger.log_intent("python3 analyze_project.py", "Analyze existing project structure")
    
    # Example: Log a result
    logger.log_result(0, "Project analyzed successfully. Found 150 files.")
    
    # Example: Log a decision
    logger.log_decision(
        "Use PostgreSQL for database",
        "PostgreSQL chosen over MySQL due to better JSON support (OSF: Security 35%, Correctness 20%)"
    )
    
    # Example: Log a phase complete
    logger.log_phase_complete("Initialization & Analysis", 1)
    
    print("\n✓ System logger demonstration complete. Check system_log.md")
