/**
 * Farms Management Page - إدارة المزارع
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import {
  Leaf,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  MapPin,
  Ruler,
  Droplets,
  Sun,
  RefreshCw,
  Map,
  BarChart3,
  Thermometer,
  Wind,
  CheckCircle2,
  XCircle,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
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
import { Progress } from "@/components/ui/progress"

import { DataTable } from "@/components/common"
import { formatDate } from "@/lib/utils"

// Form schema
const farmSchema = z.object({
  name: z.string().min(2, "اسم المزرعة يجب أن يكون على الأقل حرفين"),
  name_ar: z.string().min(2, "الاسم بالعربية يجب أن يكون على الأقل حرفين"),
  code: z.string().min(2, "الكود يجب أن يكون على الأقل حرفين"),
  location: z.string().min(2, "الموقع مطلوب"),
  area: z.number().min(1, "المساحة يجب أن تكون أكبر من صفر"),
  area_unit: z.enum(["hectare", "dunum", "sqm"]),
  soil_type: z.string().optional(),
  irrigation_type: z.enum(["drip", "sprinkler", "flood", "none"]),
  status: z.enum(["active", "inactive", "maintenance"]),
  manager: z.string().optional(),
  description: z.string().optional(),
})

// Mock data
const mockFarms = [
  {
    id: 1,
    name: "Green Valley Farm",
    name_ar: "مزرعة الوادي الأخضر",
    code: "GVF001",
    location: "المنطقة الشمالية، الرياض",
    coordinates: { lat: 24.7136, lng: 46.6753 },
    area: 150,
    area_unit: "hectare",
    soil_type: "طمي",
    irrigation_type: "drip",
    status: "active",
    manager: "أحمد محمد",
    description: "مزرعة متخصصة في إنتاج الخضروات",
    crops: ["طماطم", "خيار", "فلفل"],
    workers_count: 25,
    current_season: "شتوي 2026",
    weather: { temp: 22, humidity: 45, wind: 12 },
    created_at: "2023-01-15T10:00:00Z",
  },
  {
    id: 2,
    name: "Desert Oasis Farm",
    name_ar: "مزرعة واحة الصحراء",
    code: "DOF002",
    location: "القصيم",
    coordinates: { lat: 26.3267, lng: 43.9686 },
    area: 200,
    area_unit: "hectare",
    soil_type: "رملي",
    irrigation_type: "sprinkler",
    status: "active",
    manager: "سارة أحمد",
    description: "مزرعة متخصصة في إنتاج التمور والحمضيات",
    crops: ["نخيل", "برتقال", "ليمون"],
    workers_count: 40,
    current_season: "شتوي 2026",
    weather: { temp: 18, humidity: 30, wind: 8 },
    created_at: "2022-06-20T14:30:00Z",
  },
  {
    id: 3,
    name: "Highland Wheat Farm",
    name_ar: "مزرعة قمح المرتفعات",
    code: "HWF003",
    location: "عسير",
    coordinates: { lat: 18.2164, lng: 42.5053 },
    area: 500,
    area_unit: "hectare",
    soil_type: "طيني",
    irrigation_type: "flood",
    status: "maintenance",
    manager: "محمد علي",
    description: "مزرعة حبوب كبيرة",
    crops: ["قمح", "شعير"],
    workers_count: 60,
    current_season: "شتوي 2026",
    weather: { temp: 15, humidity: 55, wind: 20 },
    created_at: "2021-03-10T09:00:00Z",
  },
]

const FarmsPage = () => {
  const [farms, setFarms] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [viewMode, setViewMode] = useState("grid") // grid or list
  
  // Dialog states
  const [isFarmDialogOpen, setIsFarmDialogOpen] = useState(false)
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [selectedFarm, setSelectedFarm] = useState(null)
  const [dialogMode, setDialogMode] = useState("add")

  // Form
  const form = useForm({
    resolver: zodResolver(farmSchema),
    defaultValues: {
      name: "",
      name_ar: "",
      code: "",
      location: "",
      area: 0,
      area_unit: "hectare",
      soil_type: "",
      irrigation_type: "drip",
      status: "active",
      manager: "",
      description: "",
    },
  })

  useEffect(() => {
    loadFarms()
  }, [])

  const loadFarms = async () => {
    setIsLoading(true)
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))
      setFarms(mockFarms)
    } catch (error) {
      toast.error("فشل تحميل المزارع")
    } finally {
      setIsLoading(false)
    }
  }

  // Filter farms
  const filteredFarms = farms.filter((farm) => {
    const matchesSearch =
      farm.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      farm.name_ar.includes(searchQuery) ||
      farm.code.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesStatus = statusFilter === "all" || farm.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const handleAddFarm = async (data) => {
    try {
      const newFarm = {
        id: farms.length + 1,
        ...data,
        coordinates: { lat: 24.7136, lng: 46.6753 },
        crops: [],
        workers_count: 0,
        current_season: "شتوي 2026",
        weather: { temp: 20, humidity: 40, wind: 10 },
        created_at: new Date().toISOString(),
      }
      setFarms([...farms, newFarm])
      setIsFarmDialogOpen(false)
      form.reset()
      toast.success("تم إضافة المزرعة بنجاح")
    } catch (error) {
      toast.error("فشل إضافة المزرعة")
    }
  }

  const handleEditFarm = async (data) => {
    try {
      setFarms(farms.map((f) => (f.id === selectedFarm.id ? { ...f, ...data } : f)))
      setIsFarmDialogOpen(false)
      setSelectedFarm(null)
      form.reset()
      toast.success("تم تحديث المزرعة بنجاح")
    } catch (error) {
      toast.error("فشل تحديث المزرعة")
    }
  }

  const handleDelete = async () => {
    try {
      setFarms(farms.filter((f) => f.id !== selectedFarm.id))
      setIsDeleteDialogOpen(false)
      setSelectedFarm(null)
      toast.success("تم حذف المزرعة بنجاح")
    } catch (error) {
      toast.error("فشل حذف المزرعة")
    }
  }

  const openEditDialog = (farm) => {
    setSelectedFarm(farm)
    setDialogMode("edit")
    form.reset({
      name: farm.name,
      name_ar: farm.name_ar,
      code: farm.code,
      location: farm.location,
      area: farm.area,
      area_unit: farm.area_unit,
      soil_type: farm.soil_type || "",
      irrigation_type: farm.irrigation_type,
      status: farm.status,
      manager: farm.manager || "",
      description: farm.description || "",
    })
    setIsFarmDialogOpen(true)
  }

  const openAddDialog = () => {
    setSelectedFarm(null)
    setDialogMode("add")
    form.reset()
    setIsFarmDialogOpen(true)
  }

  const statusLabels = {
    active: "نشط",
    inactive: "غير نشط",
    maintenance: "صيانة",
  }

  const statusColors = {
    active: "default",
    inactive: "secondary",
    maintenance: "outline",
  }

  const irrigationLabels = {
    drip: "تنقيط",
    sprinkler: "رش",
    flood: "غمر",
    none: "بدون",
  }

  const areaUnitLabels = {
    hectare: "هكتار",
    dunum: "دونم",
    sqm: "م²",
  }

  // Stats
  const stats = {
    total: farms.length,
    active: farms.filter(f => f.status === "active").length,
    totalArea: farms.reduce((sum, f) => sum + f.area, 0),
    totalWorkers: farms.reduce((sum, f) => sum + f.workers_count, 0),
  }

  // Farm Card Component
  const FarmCard = ({ farm }) => (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
              farm.status === "active" ? "bg-green-100 dark:bg-green-900" :
              farm.status === "maintenance" ? "bg-yellow-100 dark:bg-yellow-900" :
              "bg-gray-100 dark:bg-gray-900"
            }`}>
              <Leaf className={`w-6 h-6 ${
                farm.status === "active" ? "text-green-600" :
                farm.status === "maintenance" ? "text-yellow-600" :
                "text-gray-600"
              }`} />
            </div>
            <div>
              <CardTitle className="text-lg">{farm.name_ar}</CardTitle>
              <p className="text-sm text-muted-foreground">{farm.code}</p>
            </div>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm">
                <MoreVertical className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => { setSelectedFarm(farm); setIsViewDialogOpen(true); }}>
                <Eye className="w-4 h-4 ml-2" />
                عرض التفاصيل
              </DropdownMenuItem>
              <DropdownMenuItem onClick={() => openEditDialog(farm)}>
                <Edit className="w-4 h-4 ml-2" />
                تعديل
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => { setSelectedFarm(farm); setIsDeleteDialogOpen(true); }}
                className="text-red-600"
              >
                <Trash2 className="w-4 h-4 ml-2" />
                حذف
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <MapPin className="w-4 h-4" />
            {farm.location}
          </div>
          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-1">
              <Ruler className="w-4 h-4 text-blue-500" />
              <span>{farm.area} {areaUnitLabels[farm.area_unit]}</span>
            </div>
            <div className="flex items-center gap-1">
              <Droplets className="w-4 h-4 text-cyan-500" />
              <span>{irrigationLabels[farm.irrigation_type]}</span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <Badge variant={statusColors[farm.status]}>
              {statusLabels[farm.status]}
            </Badge>
            <div className="flex items-center gap-3 text-sm text-muted-foreground">
              <div className="flex items-center gap-1">
                <Thermometer className="w-3 h-3" />
                {farm.weather.temp}°C
              </div>
              <div className="flex items-center gap-1">
                <Droplets className="w-3 h-3" />
                {farm.weather.humidity}%
              </div>
            </div>
          </div>
          <Separator />
          <div className="flex flex-wrap gap-1">
            {farm.crops.map((crop, idx) => (
              <Badge key={idx} variant="outline" className="text-xs">
                {crop}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Leaf className="w-7 h-7 text-green-500" />
            إدارة المزارع
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            إدارة ومتابعة المزارع والأراضي الزراعية
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadFarms}>
            <RefreshCw className="w-4 h-4 ml-2" />
            تحديث
          </Button>
          <Button onClick={openAddDialog}>
            <Plus className="w-4 h-4 ml-2" />
            إضافة مزرعة
          </Button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Leaf className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">إجمالي المزارع</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.active}</p>
              <p className="text-sm text-muted-foreground">مزارع نشطة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Ruler className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalArea}</p>
              <p className="text-sm text-muted-foreground">هكتار إجمالي</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Sun className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalWorkers}</p>
              <p className="text-sm text-muted-foreground">عامل</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  placeholder="بحث في المزارع..."
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
                <SelectItem value="maintenance">صيانة</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Farms Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredFarms.map((farm) => (
          <FarmCard key={farm.id} farm={farm} />
        ))}
      </div>

      {/* Farm Dialog */}
      <Dialog open={isFarmDialogOpen} onOpenChange={setIsFarmDialogOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {dialogMode === "add" ? "إضافة مزرعة جديدة" : "تعديل المزرعة"}
            </DialogTitle>
            <DialogDescription>
              {dialogMode === "add" ? "أدخل معلومات المزرعة الجديدة" : "تعديل معلومات المزرعة"}
            </DialogDescription>
          </DialogHeader>
          <form
            onSubmit={form.handleSubmit(dialogMode === "add" ? handleAddFarm : handleEditFarm)}
            className="space-y-4"
          >
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="name">اسم المزرعة (إنجليزي)</Label>
                <Input id="name" {...form.register("name")} />
              </div>
              <div>
                <Label htmlFor="name_ar">اسم المزرعة (عربي)</Label>
                <Input id="name_ar" {...form.register("name_ar")} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="code">الكود</Label>
                <Input id="code" {...form.register("code")} />
              </div>
              <div>
                <Label htmlFor="location">الموقع</Label>
                <Input id="location" {...form.register("location")} />
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <Label htmlFor="area">المساحة</Label>
                <Input
                  id="area"
                  type="number"
                  {...form.register("area", { valueAsNumber: true })}
                />
              </div>
              <div>
                <Label>وحدة القياس</Label>
                <Select
                  value={form.watch("area_unit")}
                  onValueChange={(value) => form.setValue("area_unit", value)}
                >
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="hectare">هكتار</SelectItem>
                    <SelectItem value="dunum">دونم</SelectItem>
                    <SelectItem value="sqm">متر مربع</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>نوع الري</Label>
                <Select
                  value={form.watch("irrigation_type")}
                  onValueChange={(value) => form.setValue("irrigation_type", value)}
                >
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="drip">تنقيط</SelectItem>
                    <SelectItem value="sprinkler">رش</SelectItem>
                    <SelectItem value="flood">غمر</SelectItem>
                    <SelectItem value="none">بدون</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="soil_type">نوع التربة</Label>
                <Input id="soil_type" {...form.register("soil_type")} />
              </div>
              <div>
                <Label>الحالة</Label>
                <Select
                  value={form.watch("status")}
                  onValueChange={(value) => form.setValue("status", value)}
                >
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="active">نشط</SelectItem>
                    <SelectItem value="inactive">غير نشط</SelectItem>
                    <SelectItem value="maintenance">صيانة</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div>
              <Label htmlFor="manager">المدير المسؤول</Label>
              <Input id="manager" {...form.register("manager")} />
            </div>
            <div>
              <Label htmlFor="description">الوصف</Label>
              <Textarea id="description" {...form.register("description")} />
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={() => setIsFarmDialogOpen(false)}>
                إلغاء
              </Button>
              <Button type="submit">{dialogMode === "add" ? "إضافة" : "حفظ"}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* View Details Dialog */}
      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>تفاصيل المزرعة</DialogTitle>
          </DialogHeader>
          {selectedFarm && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className={`w-16 h-16 rounded-lg flex items-center justify-center ${
                  selectedFarm.status === "active" ? "bg-green-100 dark:bg-green-900" : "bg-gray-100 dark:bg-gray-900"
                }`}>
                  <Leaf className={`w-8 h-8 ${
                    selectedFarm.status === "active" ? "text-green-600" : "text-gray-600"
                  }`} />
                </div>
                <div>
                  <h3 className="text-lg font-semibold">{selectedFarm.name_ar}</h3>
                  <p className="text-muted-foreground">{selectedFarm.name}</p>
                </div>
                <Badge variant={statusColors[selectedFarm.status]} className="mr-auto">
                  {statusLabels[selectedFarm.status]}
                </Badge>
              </div>
              <Separator />
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">الكود</p>
                  <p className="font-medium">{selectedFarm.code}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">الموقع</p>
                  <p className="font-medium">{selectedFarm.location}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">المساحة</p>
                  <p className="font-medium">{selectedFarm.area} {areaUnitLabels[selectedFarm.area_unit]}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">نوع الري</p>
                  <p className="font-medium">{irrigationLabels[selectedFarm.irrigation_type]}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">نوع التربة</p>
                  <p className="font-medium">{selectedFarm.soil_type}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">المدير</p>
                  <p className="font-medium">{selectedFarm.manager}</p>
                </div>
              </div>
              <Separator />
              <div>
                <p className="text-sm text-muted-foreground mb-2">المحاصيل</p>
                <div className="flex flex-wrap gap-2">
                  {selectedFarm.crops.map((crop, idx) => (
                    <Badge key={idx} variant="outline">{crop}</Badge>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-2">الطقس الحالي</p>
                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-2">
                    <Thermometer className="w-4 h-4 text-red-500" />
                    <span>{selectedFarm.weather.temp}°C</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Droplets className="w-4 h-4 text-blue-500" />
                    <span>{selectedFarm.weather.humidity}%</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Wind className="w-4 h-4 text-gray-500" />
                    <span>{selectedFarm.weather.wind} كم/س</span>
                  </div>
                </div>
              </div>
            </div>
          )}
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsViewDialogOpen(false)}>
              إغلاق
            </Button>
            <Button onClick={() => { setIsViewDialogOpen(false); openEditDialog(selectedFarm); }}>
              <Edit className="w-4 h-4 ml-2" />
              تعديل
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation */}
      <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>هل أنت متأكد؟</AlertDialogTitle>
            <AlertDialogDescription>
              سيتم حذف المزرعة "{selectedFarm?.name_ar}" بشكل دائم.
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
    </div>
  )
}

export default FarmsPage
