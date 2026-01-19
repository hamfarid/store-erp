"""
FILE: backend/tests/performance/locustfile.py | PURPOSE: Performance tests with Locust | OWNER: QA Team | LAST-AUDITED: 2025-11-18

Performance Tests using Locust

Tests for:
- API endpoint performance
- Concurrent user load
- Response time benchmarks
- Throughput testing

Usage:
    locust -f backend/tests/performance/locustfile.py --host=http://localhost:8000

Version: 1.0.0
"""

from locust import HttpUser, task, between, events
import random
import json


class GaaraAIUser(HttpUser):
    """
    Simulated user for Gaara AI application
    
    Simulates realistic user behavior with think time between requests.
    """
    
    # Wait 1-3 seconds between tasks
    wait_time = between(1, 3)
    
    def on_start(self):
        """Called when a user starts - login"""
        self.login()
    
    def login(self):
        """Login to get authentication token"""
        response = self.client.post("/api/auth/login", json={
            "email": f"user{random.randint(1, 100)}@example.com",
            "password": "TestP@ssw0rd123"
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task(10)
    def view_dashboard(self):
        """View dashboard (most common action)"""
        self.client.get("/api/dashboard", headers=self.headers)
    
    @task(5)
    def list_farms(self):
        """List user's farms"""
        self.client.get("/api/farms", headers=self.headers)
    
    @task(3)
    def view_farm_details(self):
        """View specific farm details"""
        farm_id = random.randint(1, 100)
        self.client.get(f"/api/farms/{farm_id}", headers=self.headers)
    
    @task(2)
    def create_farm(self):
        """Create a new farm"""
        self.client.post("/api/farms", headers=self.headers, json={
            "name": f"Test Farm {random.randint(1, 1000)}",
            "location": "Test Location",
            "area": random.randint(10, 1000),
            "crop_type": random.choice(["wheat", "corn", "rice", "tomato"])
        })
    
    @task(4)
    def list_diagnoses(self):
        """List diagnosis history"""
        self.client.get("/api/diagnosis/history", headers=self.headers)
    
    @task(1)
    def upload_image_for_diagnosis(self):
        """Upload image for disease diagnosis"""
        # Simulate image upload
        files = {
            'file': ('test.jpg', b'fake image data', 'image/jpeg')
        }
        self.client.post("/api/diagnosis/upload", headers=self.headers, files=files)
    
    @task(2)
    def view_reports(self):
        """View reports"""
        self.client.get("/api/reports", headers=self.headers)
    
    @task(1)
    def generate_report(self):
        """Generate a report"""
        self.client.post("/api/reports/generate", headers=self.headers, json={
            "report_type": "farm_summary",
            "farm_id": random.randint(1, 100),
            "format": "pdf"
        })
    
    @task(3)
    def view_profile(self):
        """View user profile"""
        self.client.get("/api/users/profile", headers=self.headers)


class AdminUser(HttpUser):
    """
    Simulated admin user
    
    Performs admin-specific tasks.
    """
    
    wait_time = between(2, 5)
    
    def on_start(self):
        """Login as admin"""
        response = self.client.post("/api/auth/login", json={
            "email": "admin@example.com",
            "password": "AdminP@ssw0rd123"
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task(5)
    def view_admin_dashboard(self):
        """View admin dashboard"""
        self.client.get("/api/admin/dashboard", headers=self.headers)
    
    @task(3)
    def list_all_users(self):
        """List all users"""
        self.client.get("/api/admin/users", headers=self.headers)
    
    @task(2)
    def view_system_stats(self):
        """View system statistics"""
        self.client.get("/api/admin/stats", headers=self.headers)
    
    @task(1)
    def view_activity_log(self):
        """View activity log"""
        self.client.get("/api/admin/activity-log", headers=self.headers)


class APIHealthCheck(HttpUser):
    """
    Health check user
    
    Continuously monitors API health.
    """
    
    wait_time = between(5, 10)
    
    @task
    def health_check(self):
        """Check API health"""
        self.client.get("/health")
    
    @task
    def api_status(self):
        """Check API status"""
        self.client.get("/api/status")


# Performance benchmarks
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts"""
    print("=" * 80)
    print("🚀 GAARA AI - PERFORMANCE TEST STARTED")
    print("=" * 80)
    print(f"Host: {environment.host}")
    print(f"Users: {environment.runner.target_user_count if hasattr(environment.runner, 'target_user_count') else 'N/A'}")
    print("=" * 80)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops"""
    print("=" * 80)
    print("🏁 GAARA AI - PERFORMANCE TEST COMPLETED")
    print("=" * 80)
    
    # Get stats
    stats = environment.stats
    
    print("\n📊 PERFORMANCE SUMMARY:")
    print(f"Total Requests: {stats.total.num_requests}")
    print(f"Total Failures: {stats.total.num_failures}")
    print(f"Average Response Time: {stats.total.avg_response_time:.2f}ms")
    print(f"Min Response Time: {stats.total.min_response_time:.2f}ms")
    print(f"Max Response Time: {stats.total.max_response_time:.2f}ms")
    print(f"Requests per Second: {stats.total.total_rps:.2f}")
    print(f"Failure Rate: {(stats.total.num_failures / stats.total.num_requests * 100) if stats.total.num_requests > 0 else 0:.2f}%")
    print("=" * 80)
    
    # Performance benchmarks
    avg_response_time = stats.total.avg_response_time
    failure_rate = (stats.total.num_failures / stats.total.num_requests * 100) if stats.total.num_requests > 0 else 0
    
    print("\n✅ PERFORMANCE BENCHMARKS:")
    print(f"Average Response Time: {'✅ PASS' if avg_response_time < 500 else '❌ FAIL'} (Target: <500ms, Actual: {avg_response_time:.2f}ms)")
    print(f"Failure Rate: {'✅ PASS' if failure_rate < 1 else '❌ FAIL'} (Target: <1%, Actual: {failure_rate:.2f}%)")
    print("=" * 80)

