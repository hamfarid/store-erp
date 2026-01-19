/**
 * Accounting Management Page - إدارة المحاسبة
 * Gaara ERP v12
 *
 * Complete accounting and financial management with journal entries, invoices, and reporting.
 *
 * @author Global v35.0 Singularity
 * @version 2.0.0
 */

import { useState, useEffect, useCallback } from "react"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Calculator,
  TrendingUp,
  TrendingDown,
  DollarSign,
  FileText,
  PieChart,
  BookOpen,
  Receipt,
  CreditCard,
  Building2,
  RefreshCw,
  Download,
  Plus,
  Filter,
  Search,
  Calendar,
  ArrowUpRight,
  ArrowDownRight,
  MoreVertical,
  Eye,
  Edit,
  Trash2,
  CheckCircle2,
  Clock,
  XCircle,
  Wallet,
  ArrowRightLeft,
  CircleDollarSign,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { DataTable } from "@/components/common"
import { ConfirmDialog, FormDialog, ViewDialog } from "@/components/dialogs"

// Form schemas
const journalSchema = z.object({
  date: z.string().min(1, "التاريخ مطلوب"),
  reference: z.string().optional(),
  description: z.string().min(3, "الوصف مطلوب"),
  entries: z.array(z.object({
    account_id: z.string(),
    account_name: z.string(),
    debit: z.number().min(0),
    credit: z.number().min(0),
  })).min(2, "يجب إدخال قيدين على الأقل"),
  notes: z.string().optional(),
})

const invoiceSchema = z.object({
  customer_id: z.string().min(1, "العميل مطلوب"),
  customer_name: z.string(),
  invoice_date: z.string().min(1, "تاريخ الفاتورة مطلوب"),
  due_date: z.string().min(1, "تاريخ الاستحقاق مطلوب"),
  items: z.array(z.object({
    description: z.string(),
    quantity: z.number().min(1),
    unit_price: z.number().min(0),
    tax_rate: z.number().min(0).default(15),
  })),
  notes: z.string().optional(),
})

// Status configurations
const statusConfig = {
  draft: { label: "مسودة", variant: "outline", color: "text-gray-500" },
  pending: { label: "معلق", variant: "secondary", color: "text-yellow-500" },
  posted: { label: "مرحّل", variant: "default", color: "text-blue-500" },
  paid: { label: "مدفوع", variant: "default", color: "text-green-500" },
  partial: { label: "مدفوع جزئياً", variant: "secondary", color: "text-orange-500" },
  overdue: { label: "متأخر", variant: "destructive", color: "text-red-500" },
  cancelled: { label: "ملغي", variant: "destructive", color: "text-red-500" },
}

// Mock data
const mockJournalEntries = [
  { id: "JE-001", date: "2026-01-17", reference: "INV-001", description: "مبيعات نقدية", total_debit: 5750, total_credit: 5750, status: "posted", created_by: "أحمد محمد" },
  { id: "JE-002", date: "2026-01-16", reference: "PO-001", description: "شراء بضاعة", total_debit: 15000, total_credit: 15000, status: "posted", created_by: "خالد علي" },
  { id: "JE-003", date: "2026-01-15", reference: "EXP-001", description: "مصاريف إدارية", total_debit: 3500, total_credit: 3500, status: "draft", created_by: "سارة أحمد" },
]

const mockInvoices = [
  { id: "INV-001", customer: "شركة الزراعة الحديثة", date: "2026-01-17", due_date: "2026-02-16", total: 45000, tax: 6750, grand_total: 51750, paid: 51750, balance: 0, status: "paid" },
  { id: "INV-002", customer: "مزرعة النخيل الذهبي", date: "2026-01-15", due_date: "2026-02-14", total: 28000, tax: 4200, grand_total: 32200, paid: 15000, balance: 17200, status: "partial" },
  { id: "INV-003", customer: "أحمد محمد العلي", date: "2026-01-10", due_date: "2026-01-25", total: 12000, tax: 1800, grand_total: 13800, paid: 0, balance: 13800, status: "overdue" },
]

const mockPayments = [
  { id: "PAY-001", date: "2026-01-17", customer: "شركة الزراعة الحديثة", invoice: "INV-001", amount: 51750, method: "تحويل بنكي", status: "completed" },
  { id: "PAY-002", date: "2026-01-16", customer: "مزرعة النخيل الذهبي", invoice: "INV-002", amount: 15000, method: "نقدي", status: "completed" },
]

const mockAccounts = [
  { id: "1100", name: "النقدية", name_en: "Cash", type: "asset", balance: 125000 },
  { id: "1200", name: "البنك", name_en: "Bank", type: "asset", balance: 580000 },
  { id: "1300", name: "المدينون", name_en: "Accounts Receivable", type: "asset", balance: 95000 },
  { id: "2100", name: "الدائنون", name_en: "Accounts Payable", type: "liability", balance: 45000 },
  { id: "4100", name: "المبيعات", name_en: "Sales Revenue", type: "revenue", balance: 850000 },
  { id: "5100", name: "تكلفة المبيعات", name_en: "Cost of Sales", type: "expense", balance: 320000 },
]

const AccountingPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("overview")
  const [journalEntries, setJournalEntries] = useState(mockJournalEntries)
  const [invoices, setInvoices] = useState(mockInvoices)
  const [payments, setPayments] = useState(mockPayments)
  const [accounts, setAccounts] = useState(mockAccounts)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [dateFilter, setDateFilter] = useState("month")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isJournalDialogOpen, setIsJournalDialogOpen] = useState(false)
  const [isInvoiceDialogOpen, setIsInvoiceDialogOpen] = useState(false)
  const [isPaymentDialogOpen, setIsPaymentDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [selectedItem, setSelectedItem] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Forms
  const journalForm = useForm({
    resolver: zodResolver(journalSchema),
    defaultValues: {
      date: new Date().toISOString().split('T')[0],
      reference: "",
      description: "",
      entries: [],
      notes: "",
    },
  })

  const invoiceForm = useForm({
    resolver: zodResolver(invoiceSchema),
    defaultValues: {
      customer_id: "",
      customer_name: "",
      invoice_date: new Date().toISOString().split('T')[0],
      due_date: "",
      items: [],
      notes: "",
    },
  })

  // Statistics
  const stats = {
    totalRevenue: mockInvoices.reduce((sum, inv) => sum + inv.grand_total, 0),
    totalReceivables: mockInvoices.reduce((sum, inv) => sum + inv.balance, 0),
    cashBalance: mockAccounts.find(a => a.id === "1100")?.balance || 0,
    bankBalance: mockAccounts.find(a => a.id === "1200")?.balance || 0,
    pendingPayments: mockInvoices.filter(inv => inv.status !== "paid").length,
    overdueInvoices: mockInvoices.filter(inv => inv.status === "overdue").length,
  }

  // Filter invoices
  const filteredInvoices = invoices.filter(inv => {
    const matchesSearch = inv.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         inv.customer.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || inv.status === statusFilter
    return matchesSearch && matchesStatus
  })

  // Handlers
  const handleCreateJournal = async (data) => {
    setIsSubmitting(true)
    try {
      const newEntry = {
        id: `JE-${String(journalEntries.length + 1).padStart(3, '0')}`,
        ...data,
        total_debit: data.entries.reduce((sum, e) => sum + e.debit, 0),
        total_credit: data.entries.reduce((sum, e) => sum + e.credit, 0),
        status: "draft",
        created_by: "المستخدم الحالي",
      }
      setJournalEntries([...journalEntries, newEntry])
      toast.success("تم إنشاء القيد المحاسبي")
      setIsJournalDialogOpen(false)
      journalForm.reset()
    } catch (error) {
      toast.error("فشل إنشاء القيد")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCreateInvoice = async (data) => {
    setIsSubmitting(true)
    try {
      const total = data.items.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0)
      const tax = total * 0.15
      const newInvoice = {
        id: `INV-${String(invoices.length + 1).padStart(3, '0')}`,
        customer: data.customer_name,
        date: data.invoice_date,
        due_date: data.due_date,
        total,
        tax,
        grand_total: total + tax,
        paid: 0,
        balance: total + tax,
        status: "pending",
      }
      setInvoices([...invoices, newInvoice])
      toast.success("تم إنشاء الفاتورة")
      setIsInvoiceDialogOpen(false)
      invoiceForm.reset()
    } catch (error) {
      toast.error("فشل إنشاء الفاتورة")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleRecordPayment = async (invoiceId, amount) => {
    const invoice = invoices.find(inv => inv.id === invoiceId)
    if (!invoice) return
    
    const newPayment = {
      id: `PAY-${String(payments.length + 1).padStart(3, '0')}`,
      date: new Date().toISOString().split('T')[0],
      customer: invoice.customer,
      invoice: invoiceId,
      amount,
      method: "نقدي",
      status: "completed",
    }
    
    setPayments([...payments, newPayment])
    
    setInvoices(invoices.map(inv => {
      if (inv.id === invoiceId) {
        const newPaid = inv.paid + amount
        const newBalance = inv.grand_total - newPaid
        return {
          ...inv,
          paid: newPaid,
          balance: newBalance,
          status: newBalance <= 0 ? "paid" : "partial",
        }
      }
      return inv
    }))
    
    toast.success("تم تسجيل الدفعة")
  }

  const handlePostJournal = (entry) => {
    setJournalEntries(journalEntries.map(je => 
      je.id === entry.id ? { ...je, status: "posted" } : je
    ))
    toast.success("تم ترحيل القيد")
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      if (selectedItem?.id?.startsWith("INV")) {
        setInvoices(invoices.filter(inv => inv.id !== selectedItem.id))
      } else if (selectedItem?.id?.startsWith("JE")) {
        setJournalEntries(journalEntries.filter(je => je.id !== selectedItem.id))
      }
      toast.success("تم الحذف بنجاح")
      setIsDeleteDialogOpen(false)
      setSelectedItem(null)
    } catch (error) {
      toast.error("فشل الحذف")
    } finally {
      setIsSubmitting(false)
    }
  }

  // Journal entries columns
  const journalColumns = [
    {
      accessorKey: "id",
      header: "رقم القيد",
      cell: ({ row }) => <span className="font-mono text-primary">{row.original.id}</span>,
    },
    {
      accessorKey: "date",
      header: "التاريخ",
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <Calendar className="w-4 h-4 text-muted-foreground" />
          {row.original.date}
        </div>
      ),
    },
    { accessorKey: "description", header: "البيان" },
    { accessorKey: "reference", header: "المرجع" },
    {
      accessorKey: "total_debit",
      header: "المدين",
      cell: ({ row }) => <span className="font-bold">{(row.original.total_debit || 0).toLocaleString()} ر.س</span>,
    },
    {
      accessorKey: "total_credit",
      header: "الدائن",
      cell: ({ row }) => <span className="font-bold">{(row.original.total_credit || 0).toLocaleString()} ر.س</span>,
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status] || statusConfig.draft
        return <Badge variant={config.variant}>{config.label}</Badge>
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const entry = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => { setSelectedItem(entry); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض
              </DropdownMenuItem>
              {entry.status === "draft" && (
                <>
                  <DropdownMenuItem onClick={() => handlePostJournal(entry)}>
                    <CheckCircle2 className="w-4 h-4 ml-2" />ترحيل
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => { setSelectedItem(entry); setIsDeleteDialogOpen(true); }} className="text-red-600">
                    <Trash2 className="w-4 h-4 ml-2" />حذف
                  </DropdownMenuItem>
                </>
              )}
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  // Invoice columns
  const invoiceColumns = [
    {
      accessorKey: "id",
      header: "رقم الفاتورة",
      cell: ({ row }) => <span className="font-mono text-primary">{row.original.id}</span>,
    },
    {
      accessorKey: "customer",
      header: "العميل",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
            <Building2 className="w-4 h-4 text-blue-500" />
          </div>
          {row.original.customer}
        </div>
      ),
    },
    { accessorKey: "date", header: "التاريخ" },
    { accessorKey: "due_date", header: "تاريخ الاستحقاق" },
    {
      accessorKey: "grand_total",
      header: "الإجمالي",
      cell: ({ row }) => <span className="font-bold">{(row.original.grand_total || 0).toLocaleString()} ر.س</span>,
    },
    {
      accessorKey: "balance",
      header: "المتبقي",
      cell: ({ row }) => (
        <span className={`font-bold ${row.original.balance > 0 ? "text-red-600" : "text-green-600"}`}>
          {(row.original.balance || 0).toLocaleString()} ر.س
        </span>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status] || statusConfig.pending
        return <Badge variant={config.variant}>{config.label}</Badge>
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const invoice = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => { setSelectedItem(invoice); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />عرض
              </DropdownMenuItem>
              {invoice.status !== "paid" && (
                <DropdownMenuItem onClick={() => handleRecordPayment(invoice.id, invoice.balance)}>
                  <Wallet className="w-4 h-4 ml-2" />تسجيل دفعة
                </DropdownMenuItem>
              )}
              <DropdownMenuItem onClick={() => toast.info("جاري طباعة الفاتورة...")}>
                <FileText className="w-4 h-4 ml-2" />طباعة
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedItem(invoice); setIsDeleteDialogOpen(true); }} className="text-red-600">
                <Trash2 className="w-4 h-4 ml-2" />حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        )
      },
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Calculator className="w-7 h-7 text-blue-500" />
            إدارة المحاسبة
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة الحسابات والقيود والفواتير</p>
        </div>
        <div className="flex gap-2">
          <Select value={dateFilter} onValueChange={setDateFilter}>
            <SelectTrigger className="w-[140px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="today">اليوم</SelectItem>
              <SelectItem value="week">هذا الأسبوع</SelectItem>
              <SelectItem value="month">هذا الشهر</SelectItem>
              <SelectItem value="year">هذه السنة</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" onClick={() => toast.info("جاري التصدير...")}>
            <Download className="w-4 h-4 ml-2" />تصدير
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{(stats.totalRevenue / 1000).toFixed(0)}K</p>
              <p className="text-xs text-muted-foreground">إجمالي الإيرادات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <ArrowDownRight className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{(stats.totalReceivables / 1000).toFixed(0)}K</p>
              <p className="text-xs text-muted-foreground">المستحقات</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <CircleDollarSign className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{(stats.cashBalance / 1000).toFixed(0)}K</p>
              <p className="text-xs text-muted-foreground">النقدية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Building2 className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{(stats.bankBalance / 1000).toFixed(0)}K</p>
              <p className="text-xs text-muted-foreground">البنك</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Clock className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.pendingPayments}</p>
              <p className="text-xs text-muted-foreground">فواتير معلقة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900 flex items-center justify-center">
              <XCircle className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <p className="text-xl font-bold">{stats.overdueInvoices}</p>
              <p className="text-xs text-muted-foreground">فواتير متأخرة</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview" className="flex items-center gap-2">
            <PieChart className="w-4 h-4" />نظرة عامة
          </TabsTrigger>
          <TabsTrigger value="journal" className="flex items-center gap-2">
            <BookOpen className="w-4 h-4" />القيود اليومية
          </TabsTrigger>
          <TabsTrigger value="invoices" className="flex items-center gap-2">
            <Receipt className="w-4 h-4" />الفواتير
          </TabsTrigger>
          <TabsTrigger value="payments" className="flex items-center gap-2">
            <CreditCard className="w-4 h-4" />المدفوعات
          </TabsTrigger>
          <TabsTrigger value="accounts" className="flex items-center gap-2">
            <BookOpen className="w-4 h-4" />دليل الحسابات
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle>آخر القيود المحاسبية</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {journalEntries.slice(0, 5).map((entry) => (
                    <div key={entry.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div>
                        <p className="font-medium">{entry.description}</p>
                        <p className="text-sm text-muted-foreground">{entry.date}</p>
                      </div>
                      <div className="text-left">
                        <p className="font-bold">{entry.total_debit.toLocaleString()} ر.س</p>
                        <Badge variant={statusConfig[entry.status]?.variant}>{statusConfig[entry.status]?.label}</Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle>أرصدة الحسابات</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {accounts.slice(0, 6).map((account) => (
                    <div key={account.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div>
                        <p className="font-medium">{account.name}</p>
                        <p className="text-sm text-muted-foreground font-mono">{account.id}</p>
                      </div>
                      <p className={`font-bold ${account.type === "asset" ? "text-green-600" : account.type === "liability" ? "text-red-600" : ""}`}>
                        {account.balance.toLocaleString()} ر.س
                      </p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Journal Tab */}
        <TabsContent value="journal" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4 justify-between">
                <div className="flex-1 relative max-w-md">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Button onClick={() => { setDialogMode("add"); setIsJournalDialogOpen(true); }}>
                  <Plus className="w-4 h-4 ml-2" />قيد جديد
                </Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>القيود اليومية ({journalEntries.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={journalColumns} data={journalEntries} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Invoices Tab */}
        <TabsContent value="invoices" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4 justify-between">
                <div className="flex-1 relative max-w-md">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[150px]"><SelectValue placeholder="الحالة" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع الحالات</SelectItem>
                    <SelectItem value="pending">معلق</SelectItem>
                    <SelectItem value="paid">مدفوع</SelectItem>
                    <SelectItem value="partial">مدفوع جزئياً</SelectItem>
                    <SelectItem value="overdue">متأخر</SelectItem>
                  </SelectContent>
                </Select>
                <Button onClick={() => { setDialogMode("add"); setIsInvoiceDialogOpen(true); }}>
                  <Plus className="w-4 h-4 ml-2" />فاتورة جديدة
                </Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>الفواتير ({filteredInvoices.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <DataTable columns={invoiceColumns} data={filteredInvoices} isLoading={isLoading} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Payments Tab */}
        <TabsContent value="payments" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>المدفوعات ({payments.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {payments.map((payment) => (
                  <div key={payment.id} className="flex items-center justify-between p-4 rounded-lg border">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
                        <Wallet className="w-5 h-5 text-green-600" />
                      </div>
                      <div>
                        <p className="font-medium">{payment.customer}</p>
                        <p className="text-sm text-muted-foreground">الفاتورة: {payment.invoice} • {payment.date}</p>
                      </div>
                    </div>
                    <div className="text-left">
                      <p className="font-bold text-green-600">{payment.amount.toLocaleString()} ر.س</p>
                      <Badge variant="outline">{payment.method}</Badge>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Accounts Tab */}
        <TabsContent value="accounts" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>دليل الحسابات</CardTitle>
              <Button onClick={() => toast.info("جاري إضافة حساب...")}>
                <Plus className="w-4 h-4 ml-2" />حساب جديد
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {accounts.map((account) => (
                  <div key={account.id} className="flex items-center justify-between p-4 rounded-lg border hover:bg-muted/50 cursor-pointer">
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                        account.type === "asset" ? "bg-green-100" : 
                        account.type === "liability" ? "bg-red-100" : 
                        account.type === "revenue" ? "bg-blue-100" : "bg-orange-100"
                      }`}>
                        <BookOpen className={`w-5 h-5 ${
                          account.type === "asset" ? "text-green-600" : 
                          account.type === "liability" ? "text-red-600" : 
                          account.type === "revenue" ? "text-blue-600" : "text-orange-600"
                        }`} />
                      </div>
                      <div>
                        <p className="font-medium">{account.name}</p>
                        <p className="text-sm text-muted-foreground font-mono">{account.id} • {account.name_en}</p>
                      </div>
                    </div>
                    <p className={`font-bold ${
                      account.type === "asset" ? "text-green-600" : 
                      account.type === "liability" ? "text-red-600" : ""
                    }`}>
                      {account.balance.toLocaleString()} ر.س
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Journal Dialog */}
      <FormDialog
        open={isJournalDialogOpen}
        onOpenChange={setIsJournalDialogOpen}
        title="قيد محاسبي جديد"
        description="إنشاء قيد محاسبي جديد"
        onSubmit={journalForm.handleSubmit(handleCreateJournal)}
        isSubmitting={isSubmitting}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>التاريخ</Label>
              <Input type="date" {...journalForm.register("date")} />
            </div>
            <div>
              <Label>المرجع</Label>
              <Input {...journalForm.register("reference")} placeholder="INV-001" />
            </div>
          </div>
          <div>
            <Label>البيان</Label>
            <Input {...journalForm.register("description")} placeholder="وصف القيد..." />
          </div>
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...journalForm.register("notes")} placeholder="ملاحظات إضافية..." />
          </div>
        </div>
      </FormDialog>

      {/* Invoice Dialog */}
      <FormDialog
        open={isInvoiceDialogOpen}
        onOpenChange={setIsInvoiceDialogOpen}
        title="فاتورة جديدة"
        description="إنشاء فاتورة مبيعات جديدة"
        onSubmit={invoiceForm.handleSubmit(handleCreateInvoice)}
        isSubmitting={isSubmitting}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>العميل</Label>
              <Input {...invoiceForm.register("customer_name")} placeholder="اسم العميل" />
            </div>
            <div>
              <Label>تاريخ الفاتورة</Label>
              <Input type="date" {...invoiceForm.register("invoice_date")} />
            </div>
          </div>
          <div>
            <Label>تاريخ الاستحقاق</Label>
            <Input type="date" {...invoiceForm.register("due_date")} />
          </div>
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...invoiceForm.register("notes")} placeholder="ملاحظات..." />
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedItem(null); }}
        title={selectedItem?.id}
        subtitle={selectedItem?.description || selectedItem?.customer}
        badge={selectedItem && {
          text: statusConfig[selectedItem.status]?.label,
          variant: statusConfig[selectedItem.status]?.variant,
        }}
        size="lg"
      >
        {selectedItem && (
          <div className="space-y-4">
            {selectedItem.id?.startsWith("INV") ? (
              <>
                <ViewDialog.Section title="معلومات الفاتورة">
                  <ViewDialog.Row label="العميل" value={selectedItem.customer} />
                  <ViewDialog.Row label="التاريخ" value={selectedItem.date} />
                  <ViewDialog.Row label="تاريخ الاستحقاق" value={selectedItem.due_date} />
                </ViewDialog.Section>
                <ViewDialog.Section title="المبالغ">
                  <ViewDialog.Row label="المجموع" value={`${selectedItem.total?.toLocaleString()} ر.س`} />
                  <ViewDialog.Row label="الضريبة" value={`${selectedItem.tax?.toLocaleString()} ر.س`} />
                  <ViewDialog.Row label="الإجمالي" value={`${selectedItem.grand_total?.toLocaleString()} ر.س`} valueClassName="font-bold" />
                  <ViewDialog.Row label="المدفوع" value={`${selectedItem.paid?.toLocaleString()} ر.س`} valueClassName="text-green-600" />
                  <ViewDialog.Row label="المتبقي" value={`${selectedItem.balance?.toLocaleString()} ر.س`} valueClassName="text-red-600" />
                </ViewDialog.Section>
              </>
            ) : (
              <>
                <ViewDialog.Section title="معلومات القيد">
                  <ViewDialog.Row label="التاريخ" value={selectedItem.date} />
                  <ViewDialog.Row label="المرجع" value={selectedItem.reference || "—"} />
                  <ViewDialog.Row label="البيان" value={selectedItem.description} />
                </ViewDialog.Section>
                <ViewDialog.Section title="المبالغ">
                  <ViewDialog.Row label="المدين" value={`${selectedItem.total_debit?.toLocaleString()} ر.س`} />
                  <ViewDialog.Row label="الدائن" value={`${selectedItem.total_credit?.toLocaleString()} ر.س`} />
                </ViewDialog.Section>
              </>
            )}
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف"
        description={`هل أنت متأكد من حذف "${selectedItem?.id}"؟`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default AccountingPage
