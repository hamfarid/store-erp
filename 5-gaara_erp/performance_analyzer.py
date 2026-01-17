#!/usr/bin/env python3
"""
Gaara ERP Performance Analyzer
==============================

Comprehensive performance analysis tool for Gaara ERP system.
Analyzes database queries, API response times, memory usage, and more.

Usage:
    python performance_analyzer.py [--mode MODE] [--duration SECONDS] [--output FILE]

Modes:
    quick       - Quick performance check (default)
    detailed    - Detailed analysis with profiling
    load        - Load testing simulation
    database    - Database performance analysis
    api         - API endpoint performance testing
"""

import os
import sys
import time
import json
import psutil
import requests
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse


class PerformanceAnalyzer:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.gaara_dir = self.base_dir / 'gaara_erp'
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self.get_system_info(),
            'tests': []
        }
        
    def get_system_info(self):
        """Get system information"""
        return {
            'python_version': sys.version,
            'platform': sys.platform,
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': psutil.virtual_memory().total / (1024**3),
            'disk_total_gb': psutil.disk_usage(self.base_dir).total / (1024**3)
        }
        
    def print_banner(self):
        """Print analyzer banner"""
        print("""
📊 GAARA ERP PERFORMANCE ANALYZER 📊
====================================
🔍 System Performance Analysis
⚡ Speed & Efficiency Testing
📈 Optimization Recommendations
        """)
        
    def test_system_resources(self):
        """Test system resource usage"""
        print("🖥️  Testing system resources...")
        
        # CPU test
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory test
        memory = psutil.virtual_memory()
        
        # Disk test
        disk = psutil.disk_usage(self.base_dir)
        
        # Network test
        network_start = psutil.net_io_counters()
        time.sleep(1)
        network_end = psutil.net_io_counters()
        
        network_speed = {
            'bytes_sent_per_sec': network_end.bytes_sent - network_start.bytes_sent,
            'bytes_recv_per_sec': network_end.bytes_recv - network_start.bytes_recv
        }
        
        result = {
            'test_name': 'System Resources',
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': memory.available / (1024**3),
            'disk_percent': (disk.used / disk.total) * 100,
            'disk_free_gb': disk.free / (1024**3),
            'network_speed': network_speed,
            'status': 'pass' if cpu_percent < 80 and memory.percent < 85 else 'warning'
        }
        
        self.results['tests'].append(result)
        
        print(f"   CPU Usage: {cpu_percent:.1f}%")
        print(f"   Memory Usage: {memory.percent:.1f}%")
        print(f"   Disk Usage: {(disk.used / disk.total) * 100:.1f}%")
        
        return result
        
    def test_django_startup(self):
        """Test Django startup time"""
        print("🐍 Testing Django startup time...")
        
        os.chdir(self.gaara_dir)
        
        start_time = time.time()
        
        try:
            # Test Django check command
            result = subprocess.run([
                sys.executable, 'manage.py', 'check'
            ], capture_output=True, text=True, timeout=60)
            
            startup_time = time.time() - start_time
            
            test_result = {
                'test_name': 'Django Startup',
                'startup_time_seconds': startup_time,
                'status': 'pass' if result.returncode == 0 else 'fail',
                'output': result.stdout if result.returncode == 0 else result.stderr
            }
            
            self.results['tests'].append(test_result)
            
            print(f"   Startup Time: {startup_time:.2f} seconds")
            print(f"   Status: {'✅ Pass' if result.returncode == 0 else '❌ Fail'}")
            
            return test_result
            
        except subprocess.TimeoutExpired:
            test_result = {
                'test_name': 'Django Startup',
                'startup_time_seconds': 60,
                'status': 'timeout',
                'output': 'Startup timeout after 60 seconds'
            }
            
            self.results['tests'].append(test_result)
            print("   ❌ Startup timeout")
            return test_result
            
    def test_database_performance(self):
        """Test database performance"""
        print("🗄️  Testing database performance...")
        
        os.chdir(self.gaara_dir)
        
        tests = [
            ('Connection Test', 'from django.db import connection; connection.ensure_connection(); print("OK")'),
            ('Model Count', 'from django.apps import apps; print(len(apps.get_models()))'),
            ('Migration Status', 'from django.core.management import execute_from_command_line; execute_from_command_line(["manage.py", "showmigrations", "--plan"])')
        ]
        
        db_results = []
        
        for test_name, test_code in tests:
            start_time = time.time()
            
            try:
                result = subprocess.run([
                    sys.executable, 'manage.py', 'shell', '-c', test_code
                ], capture_output=True, text=True, timeout=30)
                
                execution_time = time.time() - start_time
                
                test_result = {
                    'test_name': f'Database - {test_name}',
                    'execution_time_seconds': execution_time,
                    'status': 'pass' if result.returncode == 0 else 'fail',
                    'output': result.stdout.strip()
                }
                
                db_results.append(test_result)
                self.results['tests'].append(test_result)
                
                print(f"   {test_name}: {execution_time:.3f}s {'✅' if result.returncode == 0 else '❌'}")
                
            except subprocess.TimeoutExpired:
                test_result = {
                    'test_name': f'Database - {test_name}',
                    'execution_time_seconds': 30,
                    'status': 'timeout',
                    'output': 'Test timeout'
                }
                
                db_results.append(test_result)
                self.results['tests'].append(test_result)
                print(f"   {test_name}: ❌ Timeout")
                
        return db_results
        
    def test_api_endpoints(self, base_url='http://localhost:9551'):
        """Test API endpoint performance"""
        print("🔌 Testing API endpoints...")
        
        endpoints = [
            '/admin/',
            '/api/',
            '/api/auth/',
            '/api/core/',
        ]
        
        api_results = []
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                response_time = time.time() - start_time
                
                test_result = {
                    'test_name': f'API - {endpoint}',
                    'url': url,
                    'response_time_seconds': response_time,
                    'status_code': response.status_code,
                    'status': 'pass' if response.status_code < 500 else 'fail',
                    'response_size_bytes': len(response.content)
                }
                
                api_results.append(test_result)
                self.results['tests'].append(test_result)
                
                status_icon = '✅' if response.status_code < 500 else '❌'
                print(f"   {endpoint}: {response_time:.3f}s [{response.status_code}] {status_icon}")
                
            except requests.RequestException as e:
                test_result = {
                    'test_name': f'API - {endpoint}',
                    'url': url,
                    'response_time_seconds': None,
                    'status_code': None,
                    'status': 'error',
                    'error': str(e)
                }
                
                api_results.append(test_result)
                self.results['tests'].append(test_result)
                print(f"   {endpoint}: ❌ Error - {e}")
                
        return api_results
        
    def test_load_simulation(self, concurrent_requests=10, duration=30):
        """Simulate load testing"""
        print(f"🔥 Load testing ({concurrent_requests} concurrent requests for {duration}s)...")
        
        base_url = 'http://localhost:9551'
        endpoints = ['/admin/', '/api/']
        
        def make_request(endpoint):
            try:
                start_time = time.time()
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                response_time = time.time() - start_time
                return {
                    'endpoint': endpoint,
                    'response_time': response_time,
                    'status_code': response.status_code,
                    'success': response.status_code < 500
                }
            except Exception as e:
                return {
                    'endpoint': endpoint,
                    'response_time': None,
                    'status_code': None,
                    'success': False,
                    'error': str(e)
                }
                
        start_time = time.time()
        total_requests = 0
        successful_requests = 0
        response_times = []
        
        with ThreadPoolExecutor(max_workers=concurrent_requests) as executor:
            while time.time() - start_time < duration:
                # Submit requests for all endpoints
                futures = []
                for endpoint in endpoints:
                    future = executor.submit(make_request, endpoint)
                    futures.append(future)
                    
                # Collect results
                for future in as_completed(futures, timeout=15):
                    try:
                        result = future.result()
                        total_requests += 1
                        
                        if result['success']:
                            successful_requests += 1
                            if result['response_time']:
                                response_times.append(result['response_time'])
                                
                    except Exception:
                        total_requests += 1
                        
                time.sleep(0.1)  # Small delay between batches
                
        # Calculate statistics
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        requests_per_second = total_requests / duration
        
        load_result = {
            'test_name': 'Load Testing',
            'duration_seconds': duration,
            'concurrent_requests': concurrent_requests,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'success_rate_percent': success_rate,
            'average_response_time_seconds': avg_response_time,
            'requests_per_second': requests_per_second,
            'status': 'pass' if success_rate > 90 else 'warning'
        }
        
        self.results['tests'].append(load_result)
        
        print(f"   Total Requests: {total_requests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Avg Response Time: {avg_response_time:.3f}s")
        print(f"   Requests/Second: {requests_per_second:.1f}")
        
        return load_result
        
    def generate_recommendations(self):
        """Generate performance recommendations"""
        recommendations = []
        
        # Analyze results
        for test in self.results['tests']:
            if test['test_name'] == 'System Resources':
                if test['cpu_percent'] > 80:
                    recommendations.append("🔧 High CPU usage detected. Consider optimizing code or upgrading hardware.")
                if test['memory_percent'] > 85:
                    recommendations.append("🧠 High memory usage detected. Consider memory optimization or more RAM.")
                    
            elif test['test_name'] == 'Django Startup':
                if test['startup_time_seconds'] > 10:
                    recommendations.append("🐍 Slow Django startup. Consider reducing installed apps or optimizing imports.")
                    
            elif 'API -' in test['test_name']:
                if test.get('response_time_seconds', 0) > 2:
                    recommendations.append(f"🔌 Slow API response for {test['test_name']}. Consider caching or query optimization.")
                    
            elif test['test_name'] == 'Load Testing':
                if test['success_rate_percent'] < 95:
                    recommendations.append("🔥 Low success rate under load. Consider scaling or optimization.")
                if test['average_response_time_seconds'] > 1:
                    recommendations.append("⚡ Slow response times under load. Consider performance tuning.")
                    
        if not recommendations:
            recommendations.append("✅ System performance looks good! No major issues detected.")
            
        return recommendations
        
    def save_report(self, output_file=None):
        """Save performance report"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.base_dir / f'performance_report_{timestamp}.json'
            
        # Add recommendations
        self.results['recommendations'] = self.generate_recommendations()
        
        # Calculate summary
        total_tests = len(self.results['tests'])
        passed_tests = len([t for t in self.results['tests'] if t.get('status') == 'pass'])
        
        self.results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
            
        print(f"\n📄 Report saved: {output_file}")
        return output_file
        
    def print_summary(self):
        """Print performance summary"""
        print("\n" + "="*60)
        print("📊 PERFORMANCE ANALYSIS SUMMARY")
        print("="*60)
        
        total_tests = len(self.results['tests'])
        passed_tests = len([t for t in self.results['tests'] if t.get('status') == 'pass'])
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed Tests: {passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        print(f"\n💡 Recommendations:")
        recommendations = self.generate_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
            
        print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description='Gaara ERP Performance Analyzer')
    parser.add_argument('--mode', choices=['quick', 'detailed', 'load', 'database', 'api'],
                       default='quick', help='Analysis mode')
    parser.add_argument('--duration', type=int, default=30,
                       help='Duration for load testing (seconds)')
    parser.add_argument('--output', help='Output file for report')
    
    args = parser.parse_args()
    
    analyzer = PerformanceAnalyzer()
    analyzer.print_banner()
    
    try:
        if args.mode == 'quick':
            analyzer.test_system_resources()
            analyzer.test_django_startup()
            
        elif args.mode == 'detailed':
            analyzer.test_system_resources()
            analyzer.test_django_startup()
            analyzer.test_database_performance()
            analyzer.test_api_endpoints()
            
        elif args.mode == 'load':
            analyzer.test_load_simulation(duration=args.duration)
            
        elif args.mode == 'database':
            analyzer.test_database_performance()
            
        elif args.mode == 'api':
            analyzer.test_api_endpoints()
            
        analyzer.print_summary()
        analyzer.save_report(args.output)
        
    except KeyboardInterrupt:
        print("\n🛑 Analysis interrupted by user")
    except Exception as e:
        print(f"❌ Analysis error: {e}")


if __name__ == '__main__':
    main()
