import React from 'react'

const InvoicePrint = ({ invoice, onClose }) => {
  // طباعة الفاتورة
  const handlePrint = () => {
    window.print()
  }

  // تصدير PDF
  const handleExportPDF = () => {
    // محاكاة تصدير PDF
    const printContent = document.getElementById('invoice-print-content')
    const originalContent = document.body.innerHTML
    
    document.body.innerHTML = printContent.innerHTML
    window.print()
    document.body.innerHTML = originalContent
    window.location.reload()
  }

  if (!invoice) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg w-full max-w-4xl max-h-[95vh] overflow-y-auto">
        {/* أزرار التحكم */}
        <div className="flex justify-between items-center p-4 border-b print:hidden">
          <h3 className="text-lg font-semibold">طباعة الفاتورة</h3>
          <div className="flex gap-2">
            <button
              onClick={handlePrint}
              className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded"
            >
              🖨️ طباعة
            </button>
            <button
              onClick={handleExportPDF}
              className="bg-primary hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              📄 تصدير PDF
            </button>
            <button
              onClick={onClose}
              className="bg-gray-300 hover:bg-gray-400 text-foreground px-4 py-2 rounded"
            >
              إغلاق
            </button>
          </div>
        </div>

        {/* محتوى الفاتورة للطباعة */}
        <div id="invoice-print-content" className="p-8 print:p-4">
          {/* رأس الفاتورة */}
          <div className="text-center mb-8 border-b-2 border-border pb-6">
            <h1 className="text-3xl font-bold text-foreground mb-2">شركة إدارة المخزون المتقدم</h1>
            <p className="text-muted-foreground">العنوان: القاهرة، مصر | الهاتف: 01234567890 | البريد: info@company.com</p>
            <h2 className="text-xl font-semibold text-primary-600 mt-4">فاتورة مبيعات</h2>
          </div>

          {/* معلومات الفاتورة */}
          <div className="grid grid-cols-2 gap-8 mb-8">
            <div>
              <h3 className="text-lg font-semibold mb-4 text-foreground">بيانات الفاتورة</h3>
              <div className="space-y-2">
                <p><span className="font-medium">رقم الفاتورة:</span> {invoice.invoice_number}</p>
                <p><span className="font-medium">التاريخ:</span> {invoice.date}</p>
                <p><span className="font-medium">تاريخ الاستحقاق:</span> {invoice.due_date || 'غير محدد'}</p>
                <p><span className="font-medium">الحالة:</span> 
                  <span className={`ml-2 px-2 py-1 rounded text-sm ${
                    invoice.status === 'معتمدة' ? 'bg-primary/20 text-green-800' : 'bg-accent/20 text-yellow-800'
                  }`}>
                    {invoice.status}
                  </span>
                </p>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4 text-foreground">بيانات العميل</h3>
              <div className="space-y-2">
                <p><span className="font-medium">اسم العميل:</span> {invoice.customer_name}</p>
                <p><span className="font-medium">مهندس المبيعات:</span> {invoice.sales_engineer || 'غير محدد'}</p>
                <p><span className="font-medium">طريقة الدفع:</span> {invoice.payment_method || 'غير محدد'}</p>
                <p><span className="font-medium">مدة السداد:</span> {invoice.payment_term ? `${invoice.payment_term} يوم` : 'غير محدد'}</p>
              </div>
            </div>
          </div>

          {/* جدول الأصناف */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4 text-foreground">تفاصيل الأصناف</h3>
            <table className="w-full border-collapse border border-border">
              <thead>
                <tr className="bg-muted">
                  <th className="border border-border px-4 py-2 text-right">م</th>
                  <th className="border border-border px-4 py-2 text-right">الصنف</th>
                  <th className="border border-border px-4 py-2 text-right">المخزن</th>
                  <th className="border border-border px-4 py-2 text-right">اللوط</th>
                  <th className="border border-border px-4 py-2 text-right">الكمية</th>
                  <th className="border border-border px-4 py-2 text-right">السعر</th>
                  <th className="border border-border px-4 py-2 text-right">الإجمالي</th>
                </tr>
              </thead>
              <tbody>
                {invoice.items && invoice.items.map((item, index) => (
                  <tr key={index}>
                    <td className="border border-border px-4 py-2">{index + 1}</td>
                    <td className="border border-border px-4 py-2">{item.product || 'غير محدد'}</td>
                    <td className="border border-border px-4 py-2">{item.warehouse || 'غير محدد'}</td>
                    <td className="border border-border px-4 py-2">{item.lot || 'غير محدد'}</td>
                    <td className="border border-border px-4 py-2">{item.quantity}</td>
                    <td className="border border-border px-4 py-2">{item.price} جنيه</td>
                    <td className="border border-border px-4 py-2">{item.total} جنيه</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* الإجماليات */}
          <div className="flex justify-end mb-8">
            <div className="w-1/3">
              <div className="bg-muted/50 p-4 rounded border">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">المجموع الفرعي:</span>
                  <span>{invoice.total_amount} جنيه</span>
                </div>
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">الضريبة (14%):</span>
                  <span>{(invoice.total_amount * 0.14).toFixed(2)} جنيه</span>
                </div>
                <div className="border-t pt-2">
                  <div className="flex justify-between items-center text-lg font-bold">
                    <span>الإجمالي النهائي:</span>
                    <span>{(invoice.total_amount * 1.14).toFixed(2)} جنيه</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* الملاحظات */}
          {invoice.notes && (
            <div className="mb-8">
              <h3 className="text-lg font-semibold mb-2 text-foreground">ملاحظات</h3>
              <p className="text-foreground bg-muted/50 p-4 rounded border">{invoice.notes}</p>
            </div>
          )}

          {/* التوقيعات */}
          <div className="grid grid-cols-3 gap-8 mt-12 pt-8 border-t">
            <div className="text-center">
              <div className="border-t border-gray-400 pt-2 mt-16">
                <p className="font-medium">مهندس المبيعات</p>
                <p className="text-sm text-muted-foreground">{invoice.sales_engineer || 'غير محدد'}</p>
              </div>
            </div>
            <div className="text-center">
              <div className="border-t border-gray-400 pt-2 mt-16">
                <p className="font-medium">المدير المالي</p>
              </div>
            </div>
            <div className="text-center">
              <div className="border-t border-gray-400 pt-2 mt-16">
                <p className="font-medium">العميل</p>
                <p className="text-sm text-muted-foreground">{invoice.customer_name}</p>
              </div>
            </div>
          </div>

          {/* تذييل الفاتورة */}
          <div className="text-center mt-8 pt-4 border-t text-sm text-gray-500">
            <p>شكراً لتعاملكم معنا | تم إنشاء هذه الفاتورة بواسطة نظام إدارة المخزون المتقدم</p>
            <p>تاريخ الطباعة: {new Date().toLocaleDateString('ar-EG')}</p>
          </div>
        </div>
      </div>

      {/* أنماط الطباعة */}
      <style jsx>{`
        @media print {
          body * {
            visibility: hidden;
          }
          #invoice-print-content,
          #invoice-print-content * {
            visibility: visible;
          }
          #invoice-print-content {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
          }
          .print\\:hidden {
            display: none !important;
          }
          .print\\:p-4 {
            padding: 1rem !important;
          }
        }
      `}</style>
    </div>
  )
}

export default InvoicePrint

