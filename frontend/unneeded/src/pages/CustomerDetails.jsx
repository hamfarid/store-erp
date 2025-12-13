/**
 * صفحة تفاصيل العميل
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/pages/CustomerDetails.js
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { usePermissions } from '../contexts/PermissionContext';
import customerService from '../services/customerService';

const CustomerDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { canAccessCustomer } = usePermissions();

  // ==================== State Management ====================
  
  const [customer, setCustomer] = useState(null);
  const [invoices, setInvoices] = useState([]);
  const [payments, setPayments] = useState([]);
  const [accountStatement, setAccountStatement] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  
  // حالات النوافذ المنبثقة
  const [paymentDialogOpen, setPaymentDialogOpen] = useState(false);
  const [creditDialogOpen, setCreditDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  
  // بيانات النماذج
  const [paymentData, setPaymentData] = useState({
    amount: '',
    payment_method: 'cash',
    reference: '',
    notes: '',
    payment_date: new Date().toISOString().split('T')[0]
  });
  
  const [creditData, setCreditData] = useState({
    credit_limit: '',
    reason: '',
    effective_date: new Date().toISOString().split('T')[0]
  });

  // ==================== Data Loading ====================

  useEffect(() => {
    if (id) {
      loadCustomerData();
    }
  }, [id]);

  const loadCustomerData = async () => {
    try {
      setLoading(true);
      setError(null);

      // تحميل بيانات العميل
      const customerData = await customerService.getById(id);
      setCustomer(customerData);

      // تحميل البيانات المرتبطة بشكل متوازي
      const [invoicesData, paymentsData, statementData] = await Promise.allSettled([
        customerService.getInvoices(id, { limit: 10 }),
        customerService.getPaymentHistory(id, { limit: 10 }),
        customerService.getAccountStatement(id, { limit: 20 })
      ]);

      if (invoicesData.status === 'fulfilled') {
        setInvoices(invoicesData.value);
      }

      if (paymentsData.status === 'fulfilled') {
        setPayments(paymentsData.value);
      }

      if (statementData.status === 'fulfilled') {
        setAccountStatement(statementData.value);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ==================== Event Handlers ====================

  const handleAddPayment = async () => {
    try {
      await customerService.addPayment(id, paymentData);
      setPaymentDialogOpen(false);
      setPaymentData({ amount: '', payment_method: 'cash', reference: '', notes: '', payment_date: new Date().toISOString().split('T')[0] });
      await loadCustomerData(); // إعادة تحميل البيانات
    } catch (error) {
      alert(`خطأ في إضافة الدفعة: ${error.message}`);
    }
  };

  const handleUpdateCredit = async () => {
    try {
      await customerService.updateCreditLimit(id, creditData);
      setCreditDialogOpen(false);
      setCreditData({ credit_limit: '', reason: '', effective_date: new Date().toISOString().split('T')[0] });
      await loadCustomerData(); // إعادة تحميل البيانات
    } catch (error) {
      alert(`خطأ في تحديث حد الائتمان: ${error.message}`);
    }
  };

  const handleDelete = async () => {
    try {
      await customerService.delete(id);
      setDeleteDialogOpen(false);
      navigate('/customers');
    } catch (error) {
      alert(`خطأ في حذف العميل: ${error.message}`);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  // ==================== Render Functions ====================

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>
          جاري تحميل بيانات العميل...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        خطأ في تحميل العميل: {error}
      </Alert>
    );
  }

  if (!customer) {
    return (
      <Alert severity="warning" sx={{ m: 2 }}>
        العميل غير موجود
      </Alert>
    );
  }

  const getCustomerTypeIcon = (type) => {
    return type === 'company' ? <BusinessIcon /> : <PersonIcon />;
  };

  const getCustomerTypeText = (type) => {
    return type === 'company' ? 'شركة' : 'فرد';
  };

  const getBalanceColor = (balance) => {
    if (balance > 0) return 'success';
    if (balance < 0) return 'error';
    return 'default';
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ar-EG', {
      style: 'currency',
      currency: 'EGP'
    }).format(amount || 0);
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box display="flex" justifyContent="between" alignItems="center" mb={3}>
        <Box display="flex" alignItems="center">
          <IconButton onClick={() => navigate('/customers')} sx={{ mr: 1 }}>
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h4" component="h1">
            تفاصيل العميل
          </Typography>
        </Box>
        
        <Box display="flex" gap={1}>
          <ProtectedButton
            variant="outlined"
            startIcon={<PrintIcon />}
            onClick={() => window.print()}
          >
            طباعة
          </ProtectedButton>
          
          <ProtectedButton
            variant="outlined"
            startIcon={<ShareIcon />}
            onClick={() => navigator.share?.({ title: customer.name, url: window.location.href })}
          >
            مشاركة
          </ProtectedButton>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* معلومات العميل الأساسية */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  {getCustomerTypeIcon(customer.customer_type)}
                </Avatar>
                <Box>
                  <Typography variant="h5" component="h2">
                    {customer.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {getCustomerTypeText(customer.customer_type)}
                  </Typography>
                </Box>
                {customer.is_vip && (
                  <Chip label="VIP" color="warning" size="small" sx={{ ml: 2 }} />
                )}
                {customer.is_active ? (
                  <Chip label="نشط" color="success" size="small" sx={{ ml: 1 }} />
                ) : (
                  <Chip label="غير نشط" color="error" size="small" sx={{ ml: 1 }} />
                )}
              </Box>

              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <PhoneIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">الهاتف</Typography>
                  </Box>
                  <Typography variant="body1" fontWeight="bold">
                    {customer.phone || 'غير محدد'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <EmailIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">البريد الإلكتروني</Typography>
                  </Box>
                  <Typography variant="body1" fontWeight="bold">
                    {customer.email || 'غير محدد'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" mb={1}>
                    <LocationIcon sx={{ mr: 1, color: 'text.secondary' }} />
                    <Typography variant="body2" color="text.secondary">العنوان</Typography>
                  </Box>
                  <Typography variant="body1" fontWeight="bold">
                    {customer.address || 'غير محدد'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">مهندس المبيعات</Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {customer.sales_engineer_name || 'غير محدد'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12}>
                  <Typography variant="body2" color="text.secondary">ملاحظات</Typography>
                  <Typography variant="body1">
                    {customer.notes || 'لا توجد ملاحظات'}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* الرصيد والائتمان */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                الرصيد والائتمان
              </Typography>
              
              <Box mb={2}>
                <Typography variant="body2" color="text.secondary">الرصيد الحالي</Typography>
                <Typography variant="h4" color={getBalanceColor(customer.balance)}>
                  {formatCurrency(customer.balance)}
                </Typography>
              </Box>
              
              <Box mb={2}>
                <Typography variant="body2" color="text.secondary">حد الائتمان</Typography>
                <Typography variant="h6">
                  {formatCurrency(customer.credit_limit)}
                </Typography>
              </Box>
              
              <Box mb={2}>
                <Typography variant="body2" color="text.secondary">الائتمان المتاح</Typography>
                <Typography variant="h6" color="success.main">
                  {formatCurrency((customer.credit_limit || 0) - (customer.balance || 0))}
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <ProtectedComponent
                customerId={customer.id}
                requiredPermission="manage_payments"
              >
                <Box display="flex" gap={1} mb={1}>
                  <ProtectedButton
                    variant="contained"
                    size="small"
                    startIcon={<PaymentIcon />}
                    onClick={() => setPaymentDialogOpen(true)}
                    fullWidth
                  >
                    إضافة دفعة
                  </ProtectedButton>
                </Box>
              </ProtectedComponent>

              <ProtectedComponent
                customerId={customer.id}
                requiredPermission="manage_credit"
              >
                <ProtectedButton
                  variant="outlined"
                  size="small"
                  startIcon={<CreditCardIcon />}
                  onClick={() => setCreditDialogOpen(true)}
                  fullWidth
                >
                  تحديث الائتمان
                </ProtectedButton>
              </ProtectedComponent>
            </CardContent>
          </Card>
        </Grid>

        {/* التبويبات */}
        <Grid item xs={12}>
          <Card>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={activeTab} onChange={handleTabChange}>
                <Tab label="الفواتير" />
                <Tab label="المدفوعات" />
                <Tab label="كشف الحساب" />
                <Tab label="جهات الاتصال" />
                <Tab label="العناوين" />
              </Tabs>
            </Box>

            {/* تبويب الفواتير */}
            {activeTab === 0 && (
              <CardContent>
                <Box display="flex" justifyContent="between" alignItems="center" mb={2}>
                  <Typography variant="h6">آخر الفواتير</Typography>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => navigate(`/customers/${id}/invoices`)}
                  >
                    عرض الكل
                  </Button>
                </Box>
                
                {invoices.length > 0 ? (
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>رقم الفاتورة</TableCell>
                          <TableCell>التاريخ</TableCell>
                          <TableCell>المبلغ</TableCell>
                          <TableCell>الحالة</TableCell>
                          <TableCell>الإجراءات</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {invoices.map((invoice) => (
                          <TableRow key={invoice.id}>
                            <TableCell>{invoice.invoice_number}</TableCell>
                            <TableCell>
                              {new Date(invoice.invoice_date).toLocaleDateString('ar-EG')}
                            </TableCell>
                            <TableCell>{formatCurrency(invoice.total_amount)}</TableCell>
                            <TableCell>
                              <Chip
                                label={invoice.status}
                                color={invoice.status === 'paid' ? 'success' : 'warning'}
                                size="small"
                              />
                            </TableCell>
                            <TableCell>
                              <IconButton
                                size="small"
                                onClick={() => navigate(`/invoices/${invoice.id}`)}
                              >
                                <ReceiptIcon />
                              </IconButton>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    لا توجد فواتير
                  </Typography>
                )}
              </CardContent>
            )}

            {/* تبويب المدفوعات */}
            {activeTab === 1 && (
              <CardContent>
                <Box display="flex" justifyContent="between" alignItems="center" mb={2}>
                  <Typography variant="h6">آخر المدفوعات</Typography>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => navigate(`/customers/${id}/payments`)}
                  >
                    عرض الكل
                  </Button>
                </Box>
                
                {payments.length > 0 ? (
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>التاريخ</TableCell>
                          <TableCell>المبلغ</TableCell>
                          <TableCell>طريقة الدفع</TableCell>
                          <TableCell>المرجع</TableCell>
                          <TableCell>ملاحظات</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {payments.map((payment, index) => (
                          <TableRow key={index}>
                            <TableCell>
                              {new Date(payment.payment_date).toLocaleDateString('ar-EG')}
                            </TableCell>
                            <TableCell>{formatCurrency(payment.amount)}</TableCell>
                            <TableCell>{payment.payment_method}</TableCell>
                            <TableCell>{payment.reference || '-'}</TableCell>
                            <TableCell>{payment.notes || '-'}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    لا توجد مدفوعات
                  </Typography>
                )}
              </CardContent>
            )}

            {/* تبويب كشف الحساب */}
            {activeTab === 2 && (
              <CardContent>
                <Box display="flex" justifyContent="between" alignItems="center" mb={2}>
                  <Typography variant="h6">كشف الحساب</Typography>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => navigate(`/customers/${id}/statement`)}
                  >
                    عرض مفصل
                  </Button>
                </Box>
                
                {accountStatement.length > 0 ? (
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>التاريخ</TableCell>
                          <TableCell>الوصف</TableCell>
                          <TableCell>مدين</TableCell>
                          <TableCell>دائن</TableCell>
                          <TableCell>الرصيد</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {accountStatement.map((entry, index) => (
                          <TableRow key={index}>
                            <TableCell>
                              {new Date(entry.date).toLocaleDateString('ar-EG')}
                            </TableCell>
                            <TableCell>{entry.description}</TableCell>
                            <TableCell>
                              {entry.debit ? formatCurrency(entry.debit) : '-'}
                            </TableCell>
                            <TableCell>
                              {entry.credit ? formatCurrency(entry.credit) : '-'}
                            </TableCell>
                            <TableCell>{formatCurrency(entry.balance)}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    لا توجد حركات في الحساب
                  </Typography>
                )}
              </CardContent>
            )}

            {/* تبويب جهات الاتصال */}
            {activeTab === 3 && (
              <CardContent>
                <Box display="flex" justifyContent="between" alignItems="center" mb={2}>
                  <Typography variant="h6">جهات الاتصال</Typography>
                  <ProtectedButton
                    variant="outlined"
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={() => navigate(`/customers/${id}/contacts/add`)}
                  >
                    إضافة جهة اتصال
                  </ProtectedButton>
                </Box>
                
                {customer.contacts && customer.contacts.length > 0 ? (
                  <List>
                    {customer.contacts.map((contact, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <PersonIcon />
                        </ListItemIcon>
                        <ListItemText
                          primary={contact.name}
                          secondary={`${contact.position || ''} - ${contact.phone || ''} - ${contact.email || ''}`}
                        />
                        <ListItemSecondaryAction>
                          <IconButton
                            size="small"
                            onClick={() => navigate(`/customers/${id}/contacts/${contact.id}/edit`)}
                          >
                            <EditIcon />
                          </IconButton>
                        </ListItemSecondaryAction>
                      </ListItem>
                    ))}
                  </List>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    لا توجد جهات اتصال
                  </Typography>
                )}
              </CardContent>
            )}

            {/* تبويب العناوين */}
            {activeTab === 4 && (
              <CardContent>
                <Box display="flex" justifyContent="between" alignItems="center" mb={2}>
                  <Typography variant="h6">العناوين</Typography>
                  <ProtectedButton
                    variant="outlined"
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={() => navigate(`/customers/${id}/addresses/add`)}
                  >
                    إضافة عنوان
                  </ProtectedButton>
                </Box>
                
                {customer.addresses && customer.addresses.length > 0 ? (
                  <List>
                    {customer.addresses.map((address, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <LocationIcon />
                        </ListItemIcon>
                        <ListItemText
                          primary={address.type}
                          secondary={`${address.street || ''}, ${address.city || ''}, ${address.country || ''}`}
                        />
                        <ListItemSecondaryAction>
                          <IconButton
                            size="small"
                            onClick={() => navigate(`/customers/${id}/addresses/${address.id}/edit`)}
                          >
                            <EditIcon />
                          </IconButton>
                        </ListItemSecondaryAction>
                      </ListItem>
                    ))}
                  </List>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    لا توجد عناوين
                  </Typography>
                )}
              </CardContent>
            )}
          </Card>
        </Grid>

        {/* أزرار الإجراءات */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                الإجراءات
              </Typography>
              
              <Box display="flex" gap={2} flexWrap="wrap">
                <ProtectedButton
                  variant="contained"
                  startIcon={<EditIcon />}
                  onClick={() => navigate(`/customers/${id}/edit`)}
                  customerId={customer.id}
                  requiredPermission="edit"
                >
                  تعديل العميل
                </ProtectedButton>
                
                <ProtectedButton
                  variant="outlined"
                  startIcon={<HistoryIcon />}
                  onClick={() => navigate(`/customers/${id}/history`)}
                  customerId={customer.id}
                  requiredPermission="view"
                >
                  عرض التاريخ الكامل
                </ProtectedButton>
                
                <ProtectedButton
                  variant="outlined"
                  startIcon={<AccountBalanceIcon />}
                  onClick={() => navigate(`/customers/${id}/statement`)}
                  customerId={customer.id}
                  requiredPermission="view"
                >
                  كشف حساب مفصل
                </ProtectedButton>
                
                <ProtectedButton
                  variant="outlined"
                  color="error"
                  startIcon={<DeleteIcon />}
                  onClick={() => setDeleteDialogOpen(true)}
                  customerId={customer.id}
                  requiredPermission="delete"
                >
                  حذف العميل
                </ProtectedButton>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* نافذة إضافة دفعة */}
      <Dialog open={paymentDialogOpen} onClose={() => setPaymentDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>إضافة دفعة جديدة</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="المبلغ"
                type="number"
                value={paymentData.amount}
                onChange={(e) => setPaymentData({ ...paymentData, amount: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>طريقة الدفع</InputLabel>
                <Select
                  value={paymentData.payment_method}
                  onChange={(e) => setPaymentData({ ...paymentData, payment_method: e.target.value })}
                >
                  <MenuItem value="cash">نقدي</MenuItem>
                  <MenuItem value="bank_transfer">تحويل بنكي</MenuItem>
                  <MenuItem value="check">شيك</MenuItem>
                  <MenuItem value="credit_card">بطاقة ائتمان</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="المرجع"
                value={paymentData.reference}
                onChange={(e) => setPaymentData({ ...paymentData, reference: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="تاريخ الدفع"
                type="date"
                value={paymentData.payment_date}
                onChange={(e) => setPaymentData({ ...paymentData, payment_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="ملاحظات"
                multiline
                rows={2}
                value={paymentData.notes}
                onChange={(e) => setPaymentData({ ...paymentData, notes: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPaymentDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handleAddPayment} variant="contained">إضافة</Button>
        </DialogActions>
      </Dialog>

      {/* نافذة تحديث الائتمان */}
      <Dialog open={creditDialogOpen} onClose={() => setCreditDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>تحديث حد الائتمان</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="حد الائتمان الجديد"
                type="number"
                value={creditData.credit_limit}
                onChange={(e) => setCreditData({ ...creditData, credit_limit: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="تاريخ التفعيل"
                type="date"
                value={creditData.effective_date}
                onChange={(e) => setCreditData({ ...creditData, effective_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="السبب"
                multiline
                rows={2}
                value={creditData.reason}
                onChange={(e) => setCreditData({ ...creditData, reason: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreditDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handleUpdateCredit} variant="contained">تحديث</Button>
        </DialogActions>
      </Dialog>

      {/* نافذة تأكيد الحذف */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>تأكيد الحذف</DialogTitle>
        <DialogContent>
          <Typography>
            هل أنت متأكد من حذف العميل "{customer.name}"؟
            هذا الإجراء لا يمكن التراجع عنه وسيؤثر على جميع الفواتير والمدفوعات المرتبطة.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handleDelete} color="error" variant="contained">حذف</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CustomerDetails;

