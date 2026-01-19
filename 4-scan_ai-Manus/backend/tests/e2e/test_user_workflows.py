"""
FILE: backend/tests/e2e/test_user_workflows.py | PURPOSE: E2E user workflow tests | OWNER: QA Team | LAST-AUDITED: 2025-11-18

End-to-End Tests for User Workflows

Tests for:
- User registration and login
- Farm management
- Disease diagnosis
- Report generation
- Profile management

Version: 1.0.0
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "ar-SA",  # Arabic locale
    }


class TestUserRegistrationAndLogin:
    """Test user registration and login workflows"""
    
    @pytest.mark.e2e
    def test_user_registration_flow(self, page: Page):
        """Test complete user registration flow"""
        # Navigate to registration page
        page.goto("http://localhost:3000/register")
        
        # Fill registration form
        page.fill('input[name="name"]', "Test User")
        page.fill('input[name="email"]', "testuser@example.com")
        page.fill('input[name="password"]', "MyStr0ng!P@ssw0rd")
        page.fill('input[name="confirmPassword"]', "MyStr0ng!P@ssw0rd")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for redirect to dashboard or verification page
        page.wait_for_url("**/dashboard", timeout=5000)
        
        # Verify user is logged in
        expect(page.locator('text=مرحباً')).to_be_visible()
    
    @pytest.mark.e2e
    def test_user_login_flow(self, page: Page):
        """Test user login flow"""
        # Navigate to login page
        page.goto("http://localhost:3000/login")
        
        # Fill login form
        page.fill('input[name="email"]', "testuser@example.com")
        page.fill('input[name="password"]', "MyStr0ng!P@ssw0rd")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Wait for redirect to dashboard
        page.wait_for_url("**/dashboard", timeout=5000)
        
        # Verify dashboard is loaded
        expect(page.locator('h1')).to_contain_text("لوحة التحكم")
    
    @pytest.mark.e2e
    def test_login_with_invalid_credentials(self, page: Page):
        """Test login with invalid credentials"""
        page.goto("http://localhost:3000/login")
        
        # Fill with invalid credentials
        page.fill('input[name="email"]', "invalid@example.com")
        page.fill('input[name="password"]', "WrongPassword123!")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify error message
        expect(page.locator('text=خطأ')).to_be_visible()
    
    @pytest.mark.e2e
    def test_logout_flow(self, page: Page):
        """Test user logout flow"""
        # Login first
        page.goto("http://localhost:3000/login")
        page.fill('input[name="email"]', "testuser@example.com")
        page.fill('input[name="password"]', "MyStr0ng!P@ssw0rd")
        page.click('button[type="submit"]')
        page.wait_for_url("**/dashboard")
        
        # Logout
        page.click('button[aria-label="تسجيل الخروج"]')
        
        # Verify redirect to login
        page.wait_for_url("**/login")


class TestFarmManagement:
    """Test farm management workflows"""
    
    @pytest.fixture(autouse=True)
    def login(self, page: Page):
        """Login before each test"""
        page.goto("http://localhost:3000/login")
        page.fill('input[name="email"]', "testuser@example.com")
        page.fill('input[name="password"]', "MyStr0ng!P@ssw0rd")
        page.click('button[type="submit"]')
        page.wait_for_url("**/dashboard")
    
    @pytest.mark.e2e
    def test_create_farm(self, page: Page):
        """Test farm creation workflow"""
        # Navigate to farms page
        page.click('a[href="/farms"]')
        page.wait_for_url("**/farms")
        
        # Click create farm button
        page.click('button:has-text("إضافة مزرعة")')
        
        # Fill farm form
        page.fill('input[name="name"]', "Test Farm")
        page.fill('input[name="location"]', "Test Location")
        page.fill('input[name="area"]', "100")
        
        # Submit form
        page.click('button[type="submit"]')
        
        # Verify farm is created
        expect(page.locator('text=Test Farm')).to_be_visible()
    
    @pytest.mark.e2e
    def test_view_farm_details(self, page: Page):
        """Test viewing farm details"""
        # Navigate to farms page
        page.click('a[href="/farms"]')
        page.wait_for_url("**/farms")
        
        # Click on a farm
        page.click('text=Test Farm')
        
        # Verify farm details are displayed
        expect(page.locator('h1')).to_contain_text("Test Farm")
        expect(page.locator('text=Test Location')).to_be_visible()


class TestDiseaseDiagnosis:
    """Test disease diagnosis workflows"""
    
    @pytest.fixture(autouse=True)
    def login(self, page: Page):
        """Login before each test"""
        page.goto("http://localhost:3000/login")
        page.fill('input[name="email"]', "testuser@example.com")
        page.fill('input[name="password"]', "MyStr0ng!P@ssw0rd")
        page.click('button[type="submit"]')
        page.wait_for_url("**/dashboard")
    
    @pytest.mark.e2e
    def test_upload_image_for_diagnosis(self, page: Page):
        """Test uploading image for disease diagnosis"""
        # Navigate to diagnosis page
        page.click('a[href="/diagnosis"]')
        page.wait_for_url("**/diagnosis")
        
        # Upload image
        page.set_input_files('input[type="file"]', 'tests/fixtures/plant_image.jpg')
        
        # Wait for upload
        expect(page.locator('text=تم رفع الصورة')).to_be_visible()
        
        # Click analyze button
        page.click('button:has-text("تحليل")')
        
        # Wait for results
        expect(page.locator('text=النتائج')).to_be_visible(timeout=10000)
    
    @pytest.mark.e2e
    def test_view_diagnosis_history(self, page: Page):
        """Test viewing diagnosis history"""
        # Navigate to diagnosis history
        page.click('a[href="/diagnosis/history"]')
        page.wait_for_url("**/diagnosis/history")
        
        # Verify history is displayed
        expect(page.locator('h1')).to_contain_text("سجل التشخيص")


class TestReportGeneration:
    """Test report generation workflows"""
    
    @pytest.fixture(autouse=True)
    def login(self, page: Page):
        """Login before each test"""
        page.goto("http://localhost:3000/login")
        page.fill('input[name="email"]', "testuser@example.com")
        page.fill('input[name="password"]', "MyStr0ng!P@ssw0rd")
        page.click('button[type="submit"]')
        page.wait_for_url("**/dashboard")
    
    @pytest.mark.e2e
    def test_generate_pdf_report(self, page: Page):
        """Test PDF report generation"""
        # Navigate to reports page
        page.click('a[href="/reports"]')
        page.wait_for_url("**/reports")
        
        # Select report type
        page.select_option('select[name="reportType"]', "farm_summary")
        
        # Click generate button
        page.click('button:has-text("إنشاء تقرير")')
        
        # Wait for download
        with page.expect_download() as download_info:
            page.click('button:has-text("تحميل PDF")')
        
        download = download_info.value
        assert download.suggested_filename.endswith('.pdf')


@pytest.mark.e2e
def test_complete_user_journey(page: Page):
    """Test complete user journey from registration to report generation"""
    # 1. Register
    page.goto("http://localhost:3000/register")
    page.fill('input[name="name"]', "Journey User")
    page.fill('input[name="email"]', "journey@example.com")
    page.fill('input[name="password"]', "MyStr0ng!P@ssw0rd")
    page.fill('input[name="confirmPassword"]', "MyStr0ng!P@ssw0rd")
    page.click('button[type="submit"]')
    page.wait_for_url("**/dashboard")
    
    # 2. Create farm
    page.click('a[href="/farms"]')
    page.click('button:has-text("إضافة مزرعة")')
    page.fill('input[name="name"]', "Journey Farm")
    page.fill('input[name="location"]', "Journey Location")
    page.fill('input[name="area"]', "50")
    page.click('button[type="submit"]')
    
    # 3. Diagnose disease
    page.click('a[href="/diagnosis"]')
    page.set_input_files('input[type="file"]', 'tests/fixtures/plant_image.jpg')
    page.click('button:has-text("تحليل")')
    expect(page.locator('text=النتائج')).to_be_visible(timeout=10000)
    
    # 4. Generate report
    page.click('a[href="/reports"]')
    page.select_option('select[name="reportType"]', "farm_summary")
    page.click('button:has-text("إنشاء تقرير")')
    
    # 5. Logout
    page.click('button[aria-label="تسجيل الخروج"]')
    page.wait_for_url("**/login")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-m', 'e2e'])

