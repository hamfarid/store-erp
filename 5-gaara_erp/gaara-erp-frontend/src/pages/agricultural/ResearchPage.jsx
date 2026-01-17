/**
 * Agricultural Research Page - الأبحاث الزراعية
 * Gaara ERP v12
 */

import { useState } from "react"
import { toast } from "sonner"
import {
  BookOpen,
  Plus,
  Search,
  MoreVertical,
  Edit,
  Trash2,
  Eye,
  FileText,
  Users,
  Calendar,
  CheckCircle2,
  Clock,
  Target,
  Award,
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
import { DataTable } from "@/components/common"

const mockResearch = [
  { id: 1, title: "تطوير أصناف قمح مقاومة للجفاف", field: "وراثة نباتية", lead: "د. أحمد محمد", team: 5, startDate: "2024-06-01", endDate: "2027-06-01", status: "active", progress: 35, publications: 2, funding: 500000 },
  { id: 2, title: "مكافحة حشرة المن البيولوجية", field: "مكافحة آفات", lead: "د. سارة أحمد", team: 3, startDate: "2025-01-01", endDate: "2026-12-31", status: "active", progress: 20, publications: 0, funding: 150000 },
  { id: 3, title: "تحسين كفاءة استخدام المياه", field: "هندسة ري", lead: "م. محمد علي", team: 4, startDate: "2023-03-01", endDate: "2025-12-31", status: "active", progress: 80, publications: 5, funding: 350000 },
  { id: 4, title: "الزراعة العضوية المتكاملة", field: "إنتاج نباتي", lead: "د. فاطمة خالد", team: 6, startDate: "2022-01-01", endDate: "2024-12-31", status: "completed", progress: 100, publications: 8, funding: 750000 },
]

const statusConfig = {
  active: { label: "نشط", variant: "default", icon: Clock },
  completed: { label: "مكتمل", variant: "default", icon: CheckCircle2 },
  pending: { label: "معلق", variant: "secondary", icon: Clock },
}

const ResearchPage = () => {
  const [research, setResearch] = useState(mockResearch)
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")

  const filteredResearch = research.filter(r => {
    const matchesSearch = r.title.includes(searchQuery) || r.field.includes(searchQuery)
    const matchesStatus = statusFilter === "all" || r.status === statusFilter
    return matchesSearch && matchesStatus
  })

  const stats = {
    total: research.length,
    active: research.filter(r => r.status === "active").length,
    totalPublications: research.reduce((sum, r) => sum + r.publications, 0),
    totalFunding: research.reduce((sum, r) => sum + r.funding, 0),
  }

  const columns = [
    {
      accessorKey: "title",
      header: "البحث",
      cell: ({ row }) => (
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <p className="font-medium max-w-xs truncate">{row.original.title}</p>
            <p className="text-sm text-muted-foreground">{row.original.field}</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "lead",
      header: "الباحث الرئيسي",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <Users className="w-4 h-4 text-gray-500" />
          <div>
            <p className="text-sm">{row.original.lead}</p>
            <p className="text-xs text-muted-foreground">{row.original.team} باحث</p>
          </div>
        </div>
      ),
    },
    {
      accessorKey: "progress",
      header: "التقدم",
      cell: ({ row }) => (
        <div className="w-28">
          <div className="flex justify-between text-xs mb-1">
            <span>{row.original.progress}%</span>
          </div>
          <Progress value={row.original.progress} className="h-2" />
        </div>
      ),
    },
    {
      accessorKey: "publications",
      header: "المنشورات",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-purple-500" />
          <span>{row.original.publications}</span>
        </div>
      ),
    },
    {
      accessorKey: "funding",
      header: "التمويل",
      cell: ({ row }) => <span className="font-medium">{(row.original.funding / 1000).toFixed(0)}K ر.س</span>,
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
      cell: () => (
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
            <BookOpen className="w-7 h-7 text-blue-500" />
            الأبحاث الزراعية
          </h1>
          <p className="text-slate-600 dark:text-slate-400">إدارة المشاريع البحثية والعلمية</p>
        </div>
        <Button onClick={() => toast.info("قريباً...")}>
          <Plus className="w-4 h-4 ml-2" />
          مشروع جديد
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
              <Target className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-sm text-muted-foreground">مشروع بحثي</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-green-100 dark:bg-green-900 flex items-center justify-center">
              <Clock className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.active}</p>
              <p className="text-sm text-muted-foreground">نشط حالياً</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
              <Award className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.totalPublications}</p>
              <p className="text-sm text-muted-foreground">منشور علمي</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900 flex items-center justify-center">
              <FileText className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{(stats.totalFunding / 1000000).toFixed(1)}M</p>
              <p className="text-sm text-muted-foreground">ر.س تمويل</p>
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
                <SelectItem value="active">نشط</SelectItem>
                <SelectItem value="completed">مكتمل</SelectItem>
                <SelectItem value="pending">معلق</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>المشاريع البحثية ({filteredResearch.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable columns={columns} data={filteredResearch} searchKey="title" />
        </CardContent>
      </Card>
    </div>
  )
}

export default ResearchPage
