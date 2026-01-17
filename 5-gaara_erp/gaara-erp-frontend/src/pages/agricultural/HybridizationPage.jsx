/**
 * Seed Hybridization Page - تهجين البذور
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  Dna,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Leaf,
  Calendar,
  CheckCircle2,
  Clock,
  ArrowRight,
  Beaker,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
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

const mockHybridizations = [
  { id: 1, name: "هجين قمح 2026-A", parent1: "قمح سخا 94", parent2: "قمح جميزة 11", crop: "قمح", startDate: "2025-06-01", generation: "F3", status: "in_progress", progress: 65, traits: ["مقاومة الجفاف", "إنتاجية عالية"] },
  { id: 2, name: "هجين طماطم TH-5", parent1: "طماطم بوتنزا", parent2: "طماطم برايد", crop: "طماطم", startDate: "2025-09-15", generation: "F2", status: "in_progress", progress: 40, traits: ["مقاومة الأمراض", "تحمل الحرارة"] },
  { id: 3, name: "هجين ذرة MC-10", parent1: "ذرة هجين 128", parent2: "ذرة هجين 306", crop: "ذرة", startDate: "2024-03-01", generation: "F5", status: "completed", progress: 100, traits: ["حبوب كبيرة", "نضج مبكر"] },
  { id: 4, name: "هجين فلفل PH-3", parent1: "فلفل كاليفورنيا", parent2: "فلفل هالابينو", crop: "فلفل", startDate: "2025-11-01", generation: "F1", status: "planned", progress: 0, traits: ["طعم مميز", "ثمار كبيرة"] },
]

const statusConfig = {
  planned: { label: "مخطط", variant: "secondary", icon: Calendar },
  in_progress: { label: "قيد التنفيذ", variant: "default", icon: Clock },
  completed: { label: "مكتمل", variant: "default", icon: CheckCircle2 },
}

const HybridizationPage = () => {
  const [hybridizations, setHybridizations] = useState(mockHybridizations)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  const filteredHybridizations = hybridizations.filter(h => {
    const matchesSearch = h.name.includes(searchQuery) || h.crop.includes(searchQuery)
    const matchesStatus = statusFilter === "all" || h.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const stats = {
    total: hybridizations.length,
    inProgress: hybridizations.filter(h => h.status === "in_progress").length,
    completed: hybridizations.filter(h => h.status === "completed").length,
    planned: hybridizations.filter(h => h.status === "planned").length,
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <Dna className="w-7 h-7 text-purple-500" />
            تهجين البذور
          </h1>
          <p className="text-slate-600 dark:text-slate-400">برامج تهجين وتحسين الأصناف النباتية</p>
        </div>
        <Button onClick={() => toast.info("قريباً...")}>
          <Plus className="w-4 h-4 ml-2" />
          برنامج تهجين جديد
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Dna className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">برنامج تهجين</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Beaker className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.inProgress}</p>
              <p className="text-sm text-muted-foreground">قيد التنفيذ</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.completed}</p>
              <p className="text-sm text-muted-foreground">مكتمل</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Calendar className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.planned}</p>
              <p className="text-sm text-muted-foreground">مخطط</p>
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
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[150px]"><SelectValue placeholder="الحالة" /></SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الحالات</SelectItem>
                <SelectItem value="planned">مخطط</SelectItem>
                <SelectItem value="in_progress">قيد التنفيذ</SelectItem>
                <SelectItem value="completed">مكتمل</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredHybridizations.map(hybrid => {
          const config = statusConfig[hybrid.status]
          const StatusIcon = config.icon
          return (
            <Card key={hybrid.id} className="overflow-hidden">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                      hybrid.status === "completed" ? "bg-green-100 dark:bg-green-900" :
                      hybrid.status === "in_progress" ? "bg-blue-100 dark:bg-blue-900" :
                      "bg-yellow-100 dark:bg-yellow-900"
                    }`}>
                      <Dna className={`w-6 h-6 ${
                        hybrid.status === "completed" ? "text-green-600" :
                        hybrid.status === "in_progress" ? "text-blue-600" :
                        "text-yellow-600"
                      }`} />
                    </div>
                    <div>
                      <CardTitle className="text-lg">{hybrid.name}</CardTitle>
                      <p className="text-sm text-muted-foreground flex items-center gap-1">
                        <Leaf className="w-3 h-3" />
                        {hybrid.crop} • {hybrid.generation}
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
                <div className="flex items-center justify-between gap-2 p-3 bg-muted rounded-lg text-sm">
                  <span className="font-medium truncate">{hybrid.parent1}</span>
                  <ArrowRight className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                  <span className="font-medium truncate">{hybrid.parent2}</span>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>التقدم</span>
                    <span>{hybrid.progress}%</span>
                  </div>
                  <Progress value={hybrid.progress} className="h-2" />
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex gap-1 flex-wrap">
                    {hybrid.traits.map((trait, i) => (
                      <Badge key={i} variant="outline" className="text-xs">{trait}</Badge>
                    ))}
                  </div>
                  <Badge variant={config.variant}>
                    <StatusIcon className="w-3 h-3 ml-1" />
                    {config.label}
                  </Badge>
                </div>

                <p className="text-xs text-muted-foreground">
                  بدأ في: {hybrid.startDate}
                </p>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}

export default HybridizationPage
