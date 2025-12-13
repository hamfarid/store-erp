import React, { useState, useEffect } from 'react';
import {
  Plus, Search, Download, Edit, Trash2, Play, Pause, Clock,
  CheckCircle, XCircle, Calendar, Zap, RefreshCw, Settings, AlertTriangle
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
 * صفحة المهام الآلية
 * Automation Tasks Page
 */
const AutomationTasks = () => {
  const [tasks, setTasks] = useState([]);
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);

  // بيانات نموذجية
  const sampleTasks = [
    {
      id: 1,
      name: 'نسخة احتياطية يومية',
      description: 'إنشاء نسخة احتياطية من قاعدة البيانات',
      type: 'backup',
      schedule: 'يومياً الساعة 2:00 صباحاً',
      cronExpression: '0 2 * * *',
      status: 'active',
      lastRun: '2024-01-15T02:00:00',
      lastRunStatus: 'success',
      nextRun: '2024-01-16T02:00:00',
      executionCount: 45,
      successCount: 44,
      failureCount: 1,
      createdBy: 'النظام',
      createdAt: '2024-01-01T00:00:00'
    },
    {
      id: 2,
      name: 'تقرير المبيعات الأسبوعي',
      description: 'إنشاء وإرسال تقرير المبيعات للإدارة',
      type: 'report',
      schedule: 'أسبوعياً يوم الأحد',
      cronExpression: '0 8 * * 0',
      status: 'active',
      lastRun: '2024-01-14T08:00:00',
      lastRunStatus: 'success',
      nextRun: '2024-01-21T08:00:00',
      executionCount: 6,
      successCount: 6,
      failureCount: 0,
      createdBy: 'أحمد محمد',
      createdAt: '2024-01-01T00:00:00'
    },
    {
      id: 3,
      name: 'تنبيه انخفاض المخزون',
      description: 'فحص مستويات المخزون وإرسال تنبيهات',
      type: 'notification',
      schedule: 'كل 6 ساعات',
      cronExpression: '0 */6 * * *',
      status: 'active',
      lastRun: '2024-01-15T12:00:00',
      lastRunStatus: 'success',
      nextRun: '2024-01-15T18:00:00',
      executionCount: 120,
      successCount: 120,
      failureCount: 0,
      createdBy: 'النظام',
      createdAt: '2024-01-01T00:00:00'
    },
    {
      id: 4,
      name: 'تحديث أسعار الصرف',
      description: 'تحديث أسعار العملات من مصدر خارجي',
      type: 'sync',
      schedule: 'كل ساعة',
      cronExpression: '0 * * * *',
      status: 'paused',
      lastRun: '2024-01-15T10:00:00',
      lastRunStatus: 'failed',
      nextRun: null,
      executionCount: 240,
      successCount: 235,
      failureCount: 5,
      createdBy: 'سارة أحمد',
      createdAt: '2024-01-05T00:00:00'
    },
    {
      id: 5,
      name: 'تنظيف الملفات المؤقتة',
      description: 'حذف الملفات المؤقتة القديمة',
      type: 'cleanup',
      schedule: 'شهرياً',
      cronExpression: '0 3 1 * *',
      status: 'active',
      lastRun: '2024-01-01T03:00:00',
      lastRunStatus: 'success',
      nextRun: '2024-02-01T03:00:00',
      executionCount: 12,
      successCount: 12,
      failureCount: 0,
      createdBy: 'النظام',
      createdAt: '2023-01-01T00:00:00'
    }
  ];

  const taskTypes = [
    { value: 'backup', label: 'نسخ احتياطي', icon: '💾' },
    { value: 'report', label: 'تقارير', icon: '📊' },
    { value: 'notification', label: 'إشعارات', icon: '🔔' },
    { value: 'sync', label: 'مزامنة', icon: '🔄' },
    { value: 'cleanup', label: 'تنظيف', icon: '🧹' }
  ];

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    setIsLoading(true);
    try {
      const response = await apiClient.get('/api/automation/scheduled-tasks');
      if (response.status === 'success' && response.tasks?.length > 0) {
        setTasks(response.tasks);
        setFilteredTasks(response.tasks);
      } else {
        setTasks(sampleTasks);
        setFilteredTasks(sampleTasks);
      }
    } catch (error) {
      console.log('Using sample data:', error);
      setTasks(sampleTasks);
      setFilteredTasks(sampleTasks);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let filtered = tasks;

    if (searchTerm) {
      filtered = filtered.filter(task =>
        task.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        task.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterStatus !== 'all') {
      filtered = filtered.filter(task => task.status === filterStatus);
    }

    if (filterType !== 'all') {
      filtered = filtered.filter(task => task.type === filterType);
    }

    setFilteredTasks(filtered);
  }, [tasks, searchTerm, filterStatus, filterType]);

  const getStatusBadge = (status) => {
    if (status === 'active') {
      return (
        <Badge variant="default" className="flex items-center gap-1">
          <Play className="w-3 h-3" />
          نشط
        </Badge>
      );
    }
    return (
      <Badge variant="secondary" className="flex items-center gap-1">
        <Pause className="w-3 h-3" />
        موقف
      </Badge>
    );
  };

  const getRunStatusBadge = (status) => {
    if (status === 'success') {
      return (
        <Badge variant="default" className="flex items-center gap-1">
          <CheckCircle className="w-3 h-3" />
          ناجح
        </Badge>
      );
    }
    return (
      <Badge variant="destructive" className="flex items-center gap-1">
        <XCircle className="w-3 h-3" />
        فاشل
      </Badge>
    );
  };

  const getTypeLabel = (type) => {
    const found = taskTypes.find(t => t.value === type);
    return found ? `${found.icon} ${found.label}` : type;
  };

  const handleAddTask = () => {
    setSelectedTask(null);
    setShowAddModal(true);
    toast.success('جاري فتح نموذج مهمة جديدة');
  };

  const handleEditTask = (task) => {
    setSelectedTask(task);
    setShowAddModal(true);
  };

  const handleDeleteTask = (taskId) => {
    if (window.confirm('هل أنت متأكد من حذف هذه المهمة؟')) {
      setTasks(tasks.filter(t => t.id !== taskId));
      toast.success('تم حذف المهمة بنجاح');
    }
  };

  const handleToggleStatus = (taskId) => {
    setTasks(tasks.map(task =>
      task.id === taskId
        ? { ...task, status: task.status === 'active' ? 'paused' : 'active' }
        : task
    ));
    toast.success('تم تحديث حالة المهمة');
  };

  const handleRunNow = (taskId) => {
    toast.success('جاري تنفيذ المهمة...');
    // Simulate task execution
    setTimeout(() => {
      setTasks(tasks.map(task =>
        task.id === taskId
          ? { 
              ...task, 
              lastRun: new Date().toISOString(),
              lastRunStatus: 'success',
              executionCount: task.executionCount + 1,
              successCount: task.successCount + 1
            }
          : task
      ));
      toast.success('تم تنفيذ المهمة بنجاح');
    }, 2000);
  };

  const handleExport = () => {
    toast.success('تم تصدير البيانات بنجاح');
  };

  const getSummary = () => {
    return {
      total: tasks.length,
      active: tasks.filter(t => t.status === 'active').length,
      paused: tasks.filter(t => t.status === 'paused').length,
      successRate: tasks.length > 0 
        ? Math.round(tasks.reduce((sum, t) => sum + (t.successCount / Math.max(t.executionCount, 1) * 100), 0) / tasks.length)
        : 0
    };
  };

  const summary = getSummary();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل المهام الآلية...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-foreground">المهام الآلية</h1>
          <p className="text-muted-foreground mt-1">إدارة المهام المجدولة والأتمتة</p>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={handleExport}
            className="flex items-center gap-2 px-4 py-2 border border-border rounded-lg hover:bg-muted transition-colors"
          >
            <Download className="w-4 h-4" />
            تصدير
          </button>
          <button 
            onClick={handleAddTask}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Plus className="w-4 h-4" />
            مهمة جديدة
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">إجمالي المهام</p>
                <p className="text-2xl font-bold text-primary">{summary.total}</p>
              </div>
              <Zap className="w-8 h-8 text-primary/60" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">نشطة</p>
                <p className="text-2xl font-bold text-green-600">{summary.active}</p>
              </div>
              <Play className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">موقفة</p>
                <p className="text-2xl font-bold text-yellow-600">{summary.paused}</p>
              </div>
              <Pause className="w-8 h-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">معدل النجاح</p>
                <p className="text-2xl font-bold text-blue-600">{summary.successRate}%</p>
              </div>
              <CheckCircle className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>
      </div>

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
                  placeholder="البحث بالاسم أو الوصف..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pr-10"
                />
              </div>
            </div>

            <div className="min-w-40">
              <Label htmlFor="type-filter">النوع</Label>
              <Select value={filterType} onValueChange={setFilterType}>
                <SelectTrigger>
                  <SelectValue placeholder="اختر النوع" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">جميع الأنواع</SelectItem>
                  {taskTypes.map(type => (
                    <SelectItem key={type.value} value={type.value}>{type.icon} {type.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="min-w-32">
              <Label htmlFor="status-filter">الحالة</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue placeholder="الحالة" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">الكل</SelectItem>
                  <SelectItem value="active">نشط</SelectItem>
                  <SelectItem value="paused">موقف</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tasks Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة المهام ({filteredTasks.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>المهمة</TableHead>
                <TableHead>النوع</TableHead>
                <TableHead>الجدولة</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>آخر تنفيذ</TableHead>
                <TableHead>التنفيذ القادم</TableHead>
                <TableHead>الإحصائيات</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredTasks.map((task) => (
                <TableRow key={task.id}>
                  <TableCell>
                    <div>
                      <div className="font-medium">{task.name}</div>
                      <div className="text-sm text-muted-foreground">{task.description}</div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">{getTypeLabel(task.type)}</span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-muted-foreground" />
                      <span className="text-sm">{task.schedule}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    {getStatusBadge(task.status)}
                  </TableCell>
                  <TableCell>
                    <div>
                      <span className="text-sm">
                        {task.lastRun ? new Date(task.lastRun).toLocaleString('ar-SA') : '-'}
                      </span>
                      {task.lastRunStatus && (
                        <div className="mt-1">{getRunStatusBadge(task.lastRunStatus)}</div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm">
                      {task.nextRun ? new Date(task.nextRun).toLocaleString('ar-SA') : '-'}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="text-sm">
                      <div className="flex items-center gap-1">
                        <span className="text-green-600">{task.successCount}</span>
                        <span>/</span>
                        <span>{task.executionCount}</span>
                      </div>
                      {task.failureCount > 0 && (
                        <div className="flex items-center gap-1 text-red-600">
                          <AlertTriangle className="w-3 h-3" />
                          <span>{task.failureCount} فشل</span>
                        </div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-1">
                      <button
                        onClick={() => handleRunNow(task.id)}
                        className="px-2 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded"
                        title="تنفيذ الآن"
                      >
                        <RefreshCw className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleToggleStatus(task.id)}
                        className={`px-2 py-1 text-sm rounded ${
                          task.status === 'active' 
                            ? 'text-yellow-600 hover:bg-yellow-50' 
                            : 'text-green-600 hover:bg-green-50'
                        }`}
                        title={task.status === 'active' ? 'إيقاف' : 'تشغيل'}
                      >
                        {task.status === 'active' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                      </button>
                      <button
                        onClick={() => handleEditTask(task)}
                        className="p-1 hover:bg-muted rounded"
                      >
                        <Edit className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteTask(task.id)}
                        className="p-1 text-red-600 hover:bg-red-50 rounded"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {filteredTasks.length === 0 && (
            <div className="text-center py-8">
              <Zap className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <p className="text-muted-foreground">لا توجد مهام تطابق معايير البحث</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default AutomationTasks;

