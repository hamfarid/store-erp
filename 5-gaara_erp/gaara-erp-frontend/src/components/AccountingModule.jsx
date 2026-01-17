import { useState, useEffect } from "react"
import { useLocation } from "react-router-dom"
import { motion } from "framer-motion"
import { toast } from "sonner"
import {
  Calculator,
  BookOpen,
  FileText,
  DollarSign,
  TrendingUp,
  TrendingDown,
  CreditCard,
  Wallet,
  Building,
  ChevronRight,
  Plus,
  ArrowUpRight,
  ArrowDownRight,
  PieChart,
  BarChart3,
} from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
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
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import { Separator } from "@/components/ui/separator"

import { DataTable, FormModal, StatsCard } from "@/components/common"
import { formatCurrency, formatNumber } from "@/lib/utils"

// Mock Chart of Accounts
const mockAccounts = [
  {
    id: 1,
    code: "1000",
    name: "الأصول",
    type: "رئيسي",
    category: "أصول",
    balance: 500000,
    children: [
      { id: 11, code: "1100", name: "الأصول المتداولة", type: "فرعي", balance: 350000 },
      { id: 12, code: "1110", name: "النقدية والبنوك", type: "تفصيلي", balance: 150000 },
      { id: 13, code: "1120", name: "العملاء", type: "تفصيلي", balance: 120000 },
      { id: 14, code: "1130", name: "المخزون", type: "تفصيلي", balance: 80000 },
      { id: 15, code: "1200", name: "الأصول الثابتة", type: "فرعي", balance: 150000 },
    ],
  },
  {
    id: 2,
    code: "2000",
    name: "الخصوم",
    type: "رئيسي",
    category: "خصوم",
    balance: 200000,
    children: [
      { id: 21, code: "2100", name: "الخصوم المتداولة", type: "فرعي", balance: 120000 },
      { id: 22, code: "2110", name: "الموردين", type: "تفصيلي", balance: 80000 },
      { id: 23, code: "2120", name: "مصاريف مستحقة", type: "تفصيلي", balance: 40000 },
      { id: 24, code: "2200", name: "قروض طويلة الأجل", type: "فرعي", balance: 80000 },
    ],
  },
  {
    id: 3,
    code: "3000",
    name: "حقوق الملكية",
    type: "رئيسي",
    category: "حقوق ملكية",
    balance: 300000,
    children: [
      { id: 31, code: "3100", name: "رأس المال", type: "فرعي", balance: 250000 },
      { id: 32, code: "3200", name: "الأرباح المحتجزة", type: "فرعي", balance: 50000 },
    ],
  },
  {
    id: 4,
    code: "4000",
    name: "الإيرادات",
    type: "رئيسي",
    category: "إيرادات",
    balance: 450000,
    children: [
      { id: 41, code: "4100", name: "إيرادات المبيعات", type: "فرعي", balance: 400000 },
      { id: 42, code: "4200", name: "إيرادات أخرى", type: "فرعي", balance: 50000 },
    ],
  },
  {
    id: 5,
    code: "5000",
    name: "المصروفات",
    type: "رئيسي",
    category: "مصروفات",
    balance: 280000,
    children: [
      { id: 51, code: "5100", name: "تكلفة المبيعات", type: "فرعي", balance: 180000 },
      { id: 52, code: "5200", name: "مصاريف إدارية", type: "فرعي", balance: 60000 },
      { id: 53, code: "5300", name: "مصاريف تسويقية", type: "فرعي", balance: 40000 },
    ],
  },
]

// Mock Journal Entries
const mockJournalEntries = [
  {
    id: 1,
    entryNo: "JV-2025-001",
    date: "2025-01-10",
    description: "تسجيل مبيعات نقدية",
    debit: 15000,
    credit: 15000,
    status: "مرحل",
    createdBy: "أحمد محمد",
    lines: [
      { account: "النقدية", debit: 15000, credit: 0 },
      { account: "إيرادات المبيعات", debit: 0, credit: 15000 },
    ],
  },
  {
    id: 2,
    entryNo: "JV-2025-002",
    date: "2025-01-09",
    description: "سداد فاتورة مورد",
    debit: 8500,
    credit: 8500,
    status: "مرحل",
    createdBy: "محمد علي",
    lines: [
      { account: "الموردين", debit: 8500, credit: 0 },
      { account: "البنك", debit: 0, credit: 8500 },
    ],
  },
  {
    id: 3,
    entryNo: "JV-2025-003",
    date: "2025-01-08",
    description: "شراء بضاعة بالآجل",
    debit: 25000,
    credit: 25000,
    status: "معلق",
    createdBy: "سعيد أحمد",
    lines: [
      { account: "المخزون", debit: 25000, credit: 0 },
      { account: "الموردين", debit: 0, credit: 25000 },
    ],
  },
]

const accountTypes = ["رئيسي", "فرعي", "تفصيلي"]
const accountCategories = ["أصول", "خصوم", "حقوق ملكية", "إيرادات", "مصروفات"]

const AccountingModule = () => {
  const location = useLocation()
  const [activeTab, setActiveTab] = useState("chart-of-accounts")
  const [accounts, setAccounts] = useState(mockAccounts)
  const [journalEntries, setJournalEntries] = useState(mockJournalEntries)
  const [isLoading, setIsLoading] = useState(false)

  // Modals
  const [accountModal, setAccountModal] = useState(false)
  const [journalModal, setJournalModal] = useState(false)
  const [formData, setFormData] = useState({
    code: "",
    name: "",
    type: "",
    category: "",
    parentAccount: "",
    description: "",
  })

  // Set active tab based on URL
  useEffect(() => {
    if (location.pathname.includes("/chart-of-accounts")) setActiveTab("chart-of-accounts")
    else if (location.pathname.includes("/journal-entries")) setActiveTab("journal-entries")
    else if (location.pathname.includes("/financial-reports")) setActiveTab("financial-reports")
  }, [location])

  // Stats calculations
  const totalAssets = accounts.find((a) => a.code === "1000")?.balance || 0
  const totalLiabilities = accounts.find((a) => a.code === "2000")?.balance || 0
  const totalRevenue = accounts.find((a) => a.code === "4000")?.balance || 0
  const totalExpenses = accounts.find((a) => a.code === "5000")?.balance || 0
  const netIncome = totalRevenue - totalExpenses

  // Journal Entry columns
  const journalColumns = [
    { key: "entryNo", header: "رقم القيد", sortable: true },
    { key: "date", header: "التاريخ", sortable: true },
    {
      key: "description",
      header: "البيان",
      render: (val) => <span className="max-w-xs truncate block">{val}</span>,
    },
    {
      key: "debit",
      header: "مدين",
      sortable: true,
      render: (val) => formatCurrency(val),
    },
    {
      key: "credit",
      header: "دائن",
      sortable: true,
      render: (val) => formatCurrency(val),
    },
    {
      key: "status",
      header: "الحالة",
      render: (val) => (
        <Badge variant={val === "مرحل" ? "default" : "secondary"}>
          {val}
        </Badge>
      ),
    },
    { key: "createdBy", header: "بواسطة" },
  ]

  // Handlers
  const handleAddAccount = () => {
    setFormData({
      code: "",
      name: "",
      type: "",
      category: "",
      parentAccount: "",
      description: "",
    })
    setAccountModal(true)
  }

  const handleAddJournalEntry = () => {
    setJournalModal(true)
  }

  // Account Tree Component
  const AccountTree = ({ account, level = 0 }) => (
    <div className={`${level > 0 ? "mr-6 border-r pr-4" : ""}`}>
      <div
        className={`flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors ${
          level === 0 ? "bg-slate-50 dark:bg-slate-800/50" : ""
        }`}
      >
        <div className="flex items-center gap-3">
          <span className="text-sm font-mono text-muted-foreground">{account.code}</span>
          <span className={`font-medium ${level === 0 ? "text-lg" : ""}`}>{account.name}</span>
          <Badge variant="outline" className="text-xs">
            {account.type}
          </Badge>
        </div>
        <span className={`font-medium ${account.balance < 0 ? "text-red-600" : ""}`}>
          {formatCurrency(account.balance)}
        </span>
      </div>
      {account.children && (
        <div className="mt-1 space-y-1">
          {account.children.map((child) => (
            <AccountTree key={child.id} account={child} level={level + 1} />
          ))}
        </div>
      )}
    </div>
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-800 dark:text-white">
          المحاسبة المالية
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          إدارة الحسابات والقيود والتقارير المالية
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatsCard
          title="إجمالي الأصول"
          value={totalAssets}
          format="currency"
          icon={Building}
          color="blue"
          delay={0}
        />
        <StatsCard
          title="إجمالي الخصوم"
          value={totalLiabilities}
          format="currency"
          icon={CreditCard}
          color="red"
          delay={0.1}
        />
        <StatsCard
          title="الإيرادات"
          value={totalRevenue}
          format="currency"
          icon={TrendingUp}
          color="emerald"
          delay={0.2}
        />
        <StatsCard
          title="المصروفات"
          value={totalExpenses}
          format="currency"
          icon={TrendingDown}
          color="amber"
          delay={0.3}
        />
        <StatsCard
          title="صافي الربح"
          value={netIncome}
          format="currency"
          change={netIncome > 0 ? 15 : -10}
          icon={Wallet}
          color={netIncome >= 0 ? "emerald" : "red"}
          delay={0.4}
        />
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800">
          <TabsTrigger value="chart-of-accounts" className="gap-2">
            <BookOpen className="w-4 h-4" />
            شجرة الحسابات
          </TabsTrigger>
          <TabsTrigger value="journal-entries" className="gap-2">
            <FileText className="w-4 h-4" />
            القيود اليومية
          </TabsTrigger>
          <TabsTrigger value="financial-reports" className="gap-2">
            <BarChart3 className="w-4 h-4" />
            التقارير المالية
          </TabsTrigger>
        </TabsList>

        {/* Chart of Accounts Tab */}
        <TabsContent value="chart-of-accounts" className="mt-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>شجرة الحسابات</CardTitle>
                <CardDescription>تنظيم الحسابات حسب التصنيف</CardDescription>
              </div>
              <Button onClick={handleAddAccount}>
                <Plus className="w-4 h-4 ml-2" />
                إضافة حساب
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {accounts.map((account) => (
                  <AccountTree key={account.id} account={account} />
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Journal Entries Tab */}
        <TabsContent value="journal-entries" className="mt-6">
          <DataTable
            data={journalEntries}
            columns={journalColumns}
            searchKey="description"
            searchPlaceholder="البحث عن قيد..."
            addButtonText="قيد جديد"
            onAdd={handleAddJournalEntry}
            onView={(row) => toast.info(`عرض: ${row.entryNo}`)}
            onEdit={(row) => toast.info(`تعديل: ${row.entryNo}`)}
            onRefresh={() => toast.info("تم تحديث البيانات")}
          />
        </TabsContent>

        {/* Financial Reports Tab */}
        <TabsContent value="financial-reports" className="mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Balance Sheet Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <PieChart className="w-5 h-5" />
                  الميزانية العمومية
                </CardTitle>
                <CardDescription>ملخص الأصول والخصوم</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <span className="font-medium">إجمالي الأصول</span>
                  <span className="font-bold text-blue-600">{formatCurrency(totalAssets)}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                  <span className="font-medium">إجمالي الخصوم</span>
                  <span className="font-bold text-red-600">{formatCurrency(totalLiabilities)}</span>
                </div>
                <Separator />
                <div className="flex justify-between items-center p-3 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg">
                  <span className="font-medium">حقوق الملكية</span>
                  <span className="font-bold text-emerald-600">
                    {formatCurrency(totalAssets - totalLiabilities)}
                  </span>
                </div>
                <Button className="w-full" variant="outline">
                  <FileText className="w-4 h-4 ml-2" />
                  تقرير تفصيلي
                </Button>
              </CardContent>
            </Card>

            {/* Income Statement Summary */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  قائمة الدخل
                </CardTitle>
                <CardDescription>ملخص الإيرادات والمصروفات</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg">
                  <span className="font-medium">إجمالي الإيرادات</span>
                  <span className="font-bold text-emerald-600">{formatCurrency(totalRevenue)}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-amber-50 dark:bg-amber-900/20 rounded-lg">
                  <span className="font-medium">إجمالي المصروفات</span>
                  <span className="font-bold text-amber-600">{formatCurrency(totalExpenses)}</span>
                </div>
                <Separator />
                <div
                  className={`flex justify-between items-center p-3 rounded-lg ${
                    netIncome >= 0
                      ? "bg-emerald-50 dark:bg-emerald-900/20"
                      : "bg-red-50 dark:bg-red-900/20"
                  }`}
                >
                  <span className="font-medium">صافي الربح / الخسارة</span>
                  <div className="flex items-center gap-1">
                    {netIncome >= 0 ? (
                      <ArrowUpRight className="w-4 h-4 text-emerald-600" />
                    ) : (
                      <ArrowDownRight className="w-4 h-4 text-red-600" />
                    )}
                    <span className={`font-bold ${netIncome >= 0 ? "text-emerald-600" : "text-red-600"}`}>
                      {formatCurrency(Math.abs(netIncome))}
                    </span>
                  </div>
                </div>
                <Button className="w-full" variant="outline">
                  <FileText className="w-4 h-4 ml-2" />
                  تقرير تفصيلي
                </Button>
              </CardContent>
            </Card>

            {/* Quick Reports */}
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>التقارير المالية</CardTitle>
                <CardDescription>الوصول السريع للتقارير</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {[
                    { title: "ميزان المراجعة", icon: Calculator },
                    { title: "دفتر الأستاذ", icon: BookOpen },
                    { title: "التدفقات النقدية", icon: Wallet },
                    { title: "تقرير الضريبة", icon: FileText },
                    { title: "أعمار الديون", icon: CreditCard },
                    { title: "تحليل الربحية", icon: TrendingUp },
                    { title: "المقارنات الشهرية", icon: BarChart3 },
                    { title: "تقرير مخصص", icon: PieChart },
                  ].map((report, index) => (
                    <motion.div
                      key={report.title}
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.05 }}
                    >
                      <Button
                        variant="outline"
                        className="w-full h-auto py-4 flex flex-col items-center gap-2"
                        onClick={() => toast.info(`فتح: ${report.title}`)}
                      >
                        <report.icon className="w-6 h-6 text-primary" />
                        <span className="text-sm">{report.title}</span>
                      </Button>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>

      {/* Add Account Modal */}
      <FormModal
        open={accountModal}
        onOpenChange={setAccountModal}
        title="إضافة حساب جديد"
        description="أدخل بيانات الحساب الجديد"
        onSubmit={(e) => {
          e.preventDefault()
          toast.success("تم إضافة الحساب بنجاح!")
          setAccountModal(false)
        }}
        isLoading={isLoading}
        size="lg"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="code">رقم الحساب *</Label>
            <Input
              id="code"
              value={formData.code}
              onChange={(e) => setFormData({ ...formData, code: e.target.value })}
              placeholder="مثال: 1110"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="name">اسم الحساب *</Label>
            <Input
              id="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="اسم الحساب"
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="type">نوع الحساب *</Label>
            <Select
              value={formData.type}
              onValueChange={(value) => setFormData({ ...formData, type: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="اختر النوع" />
              </SelectTrigger>
              <SelectContent>
                {accountTypes.map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="category">التصنيف *</Label>
            <Select
              value={formData.category}
              onValueChange={(value) => setFormData({ ...formData, category: value })}
            >
              <SelectTrigger>
                <SelectValue placeholder="اختر التصنيف" />
              </SelectTrigger>
              <SelectContent>
                {accountCategories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {cat}
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
              placeholder="وصف الحساب (اختياري)"
              rows={3}
            />
          </div>
        </div>
      </FormModal>

      {/* Add Journal Entry Modal */}
      <FormModal
        open={journalModal}
        onOpenChange={setJournalModal}
        title="إضافة قيد يومي"
        description="أدخل بيانات القيد المحاسبي"
        onSubmit={(e) => {
          e.preventDefault()
          toast.success("تم إضافة القيد بنجاح!")
          setJournalModal(false)
        }}
        isLoading={isLoading}
        size="xl"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>التاريخ *</Label>
              <Input type="date" required />
            </div>
            <div className="space-y-2">
              <Label>رقم المرجع</Label>
              <Input placeholder="رقم المرجع (اختياري)" />
            </div>
          </div>

          <div className="space-y-2">
            <Label>البيان *</Label>
            <Textarea placeholder="وصف القيد المحاسبي" rows={2} required />
          </div>

          <Separator />

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label>سطور القيد</Label>
              <Button type="button" variant="outline" size="sm">
                <Plus className="w-4 h-4 ml-1" />
                إضافة سطر
              </Button>
            </div>

            <div className="border rounded-lg overflow-hidden">
              <table className="w-full">
                <thead className="bg-slate-50 dark:bg-slate-800">
                  <tr>
                    <th className="p-3 text-right font-medium">الحساب</th>
                    <th className="p-3 text-right font-medium">مدين</th>
                    <th className="p-3 text-right font-medium">دائن</th>
                    <th className="p-3 w-10"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-t">
                    <td className="p-2">
                      <Select>
                        <SelectTrigger>
                          <SelectValue placeholder="اختر الحساب" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="cash">النقدية</SelectItem>
                          <SelectItem value="bank">البنك</SelectItem>
                          <SelectItem value="sales">إيرادات المبيعات</SelectItem>
                        </SelectContent>
                      </Select>
                    </td>
                    <td className="p-2">
                      <Input type="number" placeholder="0.00" />
                    </td>
                    <td className="p-2">
                      <Input type="number" placeholder="0.00" />
                    </td>
                    <td className="p-2">
                      <Button variant="ghost" size="icon" className="text-red-500">
                        ×
                      </Button>
                    </td>
                  </tr>
                  <tr className="border-t">
                    <td className="p-2">
                      <Select>
                        <SelectTrigger>
                          <SelectValue placeholder="اختر الحساب" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="cash">النقدية</SelectItem>
                          <SelectItem value="bank">البنك</SelectItem>
                          <SelectItem value="sales">إيرادات المبيعات</SelectItem>
                        </SelectContent>
                      </Select>
                    </td>
                    <td className="p-2">
                      <Input type="number" placeholder="0.00" />
                    </td>
                    <td className="p-2">
                      <Input type="number" placeholder="0.00" />
                    </td>
                    <td className="p-2">
                      <Button variant="ghost" size="icon" className="text-red-500">
                        ×
                      </Button>
                    </td>
                  </tr>
                </tbody>
                <tfoot className="bg-slate-50 dark:bg-slate-800 border-t">
                  <tr>
                    <td className="p-3 font-medium">الإجمالي</td>
                    <td className="p-3 font-bold text-emerald-600">0.00</td>
                    <td className="p-3 font-bold text-blue-600">0.00</td>
                    <td></td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
        </div>
      </FormModal>
    </div>
  )
}

export default AccountingModule
