import React, { useState, useEffect } from 'react';

const OpeningBalancesTreasury = () => {
  const [balances, setBalances] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setBalances([
        {
          id: 1,
          accountName: 'الخزينة الرئيسية',
          accountType: 'نقدي',
          currency: 'جنيه مصري',
          openingBalance: 50000,
          currentBalance: 75000,
          lastUpdate: '2024-01-15'
        },
        {
          id: 2,
          accountName: 'البنك الأهلي',
          accountType: 'بنكي',
          currency: 'جنيه مصري',
          openingBalance: 100000,
          currentBalance: 125000,
          lastUpdate: '2024-01-14'
        },
        {
          id: 3,
          accountName: 'خزينة الفرع الثاني',
          accountType: 'نقدي',
          currency: 'جنيه مصري',
          openingBalance: 25000,
          currentBalance: 30000,
          lastUpdate: '2024-01-13'
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div>
          <p className="mt-4 text-muted-foreground">جاري تحميل الأرصدة الافتتاحية للخزينة...</p>
        </div>
      </div>
    );
  }

  const totalOpeningBalance = balances.reduce((sum, balance) => sum + balance.openingBalance, 0);
  const totalCurrentBalance = balances.reduce((sum, balance) => sum + balance.currentBalance, 0);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-lg">
        <div className="px-6 py-4 border-b border-border">
          <h1 className="text-2xl font-bold text-foreground">الأرصدة الافتتاحية للخزينة</h1>
          <p className="text-muted-foreground">إدارة الأرصدة الافتتاحية والحالية للخزائن والحسابات البنكية</p>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            <div className="bg-primary/10 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-primary/95">إجمالي الحسابات</h3>
              <p className="text-2xl font-bold text-primary">{balances.length}</p>
            </div>
            <div className="bg-primary/10 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-green-800">الرصيد الافتتاحي</h3>
              <p className="text-2xl font-bold text-primary">{totalOpeningBalance.toLocaleString()} ج.م</p>
            </div>
            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="text-lg font-semibold text-purple-800">الرصيد الحالي</h3>
              <p className="text-2xl font-bold text-purple-600">{totalCurrentBalance.toLocaleString()} ج.م</p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-border">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    اسم الحساب
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    نوع الحساب
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    العملة
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    الرصيد الافتتاحي
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    الرصيد الحالي
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    الفرق
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    آخر تحديث
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {balances.map((balance) => {
                  const difference = balance.currentBalance - balance.openingBalance;
                  return (
                    <tr key={balance.id} className="hover:bg-muted/50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                        {balance.accountName}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          balance.accountType === 'نقدي' 
                            ? 'bg-primary/20 text-green-800' 
                            : 'bg-primary/20 text-primary/95'
                        }`}>
                          {balance.accountType}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {balance.currency}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {balance.openingBalance.toLocaleString()} ج.م
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {balance.currentBalance.toLocaleString()} ج.م
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <span className={difference >= 0 ? 'text-primary' : 'text-destructive'}>
                          {difference >= 0 ? '+' : ''}{difference.toLocaleString()} ج.م
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {balance.lastUpdate}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="mt-6 flex justify-end space-x-3">
            <button className="bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded-lg transition-colors">
              إضافة حساب جديد
            </button>
            <button className="bg-primary hover:bg-green-700 text-white px-4 py-2 rounded-lg transition-colors">
              تحديث الأرصدة
            </button>
            <button className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors">
              تصدير التقرير
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OpeningBalancesTreasury;

