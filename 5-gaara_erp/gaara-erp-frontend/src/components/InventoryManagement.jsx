import { useState, useEffect } from "react"
import { useLocation } from "react-router-dom"
import { motion } from "framer-motion"
import { toast } from "sonner"
import {
  Package,
  Warehouse,
  ArrowRightLeft,
  FileText,
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  Plus,
  Barcode,
  Tag,
  DollarSign,
  Box,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
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

import { DataTable, FormModal, StatsCard } from "@/components/common"
import { formatCurrency, formatNumber } from "@/lib/utils"

// Mock data
const mockProducts = [
  {
    id: 1,
    sku: "PRD-001",
    name: "بذور طماطم هجين",
    category: "بذور",
    unit: "كيلو",
    costPrice: 150,
    sellPrice: 200,
    quantity: 500,
    minStock: 100,
    warehouse: "المخزن أ",
    status: "متوفر",
  },
  {
    id: 2,
    sku: "PRD-002",
    name: "سماد عضوي NPK",
    category: "أسمدة",
    unit: "كيلو",
    costPrice: 80,
    sellPrice: 120,
    quantity: 50,
    minStock: 100,
    warehouse: "المخزن أ",
    status: "منخفض",
  },
  {
    id: 3,
    sku: "PRD-003",
    name: "مبيد حشري طبيعي",
    category: "مبيدات",
    unit: "لتر",
    costPrice: 200,
    sellPrice: 280,
    quantity: 200,
    minStock: 50,
    warehouse: "المخزن ب",
    status: "متوفر",
  },
  {
    id: 4,
    sku: "PRD-004",
    name: "شتلات فراولة",
    category: "شتلات",
    unit: "قطعة",
    costPrice: 5,
    sellPrice: 10,
    quantity: 1000,
    minStock: 200,
    warehouse: "المخزن ج",
    status: "متوفر",
  },
  {
    id: 5,
    sku: "PRD-005",
    name: "أدوات ري",
    category: "معدات",
    unit: "قطعة",
    costPrice: 500,
    sellPrice: 700,
    quantity: 0,
    minStock: 10,
    warehouse: "المخزن أ",
    status: "نفذ",
  },
]

const mockWarehouses = [
  { id: 1, name: "المخزن أ", location: "المنطقة الصناعية", capacity: 1000, used: 750, manager: "أحمد محمد" },
  { id: 2, name: "المخزن ب", location: "المنطقة الشرقية", capacity: 500, used: 200, manager: "محمد علي" },
  { id: 3, name: "المخزن ج", location: "المنطقة الغربية", capacity: 800, used: 600, manager: "سعيد أحمد" },
]

const mockMovements = [
  { id: 1, date: "2025-01-10", type: "استلام", product: "بذور طماطم هجين", quantity: 100, from: "المورد X", to: "المخزن أ", reference: "PO-001" },
  { id: 2, date: "2025-01-09", type: "صرف", product: "سماد عضوي NPK", quantity: 50, from: "المخزن أ", to: "العميل Y", reference: "SO-001" },
  { id: 3, date: "2025-01-08", type: "تحويل", product: "مبيد حشري طبيعي", quantity: 30, from: "المخزن أ", to: "المخزن ب", reference: "TR-001" },
]

const categories = ["بذور", "أسمدة", "مبيدات", "شتلات", "معدات", "أخرى"]
const units = ["كيلو", "لتر", "قطعة", "متر", "صندوق"]

const InventoryManagement = () => {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState("products")
  const [products, setProducts] = useState(mockProducts)
  const [warehouses, setWarehouses] = useState(mockWarehouses)
  const [movements, setMovements] = useState(mockMovements)
  const [isLoading, setIsLoading] = useState(false)

  // Modals
  const [productModal, setProductModal] = useState(false)
  const [deleteDialog, setDeleteDialog] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [formData, setFormData] = useState({
    sku: "",
    name: "",
    category: "",
    unit: "",
    costPrice: "",
    sellPrice: "",
    quantity: "",
    minStock: "",
    warehouse: "",
    description: "",
  })

  // Set active tab based on URL
  useEffect(() => {
    if (location.pathname.includes("/products")) setActiveTab("products")
    else if (location.pathname.includes("/warehouses")) setActiveTab("warehouses")
    else if (location.pathname.includes("/movements")) setActiveTab("movements")
    else if (location.pathname.includes("/reports")) setActiveTab("reports")
  }, [location])

  // Stats calculations
  const totalProducts = products.length
  const totalValue = products.reduce((sum, p) => sum + p.costPrice * p.quantity, 0)
  const lowStockCount = products.filter((p) => p.quantity <= p.minStock && p.quantity > 0).length
  const outOfStockCount = products.filter((p) => p.quantity === 0).length

  // Product columns
  const productColumns = [
    { key: "sku", header: "الرمز", sortable: true },
    { key: "name", header: "اسم المنتج", sortable: true },
    { key: "category", header: "الفئة", sortable: true },
    {
      key: "quantity",
      header: "الكمية",
      sortable: true,
      render: (val, row) => (
        <div className="flex items-center gap-2">
          <span className={val <= row.minStock ? "text-red-600 font-medium" : ""}>
            {formatNumber(val)}
          </span>
          <span className="text-muted-foreground text-sm">{row.unit}</span>
        </div>
      ),
    },
    {
      key: "costPrice",
      header: "سعر التكلفة",
      sortable: true,
      render: (val) => formatCurrency(val),
    },
    {
      key: "sellPrice",
      header: "سعر البيع",
      sortable: true,
      render: (val) => formatCurrency(val),
    },
    {
      key: "status",
      header: "الحالة",
      render: (val) => (
        <Badge
          variant={
            val === "متوفر" ? "default" : val === "منخفض" ? "secondary" : "destructive"
          }
        >
          {val}
        </Badge>
      ),
    },
  ]

  // Warehouse columns
  const warehouseColumns = [
    { key: "name", header: "اسم المخزن", sortable: true },
    { key: "location", header: "الموقع", sortable: true },
    { key: "manager", header: "المسؤول" },
    {
      key: "capacity",
      header: "السعة",
      render: (val, row) => (
        <div className="space-y-1">
          <div className="flex justify-between text-sm">
            <span>{formatNumber(row.used)} / {formatNumber(val)}</span>
            <span className="text-muted-foreground">
              {Math.round((row.used / val) * 100)}%
            </span>
          </div>
          <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
            <div
              className="bg-primary h-2 rounded-full transition-all"
              style={{ width: `${(row.used / val) * 100}%` }}
            />
          </div>
        </div>
      ),
    },
  ]

  // Movement columns
  const movementColumns = [
    { key: "date", header: "التاريخ", sortable: true },
    { key: "reference", header: "المرجع" },
    {
      key: "type",
      header: "النوع",
      render: (val) => (
        <Badge
          variant={
            val === "استلام" ? "default" : val === "صرف" ? "secondary" : "outline"
          }
        >
          {val}
        </Badge>
      ),
    },
    { key: "product", header: "المنتج" },
    { key: "quantity", header: "الكمية", render: (val) => formatNumber(val) },
    { key: "from", header: "من" },
    { key: "to", header: "إلى" },
  ]

  // Handlers
  const handleAddProduct = () => {
    setSelectedProduct(null)
    setFormData({
      sku: `PRD-${String(products.length + 1).padStart(3, "0")}`,
      name: "",
      category: "",
      unit: "",
      costPrice: "",
      sellPrice: "",
      quantity: "",
      minStock: "",
      warehouse: "",
      description: "",
    })
    setProductModal(true)
  }

  const handleEditProduct = (product) => {
    setSelectedProduct(product)
    setFormData({
      sku: product.sku,
      name: product.name,
      category: product.category,
      unit: product.unit,
      costPrice: product.costPrice.toString(),
      sellPrice: product.sellPrice.toString(),
      quantity: product.quantity.toString(),
      minStock: product.minStock.toString(),
      warehouse: product.warehouse,
      description: product.description || "",
    })
    setProductModal(true)
  }

  const handleDeleteProduct = (product) => {
    setSelectedProduct(product)
    setDeleteDialog(true)
  }

  const handleViewProduct = (product) => {
    toast.info(`عرض تفاصيل: ${product.name}`)
  }

  const handleSubmitProduct = (e) => {
    e.preventDefault()
    setIsLoading(true)

    setTimeout(() => {
      if (selectedProduct) {
        // Edit
        setProducts((prev) =>
          prev.map((p) =>
            p.id === selectedProduct.id
              ? {
                  ...p,
                  ...formData,
                  costPrice: Number(formData.costPrice),
                  sellPrice: Number(formData.sellPrice),
                  quantity: Number(formData.quantity),
                  minStock: Number(formData.minStock),
                  status:
                    Number(formData.quantity) === 0
                      ? "نفذ"
                      : Number(formData.quantity) <= Number(formData.minStock)
                      ? "منخفض"
                      : "متوفر",
                }
              : p
          )
        )
        toast.success("تم تحديث المنتج بنجاح!")
      } else {
        // Add
        const newProduct = {
          id: products.length + 1,
          ...formData,
          costPrice: Number(formData.costPrice),
          sellPrice: Number(formData.sellPrice),
          quantity: Number(formData.quantity),
          minStock: Number(formData.minStock),
          status:
            Number(formData.quantity) === 0
              ? "نفذ"
              : Number(formData.quantity) <= Number(formData.minStock)
              ? "منخفض"
              : "متوفر",
        }
        setProducts((prev) => [...prev, newProduct])
        toast.success("تم إضافة المنتج بنجاح!")
      }

      setIsLoading(false)
      setProductModal(false)
    }, 1000)
  }

  const confirmDelete = () => {
    setProducts((prev) => prev.filter((p) => p.id !== selectedProduct.id))
    toast.success("تم حذف المنتج بنجاح!")
    setDeleteDialog(false)
    setSelectedProduct(null)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">
          إدارة المخزون
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          إدارة المنتجات والمخازن وحركات المخزون
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="إجمالي المنتجات"
          value={totalProducts}
          icon={Package}
          color="blue"
          delay={0}
        />
        <StatsCard
          title="قيمة المخزون"
          value={totalValue}
          format="currency"
          icon={DollarSign}
          color="emerald"
          delay={0.1}
        />
        <StatsCard
          title="مخزون منخفض"
          value={lowStockCount}
          icon={TrendingDown}
          color="amber"
          delay={0.2}
        />
        <StatsCard
          title="نفذ من المخزون"
          value={outOfStockCount}
          icon={AlertTriangle}
          color="red"
          delay={0.3}
        />
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800">
          <TabsTrigger value="products" className="gap-2">
            <Package className="w-4 h-4" />
            المنتجات
          </TabsTrigger>
          <TabsTrigger value="warehouses" className="gap-2">
            <Warehouse className="w-4 h-4" />
            المخازن
          </TabsTrigger>
          <TabsTrigger value="movements" className="gap-2">
            <ArrowRightLeft className="w-4 h-4" />
            الحركات
          </TabsTrigger>
          <TabsTrigger value="reports" className="gap-2">
            <FileText className="w-4 h-4" />
            التقارير
          </TabsTrigger>
        </TabsList>

        {/* Products Tab */}
        <TabsContent value="products" className="mt-6">
          <DataTable
            data={products}
            columns={productColumns}
            searchKey="name"
            searchPlaceholder="البحث عن منتج..."
            addButtonText="إضافة منتج"
            onAdd={handleAddProduct}
            onEdit={handleEditProduct}
            onDelete={handleDeleteProduct}
            onView={handleViewProduct}
            onRefresh={() => toast.info("تم تحديث البيانات")}
            onExport={() => toast.info("جاري التصدير...")}
          />
        </TabsContent>

        {/* Warehouses Tab */}
        <TabsContent value="warehouses" className="mt-6">
          <DataTable
            data={warehouses}
            columns={warehouseColumns}
            searchKey="name"
            searchPlaceholder="البحث عن مخزن..."
            addButtonText="إضافة مخزن"
            onAdd={() => toast.info("إضافة مخزن جديد")}
            onEdit={(row) => toast.info(`تعديل: ${row.name}`)}
            onView={(row) => toast.info(`عرض: ${row.name}`)}
            showSelection={false}
          />
        </TabsContent>

        {/* Movements Tab */}
        <TabsContent value="movements" className="mt-6">
          <DataTable
            data={movements}
            columns={movementColumns}
            searchKey="product"
            searchPlaceholder="البحث عن حركة..."
            addButtonText="إضافة حركة"
            onAdd={() => toast.info("إضافة حركة جديدة")}
            onView={(row) => toast.info(`عرض: ${row.reference}`)}
            showSelection={false}
          />
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { title: "تقرير المخزون الحالي", icon: Package, color: "blue" },
              { title: "تقرير المنتجات المنخفضة", icon: TrendingDown, color: "amber" },
              { title: "تقرير حركات المخزون", icon: ArrowRightLeft, color: "purple" },
              { title: "تقرير قيمة المخزون", icon: DollarSign, color: "emerald" },
              { title: "تقرير المخازن", icon: Warehouse, color: "cyan" },
              { title: "تقرير تحليلي", icon: FileText, color: "orange" },
            ].map((report, index) => (
              <motion.div
                key={report.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="cursor-pointer hover:shadow-lg transition-shadow">
                  <CardContent className="p-6 flex items-center gap-4">
                    <div className={`p-3 rounded-xl bg-${report.color}-100 dark:bg-${report.color}-900/30`}>
                      <report.icon className={`w-6 h-6 text-${report.color}-600`} />
                    </div>
                    <div>
                      <h3 className="font-medium">{report.title}</h3>
                      <p className="text-sm text-muted-foreground">تصدير PDF / Excel</p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Product Form Modal */}
      <FormModal
        open={productModal}
        onOpenChange={setProductModal}
        title={selectedProduct ? "تعديل المنتج" : "إضافة منتج جديد"}
        description={selectedProduct ? "قم بتعديل بيانات المنتج" : "أدخل بيانات المنتج الجديد"}
        onSubmit={handleSubmitProduct}
        isLoading={isLoading}
        size="xl"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="sku">الرمز التعريفي</Label>
            <div className="relative">
              <Barcode className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="sku"
                value={formData.sku}
                onChange={(e) => setFormData({ ...formData, sku: e.target.value })}
                className="pr-9"
                disabled
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="name">اسم المنتج *</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="أدخل اسم المنتج"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="category">الفئة *</Label>
            <Select
              value={formData.category}
              onValueChange={(value) => setFormData({ ...formData, category: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="اختر الفئة" />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="unit">وحدة القياس *</Label>
            <Select
              value={formData.unit}
              onValueChange={(value) => setFormData({ ...formData, unit: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="اختر الوحدة" />
              </SelectTrigger>
              <SelectContent>
                {units.map((unit) => (
                  <SelectItem key={unit} value={unit}>
                    {unit}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="costPrice">سعر التكلفة *</Label>
            <div className="relative">
              <DollarSign className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="costPrice"
                type="number"
                value={formData.costPrice}
                onChange={(e) => setFormData({ ...formData, costPrice: e.target.value })}
                className="pr-9"
                placeholder="0.00"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="sellPrice">سعر البيع *</Label>
            <div className="relative">
              <Tag className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="sellPrice"
                type="number"
                value={formData.sellPrice}
                onChange={(e) => setFormData({ ...formData, sellPrice: e.target.value })}
                className="pr-9"
                placeholder="0.00"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="quantity">الكمية *</Label>
            <div className="relative">
              <Box className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <Input
                id="quantity"
                type="number"
                value={formData.quantity}
                onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                className="pr-9"
                placeholder="0"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="minStock">الحد الأدنى *</Label>
            <Input
              id="minStock"
              type="number"
              value={formData.minStock}
              onChange={(e) => setFormData({ ...formData, minStock: e.target.value })}
              placeholder="0"
              required
            />
          </div>

          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="warehouse">المخزن *</Label>
            <Select
              value={formData.warehouse}
              onValueChange={(value) => setFormData({ ...formData, warehouse: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="اختر المخزن" />
              </SelectTrigger>
              <SelectContent>
                {warehouses.map((wh) => (
                  <SelectItem key={wh.id} value={wh.name}>
                    {wh.name} - {wh.location}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="description">الوصف</Label>
            <Textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="وصف المنتج (اختياري)"
              rows={3}
            />
          </div>
        </div>
      </FormModal>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialog} onOpenChange={setDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>تأكيد الحذف</AlertDialogTitle>
            <AlertDialogDescription>
              هل أنت متأكد من حذف المنتج "{selectedProduct?.name}"؟ لا يمكن التراجع عن هذا الإجراء.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>إلغاء</AlertDialogCancel>
            <AlertDialogAction
              onClick={confirmDelete}
              className="bg-red-600 hover:bg-red-700"
            >
              حذف
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}

export default InventoryManagement
