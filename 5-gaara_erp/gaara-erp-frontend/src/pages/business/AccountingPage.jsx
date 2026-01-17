import { useState } from "react"
import { motion } from "framer-motion"
import {
  Calculator,
  TrendingUp,
  TrendingDown,
  DollarSign,
  FileText,
  PieChart,
  BookOpen,
  Receipt,
  CreditCard,
  Building2,
  RefreshCw,
  Download,
  Plus,
  Filter,
  Search,
  Calendar,
  ArrowUpRight,
  ArrowDownRight,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const AccountingPage = () => {
  const [activeTab, setActiveTab] = useState("overview")
  const [searchTerm, setSearchTerm] = useState("")
  const [filterPeriod, setFilterPeriod] = useState("month")

  // Mock data
  const summaryStats = [
    {
      title: "إجمالي الإيرادات",
      value: "٥٨٥,٠٠٠",
      change: "+12.5%",
      trend: "up",
      icon: TrendingUp,
      color: "emerald",
    },
    {
      title: "إجمالي المصروفات",
      value: "٣٢٠,٠٠٠",
      change: "+5.2%",
      trend: "up",
      icon: TrendingDown,
      color: "red",
    },
    {
      title: "صافي الربح",
      value: "٢٦٥,٠٠٠",
      change: "+18.3%",
      trend: "up",
      icon: DollarSign,
      color: "blue",
    },
    {
      title: "الذمم المدينة",
      value: "٨٥,٠٠٠",
      change: "-8.1%",
      trend: "down",
      icon: Receipt,
      color: "amber",
    },
  ]

  const recentTransactions = [
    {
      id: "TRX001",
      date: "2025-01-17",
      description: "مبيعات منتجات زراعية",
      type: "إيراد",
      account: "حساب المبيعات",
      amount: 25000,
      status: "مكتمل",
    },
    {
      id: "TRX002",
      date: "2025-01-16",
      description: "شراء مستلزمات مزرعة",
      type: "مصروف",
      account: "مصاريف التشغيل",
      amount: -8500,
      status: "مكتمل",
    },
    {
      id: "TRX003",
      date: "2025-01-15",
      description: "رواتب الموظفين",
      type: "مصروف",
      account: "الرواتب والأجور",
      amount: -45000,
      status: "معلق",
    },
  ]

  const accounts = [
    { code: "1001", name: "النقدية", type: "أصول", balance: 150000 },
    { code: "1002", name: "البنك", type: "أصول", balance: 350000 },
    { code: "2001", name: "الذمم الدائنة", type: "خصوم", balance: 75000 },
    { code: "3001", name: "رأس المال", type: "حقوق ملكية", balance: 500000 },
    { code: "4001", name: "المبيعات", type: "إيرادات", balance: 585000 },
    { code: "5001", name: "المشتريات", type: "مصروفات", balance: 320000 },
  ]

  return (
    <div className="space-y-6 p-6" dir="rtl">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 dark:text-white flex items-center gap-3">
            <Calculator className="w-8 h-8 text-emerald-500" />
            المحاسبة
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            إدارة الحسابات والقيود المحاسبية والتقارير المالية
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <Download className="w-4 h-4 ml-2" />
            تصدير التقرير
          </Button>
          <Button className="bg-emerald-500 hover:bg-emerald-600">
            <Plus className="w-4 h-4 ml-2" />
            قيد جديد
          </Button>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {summaryStats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="border-0 shadow-lg bg-white dark:bg-slate-900">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {stat.title}
                    </p>
                    <p className="text-2xl font-bold text-slate-800 dark:text-white mt-1">
                      {stat.value} ر.س
                    </p>
                    <div className="flex items-center gap-1 mt-2">
                      {stat.trend === "up" ? (
                        <ArrowUpRight className={`w-4 h-4 ${stat.color === "red" ? "text-red-500" : "text-emerald-500"}`} />
                      ) : (
                        <ArrowDownRight className="w-4 h-4 text-emerald-500" />
                      )}
                      <span className={`text-sm ${stat.trend === "up" && stat.color === "red" ? "text-red-500" : "text-emerald-500"}`}>
                        {stat.change}
                      </span>
                    </div>
                  </div>
                  <div className={`w-12 h-12 rounded-xl bg-${stat.color}-100 dark:bg-${stat.color}-900/30 flex items-center justify-center`}>
                    <stat.icon className={`w-6 h-6 text-${stat.color}-500`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="bg-slate-100 dark:bg-slate-800 p-1">
          <TabsTrigger value="overview" className="flex items-center gap-2">
            <PieChart className="w-4 h-4" />
            نظرة عامة
          </TabsTrigger>
          <TabsTrigger value="transactions" className="flex items-center gap-2">
            <Receipt className="w-4 h-4" />
            القيود والحركات
          </TabsTrigger>
          <TabsTrigger value="accounts" className="flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            دليل الحسابات
          </TabsTrigger>
          <TabsTrigger value="reports" className="flex items-center gap-2">
            <FileText className="w-4 h-4" />
            التقارير
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6 mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-emerald-500" />
                  الإيرادات والمصروفات
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center text-slate-400">
                  [رسم بياني للإيرادات والمصروفات]
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <PieChart className="w-5 h-5 text-blue-500" />
                  توزيع المصروفات
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center text-slate-400">
                  [رسم دائري لتوزيع المصروفات]
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Transactions Tab */}
        <TabsContent value="transactions" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <CardTitle>القيود المحاسبية</CardTitle>
                <div className="flex gap-3">
                  <div className="relative">
                    <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      placeholder="بحث..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pr-9 w-64"
                    />
                  </div>
                  <Select value={filterPeriod} onValueChange={setFilterPeriod}>
                    <SelectTrigger className="w-40">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="today">اليوم</SelectItem>
                      <SelectItem value="week">هذا الأسبوع</SelectItem>
                      <SelectItem value="month">هذا الشهر</SelectItem>
                      <SelectItem value="year">هذا العام</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>رقم القيد</TableHead>
                    <TableHead>التاريخ</TableHead>
                    <TableHead>الوصف</TableHead>
                    <TableHead>النوع</TableHead>
                    <TableHead>الحساب</TableHead>
                    <TableHead>المبلغ</TableHead>
                    <TableHead>الحالة</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recentTransactions.map((transaction) => (
                    <TableRow key={transaction.id}>
                      <TableCell className="font-mono">{transaction.id}</TableCell>
                      <TableCell>{transaction.date}</TableCell>
                      <TableCell>{transaction.description}</TableCell>
                      <TableCell>
                        <Badge variant={transaction.type === "إيراد" ? "default" : "secondary"}>
                          {transaction.type}
                        </Badge>
                      </TableCell>
                      <TableCell>{transaction.account}</TableCell>
                      <TableCell className={transaction.amount > 0 ? "text-emerald-600" : "text-red-600"}>
                        {transaction.amount > 0 ? "+" : ""}
                        {transaction.amount.toLocaleString()} ر.س
                      </TableCell>
                      <TableCell>
                        <Badge variant={transaction.status === "مكتمل" ? "default" : "outline"}>
                          {transaction.status}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Accounts Tab */}
        <TabsContent value="accounts" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>دليل الحسابات</CardTitle>
                <Button className="bg-emerald-500 hover:bg-emerald-600">
                  <Plus className="w-4 h-4 ml-2" />
                  حساب جديد
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>رمز الحساب</TableHead>
                    <TableHead>اسم الحساب</TableHead>
                    <TableHead>النوع</TableHead>
                    <TableHead>الرصيد</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {accounts.map((account) => (
                    <TableRow key={account.code}>
                      <TableCell className="font-mono">{account.code}</TableCell>
                      <TableCell className="font-medium">{account.name}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{account.type}</Badge>
                      </TableCell>
                      <TableCell>{account.balance.toLocaleString()} ر.س</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Reports Tab */}
        <TabsContent value="reports" className="space-y-6 mt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { title: "الميزانية العمومية", icon: Building2, color: "emerald" },
              { title: "قائمة الدخل", icon: TrendingUp, color: "blue" },
              { title: "التدفق النقدي", icon: DollarSign, color: "amber" },
              { title: "ميزان المراجعة", icon: Calculator, color: "purple" },
              { title: "تقرير الضرائب", icon: Receipt, color: "red" },
              { title: "تقرير الأرباح", icon: PieChart, color: "cyan" },
            ].map((report, index) => (
              <motion.div
                key={report.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow cursor-pointer">
                  <CardContent className="p-6">
                    <div className="flex items-center gap-4">
                      <div className={`w-12 h-12 rounded-xl bg-${report.color}-100 dark:bg-${report.color}-900/30 flex items-center justify-center`}>
                        <report.icon className={`w-6 h-6 text-${report.color}-500`} />
                      </div>
                      <div>
                        <h3 className="font-semibold text-slate-800 dark:text-white">
                          {report.title}
                        </h3>
                        <p className="text-sm text-slate-500">
                          عرض وتصدير التقرير
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default AccountingPage
