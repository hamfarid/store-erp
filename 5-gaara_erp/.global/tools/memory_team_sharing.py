#!/usr/bin/env python3
"""
Memory Team Sharing System
Enables secure sharing and collaboration on AI memory across team members
"""

import json
import os
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum

class ShareLevel(Enum):
    """Memory sharing permission levels."""
    PRIVATE = "private"  # Only owner
    TEAM = "team"  # Team members
    PROJECT = "project"  # Project members
    PUBLIC = "public"  # Everyone

class MemoryTeamSharing:
    """Team sharing system for memory."""
    
    def __init__(self, memory_dir: str = ".memory"):
        """Initialize team sharing system."""
        self.memory_dir = Path(memory_dir)
        self.sharing_dir = self.memory_dir / "team_sharing"
        self.sharing_dir.mkdir(exist_ok=True)
        
        # Create sharing database
        self.db_path = self.sharing_dir / "sharing.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize sharing database."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                created_by TEXT NOT NULL
            )
        ''')
        
        # Team members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                joined_at TEXT NOT NULL,
                FOREIGN KEY (team_id) REFERENCES teams(id),
                UNIQUE(team_id, user_id)
            )
        ''')
        
        # Shared memory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shared_memory (
                id TEXT PRIMARY KEY,
                memory_type TEXT NOT NULL,
                memory_id TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                share_level TEXT NOT NULL,
                team_id TEXT,
                project_id TEXT,
                shared_at TEXT NOT NULL,
                metadata TEXT,
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        ''')
        
        # Access log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        # Shared knowledge index
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shared_knowledge_index (
                id TEXT PRIMARY KEY,
                title TEXT,
                content_hash TEXT,
                tags TEXT,
                category TEXT,
                importance INTEGER,
                owner_id TEXT,
                share_level TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_team(self, name: str, description: str, created_by: str) -> str:
        """Create a new team."""
        team_id = hashlib.md5(f"{name}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO teams (id, name, description, created_at, created_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (team_id, name, description, datetime.now().isoformat(), created_by))
        
        # Add creator as admin
        cursor.execute('''
            INSERT INTO team_members (team_id, user_id, role, joined_at)
            VALUES (?, ?, ?, ?)
        ''', (team_id, created_by, "admin", datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return team_id
    
    def add_team_member(self, team_id: str, user_id: str, role: str = "member") -> bool:
        """Add a member to a team."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO team_members (team_id, user_id, role, joined_at)
                VALUES (?, ?, ?, ?)
            ''', (team_id, user_id, role, datetime.now().isoformat()))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Already a member
        finally:
            conn.close()
    
    def share_memory(
        self,
        memory_type: str,
        memory_id: str,
        owner_id: str,
        share_level: ShareLevel,
        team_id: Optional[str] = None,
        project_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """Share a memory item."""
        share_id = hashlib.md5(
            f"{memory_type}_{memory_id}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO shared_memory (
                id, memory_type, memory_id, owner_id, share_level,
                team_id, project_id, shared_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            share_id,
            memory_type,
            memory_id,
            owner_id,
            share_level.value,
            team_id,
            project_id,
            datetime.now().isoformat(),
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
        
        # Log the sharing action
        self._log_access(memory_id, owner_id, "share", {
            "share_level": share_level.value,
            "team_id": team_id,
            "project_id": project_id
        })
        
        return share_id
    
    def get_shared_memories(
        self,
        user_id: str,
        memory_type: Optional[str] = None,
        team_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get memories shared with a user."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get user's teams
        cursor.execute('''
            SELECT team_id FROM team_members WHERE user_id = ?
        ''', (user_id,))
        user_teams = [row[0] for row in cursor.fetchall()]
        
        # Build query
        query = '''
            SELECT 
                sm.id, sm.memory_type, sm.memory_id, sm.owner_id,
                sm.share_level, sm.team_id, sm.project_id, sm.shared_at, sm.metadata
            FROM shared_memory sm
            WHERE (
                sm.owner_id = ?
                OR sm.share_level = 'public'
                OR (sm.share_level = 'team' AND sm.team_id IN ({}))
            )
        '''.format(','.join('?' * len(user_teams)))
        
        params = [user_id] + user_teams
        
        if memory_type:
            query += " AND sm.memory_type = ?"
            params.append(memory_type)
        
        if team_id:
            query += " AND sm.team_id = ?"
            params.append(team_id)
        
        query += " ORDER BY sm.shared_at DESC"
        
        cursor.execute(query, params)
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                "id": row[0],
                "memory_type": row[1],
                "memory_id": row[2],
                "owner_id": row[3],
                "share_level": row[4],
                "team_id": row[5],
                "project_id": row[6],
                "shared_at": row[7],
                "metadata": json.loads(row[8]) if row[8] else None
            })
        
        conn.close()
        
        # Log access
        for memory in memories:
            self._log_access(memory["memory_id"], user_id, "view", None)
        
        return memories
    
    def share_knowledge(
        self,
        knowledge_file: Path,
        owner_id: str,
        share_level: ShareLevel,
        team_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """Share a knowledge item with indexing."""
        try:
            with open(knowledge_file, 'r') as f:
                knowledge = json.load(f)
            
            # Calculate content hash
            content_hash = hashlib.md5(
                json.dumps(knowledge, sort_keys=True).encode()
            ).hexdigest()
            
            # Index the knowledge
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO shared_knowledge_index (
                    id, title, content_hash, tags, category, importance,
                    owner_id, share_level, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                knowledge.get("id"),
                knowledge.get("content", "")[:100],  # First 100 chars as title
                content_hash,
                json.dumps(tags) if tags else None,
                knowledge.get("metadata", {}).get("category"),
                knowledge.get("importance", 5),
                owner_id,
                share_level.value,
                knowledge.get("created_at", datetime.now().isoformat()),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
            # Share the memory
            self.share_memory(
                "knowledge",
                knowledge.get("id"),
                owner_id,
                share_level,
                team_id=team_id,
                metadata={"tags": tags}
            )
            
            return True
        except Exception as e:
            print(f"Error sharing knowledge: {e}")
            return False
    
    def search_shared_knowledge(
        self,
        user_id: str,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        min_importance: int = 0
    ) -> List[Dict[str, Any]]:
        """Search shared knowledge base."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Get user's teams
        cursor.execute('''
            SELECT team_id FROM team_members WHERE user_id = ?
        ''', (user_id,))
        user_teams = [row[0] for row in cursor.fetchall()]
        
        # Build search query
        sql = '''
            SELECT 
                ski.id, ski.title, ski.tags, ski.category, ski.importance,
                ski.owner_id, ski.share_level, ski.updated_at
            FROM shared_knowledge_index ski
            LEFT JOIN shared_memory sm ON ski.id = sm.memory_id
            WHERE (
                ski.owner_id = ?
                OR ski.share_level = 'public'
                OR (ski.share_level = 'team' AND sm.team_id IN ({}))
            )
            AND ski.importance >= ?
        '''.format(','.join('?' * len(user_teams)))
        
        params = [user_id] + user_teams + [min_importance]
        
        if category:
            sql += " AND ski.category = ?"
            params.append(category)
        
        if tags:
            # Simple tag matching (can be improved with full-text search)
            for tag in tags:
                sql += " AND ski.tags LIKE ?"
                params.append(f'%"{tag}"%')
        
        if query:
            sql += " AND ski.title LIKE ?"
            params.append(f"%{query}%")
        
        sql += " ORDER BY ski.importance DESC, ski.updated_at DESC"
        
        cursor.execute(sql, params)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "title": row[1],
                "tags": json.loads(row[2]) if row[2] else [],
                "category": row[3],
                "importance": row[4],
                "owner_id": row[5],
                "share_level": row[6],
                "updated_at": row[7]
            })
        
        conn.close()
        return results
    
    def _log_access(
        self,
        memory_id: str,
        user_id: str,
        action: str,
        metadata: Optional[Dict] = None
    ):
        """Log memory access."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO access_log (memory_id, user_id, action, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            memory_id,
            user_id,
            action,
            datetime.now().isoformat(),
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_team_stats(self, team_id: str) -> Dict[str, Any]:
        """Get team statistics."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Team info
        cursor.execute('''
            SELECT name, description, created_at, created_by
            FROM teams WHERE id = ?
        ''', (team_id,))
        team_row = cursor.fetchone()
        
        if not team_row:
            conn.close()
            return {"error": "Team not found"}
        
        # Member count
        cursor.execute('''
            SELECT COUNT(*) FROM team_members WHERE team_id = ?
        ''', (team_id,))
        member_count = cursor.fetchone()[0]
        
        # Shared memories count
        cursor.execute('''
            SELECT COUNT(*) FROM shared_memory WHERE team_id = ?
        ''', (team_id,))
        shared_count = cursor.fetchone()[0]
        
        # Recent activity
        cursor.execute('''
            SELECT COUNT(*) FROM access_log al
            JOIN shared_memory sm ON al.memory_id = sm.memory_id
            WHERE sm.team_id = ?
            AND datetime(al.timestamp) >= datetime('now', '-7 days')
        ''', (team_id,))
        recent_activity = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "team_id": team_id,
            "name": team_row[0],
            "description": team_row[1],
            "created_at": team_row[2],
            "created_by": team_row[3],
            "member_count": member_count,
            "shared_memories": shared_count,
            "recent_activity_7d": recent_activity
        }

def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Team Sharing System")
    parser.add_argument("--memory-dir", default=".memory", help="Memory directory path")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create team
    create_team_parser = subparsers.add_parser("create-team", help="Create a new team")
    create_team_parser.add_argument("--name", required=True, help="Team name")
    create_team_parser.add_argument("--description", help="Team description")
    create_team_parser.add_argument("--user-id", required=True, help="Creator user ID")
    
    # Add member
    add_member_parser = subparsers.add_parser("add-member", help="Add team member")
    add_member_parser.add_argument("--team-id", required=True, help="Team ID")
    add_member_parser.add_argument("--user-id", required=True, help="User ID")
    add_member_parser.add_argument("--role", default="member", help="Member role")
    
    # Share knowledge
    share_parser = subparsers.add_parser("share-knowledge", help="Share knowledge")
    share_parser.add_argument("--file", required=True, help="Knowledge file path")
    share_parser.add_argument("--owner-id", required=True, help="Owner user ID")
    share_parser.add_argument("--level", required=True, choices=["private", "team", "project", "public"])
    share_parser.add_argument("--team-id", help="Team ID (for team level)")
    share_parser.add_argument("--tags", nargs="+", help="Tags")
    
    # Search
    search_parser = subparsers.add_parser("search", help="Search shared knowledge")
    search_parser.add_argument("--user-id", required=True, help="User ID")
    search_parser.add_argument("--query", help="Search query")
    search_parser.add_argument("--tags", nargs="+", help="Tags")
    search_parser.add_argument("--category", help="Category")
    search_parser.add_argument("--min-importance", type=int, default=0, help="Minimum importance")
    
    # Team stats
    stats_parser = subparsers.add_parser("team-stats", help="Get team statistics")
    stats_parser.add_argument("--team-id", required=True, help="Team ID")
    
    args = parser.parse_args()
    
    sharing = MemoryTeamSharing(args.memory_dir)
    
    if args.command == "create-team":
        team_id = sharing.create_team(args.name, args.description or "", args.user_id)
        print(f"Team created: {team_id}")
    
    elif args.command == "add-member":
        success = sharing.add_team_member(args.team_id, args.user_id, args.role)
        print("Member added" if success else "Failed to add member")
    
    elif args.command == "share-knowledge":
        success = sharing.share_knowledge(
            Path(args.file),
            args.owner_id,
            ShareLevel(args.level),
            team_id=args.team_id,
            tags=args.tags
        )
        print("Knowledge shared" if success else "Failed to share knowledge")
    
    elif args.command == "search":
        results = sharing.search_shared_knowledge(
            args.user_id,
            query=args.query,
            tags=args.tags,
            category=args.category,
            min_importance=args.min_importance
        )
        print(json.dumps(results, indent=2))
    
    elif args.command == "team-stats":
        stats = sharing.get_team_stats(args.team_id)
        print(json.dumps(stats, indent=2))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

