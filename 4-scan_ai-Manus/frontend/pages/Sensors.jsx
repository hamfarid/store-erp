/**
 * Sensors Page - IoT Sensor Management & Monitoring
 * ==================================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  Thermometer, Droplet, Sun, Wind, Gauge, Activity, Plus, Search,
  RefreshCw, MoreVertical, Eye, Edit, Trash2, AlertTriangle, Check,
  Signal, SignalHigh, SignalLow, SignalZero, Battery, BatteryLow,
  BatteryMedium, BatteryFull, MapPin, Calendar, TrendingUp, Settings
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

import ApiService from '../services/ApiService';
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import Modal from '../src/components/Modal';
import { Input, Select } from '../src/components/Form';
import { StatCard } from '../src/components/Card';

// ============================================
// Constants
// ============================================
const SENSOR_TYPES = [
  { value: 'temperature', label: 'Temperature', labelAr: 'حرارة', icon: Thermometer, unit: '°C', color: 'red' },
  { value: 'humidity', label: 'Humidity', labelAr: 'رطوبة', icon: Droplet, unit: '%', color: 'blue' },
  { value: 'soil_moisture', label: 'Soil Moisture', labelAr: 'رطوبة التربة', icon: Droplet, unit: '%', color: 'emerald' },
  { value: 'light', label: 'Light', labelAr: 'إضاءة', icon: Sun, unit: 'lux', color: 'amber' },
  { value: 'ph', label: 'pH', labelAr: 'حموضة', icon: Gauge, unit: 'pH', color: 'purple' },
  { value: 'wind', label: 'Wind', labelAr: 'رياح', icon: Wind, unit: 'km/h', color: 'cyan' }
];

const STATUS_OPTIONS = [
  { value: 'active', label: 'Active', labelAr: 'نشط', color: 'emerald' },
  { value: 'inactive', label: 'Inactive', labelAr: 'غير نشط', color: 'gray' },
  { value: 'maintenance', label: 'Maintenance', labelAr: 'صيانة', color: 'amber' },
  { value: 'offline', label: 'Offline', labelAr: 'غير متصل', color: 'red' }
];

// ============================================
// Sensor Card Component
// ============================================
const SensorCard = ({ sensor, onView, onEdit, onDelete }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [showMenu, setShowMenu] = useState(false);
  
  const type = SENSOR_TYPES.find(t => t.value === sensor.sensor_type);
  const status = STATUS_OPTIONS.find(s => s.value === sensor.status);
  const TypeIcon = type?.icon || Activity;

  const getBatteryIcon = (level) => {
    if (level > 70) return BatteryFull;
    if (level > 30) return BatteryMedium;
    return BatteryLow;
  };
  const BatteryIcon = getBatteryIcon(sensor.battery_level || 100);

  const getSignalIcon = (status) => {
    if (status === 'active') return SignalHigh;
    if (status === 'maintenance') return SignalLow;
    return SignalZero;
  };
  const SignalIcon = getSignalIcon(sensor.status);

  // Mock reading data
  const mockReading = {
    value: Math.floor(Math.random() * 50) + 20,
    trend: Math.random() > 0.5 ? 'up' : 'down'
  };

  return (
    <Card hover onClick={() => onView(sensor)} className="relative">
      {/* Status Indicator */}
      <div className={`absolute top-0 left-0 right-0 h-1 bg-${status?.color}-500`} />

      {/* Menu */}
      <div className="absolute top-4 right-4 rtl:right-auto rtl:left-4">
        <div className="relative">
          <button
            onClick={(e) => { e.stopPropagation(); setShowMenu(!showMenu); }}
            className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <MoreVertical className="w-5 h-5 text-gray-400" />
          </button>
          {showMenu && (
            <>
              <div className="fixed inset-0 z-10" onClick={() => setShowMenu(false)} />
              <div className="absolute z-20 top-full mt-1 right-0 rtl:right-auto rtl:left-0 w-36 py-1 bg-white dark:bg-gray-800 border rounded-lg shadow-lg">
                <button onClick={(e) => { e.stopPropagation(); onView(sensor); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Eye className="w-4 h-4" /> {isRTL ? 'عرض' : 'View'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onEdit(sensor); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
                  <Edit className="w-4 h-4" /> {isRTL ? 'تعديل' : 'Edit'}
                </button>
                <button onClick={(e) => { e.stopPropagation(); onDelete(sensor); setShowMenu(false); }} className="w-full px-3 py-2 text-sm text-left rtl:text-right text-red-500 hover:bg-red-50 flex items-center gap-2">
                  <Trash2 className="w-4 h-4" /> {isRTL ? 'حذف' : 'Delete'}
                </button>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="p-4">
        {/* Header */}
        <div className="flex items-start gap-3 mb-4">
          <div className={`p-3 rounded-xl bg-${type?.color}-100 dark:bg-${type?.color}-900/30`}>
            <TypeIcon className={`w-6 h-6 text-${type?.color}-600`} />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-gray-800 dark:text-white truncate">{sensor.name}</h3>
            <p className="text-sm text-gray-500">{isRTL ? type?.labelAr : type?.label}</p>
          </div>
        </div>

        {/* Reading */}
        <div className="mb-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-xl text-center">
          <div className="flex items-center justify-center gap-2">
            <span className="text-3xl font-bold text-gray-800 dark:text-white">
              {mockReading.value}
            </span>
            <span className="text-lg text-gray-500">{type?.unit}</span>
            <TrendingUp className={`w-4 h-4 ${mockReading.trend === 'up' ? 'text-emerald-500' : 'text-red-500 rotate-180'}`} />
          </div>
          <p className="text-xs text-gray-500 mt-1">{isRTL ? 'آخر قراءة' : 'Last reading'}</p>
        </div>

        {/* Status Row */}
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <SignalIcon className={`w-4 h-4 text-${status?.color}-500`} />
            <Badge variant={status?.color}>{isRTL ? status?.labelAr : status?.label}</Badge>
          </div>
          <div className="flex items-center gap-1 text-gray-500">
            <BatteryIcon className={`w-4 h-4 ${sensor.battery_level < 30 ? 'text-red-500' : 'text-gray-400'}`} />
            <span>{sensor.battery_level || 100}%</span>
          </div>
        </div>

        {/* Location */}
        {sensor.farm_name && (
          <div className="mt-3 pt-3 border-t border-gray-100 dark:border-gray-800 flex items-center gap-2 text-sm text-gray-500">
            <MapPin className="w-4 h-4" />
            <span className="truncate">{sensor.farm_name}</span>
          </div>
        )}
      </div>
    </Card>
  );
};

// ============================================
// Sensor Form Component
// ============================================
const SensorForm = ({ sensor, farms, onSubmit, onCancel, loading }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [formData, setFormData] = useState({
    name: sensor?.name || '',
    sensor_type: sensor?.sensor_type || 'temperature',
    model: sensor?.model || '',
    serial_number: sensor?.serial_number || '',
    farm_id: sensor?.farm_id || '',
    location: sensor?.location || '',
    status: sensor?.status || 'active'
  });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.name) newErrors.name = isRTL ? 'الاسم مطلوب' : 'Name is required';
    if (!formData.farm_id) newErrors.farm_id = isRTL ? 'المزرعة مطلوبة' : 'Farm is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) onSubmit(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: null }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'اسم المستشعر' : 'Sensor Name'}
          value={formData.name}
          onChange={(v) => handleChange('name', v)}
          error={errors.name}
          required
        />
        <Select
          label={isRTL ? 'النوع' : 'Type'}
          value={formData.sensor_type}
          onChange={(v) => handleChange('sensor_type', v)}
          options={SENSOR_TYPES}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label={isRTL ? 'الموديل' : 'Model'}
          value={formData.model}
          onChange={(v) => handleChange('model', v)}
        />
        <Input
          label={isRTL ? 'الرقم التسلسلي' : 'Serial Number'}
          value={formData.serial_number}
          onChange={(v) => handleChange('serial_number', v)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label={isRTL ? 'المزرعة' : 'Farm'}
          value={formData.farm_id}
          onChange={(v) => handleChange('farm_id', v)}
          options={farms.map(f => ({ value: f.id, label: f.name }))}
          error={errors.farm_id}
          required
        />
        <Input
          label={isRTL ? 'الموقع' : 'Location'}
          value={formData.location}
          onChange={(v) => handleChange('location', v)}
          icon={MapPin}
        />
      </div>

      <Select
        label={isRTL ? 'الحالة' : 'Status'}
        value={formData.status}
        onChange={(v) => handleChange('status', v)}
        options={STATUS_OPTIONS}
      />

      <div className="flex justify-end gap-3 pt-4 border-t">
        <Button type="button" variant="secondary" onClick={onCancel}>
          {isRTL ? 'إلغاء' : 'Cancel'}
        </Button>
        <Button type="submit" loading={loading}>
          {sensor ? (isRTL ? 'تحديث' : 'Update') : (isRTL ? 'إنشاء' : 'Create')}
        </Button>
      </div>
    </form>
  );
};

// ============================================
// Sensor Detail Modal Component
// ============================================
const SensorDetailModal = ({ sensor, isOpen, onClose }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const type = SENSOR_TYPES.find(t => t.value === sensor?.sensor_type);

  // Mock chart data
  const chartData = Array.from({ length: 24 }, (_, i) => ({
    time: `${i}:00`,
    value: Math.floor(Math.random() * 30) + 20
  }));

  if (!sensor) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={sensor.name} size="xl">
      <div className="space-y-6">
        {/* Chart */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            {isRTL ? 'القراءات (آخر 24 ساعة)' : 'Readings (Last 24 Hours)'}
          </h4>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="time" stroke="#9ca3af" fontSize={10} />
              <YAxis stroke="#9ca3af" fontSize={10} />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Details */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <p className="text-xs text-gray-500">{isRTL ? 'القراءة الحالية' : 'Current Reading'}</p>
            <p className="text-xl font-bold text-gray-800 dark:text-white">28 {type?.unit}</p>
          </div>
          <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <p className="text-xs text-gray-500">{isRTL ? 'المتوسط' : 'Average'}</p>
            <p className="text-xl font-bold text-gray-800 dark:text-white">25 {type?.unit}</p>
          </div>
          <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <p className="text-xs text-gray-500">{isRTL ? 'الأعلى' : 'Highest'}</p>
            <p className="text-xl font-bold text-emerald-600">32 {type?.unit}</p>
          </div>
          <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <p className="text-xs text-gray-500">{isRTL ? 'الأدنى' : 'Lowest'}</p>
            <p className="text-xl font-bold text-blue-600">18 {type?.unit}</p>
          </div>
        </div>
      </div>
    </Modal>
  );
};

// ============================================
// Main Sensors Page
// ============================================
const Sensors = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [sensors, setSensors] = useState([]);
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('');

  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedSensor, setSelectedSensor] = useState(null);
  const [formLoading, setFormLoading] = useState(false);

  const [stats, setStats] = useState({ total: 0, active: 0, alerts: 0, lowBattery: 0 });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [sensorsRes, farmsRes] = await Promise.all([
        ApiService.getSensors({ search: searchQuery, type: typeFilter }),
        ApiService.getFarms({ limit: 100 })
      ]);

      const items = sensorsRes.items || sensorsRes || [];
      setSensors(items);
      setFarms(farmsRes.items || farmsRes || []);

      setStats({
        total: items.length,
        active: items.filter(s => s.status === 'active').length,
        alerts: items.filter(s => s.status === 'maintenance' || s.status === 'offline').length,
        lowBattery: items.filter(s => (s.battery_level || 100) < 30).length
      });
    } catch (err) {
      console.error('Error loading sensors:', err);
      // Mock data
      setSensors([
        { id: 1, name: 'Temp-001', sensor_type: 'temperature', status: 'active', battery_level: 85, farm_name: 'Green Valley' },
        { id: 2, name: 'Humid-002', sensor_type: 'humidity', status: 'active', battery_level: 45, farm_name: 'Green Valley' },
        { id: 3, name: 'Soil-003', sensor_type: 'soil_moisture', status: 'maintenance', battery_level: 22, farm_name: 'Farm B' }
      ]);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, typeFilter]);

  useEffect(() => { loadData(); }, [loadData]);

  const handleCreate = async (data) => {
    try { setFormLoading(true); await ApiService.createSensor(data); setShowCreateModal(false); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleUpdate = async (data) => {
    try { setFormLoading(true); await ApiService.updateSensor(selectedSensor.id, data); setShowEditModal(false); setSelectedSensor(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleDelete = async () => {
    try { setFormLoading(true); await ApiService.deleteSensor(selectedSensor.id); setShowDeleteModal(false); setSelectedSensor(null); loadData(); }
    finally { setFormLoading(false); }
  };

  const handleView = (sensor) => { setSelectedSensor(sensor); setShowDetailModal(true); };
  const handleEdit = (sensor) => { setSelectedSensor(sensor); setShowEditModal(true); };
  const handleDeleteClick = (sensor) => { setSelectedSensor(sensor); setShowDeleteModal(true); };

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'المستشعرات' : 'Sensors'}
        description={isRTL ? 'مراقبة وإدارة أجهزة الاستشعار' : 'Monitor and manage IoT sensors'}
        icon={Activity}
      >
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={loadData}><RefreshCw className="w-4 h-4" /></Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" />
            {isRTL ? 'مستشعر جديد' : 'New Sensor'}
          </Button>
        </div>
      </PageHeader>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard title={isRTL ? 'إجمالي المستشعرات' : 'Total Sensors'} value={stats.total} icon={Activity} iconColor="blue" />
        <StatCard title={isRTL ? 'نشط' : 'Active'} value={stats.active} icon={Check} iconColor="emerald" />
        <StatCard title={isRTL ? 'تنبيهات' : 'Alerts'} value={stats.alerts} icon={AlertTriangle} iconColor="amber" />
        <StatCard title={isRTL ? 'بطارية منخفضة' : 'Low Battery'} value={stats.lowBattery} icon={BatteryLow} iconColor="red" />
      </div>

      {/* Filters */}
      <Card>
        <div className="p-4 flex flex-wrap items-center gap-4">
          <div className="relative flex-1 max-w-xs">
            <Search className="absolute left-3 rtl:left-auto rtl:right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={isRTL ? 'بحث...' : 'Search...'}
              className="w-full pl-10 rtl:pl-4 rtl:pr-10 pr-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg text-sm"
            />
          </div>
          <Select
            value={typeFilter}
            onChange={setTypeFilter}
            options={[{ value: '', label: isRTL ? 'كل الأنواع' : 'All Types' }, ...SENSOR_TYPES]}
            className="w-40"
          />
        </div>
      </Card>

      {/* Content */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {[...Array(8)].map((_, i) => <Card key={i} className="animate-pulse h-56" />)}
        </div>
      ) : sensors.length === 0 ? (
        <Card className="p-12 text-center">
          <Activity className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'لا توجد مستشعرات' : 'No Sensors'}</h3>
          <Button onClick={() => setShowCreateModal(true)}><Plus className="w-4 h-4 mr-1" />{isRTL ? 'إضافة' : 'Add'}</Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {sensors.map(sensor => (
            <SensorCard key={sensor.id} sensor={sensor} onView={handleView} onEdit={handleEdit} onDelete={handleDeleteClick} />
          ))}
        </div>
      )}

      {/* Modals */}
      <Modal isOpen={showCreateModal} onClose={() => setShowCreateModal(false)} title={isRTL ? 'إضافة مستشعر' : 'Add Sensor'} size="lg">
        <SensorForm farms={farms} onSubmit={handleCreate} onCancel={() => setShowCreateModal(false)} loading={formLoading} />
      </Modal>

      <Modal isOpen={showEditModal} onClose={() => { setShowEditModal(false); setSelectedSensor(null); }} title={isRTL ? 'تعديل المستشعر' : 'Edit Sensor'} size="lg">
        <SensorForm sensor={selectedSensor} farms={farms} onSubmit={handleUpdate} onCancel={() => { setShowEditModal(false); setSelectedSensor(null); }} loading={formLoading} />
      </Modal>

      <SensorDetailModal sensor={selectedSensor} isOpen={showDetailModal} onClose={() => { setShowDetailModal(false); setSelectedSensor(null); }} />

      <Modal isOpen={showDeleteModal} onClose={() => { setShowDeleteModal(false); setSelectedSensor(null); }} size="sm" showCloseButton={false}>
        <div className="text-center py-4">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-100 flex items-center justify-center"><Trash2 className="w-8 h-8 text-red-500" /></div>
          <h3 className="text-lg font-semibold mb-2">{isRTL ? 'حذف المستشعر' : 'Delete Sensor'}</h3>
          <p className="text-gray-500 mb-6">{isRTL ? `حذف "${selectedSensor?.name}"؟` : `Delete "${selectedSensor?.name}"?`}</p>
          <div className="flex justify-center gap-3">
            <Button variant="secondary" onClick={() => { setShowDeleteModal(false); setSelectedSensor(null); }}>{isRTL ? 'إلغاء' : 'Cancel'}</Button>
            <Button variant="danger" onClick={handleDelete} loading={formLoading}>{isRTL ? 'حذف' : 'Delete'}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Sensors;
