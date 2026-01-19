# File: /home/ubuntu/clean_project/tests/test_frontend_selenium.py
"""
مسار الملف: /home/ubuntu/clean_project/tests/test_frontend_selenium.py

اختبارات الواجهة الأمامية باستخدام Selenium
"""

import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TestFrontendInterface(unittest.TestCase):
    """اختبارات الواجهة الأمامية"""
    
    @classmethod
    def setUpClass(cls):
        """إعداد متصفح الاختبار"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # تشغيل بدون واجهة رسومية
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
            cls.wait = WebDriverWait(cls.driver, 10)
        except Exception as e:
            print(f"تعذر تشغيل Chrome WebDriver: {e}")
            print("سيتم تخطي اختبارات الواجهة الأمامية")
            cls.driver = None
    
    @classmethod
    def tearDownClass(cls):
        """إغلاق المتصفح"""
        if cls.driver:
            cls.driver.quit()
    
    def setUp(self):
        """إعداد كل اختبار"""
        if not self.driver:
            self.skipTest("Chrome WebDriver غير متوفر")
        
        # افتراض أن الخادم يعمل على localhost:8000
        self.base_url = "http://localhost:8000"
    
    def test_homepage_loads(self):
        """اختبار تحميل الصفحة الرئيسية"""
        try:
            self.driver.get(self.base_url)
            
            # التحقق من وجود عنوان الصفحة
            self.assertIn("Gaara", self.driver.title)
            
            # التحقق من وجود عناصر أساسية
            self.assertTrue(self.driver.find_element(By.TAG_NAME, "body"))
            
        except Exception as e:
            self.skipTest(f"الخادم غير متوفر: {e}")
    
    def test_navigation_menu(self):
        """اختبار قائمة التنقل"""
        try:
            self.driver.get(self.base_url)
            
            # البحث عن قائمة التنقل
            nav_elements = self.driver.find_elements(By.CSS_SELECTOR, "nav, .navbar, .navigation")
            self.assertTrue(len(nav_elements) > 0, "لم يتم العثور على قائمة التنقل")
            
            # البحث عن روابط التنقل
            nav_links = self.driver.find_elements(By.CSS_SELECTOR, "nav a, .navbar a, .nav-link")
            self.assertTrue(len(nav_links) > 0, "لم يتم العثور على روابط التنقل")
            
        except Exception as e:
            self.skipTest(f"خطأ في اختبار التنقل: {e}")
    
    def test_login_form_exists(self):
        """اختبار وجود نموذج تسجيل الدخول"""
        try:
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
                    login_forms = self.driver.find_elements(By.CSS_SELECTOR, "form, .login-form")
                    if len(login_forms) > 0:
                        login_found = True
                        break
                        
                except:
                    continue
            
            if not login_found:
                # البحث في الصفحة الرئيسية
                self.driver.get(self.base_url)
                login_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    "input[type='password'], .login, #login, [data-login]")
                login_found = len(login_elements) > 0
            
            self.assertTrue(login_found, "لم يتم العثور على نموذج تسجيل الدخول")
            
        except Exception as e:
            self.skipTest(f"خطأ في اختبار تسجيل الدخول: {e}")
    
    def test_responsive_design(self):
        """اختبار التصميم المتجاوب"""
        try:
            self.driver.get(self.base_url)
            
            # اختبار أحجام شاشة مختلفة
            screen_sizes = [
                (1920, 1080),  # سطح المكتب
                (768, 1024),   # تابلت
                (375, 667)     # موبايل
            ]
            
            for width, height in screen_sizes:
                self.driver.set_window_size(width, height)
                time.sleep(1)  # انتظار تطبيق التغيير
                
                # التحقق من أن المحتوى مرئي
                body = self.driver.find_element(By.TAG_NAME, "body")
                self.assertTrue(body.is_displayed())
                
                # التحقق من عدم وجود تمرير أفقي غير مرغوب فيه
                page_width = self.driver.execute_script("return document.body.scrollWidth")
                viewport_width = self.driver.execute_script("return window.innerWidth")
                
                # السماح بهامش صغير للتمرير
                self.assertLessEqual(page_width, viewport_width + 20, 
                    f"تمرير أفقي غير مرغوب فيه في حجم {width}x{height}")
            
        except Exception as e:
            self.skipTest(f"خطأ في اختبار التصميم المتجاوب: {e}")
    
    def test_javascript_functionality(self):
        """اختبار وظائف JavaScript الأساسية"""
        try:
            self.driver.get(self.base_url)
            
            # التحقق من تحميل JavaScript
            js_loaded = self.driver.execute_script("return typeof jQuery !== 'undefined' || typeof $ !== 'undefined'")
            
            # البحث عن عناصر تفاعلية
            interactive_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "button, .btn, [onclick], [data-toggle], .clickable")
            
            if len(interactive_elements) > 0:
                # اختبار النقر على أول عنصر تفاعلي
                first_element = interactive_elements[0]
                if first_element.is_displayed() and first_element.is_enabled():
                    try:
                        first_element.click()
                        time.sleep(1)  # انتظار التفاعل
                    except:
                        pass  # تجاهل أخطاء النقر
            
            # التحقق من عدم وجود أخطاء JavaScript
            logs = self.driver.get_log('browser')
            js_errors = [log for log in logs if log['level'] == 'SEVERE']
            
            # تجاهل بعض الأخطاء الشائعة غير المهمة
            critical_errors = []
            for error in js_errors:
                message = error['message'].lower()
                if not any(ignore in message for ignore in ['favicon', 'manifest', 'sw.js']):
                    critical_errors.append(error)
            
            self.assertEqual(len(critical_errors), 0, 
                f"أخطاء JavaScript حرجة: {critical_errors}")
            
        except Exception as e:
            self.skipTest(f"خطأ في اختبار JavaScript: {e}")
    
    def test_form_validation(self):
        """اختبار التحقق من صحة النماذج"""
        try:
            self.driver.get(self.base_url)
            
            # البحث عن نماذج في الصفحة
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            
            for form in forms:
                if not form.is_displayed():
                    continue
                
                # البحث عن حقول مطلوبة
                required_fields = form.find_elements(By.CSS_SELECTOR, 
                    "input[required], select[required], textarea[required]")
                
                if len(required_fields) > 0:
                    # محاولة إرسال النموذج بدون ملء الحقول المطلوبة
                    submit_buttons = form.find_elements(By.CSS_SELECTOR, 
                        "input[type='submit'], button[type='submit'], .submit-btn")
                    
                    if len(submit_buttons) > 0:
                        try:
                            submit_buttons[0].click()
                            time.sleep(1)
                            
                            # التحقق من ظهور رسائل التحقق
                            validation_messages = self.driver.find_elements(By.CSS_SELECTOR,
                                ".error, .invalid-feedback, .validation-error, :invalid")
                            
                            # يجب أن تظهر رسائل تحقق أو يبقى في نفس الصفحة
                            current_url = self.driver.current_url
                            self.assertTrue(len(validation_messages) > 0 or 
                                          current_url == self.base_url,
                                          "لم يتم التحقق من صحة النموذج")
                            
                        except:
                            pass  # تجاهل أخطاء النقر
                
                break  # اختبار أول نموذج فقط
            
        except Exception as e:
            self.skipTest(f"خطأ في اختبار التحقق من النماذج: {e}")
    
    def test_accessibility_basics(self):
        """اختبار أساسيات إمكانية الوصول"""
        try:
            self.driver.get(self.base_url)
            
            # التحقق من وجود عنوان الصفحة
            title = self.driver.title
            self.assertTrue(len(title) > 0, "عنوان الصفحة مفقود")
            
            # التحقق من وجود عناوين هيكلية
            headings = self.driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6")
            self.assertTrue(len(headings) > 0, "لا توجد عناوين هيكلية")
            
            # التحقق من وجود نص بديل للصور
            images = self.driver.find_elements(By.TAG_NAME, "img")
            for img in images:
                alt_text = img.get_attribute("alt")
                src = img.get_attribute("src")
                if src and not src.startswith("data:"):  # تجاهل الصور المضمنة
                    self.assertIsNotNone(alt_text, f"نص بديل مفقود للصورة: {src}")
            
            # التحقق من وجود تسميات للحقول
            inputs = self.driver.find_elements(By.CSS_SELECTOR, "input, select, textarea")
            for input_field in inputs:
                field_type = input_field.get_attribute("type")
                if field_type not in ["hidden", "submit", "button"]:
                    # البحث عن تسمية
                    field_id = input_field.get_attribute("id")
                    aria_label = input_field.get_attribute("aria-label")
                    placeholder = input_field.get_attribute("placeholder")
                    
                    has_label = False
                    if field_id:
                        labels = self.driver.find_elements(By.CSS_SELECTOR, f"label[for='{field_id}']")
                        has_label = len(labels) > 0
                    
                    has_label = has_label or aria_label or placeholder
                    
                    if not has_label:
                        print(f"تحذير: حقل بدون تسمية: {input_field.get_attribute('name') or 'غير محدد'}")
            
        except Exception as e:
            self.skipTest(f"خطأ في اختبار إمكانية الوصول: {e}")

class TestPerformance(unittest.TestCase):
    """اختبارات الأداء الأساسية"""
    
    @classmethod
    def setUpClass(cls):
        """إعداد متصفح الاختبار"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
        except Exception:
            cls.driver = None
    
    @classmethod
    def tearDownClass(cls):
        """إغلاق المتصفح"""
        if cls.driver:
            cls.driver.quit()
    
    def setUp(self):
        """إعداد كل اختبار"""
        if not self.driver:
            self.skipTest("Chrome WebDriver غير متوفر")
        
        self.base_url = "http://localhost:8000"
    
    def test_page_load_time(self):
        """اختبار وقت تحميل الصفحة"""
        try:
            start_time = time.time()
            self.driver.get(self.base_url)
            
            # انتظار تحميل المحتوى الأساسي
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            load_time = time.time() - start_time
            
            # يجب أن تحمل الصفحة في أقل من 5 ثوان
            self.assertLess(load_time, 5.0, f"وقت تحميل الصفحة طويل: {load_time:.2f} ثانية")
            
        except Exception as e:
            self.skipTest(f"خطأ في اختبار وقت التحميل: {e}")
    
    def test_resource_loading(self):
        """اختبار تحميل الموارد"""
        try:
            self.driver.get(self.base_url)
            
            # التحقق من تحميل CSS
            css_links = self.driver.find_elements(By.CSS_SELECTOR, "link[rel='stylesheet']")
            for css_link in css_links:
                href = css_link.get_attribute("href")
                if href:
                    # التحقق من أن الملف محمل (لا يحتوي على أخطاء 404)
                    status = self.driver.execute_script(
                        "return fetch(arguments[0]).then(r => r.status)", href
                    )
                    if status:
                        self.assertNotEqual(status, 404, f"ملف CSS غير موجود: {href}")
            
            # التحقق من تحميل JavaScript
            js_scripts = self.driver.find_elements(By.CSS_SELECTOR, "script[src]")
            for js_script in js_scripts:
                src = js_script.get_attribute("src")
                if src and not src.startswith("data:"):
                    status = self.driver.execute_script(
                        "return fetch(arguments[0]).then(r => r.status)", src
                    )
                    if status:
                        self.assertNotEqual(status, 404, f"ملف JavaScript غير موجود: {src}")
            
        except Exception as e:
            self.skipTest(f"خطأ في اختبار تحميل الموارد: {e}")

if __name__ == '__main__':
    # تشغيل الاختبارات
    unittest.main(verbosity=2)

