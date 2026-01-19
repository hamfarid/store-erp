/**
 * خدمة YOLO للكشف عن الكائنات
 * YOLO Detection Service for Frontend
 */

import axios from 'axios';
import { getAuthHeader } from './authService';

const YOLO_SERVICE_URL = '/api/yolo-detection';

/**
 * الحصول على النماذج المتاحة
 */
export const getAvailableModels = async () => {
  try {
    const response = await axios.get(`${YOLO_SERVICE_URL}/models`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في الحصول على النماذج المتاحة:', error);
    throw error;
  }
};

/**
 * كشف الكائنات في صورة
 */
export const detectObjects = async (imageFile, modelName = 'general', confidence = 0.5) => {
  try {
    const formData = new FormData();
    formData.append('file', imageFile);
    formData.append('model_name', modelName);
    formData.append('confidence', confidence);

    const response = await axios.post(`${YOLO_SERVICE_URL}/detect`, formData, {
      headers: {
        ...getAuthHeader(),
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في كشف الكائنات:', error);
    throw error;
  }
};

/**
 * فحص صحة خدمة YOLO
 */
export const checkYoloHealth = async () => {
  try {
    const response = await axios.get(`${YOLO_SERVICE_URL}/health`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في فحص صحة خدمة YOLO:', error);
    throw error;
  }
};

/**
 * معالجة دفعة من الصور
 */
export const detectObjectsBatch = async (imageFiles, modelName = 'general', confidence = 0.5) => {
  try {
    const results = [];
    for (const imageFile of imageFiles) {
      const result = await detectObjects(imageFile, modelName, confidence);
      results.push({
        filename: imageFile.name,
        result: result
      });
    }
    return results;
  } catch (error) {
    console.error('خطأ في معالجة دفعة الصور:', error);
    throw error;
  }
};

