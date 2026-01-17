/**
 * نظام التشفير للواجهة الأمامية
 * ملف: encryption.js
 */

import CryptoJS from 'crypto-js'

class FrontendEncryption {
  constructor() {
    // مفتاح التشفير (يجب أن يكون آمناً في الإنتاج)
    this.encryptionKey = this.generateOrLoadKey()
    this.apiKey = localStorage.getItem('api_key') || null
    this.apiSecret = localStorage.getItem('api_secret') || null
  }

  /**
   * إنشاء أو تحميل مفتاح التشفير
   */
  generateOrLoadKey() {
    let key = sessionStorage.getItem('encryption_key')
    
    if (!key) {
      // إنشاء مفتاح جديد
      key = CryptoJS.lib.WordArray.random(256/8).toString()
      sessionStorage.setItem('encryption_key', key)
    }
    
    return key
  }

  /**
   * تشفير النص باستخدام AES
   */
  encryptText(text) {
    try {
      if (!text) return null
      
      const encrypted = CryptoJS.AES.encrypt(
        JSON.stringify(text), 
        this.encryptionKey
      ).toString()
      
      return encrypted
    } catch (error) {
      return null
    }
  }

  /**
   * فك تشفير النص
   */
  decryptText(encryptedText) {
    try {
      if (!encryptedText) return null
      
      const bytes = CryptoJS.AES.decrypt(encryptedText, this.encryptionKey)
      const decrypted = bytes.toString(CryptoJS.enc.Utf8)
      
      return JSON.parse(decrypted)
    } catch (error) {
      return null
    }
  }

  /**
   * تشفير كائن JSON
   */
  encryptObject(obj) {
    try {
      const jsonString = JSON.stringify(obj)
      return this.encryptText(jsonString)
    } catch (error) {
      return null
    }
  }

  /**
   * فك تشفير كائن JSON
   */
  decryptObject(encryptedObj) {
    try {
      const decryptedString = this.decryptText(encryptedObj)
      return JSON.parse(decryptedString)
    } catch (error) {
      return null
    }
  }

  /**
   * تشفير بيانات النموذج
   */
  encryptFormData(formData) {
    try {
      const sensitiveFields = [
        'password', 'email', 'phone', 'address', 
        'national_id', 'credit_card', 'bank_account'
      ]
      
      const encryptedData = { ...formData }
      
      sensitiveFields.forEach(field => {
        if (encryptedData[field]) {
          encryptedData[field] = this.encryptText(encryptedData[field])
        }
      })
      
      return encryptedData
    } catch (error) {
      return formData
    }
  }

  /**
   * فك تشفير بيانات النموذج
   */
  decryptFormData(encryptedFormData) {
    try {
      const sensitiveFields = [
        'password', 'email', 'phone', 'address', 
        'national_id', 'credit_card', 'bank_account'
      ]
      
      const decryptedData = { ...encryptedFormData }
      
      sensitiveFields.forEach(field => {
        if (decryptedData[field]) {
          const decrypted = this.decryptText(decryptedData[field])
          if (decrypted) {
            decryptedData[field] = decrypted
          }
        }
      })
      
      return decryptedData
    } catch (error) {
      return encryptedFormData
    }
  }

  /**
   * إنشاء توقيع HMAC للطلب
   */
  createRequestSignature(method, url, body, timestamp) {
    try {
      if (!this.apiSecret) {
        return null
      }
      
      const stringToSign = `${method}\n${url}\n${body}\n${timestamp}`
      const signature = CryptoJS.HmacSHA256(stringToSign, this.apiSecret).toString()
      
      return signature
    } catch (error) {
      return null
    }
  }

  /**
   * تشفير طلب API
   */
  encryptApiRequest(data) {
    try {
      const timestamp = Date.now().toString()
      const requestId = this.generateRequestId()
      
      const encryptedData = this.encryptObject(data)
      
      const requestPackage = {
        encrypted_data: encryptedData,
        timestamp: timestamp,
        request_id: requestId,
        version: '1.0'
      }
      
      return requestPackage
    } catch (error) {
      return null
    }
  }

  /**
   * فك تشفير استجابة API
   */
  decryptApiResponse(encryptedResponse) {
    try {
      if (!encryptedResponse || typeof encryptedResponse !== 'object') {
        return null
      }
      
      // فحص الطابع الزمني
      const responseTime = parseInt(encryptedResponse.timestamp)
      const currentTime = Date.now()
      
      // انتهاء الصلاحية خلال 10 دقائق
      if (currentTime - responseTime > 600000) {
        return null
      }
      
      // فك تشفير البيانات
      const decryptedData = this.decryptObject(encryptedResponse.encrypted_data)
      
      return decryptedData
    } catch (error) {
      return null
    }
  }

  /**
   * إنشاء معرف فريد للطلب
   */
  generateRequestId() {
    return CryptoJS.lib.WordArray.random(128/8).toString()
  }

  /**
   * تشفير التخزين المحلي
   */
  setSecureStorage(key, value) {
    try {
      const encryptedValue = this.encryptObject(value)
      localStorage.setItem(key, encryptedValue)
      return true
    } catch (error) {
      return false
    }
  }

  /**
   * فك تشفير التخزين المحلي
   */
  getSecureStorage(key) {
    try {
      const encryptedValue = localStorage.getItem(key)
      if (!encryptedValue) return null
      
      return this.decryptObject(encryptedValue)
    } catch (error) {
      return null
    }
  }

  /**
   * تشفير كلمة المرور
   */
  hashPassword(password) {
    try {
      // إضافة ملح عشوائي
      const salt = CryptoJS.lib.WordArray.random(128/8)
      const hash = CryptoJS.PBKDF2(password, salt, {
        keySize: 256/32,
        iterations: 10000
      })
      
      return {
        hash: hash.toString(),
        salt: salt.toString()
      }
    } catch (error) {
      return null
    }
  }

  /**
   * التحقق من كلمة المرور
   */
  verifyPassword(password, storedHash, storedSalt) {
    try {
      const salt = CryptoJS.enc.Hex.parse(storedSalt)
      const hash = CryptoJS.PBKDF2(password, salt, {
        keySize: 256/32,
        iterations: 10000
      })
      
      return hash.toString() === storedHash
    } catch (error) {
      return false
    }
  }

  /**
   * تنظيف البيانات الحساسة من الذاكرة
   */
  clearSensitiveData() {
    try {
      // مسح مفاتيح التشفير من الذاكرة
      sessionStorage.removeItem('encryption_key')
      localStorage.removeItem('api_key')
      localStorage.removeItem('api_secret')
      
      // إعادة تعيين المتغيرات
      this.encryptionKey = null
      this.apiKey = null
      this.apiSecret = null
      
      } catch (error) {
      }
  }

  /**
   * فحص قوة كلمة المرور
   */
  checkPasswordStrength(password) {
    const checks = {
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      numbers: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    }
    
    const score = Object.values(checks).filter(Boolean).length
    
    let strength = 'ضعيف'
    if (score >= 4) strength = 'قوي'
    else if (score >= 3) strength = 'متوسط'
    
    return {
      score,
      strength,
      checks
    }
  }

  /**
   * إنشاء كلمة مرور آمنة
   */
  generateSecurePassword(length = 12) {
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    let password = ''
    
    for (let i = 0; i < length; i++) {
      const randomIndex = Math.floor(Math.random() * charset.length)
      password += charset[randomIndex]
    }
    
    return password
  }
}

// إنشاء مثيل عام
const encryption = new FrontendEncryption()

export default encryption
export { FrontendEncryption }
