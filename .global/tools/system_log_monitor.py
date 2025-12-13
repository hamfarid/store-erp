#!/usr/bin/env python3
"""
System Log Monitor - Advanced Background Error Tracking
Monitors system logs, application logs, and runtime errors in real-time
"""

import os
import sys
import json
import time
import logging
import threading
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import re

class SystemLogMonitor:
    def __init__(self, project_root='.'):
        self.project_root = Path(project_root).resolve()
        self.log_dir = self.project_root / 'logs'
        self.log_dir.mkdir(exist_ok=True)
        
        self.errors = defaultdict(list)
        self.warnings = defaultdict(list)
        self.info_messages = defaultdict(list)
        
        self.running = False
        self.threads = []
        
        # Setup logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.log_dir / f'system_monitor_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('SystemLogMonitor')
        
    def start(self):
        """Start monitoring"""
        self.logger.info("🚀 Starting System Log Monitor...")
        self.running = True
        
        # Start monitoring threads
        monitors = [
            self.monitor_npm_logs,
            self.monitor_console_logs,
            self.monitor_application_logs,
            self.monitor_system_errors,
            self.monitor_network_errors,
            self.monitor_database_logs
        ]
        
        for monitor in monitors:
            thread = threading.Thread(target=monitor, daemon=True)
            thread.start()
            self.threads.append(thread)
            
        self.logger.info("✅ All monitors started")
        
        try:
            # Main loop - generate reports periodically
            while self.running:
                time.sleep(60)  # Generate report every minute
                self.generate_report()
        except KeyboardInterrupt:
            self.stop()
            
    def stop(self):
        """Stop monitoring"""
        self.logger.info("🛑 Stopping System Log Monitor...")
        self.running = False
        
        for thread in self.threads:
            thread.join(timeout=2)
            
        self.generate_final_report()
        self.logger.info("✅ System Log Monitor stopped")
        
    def monitor_npm_logs(self):
        """Monitor npm/node logs"""
        self.logger.info("📦 Monitoring npm logs...")
        
        npm_log_file = Path.home() / '.npm' / '_logs'
        
        while self.running:
            try:
                if npm_log_file.exists():
                    # Get latest log file
                    log_files = sorted(npm_log_file.glob('*.log'), key=os.path.getmtime, reverse=True)
                    
                    if log_files:
                        with open(log_files[0], 'r') as f:
                            content = f.read()
                            
                        # Parse errors
                        errors = re.findall(r'error (.+)', content, re.IGNORECASE)
                        for error in errors:
                            self.log_error('npm', error)
                            
                time.sleep(10)
            except Exception as e:
                self.logger.error(f"Error monitoring npm logs: {e}")
                
    def monitor_console_logs(self):
        """Monitor browser console logs"""
        self.logger.info("🌐 Monitoring console logs...")
        
        console_log = self.log_dir / 'console.log'
        
        if not console_log.exists():
            console_log.touch()
            
        last_position = 0
        
        while self.running:
            try:
                if console_log.exists():
                    with open(console_log, 'r') as f:
                        f.seek(last_position)
                        new_content = f.read()
                        last_position = f.tell()
                        
                    if new_content:
                        # Parse console errors
                        lines = new_content.split('\n')
                        for line in lines:
                            if 'ERROR' in line or 'Error' in line:
                                self.log_error('console', line)
                            elif 'WARN' in line or 'Warning' in line:
                                self.log_warning('console', line)
                                
                time.sleep(5)
            except Exception as e:
                self.logger.error(f"Error monitoring console logs: {e}")
                
    def monitor_application_logs(self):
        """Monitor application-specific logs"""
        self.logger.info("📱 Monitoring application logs...")
        
        app_log_patterns = [
            'logs/*.log',
            'logs/**/*.log',
            '.logs/*.log',
            'app.log',
            'error.log'
        ]
        
        monitored_files = {}
        
        while self.running:
            try:
                for pattern in app_log_patterns:
                    for log_file in self.project_root.glob(pattern):
                        if log_file not in monitored_files:
                            monitored_files[log_file] = 0
                            
                        with open(log_file, 'r') as f:
                            f.seek(monitored_files[log_file])
                            new_content = f.read()
                            monitored_files[log_file] = f.tell()
                            
                        if new_content:
                            self.parse_log_content(log_file.name, new_content)
                            
                time.sleep(5)
            except Exception as e:
                self.logger.error(f"Error monitoring application logs: {e}")
                
    def monitor_system_errors(self):
        """Monitor system-level errors"""
        self.logger.info("🖥️  Monitoring system errors...")
        
        while self.running:
            try:
                # Check for unhandled exceptions
                exception_log = self.log_dir / 'exceptions.log'
                if exception_log.exists():
                    with open(exception_log, 'r') as f:
                        content = f.read()
                        
                    if content:
                        self.log_error('system', f"Unhandled exception detected: {content[:200]}")
                        
                # Check for segfaults
                if sys.platform == 'linux':
                    try:
                        result = subprocess.run(
                            ['dmesg', '-T'],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        
                        if 'segfault' in result.stdout.lower():
                            self.log_error('system', "Segmentation fault detected")
                    except:
                        pass
                        
                time.sleep(30)
            except Exception as e:
                self.logger.error(f"Error monitoring system errors: {e}")
                
    def monitor_network_errors(self):
        """Monitor network-related errors"""
        self.logger.info("🌐 Monitoring network errors...")
        
        network_log = self.log_dir / 'network.log'
        
        while self.running:
            try:
                if network_log.exists():
                    with open(network_log, 'r') as f:
                        content = f.read()
                        
                    # Parse network errors
                    errors = re.findall(r'(ECONNREFUSED|ETIMEDOUT|ENOTFOUND|ERR_CONNECTION|Failed to fetch)', content)
                    for error in errors:
                        self.log_error('network', error)
                        
                time.sleep(10)
            except Exception as e:
                self.logger.error(f"Error monitoring network errors: {e}")
                
    def monitor_database_logs(self):
        """Monitor database errors"""
        self.logger.info("🗄️  Monitoring database logs...")
        
        db_log_patterns = [
            'logs/database.log',
            'logs/db.log',
            'logs/sql.log',
            'prisma.log'
        ]
        
        while self.running:
            try:
                for pattern in db_log_patterns:
                    db_log = self.project_root / pattern
                    if db_log.exists():
                        with open(db_log, 'r') as f:
                            content = f.read()
                            
                        # Parse database errors
                        errors = re.findall(r'(ERROR|FATAL|PANIC):(.+)', content)
                        for level, error in errors:
                            self.log_error('database', f"{level}: {error}")
                            
                time.sleep(15)
            except Exception as e:
                self.logger.error(f"Error monitoring database logs: {e}")
                
    def parse_log_content(self, source, content):
        """Parse log content and categorize"""
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Categorize by level
            if any(keyword in line.upper() for keyword in ['ERROR', 'FATAL', 'CRITICAL']):
                self.log_error(source, line)
            elif any(keyword in line.upper() for keyword in ['WARN', 'WARNING']):
                self.log_warning(source, line)
            elif any(keyword in line.upper() for keyword in ['INFO', 'DEBUG']):
                self.log_info(source, line)
                
    def log_error(self, source, message):
        """Log an error"""
        error = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'message': message,
            'level': 'ERROR'
        }
        
        self.errors[source].append(error)
        self.logger.error(f"[{source}] {message}")
        
        # Save to errors log
        errors_log = self.log_dir / 'errors.jsonl'
        with open(errors_log, 'a') as f:
            f.write(json.dumps(error) + '\n')
            
    def log_warning(self, source, message):
        """Log a warning"""
        warning = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'message': message,
            'level': 'WARNING'
        }
        
        self.warnings[source].append(warning)
        self.logger.warning(f"[{source}] {message}")
        
    def log_info(self, source, message):
        """Log an info message"""
        info = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'message': message,
            'level': 'INFO'
        }
        
        self.info_messages[source].append(info)
        
    def generate_report(self):
        """Generate periodic report"""
        total_errors = sum(len(errors) for errors in self.errors.values())
        total_warnings = sum(len(warnings) for warnings in self.warnings.values())
        
        if total_errors > 0 or total_warnings > 0:
            self.logger.info(f"📊 Current Status: {total_errors} errors, {total_warnings} warnings")
            
    def generate_final_report(self):
        """Generate final comprehensive report"""
        self.logger.info("📝 Generating final report...")
        
        # Calculate statistics
        total_errors = sum(len(errors) for errors in self.errors.values())
        total_warnings = sum(len(warnings) for warnings in self.warnings.values())
        total_info = sum(len(info) for info in self.info_messages.values())
        
        # Group errors by type
        error_types = defaultdict(int)
        for source, errors in self.errors.items():
            for error in errors:
                # Extract error type
                match = re.search(r'(Error|Exception|Failed|Refused|Timeout)', error['message'])
                if match:
                    error_types[match.group(1)] += 1
                else:
                    error_types['Other'] += 1
                    
        # Generate markdown report
        report = f"""# System Log Monitor Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Project:** {self.project_root.name}

---

## Summary

| Category | Count |
|----------|-------|
| **Errors** | {total_errors} |
| **Warnings** | {total_warnings} |
| **Info** | {total_info} |

---

## Errors by Source

| Source | Count |
|--------|-------|
"""
        
        for source, errors in sorted(self.errors.items(), key=lambda x: len(x[1]), reverse=True):
            report += f"| {source} | {len(errors)} |\n"
            
        report += "\n---\n\n## Errors by Type\n\n| Type | Count |\n|------|-------|\n"
        
        for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
            report += f"| {error_type} | {count} |\n"
            
        report += "\n---\n\n## Recent Errors (Last 20)\n\n"
        
        # Get last 20 errors
        all_errors = []
        for source, errors in self.errors.items():
            all_errors.extend(errors)
            
        all_errors.sort(key=lambda x: x['timestamp'], reverse=True)
        
        for error in all_errors[:20]:
            report += f"""### {error['source']} - {error['timestamp']}
```
{error['message'][:200]}
```

"""
        
        report += "\n---\n\n## Warnings by Source\n\n| Source | Count |\n|--------|-------|\n"
        
        for source, warnings in sorted(self.warnings.items(), key=lambda x: len(x[1]), reverse=True):
            report += f"| {source} | {len(warnings)} |\n"
            
        report += "\n---\n\n## Recommendations\n\n"
        
        if total_errors > 0:
            report += "⚠️ **Errors detected** - Review and fix the errors listed above\n"
        if total_warnings > 10:
            report += "⚠️ **High warning count** - Investigate and address warnings\n"
        if 'network' in self.errors and len(self.errors['network']) > 5:
            report += "🌐 **Network issues** - Check network connectivity and API endpoints\n"
        if 'database' in self.errors and len(self.errors['database']) > 0:
            report += "🗄️ **Database errors** - Review database configuration and queries\n"
        if total_errors == 0 and total_warnings == 0:
            report += "✅ **No issues detected** - System is running smoothly\n"
            
        report += "\n---\n\n**Generated by:** System Log Monitor  \n**Version:** 1.0\n"
        
        # Save report
        report_file = self.log_dir / f'SYSTEM_LOG_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        with open(report_file, 'w') as f:
            f.write(report)
            
        # Save JSON summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'project': str(self.project_root),
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'total_info': total_info,
            'errors_by_source': {k: len(v) for k, v in self.errors.items()},
            'warnings_by_source': {k: len(v) for k, v in self.warnings.items()},
            'error_types': dict(error_types)
        }
        
        summary_file = self.log_dir / 'system_log_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
            
        self.logger.info(f"📁 Report saved: {report_file}")
        self.logger.info(f"📁 Summary saved: {summary_file}")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 SYSTEM LOG MONITOR - FINAL REPORT")
        print("="*60)
        print(f"Total Errors: {total_errors}")
        print(f"Total Warnings: {total_warnings}")
        print(f"Total Info: {total_info}")
        print("\nTop Error Sources:")
        for source, errors in sorted(self.errors.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            print(f"  - {source}: {len(errors)}")
        print("\nTop Error Types:")
        for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  - {error_type}: {count}")
        print("="*60 + "\n")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='System Log Monitor')
    parser.add_argument('project_root', nargs='?', default='.', help='Project root directory')
    parser.add_argument('--duration', type=int, default=0, help='Monitor duration in seconds (0 = infinite)')
    
    args = parser.parse_args()
    
    monitor = SystemLogMonitor(args.project_root)
    
    if args.duration > 0:
        # Run for specified duration
        thread = threading.Thread(target=monitor.start, daemon=True)
        thread.start()
        time.sleep(args.duration)
        monitor.stop()
    else:
        # Run until interrupted
        monitor.start()


if __name__ == '__main__':
    main()

