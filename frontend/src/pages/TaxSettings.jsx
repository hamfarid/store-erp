/**
 * Tax Settings Page
 * صفحة إعدادات الضرائب
 * 
 * @file frontend/src/pages/TaxSettings.jsx
 * @author Store ERP v2.0.0
 */

import React, { useState, useEffect } from 'react';
import {
  Receipt, Plus, Edit, Trash2, Save, RefreshCw, Calculator,
  Percent, CheckCircle, XCircle, Globe, Building2, AlertTriangle
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// UI Components
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '../components/ui/table';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '../components/ui/select';

/**
 * Toggle Switch Component
 */
const Toggle = ({ enabled, onChange, label, description }) => (
  <div className="flex items-center justify-between py-3 border-b border-border last:border-0">
    <div className="flex-1">
      <span className="font-medium text-foreground">{label}</span>
      {description && (
        <p className="text-sm text-muted-foreground mt-0.5">{description}</p>
      )}
    </div>
    <button
      type="button"
      onClick={() => onChange(!enabled)}
      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
        enabled ? 'bg-primary' : 'bg-muted'
      }`}
    >
      <span
        className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform ${
          enabled ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
    </button>
  </div>
);

/**
 * صفحة إعدادات الضرائب
 */
const TaxSettings = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingTax, setEditingTax] = useState(null);
  
  const [settings, setSettings] = useState({
    // الإعدادات العامة للضرائب
    general: {
      taxEnabled: true,
      defaultTaxRate: 15,
      taxIncludedInPrice: false,
      showTaxOnInvoice: true,
      taxCalculationMethod: 'exclusive', // exclusive, inclusive
      roundingMethod: 'normal', // normal, up, down
      roundingPrecision: 2
    },
    // معلومات الشركة الضريبية
    company: {
      taxNumber: '',
      vatNumber: '',
      commercialRegistration: '',
      taxOffice: '',
      taxAddress: ''
    },
    // أنواع الضرائب
    taxTypes: [
      {
        id: 1,
        name: 'ضريبة القيمة المضافة',
        code: 'VAT',
        rate: 15,
        type: 'percentage',
        isDefault: true,
        isActive: true,
        appliesTo: ['products', 'services'],
        description: 'ضريبة القيمة المضافة القياسية'
      },
      {
        id: 2,
        name: 'ضريبة صفرية',
        code: 'ZERO',
        rate: 0,
        type: 'percentage',
        isDefault: false,
        isActive: true,
        appliesTo: ['exports', 'healthcare'],
        description: 'للمنتجات المعفاة من الضريبة'
      },
      {
        id: 3,
        name: 'ضريبة مخفضة',
        code: 'REDUCED',
        rate: 5,
        type: 'percentage',
        isDefault: false,
        isActive: false,
        appliesTo: ['essentials'],
        description: 'للسلع الأساسية'
      }
    ],
    // إعدادات ZATCA (هيئة الزكاة والضريبة والجمارك)
    zatca: {
      integrationEnabled: false,
      apiKey: '',
      secretKey: '',
      environment: 'sandbox', // sandbox, production
      deviceId: '',
      lastSyncDate: null
    },
    // إعدادات الفواتير الإلكترونية
    eInvoicing: {
      enabled: false,
      qrCodeEnabled: true,
      xmlExportEnabled: true,
      autoSubmit: false
    }
  });

  const [newTax, setNewTax] = useState({
    name: '',
    code: '',
    rate: 0,
    type: 'percentage',
    isActive: true,
    appliesTo: [],
    description: ''
  });

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/settings/tax');
      if (response.status === 'success' && response.data) {
        setSettings(prev => ({ ...prev, ...response.data }));
      }
    } catch (error) {
      console.log('Using default settings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      await apiClient.put('/api/settings/tax', settings);
      toast.success('تم حفظ إعدادات الضرائب بنجاح');
    } catch (error) {
      toast.error('فشل حفظ الإعدادات');
    } finally {
      setIsSaving(false);
    }
  };

  const updateSetting = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  const handleAddTax = () => {
    if (!newTax.name || !newTax.code) {
      toast.error('يرجى إدخال اسم ورمز الضريبة');
      return;
    }

    const tax = {
      ...newTax,
      id: Date.now()
    };

    setSettings(prev => ({
      ...prev,
      taxTypes: [...prev.taxTypes, tax]
    }));

    setNewTax({
      name: '',
      code: '',
      rate: 0,
      type: 'percentage',
      isActive: true,
      appliesTo: [],
      description: ''
    });
    setShowAddModal(false);
    toast.success('تم إضافة نوع الضريبة');
  };

  const handleDeleteTax = (id) => {
    if (window.confirm('هل أنت متأكد من حذف نوع الضريبة هذا؟')) {
      setSettings(prev => ({
        ...prev,
        taxTypes: prev.taxTypes.filter(t => t.id !== id)
      }));
      toast.success('تم حذف نوع الضريبة');
    }
  };

  const handleToggleTaxActive = (id) => {
    setSettings(prev => ({
      ...prev,
      taxTypes: prev.taxTypes.map(t => 
        t.id === id ? { ...t, isActive: !t.isActive } : t
      )
    }));
  };

  const handleSetDefaultTax = (id) => {
    setSettings(prev => ({
      ...prev,
      taxTypes: prev.taxTypes.map(t => ({
        ...t,
        isDefault: t.id === id
      })),
      general: {
        ...prev.general,
        defaultTaxRate: prev.taxTypes.find(t => t.id === id)?.rate || 15
      }
    }));
    toast.success('تم تعيين الضريبة الافتراضية');
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل الإعدادات...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Receipt className="w-8 h-8" />
            إعدادات الضرائب
          </h1>
          <p className="text-muted-foreground mt-1">إدارة إعدادات الضرائب والفوترة الإلكترونية</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleSave}
            disabled={isSaving}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            {isSaving ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* الإعدادات العامة */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calculator className="w-5 h-5" />
              الإعدادات العامة
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Toggle
              enabled={settings.general.taxEnabled}
              onChange={(v) => updateSetting('general', 'taxEnabled', v)}
              label="تفعيل الضرائب"
              description="تطبيق الضرائب على المبيعات والمشتريات"
            />
            <div>
              <Label htmlFor="defaultRate">نسبة الضريبة الافتراضية (%)</Label>
              <Input
                id="defaultRate"
                type="number"
                min="0"
                max="100"
                step="0.5"
                value={settings.general.defaultTaxRate}
                onChange={(e) => updateSetting('general', 'defaultTaxRate', parseFloat(e.target.value))}
              />
            </div>
            <Toggle
              enabled={settings.general.taxIncludedInPrice}
              onChange={(v) => updateSetting('general', 'taxIncludedInPrice', v)}
              label="الضريبة مضمنة في السعر"
              description="الأسعار المعروضة تشمل الضريبة"
            />
            <Toggle
              enabled={settings.general.showTaxOnInvoice}
              onChange={(v) => updateSetting('general', 'showTaxOnInvoice', v)}
              label="عرض الضريبة في الفاتورة"
              description="إظهار تفاصيل الضريبة بشكل منفصل"
            />
            <div>
              <Label htmlFor="calcMethod">طريقة حساب الضريبة</Label>
              <Select
                value={settings.general.taxCalculationMethod}
                onValueChange={(v) => updateSetting('general', 'taxCalculationMethod', v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="exclusive">خارج السعر (Exclusive)</SelectItem>
                  <SelectItem value="inclusive">داخل السعر (Inclusive)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label htmlFor="rounding">طريقة التقريب</Label>
              <Select
                value={settings.general.roundingMethod}
                onValueChange={(v) => updateSetting('general', 'roundingMethod', v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="normal">تقريب عادي</SelectItem>
                  <SelectItem value="up">تقريب لأعلى</SelectItem>
                  <SelectItem value="down">تقريب لأسفل</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* معلومات الشركة الضريبية */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building2 className="w-5 h-5" />
              معلومات الشركة الضريبية
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="taxNumber">الرقم الضريبي</Label>
              <Input
                id="taxNumber"
                placeholder="300000000000003"
                value={settings.company.taxNumber}
                onChange={(e) => updateSetting('company', 'taxNumber', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="vatNumber">رقم ضريبة القيمة المضافة</Label>
              <Input
                id="vatNumber"
                placeholder="300000000000003"
                value={settings.company.vatNumber}
                onChange={(e) => updateSetting('company', 'vatNumber', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="crNumber">رقم السجل التجاري</Label>
              <Input
                id="crNumber"
                placeholder="1010000000"
                value={settings.company.commercialRegistration}
                onChange={(e) => updateSetting('company', 'commercialRegistration', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="taxOffice">فرع الهيئة</Label>
              <Input
                id="taxOffice"
                placeholder="الرياض"
                value={settings.company.taxOffice}
                onChange={(e) => updateSetting('company', 'taxOffice', e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="taxAddress">عنوان المنشأة الضريبي</Label>
              <Input
                id="taxAddress"
                placeholder="الرياض، حي النزهة، شارع..."
                value={settings.company.taxAddress}
                onChange={(e) => updateSetting('company', 'taxAddress', e.target.value)}
              />
            </div>
          </CardContent>
        </Card>

        {/* أنواع الضرائب */}
        <Card className="lg:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Percent className="w-5 h-5" />
              أنواع الضرائب
            </CardTitle>
            <button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2 px-3 py-1.5 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 text-sm"
            >
              <Plus className="w-4 h-4" />
              إضافة نوع
            </button>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>الاسم</TableHead>
                  <TableHead>الرمز</TableHead>
                  <TableHead>النسبة</TableHead>
                  <TableHead>ينطبق على</TableHead>
                  <TableHead>الحالة</TableHead>
                  <TableHead>افتراضي</TableHead>
                  <TableHead>الإجراءات</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {settings.taxTypes.map((tax) => (
                  <TableRow key={tax.id}>
                    <TableCell className="font-medium">{tax.name}</TableCell>
                    <TableCell>
                      <Badge variant="outline">{tax.code}</Badge>
                    </TableCell>
                    <TableCell>{tax.rate}%</TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {tax.appliesTo.map((item, idx) => (
                          <Badge key={idx} variant="secondary" className="text-xs">
                            {item}
                          </Badge>
                        ))}
                      </div>
                    </TableCell>
                    <TableCell>
                      <button
                        onClick={() => handleToggleTaxActive(tax.id)}
                        className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs ${
                          tax.isActive 
                            ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                            : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                        }`}
                      >
                        {tax.isActive ? (
                          <>
                            <CheckCircle className="w-3 h-3" />
                            نشط
                          </>
                        ) : (
                          <>
                            <XCircle className="w-3 h-3" />
                            معطل
                          </>
                        )}
                      </button>
                    </TableCell>
                    <TableCell>
                      {tax.isDefault ? (
                        <Badge className="bg-blue-500">افتراضي</Badge>
                      ) : (
                        <button
                          onClick={() => handleSetDefaultTax(tax.id)}
                          className="text-xs text-muted-foreground hover:text-primary"
                        >
                          تعيين كافتراضي
                        </button>
                      )}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => setEditingTax(tax)}
                          className="p-1 hover:bg-muted rounded"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        {!tax.isDefault && (
                          <button
                            onClick={() => handleDeleteTax(tax.id)}
                            className="p-1 hover:bg-red-100 rounded text-red-500"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        {/* إعدادات ZATCA */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="w-5 h-5" />
              تكامل ZATCA
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
              <div className="flex items-start gap-2">
                <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-yellow-800 dark:text-yellow-400">
                    تكامل هيئة الزكاة والضريبة والجمارك
                  </p>
                  <p className="text-xs text-yellow-700 dark:text-yellow-500 mt-1">
                    يتطلب التسجيل في بوابة فاتورة لربط النظام
                  </p>
                </div>
              </div>
            </div>
            <Toggle
              enabled={settings.zatca.integrationEnabled}
              onChange={(v) => updateSetting('zatca', 'integrationEnabled', v)}
              label="تفعيل التكامل"
              description="ربط النظام مع بوابة فاتورة"
            />
            {settings.zatca.integrationEnabled && (
              <>
                <div>
                  <Label htmlFor="apiKey">مفتاح API</Label>
                  <Input
                    id="apiKey"
                    type="password"
                    placeholder="••••••••••••"
                    value={settings.zatca.apiKey}
                    onChange={(e) => updateSetting('zatca', 'apiKey', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="secretKey">المفتاح السري</Label>
                  <Input
                    id="secretKey"
                    type="password"
                    placeholder="••••••••••••"
                    value={settings.zatca.secretKey}
                    onChange={(e) => updateSetting('zatca', 'secretKey', e.target.value)}
                  />
                </div>
                <div>
                  <Label htmlFor="environment">البيئة</Label>
                  <Select
                    value={settings.zatca.environment}
                    onValueChange={(v) => updateSetting('zatca', 'environment', v)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sandbox">بيئة الاختبار (Sandbox)</SelectItem>
                      <SelectItem value="production">بيئة الإنتاج (Production)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="deviceId">معرّف الجهاز</Label>
                  <Input
                    id="deviceId"
                    placeholder="DEVICE-001"
                    value={settings.zatca.deviceId}
                    onChange={(e) => updateSetting('zatca', 'deviceId', e.target.value)}
                  />
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* الفوترة الإلكترونية */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Receipt className="w-5 h-5" />
              الفوترة الإلكترونية
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Toggle
              enabled={settings.eInvoicing.enabled}
              onChange={(v) => updateSetting('eInvoicing', 'enabled', v)}
              label="تفعيل الفوترة الإلكترونية"
              description="إنشاء فواتير متوافقة مع متطلبات ZATCA"
            />
            <Toggle
              enabled={settings.eInvoicing.qrCodeEnabled}
              onChange={(v) => updateSetting('eInvoicing', 'qrCodeEnabled', v)}
              label="رمز QR"
              description="إضافة رمز QR للفاتورة"
            />
            <Toggle
              enabled={settings.eInvoicing.xmlExportEnabled}
              onChange={(v) => updateSetting('eInvoicing', 'xmlExportEnabled', v)}
              label="تصدير XML"
              description="إمكانية تصدير الفاتورة بصيغة XML"
            />
            <Toggle
              enabled={settings.eInvoicing.autoSubmit}
              onChange={(v) => updateSetting('eInvoicing', 'autoSubmit', v)}
              label="إرسال تلقائي"
              description="إرسال الفواتير تلقائياً إلى ZATCA"
            />
          </CardContent>
        </Card>
      </div>

      {/* Add Tax Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-background rounded-2xl p-6 w-full max-w-md" dir="rtl">
            <h3 className="text-xl font-bold mb-4">إضافة نوع ضريبة جديد</h3>
            <div className="space-y-4">
              <div>
                <Label htmlFor="taxName">اسم الضريبة</Label>
                <Input
                  id="taxName"
                  placeholder="ضريبة القيمة المضافة"
                  value={newTax.name}
                  onChange={(e) => setNewTax(prev => ({ ...prev, name: e.target.value }))}
                />
              </div>
              <div>
                <Label htmlFor="taxCode">رمز الضريبة</Label>
                <Input
                  id="taxCode"
                  placeholder="VAT"
                  value={newTax.code}
                  onChange={(e) => setNewTax(prev => ({ ...prev, code: e.target.value.toUpperCase() }))}
                />
              </div>
              <div>
                <Label htmlFor="taxRate">نسبة الضريبة (%)</Label>
                <Input
                  id="taxRate"
                  type="number"
                  min="0"
                  max="100"
                  step="0.5"
                  value={newTax.rate}
                  onChange={(e) => setNewTax(prev => ({ ...prev, rate: parseFloat(e.target.value) }))}
                />
              </div>
              <div>
                <Label htmlFor="taxDesc">الوصف</Label>
                <Input
                  id="taxDesc"
                  placeholder="وصف نوع الضريبة"
                  value={newTax.description}
                  onChange={(e) => setNewTax(prev => ({ ...prev, description: e.target.value }))}
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 mt-6">
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 border border-border rounded-lg hover:bg-muted"
              >
                إلغاء
              </button>
              <button
                onClick={handleAddTax}
                className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
              >
                إضافة
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaxSettings;
