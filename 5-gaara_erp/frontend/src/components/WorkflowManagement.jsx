import React, { useState, useEffect } from 'react'
import {
  Plus, Search, Filter, Download, Edit, Trash2, Eye, Calendar, DollarSign, FileText, Settings, Users, Package, ShoppingCart, BarChart3, TrendingUp, AlertCircle, CheckCircle, X, Menu,
  GitBranch, AlertTriangle, Play, Clock
} from 'lucide-react'
import { toast } from 'react-hot-toast'

import ApiService from '../services/ApiService'

const WorkflowManagement = () => {
  const [loading, setLoading] = useState(false)
  const [workflows, setWorkflows] = useState([])
  const [activeWorkflows, setActiveWorkflows] = useState([])
  const [activeTab, setActiveTab] = useState('workflows')
  // const [newWorkflow, setNewWorkflow] = useState({ // Currently unused (only setter used)
  //   name: '',
  //   description: '',
  //   category: 'approval',
  //   steps: [],
  //   triggers: [],
  //   conditions: []
  // })
  const [_selectedWorkflow, setSelectedWorkflow] = useState(null)
  const [_isCreatingWorkflow, setIsCreatingWorkflow] = useState(false)

  const workflowCategories = [
    { value: 'approval', label: 'سير عمل الموافقات', icon: CheckCircle },
    { value: 'inventory', label: 'سير عمل المخزون', icon: GitBranch },
    { value: 'financial', label: 'سير عمل مالي', icon: FileText },
    { value: 'notification', label: 'سير عمل الإشعارات', icon: AlertTriangle },
    { value: 'custom', label: 'سير عمل مخصص', icon: Settings }
  ]

  useEffect(() => {
    loadWorkflows()
    loadActiveWorkflows()
  }, [])

  const loadWorkflows = async () => {
    try {
      setLoading(true)
      const response = await ApiService.get('/api/workflows')
      if (response.success) {
        setWorkflows(response.data)
      } else {
        // Mock data
        setWorkflows([
          {
            id: 1,
            name: 'موافقة الفواتير الكبيرة',
            description: 'سير عمل لموافقة الفواتير التي تزيد عن 10,000 جنيه',
            category: 'approval',
            status: 'active',
            steps: [
              { id: 1, name: 'مراجعة المحاسب', type: 'approval', assignee: 'المحاسب الرئيسي' },
              { id: 2, name: 'موافقة المدير المالي', type: 'approval', assignee: 'المدير المالي' },
              { id: 3, name: 'إشعار العميل', type: 'notification', assignee: 'النظام' }
            ],
            triggers: [{ type: 'event', condition: 'invoice_amount > 10000' }],
            createdAt: '2024-01-15T10:00:00Z',
            lastRun: '2024-01-15T14:30:00Z',
            runCount: 25
          },
          {
            id: 2,
            name: 'تنبيه المخزون المنخفض',
            description: 'إشعار تلقائي عند انخفاض مستوى المخزون',
            category: 'inventory',
            status: 'active',
            steps: [
              { id: 1, name: 'فحص مستوى المخزون', type: 'condition', assignee: 'النظام' },
              { id: 2, name: 'إشعار مدير المخزون', type: 'notification', assignee: 'مدير المخزون' },
              { id: 3, name: 'إنشاء طلب شراء', type: 'action', assignee: 'النظام' }
            ],
            triggers: [{ type: 'schedule', condition: 'daily_at_09:00' }],
            createdAt: '2024-01-10T08:00:00Z',
            lastRun: '2024-01-15T09:00:00Z',
            runCount: 120
          }
        ])
      }
    } catch (error) {
      toast.error('خطأ في تحميل سير العمل')
    } finally {
      setLoading(false)
    }
  }

  const loadActiveWorkflows = async () => {
    try {
      const response = await ApiService.get('/api/workflows/active')
      if (response.success) {
        setActiveWorkflows(response.data)
      } else {
        // Mock data
        setActiveWorkflows([
          {
            id: 1,
            workflowId: 1,
            workflowName: 'موافقة الفواتير الكبيرة',
            entityType: 'invoice',
            entityId: 'INV-2024-001',
            currentStep: 2,
            totalSteps: 3,
            status: 'pending',
            assignee: 'المدير المالي',
            startedAt: '2024-01-15T14:30:00Z',
            dueDate: '2024-01-16T14:30:00Z'
          },
          {
            id: 2,
            workflowId: 1,
            workflowName: 'موافقة الفواتير الكبيرة',
            entityType: 'invoice',
            entityId: 'INV-2024-002',
            currentStep: 1,
            totalSteps: 3,
            status: 'pending',
            assignee: 'المحاسب الرئيسي',
            startedAt: '2024-01-15T15:00:00Z',
            dueDate: '2024-01-16T15:00:00Z'
          }
        ])
      }
    } catch (error) {
      }
  }

  // TODO: Wire up these functions to UI components
  // const createWorkflow = async () => { // Currently unused
  //   try {
  //     if (!newWorkflow.name.trim()) {
  //       toast.error('اسم سير العمل مطلوب')
  //       return
  //     }
  //
  //     if (newWorkflow.steps.length === 0) {
  //       toast.error('يجب إضافة خطوة واحدة على الأقل')
  //       return
  //     }
  //
  //     const response = await ApiService.post('/api/workflows', newWorkflow)
  //     if (response.success) {
  //       setWorkflows(prev => [...prev, { ...newWorkflow, id: Date.now(), status: 'draft', runCount: 0 }])
  //       setNewWorkflow({
  //         name: '',
  //         description: '',
  //         category: 'approval',
  //         steps: [],
  //         triggers: [],
  //         conditions: []
  //       })
  //       setIsCreatingWorkflow(false)
  //       toast.success('تم إنشاء سير العمل بنجاح')
  //     }
  //   } catch (error) {
  //     toast.error('خطأ في إنشاء سير العمل')
  //   }
  // }

  const toggleWorkflowStatus = async (workflowId, currentStatus) => {
    try {
      const newStatus = currentStatus === 'active' ? 'inactive' : 'active'
      const response = await ApiService.patch(`/api/workflows/${workflowId}/status`, { status: newStatus })

      if (response.success) {
        setWorkflows(prev => prev.map(w =>
          w.id === workflowId ? { ...w, status: newStatus } : w
        ))
        toast.success(`تم ${newStatus === 'active' ? 'تفعيل' : 'إيقاف'} سير العمل`)
      }
    } catch (error) {
      toast.error('خطأ في تغيير حالة سير العمل')
    }
  }

  const deleteWorkflow = async (workflowId) => {
    try {
      if (window.confirm('هل أنت متأكد من حذف سير العمل؟')) {
        const response = await ApiService.delete(`/api/workflows/${workflowId}`)
        if (response.success) {
          setWorkflows(prev => prev.filter(w => w.id !== workflowId))
          toast.success('تم حذف سير العمل بنجاح')
        }
      }
    } catch (error) {
      toast.error('خطأ في حذف سير العمل')
    }
  }

  // const addStep = () => { // Currently unused
  //   const newStep = {
  //     id: Date.now(),
  //     name: '',
  //     type: 'approval',
  //     assignee: '',
  //     conditions: [],
  //     actions: []
  //   }
  //   setNewWorkflow(prev => ({
  //     ...prev,
  //     steps: [...prev.steps, newStep]
  //   }))
  // }

  // const updateStep = (stepId, field, value) => { // Currently unused
  //   setNewWorkflow(prev => ({
  //     ...prev,
  //     steps: prev.steps.map(step =>
  //       step.id === stepId ? { ...step, [field]: value } : step
  //     )
  //   }))
  // }

  // const removeStep = (stepId) => { // Currently unused
  //   setNewWorkflow(prev => ({
  //     ...prev,
  //     steps: prev.steps.filter(step => step.id !== stepId)
  //   }))
  // }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-5 h-5 text-primary" />
      case 'inactive':
        return <Pause className="w-5 h-5 text-muted-foreground" />
      case 'pending':
        return <Clock className="w-5 h-5 text-accent" />
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-primary" />
      case 'failed':
        return <XCircle className="w-5 h-5 text-destructive" />
      default:
        return <Square className="w-5 h-5 text-muted-foreground" />
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'active': return 'نشط'
      case 'inactive': return 'غير نشط'
      case 'pending': return 'في الانتظار'
      case 'completed': return 'مكتمل'
      case 'failed': return 'فشل'
      case 'draft': return 'مسودة'
      default: return status
    }
  }

  const getCategoryIcon = (category) => {
    const categoryData = workflowCategories.find(c => c.value === category)
    return categoryData ? <categoryData.icon className="w-5 h-5" /> : <GitBranch className="w-5 h-5" />
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('ar-EG')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto p-6" dir="rtl">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-border p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <GitBranch className="w-8 h-8 text-primary-600 ml-3" />
            <div>
              <h1 className="text-2xl font-bold text-foreground">إدارة سير العمل</h1>
              <p className="text-muted-foreground">إنشاء وإدارة سير العمل التلقائي للعمليات المختلفة</p>
            </div>
          </div>

          <button
            onClick={() => setIsCreatingWorkflow(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
          >
            <Plus className="w-4 h-4 ml-2" />
            إنشاء سير عمل جديد
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-primary-100 rounded-lg">
              <GitBranch className="w-6 h-6 text-primary-600" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">إجمالي سير العمل</p>
              <p className="text-2xl font-bold text-foreground">{workflows.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-primary/20 rounded-lg">
              <CheckCircle className="w-6 h-6 text-primary" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">سير العمل النشط</p>
              <p className="text-2xl font-bold text-foreground">
                {workflows.filter(w => w.status === 'active').length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-accent/20 rounded-lg">
              <Clock className="w-6 h-6 text-accent" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">في الانتظار</p>
              <p className="text-2xl font-bold text-foreground">{activeWorkflows.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-border p-6">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Users className="w-6 h-6 text-purple-600" />
            </div>
            <div className="mr-4">
              <p className="text-sm font-medium text-muted-foreground">المهام المعلقة</p>
              <p className="text-2xl font-bold text-foreground">
                {activeWorkflows.filter(w => w.status === 'pending').length}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-border">
        <div className="border-b border-border">
          <nav className="-mb-px flex space-x-8 space-x-reverse px-6">
            {[
              { id: 'workflows', name: 'سير العمل', icon: GitBranch },
              { id: 'active', name: 'المهام النشطة', icon: Clock },
              { id: 'history', name: 'السجل', icon: FileText }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center`}
              >
                <tab.icon className="w-4 h-4 ml-2" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'workflows' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">جميع سير العمل</h3>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {workflows.map((workflow) => (
                  <div key={workflow.id} className="bg-muted/50 rounded-lg p-6 border border-border">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center">
                        {getCategoryIcon(workflow.category)}
                        <h4 className="text-lg font-medium text-foreground mr-2">{workflow.name}</h4>
                      </div>
                      <div className="flex items-center space-x-2 space-x-reverse">
                        {getStatusIcon(workflow.status)}
                        <span className="text-sm text-muted-foreground">{getStatusText(workflow.status)}</span>
                      </div>
                    </div>

                    <p className="text-sm text-muted-foreground mb-4">{workflow.description}</p>

                    <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                      <span>{workflow.steps.length} خطوة</span>
                      <span>تم التشغيل {workflow.runCount} مرة</span>
                    </div>

                    {workflow.lastRun && (
                      <div className="text-xs text-gray-400 mb-4">
                        آخر تشغيل: {formatDate(workflow.lastRun)}
                      </div>
                    )}

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2 space-x-reverse">
                        <button
                          onClick={() => setSelectedWorkflow(workflow)}
                          className="text-primary-600 hover:text-primary-900"
                          title="عرض التفاصيل"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => {
                            // setNewWorkflow(workflow) // Currently unused
                            setIsCreatingWorkflow(true)
                          }}
                          className="text-muted-foreground hover:text-foreground"
                          title="تعديل"
                        >
                          <Edit className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => deleteWorkflow(workflow.id)}
                          className="text-destructive hover:text-red-900"
                          title="حذف"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>

                      <button
                        onClick={() => toggleWorkflowStatus(workflow.id, workflow.status)}
                        className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${
                          workflow.status === 'active'
                            ? 'bg-destructive/20 text-red-800 hover:bg-red-200'
                            : 'bg-primary/20 text-green-800 hover:bg-green-200'
                        }`}
                      >
                        {workflow.status === 'active' ? (
                          <>
                            <Pause className="w-3 h-3 ml-1" />
                            إيقاف
                          </>
                        ) : (
                          <>
                            <Play className="w-3 h-3 ml-1" />
                            تفعيل
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'active' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">المهام النشطة</h3>

              <div className="space-y-4">
                {activeWorkflows.map((workflow) => (
                  <div key={workflow.id} className="bg-white border border-border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h4 className="font-medium text-foreground">{workflow.workflowName}</h4>
                        <p className="text-sm text-muted-foreground">
                          {workflow.entityType}: {workflow.entityId}
                        </p>
                      </div>
                      <div className="text-left">
                        {getStatusIcon(workflow.status)}
                      </div>
                    </div>

                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center">
                        <Users className="w-4 h-4 text-gray-400 ml-1" />
                        <span className="text-sm text-muted-foreground">{workflow.assignee}</span>
                      </div>
                      <div className="flex items-center">
                        <Calendar className="w-4 h-4 text-gray-400 ml-1" />
                        <span className="text-sm text-muted-foreground">
                          {formatDate(workflow.dueDate)}
                        </span>
                      </div>
                    </div>

                    <div className="w-full bg-muted rounded-full h-2 mb-3">
                      <div
                        className="bg-primary-600 h-2 rounded-full"
                        style={{ width: `${(workflow.currentStep / workflow.totalSteps) * 100}%` }}
                      ></div>
                    </div>

                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">
                        الخطوة {workflow.currentStep} من {workflow.totalSteps}
                      </span>
                      <div className="flex items-center space-x-2 space-x-reverse">
                        <button className="text-primary hover:text-green-800">
                          <CheckCircle className="w-4 h-4" />
                        </button>
                        <button className="text-destructive hover:text-red-800">
                          <XCircle className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'history' && (
            <div>
              <h3 className="text-lg font-semibold text-foreground mb-4">سجل سير العمل</h3>
              <div className="text-center text-gray-500 py-8">
                سيتم عرض سجل تشغيل سير العمل هنا
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default WorkflowManagement
