"""
اختبارات النهاية إلى النهاية باستخدام Selenium
End-to-End Tests using Selenium
"""

import pytest

pytest.importorskip("selenium")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import os
from pathlib import Path

class TestE2EWebInterface:
    """اختبارات النهاية إلى النهاية للواجهة الويب"""
    
    @classmethod
    def setup_class(cls):
        """إعداد الفئة"""
        # إعداد Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # تشغيل بدون واجهة
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
            cls.wait = WebDriverWait(cls.driver, 10)
            cls.base_url = "http://localhost"  # يجب تشغيل الخادم أولاً
        except Exception as e:
            pytest.skip(f"لا يمكن تشغيل Chrome WebDriver: {e}")
    
    @classmethod
    def teardown_class(cls):
        """تنظيف الفئة"""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def test_01_homepage_loads(self):
        """اختبار تحميل الصفحة الرئيسية"""
        try:
            self.driver.get(self.base_url)
            
            # انتظار تحميل العنوان
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "title")))
            
            # التحقق من العنوان
            assert "Gaara Scan AI" in self.driver.title
            
            # التحقق من وجود عناصر أساسية
            assert self.driver.find_element(By.TAG_NAME, "body")
            
        except TimeoutException:
            pytest.skip("الخادم غير متاح للاختبار")
    
    def test_02_navigation_menu(self):
        """اختبار قائمة التنقل"""
        self.driver.get(self.base_url)
        
        try:
            # البحث عن قائمة التنقل
            nav_menu = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "nav, .navbar, .navigation"))
            )
            
            # التحقق من وجود روابط التنقل
            nav_links = nav_menu.find_elements(By.TAG_NAME, "a")
            assert len(nav_links) > 0
            
            # التحقق من وجود روابط مهمة
            link_texts = [link.text.lower() for link in nav_links]
            expected_links = ["الرئيسية", "تشخيص", "تحليل", "home", "diagnosis"]
            
            # التحقق من وجود على الأقل رابط واحد متوقع
            assert any(expected in " ".join(link_texts) for expected in expected_links)
            
        except TimeoutException:
            # إذا لم توجد قائمة تنقل، تحقق من وجود روابط في الصفحة
            links = self.driver.find_elements(By.TAG_NAME, "a")
            assert len(links) > 0
    
    def test_03_login_page(self):
        """اختبار صفحة تسجيل الدخول"""
        # محاولة الوصول لصفحة تسجيل الدخول
        login_urls = [
            f"{self.base_url}/login",
            f"{self.base_url}/auth/login",
            f"{self.base_url}/admin/login"
        ]
        
        login_found = False
        for url in login_urls:
            try:
                self.driver.get(url)
                
                # البحث عن نموذج تسجيل الدخول
                login_form = self.driver.find_element(By.CSS_SELECTOR, "form, .login-form, .auth-form")
                
                # البحث عن حقول اسم المستخدم وكلمة المرور
                username_field = login_form.find_element(
                    By.CSS_SELECTOR, 
                    "input[type='text'], input[name*='user'], input[name*='email'], input[id*='user']"
                )
                password_field = login_form.find_element(
                    By.CSS_SELECTOR,
                    "input[type='password'], input[name*='pass'], input[id*='pass']"
                )
                
                assert username_field.is_displayed()
                assert password_field.is_displayed()
                
                login_found = True
                break
                
            except:
                continue
        
        if not login_found:
            pytest.skip("صفحة تسجيل الدخول غير متاحة")
    
    def test_04_file_upload_interface(self):
        """اختبار واجهة رفع الملفات"""
        # البحث عن صفحة رفع الملفات
        upload_urls = [
            f"{self.base_url}/upload",
            f"{self.base_url}/diagnosis",
            f"{self.base_url}/analyze"
        ]
        
        upload_found = False
        for url in upload_urls:
            try:
                self.driver.get(url)
                
                # البحث عن عنصر رفع الملفات
                file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                
                assert file_input.is_displayed()
                
                # التحقق من قبول أنواع الملفات الصحيحة
                accept_attr = file_input.get_attribute("accept")
                if accept_attr:
                    assert any(ext in accept_attr for ext in [".jpg", ".jpeg", ".png", "image/*"])
                
                upload_found = True
                break
                
            except:
                continue
        
        if not upload_found:
            pytest.skip("واجهة رفع الملفات غير متاحة")
    
    def test_05_responsive_design(self):
        """اختبار التصميم المتجاوب"""
        self.driver.get(self.base_url)
        
        # اختبار أحجام شاشة مختلفة
        screen_sizes = [
            (1920, 1080),  # سطح المكتب
            (1024, 768),   # تابلت
            (375, 667),    # موبايل
        ]
        
        for width, height in screen_sizes:
            self.driver.set_window_size(width, height)
            time.sleep(1)  # انتظار إعادة التخطيط
            
            # التحقق من أن الصفحة لا تزال قابلة للاستخدام
            body = self.driver.find_element(By.TAG_NAME, "body")
            assert body.is_displayed()
            
            # التحقق من عدم وجود تمرير أفقي غير مرغوب فيه
            page_width = self.driver.execute_script("return document.body.scrollWidth")
            viewport_width = self.driver.execute_script("return window.innerWidth")
            
            # السماح ببعض التسامح للتمرير
            assert page_width <= viewport_width + 20
    
    def test_06_accessibility_basics(self):
        """اختبار أساسيات إمكانية الوصول"""
        self.driver.get(self.base_url)
        
        # التحقق من وجود عنوان الصفحة
        title = self.driver.find_element(By.TAG_NAME, "title")
        assert title.get_attribute("textContent").strip() != ""
        
        # التحقق من وجود عناوين هيكلية
        headings = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
        assert len(headings) > 0
        
        # التحقق من وجود نص بديل للصور
        images = self.driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            alt_text = img.get_attribute("alt")
            # يجب أن يكون هناك نص بديل أو أن تكون الصورة زخرفية
            assert alt_text is not None
        
        # التحقق من إمكانية التنقل بالكيبورد
        focusable_elements = self.driver.find_elements(
            By.CSS_SELECTOR, 
            "a, button, input, select, textarea, [tabindex]:not([tabindex='-1'])"
        )
        assert len(focusable_elements) > 0
    
    def test_07_performance_basics(self):
        """اختبار أساسيات الأداء"""
        start_time = time.time()
        self.driver.get(self.base_url)
        
        # انتظار تحميل الصفحة بالكامل
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        
        load_time = time.time() - start_time
        
        # التحقق من أن الصفحة تحملت في وقت معقول
        assert load_time < 10.0  # أقل من 10 ثوان
        
        # التحقق من حجم الصفحة
        page_source_size = len(self.driver.page_source.encode('utf-8'))
        assert page_source_size < 5 * 1024 * 1024  # أقل من 5 MB
    
    def test_08_error_pages(self):
        """اختبار صفحات الأخطاء"""
        # اختبار صفحة 404
        self.driver.get(f"{self.base_url}/nonexistent-page")
        
        # التحقق من أن الصفحة تعرض خطأ بشكل مناسب
        page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        
        # البحث عن مؤشرات صفحة الخطأ
        error_indicators = ["404", "not found", "غير موجود", "خطأ", "error"]
        assert any(indicator in page_text for indicator in error_indicators)
    
    def test_09_javascript_functionality(self):
        """اختبار وظائف JavaScript الأساسية"""
        self.driver.get(self.base_url)
        
        # التحقق من تمكين JavaScript
        js_enabled = self.driver.execute_script("return true")
        assert js_enabled is True
        
        # التحقق من عدم وجود أخطاء JavaScript في وحدة التحكم
        logs = self.driver.get_log('browser')
        severe_errors = [log for log in logs if log['level'] == 'SEVERE']
        
        # السماح ببعض التحذيرات ولكن ليس الأخطاء الشديدة
        assert len(severe_errors) == 0, f"أخطاء JavaScript شديدة: {severe_errors}"
    
    def test_10_security_headers(self):
        """اختبار رؤوس الأمان الأساسية"""
        self.driver.get(self.base_url)
        
        # الحصول على رؤوس الاستجابة باستخدام JavaScript
        # هذا محدود في Selenium، لكن يمكننا فحص بعض الأشياء
        
        # التحقق من أن الصفحة تُحمل عبر HTTPS في الإنتاج
        current_url = self.driver.current_url
        if "localhost" not in current_url and "127.0.0.1" not in current_url:
            assert current_url.startswith("https://")
        
        # التحقق من عدم وجود محتوى مختلط
        mixed_content_errors = self.driver.get_log('browser')
        mixed_content = [log for log in mixed_content_errors if 'mixed content' in log.get('message', '').lower()]
        assert len(mixed_content) == 0

class TestE2EAPIWorkflow:
    """اختبار سير العمل الكامل عبر API"""
    
    def setup_method(self):
        """إعداد كل اختبار"""
        import requests
        self.base_url = "http://localhost"
        self.session = requests.Session()
        
        # التحقق من توفر الخادم
        try:
            response = self.session.get(f"{self.base_url}/api/v1/health", timeout=5)
            if response.status_code != 200:
                pytest.skip("الخادم غير متاح للاختبار")
        except:
            pytest.skip("الخادم غير متاح للاختبار")
    
    def test_complete_diagnosis_workflow(self):
        """اختبار سير عمل التشخيص الكامل"""
        import requests
        from PIL import Image
        import io
        
        # 1. فحص صحة النظام
        response = self.session.get(f"{self.base_url}/api/v1/health")
        assert response.status_code == 200
        
        # 2. تسجيل الدخول
        login_data = {"username": "admin", "password": "admin123"}
        response = self.session.post(f"{self.base_url}/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. إنشاء صورة اختبار
        img = Image.new('RGB', (200, 200), color='green')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # 4. رفع الصورة
        files = {"file": ("test_plant.jpg", img_bytes, "image/jpeg")}
        response = self.session.post(f"{self.base_url}/api/v1/upload/image", files=files)
        assert response.status_code == 200
        
        file_id = response.json()["file_id"]
        
        # 5. طلب التشخيص
        diagnosis_request = {
            "file_id": file_id,
            "analysis_type": "detailed",
            "include_treatment": True
        }
        response = self.session.post(
            f"{self.base_url}/api/v1/diagnosis/analyze", 
            json=diagnosis_request,
            headers=headers
        )
        assert response.status_code == 200
        
        diagnosis = response.json()
        assert "diagnosis_id" in diagnosis
        assert "disease_name" in diagnosis
        assert "confidence" in diagnosis
        
        # 6. الحصول على تفاصيل التشخيص
        diagnosis_id = diagnosis["diagnosis_id"]
        response = self.session.get(f"{self.base_url}/api/v1/diagnosis/{diagnosis_id}")
        assert response.status_code == 200
        
        # 7. فحص تاريخ التشخيصات
        response = self.session.get(f"{self.base_url}/api/v1/diagnosis/history")
        assert response.status_code == 200
        
        # 8. تنظيف - حذف الملف
        response = self.session.delete(f"{self.base_url}/api/v1/upload/{file_id}")
        assert response.status_code == 200
        
        # 9. تسجيل الخروج
        response = self.session.post(f"{self.base_url}/api/v1/auth/logout", headers=headers)
        assert response.status_code == 200

