#!/usr/bin/env python3
"""
Global Guidelines CLI
Comprehensive command-line interface for managing AI memory and guidelines
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

# Import our tools
try:
    from memory_analytics_dashboard import MemoryAnalyticsDashboard
    from memory_team_sharing import MemoryTeamSharing, ShareLevel
except ImportError:
    # Fallback for standalone execution
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from memory_analytics_dashboard import MemoryAnalyticsDashboard
    from memory_team_sharing import MemoryTeamSharing, ShareLevel

class GlobalCLI:
    """Main CLI interface for Global Guidelines."""
    
    def __init__(self, memory_dir: str = ".memory"):
        """Initialize CLI."""
        self.memory_dir = Path(memory_dir)
        self.analytics = MemoryAnalyticsDashboard(memory_dir)
        self.sharing = MemoryTeamSharing(memory_dir)
    
    def status(self):
        """Show memory system status."""
        print("🔍 Global Guidelines - System Status")
        print("=" * 80)
        
        # Check directories
        print("\n📁 Directory Structure:")
        dirs = [
            ("Memory", self.memory_dir),
            ("Conversations", self.memory_dir / "conversations"),
            ("Knowledge", self.memory_dir / "knowledge"),
            ("Preferences", self.memory_dir / "preferences"),
            ("State", self.memory_dir / "state"),
            ("Checkpoints", self.memory_dir / "checkpoints"),
            ("Vectors", self.memory_dir / "vectors"),
            ("Team Sharing", self.memory_dir / "team_sharing")
        ]
        
        for name, path in dirs:
            exists = "✅" if path.exists() else "❌"
            print(f"  {exists} {name}: {path}")
        
        # Quick stats
        print("\n📊 Quick Stats:")
        stats = self.analytics.collect_stats()
        print(f"  Conversations: {stats['conversations']['count']}")
        print(f"  Knowledge Items: {stats['knowledge']['count']}")
        print(f"  Storage: {stats['storage']['total_mb']:.2f} MB")
        print(f"  Health: {stats['health']['score']}/100 ({stats['health']['status']})")
        
        print()
    
    def analytics(self, format: str = "text", output: Optional[str] = None):
        """Generate analytics report."""
        report = self.analytics.generate_report(format)
        
        if output:
            with open(output, 'w') as f:
                f.write(report)
            print(f"✅ Report saved to: {output}")
        else:
            print(report)
    
    def trends(self, days: int = 30):
        """Show memory trends."""
        trends = self.analytics.get_trends(days)
        
        print(f"📈 Memory Trends (Last {days} days)")
        print("=" * 80)
        
        if "error" in trends:
            print(f"❌ {trends['error']}")
            return
        
        print(f"Data Points: {trends['data_points']}")
        print(f"Conversations Growth: {trends['conversations_growth']:+d}")
        print(f"Knowledge Growth: {trends['knowledge_growth']:+d}")
        print(f"Storage Growth: {trends['storage_growth_mb']:+.2f} MB")
        print()
    
    def team_create(self, name: str, description: str, user_id: str):
        """Create a new team."""
        team_id = self.sharing.create_team(name, description, user_id)
        print(f"✅ Team created successfully!")
        print(f"Team ID: {team_id}")
        print(f"Name: {name}")
        print(f"Creator: {user_id}")
    
    def team_add_member(self, team_id: str, user_id: str, role: str = "member"):
        """Add member to team."""
        success = self.sharing.add_team_member(team_id, user_id, role)
        
        if success:
            print(f"✅ Member added successfully!")
            print(f"User: {user_id}")
            print(f"Role: {role}")
        else:
            print(f"❌ Failed to add member (may already exist)")
    
    def team_stats(self, team_id: str):
        """Show team statistics."""
        stats = self.sharing.get_team_stats(team_id)
        
        if "error" in stats:
            print(f"❌ {stats['error']}")
            return
        
        print(f"👥 Team Statistics")
        print("=" * 80)
        print(f"Name: {stats['name']}")
        print(f"Description: {stats['description']}")
        print(f"Created: {stats['created_at']}")
        print(f"Created By: {stats['created_by']}")
        print(f"Members: {stats['member_count']}")
        print(f"Shared Memories: {stats['shared_memories']}")
        print(f"Recent Activity (7d): {stats['recent_activity_7d']}")
        print()
    
    def share_knowledge(
        self,
        file: str,
        owner_id: str,
        level: str,
        team_id: Optional[str] = None,
        tags: Optional[list] = None
    ):
        """Share knowledge item."""
        success = self.sharing.share_knowledge(
            Path(file),
            owner_id,
            ShareLevel(level),
            team_id=team_id,
            tags=tags
        )
        
        if success:
            print(f"✅ Knowledge shared successfully!")
            print(f"File: {file}")
            print(f"Level: {level}")
            if team_id:
                print(f"Team: {team_id}")
        else:
            print(f"❌ Failed to share knowledge")
    
    def search_knowledge(
        self,
        user_id: str,
        query: Optional[str] = None,
        tags: Optional[list] = None,
        category: Optional[str] = None,
        min_importance: int = 0
    ):
        """Search shared knowledge."""
        results = self.sharing.search_shared_knowledge(
            user_id,
            query=query,
            tags=tags,
            category=category,
            min_importance=min_importance
        )
        
        print(f"🔍 Knowledge Search Results")
        print("=" * 80)
        print(f"Found: {len(results)} items")
        print()
        
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['title']}")
            print(f"   Category: {item['category'] or 'N/A'}")
            print(f"   Importance: {item['importance']}/10")
            print(f"   Tags: {', '.join(item['tags']) if item['tags'] else 'None'}")
            print(f"   Owner: {item['owner_id']}")
            print(f"   Share Level: {item['share_level']}")
            print(f"   Updated: {item['updated_at']}")
            print()
    
    def init(self, project_name: Optional[str] = None):
        """Initialize Global Guidelines in current directory."""
        print("🚀 Initializing Global Guidelines...")
        print("=" * 80)
        
        # Create directory structure
        dirs = [
            self.memory_dir,
            self.memory_dir / "conversations",
            self.memory_dir / "knowledge",
            self.memory_dir / "preferences",
            self.memory_dir / "state",
            self.memory_dir / "checkpoints",
            self.memory_dir / "vectors",
            self.memory_dir / "team_sharing"
        ]
        
        for dir_path in dirs:
            if not dir_path.exists():
                dir_path.mkdir(parents=True)
                print(f"✅ Created: {dir_path}")
            else:
                print(f"⏭️  Exists: {dir_path}")
        
        # Create initial state
        state_file = self.memory_dir / "state" / "current_state.json"
        if not state_file.exists():
            initial_state = {
                "user_id": "default",
                "current_project": project_name or "unnamed",
                "current_phase": "initialization",
                "context": {
                    "session_count": 0,
                    "last_activity": datetime.now().isoformat(),
                    "initialized_at": datetime.now().isoformat()
                }
            }
            with open(state_file, 'w') as f:
                json.dump(initial_state, f, indent=2)
            print(f"✅ Created initial state")
        
        print("\n✅ Initialization complete!")
        print("\nNext steps:")
        print("  1. Run 'global status' to verify setup")
        print("  2. Run 'global analytics' to see initial stats")
        print("  3. Start using the memory system")
        print()

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Global Guidelines CLI - Manage AI Memory and Guidelines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize in current directory
  global init --project myproject
  
  # Show system status
  global status
  
  # Generate analytics report
  global analytics
  global analytics --format json --output report.json
  
  # Show trends
  global trends --days 30
  
  # Create team
  global team create --name "Dev Team" --user-id user123
  
  # Add team member
  global team add-member --team-id abc123 --user-id user456
  
  # Share knowledge
  global share --file knowledge.json --owner-id user123 --level team --team-id abc123
  
  # Search knowledge
  global search --user-id user123 --query "api design" --tags rest api
        """
    )
    
    parser.add_argument("--memory-dir", default=".memory", help="Memory directory path")
    parser.add_argument("--version", action="version", version="Global Guidelines CLI v7.2.0")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init
    init_parser = subparsers.add_parser("init", help="Initialize Global Guidelines")
    init_parser.add_argument("--project", help="Project name")
    
    # Status
    subparsers.add_parser("status", help="Show system status")
    
    # Analytics
    analytics_parser = subparsers.add_parser("analytics", help="Generate analytics report")
    analytics_parser.add_argument("--format", choices=["text", "json"], default="text")
    analytics_parser.add_argument("--output", help="Output file")
    
    # Trends
    trends_parser = subparsers.add_parser("trends", help="Show memory trends")
    trends_parser.add_argument("--days", type=int, default=30, help="Number of days")
    
    # Team commands
    team_parser = subparsers.add_parser("team", help="Team management")
    team_subparsers = team_parser.add_subparsers(dest="team_command")
    
    # Team create
    team_create_parser = team_subparsers.add_parser("create", help="Create team")
    team_create_parser.add_argument("--name", required=True)
    team_create_parser.add_argument("--description", default="")
    team_create_parser.add_argument("--user-id", required=True)
    
    # Team add member
    team_add_parser = team_subparsers.add_parser("add-member", help="Add team member")
    team_add_parser.add_argument("--team-id", required=True)
    team_add_parser.add_argument("--user-id", required=True)
    team_add_parser.add_argument("--role", default="member")
    
    # Team stats
    team_stats_parser = team_subparsers.add_parser("stats", help="Team statistics")
    team_stats_parser.add_argument("--team-id", required=True)
    
    # Share
    share_parser = subparsers.add_parser("share", help="Share knowledge")
    share_parser.add_argument("--file", required=True)
    share_parser.add_argument("--owner-id", required=True)
    share_parser.add_argument("--level", required=True, choices=["private", "team", "project", "public"])
    share_parser.add_argument("--team-id")
    share_parser.add_argument("--tags", nargs="+")
    
    # Search
    search_parser = subparsers.add_parser("search", help="Search knowledge")
    search_parser.add_argument("--user-id", required=True)
    search_parser.add_argument("--query")
    search_parser.add_argument("--tags", nargs="+")
    search_parser.add_argument("--category")
    search_parser.add_argument("--min-importance", type=int, default=0)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = GlobalCLI(args.memory_dir)
    
    try:
        if args.command == "init":
            cli.init(args.project)
        
        elif args.command == "status":
            cli.status()
        
        elif args.command == "analytics":
            cli.analytics(args.format, args.output)
        
        elif args.command == "trends":
            cli.trends(args.days)
        
        elif args.command == "team":
            if args.team_command == "create":
                cli.team_create(args.name, args.description, args.user_id)
            elif args.team_command == "add-member":
                cli.team_add_member(args.team_id, args.user_id, args.role)
            elif args.team_command == "stats":
                cli.team_stats(args.team_id)
            else:
                team_parser.print_help()
        
        elif args.command == "share":
            cli.share_knowledge(args.file, args.owner_id, args.level, args.team_id, args.tags)
        
        elif args.command == "search":
            cli.search_knowledge(
                args.user_id,
                query=args.query,
                tags=args.tags,
                category=args.category,
                min_importance=args.min_importance
            )
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

