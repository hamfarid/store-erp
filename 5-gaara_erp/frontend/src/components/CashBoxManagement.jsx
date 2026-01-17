import React, { useState, useEffect } from 'react';
import {
  Search, Plus, Edit, Trash2, CreditCard, DollarSign, TrendingUp, TrendingDown, Calendar, Eye, XCircle, CheckCircle, AlertCircle
} from 'lucide-react';

const CashBoxManagement = () => {
  const [cashBoxes, setCashBoxes] = useState([]);
  const [currencies, setCurrencies] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showTransactionModal, setShowTransactionModal] = useState(false);
  const [showBalanceModal, setShowBalanceModal] = useState(false);
  const [selectedCashBox, setSelectedCashBox] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    currency_id: '',
    opening_balance: 0,
    is_active: true
  });
  const [transactionData, setTransactionData] = useState({
    transaction_type: 'deposit',
    amount: 0,
    currency_id: '',
    reference: '',
    description: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      const [cashBoxesRes, currenciesRes] = await Promise.all([
        fetch('http://localhost:5002/api/accounting/cash-boxes', {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch('http://localhost:5002/api/accounting/currencies', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);
      
      if (cashBoxesRes.ok) {
        const data = await cashBoxesRes.json();
        setCashBoxes(data.data || data.cash_boxes || []);
      }
      
      if (currenciesRes.ok) {
        const data = await currenciesRes.json();
        setCurrencies(data.data || data.currencies || []);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('Error loading data:', error);
      setLoading(false);
    }
  };

  const loadTransactions = async (cashBoxId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5002/api/accounting/cash-boxes/${cashBoxId}/transactions`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setTransactions(data.data || data.transactions || []);
      }
    } catch (error) {
      console.error('Error loading transactions:', error);
    }
  };

  const filteredCashBoxes = cashBoxes.filter(box =>
    box.name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('token');
      const url = selectedCashBox 
        ? `http://localhost:5002/api/accounting/cash-boxes/${selectedCashBox.id}`
        : 'http://localhost:5002/api/accounting/cash-boxes';
      
      const method = selectedCashBox ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        alert(selectedCashBox ? 'تم تحديث الصندوق بنجاح' : 'تم إضافة الصندوق بنجاح');
        setShowAddModal(false);
        setShowEditModal(false);
        loadData();
        resetForm();
      } else {
        alert('حدث خطأ أثناء الحفظ');
      }
    } catch (error) {
      console.error('Error saving cash box:', error);
      alert('حدث خطأ أثناء الحفظ');
    }
  };

  const handleTransactionSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5002/api/accounting/cash-boxes/${selectedCashBox.id}/transactions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(transactionData)
      });

      if (response.ok) {
        alert('تم إضافة الحركة بنجاح');
        setShowTransactionModal(false);
        loadData();
        resetTransactionForm();
      } else {
        alert('حدث خطأ أثناء إضافة الحركة');
      }
    } catch (error) {
      console.error('Error adding transaction:', error);
      alert('حدث خطأ أثناء إضافة الحركة');
    }
  };

  const handleEdit = (cashBox) => {
    setSelectedCashBox(cashBox);
    setFormData({
      name: cashBox.name || '',
      description: cashBox.description || '',
      currency_id: cashBox.currency_id || '',
      opening_balance: cashBox.opening_balance || 0,
      is_active: cashBox.is_active !== false
    });
    setShowEditModal(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('هل أنت متأكد من حذف هذا الصندوق؟')) return;
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5002/api/accounting/cash-boxes/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        alert('تم حذف الصندوق بنجاح');
        loadData();
      } else {
        alert('حدث خطأ أثناء الحذف');
      }
    } catch (error) {
      console.error('Error deleting cash box:', error);
      alert('حدث خطأ أثناء الحذف');
    }
  };

  const handleViewBalance = async (cashBox) => {
    setSelectedCashBox(cashBox);
    await loadTransactions(cashBox.id);
    setShowBalanceModal(true);
  };

  const handleAddTransaction = (cashBox) => {
    setSelectedCashBox(cashBox);
    setTransactionData({
      transaction_type: 'deposit',
      amount: 0,
      currency_id: cashBox.currency_id || '',
      reference: '',
      description: ''
    });
    setShowTransactionModal(true);
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      currency_id: '',
      opening_balance: 0,
      is_active: true
    });
    setSelectedCashBox(null);
  };

  const resetTransactionForm = () => {
    setTransactionData({
      transaction_type: 'deposit',
      amount: 0,
      currency_id: '',
      reference: '',
      description: ''
    });
  };

  const getCurrencySymbol = (currencyId) => {
    const currency = currencies.find(c => c.id === currencyId);
    return currency?.symbol || 'ج.م';
  };

  const calculateTotalBalance = () => {
    return cashBoxes.reduce((sum, box) => sum + (box.current_balance || 0), 0);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6" dir="rtl">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">إدارة الصناديق والخزائن</h1>
          <p className="text-gray-600 mt-1">إدارة صناديق النقدية والحسابات المالية</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors"
        >
          <Plus className="w-5 h-5" />
          إضافة صندوق
        </button>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">إجمالي الصناديق</p>
              <p className="text-2xl font-bold text-gray-800">{cashBoxes.length}</p>
            </div>
            <CreditCard className="w-10 h-10 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">صناديق نشطة</p>
              <p className="text-2xl font-bold text-green-600">
                {cashBoxes.filter(b => b.is_active).length}
              </p>
            </div>
            <CheckCircle className="w-10 h-10 text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">الرصيد الإجمالي</p>
              <p className="text-2xl font-bold text-blue-600">
                {calculateTotalBalance().toFixed(2)}
              </p>
            </div>
            <DollarSign className="w-10 h-10 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">آخر تحديث</p>
              <p className="text-sm font-semibold text-gray-800">
                {new Date().toLocaleDateString('ar-EG')}
              </p>
            </div>
            <Calendar className="w-10 h-10 text-gray-400" />
          </div>
        </div>
      </div>

      {/* Search */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="flex items-center gap-2">
          <Search className="w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="البحث عن صندوق..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Cash Boxes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCashBoxes.length === 0 ? (
          <div className="col-span-full bg-white rounded-lg shadow-md p-8 text-center">
            <CreditCard className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-500 text-lg">لا توجد صناديق</p>
          </div>
        ) : (
          filteredCashBoxes.map((cashBox) => (
            <div key={cashBox.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-800 mb-1">{cashBox.name}</h3>
                  <p className="text-sm text-gray-600">{cashBox.description}</p>
                </div>
                <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                  cashBox.is_active
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {cashBox.is_active ? 'نشط' : 'غير نشط'}
                </div>
              </div>

              <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-4 mb-4">
                <p className="text-sm text-gray-600 mb-1">الرصيد الحالي</p>
                <p className="text-3xl font-bold text-blue-600">
                  {(cashBox.current_balance || 0).toFixed(2)} {getCurrencySymbol(cashBox.currency_id)}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-2 mb-4 text-sm">
                <div className="bg-gray-50 rounded p-2">
                  <p className="text-gray-600 text-xs">الرصيد الافتتاحي</p>
                  <p className="font-semibold">{(cashBox.opening_balance || 0).toFixed(2)}</p>
                </div>
                <div className="bg-gray-50 rounded p-2">
                  <p className="text-gray-600 text-xs">عدد الحركات</p>
                  <p className="font-semibold">{cashBox.transaction_count || 0}</p>
                </div>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleViewBalance(cashBox)}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm flex items-center justify-center gap-1"
                >
                  <Eye className="w-4 h-4" />
                  عرض
                </button>
                <button
                  onClick={() => handleAddTransaction(cashBox)}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-lg text-sm flex items-center justify-center gap-1"
                >
                  <Plus className="w-4 h-4" />
                  حركة
                </button>
                <button
                  onClick={() => handleEdit(cashBox)}
                  className="bg-yellow-600 hover:bg-yellow-700 text-white px-3 py-2 rounded-lg text-sm"
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDelete(cashBox.id)}
                  className="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg text-sm"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Add/Edit Modal */}
      {(showAddModal || showEditModal) && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">
                  {selectedCashBox ? 'تعديل الصندوق' : 'إضافة صندوق جديد'}
                </h2>
                <button
                  onClick={() => {
                    setShowAddModal(false);
                    setShowEditModal(false);
                    resetForm();
                  }}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="space-y-4 mb-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      اسم الصندوق *
                    </label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      required
                      placeholder="الصندوق الرئيسي"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      الوصف
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      rows="3"
                      placeholder="وصف الصندوق..."
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        العملة *
                      </label>
                      <select
                        value={formData.currency_id}
                        onChange={(e) => setFormData({ ...formData, currency_id: e.target.value })}
                        required
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">اختر العملة</option>
                        {currencies.map(currency => (
                          <option key={currency.id} value={currency.id}>
                            {currency.name} ({currency.symbol})
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        الرصيد الافتتاحي
                      </label>
                      <input
                        type="number"
                        value={formData.opening_balance}
                        onChange={(e) => setFormData({ ...formData, opening_balance: parseFloat(e.target.value) || 0 })}
                        step="0.01"
                        placeholder="0.00"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  </div>

                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.is_active}
                      onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                      className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700">صندوق نشط</span>
                  </label>
                </div>

                <div className="flex justify-end gap-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowAddModal(false);
                      setShowEditModal(false);
                      resetForm();
                    }}
                    className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    إلغاء
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                  >
                    {selectedCashBox ? 'تحديث' : 'إضافة'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Transaction Modal */}
      {showTransactionModal && selectedCashBox && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-lg w-full">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">إضافة حركة مالية</h2>
                <button
                  onClick={() => {
                    setShowTransactionModal(false);
                    resetTransactionForm();
                  }}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              <form onSubmit={handleTransactionSubmit}>
                <div className="space-y-4 mb-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      نوع الحركة *
                    </label>
                    <div className="grid grid-cols-2 gap-4">
                      <button
                        type="button"
                        onClick={() => setTransactionData({ ...transactionData, transaction_type: 'deposit' })}
                        className={`p-4 rounded-lg border-2 flex flex-col items-center gap-2 ${
                          transactionData.transaction_type === 'deposit'
                            ? 'border-green-500 bg-green-50'
                            : 'border-gray-300 hover:border-green-300'
                        }`}
                      >
                        <TrendingUp className="w-8 h-8 text-green-600" />
                        <span className="font-medium">إيداع</span>
                      </button>
                      <button
                        type="button"
                        onClick={() => setTransactionData({ ...transactionData, transaction_type: 'withdrawal' })}
                        className={`p-4 rounded-lg border-2 flex flex-col items-center gap-2 ${
                          transactionData.transaction_type === 'withdrawal'
                            ? 'border-red-500 bg-red-50'
                            : 'border-gray-300 hover:border-red-300'
                        }`}
                      >
                        <TrendingDown className="w-8 h-8 text-red-600" />
                        <span className="font-medium">سحب</span>
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      المبلغ *
                    </label>
                    <input
                      type="number"
                      value={transactionData.amount}
                      onChange={(e) => setTransactionData({ ...transactionData, amount: parseFloat(e.target.value) || 0 })}
                      required
                      step="0.01"
                      min="0.01"
                      placeholder="0.00"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      المرجع
                    </label>
                    <input
                      type="text"
                      value={transactionData.reference}
                      onChange={(e) => setTransactionData({ ...transactionData, reference: e.target.value })}
                      placeholder="رقم المرجع أو الإيصال"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      الوصف
                    </label>
                    <textarea
                      value={transactionData.description}
                      onChange={(e) => setTransactionData({ ...transactionData, description: e.target.value })}
                      rows="3"
                      placeholder="وصف الحركة..."
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="flex justify-end gap-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowTransactionModal(false);
                      resetTransactionForm();
                    }}
                    className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                  >
                    إلغاء
                  </button>
                  <button
                    type="submit"
                    className={`px-6 py-2 text-white rounded-lg ${
                      transactionData.transaction_type === 'deposit'
                        ? 'bg-green-600 hover:bg-green-700'
                        : 'bg-red-600 hover:bg-red-700'
                    }`}
                  >
                    إضافة الحركة
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Balance View Modal */}
      {showBalanceModal && selectedCashBox && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">تفاصيل الصندوق: {selectedCashBox.name}</h2>
                <button
                  onClick={() => setShowBalanceModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-6 mb-6">
                <p className="text-sm text-gray-600 mb-2">الرصيد الحالي</p>
                <p className="text-4xl font-bold text-blue-600">
                  {(selectedCashBox.current_balance || 0).toFixed(2)} {getCurrencySymbol(selectedCashBox.currency_id)}
                </p>
              </div>

              <h3 className="text-lg font-semibold mb-4">آخر الحركات</h3>
              <div className="space-y-2">
                {transactions.length === 0 ? (
                  <p className="text-center text-gray-500 py-8">لا توجد حركات</p>
                ) : (
                  transactions.map((transaction) => (
                    <div key={transaction.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        {transaction.transaction_type === 'deposit' ? (
                          <TrendingUp className="w-6 h-6 text-green-600" />
                        ) : (
                          <TrendingDown className="w-6 h-6 text-red-600" />
                        )}
                        <div>
                          <p className="font-medium">{transaction.description}</p>
                          <p className="text-sm text-gray-600">
                            {new Date(transaction.created_at).toLocaleDateString('ar-EG')}
                          </p>
                        </div>
                      </div>
                      <div className={`text-lg font-bold ${
                        transaction.transaction_type === 'deposit' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {transaction.transaction_type === 'deposit' ? '+' : '-'}
                        {transaction.amount.toFixed(2)}
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div className="flex justify-end mt-6">
                <button
                  onClick={() => setShowBalanceModal(false)}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  إغلاق
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CashBoxManagement;
