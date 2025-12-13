/**
 * Purchase Orders Management Page
 * صفحة إدارة أوامر الشراء
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Card,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Chip,
  IconButton,
  TextField,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  CheckCircle as ApproveIcon,
  LocalShipping as ReceiveIcon,
  Search as SearchIcon
} from '@mui/icons-material';
import purchaseService from '../services/purchaseService';

const PurchaseOrdersManagement = () => {
  const [purchaseOrders, setPurchaseOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    status: '',
    search: ''
  });
  const [selectedPO, setSelectedPO] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogType, setDialogType] = useState(''); // view, create, edit, receive

  useEffect(() => {
    loadPurchaseOrders();
  }, [filters]);

  const loadPurchaseOrders = async () => {
    try {
      setLoading(true);
      const response = await purchaseService.getPurchaseOrders(filters);
      
      if (response.success) {
        setPurchaseOrders(response.data);
      }
    } catch (err) {
      setError(err.message || 'فشل في تحميل أوامر الشراء');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  const handleView = async (poId) => {
    try {
      const response = await purchaseService.getPurchaseOrder(poId);
      if (response.success) {
        setSelectedPO(response.data);
        setDialogType('view');
        setDialogOpen(true);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreate = () => {
    setSelectedPO(null);
    setDialogType('create');
    setDialogOpen(true);
  };

  const handleEdit = async (poId) => {
    try {
      const response = await purchaseService.getPurchaseOrder(poId);
      if (response.success) {
        setSelectedPO(response.data);
        setDialogType('edit');
        setDialogOpen(true);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (poId) => {
    if (!window.confirm('هل أنت متأكد من حذف أمر الشراء؟')) return;

    try {
      const response = await purchaseService.deletePurchaseOrder(poId);
      if (response.success) {
        loadPurchaseOrders();
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleApprove = async (poId) => {
    if (!window.confirm('هل أنت متأكد من اعتماد أمر الشراء؟')) return;

    try {
      const response = await purchaseService.approvePurchaseOrder(poId);
      if (response.success) {
        loadPurchaseOrders();
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleReceive = async (poId) => {
    try {
      const response = await purchaseService.getPurchaseOrder(poId);
      if (response.success) {
        setSelectedPO(response.data);
        setDialogType('receive');
        setDialogOpen(true);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'draft': 'default',
      'pending': 'warning',
      'approved': 'info',
      'ordered': 'primary',
      'partial': 'secondary',
      'received': 'success',
      'cancelled': 'error'
    };
    return colors[status] || 'default';
  };

  const getStatusLabel = (status) => {
    const labels = {
      'draft': 'مسودة',
      'pending': 'معلق',
      'approved': 'معتمد',
      'ordered': 'تم الطلب',
      'partial': 'استلام جزئي',
      'received': 'مستلم',
      'cancelled': 'ملغي'
    };
    return labels[status] || status;
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">إدارة أوامر الشراء</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleCreate}
        >
          أمر شراء جديد
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 3, p: 2 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="بحث"
              placeholder="رقم أمر الشراء أو ملاحظات..."
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              InputProps={{
                endAdornment: <SearchIcon />
              }}
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              select
              label="الحالة"
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
            >
              <MenuItem value="">الكل</MenuItem>
              <MenuItem value="draft">مسودة</MenuItem>
              <MenuItem value="pending">معلق</MenuItem>
              <MenuItem value="approved">معتمد</MenuItem>
              <MenuItem value="ordered">تم الطلب</MenuItem>
              <MenuItem value="partial">استلام جزئي</MenuItem>
              <MenuItem value="received">مستلم</MenuItem>
              <MenuItem value="cancelled">ملغي</MenuItem>
            </TextField>
          </Grid>
        </Grid>
      </Card>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>رقم الأمر</TableCell>
              <TableCell>المورد</TableCell>
              <TableCell>تاريخ الطلب</TableCell>
              <TableCell>التاريخ المتوقع</TableCell>
              <TableCell>الإجمالي</TableCell>
              <TableCell>الحالة</TableCell>
              <TableCell align="center">الإجراءات</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {purchaseOrders.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  <Typography variant="body2" color="textSecondary">
                    لا توجد أوامر شراء
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              purchaseOrders.map((po) => (
                <TableRow key={po.id} hover>
                  <TableCell>{po.po_number}</TableCell>
                  <TableCell>{po.supplier_name || `مورد #${po.supplier_id}`}</TableCell>
                  <TableCell>{new Date(po.order_date).toLocaleDateString('ar-EG')}</TableCell>
                  <TableCell>
                    {po.expected_date ? new Date(po.expected_date).toLocaleDateString('ar-EG') : '-'}
                  </TableCell>
                  <TableCell>{parseFloat(po.total_amount || 0).toFixed(2)} ج.م</TableCell>
                  <TableCell>
                    <Chip
                      label={getStatusLabel(po.status)}
                      color={getStatusColor(po.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton size="small" onClick={() => handleView(po.id)} title="عرض">
                      <ViewIcon fontSize="small" />
                    </IconButton>
                    
                    {(po.status === 'draft' || po.status === 'pending') && (
                      <IconButton size="small" onClick={() => handleEdit(po.id)} title="تعديل">
                        <EditIcon fontSize="small" />
                      </IconButton>
                    )}
                    
                    {po.status === 'pending' && (
                      <IconButton size="small" onClick={() => handleApprove(po.id)} title="اعتماد" color="primary">
                        <ApproveIcon fontSize="small" />
                      </IconButton>
                    )}
                    
                    {(po.status === 'approved' || po.status === 'ordered' || po.status === 'partial') && (
                      <IconButton size="small" onClick={() => handleReceive(po.id)} title="استلام" color="success">
                        <ReceiveIcon fontSize="small" />
                      </IconButton>
                    )}
                    
                    {(po.status === 'draft' || po.status === 'cancelled') && (
                      <IconButton size="small" onClick={() => handleDelete(po.id)} title="حذف" color="error">
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    )}
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Dialogs will be implemented in separate components */}
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {dialogType === 'view' && 'عرض أمر الشراء'}
          {dialogType === 'create' && 'أمر شراء جديد'}
          {dialogType === 'edit' && 'تعديل أمر الشراء'}
          {dialogType === 'receive' && 'استلام أمر الشراء'}
        </DialogTitle>
        <DialogContent>
          {selectedPO && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2">
                رقم الأمر: {selectedPO.po_number}
              </Typography>
              <Typography variant="body2">
                الحالة: {getStatusLabel(selectedPO.status)}
              </Typography>
              <Typography variant="body2">
                الإجمالي: {parseFloat(selectedPO.total_amount || 0).toFixed(2)} ج.م
              </Typography>
              {/* Add more details here */}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>إغلاق</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PurchaseOrdersManagement;
