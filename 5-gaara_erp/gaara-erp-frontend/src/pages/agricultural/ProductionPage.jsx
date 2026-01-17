/**
 * Agricultural Production Page - الإنتاج الزراعي
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Factory,
  Plus,
  Search,
  BarChart3,
  TrendingUp,
  Package,
  Leaf,
  Calendar,
  CheckCircle2,
  Clock,
  AlertTriangle,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const mockProduction = [
  { id: 1, crop: "قمح", variety: "سخا 94", area: 150, expectedYield: 600, actualYield: 585, unit: "طن", season: "شتوي 2025", status: "harvested" },
  { id: 2, crop: "طماطم", variety: "هجين 1", area: 25, expectedYield: 125, actualYield: 0, unit: "طن", season: "صيفي 2026", status: "growing" },
  { id: 3, crop: "برتقال", variety: "واشنطن نافل", area: 80, expectedYield: 400, actualYield: 380, unit: "طن", season: "2025", status: "harvesting" },
  { id: 4, crop: "ذرة", variety: "هجين 10", area: 200, expectedYield: 1200, actualYield: 0, unit: "طن", season: "صيفي 2026", status: "planted" },
  { id: 5, crop: "بطاطس", variety: "سبونتا", area: 50, expectedYield: 200, actualYield: 195, unit: "طن", season: "نيلي 2025", status: "harvested" },
]

const statusConfig = {
  planted: { label: "مزروع", variant: "secondary", icon: Leaf },
  growing: { label: "ينمو", variant: "default", icon: TrendingUp },
  harvesting: { label: "جاري الحصاد", variant: "default", icon: Factory },
  harvested: { label: "تم الحصاد", variant: "default", icon: CheckCircle2 },
}

const ProductionPage = () => {
  const [production, setProduction] = useState(mockProduction)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [activeTab, setActiveTab] = useState("overview")

  const filteredProduction = production.filter(p => {
    const matchesSearch = p.crop.includes(searchQuery) || p.variety.includes(searchQuery)
    const matchesStatus = statusFilter === "all" || p.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const stats = {
    totalArea: production.reduce((sum, p) => sum + p.area, 0),
    expectedYield: production.reduce((sum, p) => sum + p.expectedYield, 0),
    actualYield: production.reduce((sum, p) => sum + p.actualYield, 0),
    crops: new Set(production.map(p => p.crop)).size,
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Factory className="w-7 h-7 text-amber-500" />
            الإنتاج الزراعي
          </h1>
          <p className="text-slate-600 dark:text-slate-400">متابعة وإدارة الإنتاج الزراعي</p>
        </div>
        <Button onClick={() => toast.info("قريباً...")}>
          <Plus className="w-4 h-4 ml-2" />
          إضافة إنتاج
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Leaf className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.crops}</p>
              <p className="text-sm text-muted-foreground">محصول</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalArea}</p>
              <p className="text-sm text-muted-foreground">فدان</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900 flex items-center justify-center">
              <Package className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.expectedYield.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">طن (متوقع)</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.actualYield.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">طن (فعلي)</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview">نظرة عامة</TabsTrigger>
          <TabsTrigger value="details">التفاصيل</TabsTrigger>
          <TabsTrigger value="analytics">التحليلات</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <Card>
            <CardContent className="p-4">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[150px]"><SelectValue placeholder="الحالة" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">جميع الحالات</SelectItem>
                    <SelectItem value="planted">مزروع</SelectItem>
                    <SelectItem value="growing">ينمو</SelectItem>
                    <SelectItem value="harvesting">جاري الحصاد</SelectItem>
                    <SelectItem value="harvested">تم الحصاد</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>سجل الإنتاج</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>المحصول</TableHead>
                    <TableHead>الصنف</TableHead>
                    <TableHead>المساحة</TableHead>
                    <TableHead>الموسم</TableHead>
                    <TableHead>المتوقع</TableHead>
                    <TableHead>الفعلي</TableHead>
                    <TableHead>التحقيق</TableHead>
                    <TableHead>الحالة</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredProduction.map(item => {
                    const config = statusConfig[item.status]
                    const Icon = config.icon
                    const achievement = item.actualYield > 0 ? Math.round((item.actualYield / item.expectedYield) * 100) : 0
                    return (
                      <TableRow key={item.id}>
                        <TableCell className="font-medium">{item.crop}</TableCell>
                        <TableCell>{item.variety}</TableCell>
                        <TableCell>{item.area} فدان</TableCell>
                        <TableCell>{item.season}</TableCell>
                        <TableCell>{item.expectedYield} {item.unit}</TableCell>
                        <TableCell>{item.actualYield > 0 ? `${item.actualYield} ${item.unit}` : "-"}</TableCell>
                        <TableCell>
                          {item.actualYield > 0 ? (
                            <div className="flex items-center gap-2">
                              <Progress value={achievement} className="w-16 h-2" />
                              <span className="text-sm">{achievement}%</span>
                            </div>
                          ) : "-"}
                        </TableCell>
                        <TableCell>
                          <Badge variant={config.variant}>
                            <Icon className="w-3 h-3 ml-1" />
                            {config.label}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="details">
          <Card>
            <CardContent className="p-6 text-center text-muted-foreground">
              <BarChart3 className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>تفاصيل الإنتاج التفصيلية</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics">
          <Card>
            <CardContent className="p-6 text-center text-muted-foreground">
              <TrendingUp className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>تحليلات الإنتاج</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ProductionPage
