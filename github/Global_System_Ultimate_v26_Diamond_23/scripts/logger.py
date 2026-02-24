import os
import logging
from datetime import datetime
from pathlib import Path

class GaaraLogger:
    """
    A comprehensive logging system for the Gaara AI ecosystem.
    Supports System, AI, Learning, User, and IP logs.
    """
    
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_files = {
            "system": self.log_dir / "system_log.md",
            "ai": self.log_dir / "ai_log.md",
            "learning": self.log_dir / "learning_log.md",
            "user": self.log_dir / "user_log.md",
            "ip": self.log_dir / "ip_log.md"
        }
        
        self._initialize_logs()

    def _initialize_logs(self):
        """Initialize log files with headers if they don't exist."""
        headers = {
            "system": "| Timestamp | Level | Component | Event | Details |\n|---|---|---|---|---|\n",
            "ai": "| Timestamp | Agent | Activity | Input/Asset | Output/Result | Confidence/Metrics |\n|---|---|---|---|---|---|\n",
            "learning": "| Timestamp | Model/Component | Experiment/Action | Parameters | Result/Score | Decision |\n|---|---|---|---|---|---|\n",
            "user": "| Timestamp | User ID | Interaction Type | Query/Action | Response/Outcome | Satisfaction |\n|---|---|---|---|---|---|\n",
            "ip": "| Timestamp | IP Address | User ID | Action | Resource | Status |\n|---|---|---|---|---|---|\n"
        }
        
        for log_type, file_path in self.log_files.items():
            if not file_path.exists():
                with open(file_path, "w") as f:
                    f.write(f"# {log_type.capitalize()} Log\n\n")
                    f.write(headers[log_type])

    def _write_log(self, log_type, *args):
        """Write a formatted log entry to the specified log file."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        # Convert all arguments to string and replace pipes to avoid breaking markdown table
        sanitized_args = [str(arg).replace("|", "\\|") for arg in args]
        entry = f"| {timestamp} | " + " | ".join(sanitized_args) + " |\n"
        
        with open(self.log_files[log_type], "a") as f:
            f.write(entry)
            
    def log_system(self, level, component, event, details=""):
        """Log a system event."""
        self._write_log("system", level, component, event, details)

    def log_ai(self, agent, activity, input_asset, output_result, metrics=""):
        """Log an AI activity."""
        self._write_log("ai", agent, activity, input_asset, output_result, metrics)

    def log_learning(self, component, action, params, result, decision=""):
        """Log a learning or optimization event."""
        self._write_log("learning", component, action, params, result, decision)

    def log_user(self, user_id, interaction_type, query, response, satisfaction=""):
        """Log a user interaction."""
        self._write_log("user", user_id, interaction_type, query, response, satisfaction)

    def log_ip(self, ip_address, user_id, action, resource, status):
        """Log an IP access event."""
        self._write_log("ip", ip_address, user_id, action, resource, status)

# Singleton instance for easy import
logger = GaaraLogger()

if __name__ == "__main__":
    # Test logging
    logger.log_system("INFO", "Logger", "Initialized", "Logging system ready")
    logger.log_ip("192.168.1.1", "admin", "LOGIN", "Dashboard", "Success")
    print("Test logs written successfully.")
