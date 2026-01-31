import React from 'react';
import { Badge } from '../components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '../components/ui/table';
import { CreditCard, Banknote, FileText, Wallet } from 'lucide-react';

function InvoicesPage() {
  return (
    <div className="p-6 space-y-6" dir="rtl">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">نظام الفواتير المالية</h1>
        <p className="text-muted-foreground mt-1">إدارة العملات والبنوك والفواتير المالية</p>
      </div>

      <Tabs defaultValue="currencies" className="space-y-4">
        <TabsList>
          <TabsTrigger value="currencies" className="gap-2">
            <Banknote className="w-4 h-4" />
            العملات
          </TabsTrigger>
          <TabsTrigger value="banks" className="gap-2">
            <Wallet className="w-4 h-4" />
            البنوك
          </TabsTrigger>
          <TabsTrigger value="invoices" className="gap-2">
            <FileText className="w-4 h-4" />
            الفواتير
          </TabsTrigger>
        </TabsList>

        {/* Currencies Tab */}
        <TabsContent value="currencies">
          <Card>
            <CardHeader>
              <CardTitle>إدارة العملات</CardTitle>
              <CardDescription>أسعار الصرف والعملات المتاحة</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">الجنيه المصري</CardTitle>
                    <CardDescription>EGP - ج.م</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Badge variant="secondary">العملة الأساسية</Badge>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">اليورو</CardTitle>
                    <CardDescription>EUR - €</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm font-medium">سعر الصرف: 52.50 ج.م</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-lg">الدولار الأمريكي</CardTitle>
                    <CardDescription>USD - $</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm font-medium">سعر الصرف: 48.75 ج.م</p>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Banks Tab */}
        <TabsContent value="banks">
          <Card>
            <CardHeader>
              <CardTitle>إدارة البنوك</CardTitle>
              <CardDescription>الحسابات البنكية والمصرفية</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader className="pb-2">
                    <div className="flex items-center gap-2">
                      <CreditCard className="w-5 h-5 text-primary" />
                      <CardTitle className="text-lg">البنك الأهلي المصري</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <p className="text-sm text-foreground">رقم الحساب: <span className="font-mono">123456789</span></p>
                    <Badge variant="outline">حساب جاري - EGP</Badge>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="pb-2">
                    <div className="flex items-center gap-2">
                      <CreditCard className="w-5 h-5 text-primary" />
                      <CardTitle className="text-lg">بنك مصر</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <p className="text-sm text-foreground">رقم الحساب: <span className="font-mono">987654321</span></p>
                    <Badge variant="outline">حساب توفير - EGP</Badge>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Invoices Tab */}
        <TabsContent value="invoices">
          <Card data-testid="invoices-table">
            <CardHeader>
              <CardTitle>فواتير الاستيراد</CardTitle>
              <CardDescription>سجل الفواتير والمعاملات</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>رقم الفاتورة</TableHead>
                    <TableHead>المورد</TableHead>
                    <TableHead>المبلغ</TableHead>
                    <TableHead>العملة</TableHead>
                    <TableHead>التاريخ</TableHead>
                    <TableHead>الحالة</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell className="font-medium">INV-2024-001</TableCell>
                    <TableCell>شركة البذور المتقدمة</TableCell>
                    <TableCell>15,000.00</TableCell>
                    <TableCell>EUR</TableCell>
                    <TableCell>2024-01-15</TableCell>
                    <TableCell>
                      <Badge variant="default" className="bg-green-100 text-green-800 hover:bg-green-100">مدفوعة</Badge>
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell className="font-medium">INV-2024-002</TableCell>
                    <TableCell>مؤسسة الأسمدة الحديثة</TableCell>
                    <TableCell>8,500.00</TableCell>
                    <TableCell>EUR</TableCell>
                    <TableCell>2024-01-20</TableCell>
                    <TableCell>
                      <Badge variant="secondary" className="bg-yellow-100 text-yellow-800 hover:bg-yellow-100">معلقة</Badge>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default InvoicesPage;
