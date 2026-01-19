// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/tests/MonitoringComponentsTest.js
/**
 * اختبارات مكونات المراقبة
 * 
 * هذا الملف يحتوي على اختبارات Playwright للتحقق من صحة مكونات المراقبة
 */

// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('اختبارات مكونات المراقبة', () => {
  test.beforeEach(async ({ page }) => {
    // التنقل إلى صفحة المراقبة قبل كل اختبار
    await page.goto('/monitoring-dashboard');
    // التأكد من تحميل الصفحة بشكل كامل
    await page.waitForSelector('.monitoring-dashboard-container');
  });

  test('يجب أن تعرض لوحة مراقبة الموارد بشكل صحيح', async ({ page }) => {
    // التحقق من وجود العناصر الرئيسية
    await expect(page.locator('.resource-monitoring-title')).toBeVisible();
    await expect(page.locator('.resource-usage-chart')).toBeVisible();
    await expect(page.locator('.metrics-table')).toBeVisible();
  });

  test('يجب أن تعمل مخططات استخدام الموارد بشكل صحيح', async ({ page }) => {
    // التحقق من وجود المخططات
    await expect(page.locator('.resource-usage-chart')).toBeVisible();

    // تغيير نطاق الوقت للمخطط
    await page.selectOption('.time-range-selector', 'last_hour');

    // التحقق من تحديث المخطط
    await expect(page.locator('.chart-loading-indicator')).toBeVisible();
    await expect(page.locator('.chart-loading-indicator')).not.toBeVisible({ timeout: 5000 });
  });

  test('يجب أن تعمل جداول المقاييس بشكل صحيح', async ({ page }) => {
    // التحقق من وجود جدول المقاييس
    await expect(page.locator('.metrics-table')).toBeVisible();

    // البحث عن مقياس
    await page.fill('.metrics-search-input', 'CPU');

    // التحقق من تصفية الجدول
    await expect(page.locator('.metric-row')).toHaveCount(1);

    // إعادة تعيين البحث
    await page.click('.clear-search-button');

    // التحقق من عودة جميع المقاييس
    await expect(page.locator('.metric-row').count()).toBeGreaterThan(1);
  });

  test('يجب أن تعمل جداول العتبات بشكل صحيح', async ({ page }) => {
    // الانتقال إلى علامة تبويب العتبات
    await page.click('.thresholds-tab');

    // التحقق من وجود جدول العتبات
    await expect(page.locator('.thresholds-table')).toBeVisible();

    // فتح نموذج إضافة عتبة جديدة
    await page.click('.add-threshold-button');

    // التحقق من ظهور نموذج العتبة
    await expect(page.locator('.threshold-form-dialog')).toBeVisible();

    // إغلاق النموذج
    await page.click('.close-dialog-button');
  });

  test('يجب أن تعمل نماذج المقاييس بشكل صحيح', async ({ page }) => {
    // فتح نموذج إضافة مقياس جديد
    await page.click('.add-metric-button');

    // التحقق من ظهور نموذج المقياس
    await expect(page.locator('.metric-form-dialog')).toBeVisible();

    // ملء النموذج
    await page.fill('.metric-name-input', 'اختبار المقياس');
    await page.fill('.metric-description-input', 'وصف اختبار المقياس');
    await page.selectOption('.metric-type-select', 'counter');

    // إرسال النموذج
    await page.click('.submit-metric-button');

    // التحقق من إغلاق النموذج
    await expect(page.locator('.metric-form-dialog')).not.toBeVisible({ timeout: 5000 });
  });

  test('يجب أن تعمل لوحة صحة النظام بشكل صحيح', async ({ page }) => {
    // الانتقال إلى لوحة صحة النظام
    await page.click('.system-health-tab');

    // التحقق من وجود العناصر الرئيسية
    await expect(page.locator('.system-health-status')).toBeVisible();
    await expect(page.locator('.system-components-status')).toBeVisible();
    await expect(page.locator('.recent-alerts')).toBeVisible();

    // فتح تفاصيل مكون
    await page.click('.component-item:first-child');

    // التحقق من ظهور تفاصيل المكون
    await expect(page.locator('.component-details')).toBeVisible();
  });

  test('يجب أن تعمل إدارة التنبيهات بشكل صحيح', async ({ page }) => {
    // الانتقال إلى إدارة التنبيهات
    await page.click('.alerts-management-tab');

    // التحقق من وجود العناصر الرئيسية
    await expect(page.locator('.alerts-management')).toBeVisible();
    await expect(page.locator('.alerts-table')).toBeVisible();

    // تصفية التنبيهات
    await page.fill('.search-field input', 'خطأ');

    // التحقق من تصفية الجدول
    await expect(page.locator('.alerts-table .v-data-table__wrapper')).toContainText('خطأ');

    // عرض تفاصيل تنبيه
    await page.click('.alerts-table .v-data-table__wrapper .mdi-information');

    // التحقق من ظهور تفاصيل التنبيه
    await expect(page.locator('.alert-details')).toBeVisible();
  });

  test('يجب أن تعمل لوحة مراقبة الأداء بشكل صحيح', async ({ page }) => {
    // الانتقال إلى لوحة مراقبة الأداء
    await page.click('.performance-dashboard-tab');

    // التحقق من وجود العناصر الرئيسية
    await expect(page.locator('.performance-dashboard')).toBeVisible();
    await expect(page.locator('.performance-charts')).toBeVisible();
    await expect(page.locator('.performance-metrics')).toBeVisible();

    // تغيير نطاق الوقت
    await page.selectOption('.performance-time-range', 'last_day');

    // التحقق من تحديث المخططات
    await expect(page.locator('.performance-loading-indicator')).toBeVisible();
    await expect(page.locator('.performance-loading-indicator')).not.toBeVisible({ timeout: 5000 });
  });

  test('يجب أن تعمل لوحة مراقبة الذكاء الاصطناعي بشكل صحيح', async ({ page }) => {
    // الانتقال إلى لوحة مراقبة الذكاء الاصطناعي
    await page.click('.ai-monitoring-tab');

    // التحقق من وجود العناصر الرئيسية
    await expect(page.locator('.ai-monitoring-dashboard')).toBeVisible();
    await expect(page.locator('.ai-usage-stats')).toBeVisible();
    await expect(page.locator('.ai-cost-chart')).toBeVisible();
    await expect(page.locator('.ai-models-performance')).toBeVisible();

    // تصفية حسب النموذج
    await page.selectOption('.ai-model-filter', 'gpt-4');

    // التحقق من تحديث البيانات
    await expect(page.locator('.ai-loading-indicator')).toBeVisible();
    await expect(page.locator('.ai-loading-indicator')).not.toBeVisible({ timeout: 5000 });
  });
});
