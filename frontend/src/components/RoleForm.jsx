/**
 * Role Form Component
 * مكون نموذج الدور
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  TextField,
  Button,
  FormControlLabel,
  Switch
} from '@mui/material';

const RoleForm = ({ initialData, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    code: '',
    name: '',
    name_ar: '',
    description: '',
    description_ar: '',
    color: '#1976d2',
    icon: 'security',
    is_active: true
  });

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="الكود"
            value={formData.code}
            onChange={(e) => handleChange('code', e.target.value)}
            required
            disabled={!!initialData}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="اللون"
            type="color"
            value={formData.color}
            onChange={(e) => handleChange('color', e.target.value)}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="الاسم (EN)"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            required
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="الاسم (AR)"
            value={formData.name_ar}
            onChange={(e) => handleChange('name_ar', e.target.value)}
            required
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="الوصف (EN)"
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="الوصف (AR)"
            value={formData.description_ar}
            onChange={(e) => handleChange('description_ar', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={formData.is_active}
                onChange={(e) => handleChange('is_active', e.target.checked)}
              />
            }
            label="نشط"
          />
        </Grid>

        <Grid item xs={12}>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
            <Button variant="outlined" onClick={onCancel}>
              إلغاء
            </Button>
            <Button type="submit" variant="contained">
              حفظ
            </Button>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default RoleForm;
