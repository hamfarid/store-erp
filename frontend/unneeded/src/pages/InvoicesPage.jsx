import React, { useState } from 'react';

function InvoicesPage() {
  const [activeTab, setActiveTab] = useState('currencies');

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-foreground mb-2">نظام الفواتير المالية</h1>
        <p className="text-muted-foreground">إدارة العملات والبنوك والفواتير المالية</p>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-border mb-6">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'currencies', label: 'العملات', icon: '💰' },
            { id: 'banks', label: 'البنوك', icon: '🏦' },
            { id: 'invoices', label: 'الفواتير', icon: '📄' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary/100 text-primary'
                  : 'border-transparent text-gray-500 hover:text-foreground hover:border-border'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'currencies' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-medium text-foreground mb-4">إدارة العملات</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="border rounded-lg p-4">
              <h3 className="font-medium text-foreground">الجنيه المصري</h3>
              <p className="text-sm text-muted-foreground">EGP - ج.م</p>
              <p className="text-xs text-gray-500">العملة الأساسية</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-medium text-foreground">اليورو</h3>
              <p className="text-sm text-muted-foreground">EUR - €</p>
              <p className="text-xs text-gray-500">سعر الصرف: 52.50 ج.م</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-medium text-foreground">الدولار الأمريكي</h3>
              <p className="text-sm text-muted-foreground">USD - $</p>
              <p className="text-xs text-gray-500">سعر الصرف: 48.75 ج.م</p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'banks' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-medium text-foreground mb-4">إدارة البنوك</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="border rounded-lg p-4">
              <h3 className="font-medium text-foreground">البنك الأهلي المصري</h3>
              <p className="text-sm text-muted-foreground">رقم الحساب: 123456789</p>
              <p className="text-xs text-gray-500">حساب جاري - EGP</p>
            </div>
            <div className="border rounded-lg p-4">
              <h3 className="font-medium text-foreground">بنك مصر</h3>
              <p className="text-sm text-muted-foreground">رقم الحساب: 987654321</p>
              <p className="text-xs text-gray-500">حساب توفير - EGP</p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'invoices' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-medium text-foreground mb-4">فواتير الاستيراد</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">رقم الفاتورة</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المورد</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">المبلغ</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">العملة</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">التاريخ</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">الحالة</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">INV-2024-001</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">شركة البذور المتقدمة</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">15,000.00</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">EUR</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">2024-01-15</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-primary/20 text-green-800">
                      مدفوعة
                    </span>
                  </td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">INV-2024-002</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">مؤسسة الأسمدة الحديثة</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">8,500.00</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">EUR</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">2024-01-20</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-accent/20 text-yellow-800">
                      معلقة
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default InvoicesPage;
