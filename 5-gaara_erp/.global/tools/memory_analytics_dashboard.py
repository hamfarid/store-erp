#!/usr/bin/env python3
"""
Memory Analytics Dashboard
Provides comprehensive analytics and visualization for AI memory system
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import sqlite3

class MemoryAnalyticsDashboard:
    """Analytics dashboard for memory system."""
    
    def __init__(self, memory_dir: str = ".memory"):
        """Initialize dashboard."""
        self.memory_dir = Path(memory_dir)
        self.conversations_dir = self.memory_dir / "conversations"
        self.knowledge_dir = self.memory_dir / "knowledge"
        self.preferences_dir = self.memory_dir / "preferences"
        self.state_dir = self.memory_dir / "state"
        self.checkpoints_dir = self.memory_dir / "checkpoints"
        
        # Create analytics database
        self.db_path = self.memory_dir / "analytics.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize analytics database."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Analytics tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                total_conversations INTEGER,
                total_knowledge INTEGER,
                total_checkpoints INTEGER,
                memory_size_mb REAL,
                avg_conversation_length REAL,
                knowledge_categories TEXT,
                top_topics TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id TEXT,
                action_type TEXT,
                resource_type TEXT,
                resource_id TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                operation TEXT,
                duration_ms REAL,
                memory_used_mb REAL,
                success BOOLEAN
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def collect_stats(self) -> Dict[str, Any]:
        """Collect comprehensive memory statistics."""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "conversations": self._analyze_conversations(),
            "knowledge": self._analyze_knowledge(),
            "preferences": self._analyze_preferences(),
            "state": self._analyze_state(),
            "checkpoints": self._analyze_checkpoints(),
            "storage": self._analyze_storage(),
            "patterns": self._analyze_patterns(),
            "health": self._analyze_health()
        }
        
        # Save to database
        self._save_stats(stats)
        
        return stats
    
    def _analyze_conversations(self) -> Dict[str, Any]:
        """Analyze conversation data."""
        if not self.conversations_dir.exists():
            return {"count": 0, "total_messages": 0}
        
        conversations = list(self.conversations_dir.glob("*.json"))
        total_messages = 0
        users = set()
        topics = []
        lengths = []
        
        for conv_file in conversations:
            try:
                with open(conv_file, 'r') as f:
                    conv = json.load(f)
                    messages = conv.get("messages", [])
                    total_messages += len(messages)
                    lengths.append(len(messages))
                    
                    if "user_id" in conv:
                        users.add(conv["user_id"])
                    
                    if "topics" in conv:
                        topics.extend(conv["topics"])
            except:
                continue
        
        return {
            "count": len(conversations),
            "total_messages": total_messages,
            "avg_length": sum(lengths) / len(lengths) if lengths else 0,
            "unique_users": len(users),
            "top_topics": Counter(topics).most_common(10) if topics else []
        }
    
    def _analyze_knowledge(self) -> Dict[str, Any]:
        """Analyze knowledge base."""
        if not self.knowledge_dir.exists():
            return {"count": 0}
        
        knowledge_items = list(self.knowledge_dir.glob("*.json"))
        categories = []
        importance_scores = []
        types = []
        
        for know_file in knowledge_items:
            try:
                with open(know_file, 'r') as f:
                    know = json.load(f)
                    
                    if "type" in know:
                        types.append(know["type"])
                    
                    if "importance" in know:
                        importance_scores.append(know["importance"])
                    
                    if "metadata" in know and "category" in know["metadata"]:
                        categories.append(know["metadata"]["category"])
            except:
                continue
        
        return {
            "count": len(knowledge_items),
            "types": dict(Counter(types)),
            "categories": dict(Counter(categories)),
            "avg_importance": sum(importance_scores) / len(importance_scores) if importance_scores else 0,
            "high_importance_count": sum(1 for s in importance_scores if s >= 8)
        }
    
    def _analyze_preferences(self) -> Dict[str, Any]:
        """Analyze user preferences."""
        if not self.preferences_dir.exists():
            return {"count": 0}
        
        pref_files = list(self.preferences_dir.glob("*.json"))
        users = []
        projects = []
        
        for pref_file in pref_files:
            try:
                with open(pref_file, 'r') as f:
                    pref = json.load(f)
                    
                    if "user_id" in pref:
                        users.append(pref["user_id"])
                    
                    if "project" in pref:
                        projects.append(pref["project"])
            except:
                continue
        
        return {
            "count": len(pref_files),
            "unique_users": len(set(users)),
            "projects": list(set(projects))
        }
    
    def _analyze_state(self) -> Dict[str, Any]:
        """Analyze current state."""
        state_file = self.state_dir / "current_state.json"
        
        if not state_file.exists():
            return {"exists": False}
        
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
            
            return {
                "exists": True,
                "user_id": state.get("user_id"),
                "current_project": state.get("current_project"),
                "current_phase": state.get("current_phase"),
                "last_activity": state.get("context", {}).get("last_activity"),
                "session_count": state.get("context", {}).get("session_count", 0)
            }
        except:
            return {"exists": False, "error": "Failed to read state"}
    
    def _analyze_checkpoints(self) -> Dict[str, Any]:
        """Analyze checkpoints."""
        if not self.checkpoints_dir.exists():
            return {"count": 0}
        
        checkpoints = list(self.checkpoints_dir.glob("*.json"))
        
        return {
            "count": len(checkpoints),
            "latest": max([cp.stat().st_mtime for cp in checkpoints]) if checkpoints else None
        }
    
    def _analyze_storage(self) -> Dict[str, Any]:
        """Analyze storage usage."""
        def get_dir_size(path: Path) -> int:
            """Get directory size in bytes."""
            total = 0
            if path.exists():
                for item in path.rglob('*'):
                    if item.is_file():
                        total += item.stat().st_size
            return total
        
        conversations_size = get_dir_size(self.conversations_dir)
        knowledge_size = get_dir_size(self.knowledge_dir)
        checkpoints_size = get_dir_size(self.checkpoints_dir)
        total_size = conversations_size + knowledge_size + checkpoints_size
        
        return {
            "total_mb": total_size / (1024 * 1024),
            "conversations_mb": conversations_size / (1024 * 1024),
            "knowledge_mb": knowledge_size / (1024 * 1024),
            "checkpoints_mb": checkpoints_size / (1024 * 1024)
        }
    
    def _analyze_patterns(self) -> Dict[str, Any]:
        """Analyze usage patterns."""
        # This would analyze patterns from usage_patterns table
        # For now, return placeholder
        return {
            "most_active_hours": [],
            "most_active_days": [],
            "common_workflows": []
        }
    
    def _analyze_health(self) -> Dict[str, Any]:
        """Analyze memory system health."""
        health_score = 100
        issues = []
        warnings = []
        
        # Check directory structure
        required_dirs = [
            self.conversations_dir,
            self.knowledge_dir,
            self.preferences_dir,
            self.state_dir,
            self.checkpoints_dir
        ]
        
        for dir_path in required_dirs:
            if not dir_path.exists():
                health_score -= 10
                issues.append(f"Missing directory: {dir_path.name}")
        
        # Check state file
        state_file = self.state_dir / "current_state.json"
        if not state_file.exists():
            health_score -= 5
            warnings.append("No current state file")
        
        # Check for old data
        if self.conversations_dir.exists():
            old_convs = [
                f for f in self.conversations_dir.glob("*.json")
                if (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days > 90
            ]
            if len(old_convs) > 10:
                warnings.append(f"{len(old_convs)} conversations older than 90 days")
        
        # Determine status
        if health_score >= 90:
            status = "excellent"
        elif health_score >= 75:
            status = "good"
        elif health_score >= 50:
            status = "fair"
        else:
            status = "poor"
        
        return {
            "score": health_score,
            "status": status,
            "issues": issues,
            "warnings": warnings
        }
    
    def _save_stats(self, stats: Dict[str, Any]):
        """Save statistics to database."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memory_stats (
                timestamp,
                total_conversations,
                total_knowledge,
                total_checkpoints,
                memory_size_mb,
                avg_conversation_length,
                knowledge_categories,
                top_topics
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            stats["timestamp"],
            stats["conversations"]["count"],
            stats["knowledge"]["count"],
            stats["checkpoints"]["count"],
            stats["storage"]["total_mb"],
            stats["conversations"].get("avg_length", 0),
            json.dumps(stats["knowledge"].get("categories", {})),
            json.dumps(stats["conversations"].get("top_topics", []))
        ))
        
        conn.commit()
        conn.close()
    
    def generate_report(self, format: str = "text") -> str:
        """Generate analytics report."""
        stats = self.collect_stats()
        
        if format == "json":
            return json.dumps(stats, indent=2)
        
        # Text format
        report = []
        report.append("=" * 80)
        report.append("MEMORY ANALYTICS DASHBOARD")
        report.append("=" * 80)
        report.append(f"Generated: {stats['timestamp']}")
        report.append("")
        
        # Conversations
        report.append("📊 CONVERSATIONS")
        report.append("-" * 80)
        conv = stats["conversations"]
        report.append(f"Total Conversations: {conv['count']}")
        report.append(f"Total Messages: {conv['total_messages']}")
        report.append(f"Average Length: {conv['avg_length']:.1f} messages")
        report.append(f"Unique Users: {conv['unique_users']}")
        if conv.get("top_topics"):
            report.append("\nTop Topics:")
            for topic, count in conv["top_topics"][:5]:
                report.append(f"  - {topic}: {count}")
        report.append("")
        
        # Knowledge
        report.append("🧠 KNOWLEDGE BASE")
        report.append("-" * 80)
        know = stats["knowledge"]
        report.append(f"Total Items: {know['count']}")
        report.append(f"Average Importance: {know['avg_importance']:.1f}/10")
        report.append(f"High Importance Items: {know['high_importance_count']}")
        if know.get("types"):
            report.append("\nTypes:")
            for type_name, count in know["types"].items():
                report.append(f"  - {type_name}: {count}")
        if know.get("categories"):
            report.append("\nCategories:")
            for cat, count in list(know["categories"].items())[:5]:
                report.append(f"  - {cat}: {count}")
        report.append("")
        
        # Storage
        report.append("💾 STORAGE")
        report.append("-" * 80)
        storage = stats["storage"]
        report.append(f"Total Size: {storage['total_mb']:.2f} MB")
        report.append(f"  - Conversations: {storage['conversations_mb']:.2f} MB")
        report.append(f"  - Knowledge: {storage['knowledge_mb']:.2f} MB")
        report.append(f"  - Checkpoints: {storage['checkpoints_mb']:.2f} MB")
        report.append("")
        
        # Health
        report.append("❤️  SYSTEM HEALTH")
        report.append("-" * 80)
        health = stats["health"]
        report.append(f"Health Score: {health['score']}/100 ({health['status'].upper()})")
        if health["issues"]:
            report.append("\nIssues:")
            for issue in health["issues"]:
                report.append(f"  ❌ {issue}")
        if health["warnings"]:
            report.append("\nWarnings:")
            for warning in health["warnings"]:
                report.append(f"  ⚠️  {warning}")
        report.append("")
        
        # State
        report.append("🔄 CURRENT STATE")
        report.append("-" * 80)
        state = stats["state"]
        if state.get("exists"):
            report.append(f"User: {state.get('user_id', 'N/A')}")
            report.append(f"Project: {state.get('current_project', 'N/A')}")
            report.append(f"Phase: {state.get('current_phase', 'N/A')}")
            report.append(f"Last Activity: {state.get('last_activity', 'N/A')}")
            report.append(f"Session Count: {state.get('session_count', 0)}")
        else:
            report.append("No active state")
        report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def get_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get trends over time."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT 
                timestamp,
                total_conversations,
                total_knowledge,
                memory_size_mb
            FROM memory_stats
            WHERE timestamp >= ?
            ORDER BY timestamp
        ''', (since,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return {"error": "No data available"}
        
        return {
            "period_days": days,
            "data_points": len(rows),
            "conversations_growth": rows[-1][1] - rows[0][1] if len(rows) > 1 else 0,
            "knowledge_growth": rows[-1][2] - rows[0][2] if len(rows) > 1 else 0,
            "storage_growth_mb": rows[-1][3] - rows[0][3] if len(rows) > 1 else 0
        }

def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Analytics Dashboard")
    parser.add_argument("--memory-dir", default=".memory", help="Memory directory path")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--trends", type=int, metavar="DAYS", help="Show trends for N days")
    parser.add_argument("--output", help="Output file (default: stdout)")
    
    args = parser.parse_args()
    
    dashboard = MemoryAnalyticsDashboard(args.memory_dir)
    
    if args.trends:
        trends = dashboard.get_trends(args.trends)
        output = json.dumps(trends, indent=2)
    else:
        output = dashboard.generate_report(args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Report saved to: {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()

