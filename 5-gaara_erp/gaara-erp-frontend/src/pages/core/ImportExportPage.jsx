/**
 * Import/Export Page - استيراد وتصدير البيانات
 * Gaara ERP v12
 */

import { useState, useEffect } from "react"
import { toast } from "sonner"
import {
  FileDown,
  FileUp,
  FileSpreadsheet,
  FileText,
  Download,
  Upload,
  Check,
  X,
  AlertTriangle,
  RefreshCw,
  Clock,
  HardDrive,
  Loader2,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Checkbox } from "@/components/ui/checkbox"

import { DataTable } from "@/components/common"
import { formatDate, formatFileSize } from "@/lib/utils"

// Mock history data
const mockHistory = [
  {
    id: 1,
    type: "export",
    module: "beneficiaries",
    module_ar: "المستفيدين",
    format: "xlsx",
    records: 1500,
    file_size: 2500000,
    status: "completed",
    created_by: "أحمد محمد",
    created_at: "2026-01-16T10:30:00Z",
  },
  {
    id: 2,
    type: "import",
    module: "products",
    module_ar: "المنتجات",
    format: "csv",
    records: 500,
    file_size: 150000,
    status: "completed",
    created_by: "سارة أحمد",
    created_at: "2026-01-15T14:00:00Z",
  },
  {
    id: 3,
    type: "export",
    module: "transactions",
    module_ar: "المعاملات",
    format: "xlsx",
    records: 10000,
    file_size: 8500000,
    status: "failed",
    error: "نفاد الذاكرة",
    created_by: "محمد علي",
    created_at: "2026-01-14T09:00:00Z",
  },
]

const ImportExportPage = () => {
  const [activeTab, setActiveTab] = useState("export")
  const [history, setHistory] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  
  // Export settings
  const [exportModule, setExportModule] = useState("")
  const [exportFormat, setExportFormat] = useState("xlsx")
  const [selectedFields, setSelectedFields] = useState([])
  
  // Import settings
  const [importModule, setImportModule] = useState("")
  const [importFile, setImportFile] = useState(null)
  const [importPreview, setImportPreview] = useState(null)

  const modules = [
    { id: "companies", name: "الشركات" },
    { id: "users", name: "المستخدمين" },
    { id: "products", name: "المنتجات" },
    { id: "beneficiaries", name: "المستفيدين" },
    { id: "transactions", name: "المعاملات" },
    { id: "inventory", name: "المخزون" },
    { id: "farms", name: "المزارع" },
  ]

  const moduleFields = {
    companies: ["الاسم", "الكود", "الهاتف", "البريد", "المدينة", "الحالة"],
    users: ["الاسم", "البريد", "الدور", "القسم", "الحالة"],
    products: ["الاسم", "الكود", "السعر", "الكمية", "الفئة"],
    beneficiaries: ["الاسم", "رقم الهوية", "الهاتف", "الفئة", "الحالة"],
    transactions: ["التاريخ", "المبلغ", "النوع", "المرجع", "الحالة"],
    inventory: ["المنتج", "الكمية", "المستودع", "الموقع"],
    farms: ["الاسم", "الموقع", "المساحة", "الحالة"],
  }

  useEffect(() => {
    loadHistory()
    if (exportModule && moduleFields[exportModule]) {
      setSelectedFields(moduleFields[exportModule])
    }
  }, [exportModule])

  const loadHistory = async () => {
    setIsLoading(true)
    try {
      await new Promise((resolve) => setTimeout(resolve, 500))
      setHistory(mockHistory)
    } catch (error) {
      toast.error("فشل تحميل السجل")
    } finally {
      setIsLoading(false)
    }
  }

  const handleExport = async () => {
    if (!exportModule) {
      toast.error("يرجى اختيار الوحدة")
      return
    }
    
    setIsProcessing(true)
    setProgress(0)
    
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 20
      })
    }, 500)
    
    setTimeout(() => {
      setIsProcessing(false)
      setProgress(0)
      toast.success("تم تصدير البيانات بنجاح")
      loadHistory()
    }, 3000)
  }

  const handleImport = async () => {
    if (!importModule || !importFile) {
      toast.error("يرجى اختيار الوحدة والملف")
      return
    }
    
    setIsProcessing(true)
    setProgress(0)
    
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 15
      })
    }, 500)
    
    setTimeout(() => {
      setIsProcessing(false)
      setProgress(0)
      setImportFile(null)
      setImportPreview(null)
      toast.success("تم استيراد البيانات بنجاح")
      loadHistory()
    }, 4000)
  }

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImportFile(file)
      // Simulate preview
      setImportPreview({
        rows: 150,
        columns: 6,
        valid: 145,
        errors: 5,
      })
    }
  }

  const handleDownloadTemplate = () => {
    if (!exportModule) {
      toast.error("يرجى اختيار الوحدة أولاً")
      return
    }
    toast.success("جاري تحميل القالب...")
  }

  const toggleField = (field) => {
    setSelectedFields(prev => 
      prev.includes(field) 
        ? prev.filter(f => f !== field)
        : [...prev, field]
    )
  }

  const historyColumns = [
    {
      accessorKey: "type",
      header: "النوع",
      cell: ({ row }) => {
        const type = row.original.type
        return (
          <div className="flex items-center gap-2">
            {type === "export" ? (
              <FileDown className="w-4 h-4 text-blue-500" />
            ) : (
              <FileUp className="w-4 h-4 text-green-500" />
            )}
            <span>{type === "export" ? "تصدير" : "استيراد"}</span>
          </div>
        )
      },
    },
    {
      accessorKey: "module_ar",
      header: "الوحدة",
    },
    {
      accessorKey: "format",
      header: "الصيغة",
      cell: ({ row }) => (
        <Badge variant="outline">{row.original.format.toUpperCase()}</Badge>
      ),
    },
    {
      accessorKey: "records",
      header: "السجلات",
      cell: ({ row }) => row.original.records?.toLocaleString() || "-",
    },
    {
      accessorKey: "file_size",
      header: "الحجم",
      cell: ({ row }) => formatFileSize(row.original.file_size),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const status = row.original.status
        return (
          <Badge variant={status === "completed" ? "default" : "destructive"}>
            {status === "completed" ? (
              <Check className="w-3 h-3 ml-1" />
            ) : (
              <X className="w-3 h-3 ml-1" />
            )}
            {status === "completed" ? "مكتمل" : "فشل"}
          </Badge>
        )
      },
    },
    {
      accessorKey: "created_at",
      header: "التاريخ",
      cell: ({ row }) => (
        <div className="flex items-center gap-1 text-muted-foreground">
          <Clock className="w-3 h-3" />
          {formatDate(row.original.created_at, "PPp")}
        </div>
      ),
    },
    {
      accessorKey: "created_by",
      header: "بواسطة",
    },
  ]

  // Stats
  const stats = {
    totalExports: history.filter(h => h.type === "export").length,
    totalImports: history.filter(h => h.type === "import").length,
    successRate: Math.round((history.filter(h => h.status === "completed").length / history.length) * 100) || 0,
    totalRecords: history.reduce((sum, h) => sum + (h.records || 0), 0),
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <FileSpreadsheet className="w-7 h-7 text-emerald-500" />
            استيراد وتصدير البيانات
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            استيراد وتصدير البيانات بصيغ مختلفة
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <FileDown className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalExports}</p>
              <p className="text-sm text-muted-foreground">عمليات تصدير</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <FileUp className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalImports}</p>
              <p className="text-sm text-muted-foreground">عمليات استيراد</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Check className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.successRate}%</p>
              <p className="text-sm text-muted-foreground">نسبة النجاح</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <HardDrive className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalRecords.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">سجل</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="export" className="gap-2">
            <FileDown className="w-4 h-4" />
            تصدير البيانات
          </TabsTrigger>
          <TabsTrigger value="import" className="gap-2">
            <FileUp className="w-4 h-4" />
            استيراد البيانات
          </TabsTrigger>
          <TabsTrigger value="history" className="gap-2">
            <Clock className="w-4 h-4" />
            السجل
          </TabsTrigger>
        </TabsList>

        {/* Export Tab */}
        <TabsContent value="export">
          <Card>
            <CardHeader>
              <CardTitle>تصدير البيانات</CardTitle>
              <CardDescription>اختر الوحدة والصيغة لتصدير البيانات</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>الوحدة</Label>
                  <Select value={exportModule} onValueChange={setExportModule}>
                    <SelectTrigger>
                      <SelectValue placeholder="اختر الوحدة" />
                    </SelectTrigger>
                    <SelectContent>
                      {modules.map((module) => (
                        <SelectItem key={module.id} value={module.id}>
                          {module.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>صيغة الملف</Label>
                  <Select value={exportFormat} onValueChange={setExportFormat}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="xlsx">Excel (.xlsx)</SelectItem>
                      <SelectItem value="csv">CSV (.csv)</SelectItem>
                      <SelectItem value="json">JSON (.json)</SelectItem>
                      <SelectItem value="pdf">PDF (.pdf)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {exportModule && moduleFields[exportModule] && (
                <>
                  <Separator />
                  <div>
                    <Label className="mb-3 block">الحقول المراد تصديرها</Label>
                    <div className="grid grid-cols-3 md:grid-cols-6 gap-2">
                      {moduleFields[exportModule].map((field) => (
                        <div
                          key={field}
                          className={`flex items-center space-x-2 space-x-reverse p-2 rounded-lg border cursor-pointer ${
                            selectedFields.includes(field)
                              ? "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800"
                              : "hover:bg-muted"
                          }`}
                          onClick={() => toggleField(field)}
                        >
                          <Checkbox
                            checked={selectedFields.includes(field)}
                            onCheckedChange={() => toggleField(field)}
                          />
                          <span className="text-sm">{field}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {isProcessing && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>جاري التصدير...</span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} />
                </div>
              )}

              <div className="flex gap-3">
                <Button onClick={handleExport} disabled={isProcessing || !exportModule}>
                  {isProcessing ? (
                    <Loader2 className="w-4 h-4 ml-2 animate-spin" />
                  ) : (
                    <Download className="w-4 h-4 ml-2" />
                  )}
                  تصدير
                </Button>
                <Button variant="outline" onClick={handleDownloadTemplate}>
                  <FileText className="w-4 h-4 ml-2" />
                  تحميل القالب
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Import Tab */}
        <TabsContent value="import">
          <Card>
            <CardHeader>
              <CardTitle>استيراد البيانات</CardTitle>
              <CardDescription>رفع ملف لاستيراد البيانات</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>الوحدة</Label>
                  <Select value={importModule} onValueChange={setImportModule}>
                    <SelectTrigger>
                      <SelectValue placeholder="اختر الوحدة" />
                    </SelectTrigger>
                    <SelectContent>
                      {modules.map((module) => (
                        <SelectItem key={module.id} value={module.id}>
                          {module.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>الملف</Label>
                  <div className="flex gap-2">
                    <input
                      type="file"
                      id="import-file"
                      accept=".xlsx,.csv,.json"
                      onChange={handleFileSelect}
                      className="hidden"
                    />
                    <Button
                      variant="outline"
                      className="w-full"
                      onClick={() => document.getElementById("import-file").click()}
                    >
                      <Upload className="w-4 h-4 ml-2" />
                      {importFile ? importFile.name : "اختر ملف"}
                    </Button>
                  </div>
                </div>
              </div>

              {importPreview && (
                <>
                  <Separator />
                  <div className="p-4 bg-muted rounded-lg">
                    <h4 className="font-medium mb-3">معاينة الملف</h4>
                    <div className="grid grid-cols-4 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">إجمالي الصفوف</p>
                        <p className="font-bold text-lg">{importPreview.rows}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">الأعمدة</p>
                        <p className="font-bold text-lg">{importPreview.columns}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">صفوف صالحة</p>
                        <p className="font-bold text-lg text-green-600">{importPreview.valid}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">صفوف بأخطاء</p>
                        <p className="font-bold text-lg text-red-600">{importPreview.errors}</p>
                      </div>
                    </div>
                    {importPreview.errors > 0 && (
                      <div className="mt-3 p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded border border-yellow-200 dark:border-yellow-800 flex items-center gap-2">
                        <AlertTriangle className="w-4 h-4 text-yellow-600" />
                        <span className="text-sm">يوجد {importPreview.errors} صف به أخطاء سيتم تجاهلها</span>
                      </div>
                    )}
                  </div>
                </>
              )}

              {isProcessing && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>جاري الاستيراد...</span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} />
                </div>
              )}

              <div className="flex gap-3">
                <Button onClick={handleImport} disabled={isProcessing || !importModule || !importFile}>
                  {isProcessing ? (
                    <Loader2 className="w-4 h-4 ml-2 animate-spin" />
                  ) : (
                    <Upload className="w-4 h-4 ml-2" />
                  )}
                  استيراد
                </Button>
                <Button variant="outline" onClick={handleDownloadTemplate}>
                  <FileText className="w-4 h-4 ml-2" />
                  تحميل قالب فارغ
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* History Tab */}
        <TabsContent value="history">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>سجل العمليات</CardTitle>
                  <CardDescription>جميع عمليات الاستيراد والتصدير</CardDescription>
                </div>
                <Button variant="outline" onClick={loadHistory}>
                  <RefreshCw className="w-4 h-4 ml-2" />
                  تحديث
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <DataTable
                columns={historyColumns}
                data={history}
                isLoading={isLoading}
                searchKey="module_ar"
                defaultPageSize={10}
              />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ImportExportPage
