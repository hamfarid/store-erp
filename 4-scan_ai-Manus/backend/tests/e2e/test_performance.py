"""
Playwright Performance Tests
Tests for page load performance, API response times, and resource usage
"""

import pytest
from playwright.sync_api import sync_playwright
import time


class TestPagePerformance:
    """Test page load performance"""

    @pytest.fixture(scope="class")
    def browser_page(self):
        """Create browser and page fixture"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
        playwright.stop()

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_homepage_load_time(self, browser_page):
        """Test homepage load time"""
        start_time = time.time()
        browser_page.goto("http://localhost:1505", timeout=30000)
        load_time = time.time() - start_time
        
        # Homepage should load in less than 3 seconds
        assert load_time < 3.0, f"Homepage took {load_time:.2f}s to load"

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_page_size(self, browser_page):
        """Test page HTML size"""
        browser_page.goto("http://localhost:1505", timeout=30000)
        content = browser_page.content()
        size_kb = len(content.encode('utf-8')) / 1024
        
        # Page should be less than 500KB
        assert size_kb < 500, f"Page size is {size_kb:.2f}KB (too large)"

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_resource_count(self, browser_page):
        """Test number of resources loaded"""
        resources = []
        
        def handle_response(response):
            resources.append(response.url)
        
        browser_page.on("response", handle_response)
        browser_page.goto("http://localhost:1505", timeout=30000)
        browser_page.wait_for_load_state("networkidle")
        
        # Should load reasonable number of resources
        assert len(resources) < 100, f"Too many resources: {len(resources)}"


class TestAPIPerformance:
    """Test API performance"""

    @pytest.fixture(scope="class")
    def api_context(self):
        """Create API request context"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()
        playwright.stop()

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running")
    def test_health_endpoint_performance(self, api_context):
        """Test health endpoint response time"""
        start_time = time.time()
        response = api_context.request.get("http://localhost:1005/api/v1/health")
        elapsed_time = time.time() - start_time
        
        if response.status == 200:
            # Health check should be very fast (< 100ms)
            assert elapsed_time < 0.1, f"Health check took {elapsed_time*1000:.2f}ms"

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires backend server running")
    def test_api_response_size(self, api_context):
        """Test API response size"""
        response = api_context.request.get("http://localhost:1005/api/v1/health")
        if response.status == 200:
            body = response.body()
            size_kb = len(body) / 1024
            
            # Health check response should be small
            assert size_kb < 10, f"Response size is {size_kb:.2f}KB (too large)"


class TestNetworkPerformance:
    """Test network performance metrics"""

    @pytest.fixture(scope="class")
    def browser_page(self):
        """Create browser and page fixture"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()
        playwright.stop()

    @pytest.mark.e2e
    def test_external_site_performance(self, browser_page):
        """Test performance on external site"""
        start_time = time.time()
        browser_page.goto("https://example.com", timeout=30000)
        load_time = time.time() - start_time
        
        # External site should load in reasonable time
        assert load_time < 5.0, f"Site took {load_time:.2f}s to load"

    @pytest.mark.e2e
    @pytest.mark.skip(reason="Requires frontend server running")
    def test_network_requests_timing(self, browser_page):
        """Test network request timing"""
        timings = []
        
        def handle_response(response):
            timing = response.request.timing
            if timing:
                timings.append({
                    'url': response.url,
                    'duration': timing.get('responseEnd', 0) - timing.get('requestStart', 0)
                })
        
        browser_page.on("response", handle_response)
        browser_page.goto("http://localhost:1505", timeout=30000)
        browser_page.wait_for_load_state("networkidle")
        
        if timings:
            avg_duration = sum(t['duration'] for t in timings) / len(timings)
            # Average request should complete in reasonable time
            assert avg_duration < 1.0, f"Average request took {avg_duration:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "e2e"])

