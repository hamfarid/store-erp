/**
 * خدمة تحسين الصور
 * Image Enhancement Service for Frontend
 */

import axios from 'axios';
import { getAuthHeader } from './authService';

const IMAGE_ENHANCEMENT_URL = '/api/image-enhancement';

/**
 * الحصول على طرق التحسين المتاحة
 */
export const getAvailableMethods = async () => {
  try {
    const response = await axios.get(`${IMAGE_ENHANCEMENT_URL}/methods`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في الحصول على طرق التحسين:', error);
    throw error;
  }
};

/**
 * تحسين صورة واحدة
 */
export const enhanceImage = async (imageFile, method = 'auto_enhance', factor = 1.2, returnBase64 = false) => {
  try {
    const formData = new FormData();
    formData.append('file', imageFile);

    const response = await axios.post(`${IMAGE_ENHANCEMENT_URL}/enhance`, formData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'multipart/form-data'
      },
      params: {
        method: method,
        factor: factor,
        return_base64: returnBase64
      },
      responseType: returnBase64 ? 'json' : 'blob'
    });

    if (returnBase64) {
      return response.data;
    } else {
      // إنشاء URL للصورة المحسنة
      const enhancedImageUrl = URL.createObjectURL(response.data);
      return {
        enhanced_image_url: enhancedImageUrl,
        method_used: method,
        factor: factor
      };
    }
  } catch (error) {
    console.error('خطأ في تحسين الصورة:', error);
    throw error;
  }
};

/**
 * فحص صحة خدمة تحسين الصور
 */
export const checkEnhancementHealth = async () => {
  try {
    const response = await axios.get(`${IMAGE_ENHANCEMENT_URL}/health`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في فحص صحة خدمة تحسين الصور:', error);
    throw error;
  }
};

/**
 * تحسين دفعة من الصور
 */
export const enhanceImagesBatch = async (imageFiles, method = 'auto_enhance', factor = 1.2) => {
  try {
    const results = [];
    for (const imageFile of imageFiles) {
      const result = await enhanceImage(imageFile, method, factor, true);
      results.push({
        filename: imageFile.name,
        enhanced_image: result.enhanced_image,
        method_used: result.method_used
      });
    }
    return results;
  } catch (error) {
    console.error('خطأ في تحسين دفعة الصور:', error);
    throw error;
  }
};

