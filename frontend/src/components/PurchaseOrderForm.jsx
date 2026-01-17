/**
 * Purchase Order Form Component
 * مكون نموذج أمر الشراء
 */

import React, { useState, useEffect } from 'react';
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
  IconButton,
  Autocomplete,
  Typography
} from '@mui/material';
import {
  Add as AddIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';

const PurchaseOrderForm = ({ initialData, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    supplier_id: '',
    warehouse_id: '',
    order_date: new Date().toISOString().split('T')[0],
    expected_date: '',
    notes: '',
    terms: '',
    items: []
  });

  const [suppliers, setSuppliers] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [products, setProducts] = useState([]);

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
    // Load suppliers, warehouses, products
    loadData();
  }, [initialData]);

  const loadData = async () => {
    // TODO: Load from API
    setSuppliers([
      { id: 1, name: 'مورد 1' },
      { id: 2, name: 'مورد 2' }
    ]);
    setWarehouses([
      { id: 1, name: 'المخزن الرئيسي' },
      { id: 2, name: 'مخزن الفرع' }
    ]);
    setProducts([
      { id: 1, name: 'منتج 1', unit_price: 100 },
      { id: 2, name: 'منتج 2', unit_price: 200 }
    ]);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleAddItem = () => {
    setFormData(prev => ({
      ...prev,
      items: [
        ...prev.items,
        {
          product_id: '',
          quantity: 1,
          unit_price: 0,
          discount_percentage: 0,
          tax_percentage: 14,
          notes: ''
        }
      ]
    }));
  };

  const handleRemoveItem = (index) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index)
    }));
  };

  const handleItemChange = (index, field, value) => {
    setFormData(prev => ({
      ...prev,
      items: prev.items.map((item, i) => 
        i === index ? { ...item, [field]: value } : item
      )
    }));
  };

  const calculateItemTotal = (item) => {
    const subtotal = item.quantity * item.unit_price;
    const discount = subtotal * (item.discount_percentage / 100);
    const afterDiscount = subtotal - discount;
    const tax = afterDiscount * (item.tax_percentage / 100);
    return afterDiscount + tax;
  };

  const calculateTotal = () => {
    return formData.items.reduce((sum, item) => sum + calculateItemTotal(item), 0);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Autocomplete
            options={suppliers}
            getOptionLabel={(option) => option.name}
            value={suppliers.find(s => s.id === formData.supplier_id) || null}
            onChange={(e, newValue) => handleChange('supplier_id', newValue?.id || '')}
            renderInput={(params) => (
              <TextField {...params} label="المورد" required />
            )}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <Autocomplete
            options={warehouses}
            getOptionLabel={(option) => option.name}
            value={warehouses.find(w => w.id === formData.warehouse_id) || null}
            onChange={(e, newValue) => handleChange('warehouse_id', newValue?.id || '')}
            renderInput={(params) => (
              <TextField {...params} label="المخزن" />
            )}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            type="date"
            label="تاريخ الطلب"
            value={formData.order_date}
            onChange={(e) => handleChange('order_date', e.target.value)}
            InputLabelProps={{ shrink: true }}
            required
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            type="date"
            label="التاريخ المتوقع"
            value={formData.expected_date}
            onChange={(e) => handleChange('expected_date', e.target.value)}
            InputLabelProps={{ shrink: true }}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="ملاحظات"
            value={formData.notes}
            onChange={(e) => handleChange('notes', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="الشروط والأحكام"
            value={formData.terms}
            onChange={(e) => handleChange('terms', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">العناصر</Typography>
            <Button
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={handleAddItem}
            >
              إضافة عنصر
            </Button>
          </Box>

          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>المنتج</TableCell>
                  <TableCell>الكمية</TableCell>
                  <TableCell>السعر</TableCell>
                  <TableCell>الخصم %</TableCell>
                  <TableCell>الضريبة %</TableCell>
                  <TableCell>الإجمالي</TableCell>
                  <TableCell></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {formData.items.map((item, index) => (
                  <TableRow key={index}>
                    <TableCell>
                      <Autocomplete
                        size="small"
                        options={products}
                        getOptionLabel={(option) => option.name}
                        value={products.find(p => p.id === item.product_id) || null}
                        onChange={(e, newValue) => {
                          handleItemChange(index, 'product_id', newValue?.id || '');
                          if (newValue) {
                            handleItemChange(index, 'unit_price', newValue.unit_price);
                          }
                        }}
                        renderInput={(params) => (
                          <TextField {...params} size="small" />
                        )}
                        sx={{ minWidth: 200 }}
                      />
                    </TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        type="number"
                        value={item.quantity}
                        onChange={(e) => handleItemChange(index, 'quantity', parseFloat(e.target.value) || 0)}
                        sx={{ width: 80 }}
                      />
                    </TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        type="number"
                        value={item.unit_price}
                        onChange={(e) => handleItemChange(index, 'unit_price', parseFloat(e.target.value) || 0)}
                        sx={{ width: 100 }}
                      />
                    </TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        type="number"
                        value={item.discount_percentage}
                        onChange={(e) => handleItemChange(index, 'discount_percentage', parseFloat(e.target.value) || 0)}
                        sx={{ width: 70 }}
                      />
                    </TableCell>
                    <TableCell>
                      <TextField
                        size="small"
                        type="number"
                        value={item.tax_percentage}
                        onChange={(e) => handleItemChange(index, 'tax_percentage', parseFloat(e.target.value) || 0)}
                        sx={{ width: 70 }}
                      />
                    </TableCell>
                    <TableCell>
                      {calculateItemTotal(item).toFixed(2)}
                    </TableCell>
                    <TableCell>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleRemoveItem(index)}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
            <Typography variant="h6">
              الإجمالي: {calculateTotal().toFixed(2)} ج.م
            </Typography>
          </Box>
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button variant="outlined" onClick={onCancel}>
              إلغاء
            </Button>
            <Button
              type="submit"
              variant="contained"
              disabled={!formData.supplier_id || formData.items.length === 0}
            >
              حفظ
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PurchaseOrderForm;
