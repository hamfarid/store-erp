/**
 * فحص شامل للأزرار في الواجهة الأمامية
 * ملف: buttonChecker.js
 */

class ButtonChecker {
  constructor() {
    this.results = {
      timestamp: new Date().toISOString(),
      buttons: [],
      summary: {
        totalButtons: 0,
        workingButtons: 0,
        brokenButtons: 0,
        disabledButtons: 0,
        accessibilityIssues: 0
      },
      issues: [],
      recommendations: []
    }
  }

  /**
   * فحص جميع الأزرار في الصفحة
   */
  checkAllButtons() {
    // البحث عن جميع الأزرار
    const buttons = this.findAllButtons()
    
    // فحص كل زر
    buttons.forEach((button, index) => {
      const buttonAnalysis = this.analyzeButton(button, index)
      this.results.buttons.push(buttonAnalysis)
      this.updateSummary(buttonAnalysis)
    })
    
    // إنشاء التوصيات
    this.generateRecommendations()
    
    // عرض النتائج
    this.displayResults()
    
    return this.results
  }

  /**
   * البحث عن جميع الأزرار في الصفحة
   */
  findAllButtons() {
    const selectors = [
      'button',
      'input[type="button"]',
      'input[type="submit"]',
      'input[type="reset"]',
      '[role="button"]',
      '.btn',
      '.button',
      'a[onclick]'
    ]
    
    const allButtons = []
    
    selectors.forEach(selector => {
      const elements = document.querySelectorAll(selector)
      elements.forEach(element => {
        if (!allButtons.includes(element)) {
          allButtons.push(element)
        }
      })
    })
    
    return allButtons
  }

  /**
   * تحليل زر واحد
   */
  analyzeButton(button, index) {
    const analysis = {
      id: index + 1,
      element: button.tagName.toLowerCase(),
      text: this.getButtonText(button),
      type: button.type || 'button',
      disabled: button.disabled,
      visible: this.isVisible(button),
      clickable: this.isClickable(button),
      hasHandler: this.hasEventHandler(button),
      accessibility: this.checkAccessibility(button),
      styling: this.checkStyling(button),
      position: this.getPosition(button),
      issues: [],
      working: false
    }
    
    // تحديد حالة الزر
    analysis.working = analysis.visible && 
                      analysis.clickable && 
                      analysis.hasHandler && 
                      !analysis.disabled
    
    // جمع المشاكل
    this.collectIssues(analysis)
    
    return analysis
  }

  /**
   * الحصول على نص الزر
   */
  getButtonText(button) {
    // محاولة الحصول على النص من مصادر مختلفة
    return button.textContent?.trim() ||
           button.value?.trim() ||
           button.getAttribute('aria-label')?.trim() ||
           button.getAttribute('title')?.trim() ||
           button.getAttribute('alt')?.trim() ||
           'بدون نص'
  }

  /**
   * فحص إذا كان الزر مرئي
   */
  isVisible(button) {
    const style = window.getComputedStyle(button)
    const rect = button.getBoundingClientRect()
    
    return style.display !== 'none' &&
           style.visibility !== 'hidden' &&
           style.opacity !== '0' &&
           rect.width > 0 &&
           rect.height > 0
  }

  /**
   * فحص إذا كان الزر قابل للنقر
   */
  isClickable(button) {
    const style = window.getComputedStyle(button)
    
    return style.pointerEvents !== 'none' &&
           !button.disabled &&
           button.tabIndex !== -1
  }

  /**
   * فحص وجود معالج الأحداث
   */
  hasEventHandler(button) {
    // فحص معالجات الأحداث المختلفة
    const hasOnClick = button.onclick !== null ||
                      button.getAttribute('onclick') !== null
    
    const hasEventListeners = this.hasEventListeners(button)
    
    const hasReactHandler = button.getAttribute('data-reactid') !== null ||
                           button.closest('[data-reactroot]') !== null
    
    return hasOnClick || hasEventListeners || hasReactHandler
  }

  /**
   * فحص وجود Event Listeners
   */
  hasEventListeners(button) {
    try {
      // محاولة فحص Event Listeners (قد لا يعمل في جميع المتصفحات)
      // getEventListeners متاحة فقط في أدوات المطور
      const listeners = (typeof window !== 'undefined' && window.getEventListeners) ? window.getEventListeners(button) : {}
      return Object.keys(listeners).length > 0
    } catch {
      // إذا فشل، نفترض وجود معالجات إذا كان الزر في تطبيق React
      return button.closest('[data-reactroot]') !== null
    }
  }

  /**
   * فحص إمكانية الوصول
   */
  checkAccessibility(button) {
    const issues = []
    let score = 100
    
    // فحص النص
    const text = this.getButtonText(button)
    if (!text || text === 'بدون نص') {
      issues.push('لا يوجد نص واضح للزر')
      score -= 30
    } else if (text.length < 2) {
      issues.push('نص الزر قصير جداً')
      score -= 15
    }
    
    // فحص ARIA attributes
    if (!button.getAttribute('aria-label') && !button.getAttribute('aria-labelledby')) {
      if (!text || text === 'بدون نص') {
        issues.push('لا يوجد aria-label')
        score -= 20
      }
    }
    
    // فحص التباين
    const contrast = this.checkColorContrast(button)
    if (contrast.ratio < 4.5) {
      issues.push(`تباين ألوان ضعيف: ${contrast.ratio.toFixed(2)}`)
      score -= 25
    }
    
    // فحص الحجم
    const rect = button.getBoundingClientRect()
    if (rect.width < 44 || rect.height < 44) {
      issues.push('حجم الزر صغير جداً (أقل من 44px)')
      score -= 15
    }
    
    // فحص Focus
    if (!this.canReceiveFocus(button)) {
      issues.push('لا يمكن التركيز على الزر')
      score -= 20
    }
    
    return {
      score: Math.max(0, score),
      issues: issues,
      accessible: score >= 70
    }
  }

  /**
   * فحص تباين الألوان
   */
  checkColorContrast(button) {
    try {
      const style = window.getComputedStyle(button)
      const bgColor = style.backgroundColor
      const textColor = style.color
      
      // تحويل الألوان إلى RGB
      const bg = this.parseColor(bgColor)
      const text = this.parseColor(textColor)
      
      // حساب التباين
      const ratio = this.calculateContrastRatio(bg, text)
      
      return {
        ratio: ratio,
        background: bgColor,
        text: textColor,
        adequate: ratio >= 4.5
      }
    } catch {
      return { ratio: 0, adequate: false }
    }
  }

  /**
   * تحويل لون إلى RGB
   */
  parseColor(color) {
    const div = document.createElement('div')
    div.style.color = color
    document.body.appendChild(div)
    
    const computedColor = window.getComputedStyle(div).color
    document.body.removeChild(div)
    
    const match = computedColor.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/)
    if (match) {
      return {
        r: parseInt(match[1]),
        g: parseInt(match[2]),
        b: parseInt(match[3])
      }
    }
    
    return { r: 0, g: 0, b: 0 }
  }

  /**
   * حساب نسبة التباين
   */
  calculateContrastRatio(color1, color2) {
    const l1 = this.getLuminance(color1)
    const l2 = this.getLuminance(color2)
    
    const lighter = Math.max(l1, l2)
    const darker = Math.min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)
  }

  /**
   * حساب الإضاءة النسبية
   */
  getLuminance(color) {
    const { r, g, b } = color
    
    const [rs, gs, bs] = [r, g, b].map(c => {
      c = c / 255
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
    })
    
    return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs
  }

  /**
   * فحص إذا كان يمكن التركيز على الزر
   */
  canReceiveFocus(button) {
    return button.tabIndex >= 0 && 
           !button.disabled &&
           button.style.display !== 'none'
  }

  /**
   * فحص التنسيق
   */
  checkStyling(button) {
    const style = window.getComputedStyle(button)
    
    return {
      hasBackground: style.backgroundColor !== 'rgba(0, 0, 0, 0)',
      hasBorder: style.borderWidth !== '0px',
      hasPadding: style.padding !== '0px',
      hasMargin: style.margin !== '0px',
      cursor: style.cursor,
      fontSize: style.fontSize,
      fontWeight: style.fontWeight
    }
  }

  /**
   * الحصول على موقع الزر
   */
  getPosition(button) {
    const rect = button.getBoundingClientRect()
    
    return {
      x: Math.round(rect.left),
      y: Math.round(rect.top),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
      inViewport: rect.top >= 0 && 
                  rect.left >= 0 && 
                  rect.bottom <= window.innerHeight && 
                  rect.right <= window.innerWidth
    }
  }

  /**
   * جمع المشاكل
   */
  collectIssues(analysis) {
    if (!analysis.visible) {
      analysis.issues.push('الزر غير مرئي')
    }
    
    if (!analysis.clickable) {
      analysis.issues.push('الزر غير قابل للنقر')
    }
    
    if (!analysis.hasHandler) {
      analysis.issues.push('لا يوجد معالج أحداث')
    }
    
    if (analysis.disabled) {
      analysis.issues.push('الزر معطل')
    }
    
    if (!analysis.accessibility.accessible) {
      analysis.issues.push('مشاكل في إمكانية الوصول')
    }
    
    if (!analysis.position.inViewport) {
      analysis.issues.push('خارج منطقة العرض')
    }
  }

  /**
   * تحديث الملخص
   */
  updateSummary(analysis) {
    this.results.summary.totalButtons++
    
    if (analysis.working) {
      this.results.summary.workingButtons++
    } else {
      this.results.summary.brokenButtons++
    }
    
    if (analysis.disabled) {
      this.results.summary.disabledButtons++
    }
    
    if (!analysis.accessibility.accessible) {
      this.results.summary.accessibilityIssues++
    }
  }

  /**
   * إنشاء التوصيات
   */
  generateRecommendations() {
    const { summary } = this.results
    
    if (summary.brokenButtons > 0) {
      this.results.recommendations.push(
        `إصلاح ${summary.brokenButtons} زر لا يعمل بشكل صحيح`
      )
    }
    
    if (summary.accessibilityIssues > 0) {
      this.results.recommendations.push(
        `تحسين إمكانية الوصول لـ ${summary.accessibilityIssues} زر`
      )
    }
    
    const workingPercentage = (summary.workingButtons / summary.totalButtons) * 100
    
    if (workingPercentage < 80) {
      this.results.recommendations.push(
        'تحسين معدل الأزرار العاملة (أقل من 80%)'
      )
    }
    
    // فحص الأزرار بدون نص
    const buttonsWithoutText = this.results.buttons.filter(
      btn => btn.text === 'بدون نص'
    ).length
    
    if (buttonsWithoutText > 0) {
      this.results.recommendations.push(
        `إضافة نصوص واضحة لـ ${buttonsWithoutText} زر`
      )
    }
  }

  /**
   * عرض النتائج
   */
  displayResults() {
    const { summary } = this.results
    
    if (summary.totalButtons > 0) {
      const workingPercentage = (summary.workingButtons / summary.totalButtons) * 100
      console.log(`Button success rate: ${workingPercentage.toFixed(1)}%`)
      
      if (workingPercentage >= 90) {
        console.log('Excellent: Most buttons working!')
      } else if (workingPercentage >= 70) {
        console.log('Good: Some buttons need attention')
      } else {
        console.log('Needs work: Many buttons need fixing')
      }
    }
    
    // عرض التوصيات
    if (this.results.recommendations.length > 0) {
      this.results.recommendations.forEach(rec => {
        console.log(`Recommendation: ${rec}`)
      })
    }
    
    // عرض الأزرار المعطلة
    const brokenButtons = this.results.buttons.filter(btn => !btn.working)
    if (brokenButtons.length > 0) {
      brokenButtons.slice(0, 5).forEach(btn => {
        console.log(`Broken button: ${btn.id || btn.text}`)
      })
    }
  }

  /**
   * اختبار زر محدد
   */
  testButton(button) {
    console.log(`Testing button: "${button.textContent || button.id}"`)
    
    try {
      // محاولة النقر على الزر
      const clickEvent = new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window
      })
      
      button.dispatchEvent(clickEvent)
      return true
    } catch (error) {
      return false
    }
  }

  /**
   * اختبار جميع الأزرار
   */
  testAllButtons() {
    const buttons = this.findAllButtons()
    let successCount = 0
    
    buttons.forEach((button, _index) => {
      const buttonText = this.getButtonText(button)
      
      // تخطي الأزرار الخطيرة
      if (this.isDangerousButton(button, buttonText)) {
        return
      }
      
      if (this.testButton(button)) {
        successCount++
      }
      
      // انتظار قصير بين الاختبارات
      setTimeout(() => {}, 100)
    })
    
    return {
      total: buttons.length,
      working: successCount,
      percentage: (successCount / buttons.length) * 100
    }
  }

  /**
   * فحص إذا كان الزر خطير
   */
  isDangerousButton(button, text) {
    const dangerousKeywords = [
      'delete', 'remove', 'حذف', 'إزالة',
      'logout', 'تسجيل خروج', 'خروج',
      'reset', 'إعادة تعيين',
      'clear', 'مسح'
    ]
    
    const textLower = text.toLowerCase()
    const hasClass = button.className.toLowerCase()
    
    return dangerousKeywords.some(keyword => 
      textLower.includes(keyword) || hasClass.includes(keyword)
    )
  }

  /**
   * حفظ النتائج
   */
  saveResults() {
    const resultsJson = JSON.stringify(this.results, null, 2)
    const blob = new Blob([resultsJson], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    
    const a = document.createElement('a')
    a.href = url
    a.download = `button_check_results_${new Date().toISOString().slice(0, 10)}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    
    }
}

// إنشاء مثيل عام
const buttonChecker = new ButtonChecker()

// دوال سريعة للاستخدام
window.checkAllButtons = () => {
  const results = buttonChecker.checkAllButtons()
  buttonChecker.saveResults()
  return results
}

window.testAllButtons = () => {
  return buttonChecker.testAllButtons()
}

window.checkButton = (selector) => {
  const button = document.querySelector(selector)
  if (button) {
    return buttonChecker.analyzeButton(button, 0)
  } else {
    return null
  }
}

// Usage examples:
// const checker = new ButtonChecker()
// checker.checkAllButtons() - لفحص جميع الأزرار
// checker.runAllTests() - لاختبار جميع الأزرار
// checker.testButton(btn) - لفحص زر محدد

export default ButtonChecker
