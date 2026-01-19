/**
 * Profile Page - User Profile Management
 * =======================================
 * 
 * @author Global System v35.0
 * @date 2026-01-19
 */

import React, { useState, useEffect, useRef } from 'react';
import {
  User, Mail, Phone, Calendar, MapPin, Camera, Edit, Save, X,
  Warehouse, Leaf, FileText, Shield, Award, Clock, Upload, Check
} from 'lucide-react';

import ApiService from '../services/ApiService';
import { Card, CardHeader, CardContent } from '../components/UI/card';
import { Button } from '../components/UI/button';
import { Badge } from '../components/UI/badge';
import { PageHeader } from '../components/UI/page-header';
import { Input, TextArea } from '../src/components/Form';
import Modal from '../src/components/Modal';

// ============================================
// Profile Header Component
// ============================================
const ProfileHeader = ({ user, onAvatarChange, isEditing }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        onAvatarChange?.(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <Card className="relative overflow-hidden">
      {/* Background */}
      <div className="h-32 bg-gradient-to-r from-emerald-500 to-teal-500" />
      
      {/* Profile Info */}
      <div className="px-6 pb-6">
        <div className="flex flex-col md:flex-row md:items-end gap-4 -mt-16">
          {/* Avatar */}
          <div className="relative">
            <div className="w-32 h-32 rounded-full border-4 border-white dark:border-gray-800 bg-white dark:bg-gray-800 overflow-hidden shadow-lg">
              {user.avatar_url ? (
                <img src={user.avatar_url} alt={user.name} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full bg-gradient-to-br from-emerald-100 to-teal-100 dark:from-emerald-900/40 dark:to-teal-900/40 flex items-center justify-center">
                  <span className="text-4xl font-bold text-emerald-600">
                    {user.name?.charAt(0)?.toUpperCase()}
                  </span>
                </div>
              )}
            </div>
            {isEditing && (
              <>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="absolute bottom-0 right-0 p-2 rounded-full bg-emerald-500 text-white shadow-lg hover:bg-emerald-600 transition-colors"
                >
                  <Camera className="w-4 h-4" />
                </button>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </>
            )}
          </div>

          {/* User Info */}
          <div className="flex-1">
            <div className="flex flex-wrap items-center gap-3 mb-2">
              <h1 className="text-2xl font-bold text-gray-800 dark:text-white">{user.name}</h1>
              {user.is_verified && (
                <Badge variant="emerald" className="flex items-center gap-1">
                  <Shield className="w-3 h-3" />
                  {isRTL ? 'موثق' : 'Verified'}
                </Badge>
              )}
              <Badge variant={user.role === 'admin' ? 'red' : user.role === 'manager' ? 'amber' : 'blue'}>
                {user.role}
              </Badge>
            </div>
            <p className="text-gray-500">{user.email}</p>
          </div>

          {/* Stats */}
          <div className="flex gap-6 text-center">
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{user.farm_count || 0}</p>
              <p className="text-sm text-gray-500">{isRTL ? 'مزارع' : 'Farms'}</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{user.diagnosis_count || 0}</p>
              <p className="text-sm text-gray-500">{isRTL ? 'تشخيص' : 'Diagnoses'}</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-800 dark:text-white">{user.report_count || 0}</p>
              <p className="text-sm text-gray-500">{isRTL ? 'تقارير' : 'Reports'}</p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

// ============================================
// Info Row Component
// ============================================
const InfoRow = ({ icon: Icon, label, labelAr, value, isEditing, editComponent }) => {
  const isRTL = document.documentElement.dir === 'rtl';

  return (
    <div className="flex items-center gap-4 py-4 border-b border-gray-100 dark:border-gray-800 last:border-0">
      <div className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800">
        <Icon className="w-5 h-5 text-gray-500" />
      </div>
      <div className="flex-1">
        <p className="text-sm text-gray-500">{isRTL ? labelAr : label}</p>
        {isEditing && editComponent ? (
          editComponent
        ) : (
          <p className="font-medium text-gray-800 dark:text-white">{value || '-'}</p>
        )}
      </div>
    </div>
  );
};

// ============================================
// Activity Item Component
// ============================================
const ActivityItem = ({ activity }) => {
  const isRTL = document.documentElement.dir === 'rtl';
  
  const icons = {
    diagnosis: Leaf,
    farm: Warehouse,
    report: FileText
  };
  const Icon = icons[activity.type] || Leaf;
  
  const colors = {
    diagnosis: 'bg-emerald-100 text-emerald-600',
    farm: 'bg-blue-100 text-blue-600',
    report: 'bg-purple-100 text-purple-600'
  };

  return (
    <div className="flex items-start gap-3 py-3">
      <div className={`p-2 rounded-lg ${colors[activity.type]}`}>
        <Icon className="w-4 h-4" />
      </div>
      <div className="flex-1">
        <p className="text-sm text-gray-700 dark:text-gray-300">{activity.description}</p>
        <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
      </div>
    </div>
  );
};

// ============================================
// Main Profile Page
// ============================================
const Profile = () => {
  const isRTL = document.documentElement.dir === 'rtl';
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [user, setUser] = useState(null);
  const [editData, setEditData] = useState({});
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setLoading(true);
    try {
      const response = await ApiService.getProfile();
      setUser(response);
      setEditData(response);
    } catch (err) {
      console.error('Error loading profile:', err);
      // Mock data
      const mockUser = {
        id: 1,
        name: 'محمد أحمد',
        email: 'mohamed@example.com',
        phone: '+966 50 123 4567',
        role: 'admin',
        company: 'شركة الزراعة الذكية',
        location: 'الرياض، السعودية',
        bio: 'مهندس زراعي متخصص في تشخيص أمراض النباتات',
        is_verified: true,
        avatar_url: null,
        farm_count: 12,
        diagnosis_count: 156,
        report_count: 24,
        created_at: '2025-01-15',
        last_login: '2026-01-19'
      };
      setUser(mockUser);
      setEditData(mockUser);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await ApiService.updateProfile(editData);
      setUser(editData);
      setIsEditing(false);
    } catch (err) {
      console.error('Error saving profile:', err);
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field, value) => {
    setEditData(prev => ({ ...prev, [field]: value }));
  };

  const handleAvatarChange = (avatarUrl) => {
    setEditData(prev => ({ ...prev, avatar_url: avatarUrl }));
  };

  const recentActivity = [
    { type: 'diagnosis', description: isRTL ? 'تم تشخيص حالة جديدة - لفحة مبكرة' : 'New diagnosis - Early Blight', time: isRTL ? 'منذ ساعتين' : '2 hours ago' },
    { type: 'farm', description: isRTL ? 'تم تحديث مزرعة "الوادي الأخضر"' : 'Updated farm "Green Valley"', time: isRTL ? 'منذ 5 ساعات' : '5 hours ago' },
    { type: 'report', description: isRTL ? 'تم إنشاء تقرير شهري' : 'Monthly report generated', time: isRTL ? 'أمس' : 'Yesterday' },
    { type: 'diagnosis', description: isRTL ? 'تم تشخيص 3 حالات جديدة' : '3 new diagnoses completed', time: isRTL ? 'منذ يومين' : '2 days ago' }
  ];

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-64 bg-gray-200 dark:bg-gray-700 rounded-lg" />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 h-96 bg-gray-200 dark:bg-gray-700 rounded-lg" />
          <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded-lg" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title={isRTL ? 'الملف الشخصي' : 'Profile'}
        description={isRTL ? 'إدارة معلوماتك الشخصية' : 'Manage your personal information'}
        icon={User}
      >
        {isEditing ? (
          <div className="flex gap-2">
            <Button variant="secondary" onClick={() => { setIsEditing(false); setEditData(user); }}>
              <X className="w-4 h-4 mr-2" />
              {isRTL ? 'إلغاء' : 'Cancel'}
            </Button>
            <Button onClick={handleSave} loading={saving}>
              <Save className="w-4 h-4 mr-2" />
              {isRTL ? 'حفظ' : 'Save'}
            </Button>
          </div>
        ) : (
          <Button onClick={() => setIsEditing(true)}>
            <Edit className="w-4 h-4 mr-2" />
            {isRTL ? 'تعديل الملف' : 'Edit Profile'}
          </Button>
        )}
      </PageHeader>

      {/* Profile Header */}
      <ProfileHeader
        user={isEditing ? editData : user}
        onAvatarChange={handleAvatarChange}
        isEditing={isEditing}
      />

      {/* Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Personal Information */}
          <Card>
            <CardHeader>
              <h3 className="font-semibold">{isRTL ? 'المعلومات الشخصية' : 'Personal Information'}</h3>
            </CardHeader>
            <CardContent>
              <InfoRow
                icon={User}
                label="Full Name"
                labelAr="الاسم الكامل"
                value={isEditing ? undefined : user.name}
                isEditing={isEditing}
                editComponent={
                  <Input
                    value={editData.name}
                    onChange={(v) => handleChange('name', v)}
                  />
                }
              />
              <InfoRow
                icon={Mail}
                label="Email"
                labelAr="البريد الإلكتروني"
                value={user.email}
              />
              <InfoRow
                icon={Phone}
                label="Phone"
                labelAr="الهاتف"
                value={isEditing ? undefined : user.phone}
                isEditing={isEditing}
                editComponent={
                  <Input
                    value={editData.phone}
                    onChange={(v) => handleChange('phone', v)}
                  />
                }
              />
              <InfoRow
                icon={MapPin}
                label="Location"
                labelAr="الموقع"
                value={isEditing ? undefined : user.location}
                isEditing={isEditing}
                editComponent={
                  <Input
                    value={editData.location}
                    onChange={(v) => handleChange('location', v)}
                  />
                }
              />
            </CardContent>
          </Card>

          {/* Bio */}
          <Card>
            <CardHeader>
              <h3 className="font-semibold">{isRTL ? 'نبذة' : 'Bio'}</h3>
            </CardHeader>
            <CardContent>
              {isEditing ? (
                <TextArea
                  value={editData.bio}
                  onChange={(v) => handleChange('bio', v)}
                  rows={4}
                  placeholder={isRTL ? 'أخبرنا عن نفسك...' : 'Tell us about yourself...'}
                />
              ) : (
                <p className="text-gray-700 dark:text-gray-300">
                  {user.bio || (isRTL ? 'لم تتم إضافة نبذة بعد' : 'No bio added yet')}
                </p>
              )}
            </CardContent>
          </Card>

          {/* Account Details */}
          <Card>
            <CardHeader>
              <h3 className="font-semibold">{isRTL ? 'تفاصيل الحساب' : 'Account Details'}</h3>
            </CardHeader>
            <CardContent>
              <InfoRow
                icon={Calendar}
                label="Member Since"
                labelAr="عضو منذ"
                value={new Date(user.created_at).toLocaleDateString()}
              />
              <InfoRow
                icon={Clock}
                label="Last Login"
                labelAr="آخر تسجيل دخول"
                value={new Date(user.last_login).toLocaleDateString()}
              />
              <InfoRow
                icon={Shield}
                label="Role"
                labelAr="الدور"
                value={<Badge variant={user.role === 'admin' ? 'red' : 'blue'}>{user.role}</Badge>}
              />
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <h3 className="font-semibold">{isRTL ? 'إجراءات سريعة' : 'Quick Actions'}</h3>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start" onClick={() => setShowPasswordModal(true)}>
                <Shield className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                {isRTL ? 'تغيير كلمة المرور' : 'Change Password'}
              </Button>
              <Button variant="outline" className="w-full justify-start">
                <Mail className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                {isRTL ? 'تحديث البريد' : 'Update Email'}
              </Button>
              <Button variant="outline" className="w-full justify-start text-red-500 hover:bg-red-50">
                <X className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                {isRTL ? 'حذف الحساب' : 'Delete Account'}
              </Button>
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <h3 className="font-semibold">{isRTL ? 'النشاط الأخير' : 'Recent Activity'}</h3>
            </CardHeader>
            <CardContent>
              <div className="divide-y divide-gray-100 dark:divide-gray-800">
                {recentActivity.map((activity, index) => (
                  <ActivityItem key={index} activity={activity} />
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Achievements */}
          <Card>
            <CardHeader>
              <h3 className="font-semibold flex items-center gap-2">
                <Award className="w-5 h-5 text-amber-500" />
                {isRTL ? 'الإنجازات' : 'Achievements'}
              </h3>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { icon: '🌱', name: isRTL ? 'مبتدئ' : 'Starter' },
                  { icon: '🔬', name: isRTL ? 'محلل' : 'Analyzer' },
                  { icon: '⭐', name: isRTL ? 'خبير' : 'Expert' }
                ].map((badge, index) => (
                  <div key={index} className="text-center p-2 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div className="text-2xl mb-1">{badge.icon}</div>
                    <div className="text-xs text-gray-500">{badge.name}</div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Change Password Modal */}
      <Modal
        isOpen={showPasswordModal}
        onClose={() => setShowPasswordModal(false)}
        title={isRTL ? 'تغيير كلمة المرور' : 'Change Password'}
        size="sm"
      >
        <div className="space-y-4">
          <Input
            label={isRTL ? 'كلمة المرور الحالية' : 'Current Password'}
            type="password"
          />
          <Input
            label={isRTL ? 'كلمة المرور الجديدة' : 'New Password'}
            type="password"
          />
          <Input
            label={isRTL ? 'تأكيد كلمة المرور' : 'Confirm Password'}
            type="password"
          />
          <div className="flex justify-end gap-3">
            <Button variant="secondary" onClick={() => setShowPasswordModal(false)}>
              {isRTL ? 'إلغاء' : 'Cancel'}
            </Button>
            <Button>
              <Check className="w-4 h-4 mr-2" />
              {isRTL ? 'تغيير' : 'Change'}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default Profile;
