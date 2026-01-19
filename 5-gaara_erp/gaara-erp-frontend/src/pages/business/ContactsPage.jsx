/**
 * Contacts Management Page - إدارة جهات الاتصال
 * Gaara ERP v12
 *
 * Complete customer and supplier contact management with CRUD operations.
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
  Users,
  Building2,
  UserPlus,
  Search,
  Filter,
  Download,
  Upload,
  Eye,
  Edit,
  Trash2,
  Phone,
  Mail,
  MapPin,
  Star,
  MoreVertical,
  Tag,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Globe,
  CreditCard,
  History,
  MessageSquare,
  Calendar,
  FileText,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
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
import { Checkbox } from "@/components/ui/checkbox"
import { DataTable } from "@/components/common"
import { ConfirmDialog, FormDialog, ViewDialog } from "@/components/dialogs"
import customersService from "@/services/customersService"

// Form schema
const contactSchema = z.object({
  name: z.string().min(2, "الاسم يجب أن يكون على الأقل حرفين"),
  name_ar: z.string().optional(),
  type: z.enum(["customer", "supplier", "both"]),
  category: z.enum(["individual", "company"]),
  email: z.string().email("البريد الإلكتروني غير صحيح").optional().or(z.literal("")),
  phone: z.string().min(10, "رقم الهاتف غير صحيح"),
  mobile: z.string().optional(),
  address: z.string().optional(),
  city: z.string().optional(),
  country: z.string().default("السعودية"),
  postal_code: z.string().optional(),
  tax_number: z.string().optional(),
  website: z.string().optional(),
  credit_limit: z.number().min(0).default(0),
  payment_terms: z.string().default("net30"),
  notes: z.string().optional(),
  is_active: z.boolean().default(true),
})

// Mock data
const mockContacts = [
  {
    id: "C001",
    name: "شركة الزراعة الحديثة",
    type: "customer",
    category: "company",
    email: "info@modernagri.com",
    phone: "+966-50-123-4567",
    city: "الرياض",
    status: "active",
    rating: 5,
    total_orders: 25,
    total_amount: 450000,
    balance: 15000,
    last_order: "2026-01-15",
    created_at: "2024-01-01",
  },
  {
    id: "C002",
    name: "أحمد محمد العلي",
    type: "customer",
    category: "individual",
    email: "ahmed@example.com",
    phone: "+966-55-987-6543",
    city: "جدة",
    status: "active",
    rating: 4,
    total_orders: 8,
    total_amount: 75000,
    balance: 0,
    last_order: "2026-01-10",
    created_at: "2024-03-15",
  },
  {
    id: "S001",
    name: "مؤسسة البذور الذهبية",
    type: "supplier",
    category: "company",
    email: "contact@goldenseeds.sa",
    phone: "+966-12-345-6789",
    city: "الدمام",
    status: "active",
    rating: 5,
    total_orders: 42,
    total_amount: 890000,
    balance: -25000,
    last_order: "2026-01-17",
    created_at: "2023-06-01",
  },
  {
    id: "S002",
    name: "شركة المعدات الزراعية المتحدة",
    type: "supplier",
    category: "company",
    email: "sales@uniagri.com",
    phone: "+966-13-456-7890",
    city: "الخبر",
    status: "inactive",
    rating: 3,
    total_orders: 5,
    total_amount: 120000,
    balance: -5000,
    last_order: "2025-12-01",
    created_at: "2024-02-20",
  },
  {
    id: "C003",
    name: "مزرعة النخيل الذهبي",
    type: "both",
    category: "company",
    email: "info@goldpalm.sa",
    phone: "+966-50-111-2222",
    city: "القصيم",
    status: "active",
    rating: 4,
    total_orders: 15,
    total_amount: 280000,
    balance: 8000,
    last_order: "2026-01-12",
    created_at: "2023-09-10",
  },
]

const mockTags = [
  { id: 1, name: "عملاء VIP", color: "bg-amber-500", count: 15 },
  { id: 2, name: "موردون رئيسيون", color: "bg-blue-500", count: 8 },
  { id: 3, name: "عملاء جدد", color: "bg-emerald-500", count: 25 },
  { id: 4, name: "عملاء متأخرون", color: "bg-red-500", count: 5 },
  { id: 5, name: "عملاء زراعيون", color: "bg-green-500", count: 30 },
]

const ContactsPage = () => {
  // State
  const [activeTab, setActiveTab] = useState("all")
  const [contacts, setContacts] = useState(mockContacts)
  const [tags, setTags] = useState(mockTags)
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [typeFilter, setTypeFilter] = useState("all")
  const [statusFilter, setStatusFilter] = useState("all")

  // Dialog states
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isTagDialogOpen, setIsTagDialogOpen] = useState(false)
  const [selectedContact, setSelectedContact] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Form
  const form = useForm({
    resolver: zodResolver(contactSchema),
    defaultValues: {
      name: "",
      name_ar: "",
      type: "customer",
      category: "individual",
      email: "",
      phone: "",
      mobile: "",
      address: "",
      city: "",
      country: "السعودية",
      postal_code: "",
      tax_number: "",
      website: "",
      credit_limit: 0,
      payment_terms: "net30",
      notes: "",
      is_active: true,
    },
  })

  // Load data
  const loadData = useCallback(async () => {
    setIsLoading(true)
    try {
      const response = await customersService.getCustomers({
        type: typeFilter !== "all" ? typeFilter : undefined,
        status: statusFilter !== "all" ? statusFilter : undefined,
        search: searchQuery || undefined,
      })
      
      if (response.success && response.data) {
        setContacts(Array.isArray(response.data) ? response.data : mockContacts)
      }
    } catch (error) {
      console.error("Error loading contacts:", error)
    } finally {
      setIsLoading(false)
    }
  }, [typeFilter, statusFilter, searchQuery])

  useEffect(() => {
    loadData()
  }, [loadData])

  // Filter contacts based on active tab
  const filteredContacts = contacts.filter(c => {
    const matchesSearch = 
      c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.email?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.phone?.includes(searchQuery)
    
    const matchesType = typeFilter === "all" || c.type === typeFilter || 
      (typeFilter === "customer" && c.type === "both") ||
      (typeFilter === "supplier" && c.type === "both")
    
    const matchesStatus = statusFilter === "all" || c.status === statusFilter
    
    const matchesTab = 
      activeTab === "all" ||
      (activeTab === "customers" && (c.type === "customer" || c.type === "both")) ||
      (activeTab === "suppliers" && (c.type === "supplier" || c.type === "both"))
    
    return matchesSearch && matchesType && matchesStatus && matchesTab
  })

  // Statistics
  const stats = {
    total: contacts.length,
    customers: contacts.filter(c => c.type === "customer" || c.type === "both").length,
    suppliers: contacts.filter(c => c.type === "supplier" || c.type === "both").length,
    newThisMonth: contacts.filter(c => {
      const date = new Date(c.created_at)
      const now = new Date()
      return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear()
    }).length,
  }

  // Helpers
  const getInitials = (name) => {
    return name.split(" ").map((word) => word[0]).join("").slice(0, 2)
  }

  const renderStars = (rating) => (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={`w-4 h-4 ${star <= rating ? "text-amber-400 fill-amber-400" : "text-slate-300"}`}
        />
      ))}
    </div>
  )

  // Handlers
  const handleCreate = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await customersService.createCustomer(data)
      if (response.success) {
        toast.success("تم إضافة جهة الاتصال بنجاح")
        setIsCreateDialogOpen(false)
        form.reset()
        loadData()
      } else {
        throw new Error(response.message)
      }
    } catch (error) {
      toast.error(error.message || "فشل إضافة جهة الاتصال")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEdit = async (data) => {
    setIsSubmitting(true)
    try {
      const response = await customersService.updateCustomer(selectedContact.id, data)
      if (response.success) {
        toast.success("تم تحديث جهة الاتصال")
        setIsEditDialogOpen(false)
        setSelectedContact(null)
        form.reset()
        loadData()
      }
    } catch (error) {
      toast.error("فشل تحديث جهة الاتصال")
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async () => {
    setIsSubmitting(true)
    try {
      const response = await customersService.deleteCustomer(selectedContact.id)
      if (response.success) {
        toast.success("تم حذف جهة الاتصال")
        setIsDeleteDialogOpen(false)
        setSelectedContact(null)
        loadData()
      }
    } catch (error) {
      toast.error("فشل حذف جهة الاتصال")
    } finally {
      setIsSubmitting(false)
    }
  }

  const openEditDialog = (contact) => {
    setSelectedContact(contact)
    form.reset({
      name: contact.name,
      type: contact.type,
      category: contact.category,
      email: contact.email || "",
      phone: contact.phone || "",
      city: contact.city || "",
      is_active: contact.status === "active",
    })
    setIsEditDialogOpen(true)
  }

  const handleExport = async () => {
    try {
      const response = await customersService.exportCustomers('xlsx')
      if (response.success) {
        toast.success("تم تصدير البيانات")
      }
    } catch (error) {
      toast.error("فشل تصدير البيانات")
    }
  }

  // Table columns
  const columns = [
    {
      accessorKey: "contact",
      header: "جهة الاتصال",
      cell: ({ row }) => {
        const contact = row.original
        return (
          <div className="flex items-center gap-3">
            <Avatar className="w-10 h-10">
              <AvatarFallback className={contact.type === "supplier" ? "bg-amber-100 text-amber-700" : "bg-emerald-100 text-emerald-700"}>
                {getInitials(contact.name)}
              </AvatarFallback>
            </Avatar>
            <div>
              <p className="font-medium">{contact.name}</p>
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Mail className="w-3 h-3" />
                {contact.email || "—"}
              </div>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "type",
      header: "النوع",
      cell: ({ row }) => {
        const type = row.original.type
        const config = {
          customer: { label: "عميل", variant: "default", className: "bg-emerald-100 text-emerald-700" },
          supplier: { label: "مورد", variant: "default", className: "bg-amber-100 text-amber-700" },
          both: { label: "عميل/مورد", variant: "default", className: "bg-blue-100 text-blue-700" },
        }
        return <Badge className={config[type].className}>{config[type].label}</Badge>
      },
    },
    {
      accessorKey: "category",
      header: "التصنيف",
      cell: ({ row }) => (
        <Badge variant="outline">
          {row.original.category === "company" ? "شركة" : "فرد"}
        </Badge>
      ),
    },
    {
      accessorKey: "city",
      header: "المدينة",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <MapPin className="w-3 h-3" />
          {row.original.city || "—"}
        </div>
      ),
    },
    {
      accessorKey: "rating",
      header: "التقييم",
      cell: ({ row }) => renderStars(row.original.rating),
    },
    {
      accessorKey: "total_orders",
      header: "الطلبات",
      cell: ({ row }) => (
        <span className="font-medium">{row.original.total_orders}</span>
      ),
    },
    {
      accessorKey: "total_amount",
      header: "إجمالي التعاملات",
      cell: ({ row }) => (
        <span className="font-bold text-green-600">
          {(row.original.total_amount || 0).toLocaleString()} ر.س
        </span>
      ),
    },
    {
      accessorKey: "balance",
      header: "الرصيد",
      cell: ({ row }) => {
        const balance = row.original.balance || 0
        return (
          <span className={`font-medium ${balance > 0 ? "text-green-600" : balance < 0 ? "text-red-600" : ""}`}>
            {balance.toLocaleString()} ر.س
          </span>
        )
      },
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => (
        <Badge variant={row.original.status === "active" ? "default" : "secondary"}>
          {row.original.status === "active" ? (
            <><CheckCircle2 className="w-3 h-3 ml-1" />نشط</>
          ) : (
            <><XCircle className="w-3 h-3 ml-1" />غير نشط</>
          )}
        </Badge>
      ),
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const contact = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              
              <DropdownMenuItem onClick={() => { setSelectedContact(contact); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />
                عرض التفاصيل
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => openEditDialog(contact)}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              <DropdownMenuItem onClick={() => window.location.href = `tel:${contact.phone}`}>
                <Phone className="w-4 h-4 ml-2" />
                اتصال
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => window.location.href = `mailto:${contact.email}`}>
                <Mail className="w-4 h-4 ml-2" />
                إرسال بريد
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => toast.info("جاري تحميل كشف الحساب...")}>
                <FileText className="w-4 h-4 ml-2" />
                كشف حساب
              </DropdownMenuItem>
              
              <DropdownMenuItem onClick={() => toast.info("جاري تحميل السجل...")}>
                <History className="w-4 h-4 ml-2" />
                سجل التعاملات
              </DropdownMenuItem>
              
              <DropdownMenuSeparator />
              
              <DropdownMenuItem
                onClick={() => { setSelectedContact(contact); setIsDeleteDialogOpen(true); }}
                className="text-red-600"
              >
                <Trash2 className="w-4 h-4 ml-2" />
                حذف
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
            <Users className="w-7 h-7 text-emerald-500" />
            جهات الاتصال
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة العملاء والموردين</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => toast.info("جاري الاستيراد...")}>
            <Upload className="w-4 h-4 ml-2" />
            استيراد
          </Button>
          <Button variant="outline" onClick={handleExport}>
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <UserPlus className="w-4 h-4 ml-2" />
            إضافة جهة اتصال
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
              <Users className="w-6 h-6 text-emerald-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">إجمالي جهات الاتصال</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Star className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.customers}</p>
              <p className="text-sm text-muted-foreground">العملاء</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-amber-100 dark:bg-amber-900 flex items-center justify-center">
              <Building2 className="w-6 h-6 text-amber-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.suppliers}</p>
              <p className="text-sm text-muted-foreground">الموردون</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <UserPlus className="w-6 h-6 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.newThisMonth}</p>
              <p className="text-sm text-muted-foreground">جديد هذا الشهر</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="all" className="flex items-center gap-2">
            <Users className="w-4 h-4" />
            الكل
          </TabsTrigger>
          <TabsTrigger value="customers" className="flex items-center gap-2">
            <Star className="w-4 h-4" />
            العملاء
          </TabsTrigger>
          <TabsTrigger value="suppliers" className="flex items-center gap-2">
            <Building2 className="w-4 h-4" />
            الموردون
          </TabsTrigger>
          <TabsTrigger value="tags" className="flex items-center gap-2">
            <Tag className="w-4 h-4" />
            التصنيفات
          </TabsTrigger>
        </TabsList>

        {/* All/Customers/Suppliers Tab */}
        <TabsContent value={activeTab !== "tags" ? activeTab : "all"} className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="بحث بالاسم أو البريد..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pr-10"
                  />
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[150px]">
                    <SelectValue placeholder="الحالة" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع الحالات</SelectItem>
                    <SelectItem value="active">نشط</SelectItem>
                    <SelectItem value="inactive">غير نشط</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline" onClick={loadData}>
                  <RefreshCw className="w-4 h-4 ml-2" />
                  تحديث
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>جهات الاتصال ({filteredContacts.length})</CardTitle>
              <CardDescription>قائمة جميع جهات الاتصال في النظام</CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable
                columns={columns}
                data={filteredContacts}
                isLoading={isLoading}
                searchKey="name"
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tags Tab */}
        <TabsContent value="tags" className="space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>التصنيفات</CardTitle>
                <CardDescription>تنظيم جهات الاتصال بالتصنيفات</CardDescription>
              </div>
              <Button onClick={() => setIsTagDialogOpen(true)}>
                <Tag className="w-4 h-4 ml-2" />
                تصنيف جديد
              </Button>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {tags.map((tag) => (
                  <Card key={tag.id} className="cursor-pointer hover:border-emerald-300 transition-colors">
                    <CardContent className="p-4">
                      <div className="flex items-center gap-3">
                        <div className={`w-4 h-4 rounded-full ${tag.color}`} />
                        <div className="flex-1">
                          <p className="font-medium">{tag.name}</p>
                          <p className="text-sm text-muted-foreground">{tag.count} جهة اتصال</p>
                        </div>
                        <Button variant="ghost" size="sm">
                          <MoreVertical className="w-4 h-4" />
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Create/Edit Dialog */}
      <FormDialog
        open={isCreateDialogOpen || isEditDialogOpen}
        onOpenChange={(open) => {
          if (!open) {
            setIsCreateDialogOpen(false)
            setIsEditDialogOpen(false)
            setSelectedContact(null)
            form.reset()
          }
        }}
        title={isEditDialogOpen ? "تعديل جهة الاتصال" : "إضافة جهة اتصال جديدة"}
        description={isEditDialogOpen ? "تعديل بيانات جهة الاتصال" : "إضافة جهة اتصال جديدة للنظام"}
        onSubmit={form.handleSubmit(isEditDialogOpen ? handleEdit : handleCreate)}
        isSubmitting={isSubmitting}
        submitText={isEditDialogOpen ? "حفظ" : "إضافة"}
        size="lg"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>الاسم</Label>
              <Input {...form.register("name")} placeholder="الاسم الكامل" />
              {form.formState.errors.name && (
                <p className="text-sm text-red-500 mt-1">{form.formState.errors.name.message}</p>
              )}
            </div>
            <div>
              <Label>النوع</Label>
              <Select
                value={form.watch("type")}
                onValueChange={(v) => form.setValue("type", v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="customer">عميل</SelectItem>
                  <SelectItem value="supplier">مورد</SelectItem>
                  <SelectItem value="both">عميل ومورد</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>التصنيف</Label>
              <Select
                value={form.watch("category")}
                onValueChange={(v) => form.setValue("category", v)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="individual">فرد</SelectItem>
                  <SelectItem value="company">شركة</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>رقم الهاتف</Label>
              <Input {...form.register("phone")} placeholder="0501234567" />
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>البريد الإلكتروني</Label>
              <Input {...form.register("email")} type="email" placeholder="email@example.com" />
            </div>
            <div>
              <Label>المدينة</Label>
              <Input {...form.register("city")} placeholder="الرياض" />
            </div>
          </div>
          
          <div>
            <Label>العنوان</Label>
            <Textarea {...form.register("address")} placeholder="العنوان الكامل..." />
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>الرقم الضريبي</Label>
              <Input {...form.register("tax_number")} placeholder="300000000000003" />
            </div>
            <div>
              <Label>حد الائتمان</Label>
              <Input 
                type="number" 
                {...form.register("credit_limit", { valueAsNumber: true })} 
                placeholder="0" 
              />
            </div>
          </div>
          
          <div>
            <Label>شروط الدفع</Label>
            <Select
              value={form.watch("payment_terms")}
              onValueChange={(v) => form.setValue("payment_terms", v)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="cash">نقدي</SelectItem>
                <SelectItem value="net15">صافي 15 يوم</SelectItem>
                <SelectItem value="net30">صافي 30 يوم</SelectItem>
                <SelectItem value="net60">صافي 60 يوم</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div>
            <Label>ملاحظات</Label>
            <Textarea {...form.register("notes")} placeholder="ملاحظات إضافية..." />
          </div>
          
          <div className="flex items-center space-x-2 space-x-reverse">
            <Checkbox
              id="is_active"
              checked={form.watch("is_active")}
              onCheckedChange={(checked) => form.setValue("is_active", checked)}
            />
            <Label htmlFor="is_active">جهة اتصال نشطة</Label>
          </div>
        </div>
      </FormDialog>

      {/* View Dialog */}
      <ViewDialog
        open={isViewDialogOpen}
        onOpenChange={(open) => { setIsViewDialogOpen(open); if (!open) setSelectedContact(null); }}
        title={selectedContact?.name}
        subtitle={`${selectedContact?.type === "customer" ? "عميل" : selectedContact?.type === "supplier" ? "مورد" : "عميل/مورد"} - ${selectedContact?.city}`}
        badge={selectedContact && {
          text: selectedContact.status === "active" ? "نشط" : "غير نشط",
          variant: selectedContact.status === "active" ? "default" : "secondary",
        }}
        size="lg"
        actions={
          selectedContact && (
            <div className="flex gap-2">
              <Button size="sm" variant="outline" onClick={() => window.location.href = `tel:${selectedContact.phone}`}>
                <Phone className="w-4 h-4" />
              </Button>
              <Button size="sm" variant="outline" onClick={() => window.location.href = `mailto:${selectedContact.email}`}>
                <Mail className="w-4 h-4" />
              </Button>
            </div>
          )
        }
      >
        {selectedContact && (
          <div className="space-y-4">
            <ViewDialog.Section title="معلومات الاتصال">
              <ViewDialog.Row label="البريد الإلكتروني" value={selectedContact.email || "—"} />
              <ViewDialog.Row label="الهاتف" value={selectedContact.phone} />
              <ViewDialog.Row label="المدينة" value={selectedContact.city || "—"} />
            </ViewDialog.Section>
            
            <ViewDialog.Section title="معلومات التعاملات">
              <ViewDialog.Row label="إجمالي الطلبات" value={`${selectedContact.total_orders} طلب`} />
              <ViewDialog.Row label="إجمالي التعاملات" value={`${(selectedContact.total_amount || 0).toLocaleString()} ر.س`} valueClassName="text-green-600 font-bold" />
              <ViewDialog.Row 
                label="الرصيد الحالي" 
                value={`${(selectedContact.balance || 0).toLocaleString()} ر.س`} 
                valueClassName={selectedContact.balance > 0 ? "text-green-600" : selectedContact.balance < 0 ? "text-red-600" : ""}
              />
              <ViewDialog.Row label="آخر طلب" value={selectedContact.last_order || "—"} />
            </ViewDialog.Section>
            
            <ViewDialog.Section title="التقييم">
              {renderStars(selectedContact.rating)}
            </ViewDialog.Section>
          </div>
        )}
      </ViewDialog>

      {/* Delete Confirmation */}
      <ConfirmDialog
        open={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        title="حذف جهة الاتصال"
        description={`هل أنت متأكد من حذف "${selectedContact?.name}"؟ سيتم حذف جميع البيانات المرتبطة.`}
        variant="danger"
        onConfirm={handleDelete}
        isLoading={isSubmitting}
      />
    </div>
  )
}

export default ContactsPage
