"""
Error Tracker for Autonomous Multi-Agent System

Tracks and logs errors to prevent repetition.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional


class ErrorTracker:
    """Tracks errors and prevents repetition"""
    
    def __init__(self):
        """Initialize Error Tracker"""
        self.base_path = Path.home() / ".global" / "errors"
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.error_dir = self.base_path / "do_not_make_this_error_again"
        self.error_dir.mkdir(exist_ok=True)
        
        self.log_file = self.base_path / "error_log.json"
        self.stats_file = self.base_path / "error_stats.json"
        
        # Initialize files
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize error tracking files"""
        if not self.log_file.exists():
            self.log_file.write_text("[]", encoding='utf-8')
        
        if not self.stats_file.exists():
            stats = {
                "total_errors": 0,
                "errors_by_project": {},
                "errors_by_agent": {},
                "errors_by_type": {},
                "last_updated": datetime.now().isoformat()
            }
            self.stats_file.write_text(json.dumps(stats, indent=2), encoding='utf-8')
    
    def log_error(self, error_info: Dict[str, Any]) -> str:
        """
        Log an error
        
        Args:
            error_info: Error information dict with keys:
                - name: Error name
                - project: Project name
                - agent: Agent that encountered the error
                - description: Error description
                - solution: How it was fixed
                - code_snippet: (optional) Code that caused the error
                - fix_snippet: (optional) Fixed code
                
        Returns:
            Error ID
        """
        # Load existing log
        log = json.loads(self.log_file.read_text(encoding='utf-8'))
        
        # Create error entry
        error_id = len(log) + 1
        error_entry = {
            "id": error_id,
            "timestamp": datetime.now().isoformat(),
            "name": error_info.get("name", "unknown_error"),
            "project": error_info.get("project", "unknown"),
            "agent": error_info.get("agent", "unknown"),
            "description": error_info.get("description", ""),
            "solution": error_info.get("solution", ""),
            "severity": error_info.get("severity", "medium")
        }
        
        # Add to log
        log.append(error_entry)
        self.log_file.write_text(json.dumps(log, indent=2), encoding='utf-8')
        
        # Create detailed error document
        self._create_error_document(error_id, error_info)
        
        # Update stats
        self._update_stats(error_info)
        
        print(f"✅ Error logged: {error_id:03d}_{error_info['name']}")
        
        return f"{error_id:03d}"
    
    def _create_error_document(self, error_id: int, error_info: Dict[str, Any]):
        """Create detailed error document"""
        error_name = error_info.get("name", "unknown_error").replace(" ", "_")
        error_file = self.error_dir / f"{error_id:03d}_{error_name}.md"
        
        content = f"""# Error #{error_id:03d}: {error_info.get('name', 'Unknown Error')}

## Metadata

- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Project:** {error_info.get('project', 'Unknown')}
- **Agent:** {error_info.get('agent', 'Unknown')}
- **Severity:** {error_info.get('severity', 'medium')}

## Description

{error_info.get('description', 'No description provided')}

## What Went Wrong

{error_info.get('what_went_wrong', 'Not specified')}

## Solution

{error_info.get('solution', 'No solution provided')}

## Code Snippet (Before)

```python
{error_info.get('code_snippet', '# No code snippet provided')}
```

## Fixed Code (After)

```python
{error_info.get('fix_snippet', '# No fix snippet provided')}
```

## How to Avoid

{error_info.get('how_to_avoid', 'Always check this before proceeding.')}

## Related Errors

{error_info.get('related_errors', 'None')}

## Tags

{', '.join(error_info.get('tags', ['general']))}

---

**DO NOT MAKE THIS ERROR AGAIN!**
"""
        
        error_file.write_text(content, encoding='utf-8')
    
    def _update_stats(self, error_info: Dict[str, Any]):
        """Update error statistics"""
        stats = json.loads(self.stats_file.read_text(encoding='utf-8'))
        
        # Update total
        stats["total_errors"] += 1
        
        # Update by project
        project = error_info.get("project", "unknown")
        if project not in stats["errors_by_project"]:
            stats["errors_by_project"][project] = 0
        stats["errors_by_project"][project] += 1
        
        # Update by agent
        agent = error_info.get("agent", "unknown")
        if agent not in stats["errors_by_agent"]:
            stats["errors_by_agent"][agent] = 0
        stats["errors_by_agent"][agent] += 1
        
        # Update by type
        error_type = error_info.get("type", "general")
        if error_type not in stats["errors_by_type"]:
            stats["errors_by_type"][error_type] = 0
        stats["errors_by_type"][error_type] += 1
        
        # Update timestamp
        stats["last_updated"] = datetime.now().isoformat()
        
        self.stats_file.write_text(json.dumps(stats, indent=2), encoding='utf-8')
    
    def get_past_errors(self, project_name: Optional[str] = None, 
                       agent: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get past errors
        
        Args:
            project_name: Filter by project (optional)
            agent: Filter by agent (optional)
            
        Returns:
            List of past errors
        """
        log = json.loads(self.log_file.read_text(encoding='utf-8'))
        
        # Filter
        if project_name:
            log = [e for e in log if e.get("project") == project_name]
        if agent:
            log = [e for e in log if e.get("agent") == agent]
        
        return log
    
    def get_error_summary(self, project_name: str) -> str:
        """
        Get error summary for a project
        
        Args:
            project_name: Project name
            
        Returns:
            Formatted error summary
        """
        errors = self.get_past_errors(project_name)
        
        if not errors:
            return "No past errors found for this project."
        
        summary = f"# Past Errors for {project_name}\n\n"
        summary += f"Total errors: {len(errors)}\n\n"
        
        for error in errors[-10:]:  # Last 10 errors
            summary += f"## Error #{error['id']:03d}: {error['name']}\n"
            summary += f"- **Date:** {error['timestamp']}\n"
            summary += f"- **Agent:** {error['agent']}\n"
            summary += f"- **Description:** {error['description']}\n"
            summary += f"- **Solution:** {error['solution']}\n\n"
        
        return summary
    
    def get_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        return json.loads(self.stats_file.read_text(encoding='utf-8'))
    
    def __repr__(self):
        stats = self.get_stats()
        return f"ErrorTracker(total_errors={stats['total_errors']}, path='{self.base_path}')"


if __name__ == "__main__":
    # Test
    tracker = ErrorTracker()
    
    # Log a test error
    tracker.log_error({
        "name": "test_error",
        "project": "test-project",
        "agent": "test-agent",
        "description": "This is a test error",
        "solution": "Fixed by doing X",
        "severity": "low"
    })
    
    print(tracker.get_past_errors("test-project"))
    print(tracker.get_stats())

