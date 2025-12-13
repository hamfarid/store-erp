/**
 * Purchase Receipt Form Component
 * مكون نموذج استلام أمر الشراء
 */

import React, { useState } from 'react';
import {
  Box,
  Grid,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Alert
} from '@mui/material';

const PurchaseReceiptForm = ({ purchaseOrder, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    receipt_date: new Date().toISOString().split('T')[0],
    warehouse_id: purchaseOrder?.warehouse_id || '',
    notes: '',
    delivery_notes: '',
    quality_notes: '',
    driver_name: '',
    vehicle_number: '',
    delivery_company: '',
    items: purchaseOrder?.items?.map(item => ({
      ...item,
      received_quantity: item.quantity - (item.received_quantity || 0),
      batch_number: '',
      manufacture_date: '',
      expiry_date: ''
    })) || []
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleItemChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate
    const hasReceivedItems = formData.items.some(item => item.received_quantity > 0);
    if (!hasReceivedItems) {
      alert('يجب استلام كمية واحدة على الأقل');
      return;
    }

    onSubmit({
      ...formData,
      po_id: purchaseOrder.id
    });
  };

  const getRemainingQuantity = (item) => {
    return item.quantity - (item.received_quantity || 0);
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Alert severity="info" sx={{ mb: 2 }}>
        أمر الشراء: {purchaseOrder?.po_number}
      </Alert>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            type="date"
            label="تاريخ الاستلام"
            value={formData.receipt_date}
            onChange={(e) => handleChange('receipt_date', e.target.value)}
            InputLabelProps={{ shrink: true }}
            required
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="اسم السائق"
            value={formData.driver_name}
            onChange={(e) => handleChange('driver_name', e.target.value)}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="رقم المركبة"
            value={formData.vehicle_number}
            onChange={(e) => handleChange('vehicle_number', e.target.value)}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="شركة التوصيل"
            value={formData.delivery_company}
            onChange={(e) => handleChange('delivery_company', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="ملاحظات التوصيل"
            value={formData.delivery_notes}
            onChange={(e) => handleChange('delivery_notes', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="ملاحظات الجودة"
            value={formData.quality_notes}
            onChange={(e) => handleChange('quality_notes', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <Typography variant="h6" sx={{ mb: 2 }}>العناصر المستلمة</Typography>

          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>المنتج</TableCell>
                  <TableCell>الكمية المطلوبة</TableCell>
                  <TableCell>المستلم سابقاً</TableCell>
                  <TableCell>المتبقي</TableCell>
                  <TableCell>الكمية المستلمة</TableCell>
                  <TableCell>رقم اللوط</TableCell>
                  <TableCell>تاريخ الإنتاج</TableCell>
                  <TableCell>تاريخ الانتهاء</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {formData.items.map((item, index) => (
                  <TableRow key={index}>
                    <TableCell>{item.product_name || `منتج #${item.product_id}`}</TableCell>
                    <TableCell>{item.quantity}</TableCell>
                    <TableCell>{item.received_quantity || 0}</TableCell>
                    <TableCell>{getRemainingQuantity(item)}</TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        type="number"
                        value={item.received_quantity}
                        onChange={(e) => handleItemChange(index, 'received_quantity', parseFloat(e.target.value) || 0)}
                        inputProps={{
                          min: 0,
                          max: getRemainingQuantity(item),
                          step: 0.001
                        }}
                        sx={{ width: 100 }}
                      />
                    </TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        value={item.batch_number}
                        onChange={(e) => handleItemChange(index, 'batch_number', e.target.value)}
                        placeholder="اختياري"
                        sx={{ width: 120 }}
                      />
                    </TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        type="date"
                        value={item.manufacture_date}
                        onChange={(e) => handleItemChange(index, 'manufacture_date', e.target.value)}
                        InputLabelProps={{ shrink: true }}
                        sx={{ width: 150 }}
                      />
                    </TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        type="date"
                        value={item.expiry_date}
                        onChange={(e) => handleItemChange(index, 'expiry_date', e.target.value)}
                        InputLabelProps={{ shrink: true }}
                        sx={{ width: 150 }}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="ملاحظات عامة"
            value={formData.notes}
            onChange={(e) => handleChange('notes', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button variant="outlined" onClick={onCancel}>
              إلغاء
            </Button>
            <Button type="submit" variant="contained" color="success">
              تأكيد الاستلام
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PurchaseReceiptForm;
