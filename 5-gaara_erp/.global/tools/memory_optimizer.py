#!/usr/bin/env python3
"""
Memory Optimizer
Tools for optimizing, cleaning, and maintaining AI memory system
"""

import json
import os
import shutil
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

class MemoryOptimizer:
    """Memory optimization and maintenance tools."""
    
    def __init__(self, memory_dir: str = ".memory"):
        """Initialize optimizer."""
        self.memory_dir = Path(memory_dir)
        self.conversations_dir = self.memory_dir / "conversations"
        self.knowledge_dir = self.memory_dir / "knowledge"
        self.checkpoints_dir = self.memory_dir / "checkpoints"
        self.backup_dir = self.memory_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze memory for optimization opportunities."""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "conversations": self._analyze_conversations(),
            "knowledge": self._analyze_knowledge(),
            "checkpoints": self._analyze_checkpoints(),
            "duplicates": self._find_duplicates(),
            "recommendations": []
        }
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _analyze_conversations(self) -> Dict[str, Any]:
        """Analyze conversations for optimization."""
        if not self.conversations_dir.exists():
            return {"count": 0}
        
        conversations = list(self.conversations_dir.glob("*.json"))
        now = datetime.now()
        
        old_convs = []
        empty_convs = []
        large_convs = []
        
        for conv_file in conversations:
            try:
                # Check age
                age_days = (now - datetime.fromtimestamp(conv_file.stat().st_mtime)).days
                if age_days > 90:
                    old_convs.append((conv_file, age_days))
                
                # Check size
                size_mb = conv_file.stat().st_size / (1024 * 1024)
                if size_mb > 5:
                    large_convs.append((conv_file, size_mb))
                
                # Check content
                with open(conv_file, 'r') as f:
                    conv = json.load(f)
                    if not conv.get("messages") or len(conv.get("messages", [])) == 0:
                        empty_convs.append(conv_file)
            except:
                continue
        
        return {
            "count": len(conversations),
            "old_conversations": len(old_convs),
            "empty_conversations": len(empty_convs),
            "large_conversations": len(large_convs),
            "old_list": old_convs[:10],  # Top 10
            "empty_list": empty_convs[:10],
            "large_list": large_convs[:10]
        }
    
    def _analyze_knowledge(self) -> Dict[str, Any]:
        """Analyze knowledge base for optimization."""
        if not self.knowledge_dir.exists():
            return {"count": 0}
        
        knowledge_items = list(self.knowledge_dir.glob("*.json"))
        
        low_importance = []
        outdated = []
        
        for know_file in knowledge_items:
            try:
                with open(know_file, 'r') as f:
                    know = json.load(f)
                    
                    # Check importance
                    if know.get("importance", 10) < 3:
                        low_importance.append(know_file)
                    
                    # Check if outdated
                    if "metadata" in know and "expires_at" in know["metadata"]:
                        expires = datetime.fromisoformat(know["metadata"]["expires_at"])
                        if expires < datetime.now():
                            outdated.append(know_file)
            except:
                continue
        
        return {
            "count": len(knowledge_items),
            "low_importance": len(low_importance),
            "outdated": len(outdated),
            "low_importance_list": low_importance[:10],
            "outdated_list": outdated[:10]
        }
    
    def _analyze_checkpoints(self) -> Dict[str, Any]:
        """Analyze checkpoints for optimization."""
        if not self.checkpoints_dir.exists():
            return {"count": 0}
        
        checkpoints = list(self.checkpoints_dir.glob("*.json"))
        
        # Keep only last N checkpoints
        if len(checkpoints) > 10:
            checkpoints_sorted = sorted(checkpoints, key=lambda x: x.stat().st_mtime, reverse=True)
            old_checkpoints = checkpoints_sorted[10:]
        else:
            old_checkpoints = []
        
        return {
            "count": len(checkpoints),
            "old_checkpoints": len(old_checkpoints),
            "old_list": old_checkpoints[:10]
        }
    
    def _find_duplicates(self) -> Dict[str, Any]:
        """Find duplicate content."""
        duplicates = {
            "conversations": [],
            "knowledge": []
        }
        
        # Find duplicate conversations
        if self.conversations_dir.exists():
            conv_hashes = defaultdict(list)
            for conv_file in self.conversations_dir.glob("*.json"):
                try:
                    with open(conv_file, 'r') as f:
                        content = f.read()
                        content_hash = hashlib.md5(content.encode()).hexdigest()
                        conv_hashes[content_hash].append(conv_file)
                except:
                    continue
            
            for hash_val, files in conv_hashes.items():
                if len(files) > 1:
                    duplicates["conversations"].append({
                        "hash": hash_val,
                        "files": [str(f) for f in files]
                    })
        
        # Find duplicate knowledge
        if self.knowledge_dir.exists():
            know_hashes = defaultdict(list)
            for know_file in self.knowledge_dir.glob("*.json"):
                try:
                    with open(know_file, 'r') as f:
                        content = f.read()
                        content_hash = hashlib.md5(content.encode()).hexdigest()
                        know_hashes[content_hash].append(know_file)
                except:
                    continue
            
            for hash_val, files in know_hashes.items():
                if len(files) > 1:
                    duplicates["knowledge"].append({
                        "hash": hash_val,
                        "files": [str(f) for f in files]
                    })
        
        return {
            "conversation_groups": len(duplicates["conversations"]),
            "knowledge_groups": len(duplicates["knowledge"]),
            "details": duplicates
        }
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        # Conversations
        conv = analysis["conversations"]
        if conv.get("old_conversations", 0) > 10:
            recommendations.append(
                f"Archive {conv['old_conversations']} old conversations (>90 days)"
            )
        if conv.get("empty_conversations", 0) > 0:
            recommendations.append(
                f"Remove {conv['empty_conversations']} empty conversations"
            )
        if conv.get("large_conversations", 0) > 0:
            recommendations.append(
                f"Compress {conv['large_conversations']} large conversations (>5MB)"
            )
        
        # Knowledge
        know = analysis["knowledge"]
        if know.get("low_importance", 0) > 5:
            recommendations.append(
                f"Review {know['low_importance']} low-importance knowledge items"
            )
        if know.get("outdated", 0) > 0:
            recommendations.append(
                f"Remove {know['outdated']} outdated knowledge items"
            )
        
        # Checkpoints
        cp = analysis["checkpoints"]
        if cp.get("old_checkpoints", 0) > 0:
            recommendations.append(
                f"Clean up {cp['old_checkpoints']} old checkpoints (keep last 10)"
            )
        
        # Duplicates
        dup = analysis["duplicates"]
        if dup.get("conversation_groups", 0) > 0:
            recommendations.append(
                f"Remove {dup['conversation_groups']} duplicate conversation groups"
            )
        if dup.get("knowledge_groups", 0) > 0:
            recommendations.append(
                f"Remove {dup['knowledge_groups']} duplicate knowledge groups"
            )
        
        if not recommendations:
            recommendations.append("Memory is well-optimized. No actions needed.")
        
        return recommendations
    
    def backup(self, name: Optional[str] = None) -> Path:
        """Create a backup of memory."""
        if not name:
            name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = self.backup_dir / name
        backup_path.mkdir(exist_ok=True)
        
        # Backup directories
        dirs_to_backup = [
            ("conversations", self.conversations_dir),
            ("knowledge", self.knowledge_dir),
            ("preferences", self.memory_dir / "preferences"),
            ("state", self.memory_dir / "state"),
            ("checkpoints", self.checkpoints_dir)
        ]
        
        for dir_name, dir_path in dirs_to_backup:
            if dir_path.exists():
                shutil.copytree(dir_path, backup_path / dir_name, dirs_exist_ok=True)
        
        # Create backup manifest
        manifest = {
            "created_at": datetime.now().isoformat(),
            "directories": [d[0] for d in dirs_to_backup if d[1].exists()],
            "total_size_mb": sum(
                sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                for _, dir_path in dirs_to_backup if dir_path.exists()
            ) / (1024 * 1024)
        }
        
        with open(backup_path / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        return backup_path
    
    def clean_old_conversations(self, days: int = 90, dry_run: bool = True) -> Tuple[int, List[Path]]:
        """Clean old conversations."""
        if not self.conversations_dir.exists():
            return 0, []
        
        now = datetime.now()
        old_convs = []
        
        for conv_file in self.conversations_dir.glob("*.json"):
            age_days = (now - datetime.fromtimestamp(conv_file.stat().st_mtime)).days
            if age_days > days:
                old_convs.append(conv_file)
        
        if not dry_run:
            # Create backup first
            self.backup(f"before_clean_old_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Archive to a separate directory
            archive_dir = self.memory_dir / "archived_conversations"
            archive_dir.mkdir(exist_ok=True)
            
            for conv_file in old_convs:
                shutil.move(str(conv_file), str(archive_dir / conv_file.name))
        
        return len(old_convs), old_convs
    
    def remove_empty_conversations(self, dry_run: bool = True) -> Tuple[int, List[Path]]:
        """Remove empty conversations."""
        if not self.conversations_dir.exists():
            return 0, []
        
        empty_convs = []
        
        for conv_file in self.conversations_dir.glob("*.json"):
            try:
                with open(conv_file, 'r') as f:
                    conv = json.load(f)
                    if not conv.get("messages") or len(conv.get("messages", [])) == 0:
                        empty_convs.append(conv_file)
            except:
                continue
        
        if not dry_run:
            # Create backup first
            self.backup(f"before_remove_empty_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            for conv_file in empty_convs:
                conv_file.unlink()
        
        return len(empty_convs), empty_convs
    
    def remove_duplicates(self, dry_run: bool = True) -> Dict[str, int]:
        """Remove duplicate content."""
        analysis = self._find_duplicates()
        removed = {"conversations": 0, "knowledge": 0}
        
        if not dry_run:
            # Create backup first
            self.backup(f"before_dedup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Remove duplicate conversations (keep first)
            for dup_group in analysis["details"]["conversations"]:
                files = [Path(f) for f in dup_group["files"]]
                for file_to_remove in files[1:]:  # Keep first, remove rest
                    if file_to_remove.exists():
                        file_to_remove.unlink()
                        removed["conversations"] += 1
            
            # Remove duplicate knowledge (keep first)
            for dup_group in analysis["details"]["knowledge"]:
                files = [Path(f) for f in dup_group["files"]]
                for file_to_remove in files[1:]:
                    if file_to_remove.exists():
                        file_to_remove.unlink()
                        removed["knowledge"] += 1
        else:
            # Dry run - count what would be removed
            for dup_group in analysis["details"]["conversations"]:
                removed["conversations"] += len(dup_group["files"]) - 1
            for dup_group in analysis["details"]["knowledge"]:
                removed["knowledge"] += len(dup_group["files"]) - 1
        
        return removed
    
    def clean_old_checkpoints(self, keep: int = 10, dry_run: bool = True) -> Tuple[int, List[Path]]:
        """Clean old checkpoints, keeping only the most recent ones."""
        if not self.checkpoints_dir.exists():
            return 0, []
        
        checkpoints = list(self.checkpoints_dir.glob("*.json"))
        checkpoints_sorted = sorted(checkpoints, key=lambda x: x.stat().st_mtime, reverse=True)
        
        old_checkpoints = checkpoints_sorted[keep:]
        
        if not dry_run and old_checkpoints:
            # Create backup first
            self.backup(f"before_clean_cp_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            for cp_file in old_checkpoints:
                cp_file.unlink()
        
        return len(old_checkpoints), old_checkpoints
    
    def optimize_all(self, dry_run: bool = True) -> Dict[str, Any]:
        """Run all optimization tasks."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "actions": {}
        }
        
        # Backup first if not dry run
        if not dry_run:
            backup_path = self.backup(f"before_optimize_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            results["backup"] = str(backup_path)
        
        # Clean old conversations
        count, _ = self.clean_old_conversations(90, dry_run)
        results["actions"]["old_conversations_cleaned"] = count
        
        # Remove empty conversations
        count, _ = self.remove_empty_conversations(dry_run)
        results["actions"]["empty_conversations_removed"] = count
        
        # Remove duplicates
        removed = self.remove_duplicates(dry_run)
        results["actions"]["duplicates_removed"] = removed
        
        # Clean old checkpoints
        count, _ = self.clean_old_checkpoints(10, dry_run)
        results["actions"]["old_checkpoints_cleaned"] = count
        
        return results

def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Optimizer")
    parser.add_argument("--memory-dir", default=".memory", help="Memory directory path")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Analyze
    subparsers.add_parser("analyze", help="Analyze memory for optimization")
    
    # Backup
    backup_parser = subparsers.add_parser("backup", help="Create backup")
    backup_parser.add_argument("--name", help="Backup name")
    
    # Clean old
    clean_old_parser = subparsers.add_parser("clean-old", help="Clean old conversations")
    clean_old_parser.add_argument("--days", type=int, default=90, help="Days threshold")
    clean_old_parser.add_argument("--no-dry-run", action="store_true", help="Actually perform cleanup")
    
    # Remove empty
    remove_empty_parser = subparsers.add_parser("remove-empty", help="Remove empty conversations")
    remove_empty_parser.add_argument("--no-dry-run", action="store_true", help="Actually perform cleanup")
    
    # Remove duplicates
    dedup_parser = subparsers.add_parser("remove-duplicates", help="Remove duplicates")
    dedup_parser.add_argument("--no-dry-run", action="store_true", help="Actually perform cleanup")
    
    # Clean checkpoints
    clean_cp_parser = subparsers.add_parser("clean-checkpoints", help="Clean old checkpoints")
    clean_cp_parser.add_argument("--keep", type=int, default=10, help="Number to keep")
    clean_cp_parser.add_argument("--no-dry-run", action="store_true", help="Actually perform cleanup")
    
    # Optimize all
    optimize_parser = subparsers.add_parser("optimize", help="Run all optimizations")
    optimize_parser.add_argument("--no-dry-run", action="store_true", help="Actually perform cleanup")
    
    args = parser.parse_args()
    
    optimizer = MemoryOptimizer(args.memory_dir)
    
    if args.command == "analyze":
        analysis = optimizer.analyze()
        print(json.dumps(analysis, indent=2))
    
    elif args.command == "backup":
        backup_path = optimizer.backup(args.name)
        print(f"✅ Backup created: {backup_path}")
    
    elif args.command == "clean-old":
        count, files = optimizer.clean_old_conversations(args.days, not args.no_dry_run)
        if args.no_dry_run:
            print(f"✅ Archived {count} old conversations")
        else:
            print(f"Would archive {count} old conversations (use --no-dry-run to execute)")
    
    elif args.command == "remove-empty":
        count, files = optimizer.remove_empty_conversations(not args.no_dry_run)
        if args.no_dry_run:
            print(f"✅ Removed {count} empty conversations")
        else:
            print(f"Would remove {count} empty conversations (use --no-dry-run to execute)")
    
    elif args.command == "remove-duplicates":
        removed = optimizer.remove_duplicates(not args.no_dry_run)
        if args.no_dry_run:
            print(f"✅ Removed duplicates:")
            print(f"  Conversations: {removed['conversations']}")
            print(f"  Knowledge: {removed['knowledge']}")
        else:
            print(f"Would remove duplicates:")
            print(f"  Conversations: {removed['conversations']}")
            print(f"  Knowledge: {removed['knowledge']}")
            print("(use --no-dry-run to execute)")
    
    elif args.command == "clean-checkpoints":
        count, files = optimizer.clean_old_checkpoints(args.keep, not args.no_dry_run)
        if args.no_dry_run:
            print(f"✅ Cleaned {count} old checkpoints")
        else:
            print(f"Would clean {count} old checkpoints (use --no-dry-run to execute)")
    
    elif args.command == "optimize":
        results = optimizer.optimize_all(not args.no_dry_run)
        print(json.dumps(results, indent=2))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

