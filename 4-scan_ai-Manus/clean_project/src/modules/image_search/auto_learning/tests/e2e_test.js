# /home/ubuntu/image_search_integration/auto_learning/tests/e2e_test.js

/**
 * اختبارات التكامل الشامل End-to-End للبحث الذاتي الذكي
 * 
 * هذا الملف يحتوي على اختبارات التكامل الشامل بين جميع مكونات نظام البحث الذاتي الذكي
 * باستخدام بيانات تجريبية للتأكد من عمل النظام بشكل متكامل في بيئة حقيقية.
 */

import { createPage, startBrowser, closeBrowser } from 'playwright';
import axios from 'axios';

// بيانات تجريبية للاختبارات
const TEST_DATA = {
  keywords: [
    { text: 'طماطم', category: 'PLANT', synonyms: ['بندورة'] },
    { text: 'تبقع أوراق', category: 'DISEASE', plant_parts: ['ورقة'] },
    { text: 'ري بالتنقيط', category: 'TECHNIQUE' }
  ],
  sources: [
    { domain: 'agri-research.org', category: 'ACADEMIC', trust_level: 90, description: 'موقع أبحاث زراعية أكاديمي' },
    { domain: 'plant-diseases.com', category: 'EDUCATIONAL', trust_level: 80, description: 'موقع تعليمي عن أمراض النباتات' }
  ],
  search_engines: [
    { name: 'Google', type: 'GENERAL', base_url: 'https://www.google.com/search', query_param: 'q', priority: 1 },
    { name: 'Bing Images', type: 'IMAGE', base_url: 'https://www.bing.com/images/search', query_param: 'q', priority: 2 }
  ]
};

// إعدادات API
const API_URL = process.env.API_URL || 'http://localhost:8000/api/v1';
const API_TOKEN = process.env.API_TOKEN || 'test_token';

// إعدادات الاختبار
const TEST_CONFIG = {
  baseUrl: process.env.BASE_URL || 'http://localhost:8080',
  headless: process.env.HEADLESS !== 'false',
  slowMo: parseInt(process.env.SLOW_MO || '50', 10)
};

describe('نظام البحث الذاتي الذكي - اختبارات التكامل الشامل', () => {
  let browser;
  let page;
  let apiClient;
  
  beforeAll(async () => {
    // إعداد متصفح Playwright
    browser = await startBrowser({
      headless: TEST_CONFIG.headless,
      slowMo: TEST_CONFIG.slowMo
    });
    
    // إعداد عميل API
    apiClient = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_TOKEN}`
      }
    });
    
    // تهيئة بيانات الاختبار
    await setupTestData();
  });
  
  beforeEach(async () => {
    // إنشاء صفحة جديدة لكل اختبار
    page = await browser.newPage();
    
    // تسجيل الدخول
    await login(page);
  });
  
  afterEach(async () => {
    await page.close();
  });
  
  afterAll(async () => {
    // تنظيف بيانات الاختبار
    await cleanupTestData();
    
    // إغلاق المتصفح
    await closeBrowser(browser);
  });
  
  /**
   * تهيئة بيانات الاختبار عبر API
   */
  async function setupTestData() {
    try {
      // إضافة الكلمات المفتاحية
      for (const keyword of TEST_DATA.keywords) {
        await apiClient.post('/auto_learning/keywords', keyword);
      }
      
      // إضافة المصادر
      for (const source of TEST_DATA.sources) {
        await apiClient.post('/auto_learning/sources', source);
      }
      
      // إضافة محركات البحث
      for (const engine of TEST_DATA.search_engines) {
        await apiClient.post('/auto_learning/search_engines', engine);
      }
      
      console.log('تم إعداد بيانات الاختبار بنجاح');
    } catch (error) {
      console.error('خطأ في إعداد بيانات الاختبار:', error);
      throw error;
    }
  }
  
  /**
   * تنظيف بيانات الاختبار بعد الانتهاء
   */
  async function cleanupTestData() {
    try {
      // الحصول على قائمة الكلمات المفتاحية وحذفها
      const keywordsResponse = await apiClient.get('/auto_learning/keywords');
      for (const keyword of keywordsResponse.data.keywords) {
        await apiClient.delete(`/auto_learning/keywords/${keyword.id}`);
      }
      
      // الحصول على قائمة المصادر وحذفها
      const sourcesResponse = await apiClient.get('/auto_learning/sources');
      for (const source of sourcesResponse.data.sources) {
        await apiClient.delete(`/auto_learning/sources/${source.id}`);
      }
      
      // الحصول على قائمة محركات البحث وحذفها
      const enginesResponse = await apiClient.get('/auto_learning/search_engines');
      for (const engine of enginesResponse.data.search_engines) {
        await apiClient.delete(`/auto_learning/search_engines/${engine.id}`);
      }
      
      console.log('تم تنظيف بيانات الاختبار بنجاح');
    } catch (error) {
      console.error('خطأ في تنظيف بيانات الاختبار:', error);
    }
  }
  
  /**
   * تسجيل الدخول إلى النظام
   */
  async function login(page) {
    await page.goto(`${TEST_CONFIG.baseUrl}/login`);
    
    // ملء نموذج تسجيل الدخول
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', 'admin123');
    await page.click('button[type="submit"]');
    
    // انتظار الانتقال إلى الصفحة الرئيسية
    await page.waitForNavigation();
    
    // التحقق من نجاح تسجيل الدخول
    const logoutButton = await page.$('text=تسجيل الخروج');
    expect(logoutButton).toBeTruthy();
  }
  
  test('يجب أن يعرض لوحة التحكم الرئيسية بشكل صحيح', async () => {
    await page.goto(`${TEST_CONFIG.baseUrl}/dashboard`);
    
    // التحقق من وجود العناصر الرئيسية
    await expect(page.locator('h1:has-text("لوحة التحكم")')).toBeVisible();
    await expect(page.locator('a:has-text("إدارة الكلمات المفتاحية")')).toBeVisible();
    await expect(page.locator('a:has-text("إدارة المصادر الموثوقة")')).toBeVisible();
    await expect(page.locator('a:has-text("إدارة محركات البحث")')).toBeVisible();
  });
  
  describe('إدارة الكلمات المفتاحية', () => {
    test('يجب أن يعرض قائمة الكلمات المفتاحية بشكل صحيح', async () => {
      await page.goto(`${TEST_CONFIG.baseUrl}/keywords`);
      
      // التحقق من وجود العناصر الرئيسية
      await expect(page.locator('h5:has-text("إدارة الكلمات المفتاحية")')).toBeVisible();
      
      // التحقق من وجود الكلمات المفتاحية التجريبية
      await expect(page.locator('td:has-text("طماطم")')).toBeVisible();
      await expect(page.locator('td:has-text("تبقع أوراق")')).toBeVisible();
      await expect(page.locator('td:has-text("ري بالتنقيط")')).toBeVisible();
    });
    
    test('يجب أن يضيف كلمة مفتاحية جديدة بنجاح', async () => {
      await page.goto(`${TEST_CONFIG.baseUrl}/keywords`);
      
      // النقر على زر إضافة كلمة مفتاحية
      await page.click('button:has-text("إضافة كلمة مفتاحية")');
      
      // ملء نموذج الإضافة
      await page.fill('input#text', 'سماد عضوي');
      await page.selectOption('select#category', 'FERTILIZER');
      await page.check('input#is_active');
      
      // حفظ الكلمة المفتاحية
      await page.click('button:has-text("حفظ")');
      
      // انتظار إغلاق النافذة المنبثقة
      await page.waitForSelector('.modal', { state: 'hidden' });
      
      // التحقق من ظهور رسالة النجاح
      await expect(page.locator('.toast-success')).toBeVisible();
      
      // التحقق من إضافة الكلمة المفتاحية للقائمة
      await expect(page.locator('td:has-text("سماد عضوي")')).toBeVisible();
    });
    
    test('يجب أن يعدل كلمة مفتاحية موجودة بنجاح', async () => {
      await page.goto(`${TEST_CONFIG.baseUrl}/keywords`);
      
      // البحث عن الكلمة المفتاحية
      await page.fill('input[placeholder="بحث عن كلمة مفتاحية..."]', 'طماطم');
      await page.waitForTimeout(500); // انتظار تحديث القائمة
      
      // النقر على زر التعديل
      await page.click('td:has-text("طماطم") ~ td button.btn-outline-primary');
      
      // تعديل الكلمة المفتاحية
      await page.fill('input#text', 'طماطم حمراء');
      
      // حفظ التعديلات
      await page.click('button:has-text("حفظ")');
      
      // انتظار إغلاق النافذة المنبثقة
      await page.waitForSelector('.modal', { state: 'hidden' });
      
      // التحقق من ظهور رسالة النجاح
      await expect(page.locator('.toast-success')).toBeVisible();
      
      // التحقق من تحديث الكلمة المفتاحية في القائمة
      await expect(page.locator('td:has-text("طماطم حمراء")')).toBeVisible();
    });
  });
  
  describe('إدارة المصادر الموثوقة', () => {
    test('يجب أن يعرض قائمة المصادر بشكل صحيح', async () => {
      await page.goto(`${TEST_CONFIG.baseUrl}/sources`);
      
      // التحقق من وجود العناصر الرئيسية
      await expect(page.locator('h5:has-text("إدارة المصادر الموثوقة")')).toBeVisible();
      
      // التحقق من وجود المصادر التجريبية
      await expect(page.locator('td:has-text("agri-research.org")')).toBeVisible();
      await expect(page.locator('td:has-text("plant-diseases.com")')).toBeVisible();
    });
    
    test('يجب أن يتحقق من مصدر بنجاح', async () => {
      await page.goto(`${TEST_CONFIG.baseUrl}/sources`);
      
      // البحث عن المصدر
      await page.fill('input[placeholder="بحث بالنطاق أو الوصف..."]', 'agri-research');
      await page.waitForTimeout(500); // انتظار تحديث القائمة
      
      // النقر على زر التحقق
      await page.click('td:has-text("agri-research.org") ~ td button.btn-outline-info');
      
      // النقر على زر بدء التحقق
      await page.click('button:has-text("بدء التحقق")');
      
      // انتظار اكتمال عملية التحقق
      await page.waitForSelector('.alert-success');
      
      // التحقق من ظهور نتائج التحقق
      await expect(page.locator('text=تم اختبار محرك البحث بنجاح')).toBeVisible();
      
      // تطبيق نتائج التحقق
      await page.click('button:has-text("تطبيق النتائج")');
      
      // التحقق من ظهور رسالة النجاح
      await expect(page.locator('.toast-success')).toBeVisible();
    });
  });
  
  describe('إدارة محركات البحث', () => {
    test('يجب أن يعرض قائمة محركات البحث بشكل صحيح', async () => {
      await page.goto(`${TEST_CONFIG.baseUrl}/search-engines`);
      
      // التحقق من وجود العناصر الرئيسية
      await expect(page.locator('h5:has-text("إدارة محركات البحث")')).toBeVisible();
      
      // التحقق من وجود محركات البحث التجريبية
      await expect(page.locator('td:has-text("Google")')).toBeVisible();
      await expect(page.locator('td:has-text("Bing Images")')).toBeVisible();
    });
    
    test('يجب أن يختبر محرك بحث بنجاح', async () => {
      await page.goto(`${TEST_CONFIG.baseUrl}/search-engines`);
      
      // البحث عن محرك البحث
      await page.fill('input[placeholder="بحث بالاسم أو URL..."]', 'Google');
      await page.waitForTimeout(500); // انتظار تحديث القائمة
      
      // النقر على زر الاختبار
      await page.click('td:has-text("Google") ~ td button.btn-outline-info');
      
      // إدخال استعلام الاختبار
      await page.fill('input#test_query', 'الزراعة الذكية');
      
      // النقر على زر البحث
      await page.click('button:has-text("بحث")');
      
      // انتظار ظهور النتائج
      await page.waitForSelector('.alert-success, .alert-warning');
      
      // التحقق من ظهور نتائج الاختبار أو رسالة عدم وجود نتائج
      const successAlert = await page.$('.alert-success');
      const warningAlert = await page.$('.alert-warning');
      expect(successAlert || warningAlert).toBeTruthy();
    });
  });
  
  describe('اختبارات التكامل الشامل', () => {
    test('يجب أن يعمل تدفق العمل الكامل لإضافة كلمة مفتاحية وربطها بمصدر ثم البحث عنها', async () => {
      // 1. إضافة كلمة مفتاحية جديدة
      await page.goto(`${TEST_CONFIG.baseUrl}/keywords`);
      await page.click('button:has-text("إضافة كلمة مفتاحية")');
      await page.fill('input#text', 'مكافحة حيوية');
      await page.selectOption('select#category', 'TECHNIQUE');
      await page.check('input#is_active');
      await page.click('button:has-text("حفظ")');
      await page.waitForSelector('.modal', { state: 'hidden' });
      await expect(page.locator('.toast-success')).toBeVisible();
      
      // 2. الانتقال إلى صفحة المصادر
      await page.goto(`${TEST_CONFIG.baseUrl}/sources`);
      
      // 3. إضافة مصدر جديد
      await page.click('button:has-text("إضافة مصدر")');
      await page.fill('input#domain', 'biocontrol-info.org');
      await page.selectOption('select#category', 'EDUCATIONAL');
      await page.fill('textarea#description', 'موقع معلومات عن المكافحة الحيوية');
      await page.fill('input#trust_level', '85');
      await page.click('button:has-text("حفظ")');
      await page.waitForSelector('.modal', { state: 'hidden' });
      await expect(page.locator('.toast-success')).toBeVisible();
      
      // 4. الانتقال إلى صفحة البحث
      await page.goto(`${TEST_CONFIG.baseUrl}/search`);
      
      // 5. إجراء بحث باستخدام الكلمة المفتاحية الجديدة
      await page.fill('input[placeholder="أدخل كلمات البحث..."]', 'مكافحة حيوية');
      await page.click('button:has-text("بحث")');
      
      // 6. انتظار ظهور نتائج البحث
      await page.waitForSelector('.search-results');
      
      // 7. التحقق من وجود نتائج أو رسالة عدم وجود نتائج
      const resultsCount = await page.$$eval('.search-result-item', items => items.length);
      const noResultsMessage = await page.$('.no-results-message');
      
      expect(resultsCount > 0 || noResultsMessage).toBeTruthy();
    });
  });
});
