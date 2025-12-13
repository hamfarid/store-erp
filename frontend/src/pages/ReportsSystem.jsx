/**
 * صفحة نظام التقارير
 */
import React, { useState, useEffect } from 'react';
import reportsService from '../services/reportsService';
import './ReportsSystem.css';

const ReportsSystem = () => {
  const [activeTab, setActiveTab] = useState('sales');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // تعيين التواريخ الافتراضية (آخر 30 يوم)
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    setEndDate(today.toISOString().split('T')[0]);
    setStartDate(thirtyDaysAgo.toISOString().split('T')[0]);
  }, []);

  const loadReport = async (reportType) => {
    try {
      setLoading(true);
      let result;

      switch (reportType) {
        case 'sales-summary':
          result = await reportsService.getSalesSummary(startDate, endDate);
          break;
        case 'sales-by-product':
          result = await reportsService.getSalesByProduct(startDate, endDate);
          break;
        case 'sales-by-customer':
          result = await reportsService.getSalesByCustomer(startDate, endDate);
          break;
        case 'stock-levels':
          result = await reportsService.getStockLevels(false);
          break;
        case 'low-stock':
          result = await reportsService.getStockLevels(true);
          break;
        case 'expiring-lots':
          result = await reportsService.getExpiringLots(30);
          break;
        case 'profit-loss':
          result = await reportsService.getProfitLoss(startDate, endDate);
          break;
        case 'shifts-performance':
          result = await reportsService.getShiftsPerformance(startDate, endDate);
          break;
        default:
          break;
      }

      if (result && result.success) {
        setReportData({ type: reportType, data: result });
      }
    } catch (error) {
      alert('خطأ في تحميل التقرير: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePrint = () => {
    if (!reportData) return;
    
    const reportHTML = generateReportHTML(reportData);
    reportsService.printReport(reportHTML, getReportTitle(reportData.type));
  };

  const handleExport = async () => {
    if (!reportData) return;
    
    try {
      await reportsService.exportToExcel(reportData.type, {
        start_date: startDate,
        end_date: endDate
      });
    } catch (error) {
      alert('خطأ في تصدير التقرير: ' + error.message);
    }
  };

  const getReportTitle = (reportType) => {
    const titles = {
      'sales-summary': 'ملخص المبيعات',
      'sales-by-product': 'المبيعات حسب المنتج',
      'sales-by-customer': 'المبيعات حسب العميل',
      'stock-levels': 'مستويات المخزون',
      'low-stock': 'المنتجات منخفضة المخزون',
      'expiring-lots': 'اللوطات قريبة الانتهاء',
      'profit-loss': 'الأرباح والخسائر',
      'shifts-performance': 'أداء الورديات'
    };
    return titles[reportType] || 'تقرير';
  };

  const generateReportHTML = (report) => {
    // TODO: Generate HTML based on report type
    return '<div>تقرير</div>';
  };

  const renderSalesSummary = (data) => {
    const summary = data.summary;
    
    return (
      <div className="report-content">
        <h2>ملخص المبيعات</h2>
        <div className="summary-cards">
          <div className="summary-card">
            <h3>إجمالي المبيعات</h3>
            <p className="amount">{summary.total_sales.toFixed(2)} ريال</p>
          </div>
          <div className="summary-card">
            <h3>المرتجعات</h3>
            <p className="amount negative">{summary.total_refunds.toFixed(2)} ريال</p>
          </div>
          <div className="summary-card">
            <h3>صافي المبيعات</h3>
            <p className="amount">{summary.net_sales.toFixed(2)} ريال</p>
          </div>
          <div className="summary-card">
            <h3>عدد المعاملات</h3>
            <p className="count">{summary.total_transactions}</p>
          </div>
          <div className="summary-card">
            <h3>متوسط البيع</h3>
            <p className="amount">{summary.average_sale.toFixed(2)} ريال</p>
          </div>
        </div>

        <div className="payment-methods">
          <h3>المبيعات حسب طريقة الدفع</h3>
          <div className="summary-cards">
            <div className="summary-card">
              <h4>نقدي</h4>
              <p className="amount">{summary.cash_sales.toFixed(2)} ريال</p>
            </div>
            <div className="summary-card">
              <h4>بطاقة</h4>
              <p className="amount">{summary.card_sales.toFixed(2)} ريال</p>
            </div>
          </div>
        </div>

        <div className="sales-chart">
          <h3>المبيعات اليومية</h3>
          <table>
            <thead>
              <tr>
                <th>التاريخ</th>
                <th>المبيعات</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(summary.sales_by_day).map(([date, amount]) => (
                <tr key={date}>
                  <td>{date}</td>
                  <td>{amount.toFixed(2)} ريال</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  const renderSalesByProduct = (data) => {
    return (
      <div className="report-content">
        <h2>المبيعات حسب المنتج</h2>
        <table>
          <thead>
            <tr>
              <th>المنتج</th>
              <th>الكمية المباعة</th>
              <th>إجمالي المبيعات</th>
              <th>عدد المعاملات</th>
              <th>متوسط السعر</th>
            </tr>
          </thead>
          <tbody>
            {data.products.map((product, index) => (
              <tr key={index}>
                <td>{product.product_name}</td>
                <td>{product.total_quantity}</td>
                <td>{product.total_amount.toFixed(2)} ريال</td>
                <td>{product.transaction_count}</td>
                <td>{product.average_price.toFixed(2)} ريال</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderStockLevels = (data) => {
    return (
      <div className="report-content">
        <h2>مستويات المخزون</h2>
        <table>
          <thead>
            <tr>
              <th>المنتج</th>
              <th>الكود</th>
              <th>الكمية الحالية</th>
              <th>الحد الأدنى</th>
              <th>الحد الأقصى</th>
              <th>عدد اللوطات</th>
              <th>الحالة</th>
            </tr>
          </thead>
          <tbody>
            {data.products.map((product, index) => (
              <tr key={index} className={product.is_low_stock ? 'low-stock' : ''}>
                <td>{product.product_name}</td>
                <td>{product.product_code}</td>
                <td>{product.total_quantity}</td>
                <td>{product.min_stock_level}</td>
                <td>{product.max_stock_level}</td>
                <td>{product.batches_count}</td>
                <td>
                  {product.is_low_stock ? (
                    <span className="badge badge-danger">منخفض</span>
                  ) : (
                    <span className="badge badge-success">طبيعي</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderExpiringLots = (data) => {
    return (
      <div className="report-content">
        <h2>اللوطات قريبة الانتهاء</h2>
        <table>
          <thead>
            <tr>
              <th>رقم اللوط</th>
              <th>المنتج</th>
              <th>الكمية</th>
              <th>تاريخ الانتهاء</th>
              <th>الأيام المتبقية</th>
              <th>الحالة</th>
            </tr>
          </thead>
          <tbody>
            {data.batches.map((batch, index) => (
              <tr key={index} className={`urgency-${batch.urgency}`}>
                <td>{batch.batch_number}</td>
                <td>{batch.product_name}</td>
                <td>{batch.current_quantity}</td>
                <td>{new Date(batch.expiry_date).toLocaleDateString('ar-SA')}</td>
                <td>{batch.days_to_expiry}</td>
                <td>
                  {batch.is_expired ? (
                    <span className="badge badge-danger">منتهي</span>
                  ) : batch.urgency === 'critical' ? (
                    <span className="badge badge-danger">حرج</span>
                  ) : batch.urgency === 'warning' ? (
                    <span className="badge badge-warning">تحذير</span>
                  ) : (
                    <span className="badge badge-info">عادي</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const renderProfitLoss = (data) => {
    const report = data.report;
    
    return (
      <div className="report-content">
        <h2>الأرباح والخسائر</h2>
        <div className="summary-cards">
          <div className="summary-card">
            <h3>إجمالي الإيرادات</h3>
            <p className="amount">{report.total_revenue.toFixed(2)} ريال</p>
          </div>
          <div className="summary-card">
            <h3>إجمالي التكاليف</h3>
            <p className="amount negative">{report.total_cost.toFixed(2)} ريال</p>
          </div>
          <div className="summary-card">
            <h3>إجمالي الربح</h3>
            <p className="amount">{report.gross_profit.toFixed(2)} ريال</p>
          </div>
          <div className="summary-card">
            <h3>هامش الربح</h3>
            <p className="percentage">{report.profit_margin.toFixed(2)}%</p>
          </div>
        </div>
      </div>
    );
  };

  const renderReportContent = () => {
    if (!reportData) {
      return (
        <div className="no-report">
          <p>اختر تقرير من القائمة</p>
        </div>
      );
    }

    switch (reportData.type) {
      case 'sales-summary':
        return renderSalesSummary(reportData.data);
      case 'sales-by-product':
        return renderSalesByProduct(reportData.data);
      case 'stock-levels':
      case 'low-stock':
        return renderStockLevels(reportData.data);
      case 'expiring-lots':
        return renderExpiringLots(reportData.data);
      case 'profit-loss':
        return renderProfitLoss(reportData.data);
      default:
        return <div>تقرير غير معروف</div>;
    }
  };

  return (
    <div className="reports-system">
      <div className="reports-header">
        <h1>نظام التقارير</h1>
        <div className="date-range">
          <label>من:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
          <label>إلى:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
      </div>

      <div className="reports-content">
        <div className="reports-sidebar">
          <div className="report-category">
            <h3>تقارير المبيعات</h3>
            <button onClick={() => loadReport('sales-summary')}>ملخص المبيعات</button>
            <button onClick={() => loadReport('sales-by-product')}>المبيعات حسب المنتج</button>
            <button onClick={() => loadReport('sales-by-customer')}>المبيعات حسب العميل</button>
          </div>

          <div className="report-category">
            <h3>تقارير المخزون</h3>
            <button onClick={() => loadReport('stock-levels')}>مستويات المخزون</button>
            <button onClick={() => loadReport('low-stock')}>المنتجات منخفضة المخزون</button>
            <button onClick={() => loadReport('expiring-lots')}>اللوطات قريبة الانتهاء</button>
          </div>

          <div className="report-category">
            <h3>التقارير المالية</h3>
            <button onClick={() => loadReport('profit-loss')}>الأرباح والخسائر</button>
          </div>

          <div className="report-category">
            <h3>تقارير العمليات</h3>
            <button onClick={() => loadReport('shifts-performance')}>أداء الورديات</button>
          </div>
        </div>

        <div className="reports-main">
          {loading ? (
            <div className="loading">جاري تحميل التقرير...</div>
          ) : (
            <>
              {reportData && (
                <div className="report-actions">
                  <button onClick={handlePrint} className="btn-print">
                    طباعة
                  </button>
                  <button onClick={handleExport} className="btn-export">
                    تصدير Excel
                  </button>
                </div>
              )}
              {renderReportContent()}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ReportsSystem;
