#!/usr/bin/env python3
"""
Global Guidelines Test Suite
Comprehensive testing for all memory and guideline components
"""

import sys
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import time

# Import our tools
try:
    from memory_analytics_dashboard import MemoryAnalyticsDashboard
    from memory_team_sharing import MemoryTeamSharing, ShareLevel
    from memory_optimizer import MemoryOptimizer
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from memory_analytics_dashboard import MemoryAnalyticsDashboard
    from memory_team_sharing import MemoryTeamSharing, ShareLevel
    from memory_optimizer import MemoryOptimizer

class TestSuite:
    """Comprehensive test suite."""
    
    def __init__(self):
        """Initialize test suite."""
        self.temp_dir = None
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "passed": 0,
            "failed": 0,
            "skipped": 0
        }
    
    def setup(self):
        """Setup test environment."""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="global_test_"))
        self.memory_dir = self.temp_dir / ".memory"
        self._create_test_structure()
    
    def teardown(self):
        """Cleanup test environment."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def _create_test_structure(self):
        """Create test directory structure."""
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
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create test data
        self._create_test_conversation()
        self._create_test_knowledge()
        self._create_test_state()
    
    def _create_test_conversation(self):
        """Create test conversation."""
        conv = {
            "id": "test_conv_001",
            "user_id": "test_user",
            "created_at": datetime.now().isoformat(),
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]
        }
        
        conv_file = self.memory_dir / "conversations" / "test_conv_001.json"
        with open(conv_file, 'w') as f:
            json.dump(conv, f)
    
    def _create_test_knowledge(self):
        """Create test knowledge."""
        knowledge = {
            "id": "test_know_001",
            "content": "Test knowledge item",
            "importance": 8,
            "metadata": {
                "category": "testing"
            },
            "created_at": datetime.now().isoformat()
        }
        
        know_file = self.memory_dir / "knowledge" / "test_know_001.json"
        with open(know_file, 'w') as f:
            json.dump(knowledge, f)
    
    def _create_test_state(self):
        """Create test state."""
        state = {
            "user_id": "test_user",
            "current_project": "test_project",
            "current_phase": "testing",
            "context": {
                "session_count": 1,
                "last_activity": datetime.now().isoformat()
            }
        }
        
        state_file = self.memory_dir / "state" / "current_state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f)
    
    def run_test(self, name: str, test_func):
        """Run a single test."""
        print(f"Running: {name}...", end=" ")
        
        start_time = time.time()
        
        try:
            test_func()
            duration = time.time() - start_time
            
            self.results["tests"].append({
                "name": name,
                "status": "passed",
                "duration": duration
            })
            self.results["passed"] += 1
            print(f"✅ PASSED ({duration:.3f}s)")
            
        except Exception as e:
            duration = time.time() - start_time
            
            self.results["tests"].append({
                "name": name,
                "status": "failed",
                "error": str(e),
                "duration": duration
            })
            self.results["failed"] += 1
            print(f"❌ FAILED ({duration:.3f}s)")
            print(f"   Error: {e}")
    
    # Analytics Tests
    def test_analytics_dashboard_init(self):
        """Test analytics dashboard initialization."""
        dashboard = MemoryAnalyticsDashboard(str(self.memory_dir))
        assert dashboard.memory_dir.exists()
        assert dashboard.db_path.exists()
    
    def test_analytics_collect_stats(self):
        """Test stats collection."""
        dashboard = MemoryAnalyticsDashboard(str(self.memory_dir))
        stats = dashboard.collect_stats()
        
        assert "conversations" in stats
        assert "knowledge" in stats
        assert "storage" in stats
        assert "health" in stats
        assert stats["conversations"]["count"] >= 1
        assert stats["knowledge"]["count"] >= 1
    
    def test_analytics_generate_report(self):
        """Test report generation."""
        dashboard = MemoryAnalyticsDashboard(str(self.memory_dir))
        report = dashboard.generate_report("text")
        
        assert "MEMORY ANALYTICS DASHBOARD" in report
        assert "CONVERSATIONS" in report
        assert "KNOWLEDGE BASE" in report
    
    def test_analytics_trends(self):
        """Test trends analysis."""
        dashboard = MemoryAnalyticsDashboard(str(self.memory_dir))
        # Collect stats first
        dashboard.collect_stats()
        
        trends = dashboard.get_trends(30)
        assert "data_points" in trends or "error" in trends
    
    # Team Sharing Tests
    def test_team_sharing_init(self):
        """Test team sharing initialization."""
        sharing = MemoryTeamSharing(str(self.memory_dir))
        assert sharing.memory_dir.exists()
        assert sharing.db_path.exists()
    
    def test_team_create(self):
        """Test team creation."""
        sharing = MemoryTeamSharing(str(self.memory_dir))
        team_id = sharing.create_team("Test Team", "A test team", "test_user")
        
        assert team_id is not None
        assert len(team_id) > 0
    
    def test_team_add_member(self):
        """Test adding team member."""
        sharing = MemoryTeamSharing(str(self.memory_dir))
        team_id = sharing.create_team("Test Team", "A test team", "test_user")
        success = sharing.add_team_member(team_id, "test_user2", "member")
        
        assert success == True
    
    def test_share_memory(self):
        """Test memory sharing."""
        sharing = MemoryTeamSharing(str(self.memory_dir))
        team_id = sharing.create_team("Test Team", "A test team", "test_user")
        
        share_id = sharing.share_memory(
            "knowledge",
            "test_know_001",
            "test_user",
            ShareLevel.TEAM,
            team_id=team_id
        )
        
        assert share_id is not None
        assert len(share_id) > 0
    
    def test_get_shared_memories(self):
        """Test getting shared memories."""
        sharing = MemoryTeamSharing(str(self.memory_dir))
        team_id = sharing.create_team("Test Team", "A test team", "test_user")
        
        sharing.share_memory(
            "knowledge",
            "test_know_001",
            "test_user",
            ShareLevel.TEAM,
            team_id=team_id
        )
        
        memories = sharing.get_shared_memories("test_user")
        assert len(memories) >= 1
    
    def test_team_stats(self):
        """Test team statistics."""
        sharing = MemoryTeamSharing(str(self.memory_dir))
        team_id = sharing.create_team("Test Team", "A test team", "test_user")
        
        stats = sharing.get_team_stats(team_id)
        assert "team_id" in stats
        assert stats["name"] == "Test Team"
        assert stats["member_count"] >= 1
    
    # Optimizer Tests
    def test_optimizer_init(self):
        """Test optimizer initialization."""
        optimizer = MemoryOptimizer(str(self.memory_dir))
        assert optimizer.memory_dir.exists()
    
    def test_optimizer_analyze(self):
        """Test memory analysis."""
        optimizer = MemoryOptimizer(str(self.memory_dir))
        analysis = optimizer.analyze()
        
        assert "conversations" in analysis
        assert "knowledge" in analysis
        assert "recommendations" in analysis
    
    def test_optimizer_backup(self):
        """Test backup creation."""
        optimizer = MemoryOptimizer(str(self.memory_dir))
        backup_path = optimizer.backup("test_backup")
        
        assert backup_path.exists()
        assert (backup_path / "manifest.json").exists()
    
    def test_optimizer_clean_old(self):
        """Test cleaning old conversations (dry run)."""
        optimizer = MemoryOptimizer(str(self.memory_dir))
        count, files = optimizer.clean_old_conversations(90, dry_run=True)
        
        assert count >= 0
    
    def test_optimizer_remove_empty(self):
        """Test removing empty conversations (dry run)."""
        optimizer = MemoryOptimizer(str(self.memory_dir))
        count, files = optimizer.remove_empty_conversations(dry_run=True)
        
        assert count >= 0
    
    def test_optimizer_remove_duplicates(self):
        """Test removing duplicates (dry run)."""
        optimizer = MemoryOptimizer(str(self.memory_dir))
        removed = optimizer.remove_duplicates(dry_run=True)
        
        assert "conversations" in removed
        assert "knowledge" in removed
    
    def test_optimizer_optimize_all(self):
        """Test full optimization (dry run)."""
        optimizer = MemoryOptimizer(str(self.memory_dir))
        results = optimizer.optimize_all(dry_run=True)
        
        assert "actions" in results
        assert "dry_run" in results
        assert results["dry_run"] == True
    
    # Performance Tests
    def test_performance_analytics(self):
        """Test analytics performance."""
        dashboard = MemoryAnalyticsDashboard(str(self.memory_dir))
        
        start = time.time()
        for _ in range(10):
            dashboard.collect_stats()
        duration = time.time() - start
        
        avg_duration = duration / 10
        assert avg_duration < 1.0, f"Analytics too slow: {avg_duration:.3f}s per call"
    
    def test_performance_sharing(self):
        """Test sharing performance."""
        sharing = MemoryTeamSharing(str(self.memory_dir))
        team_id = sharing.create_team("Perf Team", "Performance test", "test_user")
        
        start = time.time()
        for i in range(10):
            sharing.share_memory(
                "knowledge",
                f"test_know_{i:03d}",
                "test_user",
                ShareLevel.TEAM,
                team_id=team_id
            )
        duration = time.time() - start
        
        avg_duration = duration / 10
        assert avg_duration < 0.1, f"Sharing too slow: {avg_duration:.3f}s per call"
    
    def run_all(self):
        """Run all tests."""
        print("=" * 80)
        print("GLOBAL GUIDELINES TEST SUITE v7.2.0")
        print("=" * 80)
        print()
        
        # Setup
        print("Setting up test environment...")
        self.setup()
        print(f"Test directory: {self.temp_dir}")
        print()
        
        # Analytics Tests
        print("📊 Analytics Tests")
        print("-" * 80)
        self.run_test("Analytics Dashboard Init", self.test_analytics_dashboard_init)
        self.run_test("Analytics Collect Stats", self.test_analytics_collect_stats)
        self.run_test("Analytics Generate Report", self.test_analytics_generate_report)
        self.run_test("Analytics Trends", self.test_analytics_trends)
        print()
        
        # Team Sharing Tests
        print("👥 Team Sharing Tests")
        print("-" * 80)
        self.run_test("Team Sharing Init", self.test_team_sharing_init)
        self.run_test("Team Create", self.test_team_create)
        self.run_test("Team Add Member", self.test_team_add_member)
        self.run_test("Share Memory", self.test_share_memory)
        self.run_test("Get Shared Memories", self.test_get_shared_memories)
        self.run_test("Team Stats", self.test_team_stats)
        print()
        
        # Optimizer Tests
        print("🔧 Optimizer Tests")
        print("-" * 80)
        self.run_test("Optimizer Init", self.test_optimizer_init)
        self.run_test("Optimizer Analyze", self.test_optimizer_analyze)
        self.run_test("Optimizer Backup", self.test_optimizer_backup)
        self.run_test("Optimizer Clean Old", self.test_optimizer_clean_old)
        self.run_test("Optimizer Remove Empty", self.test_optimizer_remove_empty)
        self.run_test("Optimizer Remove Duplicates", self.test_optimizer_remove_duplicates)
        self.run_test("Optimizer Optimize All", self.test_optimizer_optimize_all)
        print()
        
        # Performance Tests
        print("⚡ Performance Tests")
        print("-" * 80)
        self.run_test("Performance Analytics", self.test_performance_analytics)
        self.run_test("Performance Sharing", self.test_performance_sharing)
        print()
        
        # Teardown
        print("Cleaning up test environment...")
        self.teardown()
        print()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {len(self.results['tests'])}")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"⏭️  Skipped: {self.results['skipped']}")
        
        if self.results['failed'] == 0:
            print("\n🎉 All tests passed!")
            return 0
        else:
            print(f"\n❌ {self.results['failed']} test(s) failed")
            return 1

def main():
    """Main entry point."""
    suite = TestSuite()
    exit_code = suite.run_all()
    
    # Save results
    results_file = Path("test_results.json")
    with open(results_file, 'w') as f:
        json.dump(suite.results, f, indent=2)
    print(f"\nResults saved to: {results_file}")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()

