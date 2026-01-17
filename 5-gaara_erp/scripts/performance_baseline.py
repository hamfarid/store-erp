#!/usr/bin/env python
"""
Performance Baseline Generator for Gaara ERP v12
================================================================
Generates comprehensive performance metrics before CDN deployment.

Usage:
    python scripts/performance_baseline.py [--output baseline.json]

Metrics Collected:
    - API response times (auth, dashboard, CRUD operations)
    - Database query performance
    - Memory usage
    - CPU utilization
    - Static asset sizes

Created: 2026-01-16
"""

import os
import sys
import json
import time
import argparse
import statistics
from datetime import datetime
from typing import Dict, List, Any
import subprocess

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not installed. Memory/CPU metrics will be limited.")


class PerformanceBaseline:
    """Generate performance baseline metrics."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            "generated_at": datetime.now().isoformat(),
            "base_url": base_url,
            "metrics": {},
            "warnings": [],
        }
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all performance benchmarks."""
        print("=" * 60)
        print("🚀 Gaara ERP Performance Baseline Generator")
        print("=" * 60)
        
        # System metrics
        self.results["metrics"]["system"] = self._collect_system_metrics()
        
        # Database metrics
        self.results["metrics"]["database"] = self._collect_database_metrics()
        
        # Static asset metrics
        self.results["metrics"]["static_assets"] = self._collect_static_asset_metrics()
        
        # Django-specific metrics
        self.results["metrics"]["django"] = self._collect_django_metrics()
        
        # API endpoint metrics (if server running)
        self.results["metrics"]["api_endpoints"] = self._collect_api_metrics()
        
        # Summary
        self._generate_summary()
        
        return self.results
    
    def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level metrics."""
        print("\n📊 Collecting system metrics...")
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version,
        }
        
        if PSUTIL_AVAILABLE:
            # Memory
            memory = psutil.virtual_memory()
            metrics["memory"] = {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "percent_used": memory.percent,
            }
            
            # CPU
            metrics["cpu"] = {
                "count": psutil.cpu_count(),
                "percent_used": psutil.cpu_percent(interval=1),
            }
            
            # Disk
            disk = psutil.disk_usage('/')
            metrics["disk"] = {
                "total_gb": round(disk.total / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent_used": round(disk.percent, 2),
            }
        
        print(f"  ✅ System metrics collected")
        return metrics
    
    def _collect_database_metrics(self) -> Dict[str, Any]:
        """Collect database performance metrics."""
        print("\n📊 Collecting database metrics...")
        
        metrics = {
            "connection_test": False,
            "query_times": {},
        }
        
        try:
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')
            django.setup()
            
            from django.db import connection
            
            # Test connection
            with connection.cursor() as cursor:
                start = time.time()
                cursor.execute("SELECT 1")
                metrics["connection_test"] = True
                metrics["connection_time_ms"] = round((time.time() - start) * 1000, 2)
            
            # Count tables
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """)
                metrics["table_count"] = cursor.fetchone()[0]
            
            # Test common queries
            test_queries = {
                "user_count": "SELECT COUNT(*) FROM auth_user",
                "content_type_count": "SELECT COUNT(*) FROM django_content_type",
            }
            
            for name, query in test_queries.items():
                try:
                    with connection.cursor() as cursor:
                        start = time.time()
                        cursor.execute(query)
                        cursor.fetchone()
                        metrics["query_times"][name] = round((time.time() - start) * 1000, 2)
                except Exception:
                    pass
            
            print(f"  ✅ Database metrics collected (connection: {metrics['connection_time_ms']}ms)")
            
        except Exception as e:
            self.results["warnings"].append(f"Database metrics failed: {e}")
            print(f"  ⚠️ Database metrics failed: {e}")
        
        return metrics
    
    def _collect_static_asset_metrics(self) -> Dict[str, Any]:
        """Collect static asset size metrics."""
        print("\n📊 Collecting static asset metrics...")
        
        metrics = {
            "total_size_mb": 0,
            "by_type": {},
            "largest_files": [],
        }
        
        # Check common static directories
        static_dirs = [
            "gaara_erp/static",
            "gaara-erp-frontend/dist",
            "gaara-erp-frontend/build",
        ]
        
        all_files = []
        
        for static_dir in static_dirs:
            if os.path.exists(static_dir):
                for root, dirs, files in os.walk(static_dir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        size = os.path.getsize(filepath)
                        ext = os.path.splitext(file)[1].lower() or 'no_ext'
                        
                        all_files.append((filepath, size))
                        
                        if ext not in metrics["by_type"]:
                            metrics["by_type"][ext] = {"count": 0, "size_kb": 0}
                        
                        metrics["by_type"][ext]["count"] += 1
                        metrics["by_type"][ext]["size_kb"] += size / 1024
        
        # Calculate totals
        total_size = sum(size for _, size in all_files)
        metrics["total_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        # Round sizes
        for ext in metrics["by_type"]:
            metrics["by_type"][ext]["size_kb"] = round(metrics["by_type"][ext]["size_kb"], 2)
        
        # Get largest files
        all_files.sort(key=lambda x: x[1], reverse=True)
        metrics["largest_files"] = [
            {"path": path, "size_kb": round(size/1024, 2)}
            for path, size in all_files[:10]
        ]
        
        print(f"  ✅ Static assets: {metrics['total_size_mb']}MB total")
        return metrics
    
    def _collect_django_metrics(self) -> Dict[str, Any]:
        """Collect Django-specific metrics."""
        print("\n📊 Collecting Django metrics...")
        
        metrics = {
            "installed_apps": 0,
            "models": 0,
            "migrations": {},
        }
        
        try:
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gaara_erp.settings')
            django.setup()
            
            from django.apps import apps
            from django.conf import settings
            
            # Count apps and models
            metrics["installed_apps"] = len(settings.INSTALLED_APPS)
            
            model_count = 0
            for app_config in apps.get_app_configs():
                models = app_config.get_models()
                model_count += len(list(models))
            
            metrics["models"] = model_count
            
            # Check unapplied migrations
            from django.db.migrations.recorder import MigrationRecorder
            from django.db import connection
            
            try:
                recorder = MigrationRecorder(connection)
                applied = recorder.applied_migrations()
                metrics["applied_migrations"] = len(applied)
            except Exception:
                pass
            
            print(f"  ✅ Django: {metrics['installed_apps']} apps, {metrics['models']} models")
            
        except Exception as e:
            self.results["warnings"].append(f"Django metrics failed: {e}")
            print(f"  ⚠️ Django metrics failed: {e}")
        
        return metrics
    
    def _collect_api_metrics(self) -> Dict[str, Any]:
        """Collect API endpoint response times."""
        print("\n📊 Collecting API metrics...")
        
        metrics = {
            "endpoints_tested": 0,
            "response_times": {},
        }
        
        try:
            import requests
            
            # Test endpoints (adjust based on your actual API)
            endpoints = [
                ("health", "/api/health/"),
                ("csrf", "/api/csrf-token/"),
            ]
            
            for name, path in endpoints:
                url = f"{self.base_url}{path}"
                times = []
                
                # Run 3 iterations
                for _ in range(3):
                    try:
                        start = time.time()
                        resp = requests.get(url, timeout=10)
                        elapsed = (time.time() - start) * 1000
                        times.append(elapsed)
                    except Exception:
                        break
                
                if times:
                    metrics["response_times"][name] = {
                        "min_ms": round(min(times), 2),
                        "max_ms": round(max(times), 2),
                        "avg_ms": round(statistics.mean(times), 2),
                        "status": resp.status_code if 'resp' in dir() else None,
                    }
                    metrics["endpoints_tested"] += 1
            
            print(f"  ✅ Tested {metrics['endpoints_tested']} API endpoints")
            
        except ImportError:
            self.results["warnings"].append("requests library not installed - skipping API metrics")
            print("  ⚠️ requests library not installed - skipping API metrics")
        except Exception as e:
            self.results["warnings"].append(f"API metrics failed: {e}")
            print(f"  ⚠️ API metrics failed: {e}")
        
        return metrics
    
    def _generate_summary(self):
        """Generate performance summary."""
        print("\n" + "=" * 60)
        print("📈 PERFORMANCE BASELINE SUMMARY")
        print("=" * 60)
        
        summary = {
            "status": "healthy",
            "recommendations": [],
        }
        
        # Check memory
        if "memory" in self.results["metrics"].get("system", {}):
            mem = self.results["metrics"]["system"]["memory"]
            if mem["percent_used"] > 80:
                summary["recommendations"].append("High memory usage detected")
                summary["status"] = "warning"
        
        # Check database
        db = self.results["metrics"].get("database", {})
        if db.get("connection_time_ms", 0) > 100:
            summary["recommendations"].append("Database connection is slow (>100ms)")
        
        # Check static assets
        assets = self.results["metrics"].get("static_assets", {})
        if assets.get("total_size_mb", 0) > 50:
            summary["recommendations"].append("Large static assets - consider CDN optimization")
        
        self.results["summary"] = summary
        
        print(f"\n  Status: {summary['status'].upper()}")
        if summary["recommendations"]:
            print("\n  Recommendations:")
            for rec in summary["recommendations"]:
                print(f"    - {rec}")
        else:
            print("  ✅ No issues detected")
        
        print("\n" + "=" * 60)
    
    def save_results(self, output_path: str):
        """Save results to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n💾 Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate performance baseline metrics")
    parser.add_argument(
        "--output", "-o",
        default="performance_baseline.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--url", "-u",
        default="http://localhost:8000",
        help="Base URL for API tests"
    )
    
    args = parser.parse_args()
    
    baseline = PerformanceBaseline(base_url=args.url)
    baseline.run_all_benchmarks()
    baseline.save_results(args.output)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
