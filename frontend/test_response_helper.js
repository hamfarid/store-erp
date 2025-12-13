/**
 * اختبار دوال responseHelper
 * 
 * تشغيل: node test_response_helper.js
 */

// استيراد الدوال المساعدة
import {
  isSuccess,
  isError,
  getData,
  getErrorMessage,
  normalizeResponse,
  getStatus,
  ok
} from './src/utils/responseHelper.js'

// ألوان للطباعة
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
  reset: '\x1b[0m'
}

let passedTests = 0
let failedTests = 0

function test(name, fn) {
  try {
    fn()
    console.log(`${colors.green}✓${colors.reset} ${name}`)
    passedTests++
  } catch (error) {
    console.log(`${colors.red}✗${colors.reset} ${name}`)
    console.log(`  ${colors.red}${error.message}${colors.reset}`)
    failedTests++
  }
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message || 'Assertion failed')
  }
}

function assertEqual(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(message || `Expected ${expected}, got ${actual}`)
  }
}

console.log(`\n${colors.blue}=== اختبار دوال responseHelper ===${colors.reset}\n`)

// ==================== اختبارات isSuccess ====================
console.log(`${colors.yellow}اختبارات isSuccess:${colors.reset}`)

test('isSuccess - الصيغة الجديدة (success)', () => {
  const response = { status: 'success', data: [] }
  assert(isSuccess(response), 'يجب أن يرجع true للصيغة الجديدة')
})

test('isSuccess - الصيغة القديمة (success: true)', () => {
  const response = { success: true, data: [] }
  assert(isSuccess(response), 'يجب أن يرجع true للصيغة القديمة')
})

test('isSuccess - الصيغة الجديدة (error)', () => {
  const response = { status: 'error', message: 'خطأ' }
  assert(!isSuccess(response), 'يجب أن يرجع false للخطأ')
})

test('isSuccess - الصيغة القديمة (success: false)', () => {
  const response = { success: false, message: 'خطأ' }
  assert(!isSuccess(response), 'يجب أن يرجع false للصيغة القديمة')
})

test('isSuccess - رد فارغ', () => {
  assert(!isSuccess(null), 'يجب أن يرجع false للرد الفارغ')
  assert(!isSuccess(undefined), 'يجب أن يرجع false للرد غير المعرف')
  assert(!isSuccess({}), 'يجب أن يرجع false للكائن الفارغ')
})

// ==================== اختبارات isError ====================
console.log(`\n${colors.yellow}اختبارات isError:${colors.reset}`)

test('isError - الصيغة الجديدة (error)', () => {
  const response = { status: 'error', message: 'خطأ' }
  assert(isError(response), 'يجب أن يرجع true للخطأ')
})

test('isError - الصيغة القديمة (success: false)', () => {
  const response = { success: false, message: 'خطأ' }
  assert(isError(response), 'يجب أن يرجع true للصيغة القديمة')
})

test('isError - الصيغة الجديدة (success)', () => {
  const response = { status: 'success', data: [] }
  assert(!isError(response), 'يجب أن يرجع false للنجاح')
})

// ==================== اختبارات getData ====================
console.log(`\n${colors.yellow}اختبارات getData:${colors.reset}`)

test('getData - استخراج البيانات', () => {
  const response = { status: 'success', data: [1, 2, 3] }
  const data = getData(response)
  assert(Array.isArray(data), 'يجب أن يرجع مصفوفة')
  assertEqual(data.length, 3, 'يجب أن يرجع 3 عناصر')
})

test('getData - قيمة افتراضية', () => {
  const response = { status: 'success' }
  const data = getData(response, [])
  assert(Array.isArray(data), 'يجب أن يرجع المصفوفة الافتراضية')
  assertEqual(data.length, 0, 'يجب أن تكون فارغة')
})

test('getData - رد فارغ', () => {
  const data = getData(null, 'default')
  assertEqual(data, 'default', 'يجب أن يرجع القيمة الافتراضية')
})

// ==================== اختبارات getErrorMessage ====================
console.log(`\n${colors.yellow}اختبارات getErrorMessage:${colors.reset}`)

test('getErrorMessage - رسالة خطأ موجودة', () => {
  const response = { status: 'error', message: 'خطأ في الاتصال' }
  const msg = getErrorMessage(response)
  assertEqual(msg, 'خطأ في الاتصال', 'يجب أن يرجع رسالة الخطأ')
})

test('getErrorMessage - رسالة افتراضية', () => {
  const response = { status: 'error' }
  const msg = getErrorMessage(response, 'خطأ افتراضي')
  assertEqual(msg, 'خطأ افتراضي', 'يجب أن يرجع الرسالة الافتراضية')
})

test('getErrorMessage - حقل error بدلاً من message', () => {
  const response = { status: 'error', error: 'خطأ آخر' }
  const msg = getErrorMessage(response)
  assertEqual(msg, 'خطأ آخر', 'يجب أن يرجع من حقل error')
})

// ==================== اختبارات normalizeResponse ====================
console.log(`\n${colors.yellow}اختبارات normalizeResponse:${colors.reset}`)

test('normalizeResponse - تحويل من success إلى status', () => {
  const response = { success: true, data: [] }
  const normalized = normalizeResponse(response)
  assert('status' in normalized, 'يجب أن يحتوي على status')
  assertEqual(normalized.status, 'success', 'يجب أن يكون success')
  assert(!('success' in normalized), 'يجب ألا يحتوي على success')
})

test('normalizeResponse - تحويل من success: false إلى status: error', () => {
  const response = { success: false, message: 'خطأ' }
  const normalized = normalizeResponse(response)
  assertEqual(normalized.status, 'error', 'يجب أن يكون error')
})

test('normalizeResponse - الحفاظ على الصيغة الجديدة', () => {
  const response = { status: 'success', data: [] }
  const normalized = normalizeResponse(response)
  assertEqual(normalized.status, 'success', 'يجب أن يبقى كما هو')
})

test('normalizeResponse - رد فارغ', () => {
  const normalized = normalizeResponse(null)
  assertEqual(normalized.status, 'error', 'يجب أن يرجع error للرد الفارغ')
})

// ==================== اختبارات getStatus ====================
console.log(`\n${colors.yellow}اختبارات getStatus:${colors.reset}`)

test('getStatus - الصيغة الجديدة', () => {
  const response = { status: 'success' }
  assertEqual(getStatus(response), 'success', 'يجب أن يرجع success')
})

test('getStatus - الصيغة القديمة (true)', () => {
  const response = { success: true }
  assertEqual(getStatus(response), 'success', 'يجب أن يرجع success')
})

test('getStatus - الصيغة القديمة (false)', () => {
  const response = { success: false }
  assertEqual(getStatus(response), 'error', 'يجب أن يرجع error')
})

test('getStatus - رد غير معروف', () => {
  assertEqual(getStatus({}), 'unknown', 'يجب أن يرجع unknown')
})

// ==================== اختبارات ok (اختصار) ====================
console.log(`\n${colors.yellow}اختبارات ok:${colors.reset}`)

test('ok - يجب أن يعمل مثل isSuccess', () => {
  const response = { status: 'success' }
  assert(ok(response), 'يجب أن يرجع true')
  assertEqual(ok(response), isSuccess(response), 'يجب أن يكون مطابقاً لـ isSuccess')
})

// ==================== اختبارات التوافق العكسي ====================
console.log(`\n${colors.yellow}اختبارات التوافق العكسي:${colors.reset}`)

test('التوافق - رد من Backend قديم', () => {
  const oldResponse = { success: true, data: { id: 1, name: 'منتج' } }
  assert(isSuccess(oldResponse), 'يجب أن يتعرف على الصيغة القديمة')
  const data = getData(oldResponse)
  assert(data.id === 1, 'يجب أن يستخرج البيانات بشكل صحيح')
})

test('التوافق - رد من Backend جديد', () => {
  const newResponse = { status: 'success', data: { id: 1, name: 'منتج' } }
  assert(isSuccess(newResponse), 'يجب أن يتعرف على الصيغة الجديدة')
  const data = getData(newResponse)
  assert(data.id === 1, 'يجب أن يستخرج البيانات بشكل صحيح')
})

test('التوافق - تطبيع ثم فحص', () => {
  const oldResponse = { success: true, data: [] }
  const normalized = normalizeResponse(oldResponse)
  assert(isSuccess(normalized), 'يجب أن ينجح بعد التطبيع')
  assertEqual(normalized.status, 'success', 'يجب أن يحتوي على status')
})

// ==================== النتائج ====================
console.log(`\n${colors.blue}=== النتائج ===${colors.reset}`)
console.log(`${colors.green}✓ نجح: ${passedTests}${colors.reset}`)
console.log(`${colors.red}✗ فشل: ${failedTests}${colors.reset}`)
console.log(`${colors.blue}المجموع: ${passedTests + failedTests}${colors.reset}`)

if (failedTests === 0) {
  console.log(`\n${colors.green}🎉 جميع الاختبارات نجحت!${colors.reset}\n`)
  process.exit(0)
} else {
  console.log(`\n${colors.red}❌ بعض الاختبارات فشلت${colors.reset}\n`)
  process.exit(1)
}

