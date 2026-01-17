import React, { useState } from 'react';
import {
  Printer, Download, FileText, Settings, CheckCircle, AlertCircle, File, Package, Users, ShoppingCart, BarChart3
} from 'lucide-react';

const PrintExport = () => {
  const [selectedReport, setSelectedReport] = useState('');
  const [format, setFormat] = useState('pdf');
  const [orientation, setOrientation] = useState('portrait');
  const [pageSize, setPageSize] = useState('A4');
  const [includeHeader, setIncludeHeader] = useState(true);
  const [includeFooter, setIncludeFooter] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const reportTypes = [
    { value: 'products', label: 'قائمة المنتجات', icon: Package, color: 'blue' },
    { value: 'inventory', label: 'تقرير المخزون', icon: BarChart3, color: 'green' },
    { value: 'sales', label: 'تقرير المبيعات', icon: ShoppingCart, color: 'purple' },
    { value: 'purchases', label: 'تقرير المشتريات', icon: FileText, color: 'orange' },
    { value: 'customers', label: 'قائمة العملاء', icon: Users, color: 'red' },
    { value: 'suppliers', label: 'قائمة الموردين', icon: Users, color: 'yellow' },
  ];

  const handleGenerateReport = async () => {
    if (!selectedReport) {
      alert('يرجى اختيار نوع التقرير');
      return;
    }

    setProcessing(true);
    setResult(null);

    try {
      const token = localStorage.getItem('token');
      const params = new URLSearchParams({
        format,
        orientation,
        page_size: pageSize,
        include_header: includeHeader,
        include_footer: includeFooter
      });

      const response = await fetch(`http://localhost:5002/api/tools/print/${selectedReport}?${params}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        const extension = format === 'pdf' ? 'pdf' : format === 'excel' ? 'xlsx' : 'html';
        link.download = `${selectedReport}-report-${new Date().toISOString().split('T')[0]}.${extension}`;
        link.click();
        window.URL.revokeObjectURL(url);

        setResult({
          success: true,
          message: 'تم إنشاء التقرير بنجاح'
        });
      } else {
        setResult({
          success: false,
          message: 'حدث خطأ أثناء إنشاء التقرير'
        });
      }
    } catch (error) {
      console.error('Report generation error:', error);
      setResult({
        success: false,
        message: 'حدث خطأ أثناء الاتصال بالخادم'
      });
    } finally {
      setProcessing(false);
    }
  };

  const handleDirectPrint = async () => {
    if (!selectedReport) {
      alert('يرجى اختيار نوع التقرير');
      return;
    }

    setProcessing(true);
    setResult(null);

    try {
      const token = localStorage.getItem('token');
      const params = new URLSearchParams({
        format: 'html',
        orientation,
        page_size: pageSize,
        include_header: includeHeader,
        include_footer: includeFooter
      });

      const response = await fetch(`http://localhost:5002/api/tools/print/${selectedReport}?${params}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const html = await response.text();
        const printWindow = window.open('', '_blank');
        printWindow.document.write(html);
        printWindow.document.close();
        
        // Wait for content to load then print
        printWindow.onload = () => {
          printWindow.print();
        };

        setResult({
          success: true,
          message: 'تم فتح نافذة الطباعة'
        });
      } else {
        setResult({
          success: false,
          message: 'حدث خطأ أثناء تحضير التقرير للطباعة'
        });
      }
    } catch (error) {
      console.error('Print error:', error);
      setResult({
        success: false,
        message: 'حدث خطأ أثناء الاتصال بالخادم'
      });
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">طباعة وتصدير التقارير</h1>
          <p className="text-gray-600 mt-1">إنشاء وطباعة التقارير بصيغ متعددة</p>
        </div>
        <Printer className="w-12 h-12 text-blue-600" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration Panel */}
        <div className="lg:col-span-2 space-y-6">
          {/* Report Selection */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <FileText className="w-6 h-6 text-blue-600" />
              اختر نوع التقرير
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {reportTypes.map((type) => {
                const Icon = type.icon;
                const isSelected = selectedReport === type.value;
                return (
                  <button
                    key={type.value}
                    onClick={() => setSelectedReport(type.value)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      isSelected
                        ? `border-${type.color}-500 bg-${type.color}-50 shadow-md`
                        : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'
                    }`}
                  >
                    <Icon className={`w-10 h-10 mx-auto mb-2 ${
                      isSelected ? `text-${type.color}-600` : 'text-gray-400'
                    }`} />
                    <p className={`text-center text-sm font-medium ${
                      isSelected ? `text-${type.color}-800` : 'text-gray-700'
                    }`}>
                      {type.label}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Format Settings */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <Settings className="w-6 h-6 text-blue-600" />
              إعدادات التنسيق
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  صيغة الملف
                </label>
                <select
                  value={format}
                  onChange={(e) => setFormat(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="pdf">PDF</option>
                  <option value="excel">Excel</option>
                  <option value="html">HTML</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  حجم الصفحة
                </label>
                <select
                  value={pageSize}
                  onChange={(e) => setPageSize(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="A4">A4</option>
                  <option value="A3">A3</option>
                  <option value="Letter">Letter</option>
                  <option value="Legal">Legal</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  اتجاه الصفحة
                </label>
                <select
                  value={orientation}
                  onChange={(e) => setOrientation(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="portrait">عمودي (Portrait)</option>
                  <option value="landscape">أفقي (Landscape)</option>
                </select>
              </div>

              <div className="space-y-3">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={includeHeader}
                    onChange={(e) => setIncludeHeader(e.target.checked)}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                  />
                  <span className="text-sm font-medium text-gray-700">تضمين الرأسية</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={includeFooter}
                    onChange={(e) => setIncludeFooter(e.target.checked)}
                    className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                  />
                  <span className="text-sm font-medium text-gray-700">تضمين التذييل</span>
                </label>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={handleDirectPrint}
                disabled={!selectedReport || processing}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg flex items-center justify-center gap-2 transition-colors font-semibold"
              >
                {processing ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    جاري المعالجة...
                  </>
                ) : (
                  <>
                    <Printer className="w-5 h-5" />
                    طباعة مباشرة
                  </>
                )}
              </button>

              <button
                onClick={handleGenerateReport}
                disabled={!selectedReport || processing}
                className="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg flex items-center justify-center gap-2 transition-colors font-semibold"
              >
                {processing ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    جاري المعالجة...
                  </>
                ) : (
                  <>
                    <Download className="w-5 h-5" />
                    تحميل التقرير
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Result Message */}
          {result && (
            <div className={`p-6 rounded-lg ${
              result.success ? 'bg-green-50 border-2 border-green-200' : 'bg-red-50 border-2 border-red-200'
            }`}>
              <div className="flex items-center gap-3">
                {result.success ? (
                  <CheckCircle className="w-8 h-8 text-green-600" />
                ) : (
                  <AlertCircle className="w-8 h-8 text-red-600" />
                )}
                <p className={`font-semibold text-lg ${
                  result.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  {result.message}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Preview/Info Panel */}
        <div className="space-y-6">
          {/* Preview */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <File className="w-5 h-5 text-blue-600" />
              معاينة الإعدادات
            </h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">نوع التقرير:</span>
                <span className="font-semibold text-gray-800">
                  {reportTypes.find(r => r.value === selectedReport)?.label || 'غير محدد'}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">الصيغة:</span>
                <span className="font-semibold text-gray-800 uppercase">{format}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">حجم الصفحة:</span>
                <span className="font-semibold text-gray-800">{pageSize}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-gray-600">الاتجاه:</span>
                <span className="font-semibold text-gray-800">
                  {orientation === 'portrait' ? 'عمودي' : 'أفقي'}
                </span>
              </div>
            </div>
          </div>

          {/* Instructions */}
          <div className="bg-blue-50 rounded-lg p-6 border border-blue-200">
            <h3 className="font-semibold text-blue-800 mb-3 flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              تعليمات الاستخدام
            </h3>
            <ul className="space-y-2 text-sm text-blue-900">
              <li className="flex items-start gap-2">
                <span className="font-bold">1.</span>
                <span>اختر نوع التقرير المطلوب</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="font-bold">2.</span>
                <span>حدد صيغة الملف والإعدادات</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="font-bold">3.</span>
                <span>اضغط "طباعة مباشرة" للطباعة الفورية</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="font-bold">4.</span>
                <span>أو اضغط "تحميل التقرير" للحفظ</span>
              </li>
            </ul>
          </div>

          {/* Supported Formats */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="font-semibold text-gray-800 mb-3">الصيغ المدعومة</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2 p-2 bg-red-50 rounded">
                <File className="w-4 h-4 text-red-600" />
                <span className="text-gray-700">PDF - للطباعة والمشاركة</span>
              </div>
              <div className="flex items-center gap-2 p-2 bg-green-50 rounded">
                <File className="w-4 h-4 text-green-600" />
                <span className="text-gray-700">Excel - للتحليل والتعديل</span>
              </div>
              <div className="flex items-center gap-2 p-2 bg-blue-50 rounded">
                <File className="w-4 h-4 text-blue-600" />
                <span className="text-gray-700">HTML - للعرض على الويب</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrintExport;
