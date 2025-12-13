import React, { useState, useEffect } from 'react';
import {
  UserPlus, Search, Filter, Phone, Mail, Building2, Calendar, Star,
  ArrowRight, MessageSquare, Clock, CheckCircle, XCircle, Target,
  TrendingUp, DollarSign, Edit, Trash2, Eye
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
 * صفحة العملاء المحتملين (CRM)
 * Potential Customers CRM Page
 */
const PotentialCustomers = () => {
  const [customers, setCustomers] = useState([]);
  const [filteredCustomers, setFilteredCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStage, setFilterStage] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  // بيانات نموذجية
  const sampleCustomers = [
    {
      id: 1,
      name: 'شركة التقنية المتقدمة',
      contact_person: 'محمد العلي',
      email: 'mohammed@techadvanced.com',
      phone: '0501234567',
      company_size: 'medium',
      industry: 'تقنية المعلومات',
      source: 'موقع الويب',
      stage: 'qualified',
      priority: 'high',
      expected_value: 150000,
      probability: 70,
      next_action: 'اتصال متابعة',
      next_action_date: '2024-01-20',
      assigned_to: 'أحمد محمد',
      notes: 'مهتم بنظام إدارة المخزون',
      created_at: '2024-01-10'
    },
    {
      id: 2,
      name: 'مؤسسة البناء الحديث',
      contact_person: 'خالد الأحمد',
      email: 'khaled@modernbuild.com',
      phone: '0507654321',
      company_size: 'large',
      industry: 'البناء والتشييد',
      source: 'معرض تجاري',
      stage: 'proposal',
      priority: 'high',
      expected_value: 300000,
      probability: 85,
      next_action: 'تقديم العرض',
      next_action_date: '2024-01-18',
      assigned_to: 'سارة محمد',
      notes: 'يحتاج حل متكامل للمشاريع',
      created_at: '2024-01-05'
    },
    {
      id: 3,
      name: 'متجر الإلكترونيات',
      contact_person: 'عبدالله سعيد',
      email: 'abdullah@electronics.com',
      phone: '0509876543',
      company_size: 'small',
      industry: 'التجزئة',
      source: 'إحالة عميل',
      stage: 'new',
      priority: 'medium',
      expected_value: 50000,
      probability: 30,
      next_action: 'اتصال أولي',
      next_action_date: '2024-01-22',
      assigned_to: 'محمد علي',
      notes: 'عميل جديد محتمل',
      created_at: '2024-01-15'
    },
    {
      id: 4,
      name: 'مصنع المنتجات الغذائية',
      contact_person: 'فهد العتيبي',
      email: 'fahd@foodfactory.com',
      phone: '0505551234',
      company_size: 'large',
      industry: 'الصناعات الغذائية',
      source: 'إعلان رقمي',
      stage: 'negotiation',
      priority: 'high',
      expected_value: 500000,
      probability: 90,
      next_action: 'توقيع العقد',
      next_action_date: '2024-01-19',
      assigned_to: 'أحمد محمد',
      notes: 'في مرحلة التفاوض النهائية',
      created_at: '2023-12-20'
    },
    {
      id: 5,
      name: 'شركة الخدمات اللوجستية',
      contact_person: 'سلطان الشمري',
      email: 'sultan@logistics.com',
      phone: '0502223333',
      company_size: 'medium',
      industry: 'النقل والخدمات اللوجستية',
      source: 'LinkedIn',
      stage: 'lost',
      priority: 'low',
      expected_value: 100000,
      probability: 0,
      next_action: 'متابعة بعد 3 أشهر',
      next_action_date: '2024-04-01',
      assigned_to: 'سارة محمد',
      notes: 'اختار منافس - متابعة لاحقة',
      created_at: '2023-11-15'
    },
    {
      id: 6,
      name: 'مجموعة الاستثمار',
      contact_person: 'نايف الدوسري',
      email: 'naif@investment.com',
      phone: '0508889999',
      company_size: 'large',
      industry: 'الاستثمار والتمويل',
      source: 'موقع الويب',
      stage: 'won',
      priority: 'high',
      expected_value: 250000,
      probability: 100,
      next_action: 'تنفيذ المشروع',
      next_action_date: '2024-01-25',
      assigned_to: 'محمد علي',
      notes: 'تم التعاقد بنجاح',
      created_at: '2023-12-01'
    }
  ];

  const stageConfig = {
    new: { label: 'جديد', color: 'bg-blue-100 text-blue-800', icon: UserPlus },
    contacted: { label: 'تم التواصل', color: 'bg-cyan-100 text-cyan-800', icon: Phone },
    qualified: { label: 'مؤهل', color: 'bg-purple-100 text-purple-800', icon: CheckCircle },
    proposal: { label: 'تقديم عرض', color: 'bg-yellow-100 text-yellow-800', icon: Target },
    negotiation: { label: 'تفاوض', color: 'bg-orange-100 text-orange-800', icon: MessageSquare },
    won: { label: 'تم التعاقد', color: 'bg-green-100 text-green-800', icon: Star },
    lost: { label: 'خسر', color: 'bg-red-100 text-red-800', icon: XCircle }
  };

  const priorityConfig = {
    high: { label: 'عالية', color: 'bg-red-100 text-red-700' },
    medium: { label: 'متوسطة', color: 'bg-yellow-100 text-yellow-700' },
    low: { label: 'منخفضة', color: 'bg-gray-100 text-gray-700' }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/crm/potential-customers');
      if (response.success && response.data?.length > 0) {
        setCustomers(response.data);
        setFilteredCustomers(response.data);
      } else {
        setCustomers(sampleCustomers);
        setFilteredCustomers(sampleCustomers);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setCustomers(sampleCustomers);
      setFilteredCustomers(sampleCustomers);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = customers;

    if (searchTerm) {
      filtered = filtered.filter(c =>
        c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.contact_person.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.email.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterStage !== 'all') {
      filtered = filtered.filter(c => c.stage === filterStage);
    }

    if (filterPriority !== 'all') {
      filtered = filtered.filter(c => c.priority === filterPriority);
    }

    setFilteredCustomers(filtered);
  }, [customers, searchTerm, filterStage, filterPriority]);

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-SA', {
      style: 'currency',
      currency: 'SAR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const getStage = (stage) => {
    const config = stageConfig[stage] || stageConfig.new;
    const Icon = config.icon;
    return (
      <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${config.color}`}>
        <Icon className="w-3 h-3" />
        {config.label}
      </span>
    );
  };

  const getPriority = (priority) => {
    const config = priorityConfig[priority] || priorityConfig.medium;
    return (
      <span className={`px-2 py-0.5 text-xs font-medium rounded ${config.color}`}>
        {config.label}
      </span>
    );
  };

  // const handleStageChange = (customerId, newStage) => { // Currently unused
  //   setCustomers(customers.map(c =>
  //     c.id === customerId ? { ...c, stage: newStage } : c
  //   ));
  //   toast.success(`تم تحديث المرحلة إلى: ${stageConfig[newStage]?.label}`);
  // };

  const handleConvertToCustomer = (customerId) => {
    toast.success('تم تحويل العميل المحتمل إلى عميل فعلي');
    setCustomers(customers.map(c =>
      c.id === customerId ? { ...c, stage: 'won' } : c
    ));
  };

  // Calculate summary
  const summary = {
    total: customers.length,
    new: customers.filter(c => c.stage === 'new').length,
    qualified: customers.filter(c => c.stage === 'qualified').length,
    negotiation: customers.filter(c => c.stage === 'negotiation').length,
    won: customers.filter(c => c.stage === 'won').length,
    pipeline: customers
      .filter(c => !['won', 'lost'].includes(c.stage))
      .reduce((sum, c) => sum + (c.expected_value * c.probability / 100), 0),
    totalValue: customers.filter(c => c.stage === 'won').reduce((sum, c) => sum + c.expected_value, 0)
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري التحميل...</p>
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
            <UserPlus className="w-8 h-8" />
            العملاء المحتملين
          </h1>
          <p className="text-muted-foreground mt-1">إدارة علاقات العملاء (CRM)</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
          <UserPlus className="w-4 h-4" />
          إضافة عميل محتمل
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">الإجمالي</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <UserPlus className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">جدد</p>
                <p className="text-2xl font-bold text-blue-600">{summary.new}</p>
              </div>
              <UserPlus className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">مؤهلين</p>
                <p className="text-2xl font-bold text-purple-600">{summary.qualified}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">قيد التفاوض</p>
                <p className="text-2xl font-bold text-orange-600">{summary.negotiation}</p>
              </div>
              <MessageSquare className="w-8 h-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">قيمة الأنبوب</p>
                <p className="text-lg font-bold text-green-600">{formatCurrency(summary.pipeline)}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">تم التعاقد</p>
                <p className="text-lg font-bold text-emerald-600">{formatCurrency(summary.totalValue)}</p>
              </div>
              <DollarSign className="w-8 h-8 text-emerald-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Pipeline Funnel */}
      <Card>
        <CardHeader>
          <CardTitle>قمع المبيعات</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between gap-2">
            {Object.entries(stageConfig).map(([stage, config], index) => {
              const count = customers.filter(c => c.stage === stage).length;
              const Icon = config.icon;
              return (
                <React.Fragment key={stage}>
                  <div className="flex-1 text-center">
                    <div className={`p-3 rounded-lg ${config.color} mx-auto w-fit`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <p className="text-sm font-medium mt-2">{config.label}</p>
                    <p className="text-2xl font-bold">{count}</p>
                  </div>
                  {index < Object.keys(stageConfig).length - 1 && (
                    <ArrowRight className="w-5 h-5 text-muted-foreground flex-shrink-0" />
                  )}
                </React.Fragment>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-64">
              <Label htmlFor="search">البحث</Label>
              <div className="relative">
                <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
                <Input
                  id="search"
                  placeholder="البحث بالاسم أو البريد..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-40">
              <Label htmlFor="stage-filter">المرحلة</Label>
              <Select value={filterStage} onValueChange={setFilterStage}>
                <SelectTrigger>
                  <SelectValue placeholder="الكل" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  {Object.entries(stageConfig).map(([key, config]) => (
                    <SelectItem key={key} value={key}>{config.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="priority-filter">الأولوية</Label>
              <Select value={filterPriority} onValueChange={setFilterPriority}>
                <SelectTrigger>
                  <SelectValue placeholder="الكل" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  {Object.entries(priorityConfig).map(([key, config]) => (
                    <SelectItem key={key} value={key}>{config.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Customers Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة العملاء المحتملين ({filteredCustomers.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>الشركة</TableHead>
                <TableHead>جهة الاتصال</TableHead>
                <TableHead>المصدر</TableHead>
                <TableHead>القيمة المتوقعة</TableHead>
                <TableHead>الاحتمالية</TableHead>
                <TableHead>المرحلة</TableHead>
                <TableHead>الأولوية</TableHead>
                <TableHead>الإجراء التالي</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredCustomers.map((customer) => (
                <TableRow key={customer.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium flex items-center gap-1">
                        <Building2 className="w-4 h-4 text-muted-foreground" />
                        {customer.name}
                      </div>
                      <div className="text-sm text-muted-foreground">{customer.industry}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="font-medium">{customer.contact_person}</div>
                      <div className="flex items-center gap-1 text-sm text-muted-foreground">
                        <Mail className="w-3 h-3" />
                        {customer.email}
                      </div>
                      <div className="flex items-center gap-1 text-sm text-muted-foreground">
                        <Phone className="w-3 h-3" />
                        {customer.phone}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">{customer.source}</Badge>
                  </TableCell>
                  <TableCell className="font-mono font-bold">
                    {formatCurrency(customer.expected_value)}
                  </TableCell>
                  <TableCell>
                    <div className="w-full bg-muted h-2 rounded-full">
                      <div
                        className={`h-2 rounded-full ${customer.probability >= 70 ? 'bg-green-500' : customer.probability >= 40 ? 'bg-yellow-500' : 'bg-red-500'}`}
                        style={{ width: `${customer.probability}%` }}
                      />
                    </div>
                    <span className="text-xs">{customer.probability}%</span>
                  </TableCell>
                  <TableCell>{getStage(customer.stage)}</TableCell>
                  <TableCell>{getPriority(customer.priority)}</TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="text-sm font-medium">{customer.next_action}</div>
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Calendar className="w-3 h-3" />
                        {new Date(customer.next_action_date).toLocaleDateString('ar-SA')}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <button className="p-2 hover:bg-muted rounded" title="عرض">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button className="p-2 hover:bg-muted rounded" title="تعديل">
                        <Edit className="w-4 h-4" />
                      </button>
                      {customer.stage === 'negotiation' && (
                        <button
                          onClick={() => handleConvertToCustomer(customer.id)}
                          className="p-2 text-green-600 hover:bg-green-50 rounded"
                          title="تحويل لعميل"
                        >
                          <Star className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredCustomers.length === 0 && (
            <div className="text-center py-8">
              <UserPlus className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا يوجد عملاء محتملين</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PotentialCustomers;

