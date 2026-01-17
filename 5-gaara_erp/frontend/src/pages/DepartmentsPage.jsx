import React, { useState, useEffect, useCallback } from 'react';
import {
  Building2, Plus, Edit, Trash2, Users, FolderTree,
  DollarSign, RefreshCw, ChevronDown, ChevronLeft
} from 'lucide-react';
import { toast } from 'react-hot-toast';
import apiClient from '../services/apiClient';

// UI Components
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';

/**
 * صفحة إدارة الأقسام
 * Departments Management Page
 */
const DepartmentsPage = () => {
  const [departments, setDepartments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingDepartment, setEditingDepartment] = useState(null);
  const [expandedDepts, setExpandedDepts] = useState(new Set());
  const [formData, setFormData] = useState({
    code: '',
    name: '',
    name_ar: '',
    description: '',
    parent_id: '',
    manager_id: '',
    budget: '',
    budget_year: new Date().getFullYear(),
  });

  // Load departments
  const loadDepartments = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/hr/departments?tree=true');
      
      if (response.success) {
        setDepartments(response.data || []);
      } else {
        // Demo data with hierarchy
        setDepartments([
          {
            id: 1,
            code: 'IT',
            name: 'تقنية المعلومات',
            name_ar: 'تقنية المعلومات',
            employee_count: 15,
            budget: 500000,
            is_active: true,
            children: [
              {
                id: 5,
                code: 'DEV',
                name: 'التطوير',
                employee_count: 8,
                budget: 300000,
                is_active: true,
                children: [],
              },
              {
                id: 6,
                code: 'OPS',
                name: 'التشغيل',
                employee_count: 7,
                budget: 200000,
                is_active: true,
                children: [],
              },
            ],
          },
          {
            id: 2,
            code: 'HR',
            name: 'الموارد البشرية',
            name_ar: 'الموارد البشرية',
            employee_count: 5,
            budget: 200000,
            is_active: true,
            children: [],
          },
          {
            id: 3,
            code: 'FIN',
            name: 'المالية',
            name_ar: 'المالية',
            employee_count: 8,
            budget: 300000,
            is_active: true,
            children: [],
          },
          {
            id: 4,
            code: 'SALES',
            name: 'المبيعات',
            name_ar: 'المبيعات',
            employee_count: 20,
            budget: 600000,
            is_active: true,
            children: [],
          },
        ]);
      }
    } catch (error) {
      console.log('Using demo department data:', error);
      setDepartments([
        { id: 1, code: 'IT', name: 'تقنية المعلومات', employee_count: 15, children: [] },
        { id: 2, code: 'HR', name: 'الموارد البشرية', employee_count: 5, children: [] },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDepartments();
  }, [loadDepartments]);

  // Get flat list of departments for parent selector
  const getFlatDepartments = (depts, level = 0) => {
    let result = [];
    for (const dept of depts) {
      result.push({ ...dept, level });
      if (dept.children?.length > 0) {
        result = result.concat(getFlatDepartments(dept.children, level + 1));
      }
    }
    return result;
  };

  // Handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingDepartment) {
        const response = await apiClient.put(`/api/hr/departments/${editingDepartment.id}`, formData);
        if (response.success) {
          toast.success('تم تحديث بيانات القسم');
        } else {
          toast.success('وضع العرض - تم تحديث البيانات');
        }
      } else {
        const response = await apiClient.post('/api/hr/departments', formData);
        if (response.success) {
          toast.success('تم إضافة القسم بنجاح');
        } else {
          toast.success('وضع العرض - تم إضافة القسم');
        }
      }
      
      setShowModal(false);
      setEditingDepartment(null);
      resetForm();
      loadDepartments();
    } catch (error) {
      toast.success('وضع العرض - تم الحفظ');
      setShowModal(false);
    }
  };

  // Reset form
  const resetForm = () => {
    setFormData({
      code: '',
      name: '',
      name_ar: '',
      description: '',
      parent_id: '',
      manager_id: '',
      budget: '',
      budget_year: new Date().getFullYear(),
    });
  };

  // Open edit modal
  const openEditModal = (dept) => {
    setEditingDepartment(dept);
    setFormData({
      code: dept.code || '',
      name: dept.name || '',
      name_ar: dept.name_ar || '',
      description: dept.description || '',
      parent_id: dept.parent_id || '',
      manager_id: dept.manager_id || '',
      budget: dept.budget || '',
      budget_year: dept.budget_year || new Date().getFullYear(),
    });
    setShowModal(true);
  };

  // Toggle expand
  const toggleExpand = (deptId) => {
    setExpandedDepts(prev => {
      const newSet = new Set(prev);
      if (newSet.has(deptId)) {
        newSet.delete(deptId);
      } else {
        newSet.add(deptId);
      }
      return newSet;
    });
  };

  // Render department row
  const renderDepartmentRow = (dept, level = 0) => {
    const hasChildren = dept.children?.length > 0;
    const isExpanded = expandedDepts.has(dept.id);

    return (
      <React.Fragment key={dept.id}>
        <tr className="border-b border-border hover:bg-muted/50">
          <td className="px-4 py-3">
            <div className="flex items-center gap-2" style={{ paddingRight: `${level * 24}px` }}>
              {hasChildren && (
                <button
                  onClick={() => toggleExpand(dept.id)}
                  className="p-1 hover:bg-muted rounded"
                >
                  {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
                </button>
              )}
              {!hasChildren && <span className="w-6" />}
              <span className="font-mono bg-muted px-2 py-0.5 rounded text-sm">{dept.code}</span>
            </div>
          </td>
          <td className="px-4 py-3 font-medium">{dept.name_ar || dept.name}</td>
          <td className="px-4 py-3">
            <div className="flex items-center gap-1">
              <Users className="w-4 h-4 text-muted-foreground" />
              {dept.employee_count || 0}
            </div>
          </td>
          <td className="px-4 py-3">
            {dept.budget ? `${Number(dept.budget).toLocaleString()} ج.م` : '-'}
          </td>
          <td className="px-4 py-3">
            <span className={`px-2 py-1 rounded-full text-xs ${dept.is_active !== false ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'}`}>
              {dept.is_active !== false ? 'نشط' : 'غير نشط'}
            </span>
          </td>
          <td className="px-4 py-3">
            <div className="flex items-center gap-2">
              <button
                onClick={() => openEditModal(dept)}
                className="p-1 hover:bg-muted rounded"
                title="تعديل"
              >
                <Edit className="w-4 h-4" />
              </button>
              <button
                className="p-1 hover:bg-destructive/10 rounded text-destructive"
                title="حذف"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </td>
        </tr>
        {hasChildren && isExpanded && dept.children.map(child => renderDepartmentRow(child, level + 1))}
      </React.Fragment>
    );
  };

  // Calculate totals
  const calculateTotals = (depts) => {
    let totalEmployees = 0;
    let totalBudget = 0;
    
    const countRecursive = (items) => {
      for (const item of items) {
        totalEmployees += item.employee_count || 0;
        totalBudget += Number(item.budget) || 0;
        if (item.children?.length > 0) {
          countRecursive(item.children);
        }
      }
    };
    
    countRecursive(depts);
    return { totalEmployees, totalBudget };
  };

  const { totalEmployees, totalBudget } = calculateTotals(departments);

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground flex items-center gap-2">
            <Building2 className="w-8 h-8" />
            إدارة الأقسام
          </h1>
          <p className="text-muted-foreground mt-1">الهيكل التنظيمي للمؤسسة</p>
        </div>
        <button
          onClick={() => { resetForm(); setEditingDepartment(null); setShowModal(true); }}
          className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
        >
          <Plus className="w-5 h-5" />
          إضافة قسم
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-primary/10 rounded-lg">
              <Building2 className="w-6 h-6 text-primary" />
            </div>
            <div>
              <p className="text-2xl font-bold">{departments.length}</p>
              <p className="text-sm text-muted-foreground">إجمالي الأقسام</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-blue-500/10 rounded-lg">
              <Users className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{totalEmployees}</p>
              <p className="text-sm text-muted-foreground">إجمالي الموظفين</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-green-500/10 rounded-lg">
              <DollarSign className="w-6 h-6 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{totalBudget.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">إجمالي الميزانية</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Departments Table */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <FolderTree className="w-5 h-5" />
            الهيكل التنظيمي
          </CardTitle>
          <button
            onClick={loadDepartments}
            className="flex items-center gap-2 px-3 py-1 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            تحديث
          </button>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="flex items-center justify-center p-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-muted">
                  <tr>
                    <th className="px-4 py-3 text-right">الرمز</th>
                    <th className="px-4 py-3 text-right">اسم القسم</th>
                    <th className="px-4 py-3 text-right">الموظفين</th>
                    <th className="px-4 py-3 text-right">الميزانية</th>
                    <th className="px-4 py-3 text-right">الحالة</th>
                    <th className="px-4 py-3 text-right">الإجراءات</th>
                  </tr>
                </thead>
                <tbody>
                  {departments.map(dept => renderDepartmentRow(dept))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Add/Edit Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowModal(false)}>
          <div className="bg-background p-6 rounded-lg max-w-lg w-full mx-4" onClick={e => e.stopPropagation()}>
            <h2 className="text-xl font-bold mb-4">
              {editingDepartment ? 'تعديل بيانات القسم' : 'إضافة قسم جديد'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="code">رمز القسم *</Label>
                  <Input
                    id="code"
                    value={formData.code}
                    onChange={(e) => setFormData(prev => ({ ...prev, code: e.target.value.toUpperCase() }))}
                    required
                    disabled={!!editingDepartment}
                    placeholder="IT"
                  />
                </div>
                <div>
                  <Label htmlFor="parent_id">القسم الأب</Label>
                  <select
                    id="parent_id"
                    value={formData.parent_id}
                    onChange={(e) => setFormData(prev => ({ ...prev, parent_id: e.target.value }))}
                    className="w-full px-3 py-2 border border-border rounded-lg bg-background"
                  >
                    <option value="">بدون (قسم رئيسي)</option>
                    {getFlatDepartments(departments).map(dept => (
                      <option key={dept.id} value={dept.id} disabled={dept.id === editingDepartment?.id}>
                        {'—'.repeat(dept.level)} {dept.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <Label htmlFor="name">اسم القسم (English) *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                  required
                  placeholder="Information Technology"
                />
              </div>

              <div>
                <Label htmlFor="name_ar">اسم القسم (عربي)</Label>
                <Input
                  id="name_ar"
                  value={formData.name_ar}
                  onChange={(e) => setFormData(prev => ({ ...prev, name_ar: e.target.value }))}
                  placeholder="تقنية المعلومات"
                />
              </div>

              <div>
                <Label htmlFor="description">الوصف</Label>
                <textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  className="w-full px-3 py-2 border border-border rounded-lg bg-background resize-none"
                  rows={3}
                  placeholder="وصف القسم ومسؤولياته..."
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="budget">الميزانية</Label>
                  <Input
                    id="budget"
                    type="number"
                    value={formData.budget}
                    onChange={(e) => setFormData(prev => ({ ...prev, budget: e.target.value }))}
                    placeholder="0"
                  />
                </div>
                <div>
                  <Label htmlFor="budget_year">سنة الميزانية</Label>
                  <Input
                    id="budget_year"
                    type="number"
                    value={formData.budget_year}
                    onChange={(e) => setFormData(prev => ({ ...prev, budget_year: e.target.value }))}
                  />
                </div>
              </div>

              <div className="flex gap-2 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
                >
                  إلغاء
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
                >
                  {editingDepartment ? 'تحديث' : 'إضافة'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DepartmentsPage;
