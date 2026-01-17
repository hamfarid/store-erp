import { useState } from "react"
import { motion } from "framer-motion"
import {
  Users,
  Building2,
  UserPlus,
  Search,
  Filter,
  Download,
  Upload,
  Eye,
  Edit,
  Trash2,
  Phone,
  Mail,
  MapPin,
  Star,
  MoreVertical,
  Tag,
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
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

const ContactsPage = () => {
  const [activeTab, setActiveTab] = useState("all")
  const [searchTerm, setSearchTerm] = useState("")
  const [typeFilter, setTypeFilter] = useState("all")
  const [viewMode, setViewMode] = useState("table") // table or grid

  // Mock data
  const summaryStats = [
    {
      title: "إجمالي جهات الاتصال",
      value: "٢٥٦",
      icon: Users,
      color: "emerald",
    },
    {
      title: "العملاء",
      value: "١٤٨",
      icon: Star,
      color: "blue",
    },
    {
      title: "الموردون",
      value: "٧٢",
      icon: Building2,
      color: "amber",
    },
    {
      title: "جهات جديدة",
      value: "٣٦",
      subtext: "هذا الشهر",
      icon: UserPlus,
      color: "purple",
    },
  ]

  const contacts = [
    {
      id: 1,
      name: "شركة الزراعة الحديثة",
      type: "عميل",
      category: "شركات",
      email: "info@modernagri.com",
      phone: "+966-50-123-4567",
      city: "الرياض",
      status: "نشط",
      rating: 5,
      totalOrders: 25,
      totalAmount: 450000,
    },
    {
      id: 2,
      name: "أحمد محمد العلي",
      type: "عميل",
      category: "أفراد",
      email: "ahmed@example.com",
      phone: "+966-55-987-6543",
      city: "جدة",
      status: "نشط",
      rating: 4,
      totalOrders: 8,
      totalAmount: 75000,
    },
    {
      id: 3,
      name: "مؤسسة البذور الذهبية",
      type: "مورد",
      category: "شركات",
      email: "contact@goldenseeds.sa",
      phone: "+966-12-345-6789",
      city: "الدمام",
      status: "نشط",
      rating: 5,
      totalOrders: 42,
      totalAmount: 890000,
    },
    {
      id: 4,
      name: "شركة المعدات الزراعية المتحدة",
      type: "مورد",
      category: "شركات",
      email: "sales@uniagri.com",
      phone: "+966-13-456-7890",
      city: "الخبر",
      status: "غير نشط",
      rating: 3,
      totalOrders: 5,
      totalAmount: 120000,
    },
  ]

  const getInitials = (name) => {
    return name
      .split(" ")
      .map((word) => word[0])
      .join("")
      .slice(0, 2)
  }

  const getStatusBadge = (status) => {
    return status === "نشط" ? (
      <Badge className="bg-emerald-500">نشط</Badge>
    ) : (
      <Badge variant="secondary">غير نشط</Badge>
    )
  }

  const getTypeBadge = (type) => {
    return type === "عميل" ? (
      <Badge className="bg-blue-500">عميل</Badge>
    ) : (
      <Badge className="bg-amber-500">مورد</Badge>
    )
  }

  const renderStars = (rating) => {
    return (
      <div className="flex gap-0.5">
        {[1, 2, 3, 4, 5].map((star) => (
          <Star
            key={star}
            className={`w-4 h-4 ${
              star <= rating
                ? "text-amber-400 fill-amber-400"
                : "text-slate-300"
            }`}
          />
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6" dir="rtl">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800 dark:text-white flex items-center gap-3">
            <Users className="w-8 h-8 text-emerald-500" />
            جهات الاتصال
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            إدارة العملاء والموردين وجهات الاتصال
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <Upload className="w-4 h-4 ml-2" />
            استيراد
          </Button>
          <Button variant="outline">
            <Download className="w-4 h-4 ml-2" />
            تصدير
          </Button>
          <Button className="bg-emerald-500 hover:bg-emerald-600">
            <UserPlus className="w-4 h-4 ml-2" />
            إضافة جهة اتصال
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
                      {stat.value}
                    </p>
                    {stat.subtext && (
                      <p className="text-xs text-slate-400 mt-1">{stat.subtext}</p>
                    )}
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
          <TabsTrigger value="all" className="flex items-center gap-2">
            <Users className="w-4 h-4" />
            الكل
          </TabsTrigger>
          <TabsTrigger value="customers" className="flex items-center gap-2">
            <Star className="w-4 h-4" />
            العملاء
          </TabsTrigger>
          <TabsTrigger value="suppliers" className="flex items-center gap-2">
            <Building2 className="w-4 h-4" />
            الموردون
          </TabsTrigger>
          <TabsTrigger value="tags" className="flex items-center gap-2">
            <Tag className="w-4 h-4" />
            التصنيفات
          </TabsTrigger>
        </TabsList>

        {/* All Contacts Tab */}
        <TabsContent value="all" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <CardTitle>قائمة جهات الاتصال</CardTitle>
                <div className="flex gap-3">
                  <div className="relative">
                    <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                    <Input
                      placeholder="بحث بالاسم أو البريد..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pr-9 w-64"
                    />
                  </div>
                  <Select value={typeFilter} onValueChange={setTypeFilter}>
                    <SelectTrigger className="w-40">
                      <SelectValue placeholder="النوع" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">الكل</SelectItem>
                      <SelectItem value="customer">عملاء</SelectItem>
                      <SelectItem value="supplier">موردون</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>جهة الاتصال</TableHead>
                    <TableHead>النوع</TableHead>
                    <TableHead>التصنيف</TableHead>
                    <TableHead>المدينة</TableHead>
                    <TableHead>التقييم</TableHead>
                    <TableHead>الطلبات</TableHead>
                    <TableHead>الإجمالي</TableHead>
                    <TableHead>الحالة</TableHead>
                    <TableHead>الإجراءات</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {contacts.map((contact) => (
                    <TableRow key={contact.id}>
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <Avatar className="w-10 h-10">
                            <AvatarFallback className="bg-emerald-100 text-emerald-700">
                              {getInitials(contact.name)}
                            </AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="font-medium text-slate-800 dark:text-white">
                              {contact.name}
                            </p>
                            <div className="flex items-center gap-2 text-sm text-slate-500">
                              <Mail className="w-3 h-3" />
                              {contact.email}
                            </div>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>{getTypeBadge(contact.type)}</TableCell>
                      <TableCell>
                        <Badge variant="outline">{contact.category}</Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1">
                          <MapPin className="w-3 h-3 text-slate-400" />
                          {contact.city}
                        </div>
                      </TableCell>
                      <TableCell>{renderStars(contact.rating)}</TableCell>
                      <TableCell>{contact.totalOrders}</TableCell>
                      <TableCell>
                        {contact.totalAmount.toLocaleString()} ر.س
                      </TableCell>
                      <TableCell>{getStatusBadge(contact.status)}</TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreVertical className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>
                              <Eye className="w-4 h-4 ml-2" />
                              عرض التفاصيل
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Edit className="w-4 h-4 ml-2" />
                              تعديل
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Phone className="w-4 h-4 ml-2" />
                              اتصال
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Mail className="w-4 h-4 ml-2" />
                              إرسال بريد
                            </DropdownMenuItem>
                            <DropdownMenuItem className="text-red-600">
                              <Trash2 className="w-4 h-4 ml-2" />
                              حذف
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Customers Tab */}
        <TabsContent value="customers" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>العملاء</CardTitle>
              <CardDescription>
                قائمة العملاء المسجلين في النظام
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {contacts
                  .filter((c) => c.type === "عميل")
                  .map((contact, index) => (
                    <motion.div
                      key={contact.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card className="border hover:border-emerald-300 transition-colors">
                        <CardContent className="p-4">
                          <div className="flex items-start gap-3">
                            <Avatar className="w-12 h-12">
                              <AvatarFallback className="bg-blue-100 text-blue-700">
                                {getInitials(contact.name)}
                              </AvatarFallback>
                            </Avatar>
                            <div className="flex-1">
                              <h4 className="font-medium text-slate-800 dark:text-white">
                                {contact.name}
                              </h4>
                              <p className="text-sm text-slate-500">{contact.email}</p>
                              <div className="flex items-center gap-2 mt-2">
                                {renderStars(contact.rating)}
                                <span className="text-xs text-slate-400">
                                  ({contact.totalOrders} طلب)
                                </span>
                              </div>
                            </div>
                            {getStatusBadge(contact.status)}
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Suppliers Tab */}
        <TabsContent value="suppliers" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle>الموردون</CardTitle>
              <CardDescription>
                قائمة الموردين المسجلين في النظام
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {contacts
                  .filter((c) => c.type === "مورد")
                  .map((contact, index) => (
                    <motion.div
                      key={contact.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card className="border hover:border-amber-300 transition-colors">
                        <CardContent className="p-4">
                          <div className="flex items-start gap-3">
                            <Avatar className="w-12 h-12">
                              <AvatarFallback className="bg-amber-100 text-amber-700">
                                {getInitials(contact.name)}
                              </AvatarFallback>
                            </Avatar>
                            <div className="flex-1">
                              <h4 className="font-medium text-slate-800 dark:text-white">
                                {contact.name}
                              </h4>
                              <p className="text-sm text-slate-500">{contact.email}</p>
                              <div className="flex items-center gap-2 mt-2">
                                {renderStars(contact.rating)}
                                <span className="text-xs text-slate-400">
                                  ({contact.totalOrders} طلب)
                                </span>
                              </div>
                            </div>
                            {getStatusBadge(contact.status)}
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Tags Tab */}
        <TabsContent value="tags" className="space-y-6 mt-6">
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>التصنيفات</CardTitle>
                <Button className="bg-emerald-500 hover:bg-emerald-600">
                  <Tag className="w-4 h-4 ml-2" />
                  تصنيف جديد
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  { name: "عملاء VIP", count: 15, color: "bg-amber-500" },
                  { name: "موردون رئيسيون", count: 8, color: "bg-blue-500" },
                  { name: "عملاء جدد", count: 25, color: "bg-emerald-500" },
                  { name: "عملاء متأخرون", count: 5, color: "bg-red-500" },
                ].map((tag, index) => (
                  <motion.div
                    key={tag.name}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Card className="border hover:border-emerald-300 transition-colors cursor-pointer">
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3">
                          <div className={`w-3 h-3 rounded-full ${tag.color}`} />
                          <div>
                            <p className="font-medium text-slate-800 dark:text-white">
                              {tag.name}
                            </p>
                            <p className="text-sm text-slate-500">
                              {tag.count} جهة اتصال
                            </p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ContactsPage
