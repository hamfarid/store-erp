import React, { createContext, useContext, useState, useEffect } from 'react';
import ApiService from '../services/ApiService';

const DataContext = createContext();

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};

export const DataProvider = ({ children }) => {
  const [farms, setFarms] = useState([]);
  const [crops, setCrops] = useState([]);
  const [users, setUsers] = useState([]);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // تحميل البيانات الأساسية
  const loadInitialData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [farmsData, cropsData, usersData] = await Promise.all([
        ApiService.getFarms().catch(() => ({ farms: [] })),
        ApiService.getCrops().catch(() => ({ crops: [] })),
        ApiService.getUsers().catch(() => ({ users: [] }))
      ]);

      setFarms(farmsData.farms || []);
      setCrops(cropsData.crops || []);
      setUsers(usersData.users || []);
    } catch (error) {
      console.error('خطأ في تحميل البيانات الأساسية:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // تحديث المزارع
  const refreshFarms = async () => {
    try {
      const response = await ApiService.getFarms();
      setFarms(response.farms || []);
    } catch (error) {
      console.error('خطأ في تحديث المزارع:', error);
    }
  };

  // تحديث المحاصيل
  const refreshCrops = async () => {
    try {
      const response = await ApiService.getCrops();
      setCrops(response.crops || []);
    } catch (error) {
      console.error('خطأ في تحديث المحاصيل:', error);
    }
  };

  // تحديث المستخدمين
  const refreshUsers = async () => {
    try {
      const response = await ApiService.getUsers();
      setUsers(response.users || []);
    } catch (error) {
      console.error('خطأ في تحديث المستخدمين:', error);
    }
  };

  // إضافة مزرعة جديدة
  const addFarm = async (farmData) => {
    try {
      const response = await ApiService.createFarm(farmData);
      await refreshFarms();
      return { success: true, data: response };
    } catch (error) {
      console.error('خطأ في إضافة المزرعة:', error);
      return { success: false, error: error.message };
    }
  };

  // إضافة محصول جديد
  const addCrop = async (cropData) => {
    try {
      const response = await ApiService.createCrop(cropData);
      await refreshCrops();
      return { success: true, data: response };
    } catch (error) {
      console.error('خطأ في إضافة المحصول:', error);
      return { success: false, error: error.message };
    }
  };

  // إضافة مستخدم جديد
  const addUser = async (userData) => {
    try {
      const response = await ApiService.createUser(userData);
      await refreshUsers();
      return { success: true, data: response };
    } catch (error) {
      console.error('خطأ في إضافة المستخدم:', error);
      return { success: false, error: error.message };
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  const value = {
    // البيانات
    farms,
    crops,
    users,
    reports,
    loading,
    error,
    
    // الوظائف
    loadInitialData,
    refreshFarms,
    refreshCrops,
    refreshUsers,
    addFarm,
    addCrop,
    addUser,
    
    // إعداد البيانات مباشرة (للاستخدام الداخلي)
    setFarms,
    setCrops,
    setUsers,
    setReports,
    setError
  };

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};
