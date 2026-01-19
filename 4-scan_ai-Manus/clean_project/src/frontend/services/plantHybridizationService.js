/**
 * خدمة تهجين النباتات
 * Plant Hybridization Service for Frontend
 */

import axios from 'axios';
import { getAuthHeader } from './authService';

const HYBRIDIZATION_URL = '/api/plant-hybridization';

/**
 * الحصول على أصناف النباتات المتاحة
 */
export const getAvailableVarieties = async () => {
  try {
    const response = await axios.get(`${HYBRIDIZATION_URL}/varieties`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في الحصول على أصناف النباتات:', error);
    throw error;
  }
};

/**
 * الحصول على الصفات المتاحة
 */
export const getAvailableTraits = async () => {
  try {
    const response = await axios.get(`${HYBRIDIZATION_URL}/traits`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في الحصول على الصفات المتاحة:', error);
    throw error;
  }
};

/**
 * تنفيذ عملية تهجين
 */
export const hybridizePlants = async (hybridizationRequest) => {
  try {
    const response = await axios.post(`${HYBRIDIZATION_URL}/hybridize`, hybridizationRequest, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في عملية التهجين:', error);
    throw error;
  }
};

/**
 * الحصول على تاريخ عمليات التهجين
 */
export const getHybridizationHistory = async () => {
  try {
    const response = await axios.get(`${HYBRIDIZATION_URL}/history`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في الحصول على تاريخ التهجين:', error);
    throw error;
  }
};

/**
 * فحص صحة خدمة التهجين
 */
export const checkHybridizationHealth = async () => {
  try {
    const response = await axios.get(`${HYBRIDIZATION_URL}/health`, {
      headers: getAuthHeader()
    });
    return response.data;
  } catch (error) {
    console.error('خطأ في فحص صحة خدمة التهجين:', error);
    throw error;
  }
};

