/**
 * Nurseries Management Page - إدارة المشاتل
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Sprout,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Thermometer,
  Droplets,
  Sun,
  Leaf,
  MapPin,
  Package,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
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
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

const mockNurseries = [
  { id: 1, name: "مشتل الشتلات الرئيسي", type: "seedlings", location: "القسم الشرقي", capacity: 10000, current: 7500, temperature: 25, humidity: 70, status: "active", plants: ["طماطم", "فلفل", "باذنجان"] },
  { id: 2, name: "مشتل أشجار الفاكهة", type: "fruit_trees", location: "القسم الغربي", capacity: 5000, current: 3200, temperature: 22, humidity: 65, status: "active", plants: ["تفاح", "برتقال", "ليمون"] },
  { id: 3, name: "مشتل النباتات الزينة", type: "ornamental", location: "البيت الزجاجي", capacity: 8000, current: 6800, temperature: 24, humidity: 75, status: "active", plants: ["ورد", "ياسمين", "لافندر"] },
  { id: 4, name: "مشتل التكاثر", type: "propagation", location: "القسم الجنوبي", capacity: 3000, current: 1500, temperature: 28, humidity: 80, status: "maintenance", plants: ["عقل خضرية", "تطعيم"] },
]

const typeConfig = {
  seedlings: { label: "شتلات", color: "default" },
  fruit_trees: { label: "أشجار فاكهة", color: "secondary" },
  ornamental: { label: "نباتات زينة", color: "outline" },
  propagation: { label: "إكثار", color: "default" },
}

const NurseriesPage = () => {
  const [nurseries, setNurseries] = useState(mockNurseries)
  const [searchQuery, setSearchQuery] = useState("")
  const [typeFilter, setTypeFilter] = useState("all")

  const filteredNurseries = nurseries.filter(n => {
    const matchesSearch = n.name.includes(searchQuery) || n.location.includes(searchQuery)
    const matchesType = typeFilter === "all" || n.type === typeFilter
    return matchesSearch && matchesType
  })

  const stats = {
    total: nurseries.length,
    totalCapacity: nurseries.reduce((sum, n) => sum + n.capacity, 0),
    totalCurrent: nurseries.reduce((sum, n) => sum + n.current, 0),
    active: nurseries.filter(n => n.status === "active").length,
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Sprout className="w-7 h-7 text-green-500" />
            إدارة المشاتل
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة ومتابعة المشاتل والشتلات</p>
        </div>
        <Button onClick={() => toast.info("قريباً...")}>
          <Plus className="w-4 h-4 ml-2" />
          مشتل جديد
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Sprout className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">مشتل</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Package className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalCapacity.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">السعة الكلية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
              <Leaf className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalCurrent.toLocaleString()}</p>
              <p className="text-sm text-muted-foreground">النباتات الحالية</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Sun className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{Math.round((stats.totalCurrent / stats.totalCapacity) * 100)}%</p>
              <p className="text-sm text-muted-foreground">نسبة الإشغال</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input placeholder="بحث..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pr-10" />
            </div>
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-[150px]"><SelectValue placeholder="النوع" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الأنواع</SelectItem>
                <SelectItem value="seedlings">شتلات</SelectItem>
                <SelectItem value="fruit_trees">أشجار فاكهة</SelectItem>
                <SelectItem value="ornamental">نباتات زينة</SelectItem>
                <SelectItem value="propagation">إكثار</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredNurseries.map(nursery => (
          <Card key={nursery.id} className="overflow-hidden">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                    nursery.status === "active" ? "bg-green-100 dark:bg-green-900" : "bg-yellow-100 dark:bg-yellow-900"
                  }`}>
                    <Sprout className={`w-6 h-6 ${nursery.status === "active" ? "text-green-600" : "text-yellow-600"}`} />
                  </div>
                  <div>
                    <CardTitle className="text-lg">{nursery.name}</CardTitle>
                    <p className="text-sm text-muted-foreground flex items-center gap-1">
                      <MapPin className="w-3 h-3" />
                      {nursery.location}
                    </p>
                  </div>
                </div>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="sm"><MoreVertical className="w-4 h-4" /></Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem><Eye className="w-4 h-4 ml-2" />عرض</DropdownMenuItem>
                    <DropdownMenuItem><Edit className="w-4 h-4 ml-2" />تعديل</DropdownMenuItem>
                    <DropdownMenuItem className="text-red-600"><Trash2 className="w-4 h-4 ml-2" />حذف</DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-2 flex-wrap">
                <Badge variant={typeConfig[nursery.type].color}>{typeConfig[nursery.type].label}</Badge>
                <Badge variant={nursery.status === "active" ? "default" : "secondary"}>
                  {nursery.status === "active" ? "نشط" : "صيانة"}
                </Badge>
              </div>
              
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span>الإشغال</span>
                  <span>{nursery.current.toLocaleString()} / {nursery.capacity.toLocaleString()}</span>
                </div>
                <Progress value={(nursery.current / nursery.capacity) * 100} className="h-2" />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="flex items-center gap-2 p-2 bg-muted rounded-lg">
                  <Thermometer className="w-4 h-4 text-red-500" />
                  <span className="text-sm">{nursery.temperature}°C</span>
                </div>
                <div className="flex items-center gap-2 p-2 bg-muted rounded-lg">
                  <Droplets className="w-4 h-4 text-blue-500" />
                  <span className="text-sm">{nursery.humidity}%</span>
                </div>
              </div>

              <div>
                <p className="text-sm text-muted-foreground mb-2">النباتات:</p>
                <div className="flex gap-1 flex-wrap">
                  {nursery.plants.map((plant, i) => (
                    <Badge key={i} variant="outline" className="text-xs">{plant}</Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

export default NurseriesPage
