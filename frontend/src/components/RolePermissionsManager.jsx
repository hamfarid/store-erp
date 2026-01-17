/**
 * Role Permissions Manager Component
 * مكون إدارة أذونات الدور
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Checkbox,
  FormControlLabel,
  FormGroup,
  Paper,
  Button,
  Divider
} from '@mui/material';
import permissionService from '../services/permissionService';

const RolePermissionsManager = ({ role, onSubmit, onCancel }) => {
  const [permissions, setPermissions] = useState({});
  const [selectedPermissions, setSelectedPermissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPermissions();
  }, [role]);

  const loadPermissions = async () => {
    try {
      setLoading(true);
      const response = await permissionService.getPermissionsGrouped();
      
      if (response.success) {
        setPermissions(response.data);
      }

      // Load current role permissions
      if (role && role.permissions) {
        try {
          const rolePerms = JSON.parse(role.permissions);
          setSelectedPermissions(Array.isArray(rolePerms) ? rolePerms : []);
        } catch {
          setSelectedPermissions([]);
        }
      }
    } catch (err) {
      console.error('Failed to load permissions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePermissionToggle = (permissionCode) => {
    setSelectedPermissions(prev => {
      if (prev.includes(permissionCode)) {
        return prev.filter(p => p !== permissionCode);
      } else {
        return [...prev, permissionCode];
      }
    });
  };

  const handleCategoryToggle = (category, perms) => {
    const categoryPerms = perms.map(p => p.code);
    const allSelected = categoryPerms.every(p => selectedPermissions.includes(p));

    if (allSelected) {
      // Deselect all
      setSelectedPermissions(prev => prev.filter(p => !categoryPerms.includes(p)));
    } else {
      // Select all
      setSelectedPermissions(prev => {
        const newPerms = [...prev];
        categoryPerms.forEach(p => {
          if (!newPerms.includes(p)) {
            newPerms.push(p);
          }
        });
        return newPerms;
      });
    }
  };

  const isCategorySelected = (perms) => {
    const categoryPerms = perms.map(p => p.code);
    return categoryPerms.every(p => selectedPermissions.includes(p));
  };

  const isCategoryPartiallySelected = (perms) => {
    const categoryPerms = perms.map(p => p.code);
    const selectedCount = categoryPerms.filter(p => selectedPermissions.includes(p)).length;
    return selectedCount > 0 && selectedCount < categoryPerms.length;
  };

  const handleSubmit = () => {
    onSubmit({
      role_id: role.id,
      permissions: selectedPermissions
    });
  };

  if (loading) {
    return <Typography>جاري التحميل...</Typography>;
  }

  return (
    <Box>
      <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
        اختر الأذونات للدور: <strong>{role?.name}</strong>
      </Typography>

      <Typography variant="body2" sx={{ mb: 2 }}>
        الأذونات المحددة: {selectedPermissions.length}
      </Typography>

      <Divider sx={{ mb: 2 }} />

      <Grid container spacing={2}>
        {Object.entries(permissions).map(([category, perms]) => (
          <Grid item xs={12} md={6} key={category}>
            <Paper sx={{ p: 2 }}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={isCategorySelected(perms)}
                    indeterminate={isCategoryPartiallySelected(perms)}
                    onChange={() => handleCategoryToggle(category, perms)}
                  />
                }
                label={
                  <Typography variant="subtitle1" fontWeight="bold">
                    {category}
                  </Typography>
                }
              />
              
              <FormGroup sx={{ ml: 3 }}>
                {perms.map((perm) => (
                  <FormControlLabel
                    key={perm.code}
                    control={
                      <Checkbox
                        checked={selectedPermissions.includes(perm.code)}
                        onChange={() => handlePermissionToggle(perm.code)}
                        size="small"
                      />
                    }
                    label={
                      <Typography variant="body2">
                        {perm.name}
                      </Typography>
                    }
                  />
                ))}
              </FormGroup>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end', mt: 3 }}>
        <Button variant="outlined" onClick={onCancel}>
          إلغاء
        </Button>
        <Button variant="contained" onClick={handleSubmit}>
          حفظ الأذونات
        </Button>
      </Box>
    </Box>
  );
};

export default RolePermissionsManager;
