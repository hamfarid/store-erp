/**
 * Companies Management Page - إدارة الشركات والفروع
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Building2,
  Building,
  Plus,
  Search,
  Filter,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  MapPin,
  Phone,
  Mail,
  Globe,
  Users,
  RefreshCw,
  Download,
  ChevronRight,
  CheckCircle2,
  XCircle,
  Settings,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"

import { DataTable } from "@/components/common"
import { formatDate } from "@/lib/utils"
import { api } from "@/services/api"

// Form schemas
const companySchema = z.object({
  name: z.string().min(2, "اسم الشركة يجب أن يكون على الأقل حرفين"),
  name_ar: z.string().min(2, "الاسم بالعربية يجب أن يكون على الأقل حرفين"),
  code: z.string().min(2, "الكود يجب أن يكون على الأقل حرفين"),
  legal_name: z.string().optional(),
  tax_id: z.string().optional(),
  email: z.string().email("البريد الإلكتروني غير صحيح").optional().or(z.literal("")),
  phone: z.string().optional(),
  website: z.string().optional(),
  address: z.string().optional(),
  city: z.string().optional(),
  country: z.string().optional(),
  status: z.enum(["active", "inactive", "suspended"]),
})

const branchSchema = z.object({
  name: z.string().min(2, "اسم الفرع يجب أن يكون على الأقل حرفين"),
  name_ar: z.string().min(2, "الاسم بالعربية يجب أن يكون على الأقل حرفين"),
  code: z.string().min(2, "الكود يجب أن يكون على الأقل حرفين"),
  company: z.string().min(1, "يجب اختيار الشركة"),
  branch_type: z.enum(["main", "branch", "warehouse", "showroom"]),
  email: z.string().email("البريد الإلكتروني غير صحيح").optional().or(z.literal("")),
  phone: z.string().optional(),
  address: z.string().optional(),
  city: z.string().optional(),
  status: z.enum(["active", "inactive"]),
  is_default: z.boolean().default(false),
})

// Mock data
const mockCompanies = [
  {
    id: 1,
    name: "Gaara Agriculture",
    name_ar: "شركة غارا الزراعية",
    code: "GAARA001",
    legal_name: "Gaara Agriculture Holdings Ltd",
    tax_id: "123456789",
    email: "info@gaara-agri.com",
    phone: "+966-11-1234567",
    website: "https://gaara-agri.com",
    address: "شارع الملك فهد، حي العليا",
    city: "الرياض",
    country: "SA",
    status: "active",
    branches_count: 5,
    employees_count: 150,
    created_at: "2024-01-15T10:00:00Z",
  },
  {
    id: 2,
    name: "Green Valley Farms",
    name_ar: "مزارع الوادي الأخضر",
    code: "GVF002",
    legal_name: "Green Valley Farms Co.",
    tax_id: "987654321",
    email: "contact@greenvalley.com",
    phone: "+966-12-7654321",
    website: "https://greenvalley.com",
    address: "طريق المدينة",
    city: "جدة",
    country: "SA",
    status: "active",
    branches_count: 3,
    employees_count: 80,
    created_at: "2024-02-20T14:30:00Z",
  },
]

const mockBranches = [
  {
    id: 1,
    name: "Main Branch",
    name_ar: "الفرع الرئيسي",
    code: "BR001",
    company_id: 1,
    company_name: "Gaara Agriculture",
    branch_type: "main",
    email: "main@gaara-agri.com",
    phone: "+966-11-1234567",
    address: "شارع الملك فهد",
    city: "الرياض",
    status: "active",
    is_default: true,
    employees_count: 50,
    created_at: "2024-01-15T10:00:00Z",
  },
  {
    id: 2,
    name: "Jeddah Branch",
    name_ar: "فرع جدة",
    code: "BR002",
    company_id: 1,
    company_name: "Gaara Agriculture",
    branch_type: "branch",
    email: "jeddah@gaara-agri.com",
    phone: "+966-12-1234567",
    address: "طريق الكورنيش",
    city: "جدة",
    status: "active",
    is_default: false,
    employees_count: 30,
    created_at: "2024-03-10T09:00:00Z",
  },
]

const CompaniesPage = () => {
  const [activeTab, setActiveTab] = useState("companies")
  const [companies, setCompanies] = useState([])
  const [branches, setBranches] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  
  // Dialog states
  const [isCompanyDialogOpen, setIsCompanyDialogOpen] = useState(false)
  const [isBranchDialogOpen, setIsBranchDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [selectedItem, setSelectedItem] = useState(null)
  const [dialogMode, setDialogMode] = useState("add") // add or edit

  // Form hooks
  const companyForm = useForm({
    resolver: zodResolver(companySchema),
    defaultValues: {
      name: "",
      name_ar: "",
      code: "",
      legal_name: "",
      tax_id: "",
      email: "",
      phone: "",
      website: "",
      address: "",
      city: "",
      country: "SA",
      status: "active",
    },
  })

  const branchForm = useForm({
    resolver: zodResolver(branchSchema),
    defaultValues: {
      name: "",
      name_ar: "",
      code: "",
      company: "",
      branch_type: "branch",
      email: "",
      phone: "",
      address: "",
      city: "",
      status: "active",
      is_default: false,
    },
  })

  // Load data
  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    setIsLoading(true)
    try {
      // In production, use: const data = await api.get("/companies/")
      await new Promise((resolve) => setTimeout(resolve, 500))
      setCompanies(mockCompanies)
      setBranches(mockBranches)
    } catch (error) {
      toast.error("فشل تحميل البيانات")
    } finally {
      setIsLoading(false)
    }
  }

  // Filter data
  const filteredCompanies = companies.filter((company) => {
    const matchesSearch =
      company.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      company.name_ar.includes(searchQuery) ||
      company.code.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || company.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const filteredBranches = branches.filter((branch) => {
    const matchesSearch =
      branch.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      branch.name_ar.includes(searchQuery) ||
      branch.code.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || branch.status === statusFilter
    return matchesSearch && matchesStatus
  })

  // Handlers
  const handleAddCompany = async (data) => {
    try {
      const newCompany = {
        id: companies.length + 1,
        ...data,
        branches_count: 0,
        employees_count: 0,
        created_at: new Date().toISOString(),
      }
      setCompanies([...companies, newCompany])
      setIsCompanyDialogOpen(false)
      companyForm.reset()
      toast.success("تم إضافة الشركة بنجاح")
    } catch (error) {
      toast.error("فشل إضافة الشركة")
    }
  }

  const handleEditCompany = async (data) => {
    try {
      setCompanies(
        companies.map((c) => (c.id === selectedItem.id ? { ...c, ...data } : c))
      )
      setIsCompanyDialogOpen(false)
      setSelectedItem(null)
      companyForm.reset()
      toast.success("تم تحديث الشركة بنجاح")
    } catch (error) {
      toast.error("فشل تحديث الشركة")
    }
  }

  const handleAddBranch = async (data) => {
    try {
      const company = companies.find((c) => c.id === parseInt(data.company))
      const newBranch = {
        id: branches.length + 1,
        ...data,
        company_id: parseInt(data.company),
        company_name: company?.name || "",
        employees_count: 0,
        created_at: new Date().toISOString(),
      }
      setBranches([...branches, newBranch])
      setIsBranchDialogOpen(false)
      branchForm.reset()
      toast.success("تم إضافة الفرع بنجاح")
    } catch (error) {
      toast.error("فشل إضافة الفرع")
    }
  }

  const handleEditBranch = async (data) => {
    try {
      const company = companies.find((c) => c.id === parseInt(data.company))
      setBranches(
        branches.map((b) =>
          b.id === selectedItem.id
            ? { ...b, ...data, company_id: parseInt(data.company), company_name: company?.name || "" }
            : b
        )
      )
      setIsBranchDialogOpen(false)
      setSelectedItem(null)
      branchForm.reset()
      toast.success("تم تحديث الفرع بنجاح")
    } catch (error) {
      toast.error("فشل تحديث الفرع")
    }
  }

  const handleDelete = async () => {
    try {
      if (activeTab === "companies") {
        setCompanies(companies.filter((c) => c.id !== selectedItem.id))
      } else {
        setBranches(branches.filter((b) => b.id !== selectedItem.id))
      }
      setIsDeleteDialogOpen(false)
      setSelectedItem(null)
      toast.success("تم الحذف بنجاح")
    } catch (error) {
      toast.error("فشل الحذف")
    }
  }

  const openEditDialog = (item, type) => {
    setSelectedItem(item)
    setDialogMode("edit")
    if (type === "company") {
      companyForm.reset({
        name: item.name,
        name_ar: item.name_ar,
        code: item.code,
        legal_name: item.legal_name || "",
        tax_id: item.tax_id || "",
        email: item.email || "",
        phone: item.phone || "",
        website: item.website || "",
        address: item.address || "",
        city: item.city || "",
        country: item.country || "SA",
        status: item.status,
      })
      setIsCompanyDialogOpen(true)
    } else {
      branchForm.reset({
        name: item.name,
        name_ar: item.name_ar,
        code: item.code,
        company: item.company_id?.toString() || "",
        branch_type: item.branch_type,
        email: item.email || "",
        phone: item.phone || "",
        address: item.address || "",
        city: item.city || "",
        status: item.status,
        is_default: item.is_default,
      })
      setIsBranchDialogOpen(true)
    }
  }

  const openAddDialog = (type) => {
    setSelectedItem(null)
    setDialogMode("add")
    if (type === "company") {
      companyForm.reset()
      setIsCompanyDialogOpen(true)
    } else {
      branchForm.reset()
      setIsBranchDialogOpen(true)
    }
  }

  // Status labels
  const statusLabels = {
    active: "نشط",
    inactive: "غير نشط",
    suspended: "موقوف",
  }

  const branchTypeLabels = {
    main: "رئيسي",
    branch: "فرع",
    warehouse: "مستودع",
    showroom: "معرض",
  }

  // Company columns
  const companyColumns = [
    {
      accessorKey: "company",
      header: "الشركة",
      cell: ({ row }) => {
        const company = row.original
        return (
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Building2 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="font-medium">{company.name}</p>
              <p className="text-sm text-muted-foreground">{company.name_ar}</p>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "code",
      header: "الكود",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.code}</Badge>
      ),
    },
    {
      accessorKey: "city",
      header: "المدينة",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <MapPin className="w-4 h-4" />
          {row.original.city || "-"}
        </div>
      ),
    },
    {
      accessorKey: "branches_count",
      header: "الفروع",
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <Building className="w-4 h-4 text-muted-foreground" />
          {row.original.branches_count}
        </div>
      ),
    },
    {
      accessorKey: "employees_count",
      header: "الموظفين",
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <Users className="w-4 h-4 text-muted-foreground" />
          {row.original.employees_count}
        </div>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const status = row.original.status
        return (
          <Badge variant={status === "active" ? "default" : "secondary"}>
            {status === "active" ? (
              <CheckCircle2 className="w-3 h-3 ml-1" />
            ) : (
              <XCircle className="w-3 h-3 ml-1" />
            )}
            {statusLabels[status]}
          </Badge>
        )
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const company = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => { setSelectedItem(company); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />
                عرض التفاصيل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => openEditDialog(company, "company")}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => openAddDialog("branch")}>
                <Building className="w-4 h-4 ml-2" />
                إضافة فرع
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => { setSelectedItem(company); setIsDeleteDialogOpen(true); }}
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

  // Branch columns
  const branchColumns = [
    {
      accessorKey: "branch",
      header: "الفرع",
      cell: ({ row }) => {
        const branch = row.original
        return (
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Building className="w-5 h-5 text-green-600 dark:text-green-400" />
            </div>
            <div>
              <p className="font-medium">{branch.name}</p>
              <p className="text-sm text-muted-foreground">{branch.name_ar}</p>
            </div>
          </div>
        )
      },
    },
    {
      accessorKey: "code",
      header: "الكود",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.code}</Badge>
      ),
    },
    {
      accessorKey: "company_name",
      header: "الشركة",
    },
    {
      accessorKey: "branch_type",
      header: "النوع",
      cell: ({ row }) => (
        <Badge variant="secondary">{branchTypeLabels[row.original.branch_type]}</Badge>
      ),
    },
    {
      accessorKey: "city",
      header: "المدينة",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <MapPin className="w-4 h-4" />
          {row.original.city || "-"}
        </div>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const status = row.original.status
        const isDefault = row.original.is_default
        return (
          <div className="flex items-center gap-2">
            <Badge variant={status === "active" ? "default" : "secondary"}>
              {statusLabels[status]}
            </Badge>
            {isDefault && (
              <Badge variant="outline" className="text-blue-600">
                افتراضي
              </Badge>
            )}
          </div>
        )
      },
    },
    {
      id: "actions",
      header: "الإجراءات",
      cell: ({ row }) => {
        const branch = row.original
        return (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>الإجراءات</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem onClick={() => openEditDialog(branch, "branch")}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => { setSelectedItem(branch); setIsDeleteDialogOpen(true); }}
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
            <Building2 className="w-7 h-7 text-blue-500" />
            إدارة الشركات والفروع
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            إدارة الشركات والفروع والأقسام
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button onClick={() => openAddDialog(activeTab === "companies" ? "company" : "branch")}>
            <Plus className="w-4 h-4 ml-2" />
            {activeTab === "companies" ? "إضافة شركة" : "إضافة فرع"}
          </Button>
        </div>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="companies" className="gap-2">
            <Building2 className="w-4 h-4" />
            الشركات ({companies.length})
          </TabsTrigger>
          <TabsTrigger value="branches" className="gap-2">
            <Building className="w-4 h-4" />
            الفروع ({branches.length})
          </TabsTrigger>
        </TabsList>

        {/* Filters */}
        <Card className="mt-4">
          <CardContent className="p-4">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="بحث..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pr-10"
                  />
                </div>
              </div>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-[180px]">
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

        {/* Companies Tab */}
        <TabsContent value="companies">
          <Card>
            <CardHeader>
              <CardTitle>الشركات ({filteredCompanies.length})</CardTitle>
              <CardDescription>قائمة جميع الشركات المسجلة في النظام</CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable
                columns={companyColumns}
                data={filteredCompanies}
                isLoading={isLoading}
                searchKey="name"
                defaultPageSize={10}
              />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Branches Tab */}
        <TabsContent value="branches">
          <Card>
            <CardHeader>
              <CardTitle>الفروع ({filteredBranches.length})</CardTitle>
              <CardDescription>قائمة جميع الفروع المسجلة في النظام</CardDescription>
            </CardHeader>
            <CardContent>
              <DataTable
                columns={branchColumns}
                data={filteredBranches}
                isLoading={isLoading}
                searchKey="name"
                defaultPageSize={10}
              />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Company Dialog */}
      <Dialog open={isCompanyDialogOpen} onOpenChange={setIsCompanyDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {dialogMode === "add" ? "إضافة شركة جديدة" : "تعديل الشركة"}
            </DialogTitle>
            <DialogDescription>
              {dialogMode === "add" ? "أدخل معلومات الشركة الجديدة" : "تعديل معلومات الشركة"}
            </DialogDescription>
          </DialogHeader>
          <form
            onSubmit={companyForm.handleSubmit(
              dialogMode === "add" ? handleAddCompany : handleEditCompany
            )}
            className="space-y-4"
          >
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name">اسم الشركة (إنجليزي)</Label>
                <Input id="name" {...companyForm.register("name")} />
                {companyForm.formState.errors.name && (
                  <p className="text-sm text-red-500 mt-1">
                    {companyForm.formState.errors.name.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="name_ar">اسم الشركة (عربي)</Label>
                <Input id="name_ar" {...companyForm.register("name_ar")} />
                {companyForm.formState.errors.name_ar && (
                  <p className="text-sm text-red-500 mt-1">
                    {companyForm.formState.errors.name_ar.message}
                  </p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="code">الكود</Label>
                <Input id="code" {...companyForm.register("code")} />
                {companyForm.formState.errors.code && (
                  <p className="text-sm text-red-500 mt-1">
                    {companyForm.formState.errors.code.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="legal_name">الاسم القانوني</Label>
                <Input id="legal_name" {...companyForm.register("legal_name")} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="tax_id">الرقم الضريبي</Label>
                <Input id="tax_id" {...companyForm.register("tax_id")} />
              </div>
              <div>
                <Label htmlFor="status">الحالة</Label>
                <Select
                  value={companyForm.watch("status")}
                  onValueChange={(value) => companyForm.setValue("status", value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">نشط</SelectItem>
                    <SelectItem value="inactive">غير نشط</SelectItem>
                    <SelectItem value="suspended">موقوف</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <Separator />
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="email">البريد الإلكتروني</Label>
                <Input id="email" type="email" {...companyForm.register("email")} />
              </div>
              <div>
                <Label htmlFor="phone">الهاتف</Label>
                <Input id="phone" {...companyForm.register("phone")} />
              </div>
            </div>
            <div>
              <Label htmlFor="website">الموقع الإلكتروني</Label>
              <Input id="website" {...companyForm.register("website")} />
            </div>
            <div>
              <Label htmlFor="address">العنوان</Label>
              <Textarea id="address" {...companyForm.register("address")} />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="city">المدينة</Label>
                <Input id="city" {...companyForm.register("city")} />
              </div>
              <div>
                <Label htmlFor="country">الدولة</Label>
                <Select
                  value={companyForm.watch("country")}
                  onValueChange={(value) => companyForm.setValue("country", value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="SA">السعودية</SelectItem>
                    <SelectItem value="AE">الإمارات</SelectItem>
                    <SelectItem value="EG">مصر</SelectItem>
                    <SelectItem value="JO">الأردن</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsCompanyDialogOpen(false)}>
                إلغاء
              </Button>
              <Button type="submit">{dialogMode === "add" ? "إضافة" : "حفظ"}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Branch Dialog */}
      <Dialog open={isBranchDialogOpen} onOpenChange={setIsBranchDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {dialogMode === "add" ? "إضافة فرع جديد" : "تعديل الفرع"}
            </DialogTitle>
            <DialogDescription>
              {dialogMode === "add" ? "أدخل معلومات الفرع الجديد" : "تعديل معلومات الفرع"}
            </DialogDescription>
          </DialogHeader>
          <form
            onSubmit={branchForm.handleSubmit(
              dialogMode === "add" ? handleAddBranch : handleEditBranch
            )}
            className="space-y-4"
          >
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="branch-name">اسم الفرع (إنجليزي)</Label>
                <Input id="branch-name" {...branchForm.register("name")} />
                {branchForm.formState.errors.name && (
                  <p className="text-sm text-red-500 mt-1">
                    {branchForm.formState.errors.name.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="branch-name_ar">اسم الفرع (عربي)</Label>
                <Input id="branch-name_ar" {...branchForm.register("name_ar")} />
                {branchForm.formState.errors.name_ar && (
                  <p className="text-sm text-red-500 mt-1">
                    {branchForm.formState.errors.name_ar.message}
                  </p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="branch-code">الكود</Label>
                <Input id="branch-code" {...branchForm.register("code")} />
                {branchForm.formState.errors.code && (
                  <p className="text-sm text-red-500 mt-1">
                    {branchForm.formState.errors.code.message}
                  </p>
                )}
              </div>
              <div>
                <Label htmlFor="branch-company">الشركة</Label>
                <Select
                  value={branchForm.watch("company")}
                  onValueChange={(value) => branchForm.setValue("company", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="اختر الشركة" />
                  </SelectTrigger>
                  <SelectContent>
                    {companies.map((company) => (
                      <SelectItem key={company.id} value={company.id.toString()}>
                        {company.name_ar}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {branchForm.formState.errors.company && (
                  <p className="text-sm text-red-500 mt-1">
                    {branchForm.formState.errors.company.message}
                  </p>
                )}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="branch-type">نوع الفرع</Label>
                <Select
                  value={branchForm.watch("branch_type")}
                  onValueChange={(value) => branchForm.setValue("branch_type", value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="main">رئيسي</SelectItem>
                    <SelectItem value="branch">فرع</SelectItem>
                    <SelectItem value="warehouse">مستودع</SelectItem>
                    <SelectItem value="showroom">معرض</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="branch-status">الحالة</Label>
                <Select
                  value={branchForm.watch("status")}
                  onValueChange={(value) => branchForm.setValue("status", value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">نشط</SelectItem>
                    <SelectItem value="inactive">غير نشط</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="branch-email">البريد الإلكتروني</Label>
                <Input id="branch-email" type="email" {...branchForm.register("email")} />
              </div>
              <div>
                <Label htmlFor="branch-phone">الهاتف</Label>
                <Input id="branch-phone" {...branchForm.register("phone")} />
              </div>
            </div>
            <div>
              <Label htmlFor="branch-address">العنوان</Label>
              <Textarea id="branch-address" {...branchForm.register("address")} />
            </div>
            <div>
              <Label htmlFor="branch-city">المدينة</Label>
              <Input id="branch-city" {...branchForm.register("city")} />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsBranchDialogOpen(false)}>
                إلغاء
              </Button>
              <Button type="submit">{dialogMode === "add" ? "إضافة" : "حفظ"}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>هل أنت متأكد؟</AlertDialogTitle>
            <AlertDialogDescription>
              سيتم حذف {activeTab === "companies" ? "الشركة" : "الفرع"} "{selectedItem?.name_ar}" بشكل دائم.
              لا يمكن التراجع عن هذا الإجراء.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete} className="bg-red-600 hover:bg-red-700">
              حذف
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      {/* View Details Dialog */}
      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>تفاصيل الشركة</DialogTitle>
          </DialogHeader>
          {selectedItem && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                  <Building2 className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold">{selectedItem.name}</h3>
                  <p className="text-muted-foreground">{selectedItem.name_ar}</p>
                </div>
                <Badge variant={selectedItem.status === "active" ? "default" : "secondary"} className="mr-auto">
                  {statusLabels[selectedItem.status]}
                </Badge>
              </div>
              <Separator />
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">الكود</p>
                  <p className="font-medium">{selectedItem.code}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">الاسم القانوني</p>
                  <p className="font-medium">{selectedItem.legal_name || "-"}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">الرقم الضريبي</p>
                  <p className="font-medium">{selectedItem.tax_id || "-"}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">البريد الإلكتروني</p>
                  <p className="font-medium">{selectedItem.email || "-"}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">الهاتف</p>
                  <p className="font-medium">{selectedItem.phone || "-"}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">الموقع</p>
                  <p className="font-medium">{selectedItem.website || "-"}</p>
                </div>
                <div className="col-span-2">
                  <p className="text-sm text-muted-foreground">العنوان</p>
                  <p className="font-medium">{selectedItem.address || "-"}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">المدينة</p>
                  <p className="font-medium">{selectedItem.city || "-"}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">تاريخ الإنشاء</p>
                  <p className="font-medium">{formatDate(selectedItem.created_at)}</p>
                </div>
              </div>
              <Separator />
              <div className="flex items-center gap-4">
                <Card className="flex-1">
                  <CardContent className="p-4 flex items-center gap-3">
                    <Building className="w-8 h-8 text-blue-500" />
                    <div>
                      <p className="text-2xl font-bold">{selectedItem.branches_count}</p>
                      <p className="text-sm text-muted-foreground">فرع</p>
                    </div>
                  </CardContent>
                </Card>
                <Card className="flex-1">
                  <CardContent className="p-4 flex items-center gap-3">
                    <Users className="w-8 h-8 text-green-500" />
                    <div>
                      <p className="text-2xl font-bold">{selectedItem.employees_count}</p>
                      <p className="text-sm text-muted-foreground">موظف</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsViewDialogOpen(false)}>
              إغلاق
            </Button>
            <Button onClick={() => { setIsViewDialogOpen(false); openEditDialog(selectedItem, "company"); }}>
              <Edit className="w-4 h-4 ml-2" />
              تعديل
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default CompaniesPage
