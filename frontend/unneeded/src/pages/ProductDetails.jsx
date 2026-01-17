/**
 * صفحة تفاصيل المنتج
 * /home/ubuntu/upload/store_v1.1/complete_inventory_system/frontend/src/pages/ProductDetails.js
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { usePermissions } from '../contexts/PermissionContext';
import productService from '../services/productService';

const ProductDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { canAccessWarehouse } = usePermissions();

  // ==================== State Management ====================
  
  const [product, setProduct] = useState(null);
  const [stockHistory, setStockHistory] = useState([]);
  const [priceHistory, setPriceHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // حالات النوافذ المنبثقة
  const [stockDialogOpen, setStockDialogOpen] = useState(false);
  const [priceDialogOpen, setPriceDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  
  // بيانات النماذج
  const [stockUpdate, setStockUpdate] = useState({
    quantity: '',
    type: 'add', // add, remove, set
    reason: '',
    warehouse_id: ''
  });
  
  const [priceUpdate, setPriceUpdate] = useState({
    new_price: '',
    reason: '',
    effective_date: new Date().toISOString().split('T')[0]
  });

  // ==================== Data Loading ====================

  useEffect(() => {
    if (id) {
      loadProductData();
    }
  }, [id]);

  const loadProductData = async () => {
    try {
      setLoading(true);
      setError(null);

      // تحميل بيانات المنتج
      const productData = await productService.getById(id);
      setProduct(productData);

      // تحميل تاريخ المخزون والأسعار بشكل متوازي
      const [stockHistoryData, priceHistoryData] = await Promise.allSettled([
        productService.getStockHistory(id, { limit: 10 }),
        productService.getPriceHistory(id, { limit: 10 })
      ]);

      if (stockHistoryData.status === 'fulfilled') {
        setStockHistory(stockHistoryData.value);
      }

      if (priceHistoryData.status === 'fulfilled') {
        setPriceHistory(priceHistoryData.value);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // ==================== Event Handlers ====================

  const handleStockUpdate = async () => {
    try {
      await productService.updateStock(id, stockUpdate);
      setStockDialogOpen(false);
      setStockUpdate({ quantity: '', type: 'add', reason: '', warehouse_id: '' });
      await loadProductData(); // إعادة تحميل البيانات
    } catch (error) {
      alert(`خطأ في تحديث المخزون: ${error.message}`);
    }
  };

  const handlePriceUpdate = async () => {
    try {
      await productService.updatePrice(id, priceUpdate);
      setPriceDialogOpen(false);
      setPriceUpdate({ new_price: '', reason: '', effective_date: new Date().toISOString().split('T')[0] });
      await loadProductData(); // إعادة تحميل البيانات
    } catch (error) {
      alert(`خطأ في تحديث السعر: ${error.message}`);
    }
  };

  const handleDelete = async () => {
    try {
      await productService.delete(id);
      setDeleteDialogOpen(false);
      navigate('/products');
    } catch (error) {
      alert(`خطأ في حذف المنتج: ${error.message}`);
    }
  };

  // ==================== Render Functions ====================

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>
          جاري تحميل بيانات المنتج...
        </Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        خطأ في تحميل المنتج: {error}
      </Alert>
    );
  }

  if (!product) {
    return (
      <Alert severity="warning" sx={{ m: 2 }}>
        المنتج غير موجود
      </Alert>
    );
  }

  const getStockStatusColor = (quantity, minStock) => {
    if (quantity <= 0) return 'error';
    if (quantity <= minStock) return 'warning';
    return 'success';
  };

  const getStockStatusText = (quantity, minStock) => {
    if (quantity <= 0) return 'نفد المخزون';
    if (quantity <= minStock) return 'مخزون منخفض';
    return 'متوفر';
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box display="flex" justifyContent="between" alignItems="center" mb={3}>
        <Box display="flex" alignItems="center">
          <IconButton onClick={() => navigate('/products')} sx={{ mr: 1 }}>
            <ArrowBackIcon />
          </IconButton>
          <Typography variant="h4" component="h1">
            تفاصيل المنتج
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
            onClick={() => navigator.share?.({ title: product.name, url: window.location.href })}
          >
            مشاركة
          </ProtectedButton>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* معلومات المنتج الأساسية */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <InventoryIcon />
                </Avatar>
                <Box>
                  <Typography variant="h5" component="h2">
                    {product.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {product.category_name || 'غير محدد'}
                  </Typography>
                </Box>
              </Box>

              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">الباركود</Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {product.barcode || 'غير محدد'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">الوحدة</Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {product.unit || 'قطعة'}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">السعر</Typography>
                  <Typography variant="h6" color="primary">
                    {product.price?.toLocaleString()} ج.م
                  </Typography>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">حالة المخزون</Typography>
                  <Chip
                    label={getStockStatusText(product.stock_quantity, product.min_stock_level)}
                    color={getStockStatusColor(product.stock_quantity, product.min_stock_level)}
                    size="small"
                  />
                </Grid>
                
                <Grid item xs={12}>
                  <Typography variant="body2" color="text.secondary">الوصف</Typography>
                  <Typography variant="body1">
                    {product.description || 'لا يوجد وصف'}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* إحصائيات المخزون */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                إحصائيات المخزون
              </Typography>
              
              <Box mb={2}>
                <Typography variant="body2" color="text.secondary">الكمية الحالية</Typography>
                <Typography variant="h4" color="primary">
                  {product.stock_quantity || 0}
                </Typography>
              </Box>
              
              <Box mb={2}>
                <Typography variant="body2" color="text.secondary">الحد الأدنى</Typography>
                <Typography variant="h6">
                  {product.min_stock_level || 0}
                </Typography>
              </Box>
              
              <Box mb={2}>
                <Typography variant="body2" color="text.secondary">الحد الأقصى</Typography>
                <Typography variant="h6">
                  {product.max_stock_level || 'غير محدد'}
                </Typography>
              </Box>

              <Divider sx={{ my: 2 }} />

              <ProtectedComponent
                warehouseId={product.warehouse_id}
                requiredPermission="manage_stock"
              >
                <Box display="flex" gap={1} mb={1}>
                  <ProtectedButton
                    variant="contained"
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={() => setStockDialogOpen(true)}
                    fullWidth
                  >
                    تحديث المخزون
                  </ProtectedButton>
                </Box>
              </ProtectedComponent>

              <ProtectedComponent
                warehouseId={product.warehouse_id}
                requiredPermission="edit_prices"
              >
                <ProtectedButton
                  variant="outlined"
                  size="small"
                  startIcon={<TrendingUpIcon />}
                  onClick={() => setPriceDialogOpen(true)}
                  fullWidth
                >
                  تحديث السعر
                </ProtectedButton>
              </ProtectedComponent>
            </CardContent>
          </Card>
        </Grid>

        {/* تاريخ حركات المخزون */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                آخر حركات المخزون
              </Typography>
              
              {stockHistory.length > 0 ? (
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>التاريخ</TableCell>
                        <TableCell>النوع</TableCell>
                        <TableCell>الكمية</TableCell>
                        <TableCell>السبب</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {stockHistory.map((movement, index) => (
                        <TableRow key={index}>
                          <TableCell>
                            {new Date(movement.created_at).toLocaleDateString('ar-EG')}
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={movement.movement_type}
                              color={movement.movement_type === 'in' ? 'success' : 'error'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{movement.quantity}</TableCell>
                          <TableCell>{movement.reason || '-'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  لا توجد حركات مخزون
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* تاريخ الأسعار */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                تاريخ الأسعار
              </Typography>
              
              {priceHistory.length > 0 ? (
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>التاريخ</TableCell>
                        <TableCell>السعر القديم</TableCell>
                        <TableCell>السعر الجديد</TableCell>
                        <TableCell>السبب</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {priceHistory.map((price, index) => (
                        <TableRow key={index}>
                          <TableCell>
                            {new Date(price.effective_date).toLocaleDateString('ar-EG')}
                          </TableCell>
                          <TableCell>{price.old_price}</TableCell>
                          <TableCell>{price.new_price}</TableCell>
                          <TableCell>{price.reason || '-'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  لا يوجد تاريخ أسعار
                </Typography>
              )}
            </CardContent>
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
                  onClick={() => navigate(`/products/${id}/edit`)}
                  warehouseId={product.warehouse_id}
                  requiredPermission="edit"
                >
                  تعديل المنتج
                </ProtectedButton>
                
                <ProtectedButton
                  variant="outlined"
                  startIcon={<HistoryIcon />}
                  onClick={() => navigate(`/products/${id}/history`)}
                  warehouseId={product.warehouse_id}
                  requiredPermission="view"
                >
                  عرض التاريخ الكامل
                </ProtectedButton>
                
                <ProtectedButton
                  variant="outlined"
                  color="error"
                  startIcon={<DeleteIcon />}
                  onClick={() => setDeleteDialogOpen(true)}
                  warehouseId={product.warehouse_id}
                  requiredPermission="delete"
                >
                  حذف المنتج
                </ProtectedButton>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* نافذة تحديث المخزون */}
      <Dialog open={stockDialogOpen} onClose={() => setStockDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>تحديث المخزون</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>نوع العملية</InputLabel>
                <Select
                  value={stockUpdate.type}
                  onChange={(e) => setStockUpdate({ ...stockUpdate, type: e.target.value })}
                >
                  <MenuItem value="add">إضافة</MenuItem>
                  <MenuItem value="remove">خصم</MenuItem>
                  <MenuItem value="set">تعيين</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="الكمية"
                type="number"
                value={stockUpdate.quantity}
                onChange={(e) => setStockUpdate({ ...stockUpdate, quantity: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="السبب"
                multiline
                rows={2}
                value={stockUpdate.reason}
                onChange={(e) => setStockUpdate({ ...stockUpdate, reason: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setStockDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handleStockUpdate} variant="contained">تحديث</Button>
        </DialogActions>
      </Dialog>

      {/* نافذة تحديث السعر */}
      <Dialog open={priceDialogOpen} onClose={() => setPriceDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>تحديث السعر</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="السعر الجديد"
                type="number"
                value={priceUpdate.new_price}
                onChange={(e) => setPriceUpdate({ ...priceUpdate, new_price: e.target.value })}
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="تاريخ التفعيل"
                type="date"
                value={priceUpdate.effective_date}
                onChange={(e) => setPriceUpdate({ ...priceUpdate, effective_date: e.target.value })}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="السبب"
                multiline
                rows={2}
                value={priceUpdate.reason}
                onChange={(e) => setPriceUpdate({ ...priceUpdate, reason: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPriceDialogOpen(false)}>إلغاء</Button>
          <Button onClick={handlePriceUpdate} variant="contained">تحديث</Button>
        </DialogActions>
      </Dialog>

      {/* نافذة تأكيد الحذف */}
      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>تأكيد الحذف</DialogTitle>
        <DialogContent>
          <Typography>
            هل أنت متأكد من حذف المنتج "{product.name}"؟
            هذا الإجراء لا يمكن التراجع عنه.
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

export default ProductDetails;

