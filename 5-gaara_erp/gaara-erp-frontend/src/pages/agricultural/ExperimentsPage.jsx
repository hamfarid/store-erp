/**
 * Agricultural Experiments Page - التجارب الزراعية
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  FlaskConical,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  Calendar,
  CheckCircle2,
  Clock,
  AlertTriangle,
  Beaker,
  Leaf,
  MapPin,
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
import { DataTable } from "@/components/common"

const mockExperiments = [
  { id: 1, name: "تجربة مقارنة أصناف القمح", type: "variety_trial", crop: "قمح", location: "المزرعة الشمالية", startDate: "2025-10-01", endDate: "2026-03-01", status: "in_progress", progress: 65, researcher: "د. أحمد محمد" },
  { id: 2, name: "اختبار أسمدة عضوية", type: "fertilizer", crop: "طماطم", location: "البيت المحمي 3", startDate: "2025-11-15", endDate: "2026-02-15", status: "in_progress", progress: 45, researcher: "م. سارة أحمد" },
  { id: 3, name: "مقاومة الآفات الحشرية", type: "pest_resistance", crop: "ذرة", location: "القطاع الجنوبي", startDate: "2025-09-01", endDate: "2025-12-31", status: "completed", progress: 100, researcher: "د. محمد علي" },
  { id: 4, name: "كفاءة الري بالتنقيط", type: "irrigation", crop: "خيار", location: "البيت المحمي 1", startDate: "2026-01-01", endDate: "2026-04-01", status: "pending", progress: 0, researcher: "م. فاطمة خالد" },
]

const typeConfig = {
  variety_trial: { label: "تجربة أصناف", color: "default" },
  fertilizer: { label: "اختبار أسمدة", color: "secondary" },
  pest_resistance: { label: "مقاومة آفات", color: "outline" },
  irrigation: { label: "نظام ري", color: "default" },
}

const statusConfig = {
  pending: { label: "قيد الانتظار", variant: "secondary", icon: Clock },
  in_progress: { label: "قيد التنفيذ", variant: "default", icon: FlaskConical },
  completed: { label: "مكتمل", variant: "default", icon: CheckCircle2 },
  cancelled: { label: "ملغي", variant: "destructive", icon: AlertTriangle },
}

const ExperimentsPage = () => {
  const [experiments, setExperiments] = useState(mockExperiments)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  const filteredExperiments = experiments.filter(exp => {
    const matchesSearch = exp.name.includes(searchQuery) || exp.crop.includes(searchQuery)
    const matchesStatus = statusFilter === "all" || exp.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const stats = {
    total: experiments.length,
    active: experiments.filter(e => e.status === "in_progress").length,
    completed: experiments.filter(e => e.status === "completed").length,
    pending: experiments.filter(e => e.status === "pending").length,
  }

  const columns = [
    {
      accessorKey: "name",
      header: "التجربة",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
            <FlaskConical className="w-5 h-5 text-emerald-600" />
          </div>
          <div>
            <p className="font-medium">{row.original.name}</p>
            <p className="text-sm text-muted-foreground">{row.original.researcher}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "type",
      header: "النوع",
      cell: ({ row }) => <Badge variant={typeConfig[row.original.type].color}>{typeConfig[row.original.type].label}</Badge>,
    },
    {
      accessorKey: "crop",
      header: "المحصول",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <Leaf className="w-4 h-4 text-green-500" />
          {row.original.crop}
        </div>
      ),
    },
    {
      accessorKey: "location",
      header: "الموقع",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-gray-500" />
          {row.original.location}
        </div>
      ),
    },
    {
      accessorKey: "progress",
      header: "التقدم",
      cell: ({ row }) => (
        <div className="w-24">
          <div className="flex justify-between text-xs mb-1">
            <span>{row.original.progress}%</span>
          </div>
          <Progress value={row.original.progress} className="h-2" />
        </div>
      ),
    },
    {
      accessorKey: "status",
      header: "الحالة",
      cell: ({ row }) => {
        const config = statusConfig[row.original.status]
        const Icon = config.icon
        return (
          <Badge variant={config.variant}>
            <Icon className="w-3 h-3 ml-1" />
            {config.label}
          </Badge>
        )
      },
    },
    {
      id: "actions",
      header: "",
      cell: ({ row }) => (
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
      ),
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
            <FlaskConical className="w-7 h-7 text-emerald-500" />
            التجارب الزراعية
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة ومتابعة التجارب والأبحاث الزراعية</p>
        </div>
        <Button onClick={() => toast.info("قريباً...")}>
          <Plus className="w-4 h-4 ml-2" />
          تجربة جديدة
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Beaker className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">إجمالي التجارب</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900 flex items-center justify-center">
              <FlaskConical className="w-5 h-5 text-emerald-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.active}</p>
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
              <p className="text-sm text-muted-foreground">مكتملة</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-yellow-100 dark:bg-yellow-900 flex items-center justify-center">
              <Clock className="w-5 h-5 text-yellow-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.pending}</p>
              <p className="text-sm text-muted-foreground">قيد الانتظار</p>
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
                <SelectItem value="pending">قيد الانتظار</SelectItem>
                <SelectItem value="in_progress">قيد التنفيذ</SelectItem>
                <SelectItem value="completed">مكتمل</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>التجارب ({filteredExperiments.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable columns={columns} data={filteredExperiments} searchKey="name" />
        </CardContent>
      </Card>
    </div>
  )
}

export default ExperimentsPage
