// File: /home/ubuntu/gaara_scan_ai_final_4.2/src/frontend/components/tests/AIComponentsTest.js
/**
 * اختبارات مكونات الذكاء الاصطناعي
 * 
 * هذا الملف يحتوي على اختبارات Playwright للتحقق من صحة مكونات الذكاء الاصطناعي
 */

// @ts-check
const { test, expect } = require('@playwright/test');

test.describe('اختبارات مكونات الذكاء الاصطناعي', () => {
  test.beforeEach(async ({ page }) => {
    // التنقل إلى صفحة الذكاء الاصطناعي قبل كل اختبار
    await page.goto('/ai-dashboard');
    // التأكد من تحميل الصفحة بشكل كامل
    await page.waitForSelector('.ai-dashboard-container');
  });

  test('يجب أن يعرض لوحة معلومات الذكاء الاصطناعي بشكل صحيح', async ({ page }) => {
    // التحقق من وجود العناصر الرئيسية
    await expect(page.locator('.ai-dashboard-title')).toBeVisible();
    await expect(page.locator('.ai-agents-list')).toBeVisible();
    await expect(page.locator('.ai-stats-container')).toBeVisible();
  });

  test('يجب أن يعمل منتقي نماذج الذكاء الاصطناعي بشكل صحيح', async ({ page }) => {
    // فتح منتقي النماذج
    await page.click('.ai-model-selector-button');

    // التحقق من ظهور قائمة النماذج
    await expect(page.locator('.ai-model-list')).toBeVisible();

    // اختيار نموذج
    await page.click('.ai-model-item:first-child');

    // التحقق من تحديث النموذج المحدد
    await expect(page.locator('.selected-model-name')).toBeVisible();
  });

  test('يجب أن تعمل محادثة الذكاء الاصطناعي بشكل صحيح', async ({ page }) => {
    // فتح محادثة جديدة
    await page.click('.new-chat-button');

    // كتابة رسالة
    await page.fill('.chat-input', 'مرحباً، كيف يمكنني مساعدتك؟');

    // إرسال الرسالة
    await page.click('.send-message-button');

    // التحقق من ظهور الرسالة في المحادثة
    await expect(page.locator('.chat-message-text').last()).toContainText('مرحباً');
  });

  test('يجب أن يعمل أفتار الذكاء الاصطناعي بشكل صحيح', async ({ page }) => {
    // التحقق من وجود الأفتار
    await expect(page.locator('.ai-avatar-container')).toBeVisible();

    // التحقق من تغير حالة الأفتار عند التفكير
    await page.fill('.chat-input', 'ما هو تقرير المبيعات لهذا الشهر؟');
    await page.click('.send-message-button');

    // التحقق من ظهور حالة التفكير
    await expect(page.locator('.ai-avatar-thinking')).toBeVisible({ timeout: 5000 });
  });

  test('يجب أن تعمل بطاقة وكيل الذكاء الاصطناعي بشكل صحيح', async ({ page }) => {
    // التحقق من وجود بطاقات الوكلاء
    await expect(page.locator('.ai-agent-card')).toBeVisible();

    // فتح تفاصيل الوكيل
    await page.click('.ai-agent-card:first-child .view-details-button');

    // التحقق من ظهور تفاصيل الوكيل
    await expect(page.locator('.agent-details-dialog')).toBeVisible();

    // إغلاق التفاصيل
    await page.click('.close-details-button');
  });

  test('يجب أن تعمل قائمة وكلاء الذكاء الاصطناعي بشكل صحيح', async ({ page }) => {
    // التحقق من وجود قائمة الوكلاء
    await expect(page.locator('.ai-agent-list')).toBeVisible();

    // البحث عن وكيل
    await page.fill('.agent-search-input', 'مساعد');

    // التحقق من تصفية القائمة
    await expect(page.locator('.ai-agent-card')).toHaveCount(1);

    // إعادة تعيين البحث
    await page.click('.clear-search-button');

    // التحقق من عودة جميع الوكلاء
    const agentCount = await page.locator('.ai-agent-card').count();
    expect(agentCount, 'Expected more than one agent card').toBeGreaterThan(1);
  });

  test('يجب أن تعمل لوحة أوامر الذكاء الاصطناعي بشكل صحيح', async ({ page }) => {
    // التحقق من وجود لوحة الأوامر
    await expect(page.locator('.ai-command-panel')).toBeVisible();

    // اختيار أمر سريع
    await page.click('.quick-command:first-child');

    // التحقق من إضافة الأمر إلى حقل الإدخال
    await expect(page.locator('.command-input')).toHaveValue();

    // إرسال الأمر
    await page.click('.execute-command-button');

    // التحقق من ظهور نتيجة الأمر
    await expect(page.locator('.command-result')).toBeVisible({ timeout: 5000 });
  });

  test('should render AI component correctly', async ({ page }) => {
    await page.goto('/ai-component');
    await expect(page.locator('[data-testid="ai-component"]')).toBeVisible();
  });
});
