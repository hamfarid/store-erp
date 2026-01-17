/**
 * Payments Management Page
 */

import React, { useState } from 'react';
import {
  Search, Plus, CreditCard, DollarSign, Calendar, User, Banknote,
  ArrowDownRight, ArrowUpRight, CheckCircle, Clock, Building2
} from 'lucide-react';
import Button from '../components/ui/ModernButton';

const samplePayments = [
  { id: 'PAY-001', type: 'received', customer: 'شركة الفيصل التجارية', amount: 15000, method: 'تحويل بنكي', date: '2024-12-01', reference: 'INV-2024-089', status: 'completed' },
  { id: 'PAY-002', type: 'paid', supplier: 'Apple Inc.', amount: 200000, method: 'اعتماد مستندي', date: '2024-11-30', reference: 'PO-2024-002', status: 'completed' },
  { id: 'PAY-003', type: 'received', customer: 'أحمد محمد', amount: 5499, method: 'نقداً', date: '2024-11-29', reference: 'INV-2024-088', status: 'completed' },
  { id: 'PAY-004', type: 'paid', supplier: 'شركة التقنية', amount: 50000, method: 'شيك', date: '2024-11-28', reference: 'PO-2024-001', status: 'pending' },
  { id: 'PAY-005', type: 'received', customer: 'مؤسسة النور', amount: 25000, method: 'بطاقة ائتمان', date: '2024-11-27', reference: 'INV-2024-087', status: 'completed' },
];

const PaymentsPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');

  const totalReceived = samplePayments.filter(p => p.type === 'received').reduce((sum, p) => sum + p.amount, 0);
  const totalPaid = samplePayments.filter(p => p.type === 'paid').reduce((sum, p) => sum + p.amount, 0);

  const filteredPayments = samplePayments.filter(p => {
    const matchesSearch = p.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         (p.customer || p.supplier || '').toLowerCase().includes(searchQuery.toLowerCase());
    const matchesType = typeFilter === 'all' || p.type === typeFilter;
    return matchesSearch && matchesType;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 p-8" dir="rtl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">المدفوعات</h1>
          <p className="text-gray-500">إدارة المقبوضات والمدفوعات</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary" icon={ArrowUpRight}>تسجيل دفعة</Button>
          <Button variant="primary" icon={ArrowDownRight}>تسجيل قبض</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-xl p-5 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">إجمالي المقبوضات</p>
              <p className="text-2xl font-bold text-emerald-600">{totalReceived.toLocaleString()}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <ArrowDownRight className="text-emerald-600" size={24} />
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">إجمالي المدفوعات</p>
              <p className="text-2xl font-bold text-rose-600">{totalPaid.toLocaleString()}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-rose-100 flex items-center justify-center">
              <ArrowUpRight className="text-rose-600" size={24} />
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">صافي التدفق</p>
              <p className={`text-2xl font-bold ${totalReceived - totalPaid > 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                {(totalReceived - totalPaid).toLocaleString()}
              </p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <DollarSign className="text-blue-600" size={24} />
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 border border-gray-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">العمليات</p>
              <p className="text-2xl font-bold text-gray-900">{samplePayments.length}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <CreditCard className="text-purple-600" size={24} />
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm mb-8">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="بحث..."
              className="w-full pr-12 pl-4 py-3 bg-gray-50 border-0 rounded-xl focus:ring-2 focus:ring-teal-500"
            />
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setTypeFilter('all')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${typeFilter === 'all' ? 'bg-teal-100 text-teal-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              الكل
            </button>
            <button
              onClick={() => setTypeFilter('received')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${typeFilter === 'received' ? 'bg-emerald-100 text-emerald-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              مقبوضات
            </button>
            <button
              onClick={() => setTypeFilter('paid')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${typeFilter === 'paid' ? 'bg-rose-100 text-rose-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              مدفوعات
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-100">
            <tr>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">النوع</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">الطرف</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">المبلغ</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">الطريقة</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">التاريخ</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">المرجع</th>
              <th className="px-6 py-4 text-right text-sm font-semibold text-gray-700">الحالة</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {filteredPayments.map(payment => (
              <tr key={payment.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-xl ${payment.type === 'received' ? 'bg-emerald-100' : 'bg-rose-100'} flex items-center justify-center`}>
                      {payment.type === 'received' ? 
                        <ArrowDownRight size={18} className="text-emerald-600" /> : 
                        <ArrowUpRight size={18} className="text-rose-600" />
                      }
                    </div>
                    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${payment.type === 'received' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
                      {payment.type === 'received' ? 'قبض' : 'دفع'}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    {payment.type === 'received' ? <User size={14} className="text-gray-400" /> : <Building2 size={14} className="text-gray-400" />}
                    <span className="text-gray-900">{payment.customer || payment.supplier}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className={`font-semibold ${payment.type === 'received' ? 'text-emerald-600' : 'text-rose-600'}`}>
                    {payment.type === 'received' ? '+' : '-'}{payment.amount.toLocaleString()} ج.م
                  </span>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Banknote size={14} className="text-gray-400" />
                    <span>{payment.method}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2 text-gray-600">
                    <Calendar size={14} className="text-gray-400" />
                    <span>{new Date(payment.date).toLocaleDateString('ar-SA')}</span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-teal-600 font-medium">{payment.reference}</span>
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold ${
                    payment.status === 'completed' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'
                  }`}>
                    {payment.status === 'completed' ? <CheckCircle size={12} /> : <Clock size={12} />}
                    {payment.status === 'completed' ? 'مكتمل' : 'قيد المعالجة'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PaymentsPage;



